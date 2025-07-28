#!/usr/bin/env python3
"""
Test the modular Gaia system
"""

import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing modular imports...")
    
    try:
        from src.core.config_manager import ConfigManager
        print("✅ Config Manager imported successfully")
    except Exception as e:
        print(f"❌ Config Manager failed: {e}")
    
    try:
        from src.interfaces.cli_interface import CLIInterface
        print("✅ CLI Interface imported successfully")
    except Exception as e:
        print(f"❌ CLI Interface failed: {e}")
    
    try:
        from src.interfaces.gui_interface import GUIInterface
        print("✅ GUI Interface imported successfully")
    except Exception as e:
        print(f"❌ GUI Interface failed: {e}")
    
    try:
        from src.interfaces.hotel_interface import HotelInterface
        print("✅ Hotel Interface imported successfully")
    except Exception as e:
        print(f"❌ Hotel Interface failed: {e}")
    
    try:
        from src.training.llm_trainer import LLMTrainer
        print("✅ LLM Trainer imported successfully")
    except Exception as e:
        print(f"❌ LLM Trainer failed: {e}")
    
    try:
        from src.interfaces.email_interface import EmailInterface
        print("✅ Email Interface imported successfully")
    except Exception as e:
        print(f"❌ Email Interface failed: {e}")

def test_main_entry():
    """Test the main entry point"""
    print("\n🚀 Testing main entry point...")
    
    try:
        import gaia
        print("✅ Gaia module imported successfully")
        
        # Test that main function exists
        if hasattr(gaia, 'main'):
            print("✅ Main function found")
        else:
            print("❌ Main function not found")
            
        # Test that terminal menu function exists
        if hasattr(gaia, 'run_terminal_menu'):
            print("✅ Terminal menu function found")
        else:
            print("❌ Terminal menu function not found")
            
        # Test helper functions exist
        helper_functions = [
            '_display_banner',
            '_get_interface_mappings', 
            '_get_user_choice',
            '_is_valid_choice',
            '_get_interface_type',
            '_launch_interface',
            '_should_continue'
        ]
        
        for func_name in helper_functions:
            if hasattr(gaia, func_name):
                print(f"✅ Helper function {func_name} found")
            else:
                print(f"❌ Helper function {func_name} not found")
                
    except Exception as e:
        print(f"❌ Main entry failed: {e}")

def test_gui_launcher():
    """Test the GUI launcher functionality"""
    print("\n🖥️ Testing GUI launcher...")
    
    try:
        # Test GUI launcher module can be imported
        from gui.simple_launcher import GaiaLauncherWindow
        print("✅ GaiaLauncherWindow class imported successfully")
        
        # Test main function exists
        from gui.simple_launcher import main as launcher_main
        print("✅ GUI launcher main function found")
        
        # Test that the launcher has the expected methods
        expected_methods = ['show', 'init_ui', 'center_window', 'create_header', 'create_interface_buttons', 'launch_interface', 'apply_theme']
        for method_name in expected_methods:
            if hasattr(GaiaLauncherWindow, method_name):
                print(f"✅ Method {method_name} found")
            else:
                print(f"⚠️  Method {method_name} not found")
                
    except ImportError as e:
        print(f"⚠️  GUI launcher not available (expected in headless environment): {e}")
    except Exception as e:
        print(f"❌ GUI launcher test failed: {e}")


if __name__ == "__main__":
    print("🤖 GAIA MODULAR SYSTEM TEST")
    print("=" * 40)
    
    test_imports()
    test_main_entry()
    test_gui_launcher()
    
    print("\n🎉 Test completed!")
    print("💡 Run 'python gaia.py' to start the application")
