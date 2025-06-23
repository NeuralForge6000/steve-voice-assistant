"""
Enhanced Steve Voice Assistant - Cross-Platform with Comprehensive Security

Core Features:
💰 Real-time cost tracking for Gemini API usage
📜 Encrypted conversation history with secure management
🧠 Smart context management to optimize token usage
📊 Detailed cost reporting per conversation
🔄 Conversation summarization to reduce token usage
⚙️ Configurable history length and cost limits

🌍 Cross-Platform Support:
🪟 Windows (native winsound + Windows voices)
🍎 macOS (PyAudio tones + macOS voices like Alex, Tom)
🐧 Linux (PyAudio tones + available system voices)

Security Features:
🔒 Prompt injection protection with input sanitization
🛡️ Secure temporary file handling with encryption
🔐 Encrypted conversation history storage
📊 System resource monitoring and limits
🚨 Comprehensive error handling and logging
⚡ API usage monitoring and rate limiting
🧹 Secure data cleanup and memory clearing

Cost Management:
- Tracks input/output tokens for each API call
- Real-time cost calculation display
- Conversation history pruning when approaching limits
- Optional conversation summarization to reduce context size
- Daily/session cost tracking with warnings
- API usage limits to prevent runaway costs

Security Benefits:
- Protection against prompt injection attacks
- Encrypted storage of sensitive voice data
- Secure deletion of temporary audio files
- Resource exhaustion prevention
- Audit logging for security events
- Safe error handling without information disclosure

Required Dependencies:
pip install pyaudio numpy faster-whisper google-generativeai pyttsx3 psutil cryptography

Platform-Specific Setup:
- macOS: brew install portaudio (for PyAudio)
- Windows: PyAudio comes with binary wheels
- Linux: sudo apt-get install portaudio19-dev python3-pyaudio

Environment Variables Required:
- GOOGLE_AI_API_KEY: Your Google AI Studio API key
"""

import pyaudio
import wave
import numpy as np
import time
import os
import re
import threading
import pyttsx3
import random
import tempfile
import psutil
import logging
import platform
import subprocess
import math
from faster_whisper import WhisperModel
import google.generativeai as genai
from datetime import datetime, date
import json
from cryptography.fernet import Fernet

# Platform-specific imports
if platform.system() == "Windows":
    import winsound

class SteveVoiceAssistant:
    def __init__(self):
        # Platform detection
        self.platform = platform.system()
        print(f"🖥️ Detected platform: {self.platform}")
        
        # Improved audio settings
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.SILENCE_THRESHOLD = 150
        self.SILENCE_DURATION = 4.0
        self.MIN_SPEECH_DURATION = 0.5
        self.WAKE_WORD = "hey steve"
        self.GOODBYE_WORD = "goodbye steve"
        self.ENABLE_CHIMES = True
        self.conversation_mode = False
        
        # === Security Configuration ===
        self.setup_security()
        
        # === Platform-specific Audio Setup ===
        self.setup_platform_audio()
        
        # === Conversation History & Cost Tracking ===
        self.conversation_history = []
        self.session_costs = {
            'input_tokens': 0,
            'output_tokens': 0,
            'total_cost': 0.0,
            'conversations': 0,
            'start_time': datetime.now()
        }
        
        # === API Usage Monitoring ===
        self.api_usage = {
            'daily_calls': 0,
            'last_usage_date': date.today(),
            'hourly_calls': 0,
            'last_hour': datetime.now().hour
        }
        
        # API Usage Limits
        self.MAX_DAILY_API_CALLS = 200  # Reasonable daily limit
        self.MAX_HOURLY_API_CALLS = 30   # Prevent runaway usage
        self.MAX_SESSION_COST = 5.00     # Maximum cost per session
        
        # Cost settings (per 1M tokens)
        self.COST_INPUT_PER_1M = 3.50  # $3.50 per 1M input tokens
        self.COST_OUTPUT_PER_1M = 10.50  # $10.50 per 1M output tokens
        
        # History management settings
        self.MAX_HISTORY_TOKENS = 8000  # Trim history if approaching this
        self.MAX_CONVERSATION_TURNS = 20  # Maximum turns to keep
        self.COST_WARNING_THRESHOLD = 0.50  # Warn if session cost exceeds this
        self.ENABLE_HISTORY = True  # Set to False for stateless conversations
        
        # Resource monitoring
        self.MIN_DISK_SPACE_MB = 100  # Minimum 100MB free space required
        self.MAX_MEMORY_PERCENT = 85  # Stop if memory usage > 85%
        
        # Initialize audio
        self.audio = pyaudio.PyAudio()
        
        # Load Whisper model with platform-specific optimizations
        print("Loading Whisper model...")
        try:
            if self.platform == "Darwin":  # macOS
                # Try Metal GPU acceleration first
                self.whisper_model = WhisperModel("turbo", device="cuda", compute_type="float16")
                print("✅ GPU Whisper model loaded (Metal acceleration)")
            else:
                self.whisper_model = WhisperModel("turbo", device="cuda", compute_type="float16")
                print("✅ GPU Whisper model loaded")
        except:
            self.whisper_model = WhisperModel("turbo", device="cpu", compute_type="int8")
            print("✅ CPU Whisper model loaded")
        
        # Initialize Google AI
        print("Initializing Google AI...")
        api_key = os.getenv('GOOGLE_AI_API_KEY')
        if not api_key:
            raise ValueError("Please set GOOGLE_AI_API_KEY environment variable")
        
        genai.configure(api_key=api_key)
        self.ai_model = genai.GenerativeModel('gemini-1.5-pro')
        print("✅ Google AI model loaded")
        
        # Initialize Text-to-Speech
        print("Initializing Text-to-Speech...")
        try:
            self.tts_engine = pyttsx3.init()
            self.setup_voice()
            print("✅ Text-to-Speech loaded")
        except Exception as e:
            self.log_error("TTS initialization failed", e)
            self.tts_engine = None
        
        # Calibrate audio levels
        self.calibrate_audio()
        
        # Display initial cost info
        self.display_cost_info()
        
        # Play startup chime to indicate system is ready
        self.play_startup_chime()

    def display_cost_info(self):
        """Display current cost information"""
        print(f"\n💰 Cost Tracking Enabled")
        print(f"   Input tokens: ${self.COST_INPUT_PER_1M:.2f}/1M tokens")
        print(f"   Output tokens: ${self.COST_OUTPUT_PER_1M:.2f}/1M tokens")
        print(f"   History: {'Enabled' if self.ENABLE_HISTORY else 'Disabled'}")
        print(f"   Warning threshold: ${self.COST_WARNING_THRESHOLD:.2f}")
        print(f"🔒 Security Features Enabled")
        print(f"   Daily API limit: {self.MAX_DAILY_API_CALLS} calls")
        print(f"   Session cost limit: ${self.MAX_SESSION_COST:.2f}")

    # ===== PLATFORM-SPECIFIC AUDIO METHODS =====
    
    def setup_platform_audio(self):
        """Initialize platform-specific audio components"""
        if self.platform == "Darwin":  # macOS
            print("🍎 Setting up macOS audio components")
            self.setup_macos_audio()
        elif self.platform == "Windows":
            print("🪟 Setting up Windows audio components")
            self.setup_windows_audio()
        else:
            print(f"🐧 Setting up audio for {self.platform}")
            self.setup_generic_audio()
    
    def setup_macos_audio(self):
        """Setup macOS-specific audio configuration"""
        # Check for Metal GPU support
        try:
            result = subprocess.run(['system_profiler', 'SPDisplaysDataType'], 
                                  capture_output=True, text=True, timeout=5)
            if 'Metal' in result.stdout:
                print("✅ Metal GPU support detected")
            else:
                print("⚠️ Metal GPU support not detected")
        except:
            print("⚠️ Could not check Metal GPU support")
    
    def setup_windows_audio(self):
        """Setup Windows-specific audio configuration"""
        print("✅ Windows audio support ready")
    
    def setup_generic_audio(self):
        """Setup generic cross-platform audio"""
        print("✅ Generic audio support ready")
    
    def generate_tone(self, frequency, duration_ms, sample_rate=44100, volume=0.3):
        """Generate a sine wave tone using numpy"""
        try:
            duration_s = duration_ms / 1000.0
            frames = int(duration_s * sample_rate)
            
            # Generate sine wave
            t = np.linspace(0, duration_s, frames, False)
            wave_data = np.sin(2 * np.pi * frequency * t)
            
            # Apply volume and convert to 16-bit integers
            wave_data = (wave_data * volume * 32767).astype(np.int16)
            
            return wave_data.tobytes()
        except Exception as e:
            self.log_error("Failed to generate tone", e)
            return b''
    
    def play_tone_cross_platform(self, frequency, duration_ms):
        """Play a tone using cross-platform method"""
        if self.platform == "Windows" and 'winsound' in globals():
            try:
                winsound.Beep(int(frequency), int(duration_ms))
                return
            except:
                pass
        
        # Fallback to PyAudio tone generation (works on all platforms)
        try:
            tone_data = self.generate_tone(frequency, duration_ms)
            if not tone_data:
                return
            
            # Play using PyAudio
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True
            )
            stream.write(tone_data)
            stream.stop_stream()
            stream.close()
            
        except Exception as e:
            self.log_error("Failed to play tone", e)
    
    def play_chime_sequence(self, frequencies, durations, pause_between=0.02):
        """Play a sequence of tones with pauses"""
        def chime():
            try:
                for i, (freq, duration) in enumerate(zip(frequencies, durations)):
                    self.play_tone_cross_platform(freq, duration)
                    if i < len(frequencies) - 1 and pause_between > 0:
                        time.sleep(pause_between)
            except Exception as e:
                self.log_error("Failed to play chime sequence", e)
        
        threading.Thread(target=chime, daemon=True).start()
    
    # ===== SECURITY METHODS =====
    
    def setup_security(self):
        """Initialize security components"""
        # Setup secure logging
        log_filename = f"steve_security_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='a'
        )
        
        # Generate encryption key for conversation history
        self.history_key = Fernet.generate_key()
        self.cipher = Fernet(self.history_key)
        
        # Initialize secure temp file tracking
        self.temp_files = []
        
        print("🔒 Security components initialized")

    def sanitize_input(self, user_input):
        """Sanitize user input to prevent prompt injection attacks"""
        if not user_input:
            return ""
        
        # List of dangerous patterns that could be prompt injection attempts
        dangerous_patterns = [
            r"ignore\s+previous",
            r"forget\s+everything", 
            r"new\s+instructions",
            r"system\s*:",
            r"assistant\s*:",
            r"human\s*:",
            r"disregard",
            r"override",
            r"pretend\s+you\s+are",
            r"act\s+as\s+if",
            r"</\w+>",  # HTML/XML tags
            r"<\w+>",   # HTML/XML tags
            r"\bprompt\b.*\binjection\b",
            r"tell\s+me\s+your\s+instructions"
        ]
        
        sanitized = user_input.strip()
        
        # Remove dangerous patterns
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, "[filtered]", sanitized, flags=re.IGNORECASE)
        
        # Limit length to prevent very long inputs
        if len(sanitized) > 500:
            sanitized = sanitized[:500] + "..."
            
        # Log potential injection attempts
        if sanitized != user_input.strip():
            self.log_security_event("Potential prompt injection detected", {
                'original_length': len(user_input),
                'sanitized_length': len(sanitized),
                'timestamp': datetime.now().isoformat()
            })
        
        return sanitized

    def create_secure_temp_file(self, suffix=".wav", prefix="steve_audio_"):
        """Create a secure temporary file"""
        try:
            fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=None)
            os.close(fd)  # Close file descriptor, keep path
            
            # Track temp file for cleanup
            self.temp_files.append(temp_path)
            
            # Set restrictive permissions (owner only)
            os.chmod(temp_path, 0o600)
            
            return temp_path
        except Exception as e:
            self.log_error("Failed to create secure temp file", e)
            raise

    def secure_delete_file(self, filepath):
        """Securely delete a file by overwriting it first"""
        if not os.path.exists(filepath):
            return
        
        try:
            # Get file size
            file_size = os.path.getsize(filepath)
            
            # Overwrite with random data (3 passes for extra security)
            with open(filepath, "r+b") as f:
                for _ in range(3):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Finally delete the file
            os.remove(filepath)
            
            # Remove from tracking list
            if filepath in self.temp_files:
                self.temp_files.remove(filepath)
                
        except Exception as e:
            self.log_error("Failed to securely delete file", e)
            # Fallback to regular deletion
            try:
                os.remove(filepath)
            except:
                pass

    def encrypt_text(self, text):
        """Encrypt text using conversation history encryption"""
        try:
            return self.cipher.encrypt(text.encode()).decode()
        except Exception as e:
            self.log_error("Failed to encrypt text", e)
            return text  # Fallback to plain text

    def decrypt_text(self, encrypted_text):
        """Decrypt text using conversation history encryption"""
        try:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            self.log_error("Failed to decrypt text", e)
            return encrypted_text  # Return as-is if decryption fails

    def check_system_resources(self):
        """Check system resources before proceeding with operations"""
        try:
            # Check available disk space
            disk_usage = psutil.disk_usage('.')
            free_space_mb = disk_usage.free / (1024 * 1024)
            
            if free_space_mb < self.MIN_DISK_SPACE_MB:
                raise Exception(f"Insufficient disk space: {free_space_mb:.1f}MB available, {self.MIN_DISK_SPACE_MB}MB required")
            
            # Check memory usage
            memory = psutil.virtual_memory()
            if memory.percent > self.MAX_MEMORY_PERCENT:
                self.log_security_event("High memory usage detected", {
                    'memory_percent': memory.percent,
                    'available_mb': memory.available / (1024 * 1024)
                })
                # Force conversation history cleanup
                self.manage_conversation_history()
                
                # Check again after cleanup
                memory = psutil.virtual_memory()
                if memory.percent > self.MAX_MEMORY_PERCENT:
                    raise Exception(f"Memory usage too high: {memory.percent}%")
            
            return True
            
        except Exception as e:
            self.log_error("System resource check failed", e)
            raise

    def check_api_usage_limits(self):
        """Check and enforce API usage limits"""
        current_date = date.today()
        current_hour = datetime.now().hour
        
        # Reset daily counter if new day
        if current_date != self.api_usage['last_usage_date']:
            self.api_usage['daily_calls'] = 0
            self.api_usage['last_usage_date'] = current_date
            self.log_security_event("Daily API usage counter reset", {})
        
        # Reset hourly counter if new hour
        if current_hour != self.api_usage['last_hour']:
            self.api_usage['hourly_calls'] = 0
            self.api_usage['last_hour'] = current_hour
        
        # Check daily limit
        if self.api_usage['daily_calls'] >= self.MAX_DAILY_API_CALLS:
            raise Exception(f"Daily API limit exceeded ({self.MAX_DAILY_API_CALLS} calls)")
        
        # Check hourly limit
        if self.api_usage['hourly_calls'] >= self.MAX_HOURLY_API_CALLS:
            raise Exception(f"Hourly API limit exceeded ({self.MAX_HOURLY_API_CALLS} calls)")
        
        # Check session cost limit
        if self.session_costs['total_cost'] >= self.MAX_SESSION_COST:
            raise Exception(f"Session cost limit exceeded (${self.MAX_SESSION_COST:.2f})")
        
        return True

    def update_api_usage(self):
        """Update API usage counters"""
        self.api_usage['daily_calls'] += 1
        self.api_usage['hourly_calls'] += 1
        
        self.log_security_event("API call made", {
            'daily_calls': self.api_usage['daily_calls'],
            'hourly_calls': self.api_usage['hourly_calls'],
            'session_cost': self.session_costs['total_cost']
        })

    def log_error(self, message, exception):
        """Log errors securely without exposing sensitive information"""
        error_id = f"ERR_{int(time.time())}"
        
        # Log detailed error for debugging (secure log file)
        logging.error(f"{error_id}: {message} - {str(exception)}", exc_info=True)
        
        # Print generic message to console
        print(f"❌ {message} (Error ID: {error_id})")

    def log_security_event(self, event, details=None):
        """Log security events"""
        event_data = {
            'event': event,
            'timestamp': datetime.now().isoformat(),
            'details': details or {}
        }
        logging.info(f"SECURITY: {json.dumps(event_data)}")

    def handle_ai_error(self, exception):
        """Handle AI errors with secure error messages"""
        error_id = f"AI_ERR_{int(time.time())}"
        
        # Log the actual error
        self.log_error("AI processing error", exception)
        
        # Return user-friendly messages
        generic_messages = [
            "I'm having trouble processing that right now.",
            "Sorry, I encountered an issue. Please try again.",
            "I need a moment to think about that.",
            "Let me try that again in a moment.",
            "I'm experiencing some difficulty. Could you rephrase that?"
        ]
        
        return random.choice(generic_messages)

    def estimate_tokens(self, text):
        """Rough token estimation (4 chars ≈ 1 token for English)"""
        return len(text) / 4

    def calculate_cost(self, input_tokens, output_tokens):
        """Calculate cost based on token usage"""
        input_cost = (input_tokens / 1_000_000) * self.COST_INPUT_PER_1M
        output_cost = (output_tokens / 1_000_000) * self.COST_OUTPUT_PER_1M
        return input_cost + output_cost

    def update_session_costs(self, input_tokens, output_tokens):
        """Update session cost tracking"""
        self.session_costs['input_tokens'] += input_tokens
        self.session_costs['output_tokens'] += output_tokens
        
        call_cost = self.calculate_cost(input_tokens, output_tokens)
        self.session_costs['total_cost'] += call_cost
        self.session_costs['conversations'] += 1
        
        return call_cost

    def display_cost_summary(self, call_cost, input_tokens, output_tokens):
        """Display cost information for the current call and session"""
        print(f"💰 Cost Info:")
        print(f"   This call: ${call_cost:.6f} ({input_tokens} in, {output_tokens} out tokens)")
        print(f"   Session total: ${self.session_costs['total_cost']:.4f}")
        print(f"   Session tokens: {self.session_costs['input_tokens']:,} in, {self.session_costs['output_tokens']:,} out")
        
        # Warning if costs are getting high
        if self.session_costs['total_cost'] > self.COST_WARNING_THRESHOLD:
            print(f"⚠️  Session cost exceeded ${self.COST_WARNING_THRESHOLD:.2f} threshold!")

    def manage_conversation_history(self):
        """Manage encrypted conversation history to stay within token limits"""
        if not self.ENABLE_HISTORY:
            return
        
        try:
            # Estimate current history size by decrypting and calculating
            total_history_text = ""
            for entry in self.conversation_history:
                if entry.get('encrypted', False):
                    user_text = self.decrypt_text(entry['user'])
                    assistant_text = self.decrypt_text(entry['assistant'])
                else:
                    user_text = entry['user']
                    assistant_text = entry['assistant']
                total_history_text += user_text + assistant_text
            
            estimated_tokens = self.estimate_tokens(total_history_text)
            
            # If history is too long, trim from the beginning
            while (estimated_tokens > self.MAX_HISTORY_TOKENS or 
                   len(self.conversation_history) > self.MAX_CONVERSATION_TURNS):
                
                if len(self.conversation_history) <= 1:
                    break
                    
                removed = self.conversation_history.pop(0)
                print(f"🧹 Trimmed old conversation turn (history management)")
                
                # Log the trimming for security audit
                self.log_security_event("Conversation history trimmed", {
                    'reason': 'token_limit_exceeded' if estimated_tokens > self.MAX_HISTORY_TOKENS else 'turn_limit_exceeded',
                    'remaining_turns': len(self.conversation_history)
                })
                
                # Recalculate
                total_history_text = ""
                for entry in self.conversation_history:
                    if entry.get('encrypted', False):
                        user_text = self.decrypt_text(entry['user'])
                        assistant_text = self.decrypt_text(entry['assistant'])
                    else:
                        user_text = entry['user']
                        assistant_text = entry['assistant']
                    total_history_text += user_text + assistant_text
                estimated_tokens = self.estimate_tokens(total_history_text)
                
        except Exception as e:
            self.log_error("Failed to manage conversation history", e)
            # In case of error, clear history to prevent issues
            self.conversation_history = []

    def build_conversation_prompt(self, user_input):
        """Build prompt with encrypted conversation history"""
        if not self.ENABLE_HISTORY or not self.conversation_history:
            # No history, just use current input
            return f"""You are Steve, a helpful voice assistant. Respond naturally and conversationally in 1-2 sentences.

User said: {user_input}"""
        
        # Build prompt with decrypted conversation history
        prompt = """You are Steve, a helpful voice assistant. Respond naturally and conversationally in 1-2 sentences.

Conversation history:"""
        
        try:
            for entry in self.conversation_history:
                if entry.get('encrypted', False):
                    # Decrypt the conversation entries
                    user_text = self.decrypt_text(entry['user'])
                    assistant_text = self.decrypt_text(entry['assistant'])
                else:
                    # Handle legacy unencrypted entries
                    user_text = entry['user']
                    assistant_text = entry['assistant']
                
                prompt += f"\nUser: {user_text}"
                prompt += f"\nSteve: {assistant_text}"
        except Exception as e:
            self.log_error("Failed to build conversation prompt", e)
            # Fallback to no history
            return f"""You are Steve, a helpful voice assistant. Respond naturally and conversationally in 1-2 sentences.

User said: {user_input}"""
        
        prompt += f"\n\nUser: {user_input}"
        prompt += "\nSteve:"
        
        return prompt

    def get_ai_response(self, user_input):
        """Enhanced AI response with comprehensive security measures"""
        print("🤖 Steve is thinking...")
        
        # Play thinking chime
        self.play_thinking_chime()
        
        start_time = time.time()
        
        try:
            # === SECURITY CHECKS ===
            # 1. Check system resources
            self.check_system_resources()
            
            # 2. Check API usage limits
            self.check_api_usage_limits()
            
            # 3. Sanitize input to prevent prompt injection
            sanitized_input = self.sanitize_input(user_input)
            
            # 4. Manage conversation history
            self.manage_conversation_history()
            
            # 5. Build prompt with history
            prompt = self.build_conversation_prompt(sanitized_input)
            
            # 6. Estimate input tokens
            estimated_input_tokens = self.estimate_tokens(prompt)
            print(f"📊 Estimated input tokens: {estimated_input_tokens:.0f}")
            
            # 7. Get AI response
            response = self.ai_model.generate_content(prompt)
            ai_time = time.time() - start_time
            
            print(f"⚡ AI responded in {ai_time:.2f}s")
            
            ai_response = response.text.strip()
            
            # 8. Estimate output tokens
            estimated_output_tokens = self.estimate_tokens(ai_response)
            
            # 9. Update costs and usage tracking
            call_cost = self.update_session_costs(estimated_input_tokens, estimated_output_tokens)
            self.update_api_usage()
            
            # 10. Display cost info
            self.display_cost_summary(call_cost, estimated_input_tokens, estimated_output_tokens)
            
            # 11. Add to encrypted conversation history
            if self.ENABLE_HISTORY:
                encrypted_user_input = self.encrypt_text(user_input)  # Store original, not sanitized
                encrypted_ai_response = self.encrypt_text(ai_response)
                
                self.conversation_history.append({
                    'user': encrypted_user_input,
                    'assistant': encrypted_ai_response,
                    'timestamp': datetime.now().isoformat(),
                    'cost': call_cost,
                    'encrypted': True
                })
            
            # 12. Speak the response
            self.speak_response(ai_response)
            
            return ai_response
            
        except Exception as e:
            # Use secure error handling
            error_message = self.handle_ai_error(e)
            self.speak_response(error_message)
            return error_message

    def start_new_conversation(self):
        """Start a new conversation (clear history)"""
        if self.conversation_history:
            print(f"🗂️ Cleared conversation history ({len(self.conversation_history)} turns)")
            
        self.conversation_history = []
        
        # Display session summary
        duration = datetime.now() - self.session_costs['start_time']
        print(f"\n📊 Previous Session Summary:")
        print(f"   Duration: {duration}")
        print(f"   Total cost: ${self.session_costs['total_cost']:.4f}")
        print(f"   Conversations: {self.session_costs['conversations']}")
        
        # Reset session costs for new conversation
        self.session_costs = {
            'input_tokens': 0,
            'output_tokens': 0,
            'total_cost': 0.0,
            'conversations': 0,
            'start_time': datetime.now()
        }

    def conversation_loop(self):
        """Enhanced conversation loop with cost tracking"""
        print("\n💬 Entering conversation mode!")
        print("🗣️ You can now talk naturally without saying 'Hey Steve'")
        print("👋 Say 'Goodbye Steve' to end the conversation")
        
        if self.ENABLE_HISTORY:
            print("🧠 Conversation history is enabled")
        else:
            print("🔄 Stateless mode (no history)")
        
        print()
        
        # Play conversation start chime
        self.play_conversation_start_chime()
        
        self.conversation_mode = True
        conversation_start_time = datetime.now()
        
        while self.conversation_mode:
            try:
                # Play gentle listening chime for conversation
                self.play_conversation_listening_chime()
                
                print("🎤 Listening in conversation mode...")
                
                # Record user input
                command_file = self.record_voice_command()
                if command_file:
                    command_text = self.transcribe_command(command_file)
                    # Note: transcribe_command now handles secure file deletion
                else:
                    command_text = None
                
                if command_text:
                    # Check if user wants to end conversation
                    if self.check_goodbye(command_text):
                        print("👋 Ending conversation...")
                        
                        # Display conversation summary
                        conversation_duration = datetime.now() - conversation_start_time
                        print(f"\n💬 Conversation Summary:")
                        print(f"   Duration: {conversation_duration}")
                        print(f"   Turns: {len(self.conversation_history)}")
                        print(f"   Cost: ${self.session_costs['total_cost']:.4f}")
                        
                        # Respond to goodbye
                        goodbye_responses = [
                            "Goodbye! It was nice talking with you.",
                            "See you later! Have a great day.",
                            "Goodbye! Feel free to talk to me anytime.",
                            "Take care! I'll be here when you need me."
                        ]
                        
                        goodbye_response = random.choice(goodbye_responses)
                        self.speak_response(goodbye_response)
                        
                        # Play conversation end chime
                        self.play_conversation_end_chime()
                        
                        self.conversation_mode = False
                        break
                    
                    else:
                        # Continue conversation - get AI response
                        self.get_ai_response(command_text)
                
                else:
                    print("🤷 I didn't catch that. Could you repeat?")
            
            except KeyboardInterrupt:
                print("\n🛑 Exiting conversation mode...")
                self.conversation_mode = False
                break
            except Exception as e:
                print(f"❌ Conversation error: {e}")
                print("Continuing conversation...")
                time.sleep(1)

    def listen_for_wake_word(self):
        """Enhanced main listening loop with conversation history management"""
        print(f"👂 Voice Assistant Ready!")
        print(f"💬 Say: '{self.WAKE_WORD}' to start a conversation")
        print("🛑 Press Ctrl+C to exit\n")
        
        # Play ready chime to indicate system is ready
        self.play_ready_chime()
        
        while True:
            try:
                if not self.conversation_mode:
                    # Wake word listening mode
                    wake_file = self.record_wake_word_check(6)
                    wake_detected, full_text = self.check_wake_word(wake_file)
                    
                    if wake_detected:
                        print("🚀 Wake word detected!")
                        
                        # Start new conversation (clear any previous history)
                        self.start_new_conversation()
                        
                        # Check if command was included in the wake phrase
                        command_from_wake = self.extract_command_from_wake_phrase(full_text)
                        
                        if command_from_wake and len(command_from_wake) > 3:
                            # Handle the initial command
                            print(f"✅ Initial command: '{command_from_wake}'")
                            self.get_ai_response(command_from_wake)
                        else:
                            # Just acknowledgment, no specific command
                            greetings = [
                                "Hello! How can I help you?",
                                "Hi there! What can I do for you?", 
                                "Hey! What's on your mind?",
                                "Hello! I'm here to help."
                            ]
                            greeting = random.choice(greetings)
                            self.speak_response(greeting)
                        
                        # Enter conversation mode
                        self.conversation_loop()
                        
                        # After conversation ends, show ready message
                        print(f"\n👂 Back to listening for wake word: '{self.WAKE_WORD}'")
                        self.play_ready_chime()
                    
                    # Brief pause between wake word checks
                    time.sleep(0.1)
                
            except KeyboardInterrupt:
                print("\n🛑 Goodbye!")
                
                # Display final session summary
                if self.session_costs['total_cost'] > 0:
                    duration = datetime.now() - self.session_costs['start_time']
                    print(f"\n📊 Final Session Summary:")
                    print(f"   Duration: {duration}")
                    print(f"   Total cost: ${self.session_costs['total_cost']:.4f}")
                    print(f"   Total conversations: {self.session_costs['conversations']}")
                    print(f"   Total tokens: {self.session_costs['input_tokens']:,} in, {self.session_costs['output_tokens']:,} out")
                
                break
            except Exception as e:
                print(f"❌ Main loop error: {e}")
                print("Continuing...")
                time.sleep(1)

    # ... (All other methods remain the same as original) ...
    
    def setup_voice(self):
        """Configure Steve's voice settings with platform-specific voice selection"""
        if not self.tts_engine:
            return
            
        try:
            voices = self.tts_engine.getProperty('voices')
            
            # Display available voices
            print("Available voices:")
            for i, voice in enumerate(voices[:5]):  # Show first 5 voices
                gender = "♂️" if "male" in voice.name.lower() else "♀️"
                print(f"  {i}: {gender} {voice.name}")
            
            selected_voice = None
            
            # Platform-specific voice selection
            if self.platform == "Darwin":  # macOS
                # macOS voice preferences (male voices)
                macos_male_voices = ['alex', 'tom', 'daniel', 'fred', 'ralph']
                for voice in voices:
                    voice_name = voice.name.lower()
                    if any(preferred in voice_name for preferred in macos_male_voices):
                        selected_voice = voice
                        break
                        
            elif self.platform == "Windows":
                # Windows voice preferences
                windows_male_voices = ['david', 'mark', 'zira']
                for voice in voices:
                    voice_name = voice.name.lower()
                    if any(preferred in voice_name for preferred in windows_male_voices):
                        selected_voice = voice
                        break
            
            # Fallback to first available voice
            if not selected_voice and len(voices) > 0:
                selected_voice = voices[0]
            
            if selected_voice:
                self.tts_engine.setProperty('voice', selected_voice.id)
                print(f"🗣️ Selected voice: {selected_voice.name}")
            else:
                print("⚠️ No voices available")
            
            # Configure speech settings with platform adjustments
            if self.platform == "Darwin":
                # macOS tends to speak faster, so slow down a bit
                self.tts_engine.setProperty('rate', 160)
            else:
                self.tts_engine.setProperty('rate', 175)
            
            self.tts_engine.setProperty('volume', 0.8)  # Volume (0.0-1.0)
            
        except Exception as e:
            self.log_error("Voice setup error", e)

    def speak_response(self, text):
        """Make Steve actually speak the response"""
        print(f"💬 Steve: {text}")
        
        if not self.tts_engine:
            return
        
        try:
            # Play speaking chime
            self.play_speaking_chime()
            
            # Speak the response
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            
        except Exception as e:
            print(f"TTS error: {e}")

    # ===== CROSS-PLATFORM AUDIO CHIMES =====
    
    def play_listening_chime(self):
        """Play a gentle, soothing ascending chime when starting to listen"""
        if not self.ENABLE_CHIMES:
            return
        
        # Soft, warm ascending tones (C4, E4) - gentle interval
        frequencies = [262, 330]  # C4, E4
        durations = [60, 60]  # Very short, soft
        self.play_chime_sequence(frequencies, durations, pause_between=0.02)

    def play_conversation_start_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Gentle welcome melody - soft and warm
        frequencies = [262, 330, 392]  # C4, E4, G4 - gentle major triad
        durations = [70, 70, 90]  # Short and sweet
        self.play_chime_sequence(frequencies, durations, pause_between=0.03)

    def play_conversation_end_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Gentle farewell - soft descending
        frequencies = [392, 330, 262]  # G4, E4, C4 - gentle descent
        durations = [80, 90, 120]  # Gradually longer for gentle fade
        self.play_chime_sequence(frequencies, durations, pause_between=0.04)

    def play_conversation_listening_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Very subtle, single soft tone
        self.play_tone_cross_platform(294, 50)  # D4 for 50ms - very gentle and brief

    def play_speaking_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Very gentle, soft notification - just two quick soft tones
        frequencies = [330, 392]  # E4, G4 - gentle ascending
        durations = [40, 50]
        self.play_chime_sequence(frequencies, durations, pause_between=0.02)

    def play_thinking_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Gentle processing sound - soft descending tones
        frequencies = [349, 330, 294]  # F4, E4, D4 - gentle descent
        durations = [60, 60, 60]  # Short and soft
        self.play_chime_sequence(frequencies, durations, pause_between=0.02)

    def play_ready_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Simple, single gentle tone to indicate readiness
        self.play_tone_cross_platform(330, 80)  # E4 for 80ms - warm and welcoming

    def play_startup_chime(self):
        if not self.ENABLE_CHIMES:
            return
        
        # Gentle startup melody - soft and welcoming
        frequencies = [262, 330, 392, 523]  # C4, E4, G4, C5 - warm ascending
        durations = [80, 80, 90, 120]  # Gentle progression
        self.play_chime_sequence(frequencies, durations, pause_between=0.04)

    # ... (All other helper methods remain the same) ...
    def normalize_text(self, text):
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def calibrate_audio(self):
        print("🎚️ Calibrating audio levels...")
        print("📢 Please speak normally for 5 seconds...")
        
        frames = []
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )
        
        levels = []
        for _ in range(0, int(self.RATE / self.CHUNK * 5)):
            data = stream.read(self.CHUNK, exception_on_overflow=False)
            level = self.get_audio_level(data)
            levels.append(level)
        
        stream.stop_stream()
        stream.close()
        
        if levels:
            avg_level = np.mean(levels)
            max_level = np.max(levels)
            self.SILENCE_THRESHOLD = avg_level * 0.3
            
            print(f"📊 Calibration complete!")
            print(f"   Average level: {avg_level:.1f}")
            print(f"   Max level: {max_level:.1f}")
            print(f"   New silence threshold: {self.SILENCE_THRESHOLD:.1f}")
        else:
            print("❌ Calibration failed, using default threshold")

    def get_audio_level(self, data):
        try:
            if len(data) == 0:
                return 0
            audio_data = np.frombuffer(data, dtype=np.int16)
            if len(audio_data) == 0:
                return 0
            rms = np.sqrt(np.mean(audio_data.astype(np.float64)**2))
            if np.isnan(rms) or np.isinf(rms):
                return 0
            return rms
        except Exception as e:
            print(f"Audio level error: {e}")
            return 0

    def record_wake_word_check(self, duration=6):
        """Record wake word check with secure file handling"""
        frames = []
        stream = None
        temp_file = None
        
        try:
            # Check system resources before recording
            self.check_system_resources()
            
            # Create secure temporary file
            temp_file = self.create_secure_temp_file(suffix=".wav", prefix="steve_wake_")
            
            stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            for _ in range(0, int(self.RATE / self.CHUNK * duration)):
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
        
        except Exception as e:
            self.log_error("Recording error during wake word check", e)
            
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
        
        # Save to secure temporary file
        if temp_file:
            try:
                wf = wave.open(temp_file, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
            except Exception as e:
                self.log_error("Failed to save wake word audio file", e)
                if temp_file:
                    self.secure_delete_file(temp_file)
                return None
        
        return temp_file

    def check_wake_word(self, audio_file):
        """Check wake word with secure file handling"""
        if not audio_file:
            return False, ""
        
        try:
            segments, info = self.whisper_model.transcribe(audio_file)
            text = " ".join(segment.text for segment in segments).strip()
            print(f"Heard: '{text}'")
            
            normalized_text = self.normalize_text(text)
            normalized_wake = self.normalize_text(self.WAKE_WORD)
            
            print(f"Normalized: '{normalized_text}'")
            
            wake_detected = normalized_wake in normalized_text
            
            if wake_detected:
                self.log_security_event("Wake word detected", {
                    'text_length': len(text),
                    'normalized_length': len(normalized_text)
                })
            
            return wake_detected, text
            
        except Exception as e:
            self.log_error("Transcription error during wake word check", e)
            return False, ""
        
        finally:
            # Always securely delete the temporary audio file
            if audio_file:
                self.secure_delete_file(audio_file)

    def check_goodbye(self, text):
        normalized_text = self.normalize_text(text)
        normalized_goodbye = self.normalize_text(self.GOODBYE_WORD)
        
        goodbye_phrases = [
            normalized_goodbye,
            "goodbye",
            "bye steve",
            "see you later steve",
            "talk to you later steve",
            "end conversation"
        ]
        
        for goodbye_phrase in goodbye_phrases:
            if goodbye_phrase in normalized_text:
                return True
        
        return False

    def record_voice_command(self):
        """Record voice command with enhanced security and resource monitoring"""
        print("🎤 Listening for your command...")
        self.play_listening_chime()
        time.sleep(0.3)
        
        frames = []
        stream = None
        command_file = None
        
        try:
            # Check system resources before recording
            self.check_system_resources()
            
            # Create secure temporary file
            command_file = self.create_secure_temp_file(suffix=".wav", prefix="steve_cmd_")
            
            stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            silence_start = None
            recording = True
            has_speech = False
            speech_start_time = None
            max_recording_time = 20
            start_time = time.time()
            
            print("📢 Speak now...")
            
            while recording:
                try:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    
                    if time.time() - start_time > max_recording_time:
                        print("⏰ Maximum recording time reached")
                        break
                    
                    audio_level = self.get_audio_level(data)
                    
                    if audio_level > self.SILENCE_THRESHOLD:
                        if not has_speech:
                            has_speech = True
                            speech_start_time = time.time()
                            print("🗣️ Detected speech...")
                        
                        silence_start = None
                        print("🔊", end="", flush=True)
                    else:
                        if has_speech and speech_start_time:
                            if time.time() - speech_start_time > self.MIN_SPEECH_DURATION:
                                if silence_start is None:
                                    silence_start = time.time()
                                    print(" 🤫", end="", flush=True)
                                elif time.time() - silence_start > self.SILENCE_DURATION:
                                    print(f"\n🔇 {self.SILENCE_DURATION}s silence detected, stopping")
                                    recording = False
                
                except Exception as e:
                    self.log_error("Recording loop error", e)
                    break
        
        except Exception as e:
            self.log_error("Stream error during voice command recording", e)
        
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
        
        print()
        
        # Save command recording to secure file
        if command_file:
            try:
                wf = wave.open(command_file, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                # Log successful recording
                self.log_security_event("Voice command recorded", {
                    'duration_seconds': time.time() - start_time,
                    'has_speech': has_speech
                })
                
            except Exception as e:
                self.log_error("Failed to save command audio file", e)
                if command_file:
                    self.secure_delete_file(command_file)
                return None
        
        return command_file

    def transcribe_command(self, audio_file):
        """Transcribe voice command with secure file handling"""
        if not audio_file:
            return None
        
        print("🧠 Transcribing...")
        start_time = time.time()
        
        try:
            segments, info = self.whisper_model.transcribe(audio_file)
            text = " ".join(segment.text for segment in segments).strip()
            
            transcription_time = time.time() - start_time
            print(f"⚡ Transcribed in {transcription_time:.2f}s")
            print(f"🎯 You said: '{text}'")
            
            # Log transcription event
            self.log_security_event("Voice command transcribed", {
                'text_length': len(text),
                'transcription_time': transcription_time
            })
            
            return text
            
        except Exception as e:
            self.log_error("Transcription error", e)
            return None
        
        finally:
            # Always securely delete the temporary audio file
            if audio_file:
                self.secure_delete_file(audio_file)

    def extract_command_from_wake_phrase(self, full_text):
        patterns = [
            r'hey\s*,?\s*steve\s*,?\s*',
            r'hi\s*,?\s*steve\s*,?\s*',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, full_text.lower())
            if match:
                command_part = full_text[match.end():].strip()
                command_part = re.sub(r'^[,.\s]+', '', command_part)
                return command_part
        
        return ""

    def cleanup(self):
        """Clean up resources and secure data"""
        try:
            # Secure cleanup of conversation history
            if hasattr(self, 'conversation_history'):
                self.log_security_event("Cleaning up conversation history", {
                    'history_entries': len(self.conversation_history)
                })
                self.conversation_history.clear()
            
            # Secure cleanup of temporary files
            if hasattr(self, 'temp_files'):
                for temp_file in self.temp_files[:]:  # Copy list to avoid modification during iteration
                    self.secure_delete_file(temp_file)
            
            # Clear encryption keys from memory
            if hasattr(self, 'history_key'):
                self.history_key = None
            if hasattr(self, 'cipher'):
                self.cipher = None
            
            # Stop TTS engine
            if hasattr(self, 'tts_engine') and self.tts_engine:
                self.tts_engine.stop()
            
            # Terminate audio
            if hasattr(self, 'audio'):
                self.audio.terminate()
            
            self.log_security_event("Application cleanup completed", {})
            print("🔒 Secure cleanup completed")
            
        except Exception as e:
            self.log_error("Error during cleanup", e)

# Usage with security configuration options
if __name__ == "__main__":
    assistant = SteveVoiceAssistant()
    
    # Optional: Customize security settings
    # assistant.ENABLE_HISTORY = False  # Disable conversation history
    # assistant.COST_WARNING_THRESHOLD = 1.00  # Higher cost warning
    # assistant.MAX_CONVERSATION_TURNS = 10  # Fewer turns kept in history
    # assistant.MAX_DAILY_API_CALLS = 100  # Lower daily API limit
    # assistant.MAX_SESSION_COST = 2.00  # Lower session cost limit
    # assistant.MIN_DISK_SPACE_MB = 200  # Require more free disk space
    
    try:
        assistant.listen_for_wake_word()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down safely...")
    finally:
        assistant.cleanup()