#!/bin/bash

echo "🎵 GarageBand Voice Controller Setup"
echo "===================================="

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This application requires macOS"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "⚠️  Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install system dependencies
echo "📦 Installing system dependencies..."
brew install portaudio

# Install Python dependencies
echo "🐍 Installing Python packages..."
pip3 install speechrecognition pyaudio pynput websockets

# Check if GarageBand is installed
if [ ! -d "/Applications/GarageBand.app" ]; then
    echo "⚠️  GarageBand not found in Applications folder"
    echo "Please install GarageBand from the Mac App Store"
else
    echo "✅ GarageBand found"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the application:"
echo "  python3 start_servers.py"
echo ""
echo "Then open http://localhost:8000 in your browser"
echo ""
echo "Make sure to:"
echo "1. Keep GarageBand open and focused"
echo "2. Grant microphone permissions to your browser"
echo "3. Grant accessibility permissions to Terminal in System Preferences" 