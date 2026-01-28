#!/usr/bin/env python3
"""CLI for creating data fields with labels and types."""

import argparse
import sqlite3
from pathlib import Path

DATA_DIR = Path(".data")
DB_PATH = DATA_DIR / "data.db"
VALID_TYPES = ("numeric", "date", "text", "boolean")


def init_db() -> None:
    """Create database and fields table if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            data_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_label() -> str:
    """Prompt user for a field label."""
    while True:
        label = input("Enter field label: ").strip()
        if label:
            return label
        print("Label cannot be empty. Please try again.")


def get_data_type() -> str:
    """Prompt user for a data type."""
    print(f"Valid data types: {', '.join(VALID_TYPES)}")
    while True:
        data_type = input("Enter data type: ").strip().lower()
        if data_type in VALID_TYPES:
            return data_type
        print(f"Invalid data type. Please choose from: {', '.join(VALID_TYPES)}")


def save_field(label: str, data_type: str) -> None:
    """Save field to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO fields (label, data_type) VALUES (?, ?)",
        (label, data_type)
    )
    conn.commit()
    conn.close()


def list_fields() -> None:
    """Print all fields from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT id, label, data_type FROM fields")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No fields found.")
        return

    print(f"{'ID':<6}{'Label':<20}{'Type':<10}")
    print("-" * 36)
    for row in rows:
        print(f"{row[0]:<6}{row[1]:<20}{row[2]:<10}")


def ask_continue() -> bool:
    """Ask user if they want to create another field."""
    while True:
        response = input("\nCreate another field? (y/n): ").strip().lower()
        if response == "y":
            return True
        if response == "n":
            return False
        print("Please enter 'y' or 'n'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create and manage data fields.")
    parser.add_argument("-l", "--list", action="store_true", help="List all fields")
    args = parser.parse_args()

    init_db()

    if args.list:
        list_fields()
        return

    print("=== Field Creator ===\n")

    while True:
        label = get_label()
        data_type = get_data_type()

        save_field(label, data_type)
        print(f"\nField saved: '{label}' ({data_type})")

        if not ask_continue():
            break


if __name__ == "__main__":
    main()
