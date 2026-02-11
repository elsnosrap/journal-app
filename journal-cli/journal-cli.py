import argparse


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

    config = {
        "label": label,
        "data_type": data_type,
        "prompt": prompt,
    }

    if data_type == "int":
        min_val = get_int_bound("Minimum")
        max_val = get_int_bound("Maximum")
        config["min"] = min_val
        config["max"] = max_val

    print("\nConfiguration:")
    print(f"  Label: {config['label']}")
    print(f"  Data type: {config['data_type']}")
    print(f"  Prompt: {config['prompt']}")
    if data_type == "int":
        print(f"  Min: {config['min']}")
        print(f"  Max: {config['max']}")


def main():
    parser = argparse.ArgumentParser(description="Journal CLI")
    parser.add_argument("--config", action="store_true", help="Configure a journal field")
    args = parser.parse_args()

    if args.config:
        configure()
    else:
        print("Coming Soon!")


if __name__ == "__main__":
    main()
