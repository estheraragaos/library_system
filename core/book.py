from datetime import datetime, timedelta
from typing import Dict, Optional

class Book:
    def __init__(self, title: str, author: str, isbn: str, publication_year: int, 
                 genre: str = "Unknown", total_copies: int = 1):
        """
        Initialize a Book object
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_year = publication_year
        self.genre = genre
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.borrowers = {}  # {user_id: due_date}
        self.is_available = True if total_copies > 0 else False
    
    def borrow_book(self, user_id: str, loan_period_days: int = 14) -> bool:
        """
        Borrow a copy of the book
        """
        if self.available_copies <= 0:
            return False
        
        if user_id in self.borrowers:
            return False  # User already has this book
        
        due_date = datetime.now() + timedelta(days=loan_period_days)
        self.borrowers[user_id] = due_date
        self.available_copies -= 1
        
        if self.available_copies == 0:
            self.is_available = False
            
        return True
    
    def return_book(self, user_id: str) -> bool:
        """
        Return a borrowed book
        """
        if user_id not in self.borrowers:
            return False
        
        del self.borrowers[user_id]
        self.available_copies += 1
        self.is_available = True
        
        return True
    
    def is_overdue(self, user_id: str) -> bool:
        """
        Check if a book is overdue for a specific user
        """
        if user_id not in self.borrowers:
            return False
        
        return datetime.now() > self.borrowers[user_id]
    
    def get_due_date(self, user_id: str) -> Optional[datetime]:
        """
        Get the due date for a specific user
        """
        return self.borrowers.get(user_id)
    
    def add_copies(self, num_copies: int) -> None:
        """
        Add more copies of the book
        """
        self.total_copies += num_copies
        self.available_copies += num_copies
        self.is_available = True
    
    def remove_copies(self, num_copies: int) -> bool:
        """
        Remove copies of the book
        """
        if num_copies > self.available_copies:
            return False
        
        self.total_copies -= num_copies
        self.available_copies -= num_copies
        
        if self.available_copies == 0:
            self.is_available = False
            
        return True
    
    def get_borrower_count(self) -> int:
        """Get number of current borrowers"""
        return len(self.borrowers)
    
    def get_book_info(self) -> Dict:
        """
        Get comprehensive information about the book
        """
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_year": self.publication_year,
            "genre": self.genre,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
            "borrower_count": self.get_borrower_count(),
            "is_available": self.is_available
        }
    
    def __str__(self) -> str:
        """String representation of the book"""
        return f"'{self.title}' by {self.author} ({self.publication_year}) - ISBN: {self.isbn}"
    
    def __repr__(self) -> str:
        """Official string representation"""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"
