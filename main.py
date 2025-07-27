from core.local_llm_interface import LocalLLM
from core.voice_manager import VoiceManager
from core.tts_manager import TTSManager
from core import app_control

def main():
    tts = TTSManager()
    llm = LocalLLM()
    voice = VoiceManager()

    print("Local AI Agent Ready. Say something...")
    tts.speak("Local AI Agent is ready. Say something.")

    # Example test loop (voice → LLM → action)
    audio_file = voice.record_audio(duration=5)
    command = voice.transcribe(audio_file)
    print(f"You said: {command}")
    tts.speak(f"You said: {command}")

    # Process command via LLM
    response = llm.ask(f"User command: {command}. What should I do?")
    print(f"AI Response: {response}")
    tts.speak(response)

    # Example: Check emails if user mentions 'email'
    if "email" in command.lower():
        emails = app_control.check_outlook_inbox(limit=3)
        for mail in emails:
            print(mail)
            tts.speak(mail)

if __name__ == "__main__":
    main()
