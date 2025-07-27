"""
Professional Chat Widget for Gaia AI Assistant
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QTextCharFormat, QColor


class ChatWidget(QWidget):
    """Professional chat widget for displaying conversations"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the chat widget UI"""
        layout = QVBoxLayout(self)
        
        # Create chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Segoe UI", 11))
        
        # Set chat styling
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
                padding: 10px;
                line-height: 1.4;
            }
        """)
        
        layout.addWidget(self.chat_display)
        
    def add_user_message(self, message):
        """Add a user message to the chat"""
        html = f"""
        <div style="margin: 10px 0; padding: 10px; background-color: #2196F3; 
                    border-radius: 10px; margin-left: 50px;">
            <strong style="color: #ffffff;">👤 Luke:</strong><br>
            <span style="color: #ffffff;">{message}</span>
        </div>
        """
        self.chat_display.append(html)
        self.scroll_to_bottom()
        
    def add_gaia_message(self, message):
        """Add a Gaia message to the chat"""
        html = f"""
        <div style="margin: 10px 0; padding: 10px; background-color: #4CAF50; 
                    border-radius: 10px; margin-right: 50px;">
            <strong style="color: #ffffff;">🤖 Gaia:</strong><br>
            <span style="color: #ffffff;">{message}</span>
        </div>
        """
        self.chat_display.append(html)
        self.scroll_to_bottom()
        
    def add_system_message(self, message):
        """Add a system message to the chat"""
        html = f"""
        <div style="margin: 10px 0; padding: 8px; background-color: #666; 
                    border-radius: 5px; text-align: center;">
            <em style="color: #ccc; font-size: 10px;">⚙️ System: {message}</em>
        </div>
        """
        self.chat_display.append(html)
        self.scroll_to_bottom()
        
    def scroll_to_bottom(self):
        """Scroll to the bottom of the chat"""
        scrollbar = self.chat_display.verticalScrollBar()
        if scrollbar:
            scrollbar.setValue(scrollbar.maximum())
        
    def clear_chat(self):
        """Clear the chat display"""
        self.chat_display.clear()
