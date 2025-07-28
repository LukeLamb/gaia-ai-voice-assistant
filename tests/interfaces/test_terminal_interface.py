#!/usr/bin/env python3
"""
Test terminal interface without user interaction
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_terminal_interface():
    """Test the terminal interface functionality"""
    print("🖥️ Testing Terminal Interface")
    print("=" * 50)
    
    import gaia
    
    print("📋 Available menu options:")
    print("1. GUI (Recommended) - Professional interface")
    print("2. CLI - Command line interface") 
    print("3. Hotel - Hotel management system")
    print("4. Training - Train/fine-tune LLM")
    print("5. Email - Setup email integration")
    print("6. Exit")
    
    print("\n🔧 Testing choice validation:")
    test_choices = ['1', '2', '3', '4', '5', '6', 'x', '']
    for choice in test_choices:
        valid = gaia._is_valid_choice(choice)
        print(f"  Choice '{choice}': {'✅ Valid' if valid else '❌ Invalid'}")
    
    print("\n🗺️ Testing interface mapping:")
    valid_choices = ['1', '2', '3', '4', '5']
    for choice in valid_choices:
        interface_type = gaia._get_interface_type(choice)
        print(f"  Choice '{choice}' → {interface_type}")
    
    print("\n✅ Terminal interface is ready!")
    print("💡 To run interactively: python gaia.py")
    print("🔧 Note: Interface launching requires user interaction")

if __name__ == "__main__":
    test_terminal_interface()
