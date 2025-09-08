# Telegram Expense Bot

A Telegram chatbot that facilitates expense tracking with automatic categorization using AI. The system consists of two Python services working together to provide a seamless expense management experience.

## 🚀 Quick Start

### Prerequisites

- **Docker and Docker Compose**
- **Telegram Bot Token** (from @BotFather)
- **Ollama** (included in Docker setup - no API key needed!)

### 📋 Step-by-Step Setup

#### 1. **Get Telegram Bot Token**

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Choose a name for your bot (e.g., "My Expense Bot")
4. Choose a username (must end in 'bot', e.g., "my_expense_bot")
5. Copy the token (looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 2. **Clone and Setup**

```bash
git clone <your-repo-url>
cd ai-telegram-bot
```

#### 3. **Configure Environment**

**Windows:**
```cmd
start.bat
```

**Linux/macOS:**
```bash
./start.sh
```

#### 4. **Add Your Telegram ID to Whitelist**

1. Send a message to your bot
2. Check the logs: `docker-compose logs bot-service`
3. Copy your Telegram ID from the logs
4. Connect to the database and add your ID:

```sql
INSERT INTO users (telegram_id, username, added_at) 
VALUES ('YOUR_TELEGRAM_ID', 'your_username', NOW());
```

#### 5. **Set Webhook URL**

Replace `YOUR_BOT_TOKEN` and `YOUR_DOMAIN`:

```bash
curl -X POST "http://localhost:8001/set-webhook" \
  -H "Content-Type: application/json" \
  -d '{"webhook_url": "https://YOUR_DOMAIN/connector-service/webhook"}'
```

#### 6. **Test the Bot**

Send messages like:
- "Pizza 20 bucks"
- "Gas 45.50"
- "Netflix subscription 15.99"

## 🏗️ Architecture

- **Bot Service**: Handles expense analysis, categorization, and database operations
- **Connector Service**: Manages Telegram API integration and message routing
- **Ollama Service**: Local AI model for intelligent expense analysis
- **PostgreSQL**: Database for storing expenses and user data

## 🤖 AI Model Configuration

The bot uses **Ollama** with local AI models for expense analysis. This is completely free and runs locally!

### Available Models

You can change the model by editing `bot-service/constants.py`:

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

### Model Download

The first time you run the system, it will automatically download the specified model. This only happens once.

**To change models:**
1. Edit `bot-service/constants.py`
2. Restart the bot service: `docker-compose restart bot-service`

## 🔧 Manual Setup (Alternative)

If you prefer to run without Docker:

### 1. Install Dependencies

```bash
# Bot Service
cd bot-service
pip install -r requirements.txt

# Connector Service
cd ../connector-service
pip install -r requirements.txt
```

### 2. Set Up PostgreSQL

```sql
CREATE DATABASE expense_bot_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE expense_bot_db TO postgres;
```

### 3. Configure Environment Variables

**bot-service/.env:**
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/expense_bot_db
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
LOG_LEVEL=INFO
```

**connector-service/.env:**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
BOT_SERVICE_URL=http://localhost:8000
LOG_LEVEL=INFO
```

### 4. Start Services

```bash
# Terminal 1 - Bot Service
cd bot-service
python main.py

# Terminal 2 - Connector Service
cd connector-service
python main.py

# Terminal 3 - Ollama (if not running)
ollama serve
```

## 🛡️ Security Features

- **Whitelist Authentication**: Only authorized users can use the bot
- **Secure Logging**: No sensitive data exposed in logs
- **Environment Variables**: All sensitive data stored in .env files
- **Docker Isolation**: Services run in isolated containers

## 📊 Database Schema

```sql
-- Users table (whitelist)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id VARCHAR(50) UNIQUE NOT NULL,
    username VARCHAR(100),
    added_at TIMESTAMP DEFAULT NOW()
);

-- Expenses table
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    description TEXT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    added_at TIMESTAMP DEFAULT NOW()
);
```

## 🔍 Troubleshooting

### Common Issues

**1. Bot not responding:**
- Check if services are running: `docker-compose ps`
- Verify webhook is set: `curl http://localhost:8001/webhook-info`
- Check logs: `docker-compose logs connector-service`

**2. "User not authorized" error:**
- Add your Telegram ID to the database whitelist
- Check logs for your Telegram ID: `docker-compose logs bot-service`

**3. Ollama connection issues:**
- Verify Ollama is running: `docker-compose logs ollama`
- Check model is downloaded: `docker exec ai-telegram-bot-ollama-1 ollama list`

**4. Database connection errors:**
- Check PostgreSQL is running: `docker-compose logs postgres`
- Verify database URL in environment variables

### Useful Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f bot-service
docker-compose logs -f connector-service

# Restart services
docker-compose restart bot-service
docker-compose restart connector-service

# Check service health
curl http://localhost:8000/health
curl http://localhost:8001/health

# Test bot service directly
curl -X POST http://localhost:8000/process-expense \
  -H "Content-Type: application/json" \
  -d '{"telegram_id": "123456789", "message": "pizza 20 bucks"}'
```

## 📁 Project Structure

```
ai-telegram-bot/
├── bot-service/              # Expense analysis and database operations
│   ├── main.py              # FastAPI application
│   ├── service.py           # Business logic layer
│   ├── repository.py        # Database operations
│   ├── constants.py         # Configuration and constants
│   ├── requirements.txt     # Python dependencies
│   ├── env.example         # Environment variables template
│   └── Dockerfile          # Docker configuration
├── connector-service/        # Telegram API integration
│   ├── main.py             # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── env.example        # Environment variables template
│   └── Dockerfile         # Docker configuration
├── database/                # Database setup
│   └── schema.sql          # PostgreSQL schema
├── docker-compose.yml       # Docker Compose configuration
├── setup.py                # Automated setup script
├── start.bat               # Windows startup script
├── start.sh                # Linux/macOS startup script
├── test_bot.py             # Test script
├── DEPLOYMENT.md           # Deployment guide
└── README.md               # This file
```

## 🎯 Features

- ✅ **Whitelist-based user authentication**
- ✅ **Automatic expense categorization using AI**
- ✅ **Concurrent request handling**
- ✅ **LangChain integration with Ollama**
- ✅ **PostgreSQL database integration**
- ✅ **Secure logging (no sensitive data exposed)**
- ✅ **Docker-based deployment**
- ✅ **No hard-coded values - fully configurable**
- ✅ **Support for multiple AI models (llama2, grok, mistral, etc.)**

## 📈 Expense Categories

The bot automatically categorizes expenses into:
- **Housing** - Rent, mortgage, utilities
- **Transportation** - Gas, public transport, car maintenance
- **Food** - Groceries, restaurants, takeout
- **Utilities** - Electricity, water, internet
- **Insurance** - Health, car, home insurance
- **Medical/Healthcare** - Doctor visits, medications
- **Savings** - Emergency fund, investments
- **Debt** - Credit cards, loans
- **Education** - Courses, books, tuition
- **Entertainment** - Movies, games, subscriptions
- **Other** - Miscellaneous expenses

## 🚀 Deployment

### Local Development
```bash
docker-compose up -d
```

### Production Deployment
Both services can be deployed to:
- **Vercel** (recommended for serverless)
- **Railway** (easy deployment)
- **Heroku** (traditional PaaS)
- **Any Python-compatible PaaS**

For PostgreSQL hosting:
- **Supabase** (recommended)
- **Railway**
- **Neon**
- **Any PostgreSQL provider**

## 📝 Example Usage

Send messages to your bot like:
- "Pizza 20 bucks" → Food expense added ✅
- "Gas 45.50" → Transportation expense added ✅
- "Netflix subscription 15.99" → Entertainment expense added ✅
- "Grocery shopping 120" → Food expense added ✅

The bot will respond with: "[Category] expense added ✅"

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details. 