"""
CLI Interface - Command Line Interface
Simple command-line interface for Gaia AI Assistant
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from core.agent.gaia_agent import GaiaAgent


class CLIInterface:
    """
    Command line interface for Gaia AI Assistant
    """
    
    def __init__(self):
        self.agent = None
    
    def show_help(self):
        """Show available commands"""
        help_text = """
🤖 GAIA AI COMMAND LINE INTERFACE

Available Commands:
  ask <question>     - Ask Gaia a question
  hotel <command>    - Hotel management commands
  email              - Check and process emails
  train              - Training options
  config             - Configuration management
  help               - Show this help
  quit/exit          - Exit the CLI

Examples:
  ask What is the weather like?
  hotel status
  hotel check-in 101 "John Doe" "2023-12-31"
  email summary
        """
        print(help_text)
    
    def initialize_agent(self) -> bool:
        """Initialize Gaia agent"""
        try:
            print("🤖 Initializing Gaia AI Agent...")
            self.agent = GaiaAgent(log_callback=print)
            print("✅ Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize agent: {e}")
            return False
    
    def handle_ask_command(self, question: str):
        """Handle ask command"""
        if not self.agent:
            print("❌ Agent not initialized")
            return
        
        print(f"🤔 Question: {question}")
        try:
            response = self.agent.llm.ask(question)
            print(f"🤖 Gaia: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def handle_hotel_command(self, command_parts: list):
        """Handle hotel commands"""
        try:
            from core.hotel.hotel_manager import HotelManager
            hotel = HotelManager()
            
            if not command_parts:
                command_parts = ['status']
            
            cmd = command_parts[0].lower()
            
            if cmd == 'status':
                summary = hotel.get_hotel_summary()
                print(f"\n🏨 {summary['hotel_name']} Status:")
                print(f"📊 Occupancy: {summary['occupied_rooms']}/{summary['total_rooms']} ({summary['occupancy_rate']}%)")
                print(f"💰 Daily Revenue: ${summary['daily_revenue']}")
                print(f"🛏️ Available Rooms: {summary['available_room_list']}")
                
            elif cmd == 'rooms':
                available = hotel.get_available_rooms()
                print(f"\n🛏️ Available Rooms ({len(available)}):")
                for room in available:
                    print(f"  Room {room.room_number} - {room.room_type} (${room.rate_per_night}/night)")
                    
            else:
                print(f"❌ Unknown hotel command: {cmd}")
                print("Available: status, rooms")
                
        except ImportError:
            print("❌ Hotel system not available")
        except Exception as e:
            print(f"❌ Hotel error: {e}")
    
    def handle_email_command(self):
        """Handle email commands"""
        try:
            from core.hotel.email_classifier import HotelEmailClassifier
            classifier = HotelEmailClassifier()
            
            # Demo email processing
            sample_emails = [
                {"subject": "Booking Confirmation", "content": "Your reservation is confirmed", "sender": "guest@example.com"},
                {"subject": "Invoice Due", "content": "Payment required", "sender": "supplier@example.com"}
            ]
            
            print("\n📧 Processing sample emails...")
            for email in sample_emails:
                classification = classifier.classify_email(
                    email['subject'], email['content'], email['sender']
                )
                print(f"  📧 {email['subject']} → {classification.category.value} ({classification.priority.value})")
                
        except ImportError:
            print("❌ Email system not available")
        except Exception as e:
            print(f"❌ Email error: {e}")
    
    def process_command(self, command: str):
        """Process user command"""
        if not command.strip():
            return
        
        parts = command.strip().split()
        cmd = parts[0].lower()
        
        if cmd in ['quit', 'exit']:
            return False
        elif cmd == 'help':
            self.show_help()
        elif cmd == 'ask' and len(parts) > 1:
            question = ' '.join(parts[1:])
            self.handle_ask_command(question)
        elif cmd == 'hotel':
            self.handle_hotel_command(parts[1:])
        elif cmd == 'email':
            self.handle_email_command()
        elif cmd == 'train':
            print("🧠 For training, use: python gaia.py and select option 4")
        elif cmd == 'config':
            from src.core.config_manager import ConfigManager
            config = ConfigManager()
            print(f"📋 Current config file: {config.config_file}")
        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type 'help' for available commands")
        
        return True
    
    def run(self):
        """Run the CLI interface"""
        print("💻 Starting Gaia AI CLI Interface...")
        print("Type 'help' for commands, 'quit' to exit")
        
        if not self.initialize_agent():
            print("❌ Failed to start CLI")
            return 1
        
        try:
            while True:
                try:
                    command = input("\n🤖 gaia> ").strip()
                    if not self.process_command(command):
                        break
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except EOFError:
                    break
                    
        except Exception as e:
            print(f"❌ CLI Error: {e}")
            return 1
        
        print("👋 CLI closed")
        return 0
