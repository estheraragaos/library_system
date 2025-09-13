from datetime import datetime, timedelta
from typing import Dict, Optional
import uuid

class Reader:
    def __init__(self, name: str, email: str, reader_id: Optional[str] = None):
        """
        Initialize a Reader object
        """
        self.name = name
        self.email = email
        self.reader_id = reader_id if reader_id else self._generate_reader_id()
        self.borrowed_books = {}  # {isbn: borrow_date}
        self.max_books = 5
        self.fines = 0.0
        self.is_active = True
        self.membership_date = datetime.now()
    
    def _generate_reader_id(self) -> str:
        """Generate a unique reader ID"""
        return f"RDR-{uuid.uuid4().hex[:8].upper()}"
    
    def borrow_book(self, isbn: str) -> bool:
        """
        Borrow a book
        """
        if len(self.borrowed_books) >= self.max_books:
            return False
        
        if isbn in self.borrowed_books:
            return False  # Already borrowed this book
        
        if self.fines > 0:
            return False  # Cannot borrow with outstanding fines
        
        if not self.is_active:
            return False
        
        self.borrowed_books[isbn] = datetime.now()
        return True
    
    def return_book(self, isbn: str) -> bool:
        """
        Return a borrowed book
        """
        if isbn not in self.borrowed_books:
            return False
        
        # Calculate fine if overdue (assuming 0.50 per day)
        borrow_date = self.borrowed_books[isbn]
        due_date = borrow_date + timedelta(days=14)
        
        if datetime.now() > due_date:
            overdue_days = (datetime.now() - due_date).days
            self.fines += overdue_days * 0.50
        
        del self.borrowed_books[isbn]
        return True
    
    def pay_fine(self, amount: float) -> float:
        """
        Pay outstanding fines
        """
        if amount <= 0:
            return amount
        
        if amount >= self.fines:
            change = amount - self.fines
            self.fines = 0.0
            return change
        else:
            self.fines -= amount
            return 0.0
    
    def get_borrowed_books_count(self) -> int:
        """Get number of currently borrowed books"""
        return len(self.borrowed_books)
    
    def can_borrow_more(self) -> bool:
        """Check if reader can borrow more books"""
        return (self.get_borrowed_books_count() < self.max_books and 
                self.fines == 0 and 
                self.is_active)
    
    def suspend_membership(self) -> None:
        """Suspend reader membership"""
        self.is_active = False
    
    def activate_membership(self) -> None:
        """Activate reader membership"""
        self.is_active = True
    
    def get_reader_info(self) -> Dict:
        """
        Get comprehensive information about the reader
        """
        return {
            "reader_id": self.reader_id,
            "name": self.name,
            "email": self.email,
            "borrowed_books_count": self.get_borrowed_books_count(),
            "max_books": self.max_books,
            "outstanding_fines": self.fines,
            "is_active": self.is_active,
            "membership_date": self.membership_date.strftime("%Y-%m-%d")
        }
    
    def __str__(self) -> str:
        """String representation of the reader"""
        status = "Active" if self.is_active else "Suspended"
        return f"Reader: {self.name} ({self.reader_id}) - {status}"
    
    def __repr__(self) -> str:
        """Official string representation"""
        return f"Reader(name='{self.name}', email='{self.email}', reader_id='{self.reader_id}')"
