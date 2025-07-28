#!/usr/bin/env python3.12
"""
Test single module creation to verify the fix
"""
import asyncio
import sys
import os
from pathlib import Path

async def test_single_module():
    """Test creating a single module to verify the fix works"""
    
    # Change to backend directory and activate venv
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        from main_with_folders import SequentialCourseCreationSystemWithFolders
        
        print("🧪 Testing Single Module Creation")
        print("=" * 50)
        
        # Create a test system
        session_id = "test_session"
        topic = "Test Course"
        system = SequentialCourseCreationSystemWithFolders(session_id, topic, 1, 1)
        
        # Test module info
        module_info = {
            "filename": "test_module.md",
            "title": "Test Module",
            "subtopics": ["Basic concepts", "Examples"],
            "objectives": ["Understand basics"],
            "difficulty": "Beginner"
        }
        
        print("🚀 Creating test module...")
        
        try:
            # Test the method that was failing
            content = await system.create_single_module_content(module_info, 1, 1)
            
            if "Error generating content:" in content:
                print(f"❌ Still getting errors: {content[:200]}...")
                return False
            else:
                print("✅ Module created successfully!")
                print(f"Content length: {len(content)} characters")
                print(f"First 200 characters: {content[:200]}...")
                return True
                
        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_single_module())
    sys.exit(0 if success else 1)