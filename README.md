# Gaia - Local AI Voice Assistant

A comprehensive voice-controlled AI assistant built with Python that combines Azure Speech Services, Whisper AI, and local LLM integration for intelligent voice interactions.

## Features

- 🎤 **Voice Recognition**: CUDA-accelerated Whisper AI for speech-to-text
- 🗣️ **Text-to-Speech**: Azure Neural TTS with local fallback
- 🤖 **Local AI**: Ollama/LLaMA integration for conversational responses
- 💻 **Windows Automation**: Excel, Word, Outlook, and app control
- 🎨 **Professional GUI**: Clean Tkinter interface with tabs and controls
- 🔧 **Wake Word Detection**: "Gaia" activation with sleep mode
- 🛡️ **Robust Fallbacks**: Azure → Local TTS failover system

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Azure Speech** (optional, has local fallback):
   - Copy `config.json.example` to `config.json`
   - Add your Azure Speech Service key and region

3. **Run Gaia**:
   ```bash
   python gaia_gui.py
   ```

## Architecture

```
gaia_gui.py          # Professional Tkinter GUI interface
voice_agent.py       # Core GaiaAgent with TTS fallback system
core/
├── azure_tts.py     # Azure Neural TTS integration
├── tts_manager.py   # Local TTS fallback (pyttsx3)
├── voice_manager.py # Whisper speech recognition
├── local_llm_interface.py # Ollama/LLaMA integration
└── app_control.py   # Windows automation (Excel, Word, etc.)
```

## Usage

1. **Start**: Click "Start Gaia" in the GUI
2. **Activate**: Say "Gaia" to wake the assistant
3. **Command**: Give voice commands after hearing "Yes, I'm listening"
4. **Monitor**: View logs and conversations in separate tabs

### Voice Commands

- "What time is it?" → Gets current time
- "What's the date?" → Gets current date  
- "Create an Excel file" → Creates new Excel workbook
- "Create a Word document" → Creates new Word document
- "Open [app name]" → Opens specified application
- "Sleep" → Puts Gaia into sleep mode
- "Wake up, Gaia" → Wakes from sleep mode

## Configuration

### Azure Speech (Optional)
```json
{
  "azure_key": "your-azure-speech-key",
  "azure_region": "your-region",
  "voice": "en-US-AriaNeural"
}
```

### Environment Setup
- **Python 3.13+** required
- **CUDA support** recommended for Whisper acceleration
- **Ollama** for local LLM functionality

## Development

### Critical Features
- ✅ TTS Fallback System (Azure → Local)
- ✅ Voice Debug Logging ("Heard: ..." output)
- ✅ Robust Error Handling
- ✅ Professional GUI Interface
- ✅ Windows Automation

### Recent Updates
- Added robust TTS fallback system with Azure → Local failover
- Implemented comprehensive voice debug logging
- Enhanced error handling for production reliability
- Professional GUI with conversation history

## Dependencies

See `requirements.txt` for complete list:
- `tkinter` - GUI framework
- `azure-cognitiveservices-speech` - Azure TTS
- `faster-whisper` - Speech recognition
- `pyttsx3` - Local TTS fallback
- `requests` - HTTP client for LLM
- `pyaudio` - Audio recording
- `pywin32` - Windows automation

## License

MIT License - See LICENSE file for details

---

**Status**: Production-ready with robust fallback systems ✅
