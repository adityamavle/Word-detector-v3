import glob
import shutil
import os
import json
from PIL import Image
import hashlib
import argparse
import random
import math
parser = argparse.ArgumentParser()
"D:\consort_hard"

parser.add_argument("--pathd",
                    help="Path to Hard Consort data",
                    type=str, default="D:/consort_hard/Hard/images/")
parser.add_argument("--pathj",
                    help="Path to Hard Json",
                    type=str, default="D:/consort_hard/Hard/labels.json")
parser.add_argument("--paths",
                    help="Path to save files",
                    type=str, default="D:/consort_hard/Hard")
parser.add_argument("--region",
                    help="Region of interest (line or word)",
                    type=str, default='word')
parser.add_argument("--split",
                    help='train val test split percents',
                    nargs='+', type=float, default=[60, 20, 20])
args = parser.parse_args()


# extension of image to be considered
path_to_dataset = args.pathd
path_to_save = args.paths
path_to_json = args.pathj

# iou values to consider
# reg under consideration. Either word or line
regiondecision = args.region
split = args.split

with open(path_to_json, 'r') as file:
    data = json.load(file)

# makes the labels for training


def make_labels(impath, labels, i):
    img = Image.open(impath)

    # get width and height
    width = img.width
    height = img.height

    dimensions = img.size

    # display width and height
    # print("dimensions: ",dimensions)
    # print("The height of the image is: ", height)
    # print("The width of the image is: ", width)

    readable_hash = ""
    with open(impath, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
    test_img_path = os.path.basename(impath)
    labels[test_img_path] = {
        'img_dimensions': dimensions,
        'img_hash': readable_hash,
        'polygons': labels[test_img_path]['polygons']
    }


# f = open(path_to_json)
# all_recalls_docs = json.load(f)
# f.close()
# docs = [document_path for (recall,precision,document_path,polygons) in all_recalls_docs]
docs = list(data.keys())  # get names of hard docs in the dataset
print(docs[1])
print('making the files and folders...')
if os.path.isdir(path_to_save):
    shutil.rmtree(path_to_save)

os.mkdir(path_to_save + '/train')
os.mkdir(path_to_save + '/test')
os.mkdir(path_to_save + '/val')
os.mkdir(path_to_save + '/train/images')
os.mkdir(path_to_save + '/test/images')
os.mkdir(path_to_save + '/val/images')


cut_off_1 = 0.45
cut_off_2 = 0.63
# easylist = [item[2] for item in data if float(item[0]) > cut_off_2]
# mediumlist = [item[2] for item in data if float(
#     item[0]) > cut_off_1 and float(item[0]) <= cut_off_2]
hardlist = docs
random.shuffle(hardlist)

trainhard = hardlist[:math.floor(len(hardlist)*split[0]/100)]
val = hardlist[math.floor(len(hardlist)*split[0]/100)
                        :math.floor(len(hardlist)*(split[0]+split[1])/100)]
test = hardlist[math.floor(len(hardlist)*(split[0]+split[1])/100):]

print("starting obtaining all Hard docs")
labels = {}
for i, tiffile in enumerate(trainhard):
    shutil.copy(tiffile, path_to_save + '/Hard/train/images')
    make_labels(tiffile, labels, i)
outfile = open(path_to_save + '/Hard/train/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

labels = {}
for i, tiffile in enumerate(val):
    shutil.copy(tiffile, path_to_save + '/Hard/val/images')
    make_labels(tiffile, labels, i)
outfile = open(path_to_save + '/Hard/val/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

labels = {}
for i, tiffile in enumerate(test):
    shutil.copy(tiffile, path_to_save + '/Hard/test/images')
    make_labels(tiffile, labels, i)
outfile = open(path_to_save + '/Hard/test/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()
print('done!')
