"""
Hotel Email Classification System
AI-powered email classification for hotel business operations
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional


class EmailCategory(Enum):
    """Email category enumeration"""
    BOOKING = "booking"
    INVOICE = "invoice"
    INQUIRY = "inquiry"
    COMPLAINT = "complaint"
    SUPPLIER = "supplier"
    MARKETING = "marketing"
    SPAM = "spam"
    OTHER = "other"


class EmailPriority(Enum):
    """Email priority enumeration"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class EmailClassification:
    """Email classification result"""
    category: EmailCategory
    priority: EmailPriority
    confidence: float
    booking_reference: Optional[str] = None
    guest_name: Optional[str] = None
    recommended_action: str = ""


class HotelEmailClassifier:
    """
    Intelligent email classifier for hotel operations
    """
    
    def __init__(self):
        self.booking_keywords = [
            'booking', 'reservation', 'confirm', 'check-in', 'check-out',
            'arrival', 'departure', 'stay', 'guest', 'room', 'nights'
        ]
        
        self.invoice_keywords = [
            'invoice', 'bill', 'payment', 'due', 'overdue', 'charge',
            'amount', 'total', 'pay', 'outstanding', 'balance'
        ]
        
        self.complaint_keywords = [
            'complaint', 'problem', 'issue', 'unhappy', 'disappointed',
            'unsatisfied', 'poor', 'terrible', 'awful', 'bad service'
        ]
        
        self.supplier_keywords = [
            'delivery', 'supply', 'vendor', 'maintenance', 'repair',
            'service', 'cleaning', 'linen', 'food', 'beverage'
        ]
        
        self.urgent_keywords = [
            'urgent', 'emergency', 'asap', 'immediate', 'critical',
            'important', 'rush', 'priority', 'leak', 'fire', 'security'
        ]
    
    def classify_email(self, subject: str, content: str, sender: str = "") -> EmailClassification:
        """
        Classify an email based on subject, content, and sender
        """
        # Combine all text for analysis
        full_text = f"{subject} {content} {sender}".lower()
        
        # Extract potential booking reference
        booking_ref = self._extract_booking_reference(full_text)
        
        # Extract guest name
        guest_name = self._extract_guest_name(subject, content)
        
        # Determine category and confidence
        category, confidence = self._categorize_email(full_text)
        
        # Determine priority
        priority = self._determine_priority(full_text, category)
        
        # Generate recommended action
        action = self._generate_action(category, priority, subject)
        
        return EmailClassification(
            category=category,
            priority=priority,
            confidence=confidence,
            booking_reference=booking_ref,
            guest_name=guest_name,
            recommended_action=action
        )
    
    def _categorize_email(self, text: str) -> tuple[EmailCategory, float]:
        """Categorize email based on content analysis"""
        
        # Check for booking-related content
        booking_score = self._calculate_keyword_score(text, self.booking_keywords)
        if booking_score > 0.3:
            return EmailCategory.BOOKING, booking_score
        
        # Check for invoice-related content
        invoice_score = self._calculate_keyword_score(text, self.invoice_keywords)
        if invoice_score > 0.4:
            return EmailCategory.INVOICE, invoice_score
        
        # Check for complaint-related content
        complaint_score = self._calculate_keyword_score(text, self.complaint_keywords)
        if complaint_score > 0.2:
            return EmailCategory.COMPLAINT, complaint_score
        
        # Check for supplier-related content
        supplier_score = self._calculate_keyword_score(text, self.supplier_keywords)
        if supplier_score > 0.3:
            return EmailCategory.SUPPLIER, supplier_score
        
        # Check for spam indicators
        if self._is_likely_spam(text):
            return EmailCategory.SPAM, 0.8
        
        # Check for marketing
        if self._is_marketing_email(text):
            return EmailCategory.MARKETING, 0.7
        
        # Default to inquiry
        return EmailCategory.INQUIRY, 0.5
    
    def _calculate_keyword_score(self, text: str, keywords: List[str]) -> float:
        """Calculate keyword matching score"""
        matches = sum(1 for keyword in keywords if keyword in text)
        return min(matches / len(keywords) * 2, 1.0)
    
    def _determine_priority(self, text: str, category: EmailCategory) -> EmailPriority:
        """Determine email priority based on content and category"""
        
        # Check for urgent keywords
        if any(urgent in text for urgent in self.urgent_keywords):
            return EmailPriority.CRITICAL
        
        # Category-based priority rules
        if category == EmailCategory.COMPLAINT:
            return EmailPriority.CRITICAL
        
        if category == EmailCategory.INVOICE:
            if 'overdue' in text or 'urgent' in text:
                return EmailPriority.CRITICAL
            return EmailPriority.HIGH
        
        if category == EmailCategory.BOOKING:
            if 'confirm' in text or 'today' in text or 'tomorrow' in text:
                return EmailPriority.HIGH
            return EmailPriority.MEDIUM
        
        if category == EmailCategory.SUPPLIER:
            return EmailPriority.MEDIUM
        
        if category in [EmailCategory.MARKETING, EmailCategory.SPAM]:
            return EmailPriority.LOW
        
        # Default priority
        return EmailPriority.MEDIUM
    
    def _extract_booking_reference(self, text: str) -> Optional[str]:
        """Extract booking reference numbers from email text"""
        patterns = [
            r'booking\s*(?:ref|reference|number|#)?\s*:?\s*([A-Z0-9]{6,12})',
            r'confirmation\s*(?:number|#)?\s*:?\s*([A-Z0-9]{6,12})',
            r'reference\s*(?:number|#)?\s*:?\s*([A-Z0-9]{6,12})',
            r'#([A-Z0-9]{6,12})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_guest_name(self, subject: str, content: str) -> Optional[str]:
        """Extract guest name from email"""
        # Look for common name patterns
        patterns = [
            r'dear\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
            r'mr\.?\s+([A-Z][a-z]+)',
            r'mrs\.?\s+([A-Z][a-z]+)',
            r'ms\.?\s+([A-Z][a-z]+)',
            r'guest:?\s*([A-Z][a-z]+\s+[A-Z][a-z]+)'
        ]
        
        full_text = f"{subject} {content}"
        for pattern in patterns:
            match = re.search(pattern, full_text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _is_likely_spam(self, text: str) -> bool:
        """Check if email is likely spam"""
        spam_indicators = [
            'viagra', 'casino', 'lottery', 'winner', 'congratulations',
            'free money', 'click here', 'limited time', 'act now',
            'make money fast', 'weight loss', 'debt free'
        ]
        
        spam_count = sum(1 for indicator in spam_indicators if indicator in text)
        return spam_count >= 2
    
    def _is_marketing_email(self, text: str) -> bool:
        """Check if email is marketing/promotional"""
        marketing_indicators = [
            'unsubscribe', 'newsletter', 'promotion', 'sale', 'discount',
            'offer', 'deal', 'special price', 'limited offer', 'subscribe'
        ]
        
        marketing_count = sum(1 for indicator in marketing_indicators if indicator in text)
        return marketing_count >= 2
    
    def _generate_action(self, category: EmailCategory, priority: EmailPriority, subject: str) -> str:
        """Generate recommended action based on classification"""
        subject_snippet = subject[:30]
        
        if priority == EmailPriority.CRITICAL:
            return self._generate_critical_action(category, subject_snippet)
        elif priority == EmailPriority.HIGH:
            return self._generate_high_action(category, subject_snippet)
        elif priority == EmailPriority.MEDIUM:
            return self._generate_medium_action(category, subject_snippet)
        else:  # LOW priority
            return f"LOW: Archive or delete if not relevant - {subject_snippet}"
    
    def _generate_critical_action(self, category: EmailCategory, subject_snippet: str) -> str:
        """Generate action for critical priority emails"""
        if category == EmailCategory.COMPLAINT:
            return f"URGENT: Address guest complaint immediately - {subject_snippet}"
        elif category == EmailCategory.INVOICE:
            return f"URGENT: Process overdue payment - {subject_snippet}"
        else:
            return f"URGENT: Review critical email - {subject_snippet}"
    
    def _generate_high_action(self, category: EmailCategory, subject_snippet: str) -> str:
        """Generate action for high priority emails"""
        if category == EmailCategory.BOOKING:
            return f"HIGH: Confirm booking details - {subject_snippet}"
        elif category == EmailCategory.INVOICE:
            return f"HIGH: Process invoice payment - {subject_snippet}"
        else:
            return f"HIGH: Review important email - {subject_snippet}"
    
    def _generate_medium_action(self, category: EmailCategory, subject_snippet: str) -> str:
        """Generate action for medium priority emails"""
        if category == EmailCategory.INQUIRY:
            return f"MEDIUM: Respond to guest inquiry - {subject_snippet}"
        elif category == EmailCategory.SUPPLIER:
            return f"MEDIUM: Review supplier communication - {subject_snippet}"
        else:
            return f"MEDIUM: Review email when convenient - {subject_snippet}"