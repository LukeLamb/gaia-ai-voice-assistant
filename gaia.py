"""
Gaia AI Voice Assistant - Modular Program Entry Point
Clean, organized, professional modular architecture
"""

import sys
import os
from pathlib import Path

# Ensure the project root is in the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.interfaces.cli_interface import CLIInterface
from src.interfaces.gui_interface import GUIInterface  
from src.interfaces.hotel_interface import HotelInterface
from src.core.config_manager import ConfigManager


class GaiaApplication:
    """
    Main application entry point for all Gaia AI interfaces
    """
    
    def __init__(self):
        self.config = ConfigManager()
        self.interfaces = {
            'cli': CLIInterface,
            'gui': GUIInterface,
            'hotel': HotelInterface
        }
    
    def show_banner(self):
        """Display application banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🤖 GAIA AI ASSISTANT                      ║
║                   Professional Modular System                ║
╠══════════════════════════════════════════════════════════════╣
║  Available Interfaces:                                       ║
║  🖥️  GUI        - Professional PyQt5 interface              ║
║  💻 CLI        - Command line interface                     ║  
║  🏨 Hotel      - Hotel management system                    ║
║  🧠 Training   - LLM training and fine-tuning              ║
║  📧 Email      - Email integration setup                    ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def get_user_choice(self) -> str:
        """Get user's interface choice"""
        choices = {
            '1': 'gui',
            '2': 'cli', 
            '3': 'hotel',
            '4': 'training',
            '5': 'email'
        }
        
        print("Select interface:")
        print("1. 🖥️  GUI (Recommended) - Professional interface")
        print("2. 💻 CLI - Command line interface")
        print("3. 🏨 Hotel - Hotel management system")
        print("4. 🧠 Training - Train/fine-tune LLM")
        print("5. 📧 Email - Setup email integration")
        print("6. ❌ Exit")
        
        while True:
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == '6':
                print("👋 Goodbye!")
                sys.exit(0)
            
            if choice in choices:
                return choices[choice]
            
            print("❌ Invalid choice. Please enter 1-6.")
    
    def launch_interface(self, interface_type: str):
        """Launch the selected interface"""
        try:
            if interface_type == 'training':
                from src.training.llm_trainer import LLMTrainer
                trainer = LLMTrainer()
                trainer.run()
                
            elif interface_type == 'email':
                from src.interfaces.email_interface import EmailInterface
                email_interface = EmailInterface()
                email_interface.run()
                
            elif interface_type in self.interfaces:
                interface_class = self.interfaces[interface_type]
                interface = interface_class()
                interface.run()
                
            else:
                print(f"❌ Unknown interface: {interface_type}")
                
        except KeyboardInterrupt:
            print("\n👋 Interface closed by user")
        except Exception as e:
            print(f"❌ Error launching {interface_type}: {e}")
            print("Please check your installation and try again.")
    
    def run(self):
        """Main application loop"""
        self.show_banner()
        
        while True:
            try:
                interface_type = self.get_user_choice()
                self.launch_interface(interface_type)
                
                # Ask if user wants to try another interface
                continue_choice = input("\nTry another interface? (y/n): ").strip().lower()
                if continue_choice not in ['y', 'yes']:
                    print("👋 Thank you for using Gaia AI!")
                    break
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                print("Restarting menu...")


def main():
    """Entry point function"""
    try:
        app = GaiaApplication()
        app.run()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
