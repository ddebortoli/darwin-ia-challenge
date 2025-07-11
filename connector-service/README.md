# Connector Service

The Connector Service acts as the interface between the Telegram API and the Bot Service. It manages the reception of inbound messages from users, forwards these messages to the Bot Service for processing, and sends the appropriate responses back to the users via Telegram.

## Features

- 🤖 **Telegram Integration**: Handles Telegram Bot API communication
- 🔄 **Message Routing**: Forwards messages to Bot Service for processing
- 📤 **Response Delivery**: Sends processed responses back to users
- ⚡ **Concurrent Processing**: Handles multiple messages simultaneously
- 🔧 **Configurable**: No hard-coded values
- 🛡️ **Secure Logging**: No sensitive data exposed in logs
- 🔒 **Error Handling**: Graceful handling of API failures

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Telegram Bot Token (from @BotFather)
- Bot Service running and accessible

### Docker Setup (Recommended)

```bash
# Start all services including Connector Service
docker-compose up -d connector-service

# Check service health
curl http://localhost:8001/health
```

### Manual Setup

1. **Clone and navigate to the service directory:**
   ```bash
   cd connector-service
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp env.example .env
   # Edit .env with your actual values
   ```

5. **Start the service:**
   ```bash
   python main.py
   ```

## 🤖 Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My Expense Bot")
4. Choose a username (must end in 'bot', e.g., "my_expense_bot")
5. Copy the token provided by BotFather (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
6. Add the token to your `.env` file

## 🔗 Webhook Setup

### For Local Development

1. **Install ngrok** (for exposing local server):
   ```bash
   # Download from https://ngrok.com/
   # Or install via package manager
   ```

2. **Start the Connector Service:**
   ```bash
   docker-compose up -d connector-service
   ```

3. **Expose your local server:**
   ```bash
   ngrok http 8001
   ```

4. **Set the webhook URL:**
   ```bash
   curl -X POST "http://localhost:8001/set-webhook" \
     -H "Content-Type: application/json" \
     -d '{"webhook_url": "https://YOUR_NGROK_URL/webhook"}'
   ```

### For Production

1. **Deploy the Connector Service** to your hosting provider
2. **Set the webhook URL:**
   ```bash
   curl -X POST "https://YOUR_DOMAIN/set-webhook" \
     -H "Content-Type: application/json" \
     -d '{"webhook_url": "https://YOUR_DOMAIN/webhook"}'
   ```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token from @BotFather | Yes | - |
| `BOT_SERVICE_URL` | URL of the Bot Service | Yes | http://bot-service:8000 |
| `CONNECTOR_SERVICE_PORT` | Port to run the service on | No | 8001 |
| `CONNECTOR_SERVICE_HOST` | Host to bind to | No | 0.0.0.0 |
| `LOG_LEVEL` | Logging level | No | INFO |

## API Endpoints

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "connector-service",
  "timestamp": "2025-07-11T20:00:00.000000"
}
```

### POST /webhook

Telegram webhook endpoint for receiving updates.

**Request Body:** Telegram Update object

**Response:**
```json
{
  "status": "ok"
}
```

### POST /set-webhook

Set the Telegram webhook URL.

**Request Body:**
```json
{
  "webhook_url": "https://your-domain.com/webhook"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Webhook set successfully"
}
```

### GET /webhook-info

Get current webhook information.

**Response:**
```json
{
  "url": "https://your-domain.com/webhook",
  "has_custom_certificate": false,
  "pending_update_count": 0,
  "last_error_date": null,
  "last_error_message": null,
  "max_connections": 40,
  "allowed_updates": null
}
```

### DELETE /delete-webhook

Delete the Telegram webhook.

**Response:**
```json
{
  "status": "success",
  "message": "Webhook deleted successfully"
}
```

### GET /bot-info

Get bot information.

**Response:**
```json
{
  "id": 123456789,
  "username": "my_expense_bot",
  "first_name": "My Expense Bot",
  "can_join_groups": true,
  "can_read_all_group_messages": false,
  "supports_inline_queries": false
}
```

## 🏗️ Architecture

The service uses:
- **FastAPI**: Modern, fast web framework
- **python-telegram-bot**: Official Telegram Bot API library
- **httpx**: Async HTTP client for communicating with Bot Service
- **Pydantic**: Data validation and serialization

## 📨 Message Flow

1. **User sends message** to Telegram bot
2. **Telegram sends webhook** to Connector Service
3. **Connector Service forwards** message to Bot Service
4. **Bot Service processes** message and returns response
5. **Connector Service sends** response back to user via Telegram

## 🛡️ Security Features

- **Secure Logging**: No sensitive data exposed in logs
- **Environment Variables**: All sensitive data stored in .env files
- **Input Validation**: All inputs validated with Pydantic
- **Error Handling**: Comprehensive error handling without data exposure
- **HTTPS Required**: Production deployments require HTTPS

## Error Handling

The service handles various error scenarios:
- Telegram API errors
- Bot Service communication failures
- Invalid message formats
- Network connectivity issues
- Rate limiting
- Webhook validation errors

## Logging

The service provides comprehensive logging for:
- Incoming Telegram messages (sanitized)
- Bot Service communication (sanitized)
- Response delivery (sanitized)
- Error conditions
- Performance metrics

**Security Note**: All logs are sanitized to prevent exposure of sensitive data like user messages, bot tokens, and internal responses.

## 🔍 Troubleshooting

### Common Issues

**1. Bot not responding:**
- Check if services are running: `docker-compose ps`
- Verify webhook is set: `curl http://localhost:8001/webhook-info`
- Check logs: `docker-compose logs connector-service`

**2. Webhook not receiving updates:**
- Verify webhook URL is correct
- Check if HTTPS is required (Telegram requires HTTPS for webhooks)
- Ensure the webhook endpoint is accessible

**3. Bot Service communication errors:**
- Check if Bot Service is running: `docker-compose logs bot-service`
- Verify BOT_SERVICE_URL in environment variables
- Check network connectivity between services

**4. Telegram API errors:**
- Verify bot token is correct
- Check if bot is not blocked by users
- Ensure bot has necessary permissions

### Useful Commands

```bash
# Check service health
curl http://localhost:8001/health

# Get webhook info
curl http://localhost:8001/webhook-info

# Set webhook (replace with your URL)
curl -X POST "http://localhost:8001/set-webhook" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://your-domain.com/webhook"}'

# Delete webhook
curl -X DELETE "http://localhost:8001/delete-webhook"

# Get bot info
curl http://localhost:8001/bot-info

# View logs
docker-compose logs -f connector-service

# Restart service
docker-compose restart connector-service
```

## 🚀 Deployment

The service can be deployed to:
- **Vercel** (recommended for serverless)
- **Railway** (easy deployment)
- **Heroku** (traditional PaaS)
- **Any Python-compatible PaaS**

### Production Deployment Steps

1. **Deploy the service** to your hosting provider
2. **Set environment variables** (TELEGRAM_BOT_TOKEN, BOT_SERVICE_URL)
3. **Set up webhook URL** using the `/set-webhook` endpoint
4. **Verify webhook is working** using `/webhook-info`
5. **Test the bot** by sending a message

### Security Considerations

- Bot token should be kept secret
- Use HTTPS in production
- Validate incoming webhook requests
- Implement rate limiting if needed
- Monitor for abuse
- Use environment variables for all sensitive data 