import cv2
from doctr.io import DocumentFile
from collections import OrderedDict
from doctr.models import ocr_predictor
import matplotlib.pyplot as plt
import os
import torch
import numpy as np
import json
# Let's pick the desired backend
# os.environ['USE_TF'] = '1'
os.environ['USE_TORCH'] = '1'


def ocr_model_loader(model_path):
    """
    Load the model trained using dataparallel
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    predictor = ocr_predictor(pretrained=True).to(device)
    # original saved file with DataParallel
    state_dict = torch.load(model_path)

    print(type(state_dict.keys()))
    # COMMENT THE BELOW LINES OF CODE IF DataParallel was not used during training (provided weights used DataParallel)
    # create new OrderedDict that does not contain `module.`

    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]  # remove `module. in variable state dict nomenclature`
        new_state_dict[name] = v
    predictor.det_predictor.model.load_state_dict(new_state_dict)
    return predictor


def doctr_predictions(directory, predictor):
    """
    Input image directory and get ocr results with output as detection bounding box coordinates and the regions(=words)
    returns abs_coords(preds) and regions
    """
    # Gets the predictions from the model

    doc = DocumentFile.from_images(directory)
    result = predictor(doc)
    dic = result.export()

    page_dims = [page['dimensions'] for page in dic['pages']]

    regions = []
    abs_coords = []

    regions = [[word for block in page['blocks'] for line in block['lines']
                for word in line['words']] for page in dic['pages']]
    # a document is divided into a single region
    print('Number of Regions/words Detected', np.array(regions).shape[1])
    abs_coords = [
        [[int(round(word['geometry'][0][0] * dims[1])),  # get xmin xmax ymin y max
          int(round(word['geometry'][0][1] * dims[0])),
          int(round(word['geometry'][1][0] * dims[1])),
          int(round(word['geometry'][1][1] * dims[0]))] for word in words]
        for words, dims in zip(regions, page_dims)]

#     pred = torch.Tensor(abs_coords[0])
    return abs_coords, regions


def create_boxes(img_file, output_dir, preds):
    """
    Creates OCR detected bounding boxes on the image
    """
    # for img_file in os.listdir(image_dir):
    img = cv2.imread(img_file)
    img_name = os.path.basename(img_file)
    image = img.copy()
    for i, w in enumerate(preds[0]):  # this goes in place of enum(preds)
        cv2.rectangle(image, (w[0], w[1]), (w[2], w[3]),
                      (0, 255, 0), thickness=2)
        cv2.putText(image, str(i), (w[0], w[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=1)
    output_path = os.path.join(output_dir, img_name)
    cv2.imwrite(output_path, image)


if __name__ == "__main__":
    # img_dir = r"D:\Robust-Detector-Dataset-Prep\correct_bboxes"
    img_dir = '/content/marathi'
    predictor = ocr_model_loader('./db_resnet50.pt')
    image_preds = {}
    for image_name in os.listdir(img_dir):
        image_path = os.path.join(img_dir, image_name)
        print(image_path)
        preds, results = doctr_predictions(image_path, predictor)
        image_preds[image_name] = {
            'polygons': preds[0]
        }
        create_boxes(image_path, '/content/output', preds)
    with open('inference_output.json', 'w') as f:
        json.dump(image_preds, f, indent=6)
