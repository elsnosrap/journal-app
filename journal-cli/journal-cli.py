import argparse
import os
import sqlite3

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".data")
DB_PATH = os.path.join(DATA_DIR, "data.db")
TABLE_NAME_DATA_TYPES = "data_types"

DATA_TYPE_INT = 1
DATA_TYPE_BOOLEAN = 2
DATA_TYPE_DATE = 3
DATA_TYPE_TEXT = 4

DATA_TYPE_MAP = {
    "int": DATA_TYPE_INT,
    "boolean": DATA_TYPE_BOOLEAN,
    "date": DATA_TYPE_DATE,
    "text": DATA_TYPE_TEXT,
}


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME_DATA_TYPES} (
            key INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            data_type INTEGER NOT NULL,
            prompt TEXT NOT NULL,
            min_value INTEGER,
            max_value INTEGER
        )
    """)
    conn.commit()
    return conn


def get_data_type():
    valid_types = {"int", "boolean", "date", "text"}
    while True:
        data_type = input("Data type (int, boolean, date, text): ").strip().lower()
        if data_type in valid_types:
            return data_type
        print("Invalid data type. Please choose from: int, boolean, date, text")


def get_int_bound(bound_name):
    while True:
        value = input(f"  {bound_name} value (leave blank for none): ").strip()
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("  Please enter a valid integer or leave blank.")


def configure():
    label = input("Label: ").strip()
    data_type = get_data_type()
    prompt = input("Prompt: ").strip()

    min_val = None
    max_val = None
    if data_type == "int":
        min_val = get_int_bound("Minimum")
        max_val = get_int_bound("Maximum")

    conn = init_db()
    conn.execute(
        f"INSERT INTO {TABLE_NAME_DATA_TYPES} (label, data_type, prompt, min_value, max_value) VALUES (?, ?, ?, ?, ?)",
        (label, DATA_TYPE_MAP[data_type], prompt, min_val, max_val),
    )
    conn.commit()
    conn.close()

    print("\nConfiguration saved:")
    print(f"  Label: {label}")
    print(f"  Data type: {data_type} ({DATA_TYPE_MAP[data_type]})")
    print(f"  Prompt: {prompt}")
    if data_type == "int":
        print(f"  Min: {min_val}")
        print(f"  Max: {max_val}")


DATA_TYPE_REVERSE_MAP = {v: k for k, v in DATA_TYPE_MAP.items()}


def list_data_types():
    conn = init_db()
    rows = conn.execute(f"SELECT key, label, data_type, prompt, min_value, max_value FROM {TABLE_NAME_DATA_TYPES}").fetchall()
    conn.close()

    if not rows:
        print("No data types configured.")
        return

    for row in rows:
        key, label, data_type, prompt, min_val, max_val = row
        type_name = DATA_TYPE_REVERSE_MAP.get(data_type, "unknown")
        print(f"[{key}]")
        print(f"  Label: {label}")
        print(f"  Data type: {type_name} ({data_type})")
        print(f"  Prompt: {prompt}")
        if data_type == DATA_TYPE_INT:
            print(f"  Min: {min_val}")
            print(f"  Max: {max_val}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Journal CLI")
    parser.add_argument("--config", action="store_true", help="Configure a journal field")
    parser.add_argument("--list-data-types", action="store_true", help="List configured data types")
    args = parser.parse_args()

    if args.config:
        configure()
    elif args.list_data_types:
        list_data_types()
    else:
        print("Coming Soon!")


if __name__ == "__main__":
    main()
