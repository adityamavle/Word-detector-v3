import cv2
import json
import os

json_file = 'jsons\merged_outputs.json'
image_folder = 'merged_newdata'


def create_boxes(image_path, json_file):
    """
    Creates OCR detected bounding boxes on the image
    """
    image_name = os.path.basename(image_path)
    preds = json_file[image_name]['polygons']
    img = cv2.imread(image_path)
    image = img.copy()
    for w in preds:
        cv2.rectangle(image, (w[0][0], w[0][1]),
                      (w[2][0], w[2][1]), (0, 255, 0), thickness=6) #parsing like this because input json is in top_left,bottom_left,bottom_right,top_right format
    cv2.imwrite(f"output.png", image)
    return image


with open(json_file, 'r') as f:
    data = json.load(f)
output_directory = r'D:\Robust-Detector-Dataset-Prep\test_images'
for file_name in os.listdir(image_folder):
    if file_name.endswith(('.jpg', '.png', '.jpeg')):
        image_path = os.path.join(image_folder, file_name)
        op_db = create_boxes(image_path, data)
        # Save the output image
        output_path = os.path.join(output_directory, file_name)
        cv2.imwrite(output_path, op_db)
