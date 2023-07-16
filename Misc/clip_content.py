import os
import shutil
import json

# def copy_images(image_basenames, source_dir, destination_dir):
#     for basename in image_basenames:
#         source_path = os.path.join(source_dir, basename)
#         destination_path = os.path.join(destination_dir, basename)
#         shutil.copy2(source_path, destination_path)  # copy2 p
#         # preserves file metadata


def move_images(image_basenames, source_dir, destination_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            if filename not in image_basenames:
                source_path = os.path.join(source_dir, filename)
                destination_path = os.path.join(destination_dir, filename)
                shutil.move(source_path, destination_path)


def clip_json(image_basenames, json_file):
    for image_name in image_basenames:
        if image_name in json_file:
            del json_file[image_name]
    return json_file


image_nan = ['150_22.jpg', '150_30.jpg', '150_41.jpg', '7_32.png', '7_44.png']
inference_list = ['30_8.png', '30_13.png', '71_5.jpg', '71_20.jpg',
                  '71_22.jpg', '83_1.jpg', '83_13.jpg', '106_3.jpg', '106_10.jpg',
                  '106_14.jpg', '106_35.jpg', '106_43.jpg', '107_5.jpg', '109_3.png', '109_10.png', '109_21.png', '109_26.png',
                  '109_33.png', '117_17.jpg', '117_19.jpg', '117_23.jpg', '145_1.jpg', '145_3.jpg', '145_43.jpg', '146_3.jpg', '146_23.jpg', '146_40.jpg', '150_8.jpg', '150_10.jpg', '151_3.jpg', '151_43.jpg', '152_3.jpg', '152_27.jpg', '152_31.jpg', '152_33.jpg', '153_3.jpg', '153_10.jpg', '153_22.jpg', '153_23.jpg', '153_27.jpg', '155_3.jpg', '155_9.jpg', '155_25.jpg', '156_3.jpg', '156_18.jpg', '156_25.jpg', '157_2.jpg', '157_3.jpg', '161_3.jpg', '161_10.jpg', '163_3.jpg', '164_3.jpg', '165_3.jpg', '166_3.jpg', '166_37.jpg', '168_11.jpg', '173_3.jpg',
                  ]
# move_images(inference_list, r'C:\Users\adity\docTR-v3-finetune\merged_newdata',
#             r'D:\Robust-Detector-Dataset-Prep\clipped_new_data')

print(len(inference_list))
input_file_path = r'C:\Users\adity\docTR-v3-finetune\jsons\clipped_newdata.json'
output_file_path = r'C:\Users\adity\docTR-v3-finetune\jsons\clipped_newdata.json'
with open(input_file_path, 'r') as json_file:
    json_file = json.load(json_file)

data = clip_json(image_nan, json_file)

# print(len(data))

with open(output_file_path, 'w') as json_file:
    json.dump(data, json_file, indent=6)
print(data['106_1.jpg'])
print(len(data)) #should be 1715


def remove_matching_lists(list_of_lists, image_names):
    # Create a new list to store the filtered result
    filtered_list = []

    # Iterate over each list in the list of lists
    for lst in list_of_lists:
        # Check if the second element of the list matches any image name
        if lst[2] not in image_names:
            # If it doesn't match, add the list to the filtered list
            filtered_list.append(lst)

    return filtered_list


def check_json(image_dir_path, json_path):
    image_names = os.listdir(image_dir_path)
    with open(json_path, 'r') as json_file:
        json_data = json.load(json_file)
    missing_keys = [key for key in json_data.keys() if key not in image_names]

    return missing_keys


# with open(input_file_path, 'r') as json_file:
#     list_of_lists = json.load(json_file)

# data = clip_json(inference_list, json_file)
# with open(output_file_path, 'w') as json_file:
#     json.dump(data, json_file, indent=6)
# data = remove_matching_lists(list_of_lists, inference_list)

# with open(output_file_path, 'w') as json_file:
#     json.dump(data, json_file, indent=6)

image_file_path = r'D:\Robust-Detector-Dataset-Prep\clipped_new_data'
json_path = r'C:\Users\adity\docTR-v3-finetune\jsons\clipped_newdata.json'

print(check_json(image_file_path, json_path))
