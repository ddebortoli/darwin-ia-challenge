#!/usr/bin/env python3
"""
Bot Service - FastAPI application for expense analysis and database operations.
"""

import os
import logging
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from constants import SERVICE_CONFIG, MESSAGES
from service import ExpenseService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, SERVICE_CONFIG["LOG_LEVEL"]),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Disable httpx logging to prevent sensitive URL exposure
logging.getLogger("httpx").setLevel(logging.WARNING)

# Initialize FastAPI app
app = FastAPI(
    title="Bot Service",
    description="Expense analysis and database operations service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Initialize service
expense_service = ExpenseService(DATABASE_URL)

# Pydantic models
class ExpenseRequest(BaseModel):
    """Request model for processing an expense message."""
    telegram_id: str = Field(..., description="Telegram user ID")
    message: str = Field(..., description="User message to process")

class ExpenseResponse(BaseModel):
    """Response model for expense processing."""
    success: bool
    category: str | None = None
    description: str | None = None
    amount: float | None = None
    message: str

class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    service: str
    timestamp: datetime

class ExpenseStatsResponse(BaseModel):
    """Response model for expense statistics."""
    total_expenses: int
    total_amount: float
    categories: Dict[str, Dict[str, Any]]

class UserExpensesResponse(BaseModel):
    """Response model for user expenses."""
    expenses: list
    count: int

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Status of the bot service.
    """
    return HealthResponse(
        status=MESSAGES["HEALTH_STATUS"],
        service=MESSAGES["SERVICE_NAME"],
        timestamp=datetime.utcnow()
    )

@app.post("/process-expense", response_model=ExpenseResponse)
async def process_expense(request: ExpenseRequest) -> ExpenseResponse:
    """
    Process an expense message and add it to the database.
    
    Args:
        request (ExpenseRequest): The request containing telegram_id and message.
        
    Returns:
        ExpenseResponse: The result of the expense processing.
    """
    result = await expense_service.process_expense(request.telegram_id, request.message)
    
    return ExpenseResponse(
        success=result["success"],
        category=result.get("category"),
        description=result.get("description"),
        amount=result.get("amount"),
        message=result["message"]
    )

@app.get("/categories")
async def get_categories() -> Dict[str, Any]:
    """
    Get available expense categories.
    
    Returns:
        Dict[str, Any]: Dictionary with the list of categories.
    """
    return {"categories": expense_service.get_categories()}

@app.get("/expenses/{telegram_id}", response_model=UserExpensesResponse)
async def get_user_expenses(telegram_id: str, limit: int = 10) -> UserExpensesResponse:
    """
    Get recent expenses for a user.
    
    Args:
        telegram_id (str): Telegram user ID.
        limit (int): Maximum number of expenses to return.
        
    Returns:
        UserExpensesResponse: User's recent expenses.
    """
    expenses = expense_service.get_user_expenses(telegram_id, limit)
    return UserExpensesResponse(
        expenses=expenses,
        count=len(expenses)
    )

@app.get("/stats/{telegram_id}", response_model=ExpenseStatsResponse)
async def get_expense_stats(telegram_id: str) -> ExpenseStatsResponse:
    """
    Get expense statistics for a user.
    
    Args:
        telegram_id (str): Telegram user ID.
        
    Returns:
        ExpenseStatsResponse: User's expense statistics.
    """
    stats = expense_service.get_expense_stats(telegram_id)
    return ExpenseStatsResponse(
        total_expenses=stats["total_expenses"],
        total_amount=stats["total_amount"],
        categories=stats["categories"]
    )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("BOT_SERVICE_PORT", SERVICE_CONFIG["BOT_SERVICE_PORT"]))
    host = os.getenv("BOT_SERVICE_HOST", SERVICE_CONFIG["BOT_SERVICE_HOST"])
    
    logger.info(f"Starting Bot Service on {host}:{port}")
    uvicorn.run(app, host=host, port=port) 