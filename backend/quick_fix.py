#!/usr/bin/env python3
"""
Quick fix for the 401 authentication error
"""
import requests
import json

def test_openrouter_key():
    """Test the OpenRouter API key directly"""
    
    # Load API key from .env file
    import os
    from pathlib import Path
    
    # Load .env file
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if key == 'OPENROUTER_API_KEY':
                        os.environ[key] = value.strip('"\'')
    
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://courseai.app",
        "X-Title": "CourseAI Course Creator"
    }
    
    payload = {
        "model": "deepseek/deepseek-r1-0528:free",
        "messages": [
            {"role": "user", "content": "Hello, this is a test. Please respond with 'Test successful'."}
        ],
        "max_tokens": 100,
        "temperature": 0.8
    }
    
    print("🧪 Testing OpenRouter API key...")
    print(f"API Key: {api_key[:20]}...")
    
    if not api_key:
        print("❌ No API key found in .env file")
        return False
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✅ Success! Response: {content}")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def get_new_api_key_instructions():
    """Show instructions for getting a new API key"""
    print("\n" + "="*60)
    print("🔑 How to get a new OpenRouter API key:")
    print("="*60)
    print("1. Go to https://openrouter.ai/")
    print("2. Sign up or log in to your account")
    print("3. Go to https://openrouter.ai/keys")
    print("4. Click 'Create Key'")
    print("5. Copy the new API key")
    print("6. Replace the OPENROUTER_API_KEY in your .env file")
    print("\nAlternatively, you can use other providers:")
    print("• OpenAI: https://platform.openai.com/api-keys")
    print("• Anthropic: https://console.anthropic.com/")

if __name__ == "__main__":
    print("🔧 Quick Fix for 401 Authentication Error")
    print("="*60)
    
    success = test_openrouter_key()
    
    if not success:
        print("\n❌ The API key is not working.")
        print("This could be because:")
        print("• The API key has expired")
        print("• The API key is invalid")
        print("• The API key has reached its usage limit")
        print("• There's a temporary issue with OpenRouter")
        
        get_new_api_key_instructions()
        
        print("\n" + "="*60)
        print("🛠️ Quick Fix Steps:")
        print("="*60)
        print("1. Get a new API key from OpenRouter (see instructions above)")
        print("2. Update the OPENROUTER_API_KEY in backend/.env")
        print("3. Restart your backend server")
        print("4. Try creating a course again")
    else:
        print("\n✅ API key is working! The issue might be elsewhere.")
        print("Try restarting your backend server and creating a course again.")