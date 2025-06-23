#!/bin/bash

echo "🤖 Steve Voice Assistant - Quick Install Script"
echo "==============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    echo "Please install Python 3.8+ from https://python.org"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Check if version is 3.8+
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 8 ]; then
    echo -e "${RED}❌ Python 3.8 or higher is required${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Ask about virtual environment
read -p "Create virtual environment? (y/n): " USE_VENV

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv steve_env
    source steve_env/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
fi

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
python3 -m pip install --upgrade pip

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Run setup script
echo -e "${BLUE}🔧 Running setup...${NC}"
python3 setup.py

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️ Setup completed with warnings${NC}"
else
    echo -e "${GREEN}✅ Setup completed successfully!${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Add your Google AI API key to .env file"
echo "2. Run: python3 steve_voice_assistant.py"
echo "3. Say \"Hey Steve\" to start chatting!"
echo ""

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📝 Note: To activate the virtual environment later, run:${NC}"
    echo "   source steve_env/bin/activate"
    echo ""
fi

# Make the script executable
chmod +x quick_install.sh