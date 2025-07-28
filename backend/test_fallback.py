#!/usr/bin/env python3
"""
Test the fallback mechanism between providers
"""
import asyncio
import os
from pathlib import Path

async def test_fallback():
    """Test the fallback mechanism"""
    
    # Change to backend directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        from api_client import call_ai_api
        from config import get_config
        
        config = get_config()
        
        print("🧪 Testing AI Provider Fallback Mechanism")
        print("=" * 50)
        
        # Show configured providers
        primary = config.get_primary_provider()
        fallbacks = config.get_fallback_providers()
        
        print(f"Primary provider: {primary.name if primary else 'None'}")
        print(f"Fallback providers: {[p.name for p in fallbacks]}")
        print()
        
        # Test a simple message
        test_messages = [
            {"role": "user", "content": "Hello! Please respond with exactly: 'Fallback test successful'"}
        ]
        
        print("🚀 Testing API call with fallback...")
        
        try:
            response = await call_ai_api(test_messages)
            print(f"✅ Success! Response: {response}")
            
            # Test which provider was used
            if "fallback test successful" in response.lower():
                print("✅ Provider responded correctly")
            else:
                print("⚠️ Provider responded but with different content")
                
        except Exception as e:
            print(f"❌ All providers failed: {e}")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the backend directory")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_fallback())