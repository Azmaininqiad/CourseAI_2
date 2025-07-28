#!/usr/bin/env python3.12
"""
Test API connection directly
"""
import asyncio
import sys
import os
from pathlib import Path

async def test_api_direct():
    """Test API connection directly"""
    
    # Change to backend directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        from api_client import call_ai_api
        
        print("🧪 Testing Direct API Call")
        print("=" * 50)
        
        # Simple test message
        messages = [
            {"role": "user", "content": "Hello! Please respond with exactly: 'API test successful'"}
        ]
        
        print("🚀 Making API call...")
        
        try:
            result = await call_ai_api(messages)
            print(f"✅ Success! Response: {result}")
            
            if "api test successful" in result.lower():
                print("✅ API responded correctly")
                return True
            else:
                print("⚠️ API responded but with different content")
                return True  # Still working, just different response
                
        except Exception as e:
            print(f"❌ API call failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_direct())
    sys.exit(0 if success else 1)