import subprocess
import shutil
import ollama

class LocalLLM:
    def __init__(self, model="llama3"):
        self.model = model
        self.ollama_path = shutil.which("ollama") or r"C:\Users\infob\AppData\Local\Programs\Ollama\ollama.exe"
        self._check_ollama()

    def _check_ollama(self):
        """Check if Ollama CLI is available."""
        try:
            if not self.ollama_path or not shutil.which("ollama"):
                # Try running with full path if not in PATH
                result = subprocess.run([self.ollama_path, "--version"], capture_output=True, text=True)
            else:
                result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise FileNotFoundError
        except Exception:
            print("[ERROR] Ollama is not installed or not accessible in PATH.")
            print("Please install it from: https://ollama.ai/download")
            print("Or add the following to your PATH:")
            print(r"C:\Users\infob\AppData\Local\Programs\Ollama")
            raise SystemExit

    def ask(self, prompt: str) -> str:
        """Send a query to the local LLaMA model."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"[Local LLM Error] {e}"

