"""
Simple LLM Training Interface
Quick start script for training your hotel AI assistant
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.llm_training_manager import LLMTrainingManager

def main():
    """
    Simple interface to start LLM training
    """
    print("🤖 LLM TRAINING FOR HOTEL ASSISTANT")
    print("=" * 50)
    print()
    print("This system can train your AI to be better at:")
    print("✅ Understanding hotel terminology")
    print("✅ Prioritizing guest requests correctly") 
    print("✅ Processing hotel emails efficiently")
    print("✅ Managing room operations")
    print("✅ Handling booking inquiries")
    print()
    
    print("🎯 TRAINING OPTIONS:")
    print("1. Quick Training - Create hotel-specific model (5 minutes)")
    print("2. Interactive Menu - Full training control")
    print("3. View Current Models - See what's available")
    print()
    
    choice = input("What would you like to do? (1/2/3): ").strip()
    
    trainer = LLMTrainingManager()
    
    if choice == "1":
        print("\n🚀 QUICK TRAINING SELECTED")
        print("This will create a custom 'hotel-assistant' model...")
        print("The model will be trained on hotel-specific conversations.")
        print()
        
        confirm = input("Continue with quick training? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            success = trainer.train_hotel_model("hotel-assistant")
            if success:
                print("\n🎉 SUCCESS! Your custom hotel model is ready!")
                print("You can now use 'hotel-assistant' in your voice assistant")
                print("\nTo use the new model, update your LocalLLM:")
                print("  llm = LocalLLM(model='hotel-assistant')")
            else:
                print("\n❌ Training failed. Check the error messages above.")
        else:
            print("Training cancelled.")
    
    elif choice == "2":
        print("\n📋 OPENING INTERACTIVE MENU...")
        trainer.interactive_training_menu()
    
    elif choice == "3":
        print("\n📋 CURRENT MODELS:")
        trainer.list_available_models()
    
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()
