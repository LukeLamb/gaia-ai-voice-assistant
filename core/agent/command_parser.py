"""
Command Parser for Gaia Agent
Handles parsing and execution of voice commands
"""
import re
from datetime import datetime
from core.automation import app_control


class CommandParser:
    """Parses voice commands and executes appropriate actions"""
    
    def __init__(self):
        """Initialize command parser - no setup needed currently"""
        pass
        
    def parse_and_execute(self, command: str):
        """Parse command and execute appropriate action"""
        command = command.lower()
        
        # Time-related commands
        time_result = self._handle_time_commands(command)
        if time_result:
            return time_result
            
        # Email/Outlook commands
        email_result = self._handle_email_commands(command)
        if email_result:
            return email_result
            
        # Application control commands
        app_result = self._handle_app_commands(command)
        if app_result:
            return app_result
            
        # Return None if no specific command matched
        return None
        
    def _handle_time_commands(self, command: str):
        """Handle time and date related commands"""
        if "time" in command or "what time" in command or "current time" in command:
            return self.get_current_time()
        elif "date" in command or "what date" in command or "today" in command:
            return self.get_current_date()
        return None
        
    def _handle_email_commands(self, command: str):
        """Handle email and Outlook related commands"""
        email_keywords = ["email", "outlook", "mail", "show me emails", "check emails"]
        if not any(phrase in command for phrase in email_keywords):
            return None
            
        if "open" in command:
            # User wants to open Outlook application AND check emails
            app_result = app_control.open_app("outlook.exe")
            email_result = app_control.check_outlook_inbox()
            if isinstance(email_result, list) and email_result:
                return [app_result, "Here are your recent emails:"] + email_result
            else:
                return [app_result, "Outlook opened, but couldn't retrieve emails at this time."]
        else:
            # User just wants to check emails
            return app_control.check_outlook_inbox()
            
    def _handle_app_commands(self, command: str):
        """Handle general application commands"""
        if "excel" in command:
            return app_control.create_excel("ai_created.xlsx")
        elif "word" in command or "document" in command:
            return app_control.create_word_doc("ai_created.docx")
        elif "open" in command:
            app_match = re.search(r"open (.+)", command)
            app_name = app_match.group(1) if app_match else "notepad.exe"
            return app_control.open_app(app_name)
        return None
        
    def get_current_time(self):
        """Get current time in a friendly format."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        return f"The current time is {time_str}"

    def get_current_date(self):
        """Get current date in a friendly format."""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        return f"Today is {date_str}"
