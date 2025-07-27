"""
GUI Interface - Professional PyQt5 Interface
Clean, modular GUI interface for Gaia AI Assistant
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from PyQt5.QtWidgets import QApplication
    from gui.main_window import GaiaMainWindow
    GUI_AVAILABLE = True
    QApplicationClass = QApplication
    GaiaMainWindowClass = GaiaMainWindow
except ImportError:
    GUI_AVAILABLE = False
    QApplicationClass = None
    GaiaMainWindowClass = None


class GUIInterface:
    """
    Professional PyQt5 GUI interface
    """
    
    def __init__(self):
        if not GUI_AVAILABLE or QApplicationClass is None or GaiaMainWindowClass is None:
            raise ImportError("PyQt5 not available. Install with: pip install PyQt5")
        
        self.app = None
        self.main_window = None
    
    def run(self):
        """Run the GUI interface"""
        print("🖥️ Starting Gaia AI GUI Interface...")
        
        if not GUI_AVAILABLE or QApplicationClass is None or GaiaMainWindowClass is None:
            print("❌ GUI components not available")
            print("Try running: python -m pip install PyQt5")
            return 1
        
        try:
            self.app = QApplicationClass(sys.argv)
            self.app.setApplicationName("Gaia AI Assistant")
            self.app.setApplicationVersion("3.0")
            self.app.setOrganizationName("Gaia AI")
            
            self.main_window = GaiaMainWindowClass()
            self.main_window.show()
            
            return self.app.exec_()
            
        except Exception as e:
            print(f"❌ GUI Error: {e}")
            print("Try running: python -m pip install PyQt5")
            return 1
        
        finally:
            if self.app:
                self.app.quit()
