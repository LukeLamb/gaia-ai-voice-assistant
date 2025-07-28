"""
Gaia AI Assistant - Professional Launcher GUI
Main entry point interface for selecting different modes
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGridLayout, QLabel, QPushButton,
                             QFrame, QSystemTrayIcon, QMenu, QMessageBox, QDesktopWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QCursor


class InterfaceCard(QFrame):
    """Professional interface selection card"""
    clicked = pyqtSignal(str)
    
    def __init__(self, interface_type, title, description, icon, parent=None):
        super().__init__(parent)
        self.interface_type = interface_type
        self.setup_ui(title, description, icon)
        self.setup_animations()
        
    def setup_ui(self, title, description, icon):
        """Setup the card UI"""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFixedSize(280, 200)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; color: #2196F3;")
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; margin: 5px;")
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(description)
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setFont(QFont("Arial", 10))
        desc_label.setStyleSheet("color: #cccccc; margin: 5px;")
        layout.addWidget(desc_label)
        
        # Default card styling
        self.setStyleSheet("""
            InterfaceCard {
                background-color: #3c3c3c;
                border: 2px solid #555;
                border-radius: 15px;
                margin: 5px;
            }
            InterfaceCard:hover {
                background-color: #4a4a4a;
                border: 2px solid #2196F3;
                transform: scale(1.05);
            }
        """)
        
    def setup_animations(self):
        """Setup hover animations"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    def mousePressEvent(self, event):
        """Handle card click"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.interface_type)
        super().mousePressEvent(event)
        
    def enterEvent(self, event):
        """Handle mouse enter (hover effect)"""
        self.setStyleSheet("""
            InterfaceCard {
                background-color: #4a4a4a;
                border: 2px solid #2196F3;
                border-radius: 15px;
                margin: 5px;
            }
        """)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Handle mouse leave"""
        self.setStyleSheet("""
            InterfaceCard {
                background-color: #3c3c3c;
                border: 2px solid #555;
                border-radius: 15px;
                margin: 5px;
            }
        """)
        super().leaveEvent(event)


class GaiaLauncherWindow(QMainWindow):
    """Professional Gaia AI Launcher Window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_system_tray()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Gaia AI Assistant - Launcher")
        self.setFixedSize(900, 650)
        
        # Center window on screen
        self.center_window()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Interface cards grid
        cards_grid = self.create_interface_cards()
        main_layout.addWidget(cards_grid)
        
        # Footer
        footer = self.create_footer()
        main_layout.addWidget(footer)
        
        # Apply dark theme
        self.apply_dark_theme()
        
    def center_window(self):
        """Center the window on screen"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().availableGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
    def create_header(self):
        """Create the header section"""
        header = QFrame()
        header.setMaximumHeight(100)
        
        layout = QVBoxLayout(header)
        layout.setAlignment(Qt.AlignCenter)
        
        # Main title
        title = QLabel("🤖 GAIA AI ASSISTANT")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2196F3; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Professional Modular AI System - Select Your Interface")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setStyleSheet("color: #cccccc;")
        layout.addWidget(subtitle)
        
        return header
        
    def create_interface_cards(self):
        """Create the interface selection cards"""
        cards_widget = QWidget()
        grid = QGridLayout(cards_widget)
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)
        
        # Define interface options
        interfaces = [
            {
                'type': 'gui',
                'title': 'AI Assistant GUI',
                'description': 'Professional voice-controlled AI interface with real-time interaction',
                'icon': '🖥️'
            },
            {
                'type': 'hotel',
                'title': 'Hotel Management',
                'description': 'Complete hotel operations system with booking and email management',
                'icon': '🏨'
            },
            {
                'type': 'training',
                'title': 'AI Training Lab',
                'description': 'Train and fine-tune language models with custom datasets',
                'icon': '🧠'
            },
            {
                'type': 'cli',
                'title': 'Command Interface',
                'description': 'Terminal-based interface for advanced users and automation',
                'icon': '💻'
            },
            {
                'type': 'email',
                'title': 'Email Integration',
                'description': 'Setup and configure intelligent email classification systems',
                'icon': '📧'
            },
            {
                'type': 'settings',
                'title': 'System Settings',
                'description': 'Configure Gaia AI preferences and system parameters',
                'icon': '⚙️'
            }
        ]
        
        # Create cards in grid layout
        for i, interface in enumerate(interfaces):
            card = InterfaceCard(
                interface['type'],
                interface['title'],
                interface['description'],
                interface['icon']
            )
            card.clicked.connect(self.launch_interface)
            
            row = i // 3
            col = i % 3
            grid.addWidget(card, row, col)
        
        return cards_widget
        
    def create_footer(self):
        """Create the footer section"""
        footer = QFrame()
        footer.setMaximumHeight(60)
        
        layout = QHBoxLayout(footer)
        
        # Version info
        version_label = QLabel("Version 2.0 | Professional Edition")
        version_label.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(version_label)
        
        layout.addStretch()
        
        # Exit button
        exit_btn = QPushButton("❌ Exit")
        exit_btn.setFixedSize(80, 30)
        exit_btn.clicked.connect(self.close)
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
        layout.addWidget(exit_btn)
        
        return footer
        
    def setup_system_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Create tray menu
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Show Launcher")
            hide_action = tray_menu.addAction("Hide Launcher")
            tray_menu.addSeparator()
            quit_action = tray_menu.addAction("Quit Gaia")
            
            show_action.triggered.connect(self.show)
            hide_action.triggered.connect(self.hide)
            quit_action.triggered.connect(self.close)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            
    def apply_dark_theme(self):
        """Apply professional dark theme"""
        dark_style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QFrame {
            background-color: transparent;
        }
        
        QLabel {
            color: #ffffff;
        }
        
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 5px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        """
        
        self.setStyleSheet(dark_style)
        
    def launch_interface(self, interface_type):
        """Launch the selected interface"""
        try:
            print(f"🚀 Launching {interface_type} interface...")
            
            if interface_type == 'gui':
                self.launch_gui_interface()
            elif interface_type == 'hotel':
                self.launch_hotel_interface()
            elif interface_type == 'training':
                self.launch_training_interface()
            elif interface_type == 'cli':
                self.launch_cli_interface()
            elif interface_type == 'email':
                self.launch_email_interface()
            elif interface_type == 'settings':
                self.launch_settings_interface()
            else:
                QMessageBox.warning(self, "Error", f"Interface '{interface_type}' not implemented yet.")
                
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", f"Failed to launch {interface_type}:\n{str(e)}")
            
    def launch_gui_interface(self):
        """Launch the main AI GUI interface"""
        from src.interfaces.gui_interface import GUIInterface
        self.hide()  # Hide launcher
        gui = GUIInterface()
        gui.run()
        
    def launch_hotel_interface(self):
        """Launch hotel management interface"""
        from src.interfaces.hotel_interface import HotelInterface
        self.hide()
        hotel = HotelInterface()
        hotel.run()
        
    def launch_training_interface(self):
        """Launch AI training interface"""
        from src.training.llm_trainer import LLMTrainer
        self.hide()
        trainer = LLMTrainer()
        trainer.run()
        
    def launch_cli_interface(self):
        """Launch CLI interface"""
        from src.interfaces.cli_interface import CLIInterface
        self.hide()
        cli = CLIInterface()
        cli.run()
        
    def launch_email_interface(self):
        """Launch email integration interface"""
        from src.interfaces.email_interface import EmailInterface
        self.hide()
        email = EmailInterface()
        email.run()
        
    def launch_settings_interface(self):
        """Launch settings interface (placeholder)"""
        QMessageBox.information(
            self, 
            "Settings", 
            "Settings interface coming soon!\n\nWill include:\n• Voice preferences\n• Model configurations\n• System settings\n• Theme options"
        )
        
    def closeEvent(self, event):
        """Handle close event"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
            # Force exit the application
            app = QApplication.instance()
            if app:
                app.quit()


def main():
    """Main function to run the launcher"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Gaia AI Launcher")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Gaia AI")
    
    # Create and show launcher window
    launcher = GaiaLauncherWindow()
    launcher.show()
    
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
