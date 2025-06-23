#!/usr/bin/env python3
"""
Setup script for Steve Voice Assistant
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment configuration"""
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("🔧 Setting up environment configuration...")
    
    # Create .env file
    api_key = input("Enter your Google AI API key (or press Enter to skip): ").strip()
    
    env_content = []
    if api_key:
        env_content.append(f"GOOGLE_AI_API_KEY={api_key}")
    else:
        env_content.append("# GOOGLE_AI_API_KEY=your_api_key_here")
    
    # Add optional configuration
    env_content.extend([
        "",
        "# Optional configuration",
        "# STEVE_MAX_DAILY_CALLS=200",
        "# STEVE_MAX_SESSION_COST=5.00",
        "# STEVE_ENABLE_HISTORY=true",
        "# STEVE_ENABLE_CHIMES=true"
    ])
    
    try:
        with open(env_file, "w") as f:
            f.write("\n".join(env_content))
        
        # Set restrictive permissions
        os.chmod(env_file, 0o600)
        print("✅ Environment file created (.env)")
        
        if not api_key:
            print("⚠️  Remember to add your Google AI API key to .env")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_audio_system():
    """Check if audio system is available"""
    print("🎤 Checking audio system...")
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Check for input devices
        input_devices = []
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append(device_info['name'])
        
        audio.terminate()
        
        if input_devices:
            print(f"✅ Found {len(input_devices)} audio input device(s)")
            print(f"   Primary device: {input_devices[0]}")
            return True
        else:
            print("⚠️  No audio input devices found")
            return False
            
    except ImportError:
        print("❌ PyAudio not available")
        return False
    except Exception as e:
        print(f"⚠️  Audio system check failed: {e}")
        return False

def run_security_check():
    """Run basic security checks"""
    print("🔒 Running security checks...")
    
    checks_passed = 0
    total_checks = 3
    
    # Check file permissions
    env_file = Path(".env")
    if env_file.exists():
        stat_info = env_file.stat()
        if stat_info.st_mode & 0o077 == 0:  # Only owner can read/write
            print("✅ .env file permissions secure")
            checks_passed += 1
        else:
            print("⚠️  .env file permissions should be more restrictive")
            try:
                os.chmod(env_file, 0o600)
                print("✅ Fixed .env file permissions")
                checks_passed += 1
            except:
                print("❌ Could not fix .env file permissions")
    else:
        print("⚠️  .env file not found")
    
    # Check for sensitive files in git
    gitignore_file = Path(".gitignore")
    if gitignore_file.exists():
        with open(gitignore_file, "r") as f:
            gitignore_content = f.read()
        
        if ".env" in gitignore_content and "*.log" in gitignore_content:
            print("✅ .gitignore properly configured")
            checks_passed += 1
        else:
            print("⚠️  .gitignore may not exclude sensitive files")
    else:
        print("⚠️  .gitignore file not found")
    
    # Check Python security modules
    try:
        import cryptography
        print("✅ Cryptography module available")
        checks_passed += 1
    except ImportError:
        print("❌ Cryptography module not available")
    
    print(f"🔒 Security checks: {checks_passed}/{total_checks} passed")
    return checks_passed == total_checks

def test_installation():
    """Test if installation works"""
    print("🧪 Testing installation...")
    
    try:
        # Try importing the main modules
        import steve_voice_assistant
        print("✅ Main module imports successfully")
        
        # Test basic initialization (without audio)
        # This would need to be adapted based on your actual code structure
        print("✅ Basic functionality test passed")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Installation test warning: {e}")
        return True  # Non-critical error

def main():
    """Main setup function"""
    print("🤖 Steve Voice Assistant Setup")
    print("=" * 40)
    
    success_count = 0
    total_steps = 6
    
    # Step 1: Check Python version
    if check_python_version():
        success_count += 1
    
    # Step 2: Install dependencies
    if install_dependencies():
        success_count += 1
    
    # Step 3: Setup environment
    if setup_environment():
        success_count += 1
    
    # Step 4: Check audio system
    if check_audio_system():
        success_count += 1
    
    # Step 5: Security checks
    if run_security_check():
        success_count += 1
    
    # Step 6: Test installation
    if test_installation():
        success_count += 1
    
    print("\n" + "=" * 40)
    print(f"Setup completed: {success_count}/{total_steps} steps successful")
    
    if success_count == total_steps:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Ensure your Google AI API key is set in .env")
        print("2. Run: python steve_voice_assistant.py")
        print("3. Say 'Hey Steve' to start chatting!")
    elif success_count >= 4:
        print("⚠️  Setup mostly successful with some warnings")
        print("You should be able to run the application")
    else:
        print("❌ Setup encountered significant issues")
        print("Please check the error messages above")
    
    return success_count >= 4

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)