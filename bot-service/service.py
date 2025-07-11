"""
Service layer for expense processing business logic.
"""

import re
import json
import logging
from typing import Dict, Any, Optional, List

from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

from constants import (
    OLLAMA_CONFIG, 
    EXPENSE_ANALYSIS_PROMPT, 
    MESSAGES, 
    ERROR_MESSAGES, 
    LOG_MESSAGES,
    EXPENSE_CATEGORIES
)
from repository import ExpenseRepository

logger = logging.getLogger(__name__)

class ExpenseService:
    """Service for expense processing and analysis."""
    
    def __init__(self, database_url: str):
        """
        Initialize the expense service.
        
        Args:
            database_url (str): Database connection string.
        """
        self.repository = ExpenseRepository(database_url)
        self.llm = ChatOllama(
            model=OLLAMA_CONFIG["MODEL"],
            base_url=OLLAMA_CONFIG["BASE_URL"],
            temperature=OLLAMA_CONFIG["TEMPERATURE"]
        )
    
    def is_user_authorized(self, telegram_id: str) -> bool:
        """
        Check if a user is authorized to use the bot.
        
        Args:
            telegram_id (str): Telegram user ID.
            
        Returns:
            bool: True if user is authorized, False otherwise.
        """
        return self.repository.is_user_whitelisted(telegram_id)
    
    async def analyze_expense_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze a message to determine if it contains expense information.
        
        Args:
            message (str): The user's message to analyze.
            
        Returns:
            Dict[str, Any]: Analysis result with keys is_expense, description, amount, category.
        """
        # Create a structured prompt for expense analysis
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", EXPENSE_ANALYSIS_PROMPT),
            ("human", "{message}")
        ])
        
        try:
            # Get response from LLM
            messages = prompt_template.format_messages(message=message)
            response = await self.llm.ainvoke(messages)
            
            # Parse the response
            content = response.content
            logger.info(LOG_MESSAGES["LLM_RESPONSE"].format(content="[LLM_RESPONSE_HIDDEN]"))
            
            # Extract the first valid JSON block using regex
            json_match = re.search(r'\{[\s\S]*?\}', content)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = content.strip()
            
            result = json.loads(json_str)
            logger.info(LOG_MESSAGES["PARSED_RESULT"].format(result=result))
            
            # Validate the response
            if not result.get("is_expense", False):
                logger.info(LOG_MESSAGES["MESSAGE_NON_EXPENSE"].format(message=message))
                return {"is_expense": False}
            
            # Additional validation for expense data
            description = result.get("description")
            amount = result.get("amount")
            
            if not description or not amount or amount <= 0:
                logger.warning(ERROR_MESSAGES["INVALID_EXPENSE_RESPONSE"].format(result=result))
                return {"is_expense": False}
            
            return {
                "is_expense": True,
                "description": description,
                "amount": float(amount),
                "category": result.get("category", "Other")
            }
            
        except Exception as e:
            logger.error(ERROR_MESSAGES["LLM_ANALYSIS_ERROR"].format(error=e))
            # Always return a valid result even if there is an error
            return {"is_expense": False}
    
    async def process_expense(self, telegram_id: str, message: str) -> Dict[str, Any]:
        """
        Process an expense message and save it to the database.
        
        Args:
            telegram_id (str): Telegram user ID.
            message (str): User message to process.
            
        Returns:
            Dict[str, Any]: Processing result with success status and message.
        """
        logger.info(LOG_MESSAGES["PROCESSING_EXPENSE"].format(telegram_id=telegram_id))
        
        # Check if user is authorized
        if not self.is_user_authorized(telegram_id):
            logger.warning(LOG_MESSAGES["UNAUTHORIZED_ATTEMPT"].format(telegram_id=telegram_id))
            return {
                "success": False,
                "message": MESSAGES["UNAUTHORIZED_USER"]
            }
        
        # Analyze the message
        analysis = await self.analyze_expense_message(message)
        
        if not analysis.get("is_expense", False):
            logger.info(LOG_MESSAGES["NON_EXPENSE_MESSAGE"].format(
                telegram_id=telegram_id, 
                message=message
            ))
            return {
                "success": False,
                "message": MESSAGES["NON_EXPENSE_MESSAGE"]
            }
        
        # Extract expense details
        description = analysis.get("description")
        amount = analysis.get("amount", 0)
        category = analysis.get("category", "Other")
        
        # Validate extracted data
        if not description or amount <= 0:
            logger.error(ERROR_MESSAGES["INVALID_EXPENSE_DATA"].format(analysis=analysis))
            return {
                "success": False,
                "message": MESSAGES["INVALID_EXPENSE_DATA"]
            }
        
        # Save to database
        if self.repository.save_expense(telegram_id, description, amount, category):
            return {
                "success": True,
                "category": category,
                "description": description,
                "amount": amount,
                "message": MESSAGES["EXPENSE_ADDED"].format(category=category)
            }
        else:
            logger.error(ERROR_MESSAGES["FAILED_TO_SAVE"].format(telegram_id=telegram_id))
            return {
                "success": False,
                "message": MESSAGES["DATABASE_SAVE_ERROR"]
            }
    
    def get_user_expenses(self, telegram_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent expenses for a user.
        
        Args:
            telegram_id (str): Telegram user ID.
            limit (int): Maximum number of expenses to return.
            
        Returns:
            List[Dict[str, Any]]: List of expense dictionaries.
        """
        return self.repository.get_user_expenses(telegram_id, limit)
    
    def get_expense_stats(self, telegram_id: str) -> Dict[str, Any]:
        """
        Get expense statistics for a user.
        
        Args:
            telegram_id (str): Telegram user ID.
            
        Returns:
            Dict[str, Any]: Statistics including total amount and category breakdown.
        """
        return self.repository.get_expense_stats(telegram_id)
    
    def get_categories(self) -> List[str]:
        """
        Get available expense categories.
        
        Returns:
            List[str]: List of available categories.
        """
        return EXPENSE_CATEGORIES 