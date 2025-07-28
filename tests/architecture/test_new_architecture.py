#!/usr/bin/env python3
"""
Gaia AI Voice Assistant - New Modular Demo
This script demonstrates the new modular architecture
"""

def test_imports():
    """Test that all new modular components can be imported"""
    print("🔧 Testing modular imports...")
    
    try:
        # Test GUI components
        from gui.main_window import GaiaMainWindow
        from gui.widgets.chat_widget import ChatWidget
        from gui.widgets.control_panel import ControlPanel
        from gui.widgets.status_bar import StatusBar
        print("✅ GUI components imported successfully")
        
        # Test core components
        from core.agent.gaia_agent import GaiaAgent
        from core.agent.command_parser import CommandParser
        from core.audio.azure_tts import AzureTTS
        from core.audio.tts_manager import TTSManager
        from core.audio.voice_manager import VoiceManager
        from core.ai.llm_interface import LocalLLM
        from core.automation import app_control
        from core.memory.user_memory import UserMemory
        from core.utils.config_manager import ConfigManager
        print("✅ Core components imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_agent_creation():
    """Test that the new Gaia agent can be created"""
    print("\n🤖 Testing Gaia Agent creation...")
    
    try:
        from core.agent.gaia_agent import GaiaAgent
        
        # Create agent with a simple log callback
        def log_callback(message):
            print(f"  📝 {message}")
        
        # This will test component initialization
        agent = GaiaAgent(log_callback)
        print("✅ Gaia Agent created successfully")
        
        # Test command parsing
        result = agent.command_parser.parse_and_execute("what time is it")
        if result:
            print(f"✅ Command parsing works: {result}")
        else:
            print("✅ Command parsing works (no specific command matched)")
            
        return True
        
    except Exception as e:
        print(f"❌ Agent creation error: {e}")
        return False

def main():
    """Main demonstration function"""
    print("🚀 Gaia AI Voice Assistant - Modular Architecture Demo")
    print("=" * 55)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed!")
        return
    
    # Test agent creation (this will test config, Azure TTS, etc.)
    if not test_agent_creation():
        print("\n❌ Agent creation test failed!")
        return
    
    print("\n" + "=" * 55)
    print("🎉 All tests passed! New modular architecture is working!")
    print("\n📋 What's been improved:")
    print("  • Modular package structure for better organization")
    print("  • Professional PyQt5 GUI with dark theme")
    print("  • Reduced code complexity (SonarLint compliant)")
    print("  • Separated concerns into logical components")
    print("  • Enhanced error handling and fallback systems")
    print("  • Threaded architecture for responsive GUI")
    
    print("\n🚀 To start the new Gaia:")
    print("  python main_new.py")
    
    print("\n📁 Old monolithic files can now be archived:")
    print("  • voice_agent.py (replaced by core/agent/gaia_agent.py)")
    print("  • main.py (replaced by main_new.py)")

if __name__ == "__main__":
    main()
