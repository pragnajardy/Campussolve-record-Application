import unittest
from datetime import date, timedelta
from library_app.core import add_book, add_member, issue_book, return_book, summary, LibraryError

class LibraryCoreTests(unittest.TestCase):
    def setUp(self):
        self.db = {"books": [], "members": [], "transactions": []}
        self.book = add_book(self.db, "Python Basics", "A. Writer", "Technology", "1234567890123", 2)
        self.member = add_member(self.db, "Test Member", "test@example.com", "9876543210")

    def test_issue_and_return_updates_inventory(self):
        due = (date.today() + timedelta(days=7)).isoformat()
        txn = issue_book(self.db, self.book["id"], self.member["id"], due)
        self.assertEqual(self.book["available_copies"], 1)
        return_book(self.db, txn["id"])
        self.assertEqual(self.book["available_copies"], 2)
        self.assertEqual(summary(self.db)["returned"], 1)

    def test_duplicate_isbn_rejected(self):
        with self.assertRaises(LibraryError):
            add_book(self.db, "Duplicate", "Writer", "Tech", "1234567890123", 1)

    def test_no_stock_rejected(self):
        self.book["available_copies"] = 0
        with self.assertRaises(LibraryError):
            issue_book(self.db, self.book["id"], self.member["id"],
                       (date.today() + timedelta(days=1)).isoformat())

if __name__ == "__main__":
    unittest.main()
