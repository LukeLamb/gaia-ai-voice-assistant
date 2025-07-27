"""
Control Panel Widget for Gaia AI Assistant
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class ControlPanel(QWidget):
    """Control panel for starting, pausing, and stopping Gaia"""
    
    # Button text constants
    START_TEXT = "▶️ Start Gaia"
    PAUSE_TEXT = "⏸️ Pause Gaia"
    RESUME_TEXT = "▶️ Resume Gaia"
    STOP_TEXT = "⏹️ Stop Gaia"
    
    # Signals
    start_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.is_paused = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the control panel UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Control Panel")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Control buttons
        self.start_button = QPushButton(self.START_TEXT)
        self.start_button.clicked.connect(self.on_start_clicked)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.start_button)
        
        self.pause_button = QPushButton(self.PAUSE_TEXT)
        self.pause_button.clicked.connect(self.on_pause_clicked)
        self.pause_button.setEnabled(False)
        self.pause_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        layout.addWidget(self.pause_button)
        
        self.stop_button = QPushButton(self.STOP_TEXT)
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:disabled {
                background-color: #666;
                color: #999;
            }
        """)
        layout.addWidget(self.stop_button)
        
    def on_start_clicked(self):
        """Handle start button click"""
        self.is_running = True
        self.is_paused = False
        self.update_button_states()
        self.start_clicked.emit()
        
    def on_pause_clicked(self):
        """Handle pause/resume button click"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_button.setText(self.RESUME_TEXT)
        else:
            self.pause_button.setText(self.PAUSE_TEXT)
        self.pause_clicked.emit()
        
    def on_stop_clicked(self):
        """Handle stop button click"""
        self.is_running = False
        self.is_paused = False
        self.update_button_states()
        self.stop_clicked.emit()
        
    def update_button_states(self):
        """Update button enabled/disabled states"""
        self.start_button.setEnabled(not self.is_running)
        self.pause_button.setEnabled(self.is_running)
        self.stop_button.setEnabled(self.is_running)
        
        if not self.is_running:
            self.pause_button.setText(self.PAUSE_TEXT)
