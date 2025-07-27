import re
import threading
import time
from datetime import datetime
from core.local_llm_interface import LocalLLM
from core.voice_manager import VoiceManager
from core.azure_tts import AzureTTS
from core.tts_manager import TTSManager
from core.config_manager import ConfigManager
from core import app_control

WAKE_WORD = "gaia"  # Wake word

class GaiaAgent:
    def __init__(self, log_callback=None):
        config = ConfigManager()
        azure_key = config.get("azure_key")
        azure_region = config.get("azure_region")
        voice = config.get("voice", "en-GB-SoniaNeural")

        self.azure_tts = AzureTTS(key=azure_key, region=azure_region, voice=voice)
        self.local_tts = TTSManager()  # Local backup TTS
        self.llm = LocalLLM()
        self.voice = VoiceManager()
        self.running = False
        self.paused = False
        self.sleep_mode = False
        self.log_callback = log_callback or (lambda msg: print(msg))

    def log(self, message):
        self.log_callback(message)

    def speak(self, text):
        """Robust TTS with Azure → Local fallback"""
        try:
            self.azure_tts.speak(text)
            self.log(f"Azure TTS: {text}")
        except Exception as e:
            self.log(f"Azure TTS failed: {e}")
            try:
                self.local_tts.speak(text)
                self.log(f"Local TTS: {text}")
            except Exception as e2:
                self.log(f"All TTS failed: {e2}")

    def get_current_time(self):
        """Get current time in a friendly format"""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"

    def get_current_date(self):
        """Get current date in a friendly format"""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"

    def parse_command(self, command: str):
        command = command.lower()
        if "time" in command or "what time" in command:
            return ("time", self.get_current_time)
        elif "date" in command or "what date" in command or "today" in command:
            return ("date", self.get_current_date)
        elif "email" in command:
            return ("email", app_control.check_outlook_inbox)
        elif "excel" in command:
            return ("excel", lambda: app_control.create_excel("ai_created.xlsx"))
        elif "word" in command or "document" in command:
            return ("word", lambda: app_control.create_word_doc("ai_created.docx"))
        elif "open" in command:
            app_match = re.search(r"open (.+)", command)
            app_name = app_match.group(1) if app_match else "notepad.exe"
            return ("open_app", lambda: app_control.open_app(app_name))
        return (None, None)

    def listen_for_wake_word(self):
        while self.running and not self.sleep_mode:
            if self.paused:
                time.sleep(0.5)
                continue
            self.log("Listening for wake word...")
            audio_file = self.voice.record_audio(duration=3)
            transcription = self.voice.transcribe(audio_file).lower()
            self.log(f"Heard: '{transcription}'")
            if WAKE_WORD in transcription:
                self.log("Wake word detected: Gaia")
                return True
        return False

    def handle_sleep_mode(self):
        while self.sleep_mode and self.running:
            if self.paused:
                time.sleep(0.5)
                continue
            self.log("Gaia is sleeping... say 'Wake up, Gaia'.")
            audio_file = self.voice.record_audio(duration=3)
            transcription = self.voice.transcribe(audio_file).lower()
            self.log(f"Heard: '{transcription}'")
            if "wake up" in transcription and WAKE_WORD in transcription:
                self.speak("I'm awake.")
                self.log("Gaia woke up.")
                self.sleep_mode = False

    def process_command(self, command: str):
        action_name, action_func = self.parse_command(command)
        if action_func:
            self.speak(f"Executing {action_name} action.")
            self.log(f"AI: Executing {action_name}...")
            result = action_func()
            if isinstance(result, list):
                for r in result:
                    self.log(f"AI: {r}")
                    self.speak(r)
            else:
                self.log(f"AI: {result}")
                self.speak(result)
        else:
            response = self.llm.ask(f"User said: {command}. Provide a helpful response.")
            self.log(f"AI: {response}")
            self.speak(response)

    def run(self):
        self.speak("Gaia is ready. Say 'Gaia' to activate me.")
        self.log("AI: Gaia is ready and listening for wake word.")

        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue

            if self.sleep_mode:
                self.handle_sleep_mode()
                continue

            if self.listen_for_wake_word():
                self.speak("Yes, I'm listening.")
                audio_file = self.voice.record_audio(duration=5)
                command = self.voice.transcribe(audio_file).strip().lower()

                if not command:
                    self.log("AI: No command detected.")
                    continue

                self.log(f"You said: {command}")
                self.speak(f"You said: {command}")

                if "sleep" in command:
                    self.speak("Going to sleep. Say 'Wake up, Gaia' to wake me.")
                    self.log("AI: Entering sleep mode.")
                    self.sleep_mode = True
                else:
                    self.process_command(command)

    def start(self):
        self.running = True
        self.paused = False
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.running = False
        self.speak("Shutting down. Goodbye.")
        self.log("AI: Gaia stopped.")
        time.sleep(0.5)

    def pause(self):
        self.paused = True
        self.log("AI: Gaia paused.")
        self.speak("Gaia is paused.")

    def resume(self):
        self.paused = False
        self.log("AI: Gaia resumed.")
        self.speak("Gaia is active again.")







