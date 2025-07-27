"""
Hotel Interface - Hotel Management System Interface
Specialized interface for hotel operations and management
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from core.hotel.hotel_manager import HotelManager
    from core.hotel.email_classifier import HotelEmailClassifier
    HOTEL_AVAILABLE = True
    HotelManagerClass = HotelManager
    HotelEmailClassifierClass = HotelEmailClassifier
except ImportError:
    HOTEL_AVAILABLE = False
    HotelManagerClass = None
    HotelEmailClassifierClass = None


class HotelInterface:
    """
    Specialized hotel management interface
    """
    
    def __init__(self):
        if not HOTEL_AVAILABLE or HotelManagerClass is None or HotelEmailClassifierClass is None:
            raise ImportError("Hotel system not available")
        
        self.hotel_manager = HotelManagerClass()
        self.email_classifier = HotelEmailClassifierClass()
    
    def show_main_menu(self):
        """Show main hotel menu"""
        print("\n🏨 HOTEL MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. 📊 Hotel Status Dashboard")
        print("2. 🛏️  Room Management")
        print("3. 👥 Guest Management") 
        print("4. 📧 Email Processing")
        print("5. 💰 Revenue Report")
        print("6. ⚙️  Hotel Settings")
        print("7. ❌ Back to Main Menu")
    
    def show_hotel_dashboard(self):
        """Show hotel status dashboard"""
        summary = self.hotel_manager.get_hotel_summary()
        
        print(f"\n🏨 {summary['hotel_name']} - Dashboard")
        print("=" * 50)
        print(f"📊 Occupancy Rate: {summary['occupancy_rate']}% ({summary['occupied_rooms']}/{summary['total_rooms']} rooms)")
        print(f"💰 Daily Revenue: ${summary['daily_revenue']:.2f}")
        print(f"🛏️  Available Rooms: {len(summary['available_room_list'])}")
        print(f"🧹 Rooms Cleaning: {summary['rooms_cleaning']}")
        print(f"🔧 Rooms Maintenance: {summary['rooms_maintenance']}")
        
        print(f"\n📋 Available Rooms: {', '.join(summary['available_room_list'])}")
        
        if summary['occupied_room_list']:
            print("\n👥 Occupied Rooms:")
            for room_num, guest_name in summary['occupied_room_list']:
                print(f"  • Room {room_num}: {guest_name}")
    
    def show_room_management(self):
        """Show room management options"""
        print("\n🛏️ ROOM MANAGEMENT")
        print("=" * 30)
        print("1. 📋 List All Rooms")
        print("2. ✅ Check-in Guest")
        print("3. ❌ Check-out Guest")
        print("4. 🔧 Update Room Status")
        print("5. 🔙 Back")
        
        choice = input("Select option (1-5): ").strip()
        
        if choice == '1':
            self.list_all_rooms()
        elif choice == '2':
            self.check_in_guest()
        elif choice == '3':
            self.check_out_guest()
        elif choice == '4':
            self.update_room_status()
    
    def list_all_rooms(self):
        """List all rooms with their status"""
        print(f"\n📋 All Rooms - {self.hotel_manager.hotel_name}")
        print("-" * 60)
        
        for room_num, room in self.hotel_manager.rooms.items():
            status_emoji = {
                'available': '✅',
                'occupied': '👥',
                'cleaning': '🧹',
                'maintenance': '🔧',
                'out_of_order': '❌'
            }.get(room.status.value, '❓')
            
            print(f"{status_emoji} Room {room.room_number}: {room.room_type} - ${room.rate_per_night}/night")
            if room.guest_name:
                print(f"    Guest: {room.guest_name}")
            if room.check_out_date:
                print(f"    Check-out: {room.check_out_date}")
    
    def check_in_guest(self):
        """Handle guest check-in"""
        available_rooms = self.hotel_manager.get_available_rooms()
        
        if not available_rooms:
            print("❌ No available rooms")
            return
        
        print("\n✅ Available Rooms:")
        for room in available_rooms:
            print(f"  • Room {room.room_number}: {room.room_type} (${room.rate_per_night}/night)")
        
        room_number = input("Enter room number: ").strip()
        guest_name = input("Enter guest name: ").strip()
        check_out_date = input("Enter check-out date (YYYY-MM-DD): ").strip()
        
        if self.hotel_manager.check_in_guest(room_number, guest_name, check_out_date):
            print(f"✅ {guest_name} checked into Room {room_number}")
        else:
            print("❌ Check-in failed. Room may not be available.")
    
    def check_out_guest(self):
        """Handle guest check-out"""
        occupied_rooms = self.hotel_manager.get_occupied_rooms()
        
        if not occupied_rooms:
            print("❌ No occupied rooms")
            return
        
        print("\n👥 Occupied Rooms:")
        for room in occupied_rooms:
            print(f"  • Room {room.room_number}: {room.guest_name}")
        
        room_number = input("Enter room number for check-out: ").strip()
        
        if self.hotel_manager.check_out_guest(room_number):
            print(f"✅ Guest checked out from Room {room_number}")
        else:
            print("❌ Check-out failed. Room may not be occupied.")
    
    def update_room_status(self):
        """Update room status"""
        from core.hotel.hotel_manager import RoomStatus
        
        room_number = input("Enter room number: ").strip()
        
        print("Room Status Options:")
        statuses = list(RoomStatus)
        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status.value.title()}")
        
        try:
            choice = int(input("Select new status: ")) - 1
            new_status = statuses[choice]
            
            if self.hotel_manager.update_room_status(room_number, new_status):
                print(f"✅ Room {room_number} status updated to {new_status.value}")
            else:
                print("❌ Failed to update room status")
                
        except (ValueError, IndexError):
            print("❌ Invalid selection")
    
    def process_emails(self):
        """Process and classify emails"""
        print("\n📧 EMAIL PROCESSING")
        print("=" * 30)
        
        # Demo with sample emails
        sample_emails = [
            {"subject": "Urgent: Booking Confirmation Required", "content": "Please confirm your booking", "sender": "guest@hotel.com"},
            {"subject": "Invoice Overdue - Linen Service", "content": "Payment due immediately", "sender": "linens@supplier.com"},
            {"subject": "Guest Complaint - Room 205", "content": "Noise issue reported", "sender": "frontdesk@hotel.com"},
            {"subject": "Marketing Newsletter", "content": "Special offers this month", "sender": "marketing@travel.com"}
        ]
        
        print("Processing sample emails...")
        summary = self.hotel_manager.process_emails(sample_emails)
        
        print("\n📊 Email Summary:")
        print(f"  Total: {summary.total_emails}")
        print(f"  Critical: {summary.critical_count}")
        print(f"  High Priority: {summary.high_priority_count}")
        print(f"  Booking Related: {summary.booking_count}")
        print(f"  Invoice Related: {summary.invoice_count}")
        
        if summary.recommended_actions:
            print("\n⚡ Recommended Actions:")
            for action in summary.recommended_actions:
                print(f"  • {action}")
    
    def show_revenue_report(self):
        """Show revenue report"""
        summary = self.hotel_manager.get_hotel_summary()
        occupied_rooms = self.hotel_manager.get_occupied_rooms()
        
        print("\n💰 REVENUE REPORT")
        print("=" * 30)
        print(f"Daily Revenue: ${summary['daily_revenue']:.2f}")
        print(f"Occupancy Rate: {summary['occupancy_rate']}%")
        
        if occupied_rooms:
            print("\nRevenue Breakdown:")
            total = 0
            for room in occupied_rooms:
                print(f"  Room {room.room_number}: ${room.rate_per_night:.2f}")
                total += room.rate_per_night
            print(f"  Total: ${total:.2f}")
    
    def hotel_settings(self):
        """Show hotel settings"""
        print("\n⚙️ HOTEL SETTINGS")
        print("=" * 30)
        print(f"Hotel Name: {self.hotel_manager.hotel_name}")
        print(f"Total Rooms: {self.hotel_manager.total_rooms}")
        print(f"Data File: {self.hotel_manager.data_file}")
    
    def run(self):
        """Run the hotel interface"""
        print("🏨 Starting Hotel Management System...")
        
        try:
            while True:
                self.show_main_menu()
                choice = input("\nSelect option (1-7): ").strip()
                
                if choice == '1':
                    self.show_hotel_dashboard()
                elif choice == '2':
                    self.show_room_management()
                elif choice == '3':
                    print("👥 Guest management coming soon...")
                elif choice == '4':
                    self.process_emails()
                elif choice == '5':
                    self.show_revenue_report()
                elif choice == '6':
                    self.hotel_settings()
                elif choice == '7':
                    print("👋 Returning to main menu...")
                    break
                else:
                    print("❌ Invalid choice. Please select 1-7.")
                
                input("\nPress Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Hotel interface closed")
        except Exception as e:
            print(f"❌ Hotel interface error: {e}")
            
        return 0
