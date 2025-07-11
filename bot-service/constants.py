"""
Constants and configuration values for the Bot Service.
"""

from enum import Enum
from typing import List

# Database configuration
DATABASE_CONFIG = {
    "POSTGRES_DB": "expense_bot_db",
    "POSTGRES_USER": "postgres",
    "POSTGRES_PASSWORD": "password",
    "POSTGRES_HOST": "postgres",
    "POSTGRES_PORT": "5432"
}

# Ollama configuration
OLLAMA_CONFIG = {
    "BASE_URL": "http://ollama:11434",
    "MODEL": "llama2",
    "TEMPERATURE": 0
}

# Service configuration
SERVICE_CONFIG = {
    "BOT_SERVICE_PORT": 8000,
    "BOT_SERVICE_HOST": "0.0.0.0",
    "LOG_LEVEL": "INFO"
}

# Expense categories
class ExpenseCategory(Enum):
    """Enum for expense categories."""
    HOUSING = "Housing"
    TRANSPORTATION = "Transportation"
    FOOD = "Food"
    UTILITIES = "Utilities"
    INSURANCE = "Insurance"
    MEDICAL_HEALTHCARE = "Medical/Healthcare"
    SAVINGS = "Savings"
    DEBT = "Debt"
    EDUCATION = "Education"
    ENTERTAINMENT = "Entertainment"
    OTHER = "Other"

# Available categories list
EXPENSE_CATEGORIES: List[str] = [category.value for category in ExpenseCategory]

# Messages
MESSAGES = {
    "UNAUTHORIZED_USER": "User not authorized to use this bot",
    "NON_EXPENSE_MESSAGE": "Message does not appear to be an expense",
    "INVALID_EXPENSE_DATA": "Could not extract valid expense information",
    "DATABASE_SAVE_ERROR": "Failed to save expense to database",
    "EXPENSE_ADDED": "{category} expense added ✅",
    "HEALTH_STATUS": "healthy",
    "SERVICE_NAME": "bot-service"
}

# Database queries
QUERIES = {
    "CHECK_USER_WHITELIST": "SELECT id FROM users WHERE telegram_id = :telegram_id",
    "INSERT_EXPENSE": """
        INSERT INTO expenses (user_id, description, amount, category, added_at)
        VALUES (:user_id, :description, :amount, :category, :added_at)
    """
}

# LLM Prompt template
EXPENSE_ANALYSIS_PROMPT = """You are an expense analysis expert. Your job is to determine if a message contains expense information and extract it.

IMPORTANT: Only messages that explicitly mention a purchase, payment, or expense with a monetary amount should be considered expenses.

Available categories: Housing, Transportation, Food, Utilities, Insurance, Medical/Healthcare, Savings, Debt, Education, Entertainment, Other

Rules:
1. ONLY messages that mention a purchase, payment, or expense with a monetary amount are expenses
2. Messages without monetary amounts are NOT expenses
3. Greetings, questions, random text, or non-financial messages are NOT expenses
4. If the message is not about an expense, set is_expense to false and return null for other fields
5. Extract the description (what was purchased)
6. Extract the amount (numeric value)
7. Categorize into the most appropriate category
8. Amount should be a positive number

Examples of EXPENSES:
- "Pizza 20 bucks" → is_expense: true, description: "Pizza", amount: 20.0, category: "Food"
- "Gas 45.50" → is_expense: true, description: "Gas", amount: 45.50, category: "Transportation"
- "Netflix subscription 15.99" → is_expense: true, description: "Netflix subscription", amount: 15.99, category: "Entertainment"

Examples of NON-EXPENSES:
- "Hello there" → is_expense: false, description: null, amount: null, category: null
- "How are you?" → is_expense: false, description: null, amount: null, category: null
- "I'm feeling great" → is_expense: false, description: null, amount: null, category: null
- "What's the weather?" → is_expense: false, description: null, amount: null, category: null

Return only the JSON response with fields: is_expense, description, amount, category"""

# Error messages
ERROR_MESSAGES = {
    "DATABASE_URL_MISSING": "DATABASE_URL environment variable is required",
    "USER_NOT_FOUND": "User {telegram_id} not found in database",
    "DATABASE_WHITELIST_ERROR": "Database error checking whitelist: {error}",
    "DATABASE_SAVE_ERROR": "Database error saving expense: {error}",
    "LLM_ANALYSIS_ERROR": "Error analyzing message with LLM: {error}",
    "INVALID_EXPENSE_RESPONSE": "Invalid expense data in response: {result}",
    "FAILED_TO_SAVE": "Failed to save expense for user {telegram_id}",
    "INVALID_EXPENSE_DATA": "Invalid expense data extracted: {analysis}"
}

# Log messages
LOG_MESSAGES = {
    "PROCESSING_EXPENSE": "Processing expense request from user {telegram_id}",
    "UNAUTHORIZED_ATTEMPT": "Unauthorized user attempt: {telegram_id}",
    "NON_EXPENSE_MESSAGE": "Non-expense message from {telegram_id}: [MESSAGE_HIDDEN]",
    "LLM_RESPONSE": "LLM Response: {content}",
    "PARSED_RESULT": "Parsed result: [RESULT_HIDDEN]",
    "MESSAGE_NON_EXPENSE": "Message identified as non-expense: [MESSAGE_HIDDEN]",
    "EXPENSE_SAVED": "Expense saved: {description} - ${amount} - {category}",
    "SERVICE_STARTING": "Starting Bot Service on {host}:{port}"
} 