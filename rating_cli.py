#!/usr/bin/env python3
"""A simple CLI that asks for a user rating from 1 to 10."""

from datetime import datetime


def get_rating() -> int:
    """Prompt the user for a rating between 1 and 10."""
    while True:
        try:
            rating = int(input("Please enter your rating (1-10): "))
            if 1 <= rating <= 10:
                return rating
            print("Rating must be between 1 and 10.")
        except ValueError:
            print("Please enter a valid number.")


def save_rating(rating: int) -> str:
    """Save the rating to a timestamped file."""
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M")
    filename = f"rating_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(str(rating))
    return filename


def main() -> None:
    """Main entry point."""
    print("Welcome to the Rating CLI!")
    rating = get_rating()
    filename = save_rating(rating)
    print(f"You rated: {rating}/10")
    print(f"Rating saved to {filename}")


if __name__ == "__main__":
    main()
