#!/bin/bash
# Install backend requirements

echo "🔧 Installing CourseAI Backend Requirements"
echo "=" * 50

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment detected: $VIRTUAL_ENV"
else
    echo "⚠️ No virtual environment detected. Consider using one:"
    echo "python3 -m venv venv"
    echo "source venv/bin/activate"
    echo ""
fi

# Install requirements
echo "📦 Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 To start the server:"
echo "python3 -m uvicorn main_with_folders:app --reload --port 8000"