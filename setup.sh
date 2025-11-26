#!/bin/bash

# Setup script for AI Image Classifier

set -e  # Exit on error

echo "🚀 Setting up AI Image Classifier..."
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "✓ pip upgraded"

# Install dependencies
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "⚠️  requirements.txt not found"
    exit 1
fi

# Check for Git LFS
echo "📋 Checking for Git LFS..."
if command -v git-lfs &> /dev/null; then
    echo "✓ Git LFS is installed"
    echo "📥 Pulling Git LFS files..."
    git lfs pull > /dev/null 2>&1
    echo "✓ Git LFS files pulled"
else
    echo "⚠️  Git LFS is not installed"
    echo "   Please install Git LFS: https://git-lfs.github.com/"
    echo "   Then run: git lfs pull"
fi

# Check model file
echo "📋 Checking model file..."
if [ -f "AIGeneratedModel.h5" ]; then
    file_type=$(file AIGeneratedModel.h5)
    file_size=$(ls -lh AIGeneratedModel.h5 | awk '{print $5}')
    
    if echo "$file_type" | grep -q "ASCII text"; then
        echo "⚠️  Model file is Git LFS pointer (not downloaded)"
        echo "   Run: git lfs pull"
    else
        echo "✓ Model file found ($file_size)"
    fi
else
    echo "❌ Model file not found"
    exit 1
fi

# Check Streamlit config
echo "📋 Checking Streamlit configuration..."
if [ -f ".streamlit/config.toml" ]; then
    echo "✓ Streamlit config found"
else
    echo "⚠️  Streamlit config not found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the app, execute:"
echo "   streamlit run main.py"
echo ""
echo "Or visit http://localhost:8501 in your browser"
echo ""
