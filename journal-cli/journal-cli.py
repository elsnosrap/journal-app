import argparse
from datetime import datetime
import os
import sqlite3
import subprocess
import tempfile

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".data")
DB_PATH = os.path.join(DATA_DIR, "data.db")
TABLE_NAME_DATA_TYPES = "data_types"
TABLE_NAME_USER_DATA = "user_data"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"

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
    conn.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME_USER_DATA} (
            key INTEGER PRIMARY KEY AUTOINCREMENT,
            data_type INTEGER NOT NULL REFERENCES {TABLE_NAME_DATA_TYPES}(key),
            created TEXT NOT NULL,
            int_value INTEGER,
            text_value TEXT
        )
    """)
    conn.commit()
    return conn


def get_data_type(default=None):
    valid_types = {"int", "boolean", "date", "text"}
    while True:
        default_hint = f" [{default}]" if default else ""
        data_type = input(f"Data type (int, boolean, date, text){default_hint}: ").strip().lower()
        if data_type == "" and default:
            return default
        if data_type in valid_types:
            return data_type
        print("Invalid data type. Please choose from: int, boolean, date, text")


def get_int_bound(bound_name, default=None):
    while True:
        default_hint = f" [{default}]" if default is not None else ""
        value = input(f"  {bound_name} value (leave blank for none){default_hint}: ").strip()
        if value == "" and default is not None:
            return default
        if value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("  Please enter a valid integer or leave blank.")


def configure(defaults=None):
    default_label = defaults["label"] if defaults else None
    default_data_type = defaults["data_type"] if defaults else None
    default_prompt = defaults["prompt"] if defaults else None
    default_min = defaults.get("min") if defaults else None
    default_max = defaults.get("max") if defaults else None

    label_hint = f" [{default_label}]" if default_label else ""
    label = input(f"Label{label_hint}: ").strip()
    if label == "" and default_label:
        label = default_label

    data_type = get_data_type(default=default_data_type)

    prompt_hint = f" [{default_prompt}]" if default_prompt else ""
    prompt = input(f"Prompt{prompt_hint}: ").strip()
    if prompt == "" and default_prompt:
        prompt = default_prompt

    min_val = None
    max_val = None
    if data_type == "int":
        min_val = get_int_bound("Minimum", default=default_min)
        max_val = get_int_bound("Maximum", default=default_max)

    return {
        "label": label,
        "data_type": data_type,
        "prompt": prompt,
        "min": min_val,
        "max": max_val,
    }


def create_data_type():
    config = configure()

    conn = init_db()
    conn.execute(
        f"INSERT INTO {TABLE_NAME_DATA_TYPES} (label, data_type, prompt, min_value, max_value) VALUES (?, ?, ?, ?, ?)",
        (config["label"], DATA_TYPE_MAP[config["data_type"]], config["prompt"], config["min"], config["max"]),
    )
    conn.commit()
    conn.close()

    print("\nConfiguration saved:")
    print(f"  Label: {config['label']}")
    print(f"  Data type: {config['data_type']} ({DATA_TYPE_MAP[config['data_type']]})")
    print(f"  Prompt: {config['prompt']}")
    if config["data_type"] == "int":
        print(f"  Min: {config['min']}")
        print(f"  Max: {config['max']}")


def edit_data_type(key):
    conn = init_db()
    row = conn.execute(
        f"SELECT key, label, data_type, prompt, min_value, max_value FROM {TABLE_NAME_DATA_TYPES} WHERE key = ?",
        (key,),
    ).fetchone()

    if not row:
        conn.close()
        print(f"No data type found with key {key}.")
        return

    _, label, data_type_int, prompt, min_val, max_val = row
    data_type_name = DATA_TYPE_REVERSE_MAP.get(data_type_int, "unknown")

    defaults = {
        "label": label,
        "data_type": data_type_name,
        "prompt": prompt,
        "min": min_val,
        "max": max_val,
    }

    config = configure(defaults=defaults)

    conn.execute(
        f"UPDATE {TABLE_NAME_DATA_TYPES} SET label = ?, data_type = ?, prompt = ?, min_value = ?, max_value = ? WHERE key = ?",
        (config["label"], DATA_TYPE_MAP[config["data_type"]], config["prompt"], config["min"], config["max"], key),
    )
    conn.commit()
    conn.close()

    print("\nConfiguration updated:")
    print(f"  Label: {config['label']}")
    print(f"  Data type: {config['data_type']} ({DATA_TYPE_MAP[config['data_type']]})")
    print(f"  Prompt: {config['prompt']}")
    if config["data_type"] == "int":
        print(f"  Min: {config['min']}")
        print(f"  Max: {config['max']}")


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


def collect_data():
    conn = init_db()
    rows = conn.execute(
        f"SELECT key, label, data_type, prompt, min_value, max_value FROM {TABLE_NAME_DATA_TYPES}"
    ).fetchall()

    if not rows:
        print("No data types configured. Run with --config to add one.")
        conn.close()
        return

    for row in rows:
        dt_key, label, data_type, prompt_text, min_val, max_val = row

        print(label)

        if data_type == DATA_TYPE_INT:
            range_hint = ""
            if min_val is not None and max_val is not None:
                range_hint = f" ({min_val}-{max_val})"
            while True:
                response = input(f"{prompt_text}{range_hint}: ").strip()
                try:
                    int_val = int(response)
                except ValueError:
                    print("Please enter a valid integer.")
                    continue
                if min_val is not None and int_val < min_val:
                    print(f"Value must be at least {min_val}.")
                    continue
                if max_val is not None and int_val > max_val:
                    print(f"Value must be at most {max_val}.")
                    continue
                conn.execute(
                    f"INSERT INTO {TABLE_NAME_USER_DATA} (data_type, int_value, created) VALUES (?, ?, ?)",
                    (dt_key, int_val, datetime.now().strftime(DATETIME_FORMAT)),
                )
                conn.commit()
                break

        elif data_type == DATA_TYPE_TEXT:
            response = input(f"{prompt_text} (Y/n): ").strip()
            if response == "" or response == "Y":
                fd, tmp_path = tempfile.mkstemp(suffix=".txt")
                os.close(fd)
                result = subprocess.run(["vim", tmp_path])
                if result.returncode == 0:
                    with open(tmp_path, "r") as f:
                        text_val = f.read().strip()
                    conn.execute(
                        f"INSERT INTO {TABLE_NAME_USER_DATA} (data_type, text_value, created) VALUES (?, ?, ?)",
                        (dt_key, text_val, datetime.now().strftime(DATETIME_FORMAT)),
                    )
                    conn.commit()
                else:
                    print("Vim exited with an error. Skipping.")
                os.unlink(tmp_path)

        print()

    conn.close()


def list_user_data():
    conn = init_db()
    rows = conn.execute(
        f"""SELECT u.key, u.data_type, u.created, u.int_value, u.text_value, d.label
            FROM {TABLE_NAME_USER_DATA} u
            JOIN {TABLE_NAME_DATA_TYPES} d ON u.data_type = d.key"""
    ).fetchall()
    conn.close()

    if not rows:
        print("No user data recorded.")
        return

    for row in rows:
        key, dt_key, created, int_value, text_value, label = row
        print(f"[{key}]")
        print(f"  Label: {label}")
        print(f"  Created: {created}")
        print(f"  Int value: {int_value}")
        print(f"  Text value: {text_value}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Journal CLI")
    parser.add_argument("--config", action="store_true", help="Configure a journal field")
    parser.add_argument("--list-data-types", action="store_true", help="List configured data types")
    parser.add_argument("--edit-data-type", type=int, metavar="KEY", help="Edit a data type by its key")
    parser.add_argument("--list-user-data", action="store_true", help="List all user data")
    args = parser.parse_args()

    if args.config:
        create_data_type()
    elif args.edit_data_type is not None:
        edit_data_type(args.edit_data_type)
    elif args.list_data_types:
        list_data_types()
    elif args.list_user_data:
        list_user_data()
    else:
        collect_data()


if __name__ == "__main__":
    main()
