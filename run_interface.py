#!/usr/bin/env python3
"""
Interface Runner - Launch specific interfaces
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Main function to run specified interface"""
    if len(sys.argv) < 2:
        print("Usage: python run_interface.py <interface_type>")
        print("Available interfaces: gui, hotel, training, cli, email")
        return 1
    
    interface_type = sys.argv[1].lower()
    
    try:
        if interface_type == 'gui':
            from src.interfaces.gui_interface import GUIInterface
            gui = GUIInterface()
            return gui.run()
            
        elif interface_type == 'hotel':
            from src.interfaces.hotel_interface import HotelInterface
            hotel = HotelInterface()
            return hotel.run()
            
        elif interface_type == 'training':
            from src.training.llm_trainer import LLMTrainer
            trainer = LLMTrainer()
            return trainer.run()
            
        elif interface_type == 'cli':
            from src.interfaces.cli_interface import CLIInterface
            cli = CLIInterface()
            return cli.run()
            
        elif interface_type == 'email':
            from src.interfaces.email_interface import EmailInterface
            email = EmailInterface()
            return email.run()
            
        else:
            print(f"❌ Unknown interface: {interface_type}")
            print("Available interfaces: gui, hotel, training, cli, email")
            return 1
            
    except Exception as e:
        print(f"❌ Failed to launch {interface_type}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
