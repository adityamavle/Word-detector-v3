import json
import os


input_json_path = "data/val/labels.json"
output_json_path = "data/val/labels_2.json"


def rearrange_json(input_json_path, output_json_path):
    with open(input_json_path, 'r') as f:
        json_data = json.load(f)
    converted_data = {}
    for image_name, image_data in json_data.items():
        converted_polygons = []
        print('New Image Data')
        for bbox in image_data['polygons']:
            bbox[0], bbox[1] = bbox[1], bbox[0]
            bbox[2], bbox[3] = bbox[3], bbox[2]
        converted_data[image_name] = {
            'img_dimensions': image_data['img_dimensions'],
            'img_hash': image_data['img_hash'],
            'polygons': image_data['polygons']
        }
    with open(output_json_path, 'w') as f:
        json.dump(converted_data, f, indent=6)

rearrange_json(input_json_path, output_json_path)
