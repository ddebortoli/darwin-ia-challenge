#!/usr/bin/env python3
"""
Connector Service - Telegram API Integration
Handles Telegram webhook, message forwarding, and response delivery.
"""

import os
import logging
from typing import Optional
from datetime import datetime

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from telegram import Update, Bot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Disable httpx logging to prevent token exposure
logging.getLogger("httpx").setLevel(logging.WARNING)

# Initialize FastAPI app
app = FastAPI(
    title="Connector Service",
    description="Telegram API integration service",
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

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_SERVICE_URL = os.getenv("BOT_SERVICE_URL", "http://bot-service:8000")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: datetime

class WebhookResponse(BaseModel):
    status: str

class BotServiceRequest(BaseModel):
    telegram_id: str
    message: str

class BotServiceResponse(BaseModel):
    success: bool
    message: str
    category: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None

async def forward_to_bot_service(telegram_id: str, message: str) -> BotServiceResponse:
    """Forward message to Bot Service for processing"""
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            request_data = BotServiceRequest(
                telegram_id=telegram_id,
                message=message
            )
            
            logger.info(f"Forwarding message to Bot Service: {telegram_id} - [MESSAGE_HIDDEN]")
            
            logger.info(f"Making request to: {BOT_SERVICE_URL}/process-expense")
            response = await client.post(
                f"{BOT_SERVICE_URL}/process-expense",
                json=request_data.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            logger.info(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Bot Service response: [RESPONSE_HIDDEN]")
                return BotServiceResponse(**result)
            else:
                logger.error(f"Bot Service error: {response.status_code} - {response.text}")
                return BotServiceResponse(
                    success=False,
                    message="Error processing expense"
                )
                
        except httpx.RequestError as e:
            logger.error(f"HTTP request error: {e}")
            logger.error(f"Request URL: {BOT_SERVICE_URL}/process-expense")
            logger.error(f"Request data: [DATA_HIDDEN]")
            return BotServiceResponse(
                success=False,
                message="Service temporarily unavailable"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return BotServiceResponse(
                success=False,
                message="Internal server error"
            )

async def send_telegram_response(chat_id: int, message: str) -> bool:
    """Send response back to Telegram user"""
    
    try:
        logger.info('Sending response to Telegram user')
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Response sent to {chat_id}: [MESSAGE_HIDDEN]")
        return True
    except Exception as e:
        logger.error(f"Failed to send Telegram response: {e}")
        return False

async def handle_telegram_message(update: Update):
    """Handle incoming Telegram messages"""
    
    if not update.message or not update.message.text:
        return
    
    chat_id = update.message.chat_id
    user_id = str(update.message.from_user.id) if update.message.from_user else "unknown"
    message_text = update.message.text.strip()
    
    logger.info(f"Received message from {user_id} ({chat_id}): {message_text}")
    
    # Forward to Bot Service
    bot_response = await forward_to_bot_service(user_id, message_text)
    
    # Send response back to user
    response_message = bot_response.message
    await send_telegram_response(chat_id, response_message)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="connector-service",
        timestamp=datetime.utcnow()
    )

@app.post("/webhook", response_model=WebhookResponse)
async def telegram_webhook(request: Request):
    """Handle Telegram webhook updates"""
    
    try:
        # Parse the update
        update_data = await request.json()
        update = Update.de_json(update_data, bot)
        
        # Handle the update
        await handle_telegram_message(update)
        
        return WebhookResponse(status="ok")
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    

@app.post("/set-webhook")
async def set_webhook(webhook_url: str):
    """Set Telegram webhook URL"""
    
    try:
        success = await bot.set_webhook(url=webhook_url)
        if success:
            logger.info(f"Webhook set successfully: {webhook_url}")
            return {"status": "success", "message": "Webhook set successfully"}
        else:
            logger.error("Failed to set webhook")
            return {"status": "error", "message": "Failed to set webhook"}
            
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/webhook-info")
async def get_webhook_info():
    """Get current webhook information"""
    
    try:
        webhook_info = await bot.get_webhook_info()
        return {
            "url": webhook_info.url,
            "has_custom_certificate": webhook_info.has_custom_certificate,
            "pending_update_count": webhook_info.pending_update_count,
            "last_error_date": webhook_info.last_error_date,
            "last_error_message": webhook_info.last_error_message,
            "max_connections": webhook_info.max_connections,
            "allowed_updates": webhook_info.allowed_updates
        }
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return {"status": "error", "message": str(e)}

@app.delete("/delete-webhook")
async def delete_webhook():
    """Delete Telegram webhook"""
    
    try:
        success = await bot.delete_webhook()
        if success:
            logger.info("Webhook deleted successfully")
            return {"status": "success", "message": "Webhook deleted successfully"}
        else:
            logger.error("Failed to delete webhook")
            return {"status": "error", "message": "Failed to delete webhook"}
            
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/bot-info")
async def get_bot_info():
    """Get bot information"""
    
    try:
        bot_info = await bot.get_me()
        return {
            "id": bot_info.id,
            "username": bot_info.username,
            "first_name": bot_info.first_name,
            "can_join_groups": bot_info.can_join_groups,
            "can_read_all_group_messages": bot_info.can_read_all_group_messages,
            "supports_inline_queries": bot_info.supports_inline_queries
        }
    except Exception as e:
        logger.error(f"Error getting bot info: {e}")
        return {"status": "error", "message": str(e)}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Connector Service starting up...")
    
    # Test bot connection
    try:
        bot_info = await bot.get_me()
        logger.info(f"Bot connected: @{bot_info.username}")
    except Exception as e:
        logger.error(f"Failed to connect to Telegram bot: {e}")
        raise

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Connector Service shutting down...")

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("CONNECTOR_SERVICE_PORT", 8001))
    host = os.getenv("CONNECTOR_SERVICE_HOST", "0.0.0.0")
    
    logger.info(f"Starting Connector Service on {host}:{port}")
    uvicorn.run(app, host=host, port=port) 