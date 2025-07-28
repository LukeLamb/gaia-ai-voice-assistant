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
        # Handle questions about available programs
        if self._is_program_list_query(command):
            return self._list_available_programs()
        elif "excel" in command:
            return app_control.create_excel("ai_created.xlsx")
        elif "word" in command or "document" in command:
            return app_control.create_word_doc("ai_created.docx")
        elif "open" in command:
            return self._handle_open_command(command)
        return None
    
    def _is_program_list_query(self, command: str):
        """Check if command is asking for list of available programs"""
        program_queries = [
            ("what programs" in command and "open" in command),
            ("which programs" in command and "open" in command),
            ("list programs" in command),
            ("available programs" in command)
        ]
        return any(program_queries)
    
    def _handle_open_command(self, command: str):
        """Handle 'open' commands with robust parsing"""
        # More robust parsing - avoid questions about opening
        if self._is_question_about_opening(command):
            return None  # Let LLM handle questions about opening
            
        app_match = re.search(r"open (.+)", command)
        if app_match:
            app_name = app_match.group(1).strip()
            # Filter out common question words that aren't program names
            if self._contains_question_words(app_name):
                return None
            return app_control.open_app(app_name)
        return app_control.open_app("notepad.exe")
    
    def _is_question_about_opening(self, command: str):
        """Check if command is a question about opening rather than a command to open"""
        question_indicators = ["can you", "which", "what", "?"]
        return any(indicator in command for indicator in question_indicators)
    
    def _contains_question_words(self, app_name: str):
        """Check if app name contains question words that indicate it's not a real app name"""
        question_words = ["can", "you", "which", "what", "how", "verbally", "?"]
        return any(word in app_name.lower() for word in question_words)
        
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

    def _list_available_programs(self):
        """List programs that can be opened verbally"""
        programs = [
            "You can open these programs by saying 'open' followed by:",
            "• Excel - Creates a new Excel spreadsheet",
            "• Word or Document - Creates a new Word document", 
            "• Outlook - Opens Outlook and shows recent emails",
            "• Any program name like 'notepad', 'calculator', 'chrome', etc.",
            "",
            "You can also ask me to:",
            "• Check emails or show emails",
            "• Get the current time or date",
            "• Have general conversations about any topic"
        ]
        return programs
