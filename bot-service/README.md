# Bot Service

The Bot Service is responsible for analyzing incoming messages, extracting expense details, categorizing expenses, and persisting them to the database using AI-powered analysis.

## Features

- 🔍 **Intelligent Message Analysis**: Uses LangChain with Ollama to extract expense details
- 🏷️ **Automatic Categorization**: Categorizes expenses into predefined categories
- 👥 **User Whitelist**: Only processes messages from whitelisted users
- 💾 **Database Integration**: Stores expenses in PostgreSQL
- ⚡ **Concurrent Processing**: Handles multiple requests simultaneously
- 🔧 **Configurable**: No hard-coded values
- 🛡️ **Secure Logging**: No sensitive data exposed in logs
- 🤖 **Multiple AI Models**: Support for llama2, grok, mistral, and more

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Ollama (included automatically in Docker)

### Docker Setup (Recommended)

```bash
# Start all services including Bot Service
docker-compose up -d bot-service

# Check service health
curl http://localhost:8000/health
```

### Manual Setup

1. **Clone and navigate to the service directory:**
   ```bash
   cd bot-service
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

5. **Run database migrations:**
   ```bash
   # Execute the schema.sql file in your PostgreSQL database
   psql -d your_database -f ../database/schema.sql
   ```

6. **Start the service:**
   ```bash
   python main.py
   ```

## 🤖 AI Model Configuration

The service uses **Ollama** with local AI models for expense analysis. This is completely free and runs locally!

### Available Models

You can change the model by editing `constants.py`:

```python
OLLAMA_CONFIG = {
    "BASE_URL": "http://ollama:11434",
    "MODEL": "llama2",        # Default (recommended)
    "TEMPERATURE": 0
}
```

**Popular Models:**
- `llama2` - Default, good balance (4GB)
- `llama2:7b` - Smaller, faster (4GB)
- `llama2:13b` - Larger, more accurate (8GB)
- `grok` - Advanced reasoning (if available)
- `codellama` - Good for code-related expenses
- `mistral` - Fast and efficient
- `llama3` - Latest model (if available)

### Model Download

The first time you run the system, it will automatically download the specified model. This only happens once.

**To change models:**
1. Edit `constants.py`
2. Restart the service: `docker-compose restart bot-service`

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `OLLAMA_BASE_URL` | Ollama service URL | No | http://localhost:11434 |
| `OLLAMA_MODEL` | Ollama model name | No | llama2 |
| `BOT_SERVICE_PORT` | Port to run the service on | No | 8000 |
| `BOT_SERVICE_HOST` | Host to bind to | No | 0.0.0.0 |
| `LOG_LEVEL` | Logging level | No | INFO |

## API Endpoints

### POST /process-expense

Processes an expense message and adds it to the database.

**Request Body:**
```json
{
  "telegram_id": "123456789",
  "message": "Pizza 20 bucks"
}
```

**Response:**
```json
{
  "success": true,
  "category": "Food",
  "description": "Pizza",
  "amount": 20.00,
  "message": "Food expense added ✅"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "bot-service",
  "timestamp": "2025-07-11T20:00:00.000000"
}
```

### GET /categories

Get available expense categories.

**Response:**
```json
{
  "categories": [
    "Housing",
    "Transportation",
    "Food",
    "Utilities",
    "Insurance",
    "Medical/Healthcare",
    "Savings",
    "Debt",
    "Education",
    "Entertainment",
    "Other"
  ]
}
```

### GET /expenses/{telegram_id}

Get recent expenses for a user.

**Response:**
```json
{
  "expenses": [
    {
      "id": 1,
      "description": "Pizza",
      "amount": 20.00,
      "category": "Food",
      "added_at": "2025-07-11T20:00:00.000000"
    }
  ],
  "count": 1
}
```

### GET /stats/{telegram_id}

Get expense statistics for a user.

**Response:**
```json
{
  "total_expenses": 10,
  "total_amount": 250.00,
  "categories": {
    "Food": {
      "count": 5,
      "total": 120.00
    },
    "Transportation": {
      "count": 3,
      "total": 80.00
    }
  }
}
```

## 📈 Expense Categories

The service automatically categorizes expenses into:

- **Housing**: Rent, mortgage, home repairs
- **Transportation**: Gas, public transport, car maintenance
- **Food**: Groceries, restaurants, takeout
- **Utilities**: Electricity, water, internet, phone
- **Insurance**: Health, car, home insurance
- **Medical/Healthcare**: Doctor visits, medications, medical supplies
- **Savings**: Investments, emergency fund
- **Debt**: Credit card payments, loans
- **Education**: Tuition, books, courses
- **Entertainment**: Movies, games, hobbies
- **Other**: Miscellaneous expenses

## 🏗️ Architecture

The service uses a layered architecture:

- **FastAPI**: Modern, fast web framework
- **Service Layer**: Business logic and AI processing
- **Repository Layer**: Database operations
- **LangChain**: AI-powered message analysis
- **Ollama**: LLM for intelligent text processing
- **Pydantic**: Data validation and serialization
- **SQLAlchemy**: Database ORM

### File Structure

```
bot-service/
├── main.py              # FastAPI application
├── service.py           # Business logic layer
├── repository.py        # Database operations
├── constants.py         # Configuration and constants
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
└── Dockerfile          # Docker configuration
```

## 🛡️ Security Features

- **Whitelist Authentication**: Only authorized users can use the service
- **Secure Logging**: No sensitive data exposed in logs
- **Environment Variables**: All sensitive data stored in .env files
- **Input Validation**: All inputs validated with Pydantic
- **Error Handling**: Comprehensive error handling without data exposure

## Error Handling

The service handles various error scenarios:
- Invalid user (not in whitelist)
- Non-expense messages
- Database connection issues
- Ollama service errors
- Invalid message format
- AI model errors

## Logging

The service provides comprehensive logging for:
- Request processing
- Database operations
- AI model interactions
- Error conditions
- Performance metrics

**Security Note**: All logs are sanitized to prevent exposure of sensitive data like user messages, AI responses, and database queries.

## 🔍 Troubleshooting

### Common Issues

**1. Ollama connection errors:**
- Check if Ollama is running: `docker-compose logs ollama`
- Verify model is downloaded: `docker exec ai-telegram-bot-ollama-1 ollama list`
- Check URL in constants.py

**2. Database connection errors:**
- Verify PostgreSQL is running: `docker-compose logs postgres`
- Check DATABASE_URL in environment variables
- Ensure database schema is created

**3. AI model errors:**
- Check model name in constants.py
- Verify model is downloaded
- Check Ollama service logs

### Useful Commands

```bash
# Check service health
curl http://localhost:8000/health

# Test expense processing
curl -X POST http://localhost:8000/process-expense \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": "123456789", "message": "pizza 20 bucks"}'

# View logs
docker-compose logs -f bot-service

# Restart service
docker-compose restart bot-service
``` 