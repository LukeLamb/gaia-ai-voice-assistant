# Gaia AI Voice Assistant - Project Structure

## 📁 Clean Modular Organization

```text
local_agent/
├── 🚀 gaia.py                    # Main entry point (GUI-first with --terminal flag)
├── 🔧 run_interface.py           # Interface runner for clean process separation
├── 🧪 run_tests.py               # Test runner for all test categories
├── 📋 requirements.txt           # Python dependencies
├── ⚙️ config.json               # Configuration settings
├── 💾 user_memory.json          # User memory storage
├── 📊 hotel_data.json           # Hotel system data
│
├── 🏗️ core/                     # Core system components
│   ├── 🤖 agent/               # AI agent logic
│   ├── 🎵 audio/               # Voice & TTS management
│   ├── 🧠 ai/                  # LLM interfaces
│   ├── 🔧 automation/          # App control & automation
│   ├── 💭 memory/              # User memory management
│   └── ⚙️ utils/               # Utilities & config
│
├── 🖥️ gui/                      # GUI components
│   ├── 🚀 simple_launcher.py   # Professional GUI launcher
│   ├── 🪟 main_window.py       # Main application window
│   └── 🧩 widgets/             # GUI widgets & components
│
├── 🌐 src/                      # Source interfaces
│   └── 📱 interfaces/          # CLI & other interfaces
│
├── 📚 docs/                     # Documentation
│   ├── 🏗️ architecture/        # Architecture documentation
│   ├── 🏨 hotel/               # Hotel system docs
│   ├── 🔄 migration/           # Migration documentation
│   └── ⚙️ setup/               # Setup guides
│
├── 🧪 tests/                    # Test suite
│   ├── 🏗️ architecture/        # Architecture tests
│   ├── 🏗️ core/                # Core component tests
│   ├── 🏨 hotel/               # Hotel system tests
│   ├── 📱 interfaces/          # Interface tests
│   └── 🧠 llm/                 # LLM tests
│
├── 📝 examples/                 # Examples & demos
│   ├── 📧 email integration examples
│   ├── 🎓 training examples
│   └── 🛠️ setup guides
│
├── 🗃️ legacy/                   # Deprecated files
│   ├── 📜 main.py (old)
│   ├── 📜 voice_agent.py (old)
│   └── 📜 other deprecated files
│
└── 🎨 resources/               # Resources & assets
    └── 🎵 audio files, icons, etc.
```

## 🔧 Main Components

### **Entry Points:**

- **`gaia.py`** - Main entry point (GUI-first, --terminal for CLI)
- **`run_interface.py`** - Clean interface runner
- **`run_tests.py`** - Comprehensive test runner

### **Core System:**

- **Agent**: GaiaAgent with conversation mode & smart recording
- **Audio**: VoiceManager, AzureTTS, TTSManager with activity detection
- **AI**: LocalLLM interface with personalized responses
- **Memory**: User memory with persistent storage
- **Automation**: App control and system automation

### **GUI System:**

- **Professional Launcher**: Dark-themed with subprocess management
- **Main Window**: Integrated chat, system logs, and controls
- **Widgets**: Modular UI components for extensibility

### **Organization Benefits:**

✅ **Clean separation** of concerns
✅ **Easy navigation** with logical folder structure
✅ **Clear entry points** for different use cases
✅ **Comprehensive testing** organized by component
✅ **Well-documented** architecture and setup
✅ **Examples** for learning and extension
✅ **Legacy preservation** without clutter

## 🚀 Quick Start

1. **GUI Mode**: `python gaia.py`
2. **Terminal Mode**: `python gaia.py --terminal`
3. **Run Tests**: `python run_tests.py`
4. **Interface Runner**: `python run_interface.py gui`

## 📋 Features Included

- ✅ Professional GUI launcher with user identification
- ✅ Smart voice recording with activity detection
- ✅ Conversation mode (30-second timeout)
- ✅ Robust command parsing with error handling
- ✅ User memory and personalization
- ✅ Azure TTS with local fallback
- ✅ Comprehensive test suite
- ✅ Clean modular architecture
- ✅ Extensive documentation
