"""
Hotel Management Module
Core hotel operations and email processing
"""

from .hotel_manager import HotelManager, HotelRoom, EmailSummary, RoomStatus, GuestStatus
from .email_classifier import HotelEmailClassifier, EmailClassification, EmailCategory, EmailPriority

__all__ = [
    'HotelManager',
    'HotelRoom', 
    'EmailSummary',
    'RoomStatus',
    'GuestStatus',
    'HotelEmailClassifier',
    'EmailClassification',
    'EmailCategory',
    'EmailPriority'
]