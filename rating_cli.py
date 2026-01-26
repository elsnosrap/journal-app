#!/usr/bin/env python3
"""A simple CLI that asks for a user rating from 1 to 10."""

from datetime import datetime
from pathlib import Path


def get_rating() -> int | None:
    """Prompt the user for a rating between 1 and 10, or 0 to exit."""
    while True:
        try:
            rating = int(input("Please enter your rating (1-10, or 0 to exit): "))
            if rating == 0:
                return None
            if 1 <= rating <= 10:
                return rating
            print("Rating must be between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def save_rating(rating: int) -> str:
    """Save the rating to a timestamped file in the .data directory."""
    data_dir = Path(".data")
    data_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filepath = data_dir / f"rating_{timestamp}.txt"
    filepath.write_text(str(rating))
    return str(filepath)


def main() -> None:
    """Main entry point."""
    print("Welcome to the Rating CLI!")
    rating = get_rating()
    if rating is None:
        print("Goodbye!")
        return
    filename = save_rating(rating)
    print(f"You rated: {rating}/10")
    print(f"Rating saved to {filename}")


if __name__ == "__main__":
    main()
