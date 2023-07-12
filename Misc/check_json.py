import json


# def check_json(input_json_path):
#     with open(input_json_path, 'r') as f:
#         json_data = json.load(f)
#     converted_data = {}
#     for image_name, image_data in json_data.items():
#         converted_polygons = []
#         print(type(image_data['polygons']))
#         print(image_data[:,:4])


# for boxes_pred in loc_preds:
#     # Convert pred to boxes [xmin, ymin, xmax, ymax]  N, 4, 2 --> N, 4
#     # boxes_pred = np.concatenate((boxes_pred.min(axis=1), boxes_pred.max(axis=1)), axis=-1)
#     val_metric.update(gts=boxes_gt, preds=boxes_pred[:, :4])

def check_json(input_path):
    with open(input_path, 'r') as f:
        json_data = json.load(f)
    print(len(json_data))
check_json('data/test/labels.json')
