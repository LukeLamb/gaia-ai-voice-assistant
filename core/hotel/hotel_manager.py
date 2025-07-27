"""
Hotel Management System
Comprehensive hotel operations management for 8-bedroom boutique hotel
"""

import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from enum import Enum


class RoomStatus(Enum):
    """Room status enumeration"""
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    CLEANING = "cleaning"
    MAINTENANCE = "maintenance"
    OUT_OF_ORDER = "out_of_order"


class GuestStatus(Enum):
    """Guest status enumeration"""
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    EXPECTED = "expected"
    NO_SHOW = "no_show"


@dataclass
class HotelRoom:
    """Hotel room data structure"""
    room_number: str
    room_type: str
    status: RoomStatus
    guest_name: str = ""
    check_in_date: Optional[str] = None
    check_out_date: Optional[str] = None
    rate_per_night: float = 0.0
    special_requests: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.special_requests is None:
            self.special_requests = []


@dataclass
class EmailSummary:
    """Email processing summary"""
    total_emails: int = 0
    critical_count: int = 0
    high_priority_count: int = 0
    booking_count: int = 0
    invoice_count: int = 0
    recommended_actions: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.recommended_actions is None:
            self.recommended_actions = []


class HotelManager:
    """
    Comprehensive hotel management system for boutique hotel operations
    """
    
    def __init__(self, hotel_name: str = "Boutique Hotel", total_rooms: int = 8):
        self.hotel_name = hotel_name
        self.total_rooms = total_rooms
        self.rooms: Dict[str, HotelRoom] = {}
        self.data_file = "hotel_data.json"
        
        # Initialize hotel data
        self.load_hotel_data()
    
    def load_hotel_data(self):
        """Load hotel data from JSON file with refactored helper methods"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load hotel settings
                self._load_hotel_settings(data)
                
                # Load room data
                self._load_room_data(data)
                
                # Load email data if available
                self._load_email_data(data)
                
            else:
                self._initialize_default_rooms()
                self.save_hotel_data()
                
        except Exception as e:
            print(f"Error loading hotel data: {e}")
            self._initialize_default_rooms()
    
    def _load_hotel_settings(self, data: Dict[str, Any]):
        """Load hotel settings from data"""
        self.hotel_name = data.get('hotel_name', self.hotel_name)
        self.total_rooms = data.get('total_rooms', self.total_rooms)
    
    def _load_room_data(self, data: Dict[str, Any]):
        """Load room data from JSON"""
        rooms_data = data.get('rooms', {})
        for room_num, room_data in rooms_data.items():
            self._update_room_from_data(room_num, room_data)
    
    def _update_room_from_data(self, room_num: str, room_data: Dict[str, Any]):
        """Update a single room from JSON data"""
        self.rooms[room_num] = HotelRoom(
            room_number=room_num,
            room_type=room_data.get('room_type', 'Standard'),
            status=RoomStatus(room_data.get('status', 'available')),
            guest_name=room_data.get('guest_name', ''),
            check_in_date=room_data.get('check_in_date'),
            check_out_date=room_data.get('check_out_date'),
            rate_per_night=room_data.get('rate_per_night', 100.0),
            special_requests=room_data.get('special_requests', [])
        )
    
    def _load_email_data(self, data: Dict[str, Any]):
        """Load email-related data if available"""
        email_data = data.get('email_settings', {})
        # Store email settings for future use
        self.email_settings = email_data
    
    def _initialize_default_rooms(self):
        """Initialize default room configuration"""
        room_types = [
            "Standard Double", "Standard Double", "Deluxe Queen", 
            "Deluxe Queen", "Junior Suite", "Junior Suite", 
            "Executive Suite", "Presidential Suite"
        ]
        
        base_rates = [80, 80, 120, 120, 180, 180, 250, 400]
        
        for i in range(1, self.total_rooms + 1):
            room_number = f"{100 + i}"
            self.rooms[room_number] = HotelRoom(
                room_number=room_number,
                room_type=room_types[i-1],
                status=RoomStatus.AVAILABLE,
                rate_per_night=base_rates[i-1]
            )
    
    def save_hotel_data(self):
        """Save hotel data to JSON file"""
        try:
            data = {
                'hotel_name': self.hotel_name,
                'total_rooms': self.total_rooms,
                'last_updated': datetime.now().isoformat(),
                'rooms': {},
                'email_settings': getattr(self, 'email_settings', {})
            }
            
            # Convert rooms to JSON-serializable format
            for room_num, room in self.rooms.items():
                room_dict = asdict(room)
                room_dict['status'] = room.status.value  # Convert enum to string
                data['rooms'][room_num] = room_dict
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Error saving hotel data: {e}")
    
    def get_available_rooms(self) -> List[HotelRoom]:
        """Get list of available rooms"""
        return [room for room in self.rooms.values() 
                if room.status == RoomStatus.AVAILABLE]
    
    def get_occupied_rooms(self) -> List[HotelRoom]:
        """Get list of occupied rooms"""
        return [room for room in self.rooms.values() 
                if room.status == RoomStatus.OCCUPIED]
    
    def check_in_guest(self, room_number: str, guest_name: str, 
                      check_out_date: str, special_requests: Optional[List[str]] = None) -> bool:
        """Check in a guest to a room"""
        if room_number not in self.rooms:
            return False
        
        room = self.rooms[room_number]
        if room.status != RoomStatus.AVAILABLE:
            return False
        
        # Update room information
        room.status = RoomStatus.OCCUPIED
        room.guest_name = guest_name
        room.check_in_date = datetime.now().isoformat()
        room.check_out_date = check_out_date
        room.special_requests = special_requests or []
        
        self.save_hotel_data()
        return True
    
    def check_out_guest(self, room_number: str) -> bool:
        """Check out a guest from a room"""
        if room_number not in self.rooms:
            return False
        
        room = self.rooms[room_number]
        if room.status != RoomStatus.OCCUPIED:
            return False
        
        # Clear room information
        room.status = RoomStatus.CLEANING
        room.guest_name = ""
        room.check_in_date = None
        room.check_out_date = None
        room.special_requests = []
        
        self.save_hotel_data()
        return True
    
    def update_room_status(self, room_number: str, status: RoomStatus) -> bool:
        """Update room status"""
        if room_number not in self.rooms:
            return False
        
        self.rooms[room_number].status = status
        self.save_hotel_data()
        return True
    
    def get_hotel_summary(self) -> Dict[str, Any]:
        """Get comprehensive hotel status summary"""
        available_rooms = self.get_available_rooms()
        occupied_rooms = self.get_occupied_rooms()
        
        # Calculate occupancy statistics
        occupancy_rate = (len(occupied_rooms) / self.total_rooms) * 100
        
        # Get revenue information
        today_revenue = sum(room.rate_per_night for room in occupied_rooms)
        
        return {
            'hotel_name': self.hotel_name,
            'total_rooms': self.total_rooms,
            'available_rooms': len(available_rooms),
            'occupied_rooms': len(occupied_rooms),
            'occupancy_rate': round(occupancy_rate, 1),
            'rooms_cleaning': len([r for r in self.rooms.values() if r.status == RoomStatus.CLEANING]),
            'rooms_maintenance': len([r for r in self.rooms.values() if r.status == RoomStatus.MAINTENANCE]),
            'daily_revenue': today_revenue,
            'available_room_list': [r.room_number for r in available_rooms],
            'occupied_room_list': [(r.room_number, r.guest_name) for r in occupied_rooms]
        }
    
    def process_emails(self, emails: List[Dict[str, Any]]) -> EmailSummary:
        """
        Process emails using the hotel email classifier
        """
        summary = EmailSummary()
        summary.total_emails = len(emails)
        
        try:
            from .email_classifier import HotelEmailClassifier
            classifier = HotelEmailClassifier()
            
            for email_data in emails:
                # Classify each email
                classification = classifier.classify_email(
                    email_data.get('subject', ''),
                    email_data.get('content', ''),
                    email_data.get('sender', '')
                )
                
                # Update summary counts
                if classification.priority.value == 'CRITICAL':
                    summary.critical_count += 1
                elif classification.priority.value == 'HIGH':
                    summary.high_priority_count += 1
                
                if classification.category.value == 'BOOKING':
                    summary.booking_count += 1
                elif classification.category.value == 'INVOICE':
                    summary.invoice_count += 1
                
                # Add recommended actions (ensure list is initialized)
                if summary.recommended_actions is None:
                    summary.recommended_actions = []
                
                if classification.priority.value in ['CRITICAL', 'HIGH']:
                    action = f"Review {classification.category.value.lower()} email: {email_data.get('subject', '')[:50]}"
                    summary.recommended_actions.append(action)
            
            return summary
            
        except ImportError as e:
            # Fallback if email classifier not available
            print(f"Email classifier not available: {e}")
            if summary.recommended_actions is None:
                summary.recommended_actions = []
            summary.recommended_actions.append("Email classifier not available - manual review required")
            return summary