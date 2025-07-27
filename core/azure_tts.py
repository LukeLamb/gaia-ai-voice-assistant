import azure.cognitiveservices.speech as speechsdk

class AzureTTS:
    def __init__(self, key: str, region: str, voice: str = "en-GB-SoniaNeural"):
        self.key = key
        self.region = region
        self.voice = voice
        self.speech_config = speechsdk.SpeechConfig(subscription=self.key, region=self.region)
        self.speech_config.speech_synthesis_voice_name = self.voice
        self.synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def speak(self, text: str):
        """Synthesize and speak the provided text using Azure TTS."""
        try:
            result = self.synthesizer.speak_text_async(text).get()
            
            if result is None:
                print("[AzureTTS] Error: No result returned from speech synthesis")
                return False
                
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = speechsdk.CancellationDetails(result)
                print(f"[AzureTTS] Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    print(f"[AzureTTS] Error details: {cancellation_details.error_details}")
                return False
            else:
                print(f"[AzureTTS] Error synthesizing speech: {result.reason}")
                return False
                
        except Exception as e:
            print(f"[AzureTTS] Exception during speech synthesis: {e}")
            return False

