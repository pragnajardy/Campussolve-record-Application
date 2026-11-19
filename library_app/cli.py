"""Terminal user interface."""
import os
from datetime import date, timedelta
from .storage import load_data, save_data
from .core import (add_book, add_member, issue_book, return_book, search_records,
                   summary, overdue_transactions, find_by_id, LibraryError)
from .validators import ask_text, ask_int, ask_email, ask_date, ask_choice
from .reports import export_reports

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def header():
    print("\n" + "=" * 62)
    print("              CAMPUSSOLVE | LIBRARY RECORDS")
    print("       Books • Members • Issue & Return • Analytics")
    print("=" * 62)

def table(rows, columns):
    if not rows:
        print("No records found.")
        return
    widths = [max(len(c), min(24, max(len(str(r.get(c, ""))) for r in rows))) for c in columns]
    line = "-+-".join("-" * w for w in widths)
    print(" | ".join(c.ljust(w) for c, w in zip(columns, widths)))
    print(line)
    for row in rows:
        print(" | ".join(str(row.get(c, ""))[:w].ljust(w) for c, w in zip(columns, widths)))

def pause():
    input("\nPress Enter to continue...")

def run():
    db = load_data()
    while True:
        header()
        print("1. Add book             2. Register member")
        print("3. Issue a book         4. Return a book")
        print("5. View / search books  6. View members")
        print("7. View transactions    8. Executive summary")
        print("9. Overdue alerts       10. Export reports")
        print("0. Save and exit")
        choice = input("\nSelect an option: ").strip()
        try:
            if choice == "1":
                title = ask_text("Book title: ", 2, 120)
                author = ask_text("Author: ", 2, 80)
                category = ask_text("Category: ", 2, 40)
                isbn = ask_text("ISBN (10 or 13 digits; X allowed at end for ISBN-10): ", 10, 13).upper()
                if not (len(isbn) == 13 and isbn.isdigit() or len(isbn) == 10 and isbn[:9].isdigit() and (isbn[-1].isdigit() or isbn[-1] == "X")):
                    print("Invalid ISBN format."); pause(); continue
                copies = ask_int("Number of copies: ", 1, 10000)
                item = add_book(db, title, author, category, isbn, copies)
                save_data(db); print(f"Added {item['id']} — {item['title']}")
            elif choice == "2":
                name = ask_text("Member name: ", 2, 80)
                email = ask_email("Email: ")
                phone = ask_text("Phone (include country code if needed): ", 7, 20)
                item = add_member(db, name, email, phone)
                save_data(db); print(f"Registered {item['id']} — {item['name']}")
            elif choice == "3":
                if not db["books"] or not db["members"]:
                    print("Add at least one book and one member first.")
                else:
                    table(db["books"], ["id", "title", "available_copies"])
                    book_id = ask_text("Book ID: ", 3, 20).upper()
                    table(db["members"], ["id", "name", "email"])
                    member_id = ask_text("Member ID: ", 3, 20).upper()
                    due = ask_date("Due date (YYYY-MM-DD): ")
                    txn = issue_book(db, book_id, member_id, due)
                    save_data(db); print(f"Issued successfully. Transaction: {txn['id']}")
            elif choice == "4":
                active = [t for t in db["transactions"] if t["status"] == "ISSUED"]
                table(active, ["id", "book_id", "member_id", "issue_date", "due_date"])
                tid = ask_text("Transaction ID to return: ", 3, 20).upper()
                return_book(db, tid); save_data(db); print("Return recorded successfully.")
            elif choice == "5":
                keyword = input("Search keyword (blank = all): ").strip()
                category = input("Category filter (blank = all): ").strip()
                table(search_records(db, "books", keyword, category),
                      ["id", "title", "author", "category", "isbn", "total_copies", "available_copies"])
            elif choice == "6":
                table(db["members"], ["id", "name", "email", "phone", "joined_on"])
            elif choice == "7":
                table(db["transactions"], ["id", "book_id", "member_id", "issue_date", "due_date", "return_date", "status"])
            elif choice == "8":
                s = summary(db)
                print("\nEXECUTIVE SUMMARY")
                for key, value in s.items():
                    print(f"{key.replace('_', ' ').title():28} {value}")
                if s["categories"]:
                    print("\nBooks by category:")
                    for category, count in s["categories"].items():
                        print(f"  {category:22} {count}")
            elif choice == "9":
                overdue = overdue_transactions(db)
                print(f"\nOVERDUE ITEMS: {len(overdue)}")
                for t in overdue:
                    book, member = find_by_id(db["books"], t["book_id"]), find_by_id(db["members"], t["member_id"])
                    days = (date.today() - date.fromisoformat(t["due_date"])).days
                    print(f"[OVERDUE {days}d] {t['id']} | {book['title'] if book else t['book_id']} | {member['name'] if member else t['member_id']} | due {t['due_date']}")
                if not overdue: print("No overdue books. Great!")
            elif choice == "10":
                paths = export_reports(db)
                print("\nReports generated:")
                for path in paths: print(" - " + path)
            elif choice == "0":
                save_data(db); print("All records saved. Goodbye!"); break
            else:
                print("Invalid menu choice. Enter a number from 0 to 10.")
        except (LibraryError, ValueError) as exc:
            print(f"\n[!] {exc}")
        except (OSError, KeyError) as exc:
            print(f"\n[ERROR] Operation could not be completed: {exc}")
        pause()
