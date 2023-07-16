import json
import os
import sys


def count_json_keys(file_path, image_folder):
    # Load JSON from file
    with open(file_path, 'r') as f:
        json_obj = json.load(f)

    # Print keys
    keys = json_obj.keys()
    print("Keys:")
    # for key in keys:
    #     print(key)

    # Count total number of keys
    num_keys = len(keys)
    print("Total number of keys:", num_keys)

    # Check if all keys are present as images in the folder
    image_files = os.listdir(image_folder)
    missing_keys = set(
        keys) - set([os.path.basename(filename) for filename in image_files])
    if missing_keys:
        print("Keys missing as image files:")
        for key in missing_keys:
            print(key)
    else:
        print('Verified images and jsons,no keys missing!')


# Command-line usage: python script.py path/to/json_file.json path/to/image_folder
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide the path to the JSON file and the image folder as command-line arguments.")
        sys.exit(1)

    file_path = sys.argv[1]
    image_folder = sys.argv[2]
    count_json_keys(file_path, image_folder)
