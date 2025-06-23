# 🍎 macOS Setup Guide for Steve Voice Assistant

This guide walks you through setting up Steve Voice Assistant on macOS, including all the common issues you might encounter.

## 📋 **Prerequisites**

- macOS 10.14 or later
- Python 3.8 or higher
- Microphone access
- Internet connection for API calls

## 🔍 **Step 0: Check Your System**

```bash
# Check macOS version
sw_vers -productVersion

# Check Python version
python3 --version
# Should show Python 3.8 or higher

# Check if Homebrew is installed
brew --version
# If you see "command not found", continue to Step 1
```

## 🍺 **Step 1: Install Homebrew**

Homebrew is macOS's package manager. Most Mac users don't have it by default.

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**After installation, you'll see instructions like this:**
```bash
# Add Homebrew to your PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Important:** Copy and run the exact commands Homebrew shows you (paths might vary).

**Verify installation:**
```bash
brew --version
# Should show: Homebrew 4.x.x
```

## 🔧 **Step 2: Install System Dependencies**

```bash
# Install PortAudio (required for microphone/speaker access)
brew install portaudio

# Install FFmpeg (optional, for better audio processing)
brew install ffmpeg

# Check Metal GPU support (Steve can use this for acceleration)
system_profiler SPDisplaysDataType | grep -i metal
# If you see "Metal" in the output, you have GPU acceleration!
```

## 📥 **Step 3: Download Steve Voice Assistant**

```bash
# Clone the repository
git clone https://github.com/NeuralForge6000/steve-voice-assistant.git
cd steve-voice-assistant

# List files to make sure it downloaded correctly
ls -la
# You should see files like steve_voice_assistant.py, requirements.txt, etc.
```

## 🐍 **Step 4: Install Python Dependencies**

```bash
# Install all required Python packages
pip3 install -r requirements.txt
```

**If PyAudio installation fails, try:**
```bash
# Method 1: Install with specific compiler flags
pip3 install --global-option='build_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio

# Method 2: Install other packages first, then PyAudio
pip3 install numpy
brew install portaudio
pip3 install pyaudio

# Method 3: Use conda if you have it
conda install pyaudio
```

## 🔑 **Step 5: Get and Set Your Google AI API Key**

### **Get Your API Key:**
1. Go to https://aistudio.google.com/
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the key (looks like: `AIzaSyC7b2KvXYZ...`)

### **Set Your API Key (Choose One Method):**

**Method A: Permanent Environment Variable (Recommended)**
```bash
# Add to your shell profile (persists across restarts)
echo 'export GOOGLE_AI_API_KEY="AIzaSyC7b2KvXYZ_replace_with_your_actual_key"' >> ~/.zprofile

# Reload your profile
source ~/.zprofile

# Test that it's set
echo $GOOGLE_AI_API_KEY
# Should show your API key
```

**Method B: .env File (Alternative)**
```bash
# Create a secure .env file
echo "GOOGLE_AI_API_KEY=AIzaSyC7b2KvXYZ_replace_with_your_actual_key" > .env

# Make it secure (only you can read it)
chmod 600 .env

# Verify it was created
cat .env
```

**Method C: Temporary (Testing Only)**
```bash
# Only lasts for current terminal session
export GOOGLE_AI_API_KEY="AIzaSyC7b2KvXYZ_replace_with_your_actual_key"
```

## 🧪 **Step 6: Test Your Setup**

```bash
# Run the platform test
python3 test_platform.py
```

**Expected output:**
```
✅ PyAudio available
✅ NumPy available
✅ pyttsx3 available
✅ Found X input device(s)
✅ Found X output device(s)
✅ Metal GPU support detected
🎉 All tests passed! Steve should work great on your system.
```

## 🚀 **Step 7: Run Steve**

```bash
# Start the voice assistant
python3 steve_voice_assistant.py
```

**First time setup:**
1. **Grant microphone permission** when macOS asks
2. **Audio calibration** - speak normally for 5 seconds when prompted
3. **Wait for "Voice Assistant Ready!"**
4. **Say "Hey Steve"** to start a conversation!

## 🎵 **macOS-Specific Features**

Steve on macOS includes special optimizations:

- **🍎 Native macOS Voices**: Alex, Tom, Daniel, and others
- **⚡ Metal GPU Acceleration**: Faster speech recognition if you have compatible hardware
- **🎶 PyAudio Audio Chimes**: Beautiful, generated tones (no system dependency)
- **🔒 macOS Security Integration**: Proper permission handling

## 🚨 **Common Issues & Solutions**

### **"brew: command not found"**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Follow the PATH instructions Homebrew gives you
```

### **"No module named 'pyaudio'"**
```bash
# Install PortAudio first
brew install portaudio

# Then install PyAudio
pip3 install pyaudio
```

### **"API key not found"**
```bash
# Check if it's set
echo $GOOGLE_AI_API_KEY

# If empty, set it again
echo 'export GOOGLE_AI_API_KEY="your_key_here"' >> ~/.zprofile
source ~/.zprofile
```

### **"Permission denied" for microphone**
1. Go to **Apple menu > System Preferences**
2. Click **Security & Privacy**
3. Click **Privacy** tab
4. Select **Microphone** from the list
5. Check the box next to **Terminal** (or your Python app)
6. Restart Terminal

### **Audio sounds weird or doesn't work**
```bash
# Test your setup
python3 test_platform.py

# Try different voice
# Steve will show available voices on startup and auto-select the best one
```

### **Steve responds very slowly**
- **With Metal GPU**: Should be very fast
- **Without GPU**: Will use CPU (slower but still works)
- **Check internet**: API calls need internet connection

## 🎯 **Quick Start Commands**

Once everything is installed:

```bash
# Navigate to Steve's directory
cd steve-voice-assistant

# Set API key (if not already set)
export GOOGLE_AI_API_KEY="your_key_here"

# Run Steve
python3 steve_voice_assistant.py

# Say "Hey Steve" when ready!
```

## 🆘 **Still Having Issues?**

1. **Run the test script**: `python3 test_platform.py`
2. **Check the main troubleshooting guide**: See README.md
3. **Update everything**:
   ```bash
   brew update
   pip3 install --upgrade pip
   pip3 install --upgrade -r requirements.txt
   ```

## 🎉 **Success!**

When everything works, you'll see:
```
🤖 Steve Voice Assistant Ready!
💬 Say: 'hey steve' to start a conversation
🛑 Press Ctrl+C to exit
```

**Say "Hey Steve" and start chatting!** 🗣️

---

**Made with ❤️ for Mac users who want a secure, intelligent voice assistant!**