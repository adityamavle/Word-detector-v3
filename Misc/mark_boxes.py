import cv2
import json
import os

json_file = 'jsons/merged_outputs.json'
image_folder = 'merged_newdata/146_1.jpg'

with open(json_file, 'r') as f:
    data = json.load(f)

numbered_boxes_json = {}


def create_boxes(image_path, json_file):
    """
    Creates OCR detected bounding boxes on the image
    """
    numbered_polygons = {}
    image_name = os.path.basename(image_path)
    preds = json_file[image_name]['polygons']
    img = cv2.imread(image_path)
    image = img.copy()
    for i, bbox in enumerate(preds):
        x_min, y_min, x_max, y_max = bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]
        cv2.rectangle(image, (x_min, y_min), (x_max, y_max),
                      (0, 255, 0), thickness=6)
        cv2.putText(image, str(i), (x_min, y_min-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), thickness=2)
        print(json_file[image_name]['polygons'])
    numbered_polygons[image_name] = {
        'img_dimensions': json_file[image_name]['img_dimensions'],
        'img_hash': json_file[image_name]['img_hash'],
        'polygons': json_file[image_name]['polygons']
    }
    cv2.imwrite(f"output.png", image)
    return image


# with open(json_file, 'r') as f:
#     data = json.load(f)
# output_directory = r'D:\Robust-Detector-Dataset-Prep\test_images'
# for file_name in os.listdir(image_folder):
#     if file_name.endswith(('.jpg', '.png', '.jpeg')):
#         image_path = os.path.join(image_folder, file_name)
#         op_db = create_boxes(image_path, data)
#         # Save the output image
#         output_path = os.path.join(output_directory, file_name)
#         cv2.imwrite(output_path, op_db)
create_boxes(image_folder, data)
