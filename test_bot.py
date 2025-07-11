#!/usr/bin/env python3
"""
Test script for the Telegram Expense Bot
Tests both Bot Service and Connector Service functionality.
"""

import asyncio
import httpx
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BOT_SERVICE_URL = os.getenv("BOT_SERVICE_URL", "http://bot-service:8000")
CONNECTOR_SERVICE_URL = os.getenv("CONNECTOR_SERVICE_URL", "http://connector-service:8001")

class BotTester:
    def __init__(self):
        self.bot_service_url = BOT_SERVICE_URL
        self.connector_service_url = CONNECTOR_SERVICE_URL
        
    async def test_health_endpoints(self):
        """Test health endpoints of both services"""
        print("🔍 Testing health endpoints...")
        
        async with httpx.AsyncClient() as client:
            # Test Bot Service health
            try:
                response = await client.get(f"{self.bot_service_url}/health")
                if response.status_code == 200:
                    print("✅ Bot Service health check passed")
                else:
                    print(f"❌ Bot Service health check failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Bot Service health check error: {e}")
            
            # Test Connector Service health
            try:
                response = await client.get(f"{self.connector_service_url}/health")
                if response.status_code == 200:
                    print("✅ Connector Service health check passed")
                else:
                    print(f"❌ Connector Service health check failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Connector Service health check error: {e}")
    
    async def test_expense_processing(self):
        """Test expense processing with various messages"""
        print("\n🧪 Testing expense processing...")
        
        test_cases = [
            {
                "telegram_id": "123456789",
                "message": "Pizza 20 bucks",
                "expected_category": "Food"
            },
            {
                "telegram_id": "123456789",
                "message": "Gas 45.50",
                "expected_category": "Transportation"
            },
            {
                "telegram_id": "123456789",
                "message": "Netflix subscription 15.99",
                "expected_category": "Entertainment"
            },
            {
                "telegram_id": "123456789",
                "message": "Hello there",
                "expected_category": None  # Should be ignored
            },
            {
                "telegram_id": "999999999",  # Non-whitelisted user
                "message": "Pizza 20 bucks",
                "expected_category": None  # Should be unauthorized
            }
        ]
        
        async with httpx.AsyncClient() as client:
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n📝 Test case {i}: {test_case['message']}")
                
                try:
                    response = await client.post(
                        f"{self.bot_service_url}/process-expense",
                        json={
                            "telegram_id": test_case["telegram_id"],
                            "message": test_case["message"]
                        },
                        headers={"Content-Type": "application/json"}
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        print(f"   Status: {result.get('success')}")
                        print(f"   Message: {result.get('message')}")
                        
                        if result.get('success'):
                            category = result.get('category')
                            amount = result.get('amount')
                            description = result.get('description')
                            print(f"   Category: {category}")
                            print(f"   Amount: ${amount}")
                            print(f"   Description: {description}")
                            
                            if test_case["expected_category"]:
                                if category == test_case["expected_category"]:
                                    print("   ✅ Category matches expected")
                                else:
                                    print(f"   ⚠️  Category mismatch: expected {test_case['expected_category']}, got {category}")
                        else:
                            if test_case["expected_category"] is None:
                                print("   ✅ Correctly rejected non-expense/unauthorized message")
                            else:
                                print("   ❌ Unexpected failure")
                    else:
                        print(f"   ❌ HTTP Error: {response.status_code}")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
    
    async def test_categories_endpoint(self):
        """Test the categories endpoint"""
        print("\n📋 Testing categories endpoint...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.bot_service_url}/categories")
                if response.status_code == 200:
                    categories = response.json().get("categories", [])
                    print(f"✅ Available categories: {len(categories)}")
                    for category in categories:
                        print(f"   - {category}")
                else:
                    print(f"❌ Categories endpoint failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Categories endpoint error: {e}")
    
    async def test_connector_endpoints(self):
        """Test Connector Service endpoints"""
        print("\n🤖 Testing Connector Service endpoints...")
        
        async with httpx.AsyncClient() as client:
            # Test bot info
            try:
                response = await client.get(f"{self.connector_service_url}/bot-info")
                if response.status_code == 200:
                    bot_info = response.json()
                    print(f"✅ Bot info retrieved: @{bot_info.get('username')}")
                else:
                    print(f"❌ Bot info failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Bot info error: {e}")
            
            # Test webhook info
            try:
                response = await client.get(f"{self.connector_service_url}/webhook-info")
                if response.status_code == 200:
                    webhook_info = response.json()
                    print(f"✅ Webhook info retrieved: {webhook_info.get('url', 'Not set')}")
                else:
                    print(f"❌ Webhook info failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Webhook info error: {e}")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Telegram Expense Bot Tests")
        print("=" * 50)
        
        await self.test_health_endpoints()
        await self.test_expense_processing()
        await self.test_categories_endpoint()
        await self.test_connector_endpoints()
        
        print("\n" + "=" * 50)
        print("🏁 Tests completed!")

async def main():
    """Main test function"""
    tester = BotTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 