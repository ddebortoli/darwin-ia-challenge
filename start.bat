@echo off
REM Telegram Expense Bot - Quick Start Script for Windows
REM This script helps you get the bot running quickly with Docker

echo 🚀 Telegram Expense Bot - Quick Start
echo ======================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first:
    echo    https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are available
echo.

REM Create environment files if they don't exist
if not exist "bot-service\.env" (
    echo 📝 Creating bot-service\.env...
    copy "bot-service\env.example" "bot-service\.env" >nul
    echo ⚠️  Please edit bot-service\.env with your Ollama configuration (optional)
)

if not exist "connector-service\.env" (
    echo 📝 Creating connector-service\.env...
    copy "connector-service\env.example" "connector-service\.env" >nul
    echo ⚠️  Please edit connector-service\.env with your Telegram bot token
)

echo.
echo 🔧 Configuration required:
echo    1. Edit bot-service\.env - Configure Ollama settings (optional)
echo    2. Edit connector-service\.env - Add your TELEGRAM_BOT_TOKEN
echo.
set /p CONFIRM="Have you configured the environment files? (y/n): "

if /i "%CONFIRM%" neq "y" (
    echo Please configure the environment files first, then run this script again.
    pause
    exit /b 1
)

echo 🐳 Starting services with Docker Compose...
docker-compose up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo 🔍 Checking service health...

curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Bot Service is running
) else (
    echo ❌ Bot Service is not responding
)

curl -f http://localhost:8001/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Connector Service is running
) else (
    echo ❌ Connector Service is not responding
)

echo.
echo 🎉 Setup complete!
echo.
echo 📊 Services:
echo    - Bot Service: http://localhost:8000
echo    - Connector Service: http://localhost:8001
echo    - Database: localhost:5432
echo.
echo 📝 Useful commands:
echo    - View logs: docker-compose logs -f
echo    - Stop services: docker-compose down
echo    - Restart services: docker-compose restart
echo    - Test the bot: docker-compose exec bot-service python test_bot.py
echo.
echo 🤖 Next steps:
echo    1. Set up your Telegram webhook (see DEPLOYMENT.md)
echo    2. Test the bot by sending a message
echo    3. Monitor logs for any issues
echo.
pause 