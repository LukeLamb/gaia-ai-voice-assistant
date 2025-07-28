"""
Professional PyQt5 Main Window for Gaia AI Assistant
"""
import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QTextEdit, QPushButton,
                             QLabel, QFrame, QSplitter, QSystemTrayIcon, QMenu)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QPixmap, QCloseEvent
from gui.widgets.chat_widget import ChatWidget
from gui.widgets.control_panel import ControlPanel
from gui.widgets.status_bar import StatusBar
from core.agent.gaia_agent import GaiaAgent


class GaiaMainWindow(QMainWindow):
    """Professional main window for Gaia AI Assistant"""
    
    def __init__(self):
        super().__init__()
        self.gaia_agent = None
        self.init_ui()
        self.setup_system_tray()
        self.connect_signals()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Gaia - AI Voice Assistant")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Set application icon (placeholder for now)
        # self.setWindowIcon(QIcon('resources/icons/gaia_icon.png'))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content area with splitter
        splitter = QSplitter()
        
        # Left panel - Controls and status
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Chat and logs
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)
        
        # Create status bar
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        
        # Apply dark theme
        self.apply_dark_theme()
        
    def create_header(self):
        """Create the header section"""
        header = QFrame()
        header.setFrameStyle(QFrame.StyledPanel)
        header.setMaximumHeight(80)
        
        layout = QHBoxLayout(header)
        
        # Logo/Icon placeholder
        logo_label = QLabel("🤖")
        logo_label.setStyleSheet("font-size: 32px;")
        layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel("Gaia AI Voice Assistant")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #2196F3; margin-left: 10px;")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Version label
        version_label = QLabel("v2.0")
        version_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(version_label)
        
        return header
        
    def create_left_panel(self):
        """Create the left control panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setMaximumWidth(320)
        
        layout = QVBoxLayout(panel)
        
        # Control panel
        self.control_panel = ControlPanel()
        layout.addWidget(self.control_panel)
        
        # Status section
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.StyledPanel)
        status_layout = QVBoxLayout(status_frame)
        
        status_title = QLabel("Status")
        status_title.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(status_title)
        
        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet("color: #FFA726; font-size: 14px; padding: 5px;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_frame)
        
        # User info section
        user_frame = QFrame()
        user_frame.setFrameStyle(QFrame.StyledPanel)
        user_layout = QVBoxLayout(user_frame)
        
        user_title = QLabel("User")
        user_title.setFont(QFont("Arial", 12, QFont.Bold))
        user_layout.addWidget(user_title)
        
        self.user_label = QLabel("Not identified")
        self.user_label.setStyleSheet("color: #66BB6A; font-size: 14px; padding: 5px;")
        user_layout.addWidget(self.user_label)
        
        layout.addWidget(user_frame)
        
        layout.addStretch()
        
        return panel
        
    def create_right_panel(self):
        """Create the right content panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(panel)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Chat tab
        self.chat_widget = ChatWidget()
        tab_widget.addTab(self.chat_widget, "💬 Conversation")
        
        # Logs tab
        self.log_widget = QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.setFont(QFont("Consolas", 10))
        tab_widget.addTab(self.log_widget, "📋 System Logs")
        
        layout.addWidget(tab_widget)
        
        return panel
        
    def setup_system_tray(self):
        """Setup system tray icon"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            # Use a simple built-in icon to avoid the "No Icon set" warning
            try:
                from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
                
                # Create a simple icon programmatically
                pixmap = QPixmap(16, 16)
                pixmap.fill(QColor(0, 0, 0, 0))  # Transparent
                painter = QPainter(pixmap)
                painter.fillRect(4, 4, 8, 8, QColor(0, 0, 255))  # Blue
                painter.end()
                
                self.tray_icon.setIcon(QIcon(pixmap))
                self.tray_icon.setToolTip("Gaia AI Assistant")
            except Exception:
                # If icon creation fails, skip the system tray
                return
            
            # Create tray menu
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Show Gaia")
            hide_action = tray_menu.addAction("Hide Gaia")
            tray_menu.addSeparator()
            quit_action = tray_menu.addAction("Quit")
            
            # Connect signals safely
            if show_action:
                show_action.triggered.connect(self.show_window)
            if hide_action:
                hide_action.triggered.connect(self.hide_window)
            if quit_action:
                quit_action.triggered.connect(self.quit_application)
            
            self.tray_icon.setContextMenu(tray_menu)
            
            # Only show tray icon if we have an icon set
            try:
                self.tray_icon.show()
            except Exception:
                # If tray icon fails, continue without it
                pass
            
    def apply_dark_theme(self):
        """Apply dark theme styling"""
        dark_style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QFrame {
            background-color: #3c3c3c;
            border: 1px solid #555;
            border-radius: 5px;
        }
        
        QTabWidget::pane {
            border: 1px solid #555;
            background-color: #3c3c3c;
        }
        
        QTabBar::tab {
            background-color: #4a4a4a;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        
        QTabBar::tab:selected {
            background-color: #2196F3;
        }
        
        QTextEdit {
            background-color: #2b2b2b;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 3px;
            padding: 5px;
        }
        
        QLabel {
            color: #ffffff;
        }
        
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        
        QPushButton:hover {
            background-color: #45a049;
        }
        
        QPushButton:pressed {
            background-color: #3d8b40;
        }
        
        QPushButton:disabled {
            background-color: #666;
            color: #999;
        }
        
        QStatusBar {
            background-color: #3c3c3c;
            color: #ffffff;
            border-top: 1px solid #555;
        }
        """
        
        self.setStyleSheet(dark_style)
        
    def log_message(self, message):
        """Add message to log widget with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # Add to log widget
        self.log_widget.append(formatted_message)
        
        # Auto-scroll to bottom
        scrollbar = self.log_widget.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
        
        # Also print to console for debugging
        print(formatted_message)
        
    def update_status(self, status):
        """Update status display"""
        self.status_label.setText(status)
        self.status_bar.update_status(status)
        
    def update_user(self, user_name):
        """Update user display"""
        self.user_label.setText(user_name if user_name else "Not identified")
        
    def connect_signals(self):
        """Connect control panel signals to agent methods"""
        self.control_panel.start_clicked.connect(self.start_gaia)
        self.control_panel.pause_clicked.connect(self.pause_gaia)
        self.control_panel.stop_clicked.connect(self.stop_gaia)
    
    def start_gaia(self):
        """Start the Gaia AI agent"""
        try:
            if self.gaia_agent is None:
                # Initialize the agent with GUI log callback
                self.gaia_agent = GaiaAgent(log_callback=self.log_message)
                self.log_message("🤖 Gaia AI Agent initialized")
            
            # Start the agent
            self.gaia_agent.start()
            self.log_message("✅ Gaia AI started successfully")
            self.status_label.setText("Running")
            self.status_label.setStyleSheet("color: #4CAF50; font-size: 14px; padding: 5px;")
            
        except Exception as e:
            error_msg = f"❌ Failed to start Gaia: {str(e)}"
            self.log_message(error_msg)
            self.status_label.setText("Error")
            self.status_label.setStyleSheet("color: #F44336; font-size: 14px; padding: 5px;")
    
    def pause_gaia(self):
        """Pause/resume the Gaia AI agent"""
        try:
            if self.gaia_agent and self.gaia_agent.running:
                if self.gaia_agent.paused:
                    self.gaia_agent.resume()
                    self.log_message("▶️ Gaia AI resumed")
                    self.status_label.setText("Running")
                    self.status_label.setStyleSheet("color: #4CAF50; font-size: 14px; padding: 5px;")
                else:
                    self.gaia_agent.pause()
                    self.log_message("⏸️ Gaia AI paused")
                    self.status_label.setText("Paused")
                    self.status_label.setStyleSheet("color: #FF9800; font-size: 14px; padding: 5px;")
            else:
                self.log_message("⚠️ Gaia is not running")
                
        except Exception as e:
            error_msg = f"❌ Failed to pause/resume Gaia: {str(e)}"
            self.log_message(error_msg)
    
    def stop_gaia(self):
        """Stop the Gaia AI agent"""
        try:
            if self.gaia_agent:
                self.gaia_agent.stop()
                self.log_message("⏹️ Gaia AI stopped")
                self.status_label.setText("Stopped")
                self.status_label.setStyleSheet("color: #F44336; font-size: 14px; padding: 5px;")
            else:
                self.log_message("⚠️ Gaia is not running")
                
        except Exception as e:
            error_msg = f"❌ Failed to stop Gaia: {str(e)}"
            self.log_message(error_msg)

    def show_window(self):
        """Show the main window"""
        self.show()
        
    def hide_window(self):
        """Hide the main window"""
        self.hide()
        
    def quit_application(self):
        """Quit the application"""
        self.close()
        
    def closeEvent(self, a0: QCloseEvent | None):
        """Handle close event"""
        if a0 is None:
            return
        
        # If system tray is available, minimize to tray instead of closing
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            a0.ignore()
        else:
            # Proper cleanup when actually closing
            if hasattr(self, 'gaia_agent') and self.gaia_agent:
                self.gaia_agent.stop()
            a0.accept()
            # Force exit the application
            app = QApplication.instance()
            if app:
                app.quit()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Gaia AI Assistant")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Gaia AI")
    
    # Create and show main window
    window = GaiaMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
