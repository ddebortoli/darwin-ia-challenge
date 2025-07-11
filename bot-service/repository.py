"""
Repository pattern implementation for database operations.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from constants import QUERIES, ERROR_MESSAGES, LOG_MESSAGES

logger = logging.getLogger(__name__)

class ExpenseRepository:
    """Repository for expense-related database operations."""
    
    def __init__(self, database_url: str):
        """
        Initialize the repository with database connection.
        
        Args:
            database_url (str): Database connection string.
        """
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def is_user_whitelisted(self, telegram_id: str) -> bool:
        """
        Check if a user is in the whitelist.
        
        Args:
            telegram_id (str): Telegram user ID.
            
        Returns:
            bool: True if user is whitelisted, False otherwise.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text(QUERIES["CHECK_USER_WHITELIST"]),
                    {"telegram_id": telegram_id}
                )
                return result.fetchone() is not None
        except SQLAlchemyError as e:
            logger.error(ERROR_MESSAGES["DATABASE_WHITELIST_ERROR"].format(error=e))
            return False
    
    def get_user_id(self, telegram_id: str) -> Optional[int]:
        """
        Get user ID from telegram_id.
        
        Args:
            telegram_id (str): Telegram user ID.
            
        Returns:
            Optional[int]: User ID if found, None otherwise.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text(QUERIES["CHECK_USER_WHITELIST"]),
                    {"telegram_id": telegram_id}
                )
                user = result.fetchone()
                return user[0] if user else None
        except SQLAlchemyError as e:
            logger.error(ERROR_MESSAGES["DATABASE_WHITELIST_ERROR"].format(error=e))
            return None
    
    def save_expense(self, telegram_id: str, description: str, amount: float, category: str) -> bool:
        """
        Save an expense to the database.
        
        Args:
            telegram_id (str): Telegram user ID.
            description (str): Expense description.
            amount (float): Expense amount.
            category (str): Expense category.
            
        Returns:
            bool: True if saved successfully, False otherwise.
        """
        try:
            with self.engine.connect() as conn:
                # Get user ID
                user_id = self.get_user_id(telegram_id)
                if not user_id:
                    logger.error(ERROR_MESSAGES["USER_NOT_FOUND"].format(telegram_id=telegram_id))
                    return False
                
                # Insert expense
                conn.execute(
                    text(QUERIES["INSERT_EXPENSE"]),
                    {
                        "user_id": user_id,
                        "description": description,
                        "amount": amount,
                        "category": category,
                        "added_at": datetime.utcnow()
                    }
                )
                conn.commit()
                
                logger.info(LOG_MESSAGES["EXPENSE_SAVED"].format(
                    description=description, 
                    amount=amount, 
                    category=category
                ))
                return True
                
        except SQLAlchemyError as e:
            logger.error(ERROR_MESSAGES["DATABASE_SAVE_ERROR"].format(error=e))
            return False
    
    def get_user_expenses(self, telegram_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent expenses for a user.
        
        Args:
            telegram_id (str): Telegram user ID.
            limit (int): Maximum number of expenses to return.
            
        Returns:
            List[Dict[str, Any]]: List of expense dictionaries.
        """
        try:
            with self.engine.connect() as conn:
                query = """
                    SELECT e.description, e.amount, e.category, e.added_at
                    FROM expenses e
                    JOIN users u ON e.user_id = u.id
                    WHERE u.telegram_id = :telegram_id
                    ORDER BY e.added_at DESC
                    LIMIT :limit
                """
                result = conn.execute(
                    text(query),
                    {"telegram_id": telegram_id, "limit": limit}
                )
                
                expenses = []
                for row in result.fetchall():
                    expenses.append({
                        "description": row[0],
                        "amount": float(row[1]),
                        "category": row[2],
                        "added_at": row[3].isoformat() if row[3] else None
                    })
                
                return expenses
                
        except SQLAlchemyError as e:
            logger.error(ERROR_MESSAGES["DATABASE_WHITELIST_ERROR"].format(error=e))
            return []
    
    def get_expense_stats(self, telegram_id: str) -> Dict[str, Any]:
        """
        Get expense statistics for a user.
        
        Args:
            telegram_id (str): Telegram user ID.
            
        Returns:
            Dict[str, Any]: Statistics including total amount and category breakdown.
        """
        try:
            with self.engine.connect() as conn:
                query = """
                    SELECT 
                        e.category,
                        COUNT(*) as count,
                        SUM(e.amount::numeric) as total_amount
                    FROM expenses e
                    JOIN users u ON e.user_id = u.id
                    WHERE u.telegram_id = :telegram_id
                    GROUP BY e.category
                    ORDER BY total_amount DESC
                """
                result = conn.execute(
                    text(query),
                    {"telegram_id": telegram_id}
                )
                
                stats = {
                    "total_expenses": 0,
                    "total_amount": 0.0,
                    "categories": {}
                }
                
                for row in result.fetchall():
                    category = row[0]
                    count = row[1]
                    total = float(row[2]) if row[2] else 0.0
                    
                    stats["total_expenses"] += count
                    stats["total_amount"] += total
                    stats["categories"][category] = {
                        "count": count,
                        "total_amount": total
                    }
                
                return stats
                
        except SQLAlchemyError as e:
            logger.error(ERROR_MESSAGES["DATABASE_WHITELIST_ERROR"].format(error=e))
            return {
                "total_expenses": 0,
                "total_amount": 0.0,
                "categories": {}
            } 