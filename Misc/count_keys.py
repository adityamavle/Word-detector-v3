import json
import sys


def count_json_keys(file_path):
    # Load JSON from file
    with open(file_path, 'r') as f:
        json_obj = json.load(f)

    # Print keys
    keys = json_obj.keys()
    print("Keys:")
    for key in keys:
        print(key)

    # Count total number of keys
    num_keys = len(keys)
    print("Total number of keys:", num_keys)


# Command-line usage: python script.py path/to/json_file.json
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the JSON file as a command-line argument.")
        sys.exit(1)

    file_path = sys.argv[1]
    count_json_keys(file_path)
