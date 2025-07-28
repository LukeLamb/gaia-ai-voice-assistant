"""
Simple GUI Launcher for Gaia AI Assistant
"""

import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QMouseEvent


class ClickableFrame(QFrame):
    """Clickable frame widget for interface buttons"""
    clicked = pyqtSignal(str)
    
    def __init__(self, interface_type):
        super().__init__()
        self.interface_type = interface_type
        self.setFixedSize(300, 80)
        self.setStyleSheet("""
            QFrame {
                background-color: #3c3c3c;
                border: 2px solid #555;
                border-radius: 10px;
            }
            QFrame:hover {
                background-color: #4a4a4a;
                border: 2px solid #4CAF50;
            }
        """)
        
    def mousePressEvent(self, a0):  # type: ignore
        if a0 and a0.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.interface_type)  # type: ignore
        super().mousePressEvent(a0)


class GaiaLauncherWindow(QMainWindow):
    """Simple and effective launcher window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🤖 Gaia AI Assistant - Launcher")
        self.setFixedSize(700, 500)
        self.center_window()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        self.create_header(main_layout)
        
        # Interface buttons
        self.create_interface_buttons(main_layout)
        
        # Footer
        self.create_footer(main_layout)
        
        # Apply dark theme
        self.apply_theme()
        
    def center_window(self):
        """Center the window on screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().availableGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
    def create_header(self, layout):
        """Create header section"""
        header = QFrame()
        header_layout = QVBoxLayout(header)
        
        # Title
        title = QLabel("🤖 GAIA AI ASSISTANT")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #4CAF50; text-align: center;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Professional Modular AI System")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #cccccc; text-align: center;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
    def create_interface_buttons(self, layout):
        """Create interface selection buttons"""
        buttons_frame = QFrame()
        grid = QGridLayout(buttons_frame)
        grid.setSpacing(15)
        
        # Define interfaces
        interfaces = [
            ("🖥️ AI Assistant GUI", "gui", "Launch the main voice-controlled AI interface"),
            ("🏨 Hotel Management", "hotel", "Manage hotel operations and bookings"),
            ("🧠 AI Training Lab", "training", "Train and customize AI models"),
            ("💻 Command Interface", "cli", "Access terminal-based interface"),
            ("📧 Email Integration", "email", "Setup email classification system"),
            ("⚙️ Settings", "settings", "Configure system preferences")
        ]
        
        # Create buttons in grid
        for i, (title, interface_type, description) in enumerate(interfaces):
            button = self.create_interface_button(title, interface_type, description)
            row = i // 2
            col = i % 2
            grid.addWidget(button, row, col)
        
        layout.addWidget(buttons_frame)
        
    def create_interface_button(self, title, interface_type, description):
        """Create a single interface button"""
        button_frame = ClickableFrame(interface_type)
        button_frame.clicked.connect(self.launch_interface)  # type: ignore
        
        layout = QVBoxLayout(button_frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setFont(QFont("Arial", 9))
        desc_label.setStyleSheet("color: #cccccc;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return button_frame
        
    def create_footer(self, layout):
        """Create footer section"""
        footer = QFrame()
        footer_layout = QHBoxLayout(footer)
        
        # Version
        version_label = QLabel("Version 2.0 Professional")
        version_label.setStyleSheet("color: #666; font-size: 10px;")
        footer_layout.addWidget(version_label)
        
        footer_layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton("❌ Exit")
        exit_btn.setFixedSize(70, 30)
        exit_btn.clicked.connect(lambda: self.close())  # type: ignore
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        footer_layout.addWidget(exit_btn)
        
        layout.addWidget(footer)
        
    def apply_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
        """)
        
    def launch_interface(self, interface_type):
        """Launch selected interface in separate process"""
        try:
            print(f"🚀 Launching {interface_type} interface...")
            
            if interface_type == 'settings':
                QMessageBox.information(
                    self, 
                    "Settings", 
                    "Settings interface coming soon!\n\n• Voice preferences\n• Model configurations\n• System settings"
                )
                return
            
            # Launch interface using runner script
            success = self._launch_interface_process(interface_type)
            
            if success:
                # Show success message but keep launcher open
                QMessageBox.information(
                    self,
                    "Interface Launched",
                    f"✅ {interface_type.title()} interface has been launched!\n\nThe launcher will remain open for additional selections."
                )
            else:
                QMessageBox.warning(self, "Error", f"Unknown interface: {interface_type}")
                
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Failed to launch {interface_type}:\n{str(e)}")
            print(f"❌ Error: {e}")
    
    def _launch_interface_process(self, interface_type):
        """Launch interface in separate process and return success status"""
        try:
            project_root = Path(__file__).parent.parent
            
            if interface_type == 'cli':
                # For CLI, use gaia.py with terminal flag - needs new console
                gaia_script = project_root / "gaia.py"
                subprocess.Popen([sys.executable, str(gaia_script), '--terminal'], 
                               cwd=str(project_root),
                               creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            else:
                # For GUI interfaces, run without new console
                runner_script = project_root / "run_interface.py"
                if os.name == 'nt':
                    # On Windows, run GUI interfaces without console window
                    subprocess.Popen([sys.executable, str(runner_script), interface_type], 
                                   cwd=str(project_root),
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    # On Unix-like systems
                    subprocess.Popen([sys.executable, str(runner_script), interface_type], 
                                   cwd=str(project_root))
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to launch process: {e}")
            return False


def main():
    """Main function to run the launcher"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Gaia AI Launcher")
    app.setApplicationVersion("2.0")
    
    # Create and show launcher
    launcher = GaiaLauncherWindow()
    launcher.show()
    
    # Run the event loop and return the exit code
    exit_code = app.exec_()
    
    # Ensure proper cleanup
    app.quit()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
