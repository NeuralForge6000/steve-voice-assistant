# 🤖 Steve Voice Assistant

A secure, intelligent voice assistant powered by OpenAI Whisper and Google Gemini AI, designed for local desktop use with enterprise-grade security features.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Security](https://img.shields.io/badge/Security-Enhanced-red.svg)

## ✨ Features

### 🌍 **Cross-Platform Support**
- **🪟 Windows**: Native winsound audio + Windows voices (David, Mark, Zira)
- **🍎 macOS**: PyAudio tones + macOS voices (Alex, Tom, Daniel) + Metal GPU acceleration
- **🐧 Linux**: PyAudio tones + available system voices

### 🎙️ **Core Voice Capabilities**
- **Wake Word Detection**: Say "Hey Steve" to start conversations
- **Continuous Conversation Mode**: Natural back-and-forth without repeating wake words
- **GPU-Accelerated Speech Recognition**: Uses OpenAI Whisper with CUDA/Metal support
- **Natural Text-to-Speech**: Platform-native voice synthesis with voice selection
- **Smart Audio Processing**: Automatic silence detection and noise handling

### 🧠 **AI-Powered Responses**
- **Google Gemini 1.5 Pro Integration**: Advanced conversational AI
- **Conversation Memory**: Maintains context throughout sessions
- **Cost Tracking**: Real-time API usage and cost monitoring
- **Smart Context Management**: Automatic history optimization

### 🔒 **Enterprise Security Features**
- **🛡️ Prompt Injection Protection**: Advanced input sanitization
- **🔐 Encrypted Data Storage**: All conversation history encrypted at rest
- **🗂️ Secure File Handling**: Temporary files with secure deletion
- **📊 Resource Monitoring**: System resource limits and monitoring
- **🚨 Audit Logging**: Comprehensive security event logging
- **⚡ API Rate Limiting**: Configurable usage limits and cost controls

### 🎵 **Enhanced User Experience**
- **Soothing Audio Chimes**: Gentle, musical notification sounds
- **Real-time Feedback**: Visual indicators for speech detection
- **Configurable Settings**: Extensive customization options
- **Session Analytics**: Detailed cost and usage reporting

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 to 3.12** (⚠️ **Avoid Python 3.13+** - known audio compatibility issues)
- Microphone access
- NVIDIA GPU (optional, for faster speech recognition)
- Google AI Studio API key

**⚠️ Important Python Version Note:**
- **✅ Recommended**: Python 3.10 or 3.11 
- **❌ Avoid**: Python 3.13+ (audio/Whisper compatibility issues)
- **⚠️ Minimum**: Python 3.8 (some features may be limited)

**Platform-specific requirements:**
- **Windows**: No additional requirements
- **macOS**: Homebrew recommended (`brew install portaudio`)
- **Linux**: `sudo apt-get install portaudio19-dev`

### Installation

#### 🍎 **macOS Installation (Detailed)**

**Quick Start:**
```bash
# Run the automated installer
git clone https://github.com/NeuralForge6000/steve-voice-assistant.git
cd steve-voice-assistant
chmod +x install_macos.sh
./install_macos.sh
```

**For detailed step-by-step instructions, see [MACOS_SETUP.md](MACOS_SETUP.md)**

**Common macOS Requirements:**
- Homebrew (installer will offer to install this)
- PortAudio (via `brew install portaudio`)
- Microphone permissions (granted during first run)

**macOS-Specific Features:**
- 🍎 Native macOS voices (Alex, Tom, Daniel)
- ⚡ Metal GPU acceleration for Whisper
- 🎵 Native PyAudio audio chimes
- 🔒 macOS security permissions integration

#### 🪟 **Windows Installation**
```bash
# Clone the repository
git clone https://github.com/NeuralForge6000/steve-voice-assistant.git
cd steve-voice-assistant

# Run the Windows installer
quick_install.bat
```

#### 🐧 **Linux Installation**
```bash
# Install system dependencies first
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio

# Clone the repository
git clone https://github.com/NeuralForge6000/steve-voice-assistant.git
cd steve-voice-assistant

# Run the installer
chmod +x quick_install.sh
./quick_install.sh
```

#### 📦 **Manual Installation (All Platforms)**
```bash
# Clone the repository
git clone https://github.com/yourusername/steve-voice-assistant.git
cd steve-voice-assistant

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py
```

### Getting Your Google AI API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and set it as an environment variable

## 💬 Usage

### Basic Conversation
1. **Start**: Say "Hey Steve" to wake up the assistant
2. **Talk**: Speak naturally - Steve will remember the conversation context
3. **End**: Say "Goodbye Steve" to end the conversation

### Example Interaction
```
You: "Hey Steve, what's the weather like today?"
Steve: "I'd be happy to help, but I don't have access to current weather data. You might want to check a weather app or website for today's forecast."

You: "Can you help me plan a workout routine?"
Steve: "Absolutely! I can suggest a balanced routine. Are you looking for strength training, cardio, or a combination of both?"
```

### Advanced Features
- **Voice Calibration**: Automatic audio level calibration on startup
- **Resource Monitoring**: Built-in system resource protection
- **Cost Tracking**: Real-time API usage and cost display
- **Security Logging**: All interactions logged for security audit

## ⚙️ Configuration

### Security Settings
```python
# Customize security parameters
assistant.MAX_DAILY_API_CALLS = 100        # API call limit per day
assistant.MAX_SESSION_COST = 2.00          # Maximum cost per session
assistant.COST_WARNING_THRESHOLD = 0.50    # Cost warning threshold
assistant.MIN_DISK_SPACE_MB = 200          # Required free disk space
assistant.MAX_MEMORY_PERCENT = 85          # Memory usage limit
```

### Conversation Settings
```python
# Customize conversation behavior
assistant.ENABLE_HISTORY = True            # Enable conversation memory
assistant.MAX_CONVERSATION_TURNS = 20      # Maximum conversation history
assistant.MAX_HISTORY_TOKENS = 8000        # Token limit for history
```

### Audio Settings
```python
# Customize audio behavior
assistant.ENABLE_CHIMES = True             # Enable audio feedback
assistant.SILENCE_DURATION = 4.0           # Silence detection timeout
assistant.SILENCE_THRESHOLD = 150          # Audio level threshold
```

## 🛡️ Security Features

### Data Protection
- **Encryption**: All conversation history encrypted using Fernet symmetric encryption
- **Secure Deletion**: Temporary audio files overwritten with random data before deletion
- **Memory Protection**: Sensitive data cleared from memory on cleanup
- **Access Control**: Temporary files created with owner-only permissions

### Input Validation
- **Prompt Injection Protection**: Advanced pattern detection and filtering
- **Input Sanitization**: Malicious content removed before processing
- **Length Limiting**: Input size restrictions to prevent abuse
- **Content Filtering**: HTML/XML tag removal and dangerous phrase detection

### Monitoring & Logging
- **Resource Monitoring**: Real-time system resource usage tracking
- **Security Events**: Comprehensive audit logging of security-relevant events
- **Error Handling**: Secure error messages without information disclosure
- **Usage Tracking**: API call monitoring with rate limiting

### Cost Controls
- **Daily Limits**: Configurable daily API call limits
- **Hourly Limits**: Burst protection with hourly rate limiting
- **Cost Thresholds**: Session cost limits with real-time tracking
- **Usage Alerts**: Automatic warnings when approaching limits

## 📊 API Cost Information

### Google Gemini 1.5 Pro Pricing
- **Input tokens**: $3.50 per 1M tokens
- **Output tokens**: $10.50 per 1M tokens

### Estimated Costs
- **Simple conversation (5 turns)**: ~$0.01
- **Extended conversation (20 turns)**: ~$0.05
- **Daily usage (50 interactions)**: ~$0.25

*Costs may vary based on conversation length and complexity*

## 🔧 Troubleshooting

### Python Version Issues

**"Whisper not working" or "Audio processing fails"**
```bash
# Check your Python version
python3 --version

# If you have Python 3.13+, downgrade to Python 3.11:
# macOS with Homebrew:
brew install python@3.11
brew unlink python@3.12  # or whatever version you have
brew link python@3.11

# Or use pyenv:
pyenv install 3.11.9
pyenv local 3.11.9
```

**Known Python Version Compatibility:**
- ✅ **Python 3.10.x**: Excellent compatibility
- ✅ **Python 3.11.x**: Recommended (best performance)
- ⚠️ **Python 3.12.x**: Usually works, some edge cases
- ❌ **Python 3.13.x**: Audio library conflicts, Whisper issues
- ❌ **Python 3.14+**: Not tested, likely incompatible

### Common Issues

**"brew: command not found" (macOS)**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile
```

**"No module named 'pyaudio'" (macOS)**
```bash
# Install PortAudio first, then PyAudio
brew install portaudio
pip3 install pyaudio

# If still failing, try:
pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio
```

**"API key not found"**
```bash
# Set environment variable (permanent method)
echo 'export GOOGLE_AI_API_KEY="your_key_here"' >> ~/.zprofile
source ~/.zprofile

# Verify it's set
echo $GOOGLE_AI_API_KEY

# Alternative: Create .env file
echo "GOOGLE_AI_API_KEY=your_key_here" > .env
```

**"Permission denied" for microphone (macOS)**
- Go to **System Preferences > Security & Privacy > Privacy > Microphone**
- Allow Terminal or your Python app to access microphone
- Restart Terminal after granting permission

**"CUDA not available"**
- GPU acceleration will fallback to CPU automatically
- Install CUDA toolkit for GPU support (optional)

**Audio issues**
- Check microphone permissions
- Ensure audio drivers are up to date
- Try running audio calibration
- Test with: `python3 test_platform.py`
- **If using Python 3.13+**: Downgrade to Python 3.11

### Performance Optimization
- **GPU**: Install CUDA for faster speech recognition
- **Memory**: Disable conversation history for lower memory usage
- **Storage**: Increase minimum disk space if running low

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `pip install -r requirements-dev.txt`
4. Make your changes
5. Run tests: `python -m pytest`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔐 Security

For security-related issues, please see our [Security Policy](SECURITY.md).

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [macOS Setup Guide](MACOS_SETUP.md)
- [**Compatibility Guide**](COMPATIBILITY.md) ⚠️ **Important: Python 3.13+ issues**
- [Configuration Reference](docs/configuration.md)
- [Security Guide](docs/security.md)
- [API Reference](docs/api.md)

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [Google Generative AI](https://ai.google.dev/) - Language model
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3) - Text-to-speech
- [cryptography](https://cryptography.io/) - Encryption library

## 📈 Roadmap

- [x] ✅ **Cross-platform support** (Windows, macOS, Linux)
- [x] ✅ **Enterprise-grade security features**
- [x] ✅ **Real-time cost monitoring**
- [ ] 🌐 **Web interface for remote access**
- [ ] 🔌 **Plugin system for extensibility**
- [ ] 🗣️ **Voice authentication and user profiles**
- [ ] 🤖 **Local AI model support (offline mode)**
- [ ] 🌍 **Multi-language support**
- [ ] ☁️ **Cloud deployment options**
- [ ] 📱 **Mobile companion app**

---

**Made with ❤️ for secure, intelligent voice interaction**