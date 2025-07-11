#!/usr/bin/env python3
"""
Setup script for Ollama model download
This script downloads the specified model when the Ollama service starts
"""

import os
import time
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_ollama(base_url: str, max_retries: int = 30) -> bool:
    """Wait for Ollama service to be ready"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info("Ollama service is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        
        logger.info(f"Waiting for Ollama service... ({i+1}/{max_retries})")
        time.sleep(10)
    
    logger.error("Ollama service failed to start")
    return False

def download_model(base_url: str, model_name: str) -> bool:
    """Download the specified model"""
    try:
        logger.info(f"Downloading model: {model_name}")
        
        # Check if model already exists
        response = requests.get(f"{base_url}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            if any(model["name"] == model_name for model in models):
                logger.info(f"Model {model_name} already exists")
                return True
        
        # Download the model
        response = requests.post(
            f"{base_url}/api/pull",
            json={"name": model_name}
        )
        
        if response.status_code == 200:
            logger.info(f"Model {model_name} downloaded successfully")
            return True
        else:
            logger.error(f"Failed to download model: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error downloading model: {e}")
        return False

def main():
    """Main function"""
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    model_name = os.getenv("OLLAMA_MODEL", "llama2")
    
    logger.info(f"Setting up Ollama with model: {model_name}")
    
    # Wait for Ollama service
    if not wait_for_ollama(base_url):
        return False
    
    # Download model
    if not download_model(base_url, model_name):
        return False
    
    logger.info("Ollama setup completed successfully")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 