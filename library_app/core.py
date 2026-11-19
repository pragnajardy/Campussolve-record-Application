"""Library domain operations and reporting."""
from datetime import date, datetime
from collections import Counter

class LibraryError(Exception):
    """Expected business-rule violation."""

def next_id(items, prefix):
    nums = []
    for item in items:
        try:
            nums.append(int(item["id"].split("-")[-1]))
        except (KeyError, ValueError):
            continue
    return f"{prefix}-{max(nums, default=0) + 1:04d}"

def add_book(db, title, author, category, isbn, copies):
    if any(b["isbn"] == isbn for b in db["books"]):
        raise LibraryError("A book with this ISBN already exists.")
    book = {"id": next_id(db["books"], "B"), "title": title, "author": author,
            "category": category, "isbn": isbn, "total_copies": copies,
            "available_copies": copies}
    db["books"].append(book)
    return book

def add_member(db, name, email, phone):
    if any(m["email"].lower() == email.lower() for m in db["members"]):
        raise LibraryError("A member with this email already exists.")
    member = {"id": next_id(db["members"], "M"), "name": name,
              "email": email, "phone": phone, "joined_on": date.today().isoformat()}
    db["members"].append(member)
    return member

def issue_book(db, book_id, member_id, due_date):
    book = find_by_id(db["books"], book_id)
    member = find_by_id(db["members"], member_id)
    if not book:
        raise LibraryError("Book ID not found.")
    if not member:
        raise LibraryError("Member ID not found.")
    if book["available_copies"] < 1:
        raise LibraryError("No copies are currently available.")
    if date.fromisoformat(due_date) < date.today():
        raise LibraryError("Due date cannot be in the past.")
    active = [t for t in db["transactions"] if t["book_id"] == book_id and
              t["member_id"] == member_id and t["status"] == "ISSUED"]
    if active:
        raise LibraryError("This member already has an active issue for this book.")
    txn = {"id": next_id(db["transactions"], "T"), "book_id": book_id,
           "member_id": member_id, "issue_date": date.today().isoformat(),
           "due_date": due_date, "return_date": None, "status": "ISSUED"}
    book["available_copies"] -= 1
    db["transactions"].append(txn)
    return txn

def return_book(db, transaction_id):
    txn = find_by_id(db["transactions"], transaction_id)
    if not txn:
        raise LibraryError("Transaction ID not found.")
    if txn["status"] == "RETURNED":
        raise LibraryError("This book has already been returned.")
    txn["status"] = "RETURNED"
    txn["return_date"] = date.today().isoformat()
    book = find_by_id(db["books"], txn["book_id"])
    if book:
        book["available_copies"] = min(book["total_copies"], book["available_copies"] + 1)
    return txn

def find_by_id(items, record_id):
    return next((x for x in items if x.get("id", "").lower() == record_id.lower()), None)

def search_records(db, collection, keyword="", category=""):
    if collection not in ("books", "members", "transactions"):
        raise LibraryError("Unknown record category.")
    rows = db[collection]
    result = []
    for row in rows:
        haystack = " ".join(str(v) for v in row.values()).lower()
        if keyword.lower() in haystack and (not category or row.get("category", "").lower() == category.lower()):
            result.append(row)
    return result

def overdue_transactions(db, today=None):
    today = today or date.today()
    result = []
    for txn in db["transactions"]:
        if txn["status"] == "ISSUED" and date.fromisoformat(txn["due_date"]) < today:
            result.append(txn)
    return result

def summary(db):
    books, members, txns = db["books"], db["members"], db["transactions"]
    active = [t for t in txns if t["status"] == "ISSUED"]
    returned = [t for t in txns if t["status"] == "RETURNED"]
    overdue = overdue_transactions(db)
    total_copies = sum(b["total_copies"] for b in books)
    available = sum(b["available_copies"] for b in books)
    categories = Counter(b["category"] for b in books)
    return {
        "book_titles": len(books), "total_copies": total_copies,
        "available_copies": available, "issued_copies": total_copies - available,
        "members": len(members), "total_transactions": len(txns),
        "active_issues": len(active), "returned": len(returned),
        "overdue": len(overdue),
        "return_rate_percent": round((len(returned) / len(txns) * 100), 1) if txns else 0.0,
        "average_copies_per_title": round(total_copies / len(books), 2) if books else 0.0,
        "categories": dict(categories)
    }
