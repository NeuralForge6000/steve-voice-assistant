#!/bin/bash

echo "🍎 Steve Voice Assistant - macOS Installation Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is designed for macOS only${NC}"
    echo "For other platforms, use the generic installation script"
    exit 1
fi

echo -e "${GREEN}✅ Detected macOS $(sw_vers -productVersion)${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ from https://python.org or using Homebrew:"
    echo "  brew install python"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Found Python $PYTHON_VERSION${NC}"

# Check if version is 3.8+ but not 3.13+
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
PATCH=$(echo $PYTHON_VERSION | cut -d. -f3)

if [ "$MAJOR" -lt 3 ] || [ "$MAJOR" -eq 3 -a "$MINOR" -lt 8 ]; then
    echo -e "${RED}❌ Python 3.8 or higher is required${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
elif [ "$MAJOR" -eq 3 -a "$MINOR" -ge 13 ]; then
    echo -e "${RED}❌ CRITICAL: Python 3.13+ has known audio compatibility issues${NC}"
    echo "Current version: $PYTHON_VERSION"
    echo ""
    echo -e "${YELLOW}Steve Voice Assistant requires Python 3.8-3.12 for audio processing.${NC}"
    echo "Python 3.13+ breaks Whisper and audio libraries."
    echo ""
    echo "To fix this:"
    echo "1. Install Python 3.11: brew install python@3.11"
    echo "2. Switch to it: brew unlink python && brew link python@3.11"
    echo "3. Or use pyenv: pyenv install 3.11.9 && pyenv local 3.11.9"
    echo ""
    read -p "Continue anyway? (not recommended) (y/n): " CONTINUE_ANYWAY
    if [[ ! $CONTINUE_ANYWAY =~ ^[Yy]$ ]]; then
        echo "Please downgrade Python and run this script again."
        exit 1
    fi
    echo -e "${YELLOW}⚠️ Continuing with unsupported Python version...${NC}"
elif [ "$MAJOR" -eq 3 -a "$MINOR" -eq 12 ]; then
    echo -e "${YELLOW}⚠️ Python 3.12 detected - should work but 3.11 is preferred${NC}"
else
    echo -e "${GREEN}✅ Python version compatible${NC}"
fi

# Check for Homebrew and offer to install it
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}⚠️ Homebrew not found${NC}"
    echo "Homebrew is the package manager for macOS and is needed for PortAudio."
    echo ""
    read -p "Install Homebrew now? (strongly recommended) (y/n): " INSTALL_BREW
    
    if [[ $INSTALL_BREW =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}📦 Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH
        echo -e "${BLUE}🔧 Adding Homebrew to PATH...${NC}"
        if [[ -f "/opt/homebrew/bin/brew" ]]; then
            # Apple Silicon Mac
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        elif [[ -f "/usr/local/bin/brew" ]]; then
            # Intel Mac
            echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/usr/local/bin/brew shellenv)"
        fi
        
        # Verify Homebrew installation
        if command -v brew &> /dev/null; then
            echo -e "${GREEN}✅ Homebrew installed successfully${NC}"
        else
            echo -e "${RED}❌ Homebrew installation failed${NC}"
            echo "Please install manually from https://brew.sh"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️ Continuing without Homebrew${NC}"
        echo "You may need to install PortAudio manually if PyAudio fails"
    fi
else
    echo -e "${GREEN}✅ Homebrew found: $(brew --version | head -1)${NC}"
fi

# Install system dependencies
echo -e "${BLUE}📦 Installing system dependencies...${NC}"

if command -v brew &> /dev/null; then
    echo "Installing PortAudio for PyAudio..."
    brew install portaudio
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ PortAudio installed${NC}"
    else
        echo -e "${YELLOW}⚠️ PortAudio installation had issues, but continuing...${NC}"
    fi
    
    echo "Installing FFmpeg for audio processing..."
    brew install ffmpeg
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ FFmpeg installed${NC}"
    else
        echo -e "${YELLOW}⚠️ FFmpeg installation had issues, but continuing...${NC}"
    fi
    
    echo -e "${GREEN}✅ System dependencies installation completed${NC}"
else
    echo -e "${YELLOW}⚠️ Homebrew not available, skipping system dependencies${NC}"
    echo "If PyAudio installation fails, install PortAudio with:"
    echo "  brew install portaudio"
fi

# Check for Metal GPU support
echo -e "${BLUE}🔍 Checking for Metal GPU support...${NC}"
if system_profiler SPDisplaysDataType 2>/dev/null | grep -i metal > /dev/null; then
    echo -e "${GREEN}✅ Metal GPU support detected - AI processing will be accelerated${NC}"
else
    echo -e "${YELLOW}⚠️ Metal GPU support not detected - will use CPU processing${NC}"
fi

# Ask about virtual environment
echo ""
read -p "Create virtual environment? (recommended for isolation) (y/n): " USE_VENV

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv steve_env
    source steve_env/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
fi

# Upgrade pip
echo -e "${BLUE}📦 Upgrading pip...${NC}"
python3 -m pip install --upgrade pip

# Install Python dependencies with better error handling
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"

# Try to install PyAudio with different methods
echo "Installing PyAudio (this might take a moment)..."
if ! python3 -m pip install pyaudio; then
    echo -e "${YELLOW}⚠️ Standard PyAudio installation failed, trying alternative method...${NC}"
    
    if command -v brew &> /dev/null; then
        # Try with explicit paths for Homebrew
        if [[ -d "/opt/homebrew" ]]; then
            # Apple Silicon
            python3 -m pip install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
        else
            # Intel Mac
            python3 -m pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
        fi
    fi
fi

# Install other dependencies
echo "Installing other Python packages..."
python3 -m pip install numpy pyttsx3 faster-whisper google-generativeai psutil cryptography

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install some dependencies${NC}"
    echo ""
    echo "Common solutions:"
    echo "1. Install PortAudio: brew install portaudio"
    echo "2. Install Xcode command line tools: xcode-select --install"
    echo "3. Update pip: python3 -m pip install --upgrade pip"
    echo "4. Try manual installation: pip3 install pyaudio numpy pyttsx3"
    exit 1
fi

# Check API key setup
echo -e "${BLUE}🔑 Checking API key setup...${NC}"
if [[ -z "$GOOGLE_AI_API_KEY" ]]; then
    echo -e "${YELLOW}⚠️ Google AI API key not found${NC}"
    echo ""
    echo "To set up your API key:"
    echo "1. Get your key from: https://aistudio.google.com/"
    echo "2. Set it permanently:"
    echo "   echo 'export GOOGLE_AI_API_KEY=\"your_key_here\"' >> ~/.zprofile"
    echo "   source ~/.zprofile"
    echo ""
    read -p "Enter your Google AI API key now (or press Enter to skip): " API_KEY
    
    if [[ ! -z "$API_KEY" ]]; then
        echo "export GOOGLE_AI_API_KEY=\"$API_KEY\"" >> ~/.zprofile
        export GOOGLE_AI_API_KEY="$API_KEY"
        echo -e "${GREEN}✅ API key set${NC}"
    else
        echo -e "${YELLOW}⚠️ API key not set - you'll need to set it before running Steve${NC}"
    fi
else
    echo -e "${GREEN}✅ Google AI API key found${NC}"
fi

# Run setup script
echo -e "${BLUE}🔧 Running setup script...${NC}"
if [[ -f "setup.py" ]]; then
    python3 setup.py
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️ Setup completed with warnings${NC}"
    else
        echo -e "${GREEN}✅ Setup completed successfully!${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ setup.py not found, skipping setup script${NC}"
fi

# Test the installation
echo -e "${BLUE}🧪 Testing installation...${NC}"
if [[ -f "test_platform.py" ]]; then
    python3 test_platform.py
else
    echo -e "${YELLOW}⚠️ test_platform.py not found, skipping tests${NC}"
fi

echo ""
echo -e "${GREEN}🎉 macOS Installation complete!${NC}"
echo ""
echo -e "${PURPLE}macOS-specific features enabled:${NC}"
echo "• 🍎 Native macOS voice support (Alex, Tom, Daniel, etc.)"
echo "• 🎵 PyAudio-based audio chimes (no winsound dependency)"
echo "• ⚡ Metal GPU acceleration for Whisper (if available)"
echo "• 🔒 macOS-native file permissions and security"
echo ""
echo -e "${BLUE}Next steps:${NC}"
if [[ -z "$GOOGLE_AI_API_KEY" ]]; then
    echo "1. ⚠️ Set your Google AI API key (see instructions above)"
else
    echo "1. ✅ API key is set"
fi
echo "2. Grant microphone permissions when prompted"
echo "3. Run: python3 steve_voice_assistant.py"
echo "4. Say \"Hey Steve\" to start chatting!"
echo ""

if [[ $USE_VENV =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}📝 Virtual Environment Note:${NC}"
    echo "To activate the virtual environment later, run:"
    echo "   source steve_env/bin/activate"
    echo ""
fi

echo -e "${BLUE}🔐 Security Notes:${NC}"
echo "• On first run, macOS will ask for microphone permissions"
echo "• This is required for voice recognition to work"
echo "• Your conversations are encrypted and stored locally only"
echo "• You can manage permissions in System Preferences > Security & Privacy"
echo ""

# Check microphone permissions (macOS Monterey+)
MACOS_VERSION=$(sw_vers -productVersion | cut -d. -f1)
if [[ $MACOS_VERSION -ge 12 ]]; then
    echo -e "${YELLOW}💡 Tip for macOS 12+:${NC}"
    echo "Manage microphone permissions in:"
    echo "   System Preferences > Security & Privacy > Privacy > Microphone"
fi

echo -e "${GREEN}Ready to chat with Steve! 🤖✨${NC}"