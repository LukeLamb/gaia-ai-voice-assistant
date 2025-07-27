import pyttsx3

class TTSManager:
    def __init__(self, rate=180, volume=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text: str):
        """Speak the provided text aloud."""
        self.engine.say(text)
        self.engine.runAndWait()
