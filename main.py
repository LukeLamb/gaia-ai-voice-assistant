"""
⚠️  DEPRECATED: This file is obsolete and replaced by the new modular architecture.

This simple main.py has been superseded by:
- main_new.py (new PyQt5 GUI entry point)
- core/agent/gaia_agent.py (full voice assistant functionality)

🚀 To use the new Gaia system:
   python main_new.py

📋 Benefits of new system:
- Professional PyQt5 GUI with dark theme
- Complete voice assistant with wake word detection
- User memory and personalization
- Azure TTS with local fallback
- Modular architecture for easy extension

🗂️ This file will be removed in the next cleanup.
"""

import warnings
import sys

warnings.warn(
    "main.py is deprecated. Use 'python main_new.py' for the full Gaia experience",
    DeprecationWarning,
    stacklevel=2
)

def main():
    print("⚠️  This is the old main.py - please use the new system!")
    print("🚀 Run: python main_new.py")
    print("📋 For the full Gaia AI Voice Assistant experience")
    
    response = input("\nWould you like to start the new system? (y/n): ")
    if response.lower() in ['y', 'yes']:
        import subprocess
        try:
            subprocess.run([sys.executable, "main_new.py"])
        except Exception as e:
            print(f"Error starting new system: {e}")
            print("Please run: python main_new.py")
    else:
        print("Exiting. Run 'python main_new.py' when ready!")

if __name__ == "__main__":
    main()
