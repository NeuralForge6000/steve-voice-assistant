#!/usr/bin/env python3
"""
Platform Compatibility Test for Steve Voice Assistant
Tests cross-platform audio and TTS functionality
"""

import platform
import sys
import time

def test_python_version():
    """Test Python version compatibility"""
    print("\n🐍 Testing Python version compatibility...")
    
    version_info = sys.version_info
    version_str = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
    
    print(f"Python version: {version_str}")
    
    # Check minimum version
    if version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    # Check for problematic versions
    if version_info >= (3, 13):
        print("❌ CRITICAL: Python 3.13+ has known audio compatibility issues")
        print("   Whisper and audio libraries may not work correctly")
        print("   Recommended: Downgrade to Python 3.11 or 3.12")
        print("   Solutions:")
        print("   - macOS: brew install python@3.11")
        print("   - pyenv: pyenv install 3.11.9 && pyenv local 3.11.9")
        return False
    elif version_info >= (3, 12):
        print("⚠️  Python 3.12 detected - should work but 3.11 is preferred")
        return True
    else:
        print("✅ Python version is compatible")
        return True

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    try:
        import pyaudio
        print("✅ PyAudio available")
    except ImportError as e:
        print(f"❌ PyAudio not available: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy available")
    except ImportError as e:
        print(f"❌ NumPy not available: {e}")
        return False
    
    try:
        import pyttsx3
        print("✅ pyttsx3 available")
    except ImportError as e:
        print(f"❌ pyttsx3 not available: {e}")
        return False
    
    # Test platform-specific imports
    if platform.system() == "Windows":
        try:
            import winsound
            print("✅ winsound available (Windows)")
        except ImportError:
            print("⚠️ winsound not available (unexpected on Windows)")
    
    return True

def test_audio_system():
    """Test PyAudio audio system"""
    print("\n🎵 Testing audio system...")
    
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        # Check for output devices
        output_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxOutputChannels'] > 0:
                output_devices.append(device_info['name'])
        
        audio.terminate()
        
        print(f"✅ Found {len(input_devices)} input device(s)")
        print(f"✅ Found {len(output_devices)} output device(s)")
        
        if input_devices:
            print(f"   Primary input: {input_devices[0]}")
        if output_devices:
            print(f"   Primary output: {output_devices[0]}")
        
        return len(input_devices) > 0 and len(output_devices) > 0
        
    except Exception as e:
        print(f"❌ Audio system test failed: {e}")
        return False

def test_tts_voices():
    """Test Text-to-Speech voice availability"""
    print("\n🗣️ Testing TTS voices...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if not voices:
            print("❌ No TTS voices found")
            return False
        
        print(f"✅ Found {len(voices)} voice(s)")
        
        # Show platform-appropriate voices
        platform_name = platform.system()
        if platform_name == "Darwin":  # macOS
            preferred_voices = ['alex', 'tom', 'daniel']
            print("🍎 macOS voices:")
        elif platform_name == "Windows":
            preferred_voices = ['david', 'mark', 'zira']
            print("🪟 Windows voices:")
        else:
            preferred_voices = []
            print("🐧 Available voices:")
        
        found_preferred = False
        for voice in voices[:5]:  # Show first 5
            voice_name = voice.name.lower()
            is_preferred = any(pref in voice_name for pref in preferred_voices)
            if is_preferred:
                found_preferred = True
                print(f"   ✅ {voice.name} (preferred)")
            else:
                print(f"   📢 {voice.name}")
        
        engine.stop()
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def test_tone_generation():
    """Test cross-platform tone generation"""
    print("\n🎶 Testing tone generation...")
    
    try:
        import numpy as np
        import pyaudio
        
        # Generate a simple test tone
        frequency = 440  # A4
        duration_ms = 100
        sample_rate = 44100
        volume = 0.1  # Quiet test
        
        duration_s = duration_ms / 1000.0
        frames = int(duration_s * sample_rate)
        
        # Generate sine wave
        t = np.linspace(0, duration_s, frames, False)
        wave_data = np.sin(2 * np.pi * frequency * t)
        wave_data = (wave_data * volume * 32767).astype(np.int16)
        
        print("✅ Tone generation successful")
        
        # Test playback (optional - user can skip)
        test_playback = input("🔊 Test audio playback? (y/n): ").lower().strip()
        
        if test_playback in ['y', 'yes']:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=sample_rate,
                output=True
            )
            
            print("🎵 Playing test tone...")
            stream.write(wave_data.tobytes())
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            print("✅ Audio playback test completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Tone generation test failed: {e}")
        return False

def test_platform_specific():
    """Test platform-specific features"""
    print(f"\n🖥️ Testing {platform.system()}-specific features...")
    
    platform_name = platform.system()
    
    if platform_name == "Darwin":  # macOS
        # Test Metal GPU detection
        try:
            import subprocess
            result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                  capture_output=True, text=True, timeout=5)
            if 'Metal' in result.stdout:
                print("✅ Metal GPU support detected")
            else:
                print("⚠️ Metal GPU support not detected")
        except:
            print("⚠️ Could not check Metal GPU support")
    
    elif platform_name == "Windows":
        # Test winsound
        try:
            import winsound
            print("✅ winsound module available")
            
            test_beep = input("🔊 Test Windows beep? (y/n): ").lower().strip()
            if test_beep in ['y', 'yes']:
                print("🎵 Testing Windows beep...")
                winsound.Beep(440, 200)
                print("✅ Windows beep test completed")
        except Exception as e:
            print(f"❌ winsound test failed: {e}")
    
    elif platform_name == "Linux":
        # Test ALSA/PulseAudio
        print("🐧 Linux audio system detected")
        try:
            import subprocess
            # Check for ALSA
            result = subprocess.run(['which', 'aplay'], capture_output=True)
            if result.returncode == 0:
                print("✅ ALSA detected")
            
            # Check for PulseAudio
            result = subprocess.run(['which', 'pulseaudio'], capture_output=True)
            if result.returncode == 0:
                print("✅ PulseAudio detected")
        except:
            print("⚠️ Could not check Linux audio system")
    
    return True

def main():
    """Run all platform tests"""
    print("🤖 Steve Voice Assistant - Platform Compatibility Test")
    print("=" * 55)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 55)
    
    tests = [
        ("Python Version Test", test_python_version),
        ("Import Test", test_imports),
        ("Whisper Compatibility Test", test_whisper_compatibility),
        ("Audio System Test", test_audio_system),
        ("TTS Voices Test", test_tts_voices),
        ("Tone Generation Test", test_tone_generation),
        ("Platform-Specific Test", test_platform_specific),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
    
    print("\n" + "=" * 55)
    print(f"🧪 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Steve should work great on your system.")
    elif passed >= total - 1:
        print("✅ Most tests passed. Steve should work with minor limitations.")
    else:
        print("⚠️ Some tests failed. You may need to install additional dependencies.")
        print("\nCommon solutions:")
        print("- Python 3.13+ issues: Downgrade to Python 3.11")
        print("- macOS: brew install portaudio")
        print("- Linux: sudo apt-get install portaudio19-dev python3-pyaudio")
        print("- Windows: pip install --upgrade pyaudio")
        print("\nPython version recommendations:")
        print("- ✅ Best: Python 3.11.x")
        print("- ✅ Good: Python 3.10.x") 
        print("- ⚠️ OK: Python 3.12.x")
        print("- ❌ Broken: Python 3.13+")
    
    print("\n🚀 Ready to run Steve? Try: python steve_voice_assistant.py")

if __name__ == "__main__":
    main()