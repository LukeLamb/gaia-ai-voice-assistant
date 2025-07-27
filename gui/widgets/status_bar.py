"""
Status Bar Widget for Gaia AI Assistant
"""
from PyQt5.QtWidgets import QStatusBar, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class StatusBar(QStatusBar):
    """Professional status bar for Gaia"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the status bar"""
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.addWidget(self.status_label)
        
        # Add stretch
        self.addPermanentWidget(QLabel(""), 1)
        
        # Connection status
        self.connection_label = QLabel("🔗 Connected")
        self.connection_label.setFont(QFont("Arial", 10))
        self.addPermanentWidget(self.connection_label)
        
    def update_status(self, status):
        """Update the status message"""
        self.status_label.setText(status)
        
    def update_connection(self, connected):
        """Update connection status"""
        if connected:
            self.connection_label.setText("🔗 Connected")
            self.connection_label.setStyleSheet("color: #4CAF50;")
        else:
            self.connection_label.setText("🔗 Disconnected")
            self.connection_label.setStyleSheet("color: #F44336;")
