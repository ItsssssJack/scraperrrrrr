#!/bin/bash
# Quick Start Script for AI News Dashboard

echo "🚀 AI News Dashboard - Quick Start"
echo "===================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up Supabase (see SUPABASE_SETUP.md)"
echo "2. Configure .env file with your credentials"
echo "3. Run scrapers: python tools/orchestrator.py"
echo "4. Start dashboard: python -m http.server 8000"
echo ""
echo "💡 Tip: Keep this terminal open and run commands from here"
echo ""
