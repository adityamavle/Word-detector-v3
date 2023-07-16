import json


# def convert_bbox_format(json_data):
#     converted_data = {}
#     for image_name, image_data in json_data.items():
#         converted_polygons = []
#         for word in details['words']:
#             # Retrieve the ground truth coordinates
#         gt = word['groundTruth']
#         xmin, ymin, xmax, ymax = gt
#         polygon = [[x_min, y_max], [x_min, y_min],
#                    [x_max, y_min], [x_max, y_max]]
#         converted_polygons.append(polygon)
#         converted_data[image_name] = {
#             'img_dimensions': image_data['img_dimensions'],
#             'img_hash': image_data['img_hash'],
#             'polygons': converted_polygons
#         }
#     return converted_data


# # Load the original JSON data
# with open(r'jsons\merged_newdata_json.json', 'r') as f:
#     json_data = json.load(f)

# # Convert the bounding box formatṇ
# converted_data = convert_bbox_format(json_data)

# # Save the converted data to a new JSON file
# with open('jsons/merged_polygons_new_data.json', 'w') as f:
#     json.dump(converted_data, f, indent=6)

# print('Done converting')
# with open(r'jsons\merged_newdata_json.json', 'r') as f:
#     json_data = json.load(f)

# print(type(json_data.items()))

# c = 0
# converted_json = {}
# for image_name, image_data in json_data.items():
    
#     converted_polygons = []
#     # print('Image data ', image_data)
#     for bbox in image_data['words']:
#         [x_min,y_min,x_max,y_max] = bbox['groundTruth']
#         polygon = [[x_min, y_min], [x_min, y_max],[x_max, y_max], [x_max, y_min]]
#         converted_polygons.append(polygon)
#     json_data[image_name] = {
#         'polygons' : converted_polygons
#     }
# print(len(json_data))
with open('jsons/merged_outputs.json', 'r') as f:
    json_data = json.load(f)

c=0
for image_name, image_data in json_data.items():
    print((json_data[image_name]['polygons'][0]))
    print((json_data[image_name]['polygons'][0][2]))
    print((json_data[image_name]['polygons'][0][2][0]))
    c+=1
    if(c==2):
        break 
# pr
# int(len(json_data))

