import os
import json

def create_labels_json(image_folder, labels_json_path, output_folder):
    # Load the existing labels.json
    with open(labels_json_path, 'r') as f:
        labels = json.load(f)

    # Create a new dictionary to store aggregated image data
    aggregated_data = {}

    # Iterate over the image folder
    for root, _, files in os.walk(image_folder):
        for file in files:
            image_path = os.path.join(root, file)
            image_name = os.path.splitext(file)[0]

            if image_name in labels:
                image_data = labels[image_name]
                aggregated_data[image_name] = image_data
            else:
                print(f"No label found for image: {image_name}")

    # Write the aggregated data to a new labels.json file
    output_path = os.path.join(output_folder, 'labels.json')
    with open(output_path, 'w') as f:
        json.dump(aggregated_data, f, indent=4)


train_folder = '/home/ndli19/docvisor/consort_hard/train/images'
test_folder = '/home/ndli19/docvisor/consort_hard/test/images'
val_folder = '/home/ndli19/docvisor/consort_hard/val/images'
labels_json_path = '/home/ndli19/docvisor/consort_hard/Hard/labels.json'
train_output_folder = '/home/ndli19/docvisor/consort_hard/train/'
test_output_folder = '/home/ndli19/docvisor/consort_hard/test/'
val_output_folder = '/home/ndli19/docvisor/consort_hard/val/'


create_labels_json(train_folder, labels_json_path, train_output_folder)
create_labels_json(test_folder, labels_json_path, test_output_folder)
create_labels_json(val_folder, labels_json_path, val_output_folder)


