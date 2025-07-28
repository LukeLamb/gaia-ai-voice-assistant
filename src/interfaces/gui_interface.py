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
            # Check if QApplication already exists (from launcher)
            existing_app = QApplicationClass.instance()
            
            if existing_app is None:
                # Create new application if none exists
                self.app = QApplicationClass(sys.argv)
                self.app.setApplicationName("Gaia AI Assistant")
                self.app.setApplicationVersion("3.0")
                self.app.setOrganizationName("Gaia AI")
                
                self.main_window = GaiaMainWindowClass()
                self.main_window.show()
                
                return self.app.exec_()
            else:
                # Use existing application - show window and wait for user input
                self.main_window = GaiaMainWindowClass()
                self.main_window.show()
                
                # Keep the interface running until user closes the window
                print("✅ GUI window opened. Close the window to continue...")
                while self.main_window.isVisible():
                    existing_app.processEvents()
                    import time
                    time.sleep(0.1)
                
                return 0
            
        except Exception as e:
            print(f"❌ GUI Error: {e}")
            print("Try running: python -m pip install PyQt5")
            return 1
