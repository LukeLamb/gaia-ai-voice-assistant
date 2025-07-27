"""
LLM Training and Fine-tuning System
This module provides different approaches to train/customize your local LLM
"""

import json
import os
import subprocess
import ollama
from typing import List, Dict, Any
from datetime import datetime

class LLMTrainingManager:
    """
    Manages LLM training and fine-tuning for the hotel voice assistant
    """
    
    def __init__(self, base_model="llama3"):
        self.base_model = base_model
        self.training_data_dir = "training_data"
        self.models_dir = "custom_models"
        self.ensure_directories()
    
    def ensure_directories(self):
        """Create necessary directories for training data and models"""
        os.makedirs(self.training_data_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
    
    def create_hotel_training_dataset(self):
        """
        Create a comprehensive training dataset for hotel operations
        """
        print("🏨 CREATING HOTEL TRAINING DATASET")
        print("=" * 40)
        
        # Hotel-specific conversation data
        hotel_conversations = [
            {
                "input": "Check room availability for tonight",
                "output": "I'll check our room availability for tonight. Let me access the hotel system. We currently have 3 rooms available: Room 101 (Standard Double), Room 205 (Deluxe Queen), and Room 308 (Suite). Would you like me to provide details about any of these rooms?"
            },
            {
                "input": "A guest is complaining about noise",
                "output": "I understand there's a noise complaint. This is a high priority issue. Let me help you address this immediately. First, I'll log this as a critical guest service issue. Would you like me to: 1) Check which rooms are adjacent for potential relocation, 2) Document the complaint in the guest record, or 3) Suggest noise reduction solutions?"
            },
            {
                "input": "Process invoice for linen service",
                "output": "I'll help you process the linen service invoice. This should be categorized as a CRITICAL priority operational expense. Let me extract the key details: vendor, amount, service period, and due date. I'll also check if this matches our expected delivery schedule and budget allocations."
            },
            {
                "input": "Guest wants to extend their stay",
                "output": "I'll help with the stay extension request. This is great news for occupancy! Let me check: 1) Room availability for the extended dates, 2) Current rate compatibility, 3) Any upcoming reservations that might conflict. I'll also update the guest record and generate a new confirmation."
            },
            {
                "input": "Daily hotel summary",
                "output": "Here's your daily hotel summary: Current occupancy: 6/8 rooms (75%). Check-outs today: 2 guests. Check-ins expected: 3 guests. Critical emails: 1 invoice overdue. High priority: 2 booking confirmations pending. Maintenance needs: Room 204 AC service scheduled. Revenue status: On track for monthly targets."
            },
            {
                "input": "Email about booking cancellation",
                "output": "I've identified this as a booking cancellation email - HIGH priority. Key actions needed: 1) Update room availability in the system, 2) Process any applicable cancellation fees per policy, 3) Release the room for new bookings, 4) Send confirmation to the guest, 5) Update revenue projections. Would you like me to handle any of these steps?"
            },
            {
                "input": "Check housekeeping status",
                "output": "Let me check the housekeeping status across all 8 rooms. Room status: Clean and ready (5 rooms), In progress (2 rooms), Maintenance required (1 room). Priority items: Room 308 suite needs deep cleaning after checkout, Room 101 requires linen restocking. Estimated completion time for all rooms: 2 hours."
            },
            {
                "input": "Guest feedback about breakfast",
                "output": "Guest feedback about breakfast is valuable service intelligence. I'll categorize this as MEDIUM priority guest service feedback. Key actions: 1) Log feedback in guest profile, 2) Forward to kitchen management, 3) Check if pattern exists with other guest comments, 4) Prepare response acknowledging their input. Would you like me to draft a response?"
            }
        ]
        
        # Save training data
        training_file = os.path.join(self.training_data_dir, "hotel_conversations.json")
        with open(training_file, 'w', encoding='utf-8') as f:
            json.dump(hotel_conversations, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Created {len(hotel_conversations)} hotel conversation examples")
        print(f"📁 Saved to: {training_file}")
        
        # Create Ollama-compatible Modelfile
        self.create_hotel_modelfile(hotel_conversations)
        
        return training_file
    
    def create_hotel_modelfile(self, conversations: List[Dict]):
        """
        Create an Ollama Modelfile for hotel-specific fine-tuning
        """
        modelfile_content = f"""# Hotel Assistant Model
FROM {self.base_model}

# Set the temperature to be more consistent for hotel operations
PARAMETER temperature 0.1

# Set context length for longer conversations
PARAMETER num_ctx 4096

# Hotel-specific system prompt
SYSTEM \"\"\"You are a professional hotel management assistant with expertise in:
- 8-bedroom boutique hotel operations
- Email classification and prioritization
- Guest service excellence
- Revenue management
- Housekeeping coordination
- Booking management
- Invoice processing
- Customer complaint resolution

You provide concise, actionable responses with clear priorities (CRITICAL, HIGH, MEDIUM, LOW).
You understand hotel terminology and operational workflows.
You always maintain professional hospitality standards.
\"\"\"

"""
        
        # Add training examples
        for conv in conversations[:5]:  # Use first 5 for quick training
            modelfile_content += f"""
# Training example
USER: {conv['input']}
ASSISTANT: {conv['output']}
"""
        
        modelfile_path = os.path.join(self.models_dir, "HotelModelfile")
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        print(f"📝 Created Modelfile: {modelfile_path}")
        return modelfile_path
    
    def train_hotel_model(self, model_name="hotel-assistant"):
        """
        Train a custom hotel model using Ollama
        """
        print(f"🚀 TRAINING CUSTOM HOTEL MODEL: {model_name}")
        print("=" * 50)
        
        # Create training data first
        self.create_hotel_training_dataset()
        
        modelfile_path = os.path.join(self.models_dir, "HotelModelfile")
        
        try:
            # Create the custom model
            print("🔧 Creating custom model with Ollama...")
            subprocess.run([
                "ollama", "create", model_name, "-f", modelfile_path
            ], capture_output=True, text=True, check=True)
            
            print(f"✅ Model '{model_name}' created successfully!")
            print("🧪 Testing the new model...")
            
            # Test the new model
            self.test_trained_model(model_name)
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating model: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def test_trained_model(self, model_name="hotel-assistant"):
        """
        Test the trained model with hotel-specific queries
        """
        print(f"\n🧪 TESTING MODEL: {model_name}")
        print("=" * 30)
        
        test_queries = [
            "Check room availability",
            "Process guest complaint",
            "Daily hotel summary",
            "Email about booking"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            print("-" * 20)
            try:
                response = ollama.chat(
                    model=model_name,
                    messages=[{"role": "user", "content": query}]
                )
                print(f"🤖 Response: {response['message']['content'][:200]}...")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def create_fine_tuning_workflow(self):
        """
        Create an advanced fine-tuning workflow
        """
        print("🎯 ADVANCED FINE-TUNING WORKFLOW")
        print("=" * 40)
        
        workflow_steps = [
            "1. 📊 Data Collection - Gather hotel-specific conversations",
            "2. 🧹 Data Preparation - Clean and format training data", 
            "3. 🏗️ Model Architecture - Choose base model and parameters",
            "4. 🚀 Training Process - Fine-tune on hotel operations",
            "5. 🧪 Validation - Test model performance on hotel tasks",
            "6. 🚀 Deployment - Replace current model with trained version",
            "7. 📈 Monitoring - Track performance improvements"
        ]
        
        for step in workflow_steps:
            print(step)
        
        print("\n🎛️ TRAINING OPTIONS AVAILABLE:")
        print("A. Quick Training (Ollama Modelfile) - Fast, basic customization")
        print("B. Dataset Training (JSON format) - Structured conversation training") 
        print("C. Advanced Fine-tuning (External tools) - Deep model customization")
        print("D. Continuous Learning - Update model with new hotel data")
        
        return workflow_steps
    
    def setup_continuous_learning(self):
        """
        Set up continuous learning from hotel operations
        """
        print("🔄 CONTINUOUS LEARNING SETUP")
        print("=" * 30)
        
        learning_config = {
            "data_sources": [
                "guest_interactions", 
                "email_classifications",
                "successful_resolutions", 
                "user_corrections"
            ],
            "update_frequency": "weekly",
            "quality_threshold": 0.8,
            "auto_retrain": True
        }
        
        config_file = os.path.join(self.training_data_dir, "learning_config.json")
        with open(config_file, 'w') as f:
            json.dump(learning_config, f, indent=2)
        
        print("✅ Continuous learning configured")
        print(f"📁 Config saved: {config_file}")
        
        return learning_config
    
    def list_available_models(self):
        """
        List all available models including custom ones
        """
        print("📋 AVAILABLE MODELS")
        print("=" * 20)
        
        try:
            # Get list of models from Ollama
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            print("🤖 Ollama Models:")
            print(result.stdout)
            
            # Check for custom models
            if os.path.exists(self.models_dir):
                custom_models = os.listdir(self.models_dir)
                if custom_models:
                    print("\n🏨 Custom Hotel Models:")
                    for model in custom_models:
                        print(f"  • {model}")
            
        except Exception as e:
            print(f"❌ Error listing models: {e}")
    
    def interactive_training_menu(self):
        """
        Interactive menu for training options
        """
        print("\n🏨 LLM TRAINING MENU")
        print("=" * 25)
        print("1. 🚀 Quick Train Hotel Model")
        print("2. 📊 Create Training Dataset") 
        print("3. 🧪 Test Current Model")
        print("4. 📋 List Available Models")
        print("5. 🔄 Setup Continuous Learning")
        print("6. 🎯 View Training Workflow")
        print("7. ❌ Exit")
        
        while True:
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == "7":
                print("👋 Exiting training menu")
                break
                
            self._handle_menu_choice(choice)
    
    def _handle_menu_choice(self, choice: str):
        """Handle individual menu choices"""
        if choice == "1":
            self._handle_train_model()
        elif choice == "2":
            self.create_hotel_training_dataset()
        elif choice == "3":
            self._handle_test_model()
        elif choice == "4":
            self.list_available_models()
        elif choice == "5":
            self.setup_continuous_learning()
        elif choice == "6":
            self.create_fine_tuning_workflow()
        else:
            print("❌ Invalid choice. Please select 1-7.")
    
    def _handle_train_model(self):
        """Handle model training choice"""
        model_name = input("Enter custom model name (default: hotel-assistant): ").strip()
        if not model_name:
            model_name = "hotel-assistant"
        self.train_hotel_model(model_name)
    
    def _handle_test_model(self):
        """Handle model testing choice"""
        model_name = input("Enter model name to test (default: llama3): ").strip()
        if not model_name:
            model_name = "llama3"
        self.test_trained_model(model_name)


def main():
    """Main training interface"""
    trainer = LLMTrainingManager()
    trainer.interactive_training_menu()


if __name__ == "__main__":
    main()
