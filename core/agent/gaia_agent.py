import re
import threading
import time
from datetime import datetime
from core.ai.llm_interface import LocalLLM
from core.audio.voice_manager import VoiceManager
from core.audio.azure_tts import AzureTTS
from core.audio.tts_manager import TTSManager
from core.utils.config_manager import ConfigManager
from core.memory.user_memory import UserMemory
from core.automation import app_control
from core.agent.command_parser import CommandParser

WAKE_WORD = "gaia"  # Wake word

class GaiaAgent:
    """Main Gaia AI Agent with modular architecture"""
    
    def __init__(self, log_callback=None, conversation_callback=None):
        self.log_callback = log_callback or (lambda msg: print(msg))
        self.conversation_callback = conversation_callback or (lambda speaker, msg: None)
        
        # Initialize components
        self._initialize_components()
        
        # State management
        self.running = False
        self.paused = False
        self.sleep_mode = False
        self.awaiting_name = False
        self.agent_thread = None
        
    def _initialize_components(self):
        """Initialize all components"""
        try:
            # Configuration
            config = ConfigManager()
            azure_key = config.get("azure_key")
            azure_region = config.get("azure_region")
            voice = config.get("voice", "en-US-AriaNeural")
            
            # Audio components
            self.azure_tts = AzureTTS(key=azure_key, region=azure_region, voice=voice)
            self.local_tts = TTSManager()
            self.voice = VoiceManager()
            
            # AI components
            self.llm = LocalLLM()
            
            # Memory and parsing
            self.user_memory = UserMemory()
            self.command_parser = CommandParser()
            
            self.log("Components initialized successfully")
            
        except Exception as e:
            self.log(f"Error initializing components: {e}")
            raise

    def log(self, message):
        self.log_callback(message)

    def speak(self, text):
        """Robust TTS with Azure → Local fallback"""
        try:
            success = self.azure_tts.speak(text)
            if success:
                self.log(f"Gaia: {text}")
                self.conversation_callback("Gaia", text)
            else:
                # Azure failed, try local
                self.local_tts.speak(text)
                self.log(f"Gaia: {text}")
                self.conversation_callback("Gaia", text)
        except Exception as e:
            self.log(f"Azure TTS Error: {e}")
            try:
                self.local_tts.speak(text)
                self.log(f"Gaia: {text}")
                self.conversation_callback("Gaia", text)
            except Exception as e2:
                self.log(f"TTS Error: {e2}")

    def process_command(self, command: str):
        """Process a voice command"""
        try:
            self.log(f"Processing command: {command}")
            
            # Handle name input during introduction
            if self.awaiting_name:
                self._handle_name_input(command)
                return
            
            # Parse and execute command
            self._execute_parsed_command(command)
                
        except Exception as e:
            self.log(f"Error processing command: {e}")
            self.speak("Sorry, I encountered an error processing your request.")
    
    def _handle_name_input(self, command: str):
        """Handle name input during user introduction"""
        name = self._extract_name(command)
        if name:
            self.user_memory.set_user_name(name)
            self.speak(f"Nice to meet you, {name}! I'll remember you. What can I help you with?")
            self.awaiting_name = False
        else:
            self.speak("Sorry, I didn't catch your name. Could you tell me again?")
    
    def _execute_parsed_command(self, command: str):
        """Execute command using parser or LLM"""
        self.log("Parsing command with command parser...")
        result = self.command_parser.parse_and_execute(command)
        
        if result:
            self._handle_parser_result(result)
        else:
            self._handle_llm_conversation(command)
    
    def _handle_parser_result(self, result):
        """Handle result from command parser"""
        self.log(f"Command parser returned: {type(result)} - {result}")
        if isinstance(result, list):
            for item in result:
                self.speak(item)
        else:
            self.speak(result)
    
    def _handle_llm_conversation(self, command: str):
        """Handle general conversation using LLM"""
        self.log("No command match, using LLM for response...")
        user_name = self.user_memory.get_user_name() or "there"
        self.log(f"Debug: user_name retrieved = '{user_name}', is_user_known = {self.user_memory.is_user_known()}")
        
        # Make the prompt more personal to encourage using the user's name
        if user_name and user_name != "there":
            response = self.llm.ask(f"Your user {user_name} asked: '{command}'. Please provide a helpful and friendly response. You can address them by name when appropriate.")
        else:
            response = self.llm.ask(f"The user asked: '{command}'. Please provide a helpful and friendly response.")
        
        self.log(f"LLM response: {response}")
        self.speak(response)
            
    def _extract_name(self, text):
        """Extract name from user input"""
        text = text.lower().strip()
        patterns = [
            r"i am (\w+)",
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"it's (\w+)",
            r"(\w+)$"  # Just the name
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                name = match.group(1).strip()
                # Filter out common words that aren't names
                if name not in ["yes", "no", "the", "a", "an", "is", "am", "are", "gaia"]:
                    return name.capitalize()
        return None
        
    def listen_for_wake_word(self):
        """Listen for the wake word"""
        while self.running and not self.sleep_mode:
            if self.paused:
                time.sleep(0.5)
                continue
                
            try:
                # Use shorter duration for wake word to be more responsive
                audio_file = self.voice.record_audio(duration=2)
                transcription = self.voice.transcribe(audio_file).lower().strip()
                
                # Only log if something was actually heard
                if transcription:
                    self.log(f"Luke: {transcription}")
                    self.conversation_callback("Luke", transcription)
                    if WAKE_WORD in transcription:
                        return True
            except Exception as e:
                self.log(f"Error in wake word detection: {e}")
                time.sleep(1)
                
        return False
        
    def handle_sleep_mode(self):
        """Handle sleep mode"""
        while self.sleep_mode and self.running:
            if self.paused:
                time.sleep(0.5)
                continue
                
            try:
                audio_file = self.voice.record_audio(duration=3)
                transcription = self.voice.transcribe(audio_file).lower().strip()
                if transcription and "wake up" in transcription and WAKE_WORD in transcription:
                    self.log(f"Luke: {transcription}")
                    self.conversation_callback("Luke", transcription)
                    self.speak("I'm awake.")
                    self.sleep_mode = False
            except Exception as e:
                self.log(f"Error in sleep mode: {e}")
                time.sleep(1)
                
    def _handle_first_time_user(self):
        """Handle first-time user introduction"""
        self.speak("Hello! Who are you?")
        self.awaiting_name = True
        
        # Get name response
        try:
            # Longer duration for name input
            audio_file = self.voice.record_audio(duration=8)
            command = self.voice.transcribe(audio_file).strip().lower()
            if command:
                self.log(f"Luke: {command}")
                self.process_command(command)
        except Exception as e:
            self.log(f"Error getting user name: {e}")
            
    def _handle_normal_command(self):
        """Handle normal command processing"""
        try:
            self.log("Listening for command...")
            # Use smart recording to capture complete sentences
            audio_file = self.voice.record_audio_smart(max_duration=10, silence_duration=2)
            if not audio_file:
                self.log("Smart recording failed, falling back to regular recording")
                audio_file = self.voice.record_audio(duration=8)
                
            command = self.voice.transcribe(audio_file).strip().lower()

            if not command:
                self.log("No command received, returning to wake word detection")
                return False

            self.log(f"Luke: {command}")
            self.conversation_callback("Luke", command)

            if "sleep" in command:
                self.speak("Going to sleep. Say 'Wake up, Gaia' to wake me.")
                self.sleep_mode = True
                return True
            else:
                self.log("Processing command...")
                self.process_command(command)
                self.log("Command processing complete")
                return True
                
        except Exception as e:
            self.log(f"Error handling command: {e}")
            self.speak("Sorry, I had trouble processing that. Please try again.")
            return False
            
    def _greet_user(self):
        """Provide personalized greeting"""
        if self.user_memory.is_user_known():
            user_name = self.user_memory.get_user_name()
            self.speak(f"Welcome back, {user_name}! Gaia is ready. Say 'Gaia' to activate me.")
            self.user_memory.update_last_seen()
        else:
            self.speak("Welcome to Gaia! Gaia is ready. Say 'Gaia' to activate me.")

    def run(self):
        """Main execution loop"""
        try:
            # Personalized greeting
            self._greet_user()
            
            # Main loop
            self._main_execution_loop()
                        
        except Exception as e:
            self.log(f"Error in main loop: {e}")
    
    def _main_execution_loop(self):
        """Main execution loop handling different states"""
        while self.running:
            try:
                if self._should_pause_or_sleep():
                    continue
                    
                if self.listen_for_wake_word():
                    self._handle_wake_word_activation()
                    
            except Exception as e:
                self.log(f"Error in main loop iteration: {e}")
                time.sleep(1)  # Brief pause before retrying
    
    def _should_pause_or_sleep(self):
        """Check if agent should pause or enter sleep mode"""
        if self.paused:
            time.sleep(0.5)
            return True
            
        if self.sleep_mode:
            self.handle_sleep_mode()
            return True
            
        return False
    
    def _handle_wake_word_activation(self):
        """Handle actions after wake word is detected"""
        # Handle first-time user introduction
        if not self.user_memory.is_user_known():
            self._handle_first_time_user()
            return
        else:
            self.speak("Yes, I'm listening.")
            
        # Enter conversation mode
        self._enter_conversation_mode()
    
    def _enter_conversation_mode(self):
        """Enter conversation mode with timeout management"""
        conversation_timeout = 30  # seconds
        start_time = time.time()
        
        while self._should_continue_conversation(start_time, conversation_timeout):
            command_received = self._handle_normal_command()
            
            if command_received:
                # Reset timeout if command was received
                start_time = time.time()
            else:
                # No command received, brief pause
                time.sleep(1)
        
        # If we exit conversation mode due to timeout, let user know
        if (time.time() - start_time) >= conversation_timeout:
            self.log("Conversation timeout - returning to wake word detection")
    
    def _should_continue_conversation(self, start_time, timeout):
        """Check if conversation mode should continue"""
        return (self.running and not self.paused and not self.sleep_mode and 
                (time.time() - start_time) < timeout)

    def start(self):
        """Start the agent"""
        self.running = True
        self.paused = False
        self.agent_thread = threading.Thread(target=self.run, daemon=False)
        self.agent_thread.start()

    def stop(self):
        """Stop the agent"""
        self.running = False
        user_name = self.user_memory.get_user_name()
        if user_name:
            self.speak(f"Goodbye, {user_name}!")
        else:
            self.speak("Shutting down. Goodbye.")
        self.log("System: Gaia stopped.")
        
        # Clean up audio components
        try:
            if hasattr(self, 'voice') and self.voice:
                self.voice.cleanup()
            if hasattr(self, 'local_tts') and self.local_tts:
                self.local_tts.cleanup()
            if hasattr(self, 'azure_tts') and self.azure_tts:
                # Azure TTS might need cleanup too
                pass
            self.log("Audio components cleaned up")
        except Exception as e:
            self.log(f"Error during audio cleanup: {e}")
        
        # Wait for the agent thread to finish
        if hasattr(self, 'agent_thread') and self.agent_thread and self.agent_thread.is_alive():
            self.log("Waiting for agent thread to stop...")
            self.agent_thread.join(timeout=5.0)  # Wait up to 5 seconds
            if self.agent_thread.is_alive():
                self.log("Warning: Agent thread did not stop gracefully")
        
        time.sleep(0.5)

    def pause(self):
        self.paused = True
        self.log("System: Gaia paused.")
        self.speak("Gaia is paused.")

    def resume(self):
        self.paused = False
        self.log("System: Gaia resumed.")
        self.speak("Gaia is active again.")







