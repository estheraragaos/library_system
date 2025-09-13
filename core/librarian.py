from datetime import datetime
from typing import Dict

class Librarian:
    def __init__(self, name: str, employee_id: str, email: str, access_level: str = "standard"):
        """
        Initialize a Librarian object
        """
        self.name = name
        self.employee_id = employee_id
        self.email = email
        self.access_level = access_level.lower()
        self.is_available = True
        self.shift_schedule = {}  # {day: (start_time, end_time)}
    
    def add_book_to_system(self, library, book: 'Book') -> bool:
        """
        Add a new book to the library system
        """
        if self.access_level not in ['standard', 'admin']:
            return False
        
        print(f"Librarian {self.name} added book: {book.title}")
        return True
    
    def remove_book_from_system(self, library, isbn: str) -> bool:
        """
        Remove a book from the library system
        """
        if self.access_level != 'admin':
            print("Insufficient permissions: Admin access required")
            return False
        
        print(f"Librarian {self.name} removed book with ISBN: {isbn}")
        return True
    
    def manage_reader_account(self, reader: 'Reader', action: str, **kwargs) -> bool:
        """
        Manage reader accounts
        """
        if action == 'suspend':
            reader.suspend_membership()
            print(f"Reader {reader.name} account suspended")
            return True
        
        elif action == 'activate':
            reader.activate_membership()
            print(f"Reader {reader.name} account activated")
            return True
        
        elif action == 'update_limit':
            new_limit = kwargs.get('new_limit')
            if new_limit and isinstance(new_limit, int) and new_limit > 0:
                reader.max_books = new_limit
                print(f"Reader {reader.name} book limit updated to {new_limit}")
                return True
        
        elif action == 'waive_fine':
            if self.access_level == 'admin':
                reader.fines = 0.0
                print(f"Fines waived for reader {reader.name}")
                return True
            else:
                print("Insufficient permissions: Admin access required for waiving fines")
                return False
        
        return False
    
    def generate_report(self, report_type: str) -> Dict:
        """
        Generate various library reports
        """
        reports = {
            'borrowing': {"title": "Borrowing Activity Report", "data": {}},
            'fines': {"title": "Outstanding Fines Report", "data": {}},
            'popular_books': {"title": "Popular Books Report", "data": {}}
        }
        
        if report_type in reports:
            print(f"Generating {report_type} report...")
            return reports[report_type]
        
        return {"error": "Invalid report type"}
    
    def set_shift_schedule(self, day: str, start_time: str, end_time: str) -> None:
        """
        Set shift schedule for the librarian
        """
        self.shift_schedule[day] = (start_time, end_time)
    
    def get_librarian_info(self) -> Dict:
        """
        Get comprehensive information about the librarian
        """
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "email": self.email,
            "access_level": self.access_level,
            "is_available": self.is_available,
            "shift_schedule": self.shift_schedule
        }
    
    def __str__(self) -> str:
        """String representation of the librarian"""
        return f"Librarian: {self.name} ({self.employee_id}) - {self.access_level.title()} Access"
    
    def __repr__(self) -> str:
        """Official string representation"""
        return f"Librarian(name='{self.name}', employee_id='{self.employee_id}', access_level='{self.access_level}')"

