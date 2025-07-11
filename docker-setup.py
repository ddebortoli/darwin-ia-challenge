#!/usr/bin/env python3
"""
Docker Setup Script for Telegram Expense Bot
Helps users configure the environment for Docker deployment.
"""

import os
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🐳 Telegram Expense Bot - Docker Setup")
    print("=" * 60)
    print()

def check_docker():
    """Check if Docker is available"""
    print("🔍 Checking Docker...")
    
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
        print("   Please install Docker from: https://docs.docker.com/get-docker/")
        return False

def create_env_files():
    """Create environment files if they don't exist"""
    print("\n📝 Creating environment files...")
    
    # Bot Service .env
    bot_env_path = Path("bot-service/.env")
    if not bot_env_path.exists():
        bot_env_example = Path("bot-service/env.example")
        if bot_env_example.exists():
            shutil.copy(bot_env_example, bot_env_path)
            print("✅ Created bot-service/.env")
        else:
            print("⚠️  bot-service/env.example not found")
    else:
        print("✅ bot-service/.env already exists")
    
    # Connector Service .env
    connector_env_path = Path("connector-service/.env")
    if not connector_env_path.exists():
        connector_env_example = Path("connector-service/env.example")
        if connector_env_example.exists():
            shutil.copy(connector_env_example, connector_env_path)
            print("✅ Created connector-service/.env")
        else:
            print("⚠️  connector-service/env.example not found")
    else:
        print("✅ connector-service/.env already exists")

def print_configuration_guide():
    """Print configuration guide"""
    print("\n" + "=" * 60)
    print("📋 Configuration Guide")
    print("=" * 60)
    print()
    print("You need to configure the following environment variables:")
    print()
    print("1. 🤖 Telegram Bot Token:")
    print("   - Message @BotFather on Telegram")
    print("   - Send /newbot command")
    print("   - Follow instructions to create your bot")
    print("   - Copy the token to connector-service/.env")
    print("   - Example: TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
    print()
    print("2. 🤖 Ollama Setup:")
    print("   - Ollama is automatically configured")
    print("   - No API key needed!")
    print("   - Models are downloaded automatically")
    print("   - Optional: Change model in bot-service/.env")
    print()
    print("3. 🗄️  Database Configuration:")
    print("   - For local development, Docker will handle this automatically")
    print("   - For production, update DATABASE_URL in bot-service/.env")
    print("   - Example: DATABASE_URL=postgresql://user:pass@host:port/db")
    print()

def print_next_steps():
    """Print next steps"""
    print("\n" + "=" * 60)
    print("🚀 Ready to Deploy!")
    print("=" * 60)
    print()
    print("Next steps:")
    print()
    print("1. 📝 Configure your environment variables:")
    print("   - Edit bot-service/.env")
    print("   - Edit connector-service/.env")
    print()
    print("2. 🐳 Start the services:")
    print("   docker-compose up -d")
    print()
    print("3. 🧪 Test the setup:")
    print("   docker-compose exec bot-service python test_bot.py")
    print()
    print("4. 🌐 Access the services:")
    print("   - Bot Service: http://localhost:8000")
    print("   - Connector Service: http://localhost:8001")
    print("   - Database: localhost:5432")
    print()
    print("5. 📊 Monitor logs:")
    print("   docker-compose logs -f")
    print()
    print("6. 🛑 Stop services:")
    print("   docker-compose down")
    print()
    print("📚 For more information:")
    print("   - README.md - Main documentation")
    print("   - DEPLOYMENT.md - Production deployment")
    print("   - docker-compose.yml - Service configuration")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Docker
    if not check_docker():
        print("\n❌ Docker is required to run this project.")
        print("   Please install Docker and try again.")
        return
    
    # Create environment files
    create_env_files()
    
    # Print configuration guide
    print_configuration_guide()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 