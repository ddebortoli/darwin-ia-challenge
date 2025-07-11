#!/usr/bin/env python3
"""
Setup script for the Telegram Expense Bot
Helps users get started quickly with the project.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🚀 Telegram Expense Bot Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_docker():
    """Check if Docker is available"""
    print("\n🐳 Checking Docker...")
    
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
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

def setup_virtual_environments():
    """Set up virtual environments for both services"""
    print("\n🐍 Setting up virtual environments...")
    
    services = ["bot-service", "connector-service"]
    
    for service in services:
        venv_path = Path(service) / "venv"
        if not venv_path.exists():
            print(f"Creating virtual environment for {service}...")
            try:
                subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
                print(f"✅ Created virtual environment for {service}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to create virtual environment for {service}: {e}")
        else:
            print(f"✅ Virtual environment for {service} already exists")

def install_dependencies():
    """Install dependencies for both services"""
    print("\n📦 Installing dependencies...")
    
    services = ["bot-service", "connector-service"]
    
    for service in services:
        print(f"\nInstalling dependencies for {service}...")
        requirements_path = Path(service) / "requirements.txt"
        
        if requirements_path.exists():
            try:
                # Determine pip path based on OS
                if os.name == 'nt':  # Windows
                    pip_path = Path(service) / "venv" / "Scripts" / "pip"
                else:  # Unix/Linux/macOS
                    pip_path = Path(service) / "venv" / "bin" / "pip"
                
                subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True)
                print(f"✅ Dependencies installed for {service}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies for {service}: {e}")
        else:
            print(f"⚠️  requirements.txt not found in {service}")

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "=" * 60)
    print("🎉 Setup completed!")
    print("=" * 60)
    print()
    print("Next steps:")
    print()
    print("1. 📝 Configure environment variables:")
    print("   - Edit bot-service/.env")
    print("   - Edit connector-service/.env")
    print()
    print("2. 🗄️  Set up PostgreSQL database:")
    print("   - Create a PostgreSQL database")
    print("   - Run database/schema.sql")
    print("   - Update DATABASE_URL in bot-service/.env")
    print()
    print("3. 🤖 Get Telegram Bot Token:")
    print("   - Message @BotFather on Telegram")
    print("   - Create a new bot with /newbot")
    print("   - Copy the token to connector-service/.env")
    print()
    print("4. 🤖 Ollama Setup (Optional):")
    print("   - Ollama is automatically configured")
    print("   - No API key needed!")
    print()
    print("5. 🚀 Start the services:")
    print("   Option A - Docker Compose:")
    print("   docker-compose up -d")
    print()
    print("   Option B - Manual:")
    print("   cd bot-service && python main.py")
    print("   cd connector-service && python main.py")
    print()
    print("6. 🧪 Test the setup:")
    print("   python test_bot.py")
    print()
    print("📚 For more information, see:")
    print("   - README.md")
    print("   - DEPLOYMENT.md")
    print("   - bot-service/README.md")
    print("   - connector-service/README.md")

def main():
    """Main setup function"""
    print_banner()
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    docker_available = check_docker()
    
    # Create environment files
    create_env_files()
    
    # Set up virtual environments
    setup_virtual_environments()
    
    # Install dependencies
    install_dependencies()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main() 