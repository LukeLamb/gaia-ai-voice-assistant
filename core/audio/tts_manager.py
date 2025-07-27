import pyttsx3

class TTSManager:
    def __init__(self, rate=180, volume=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text: str):
        """Speak the provided text aloud."""
        if hasattr(self, 'engine') and self.engine:
            self.engine.say(text)
            self.engine.runAndWait()
        else:
            print("TTS engine not available")

    def cleanup(self):
        """Clean up TTS resources."""
        try:
            if hasattr(self, 'engine') and self.engine:
                self.engine.stop()
                del self.engine
                self.engine = None
                print("[TTSManager] TTS engine cleaned up")
        except Exception as e:
            print(f"[TTSManager] Cleanup error: {e}")
