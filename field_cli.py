#!/usr/bin/env python3
"""CLI for creating data fields with labels and types."""

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


def main() -> None:
    init_db()
    print("=== Field Creator ===\n")

    label = get_label()
    data_type = get_data_type()

    save_field(label, data_type)
    print(f"\nField saved: '{label}' ({data_type})")


if __name__ == "__main__":
    main()
