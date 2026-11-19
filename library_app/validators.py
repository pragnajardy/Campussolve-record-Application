"""Centralized defensive input validation."""
import re
from datetime import date, datetime

ISBN_RE = re.compile(r"^(?:\d{9}[\dX]|\d{13})$")

def ask_text(prompt, minimum=1, maximum=100):
    while True:
        value = input(prompt).strip()
        if minimum <= len(value) <= maximum:
            return value
        print(f"Enter between {minimum} and {maximum} characters.")

def ask_int(prompt, minimum=1, maximum=100000):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if minimum <= value <= maximum:
                return value
            print(f"Enter a whole number from {minimum} to {maximum}.")
        except ValueError:
            print("Invalid number. Please enter a whole number.")

def ask_email(prompt):
    while True:
        value = input(prompt).strip().lower()
        if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            return value
        print("Enter a valid email address (example: name@example.com).")

def ask_date(prompt, default_today=False):
    while True:
        raw = input(prompt).strip()
        if not raw and default_today:
            return date.today().isoformat()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Use YYYY-MM-DD format (example: 2026-11-19).")

def ask_choice(prompt, choices):
    normalized = {str(c).lower(): str(c) for c in choices}
    while True:
        value = input(prompt).strip().lower()
        if value in normalized:
            return normalized[value]
        print("Choose one of: " + ", ".join(normalized))
