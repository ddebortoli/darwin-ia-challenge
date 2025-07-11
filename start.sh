#!/bin/bash

# Telegram Expense Bot - Quick Start Script
# This script helps you get the bot running quickly with Docker

set -e

echo "🚀 Telegram Expense Bot - Quick Start"
echo "======================================"
echo

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"
echo

# Create environment files if they don't exist
if [ ! -f "bot-service/.env" ]; then
    echo "📝 Creating bot-service/.env..."
    cp bot-service/env.example bot-service/.env
    echo "⚠️  Please edit bot-service/.env with your Ollama configuration (optional)"
fi

if [ ! -f "connector-service/.env" ]; then
    echo "📝 Creating connector-service/.env..."
    cp connector-service/env.example connector-service/.env
    echo "⚠️  Please edit connector-service/.env with your Telegram bot token"
fi

echo
echo "🔧 Configuration required:"
echo "   1. Edit bot-service/.env - Configure Ollama settings (optional)"
echo "   2. Edit connector-service/.env - Add your TELEGRAM_BOT_TOKEN"
echo
read -p "Have you configured the environment files? (y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please configure the environment files first, then run this script again."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

echo
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Bot Service is running"
else
    echo "❌ Bot Service is not responding"
fi

if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ Connector Service is running"
else
    echo "❌ Connector Service is not responding"
fi

echo
echo "🎉 Setup complete!"
echo
echo "📊 Services:"
echo "   - Bot Service: http://localhost:8000"
echo "   - Connector Service: http://localhost:8001"
echo "   - Database: localhost:5432"
echo
echo "📝 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo "   - Test the bot: docker-compose exec bot-service python test_bot.py"
echo
echo "🤖 Next steps:"
echo "   1. Set up your Telegram webhook (see DEPLOYMENT.md)"
echo "   2. Test the bot by sending a message"
echo "   3. Monitor logs for any issues" 