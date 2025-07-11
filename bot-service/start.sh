#!/bin/bash

# Wait for Ollama service and download model
echo "Setting up Ollama..."
python /app/setup-ollama.py

# Start the bot service
echo "Starting bot service..."
python main.py 