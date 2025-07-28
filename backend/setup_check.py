#!/usr/bin/env python3
"""
Setup check script for CourseAI backend
"""
import os
import sys
from pathlib import Path

def main():
    print("🔧 CourseAI Backend Setup Check")
    print("=" * 50)
    
    # Change to backend directory if needed
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if we have the required files
    if not Path("config.py").exists():
        print("❌ config.py not found in backend directory")
        sys.exit(1)
    
    # Import our modules
    try:
        from config import get_config, is_configured
        from api_client import test_api_connections
        
        # Check configuration
        config = get_config()
        config.print_status()
        
        if not is_configured():
            print("\n" + "=" * 50)
            print("❌ Configuration is incomplete!")
            print("\nTo fix this:")
            print("1. Copy .env.example to .env")
            print("2. Add your API keys to the .env file")
            print("3. Run this script again")
            print("\nMinimum required: OPENROUTER_API_KEY")
            return
        
        print("\n" + "=" * 50)
        print("🧪 Testing API Connections...")
        
        # Test API connections
        test_results = test_api_connections()
        
        for provider, result in test_results.items():
            if result["success"]:
                print(f"✅ {provider.title()}: {result['message']} ({result.get('response_time', 0):.2f}s)")
            else:
                print(f"❌ {provider.title()}: {result['message']}")
        
        # Check if at least one provider works
        working_providers = [p for p, r in test_results.items() if r["success"]]
        
        if working_providers:
            print(f"\n✅ Setup complete! Working providers: {', '.join(working_providers)}")
            print("\nYou can now start the backend server:")
            print("python -m uvicorn main_with_folders:app --reload --port 8000")
        else:
            print("\n❌ No working API providers found!")
            print("Please check your API keys and try again.")
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
    
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()