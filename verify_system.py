#!/usr/bin/env python3
"""
Gaia AI System Verification Script
Quick verification of all major components
"""

import sys
from pathlib import Path

def test_imports():
    """Test all critical imports"""
    print("🔧 Testing Core Imports...")
    
    try:
        # Test main entry point
        import gaia
        print("✅ Main entry point (gaia.py) imports successfully")
        
        # Test GUI system
        from gui.simple_launcher import main as launcher_main
        from gui.main_window import GaiaMainWindow
        print("✅ GUI system imports successfully")
        
        # Test core agent
        from core.agent.gaia_agent import GaiaAgent
        print("✅ Core agent imports successfully")
        
        # Test interfaces
        from src.interfaces.cli_interface import CLIInterface
        from src.interfaces.gui_interface import GUIInterface
        from src.interfaces.hotel_interface import HotelInterface
        print("✅ All interfaces import successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_functionality():
    """Test basic functionality"""
    print("\n🎯 Testing Basic Functionality...")
    
    try:
        # Test agent creation
        from core.agent.gaia_agent import GaiaAgent
        GaiaAgent(log_callback=lambda msg: None)  # Silent mode
        print("✅ GaiaAgent can be created")
        
        # Test GUI imports (skip actual creation)
        from gui.main_window import GaiaMainWindow
        from gui.widgets.chat_widget import ChatWidget
        from gui.widgets.control_panel import ControlPanel
        from gui.widgets.status_bar import StatusBar
        print("✅ GUI components can be imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("🤖 GAIA AI SYSTEM VERIFICATION")
    print("=" * 50)
    
    imports_ok = test_imports()
    functionality_ok = test_functionality()
    
    print("\n" + "=" * 50)
    print("📊 VERIFICATION RESULTS")
    print("=" * 50)
    
    if imports_ok and functionality_ok:
        print("🎉 ✅ ALL TESTS PASSED")
        print("🚀 System is ready to use!")
        print("\n💡 To start Gaia AI:")
        print("   python gaia.py")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
