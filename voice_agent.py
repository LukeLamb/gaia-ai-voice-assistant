"""
⚠️  DEPRECATED: This file is obsolete and replaced by the new modular architecture.

This monolithic voice_agent.py has been superseded by:
- core/agent/gaia_agent.py (main agent with reduced complexity)
- core/agent/command_parser.py (command parsing logic)
- gui/main_window.py (professional PyQt5 interface)
- main_new.py (new entry point)

🚀 To use the new Gaia system:
   python main_new.py

📋 Benefits of new architecture:
- Reduced cognitive complexity (SonarLint compliant)
- Professional PyQt5 GUI with dark theme
- Modular structure for better maintainability
- Enhanced error handling and logging
- Threaded architecture for responsive GUI

🗂️ This file will be removed in the next cleanup.
"""

# Import the new agent for backwards compatibility
import warnings
from core.agent.gaia_agent import GaiaAgent as NewGaiaAgent

warnings.warn(
    "voice_agent.py is deprecated. Use 'python main_new.py' or import from 'core.agent.gaia_agent'",
    DeprecationWarning,
    stacklevel=2
)

# Alias for backwards compatibility (if needed)
GaiaAgent = NewGaiaAgent







