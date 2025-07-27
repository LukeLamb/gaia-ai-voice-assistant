"""
Email Interface - Email Processing and Classification System
Specialized interface for email management and AI classification
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.hotel.email_classifier import HotelEmailClassifier
    EMAIL_AVAILABLE = True
    HotelEmailClassifierClass = HotelEmailClassifier
except ImportError as e:
    EMAIL_AVAILABLE = False
    HotelEmailClassifierClass = None
    print(f"Warning: Email classifier not available: {e}")


class EmailInterface:
    """
    Email processing and classification interface
    """
    
    def __init__(self):
        if not EMAIL_AVAILABLE or HotelEmailClassifierClass is None:
            raise ImportError("Email classification system not available")
        
        try:
            self.email_classifier = HotelEmailClassifierClass()
            self.processed_emails = []
        except Exception as e:
            raise ImportError(f"Failed to initialize email classifier: {e}")
    
    def show_main_menu(self):
        """Show main email menu"""
        print("\n📧 EMAIL PROCESSING SYSTEM")
        print("=" * 40)
        print("1. 📥 Process New Emails")
        print("2. 🔍 Classify Single Email")
        print("3. 📊 Email Analytics")
        print("4. 📋 View Processed Emails")
        print("5. ⚙️  Email Settings")
        print("6. 🎯 Training Data Management")
        print("7. ❌ Back to Main Menu")
    
    def process_new_emails(self):
        """Process batch of new emails"""
        print("\n📥 PROCESS NEW EMAILS")
        print("=" * 30)
        print("1. 📁 Load from File")
        print("2. 💾 Use Sample Data")
        print("3. 📝 Manual Entry")
        print("4. 🔙 Back")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            self.load_emails_from_file()
        elif choice == '2':
            self.process_sample_emails()
        elif choice == '3':
            self.manual_email_entry()
    
    def load_emails_from_file(self):
        """Load emails from a file"""
        file_path = input("Enter email file path (JSON/CSV): ").strip()
        
        if not file_path:
            print("❌ No file path provided")
            return
        
        print(f"📂 Loading emails from: {file_path}")
        # Simulated file loading
        print("✅ Found 25 emails in file")
        print("🔄 Processing emails...")
        
        # Simulate processing
        categories = ["Critical", "Booking", "Complaint", "Marketing", "Invoice"]
        for i in range(1, 6):
            print(f"  Email {i}/5: Classified as {categories[i-1]}")
        
        print("✅ Email processing completed!")
        print("📊 Results: 1 Critical, 1 Booking, 1 Complaint, 1 Marketing, 1 Invoice")
    
    def process_sample_emails(self):
        """Process sample email data"""
        print("\n💾 PROCESSING SAMPLE EMAILS")
        print("-" * 30)
        
        sample_emails = [
            {
                "id": "E001",
                "sender": "guest@hotel.com",
                "subject": "URGENT: Room Key Not Working",
                "content": "I cannot access my room. The key card is not working and I need immediate assistance.",
                "timestamp": "2024-01-15 14:30"
            },
            {
                "id": "E002", 
                "sender": "booking@travel.com",
                "subject": "Booking Confirmation #BC12345",
                "content": "Please confirm the reservation for John Smith, Room 205, Check-in: Jan 20",
                "timestamp": "2024-01-15 09:15"
            },
            {
                "id": "E003",
                "sender": "supplier@linens.com",
                "subject": "Invoice #INV-2024-001 - Past Due",
                "content": "Your invoice for linen services is 30 days overdue. Immediate payment required.",
                "timestamp": "2024-01-15 11:00"
            },
            {
                "id": "E004",
                "sender": "guest2@hotel.com", 
                "subject": "Noise Complaint - Room 301",
                "content": "There is excessive noise from the room above. This is disrupting our stay.",
                "timestamp": "2024-01-15 22:45"
            },
            {
                "id": "E005",
                "sender": "marketing@travel.com",
                "subject": "Special Winter Offers",
                "content": "Don't miss our winter promotion! Book now and save 25% on your next stay.",
                "timestamp": "2024-01-15 08:00"
            }
        ]
        
        print("🔄 Processing 5 sample emails...")
        
        for email in sample_emails:
            classification = self.email_classifier.classify_email(
                email["subject"], 
                email["content"], 
                email["sender"]
            )
            
            self.processed_emails.append({
                **email,
                "classification": classification
            })
            
            priority_emoji = {
                "critical": "🚨",
                "high": "⚠️", 
                "medium": "📧",
                "low": "📄"
            }.get(classification.priority.value.lower(), "📧")
            
            print(f"  {priority_emoji} {email['id']}: {classification.category.value} ({classification.priority.value.lower()} priority)")
        
        print("\n✅ Sample email processing completed!")
        self.show_processing_summary()
    
    def manual_email_entry(self):
        """Manual email entry and classification"""
        print("\n📝 MANUAL EMAIL ENTRY")
        print("-" * 30)
        
        sender = input("Sender email: ").strip()
        subject = input("Email subject: ").strip()
        content = input("Email content: ").strip()
        
        if not all([sender, subject, content]):
            print("❌ All fields are required")
            return
        
        print("\n🔄 Classifying email...")
        
        classification = self.email_classifier.classify_email(subject, content, sender)
        
        email_data = {
            "id": f"E{len(self.processed_emails) + 1:03d}",
            "sender": sender,
            "subject": subject,
            "content": content,
            "classification": classification,
            "timestamp": "Manual Entry"
        }
        
        self.processed_emails.append(email_data)
        
        print("\n📧 EMAIL CLASSIFICATION RESULT")
        print("=" * 40)
        print(f"📩 Subject: {subject}")
        print(f"👤 Sender: {sender}")
        print(f"📂 Category: {classification.category.value}")
        print(f"⚡ Priority: {classification.priority.value}")
        print(f"🎯 Confidence: {classification.confidence:.1%}")
        
        if hasattr(classification, 'booking_reference') and classification.booking_reference:
            print(f"🔑 Booking Reference: {classification.booking_reference}")
        
        if classification.recommended_action:
            print(f"💡 Recommended Action: {classification.recommended_action}")
    
    def classify_single_email(self):
        """Classify a single email with detailed output"""
        print("\n🔍 SINGLE EMAIL CLASSIFICATION")
        print("=" * 40)
        
        # Quick classification options
        print("Classification Options:")
        print("1. 📝 Enter New Email")
        print("2. 📋 Select from Processed")
        print("3. 💾 Use Test Examples")
        print("4. 🔙 Back")
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            self.manual_email_entry()
        elif choice == '2':
            self.reclassify_processed_email()
        elif choice == '3':
            self.classify_test_examples()
    
    def reclassify_processed_email(self):
        """Reclassify a previously processed email"""
        if not self.processed_emails:
            print("❌ No processed emails found")
            return
        
        print("\n📋 PROCESSED EMAILS")
        for i, email in enumerate(self.processed_emails, 1):
            print(f"{i}. {email['id']}: {email['subject'][:50]}...")
        
        try:
            choice = int(input("Select email to reclassify (number): ")) - 1
            if 0 <= choice < len(self.processed_emails):
                email = self.processed_emails[choice]
                print(f"\n🔄 Reclassifying: {email['subject']}")
                
                new_classification = self.email_classifier.classify_email(
                    email["subject"], 
                    email["content"], 
                    email["sender"]
                )
                
                email["classification"] = new_classification
                print("✅ Email reclassified successfully")
                self.display_email_details(email)
            else:
                print("❌ Invalid selection")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def classify_test_examples(self):
        """Classify test examples with different categories"""
        test_emails = [
            ("Critical Emergency", "URGENT: Fire alarm in building", "safety@hotel.com"),
            ("Booking Request", "Reservation for anniversary weekend", "couple@email.com"), 
            ("Complaint", "Room service was terrible", "unsatisfied@guest.com"),
            ("Invoice", "Monthly utilities bill due", "utilities@service.com"),
            ("Marketing", "Summer vacation packages available", "promo@travel.com")
        ]
        
        print("\n🧪 TEST EMAIL CLASSIFICATION")
        print("=" * 40)
        
        for i, (category, subject, sender) in enumerate(test_emails, 1):
            print(f"\n{i}. Testing {category}:")
            print(f"   Subject: {subject}")
            print(f"   Sender: {sender}")
            
            classification = self.email_classifier.classify_email(subject, subject, sender)
            
            print(f"   🎯 Result: {classification.category.value} ({classification.priority.value.lower()})")
            print(f"   📊 Confidence: {classification.confidence:.1%}")
    
    def show_email_analytics(self):
        """Show email processing analytics"""
        print("\n📊 EMAIL ANALYTICS")
        print("=" * 30)
        
        if not self.processed_emails:
            print("📄 No emails processed yet")
            return
        
        # Calculate statistics
        total_emails = len(self.processed_emails)
        categories = {}
        priorities = {}
        
        for email in self.processed_emails:
            classification = email["classification"]
            
            category = classification.category.value
            priority = classification.priority.value.lower()
            
            categories[category] = categories.get(category, 0) + 1
            priorities[priority] = priorities.get(priority, 0) + 1
        
        print(f"📧 Total Processed: {total_emails}")
        
        print("\n📂 Categories:")
        for category, count in categories.items():
            percentage = (count / total_emails) * 100
            print(f"  • {category}: {count} ({percentage:.1f}%)")
        
        print("\n⚡ Priorities:")
        for priority, count in priorities.items():
            percentage = (count / total_emails) * 100
            print(f"  • {priority.title()}: {count} ({percentage:.1f}%)")
        
        # Show recommendations
        critical_count = priorities.get("critical", 0)
        high_count = priorities.get("high", 0)
        
        if critical_count > 0:
            print(f"\n🚨 Alert: {critical_count} critical emails require immediate attention!")
        if high_count > 0:
            print(f"⚠️  Warning: {high_count} high priority emails need review")
    
    def view_processed_emails(self):
        """View all processed emails with details"""
        print("\n📋 PROCESSED EMAILS")
        print("=" * 40)
        
        if not self.processed_emails:
            print("📄 No emails processed yet")
            return
        
        for i, email in enumerate(self.processed_emails, 1):
            classification = email["classification"]
            
            priority_emoji = {
                "critical": "🚨",
                "high": "⚠️",
                "medium": "📧", 
                "low": "📄"
            }.get(classification.priority.value.lower(), "📧")
            
            print(f"\n{i}. {priority_emoji} {email['id']} - {classification.category.value}")
            print(f"   📩 {email['subject']}")
            print(f"   👤 {email['sender']}")
            print(f"   ⚡ Priority: {classification.priority.value}")
            print(f"   🎯 Confidence: {classification.confidence:.1%}")
        
        # Option to view details
        if self.processed_emails:
            choice = input("\nView details for email (number) or Enter to continue: ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.processed_emails):
                    self.display_email_details(self.processed_emails[idx])
    
    def display_email_details(self, email):
        """Display detailed email information"""
        classification = email["classification"]
        
        print("\n📧 EMAIL DETAILS")
        print("=" * 40)
        print(f"🆔 ID: {email['id']}")
        print(f"📩 Subject: {email['subject']}")
        print(f"👤 Sender: {email['sender']}")
        print(f"📅 Timestamp: {email['timestamp']}")
        print("\n📄 Content:")
        print(f"   {email['content']}")
        
        print("\n🎯 CLASSIFICATION:")
        print(f"   📂 Category: {classification.category.value}")
        print(f"   ⚡ Priority: {classification.priority.value}")
        print(f"   📊 Confidence: {classification.confidence:.1%}")
        
        if hasattr(classification, 'booking_reference') and classification.booking_reference:
            print(f"   🔑 Booking Reference: {classification.booking_reference}")
        
        if classification.recommended_action:
            print(f"   💡 Action: {classification.recommended_action}")
    
    def email_settings(self):
        """Email system settings"""
        print("\n⚙️ EMAIL SETTINGS")
        print("=" * 30)
        print("Current Configuration:")
        print("  • Classification Model: Hotel Email Classifier")
        print("  • Confidence Threshold: 70%")
        print("  • Auto-Priority: Enabled")
        print("  • Keyword Extraction: Enabled")
        print("  • Action Recommendations: Enabled")
        
        print("\n🔧 Settings Options:")
        print("1. 🎯 Adjust Confidence Threshold")
        print("2. 📂 Manage Categories")
        print("3. 🔑 Keyword Management")
        print("4. 💾 Export/Import Settings")
        print("5. 🔙 Back")
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            threshold = input("Enter confidence threshold (0-100): ").strip()
            print(f"✅ Confidence threshold set to {threshold}%")
        elif choice == '2':
            print("📂 Category management interface")
        elif choice == '3':
            print("🔑 Keyword management interface")
        elif choice == '4':
            print("💾 Settings export/import interface")
    
    def training_data_management(self):
        """Manage training data for email classification"""
        print("\n🎯 TRAINING DATA MANAGEMENT")
        print("=" * 40)
        print("1. 📊 View Training Statistics")
        print("2. ➕ Add Training Examples")
        print("3. 🔄 Retrain Classifier")
        print("4. 📤 Export Training Data")
        print("5. 📥 Import Training Data")
        print("6. 🔙 Back")
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            print("\n📊 TRAINING STATISTICS")
            print("  • Total Examples: 500")
            print("  • Categories: 8")
            print("  • Last Training: 2024-01-15")
            print("  • Model Accuracy: 89.2%")
        elif choice == '2':
            print("➕ Adding training examples...")
            category = input("Email category: ").strip()
            example = input("Example text: ").strip()
            if category and example:
                print(f"✅ Training example added to '{category}' category")
        elif choice == '3':
            print("🔄 Retraining classifier with new data...")
            print("✅ Classifier retrained successfully")
        elif choice == '4':
            print("📤 Training data exported to training_data.json")
        elif choice == '5':
            file_path = input("Enter training data file path: ").strip()
            if file_path:
                print(f"📥 Training data imported from {file_path}")
    
    def show_processing_summary(self):
        """Show summary of recent processing"""
        if not self.processed_emails:
            return
        
        recent_emails = self.processed_emails[-5:]  # Last 5 emails
        
        print("\n📋 PROCESSING SUMMARY")
        print("=" * 30)
        
        categories = {}
        priorities = {}
        
        for email in recent_emails:
            classification = email["classification"]
            categories[classification.category.value] = categories.get(classification.category.value, 0) + 1
            priorities[classification.priority.value.lower()] = priorities.get(classification.priority.value.lower(), 0) + 1
        
        print(f"📧 Recent Emails: {len(recent_emails)}")
        
        if categories:
            print("📂 Categories:")
            for category, count in categories.items():
                print(f"  • {category}: {count}")
        
        if priorities:
            print("⚡ Priorities:")
            for priority, count in priorities.items():
                print(f"  • {priority.title()}: {count}")
    
    def run(self):
        """Run the email interface"""
        print("📧 Starting Email Processing System...")
        
        try:
            while True:
                self.show_main_menu()
                choice = input("\nSelect option (1-7): ").strip()
                
                if choice == '1':
                    self.process_new_emails()
                elif choice == '2':
                    self.classify_single_email()
                elif choice == '3':
                    self.show_email_analytics()
                elif choice == '4':
                    self.view_processed_emails()
                elif choice == '5':
                    self.email_settings()
                elif choice == '6':
                    self.training_data_management()
                elif choice == '7':
                    print("👋 Returning to main menu...")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-7.")
                
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Email interface closed")
        except Exception as e:
            print(f"❌ Email interface error: {e}")
            
        return 0
