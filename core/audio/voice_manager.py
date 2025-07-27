import os
import tempfile
import pyaudio
import wave
from faster_whisper import WhisperModel

class VoiceManager:
    def __init__(self, model_size="base"):
        """
        Initialize Whisper model with automatic CUDA detection.
        Falls back to CPU if GPU is not available.
        """
        self.device = "cuda" if self._cuda_available() else "cpu"
        print(f"[VoiceManager] Initializing Whisper on {self.device.upper()}...")
        self.model = WhisperModel(model_size, device=self.device, compute_type="float16" if self.device == "cuda" else "int8")

    def _cuda_available(self):
        """Check if CUDA is available via environment variables or nvidia-smi."""
        try:
            # Check if CUDA_VISIBLE_DEVICES is set
            if "CUDA_VISIBLE_DEVICES" in os.environ and os.environ["CUDA_VISIBLE_DEVICES"] == "":
                return False

            # Try to run nvidia-smi to see if a GPU is present
            import subprocess
            result = subprocess.run(["nvidia-smi"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except Exception:
            return False

    def record_audio(self, duration=5, filename=None):
        """Record audio from microphone with improved sensitivity."""
        if filename is None:
            filename = os.path.join(tempfile.gettempdir(), "input.wav")

        chunk = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 16000

        p = None
        stream = None
        frames = []
        sample_width = 2  # Default for paInt16
        
        try:
            p = pyaudio.PyAudio()
            sample_width = p.get_sample_size(audio_format)
            
            # Find the best input device
            input_device_index = None
            for i in range(p.get_device_count()):
                info = p.get_device_info_by_index(i)
                max_inputs = info.get('maxInputChannels', 0)
                if isinstance(max_inputs, (int, float)) and max_inputs > 0:
                    input_device_index = i
                    break
            
            stream = p.open(
                format=audio_format, 
                channels=channels, 
                rate=rate, 
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=chunk
            )

            # Start recording
            for _ in range(0, int(rate / chunk * duration)):
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            
        except Exception as e:
            print(f"Error during recording: {e}")
            return None
        finally:
            if stream:
                stream.stop_stream()
                stream.close()
            if p:
                p.terminate()

        try:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(channels)
                wf.setsampwidth(sample_width)
                wf.setframerate(rate)
                wf.writeframes(b''.join(frames))
        except Exception as e:
            print(f"Error saving audio file: {e}")
            return None

        return filename

    def transcribe(self, audio_file):
        """Convert speech to text."""
        try:
            if not hasattr(self, 'model') or not self.model:
                print("VoiceManager model not available")
                return ""
                
            if not os.path.exists(audio_file):
                print(f"Audio file not found: {audio_file}")
                return ""
            
            segments, _ = self.model.transcribe(audio_file)
            text = " ".join([seg.text for seg in segments])
            return text.strip()
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""

    def cleanup(self):
        """Clean up resources."""
        try:
            if hasattr(self, 'model') and self.model:
                # Whisper model cleanup
                del self.model
                self.model = None
                print("[VoiceManager] Whisper model cleaned up")
        except Exception as e:
            print(f"[VoiceManager] Cleanup error: {e}")

