#!/usr/bin/env python3
"""
Test the modular Gaia system
"""

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
        from gaia import GaiaApplication
        app = GaiaApplication()
        print("✅ Gaia Application created successfully")
        print(f"📋 Available interfaces: {list(app.interfaces.keys())}")
    except Exception as e:
        print(f"❌ Main entry failed: {e}")

if __name__ == "__main__":
    print("🤖 GAIA MODULAR SYSTEM TEST")
    print("=" * 40)
    
    test_imports()
    test_main_entry()
    
    print("\n🎉 Test completed!")
    print("💡 Run 'python gaia.py' to start the application")
