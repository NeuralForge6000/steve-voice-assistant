# 🔧 Steve Voice Assistant - Compatibility Guide

## 🐍 Python Version Compatibility

| Python Version | Status | Notes |
|---------------|--------|-------|
| **3.8.x** | ✅ Supported | Minimum version, basic functionality |
| **3.9.x** | ✅ Supported | Good compatibility |
| **3.10.x** | ✅ **Recommended** | Excellent performance and stability |
| **3.11.x** | ✅ **Recommended** | Best performance, optimal choice |
| **3.12.x** | ⚠️ Usually OK | Generally works, some edge cases |
| **3.13.x** | ❌ **BROKEN** | Audio library conflicts, Whisper fails |
| **3.14+** | ❌ **BROKEN** | Not tested, likely incompatible |

### ⚠️ **Critical Issue: Python 3.13+**

Python 3.13 introduced changes that break several audio processing libraries:

**Symptoms:**
- Whisper fails to load or process audio
- PyAudio crashes during initialization
- Audio file processing errors
- "Module not found" errors for audio dependencies

**Solution:**
```bash
# Check your Python version
python3 --version

# If 3.13+, downgrade to 3.11:

# macOS with Homebrew:
brew install python@3.11
brew unlink python
brew link python@3.11

# Using pyenv (all platforms):
pyenv install 3.11.9
pyenv local 3.11.9

# Verify the change:
python3 --version  # Should show 3.11.x
```

## 🖥️ Platform Compatibility

### **Windows**
| Version | Status | Notes |
|---------|--------|-------|
| Windows 10 | ✅ Fully Supported | Recommended |
| Windows 11 | ✅ Fully Supported | Excellent |
| Windows 8.1 | ⚠️ Limited | May work but not tested |
| Windows 7 | ❌ Not Supported | Python 3.8+ not supported |

**Windows Features:**
- Native `winsound` audio chimes
- Windows TTS voices (David, Mark, Zira)
- CUDA GPU acceleration (with compatible hardware)

### **macOS**
| Version | Status | Notes |
|---------|--------|-------|
| macOS 14 (Sonoma) | ✅ Fully Supported | Latest features |
| macOS 13 (Ventura) | ✅ Fully Supported | Excellent |
| macOS 12 (Monterey) | ✅ Fully Supported | Good |
| macOS 11 (Big Sur) | ✅ Supported | Basic support |
| macOS 10.15 (Catalina) | ⚠️ Limited | May work with setup |
| macOS 10.14 (Mojave) | ⚠️ Limited | Minimum version |
| macOS 10.13 and older | ❌ Not Supported | Python compatibility issues |

**macOS Features:**
- Metal GPU acceleration (M1/M2/M3 Macs)
- Native macOS voices (Alex, Tom, Daniel)
- PyAudio-generated audio chimes
- Homebrew integration

### **Linux**
| Distribution | Status | Notes |
|-------------|--------|-------|
| Ubuntu 20.04+ | ✅ Supported | Well tested |
| Ubuntu 18.04 | ⚠️ Limited | May need manual setup |
| Debian 11+ | ✅ Supported | Good compatibility |
| Fedora 35+ | ✅ Supported | Works well |
| CentOS/RHEL 8+ | ⚠️ Limited | May need extra packages |
| Arch Linux | ✅ Supported | Community tested |

**Linux Requirements:**
- ALSA or PulseAudio
- `portaudio19-dev` package
- `python3-pyaudio` (if available)

## 🎤 Audio System Compatibility

### **Microphone Support**
| Type | Windows | macOS | Linux |
|------|---------|-------|-------|
| USB Microphones | ✅ | ✅ | ✅ |
| Built-in Laptop Mic | ✅ | ✅ | ✅ |
| Bluetooth Headsets | ⚠️ | ⚠️ | ⚠️ |
| Professional Audio Interfaces | ✅ | ✅ | ⚠️ |

**Note:** Bluetooth audio may have latency issues affecting voice recognition accuracy.

### **Audio Output**
| Type | Windows | macOS | Linux |
|------|---------|-------|-------|
| Built-in Speakers | ✅ | ✅ | ✅ |
| USB/3.5mm Headphones | ✅ | ✅ | ✅ |
| Bluetooth Headphones | ✅ | ✅ | ⚠️ |
| External Speakers | ✅ | ✅ | ✅ |

## 🚀 GPU Acceleration Support

### **NVIDIA CUDA**
| GPU Series | Status | Notes |
|------------|--------|-------|
| RTX 40 Series | ✅ Excellent | Best performance |
| RTX 30 Series | ✅ Excellent | Great performance |
| RTX 20 Series | ✅ Good | Solid performance |
| GTX 16 Series | ✅ Good | Decent performance |
| GTX 10 Series | ⚠️ Limited | Basic support |
| Older than GTX 10 | ❌ Not Supported | Use CPU mode |

### **Apple Silicon (macOS)**
| Chip | Status | Notes |
|------|--------|-------|
| M3 Series | ✅ Excellent | Metal acceleration |
| M2 Series | ✅ Excellent | Metal acceleration |
| M1 Series | ✅ Good | Metal acceleration |
| Intel Macs | ⚠️ CPU Only | No Metal support |

### **AMD GPUs**
| Type | Status | Notes |
|------|--------|-------|
| ROCm Compatible | ⚠️ Limited | Experimental support |
| Other AMD GPUs | ❌ Not Supported | Use CPU mode |

## 🔍 Dependency Compatibility

### **Critical Dependencies**
| Package | Minimum Version | Recommended | Notes |
|---------|----------------|-------------|-------|
| `faster-whisper` | 0.9.0+ | Latest | Core speech recognition |
| `google-generativeai` | 0.3.0+ | Latest | AI responses |
| `pyaudio` | 0.2.11+ | Latest | Audio I/O |
| `numpy` | 1.21.0+ | Latest | Numerical processing |
| `pyttsx3` | 2.90+ | Latest | Text-to-speech |
| `cryptography` | 41.0.0+ | Latest | Security features |
| `psutil` | 5.9.0+ | Latest | System monitoring |

### **Known Incompatible Packages**
- `pyaudio` versions before 0.2.10 (missing features)
- `numpy` versions before 1.20 (compatibility issues)
- Any package versions from Python 3.13+ repos (may conflict)

## 🧪 Testing Your Setup

Run the compatibility test to check your specific configuration:

```bash
python3 test_platform.py
```

This will test:
- ✅ Python version compatibility
- ✅ Required package imports
- ✅ Whisper functionality
- ✅ Audio system access
- ✅ TTS voice availability
- ✅ Platform-specific features

## 🚨 Known Issues and Solutions

### **Issue: Python 3.13 Audio Failures**
**Symptoms:** Whisper crashes, audio processing fails
**Solution:** Downgrade to Python 3.11

### **Issue: PyAudio Installation Fails (macOS)**
**Symptoms:** `pip install pyaudio` fails with compiler errors
**Solution:** Install PortAudio first: `brew install portaudio`

### **Issue: No Microphone Access (macOS)**
**Symptoms:** Permission denied errors
**Solution:** Grant microphone permission in System Preferences

### **Issue: CUDA Not Detected**
**Symptoms:** Falls back to CPU processing
**Solution:** Install CUDA toolkit and compatible PyTorch

### **Issue: TTS Voice Not Found**
**Symptoms:** No voices available or robotic voice
**Solution:** Install system TTS voices or use different voice selection

## 📞 Getting Help

If you're experiencing compatibility issues:

1. **Run the test script:** `python3 test_platform.py`
2. **Check Python version:** `python3 --version`
3. **Verify dependencies:** `pip3 list | grep -E "(whisper|pyaudio|pyttsx3)"`
4. **Review platform-specific setup guides**
5. **Check GitHub issues for similar problems**

## 🔄 Version Update Recommendations

**Current Setup Working?** 
- ✅ Don't update unless necessary
- ✅ Pin your Python version to avoid automatic updates

**Need to Update?**
- Update packages gradually, test after each update
- Always backup your working configuration
- Test with `python3 test_platform.py` after updates

---

**Last Updated:** Compatible with Steve Voice Assistant v1.0.0  
**Testing Date:** Based on real-world testing with Python 3.8-3.13