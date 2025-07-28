"""
Gaia AI Voice Assistant - Professional GUI Entry Point
Clean, organized, professional launcher interface
"""

import sys
import os
from pathlib import Path

# Ensure the project root is in the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main function - Launch GUI launcher by default"""
    try:
        # Import and launch the simple GUI launcher
        from gui.simple_launcher import main as launcher_main
        return launcher_main()
        
    except ImportError as e:
        print(f"❌ GUI launcher not available: {e}")
        print("🔄 Falling back to terminal interface...")
        
        # Fallback to terminal interface
        return run_terminal_menu()
        
    except Exception as e:
        print(f"❌ Failed to start Gaia: {e}")
        print("🔄 Trying terminal interface...")
        return run_terminal_menu()


def run_terminal_menu():
    """Terminal-based interface selection (fallback)"""
    _display_banner()
    interfaces = _get_interface_mappings()
    
    while True:
        try:
            choice = _get_user_choice()
            
            if choice == '6':
                print("👋 Goodbye!")
                break
            
            if not _is_valid_choice(choice):
                continue
                
            interface_type = _get_interface_type(choice)
            _launch_interface(interface_type, interfaces)
            
            if not _should_continue():
                print("👋 Thank you for using Gaia AI!")
                break
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Restarting menu...")
    
    return 0


def _display_banner():
    """Display the main terminal banner"""
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


def _get_interface_mappings():
    """Get the mapping of interface types to classes"""
    from src.interfaces.cli_interface import CLIInterface
    from src.interfaces.gui_interface import GUIInterface  
    from src.interfaces.hotel_interface import HotelInterface
    
    return {
        'cli': CLIInterface,
        'gui': GUIInterface,
        'hotel': HotelInterface
    }


def _get_user_choice():
    """Display menu and get user choice"""
    print("Select interface:")
    print("1. 🖥️  GUI (Recommended) - Professional interface")
    print("2. 💻 CLI - Command line interface")
    print("3. 🏨 Hotel - Hotel management system")
    print("4. 🧠 Training - Train/fine-tune LLM")
    print("5. 📧 Email - Setup email integration")
    print("6. ❌ Exit")
    
    return input("\nEnter choice (1-6): ").strip()


def _is_valid_choice(choice):
    """Validate user choice"""
    valid_choices = {'1', '2', '3', '4', '5', '6'}
    if choice not in valid_choices:
        print("❌ Invalid choice. Please enter 1-6.")
        return False
    return True


def _get_interface_type(choice):
    """Map choice number to interface type"""
    choices = {
        '1': 'gui',
        '2': 'cli', 
        '3': 'hotel',
        '4': 'training',
        '5': 'email'
    }
    return choices[choice]


def _launch_interface(interface_type, interfaces):
    """Launch the selected interface"""
    if interface_type == 'training':
        from src.training.llm_trainer import LLMTrainer
        trainer = LLMTrainer()
        trainer.run()
    elif interface_type == 'email':
        from src.interfaces.email_interface import EmailInterface
        email_interface = EmailInterface()
        email_interface.run()
    elif interface_type in interfaces:
        interface_class = interfaces[interface_type]
        interface = interface_class()
        interface.run()
    else:
        print(f"❌ Unknown interface: {interface_type}")


def _should_continue():
    """Ask user if they want to try another interface"""
    continue_choice = input("\nTry another interface? (y/n): ").strip().lower()
    return continue_choice in ['y', 'yes']


if __name__ == "__main__":
    sys.exit(main())
