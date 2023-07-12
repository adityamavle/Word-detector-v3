import json


def convert_bbox_format(json_data):
    converted_data = {}
    for image_name, image_data in json_data.items():
        converted_polygons = []
        for bbox in image_data['polygons']:
            x_min, y_min, x_max, y_max = map(int, bbox)
            polygon = [[x_min, y_max], [x_min, y_min],
                       [x_max, y_min], [x_max, y_max]]
            converted_polygons.append(polygon)
        converted_data[image_name] = {
            'img_dimensions': image_data['img_dimensions'],
            'img_hash': image_data['img_hash'],
            'polygons': converted_polygons
        }
    return converted_data


# Load the original JSON data
with open(r'data\val\labels.json', 'r') as f:
    json_data = json.load(f)

# Convert the bounding box format
converted_data = convert_bbox_format(json_data)

# Save the converted data to a new JSON file
with open('data/val/labels_1.json', 'w') as f:
    json.dump(converted_data, f, indent=6)

print('Done converting')
