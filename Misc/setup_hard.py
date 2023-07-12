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

parser.add_argument("--pathd",
                    help="Path to dataset",
                    type=str, default="/home/ndli19/docvisor/Consortium_dataset/")
parser.add_argument("--pathj",
                    help="Path to json",
                    type=str, default="/home/ndli19/docvisor/reclists/reclistsimage_recall_list_finetuned_db_resnet50.json")  # to be copied
parser.add_argument("--paths",
                    help="Path to save files",
                    type=str, default="/home/ndli19/docvisor/Consort_Hard/Hard_all")
parser.add_argument("--pathg",
                    help="Path to ground truth",
                    type=str, default="/home/ndli19/docvisor/docvisor_consortium_gt/Filtered_GT/")
parser.add_argument("--ext",
                    help="Extension of files to be considered (supports one at this moment)",
                    type=str, default='tif')
parser.add_argument("--cutoffs",
                    help='list of two cutoffs for dividing into easy, medium, hard',
                    nargs='+', type=float, default=[10, 40])
parser.add_argument("--languages",
                    help='list of languages in dataset/to be used in current run',
                    nargs='+', type=str, default=["Assamese", "Bangla", "Gujarati", "Gurumukhi", "Hindi", "Kannada", "Malayalam", "Manipuri", "Marathi", "Oriya", "Tamil", "Telugu", "Urdu"])
parser.add_argument("--region",
                    help="Region of interest (line or word)",
                    type=str, default='word')
parser.add_argument("--split",
                    help='train val test split percents',
                    nargs='+', type=float, default=[60, 20, 20])
args = parser.parse_args()


# extension of image to be considered
ext = args.ext
# paths to different folders
path_to_dataset = args.pathd
path_to_json = args.pathj
path_to_groundtruth = args.pathg
path_to_save = args.paths
# iou values to consider
cutoffs = args.cutoffs
# languages under consideration for current run
languages = args.languages
# reg under consideration. Either word or line
regiondecision = args.region
split = args.split

# loading all ground truths for languages
print('Loading ground truths....')
data = {}
for language in languages:
    path_to_ground = path_to_groundtruth+language + "_filtered" + ".json"
    f = open(path_to_ground)
    data[language] = json.load(f)

# makes the labels for training


def make_labels(impath, labels, i):
    img = Image.open(impath)

    # get width and height
    width = img.width
    height = img.height

    dimensions = img.size
    readable_hash = ""
    with open(impath, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        readable_hash = hashlib.sha256(bytes).hexdigest()
    test_img_path = os.path.basename(impath)
    labels[test_img_path] = {
        'img_dimensions': dimensions,
        'img_hash': readable_hash,
        'polygons': data[i][3]
    }


f = open(path_to_json)
all_recalls_docs = json.load(f)
f.close()
# docs = [document_path for (recall,precision,document_path,polygons) in all_recalls_docs]
docs = [element[2] for element in all_recalls_docs]
print(docs[1])
print('making the files and folders...')
if os.path.isdir(path_to_save):
    shutil.rmtree(path_to_save)

os.mkdir(path_to_save)
os.mkdir(path_to_save + '/train/')
os.mkdir(path_to_save + '/val/')
os.mkdir(path_to_save + '/val/images')
os.mkdir(path_to_save + '/test/')
os.mkdir(path_to_save + '/test/images')
os.mkdir(path_to_save + '/train/Easy/')
os.mkdir(path_to_save + '/train/Medium/')
os.mkdir(path_to_save + '/train/Hard/')
os.mkdir(path_to_save + '/train/Easy/images')
os.mkdir(path_to_save + '/train/Medium/images')
os.mkdir(path_to_save + '/train/Hard/images')

cut_off_1 = 0.1
cut_off_2 = 0.4
easylist = [item[2] for item in data if float(item[0]) > cut_off_2]
mediumlist = [item[2] for item in data if float(
    item[0]) > cut_off_1 and float(item[0]) <= cut_off_2]
hardlist = [item[2] for item in data if float(item[0]) <= cut_off_1]

random.shuffle(easylist)
random.shuffle(mediumlist)
random.shuffle(hardlist)

traineasy = easylist[:math.floor(len(easylist)*split[0]/100)]
val = easylist[math.floor(len(easylist)*split[0]/100)               :math.floor(len(easylist)*(split[0]+split[1])/100)]
test = easylist[math.floor(len(easylist)*(split[0]+split[1])/100):]

trainmedium = mediumlist[:math.floor(len(mediumlist)*split[0]/100)]
val = val + mediumlist[math.floor(len(mediumlist)*split[0]/100)                       :math.floor(len(mediumlist)*(split[0]+split[1])/100)]
test = test + mediumlist[math.floor(len(mediumlist)*(split[0]+split[1])/100):]

trainhard = hardlist[:math.floor(len(hardlist)*split[0]/100)]
val = val + hardlist[math.floor(len(hardlist)*split[0]/100)                     :math.floor(len(hardlist)*(split[0]+split[1])/100)]
test = test + hardlist[math.floor(len(hardlist)*(split[0]+split[1])/100):]

print("starting train hard")
labels = {}
for i, tiffile in enumerate(trainhard):
    shutil.copy(tiffile, path_to_save + '/train/Hard/images')
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/train/Hard/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

print("starting train medium")
labels = {}
for i, tiffile in enumerate(trainmedium):
    shutil.copy(tiffile, path_to_save + '/train/Medium/images')
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/train/Medium/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

print("starting train easy")
labels = {}
for i, tiffile in enumerate(traineasy):
    shutil.copy(tiffile, path_to_save + '/train/Easy/images')
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/train/Easy/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

print("starting val")
labels = {}
for i, tiffile in enumerate(val):
    shutil.copy(tiffile, path_to_save + '/val/images')
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/val/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

print("starting test")
labels = {}
for i, tiffile in enumerate(test):
    shutil.copy(tiffile, path_to_save + '/test/images')
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/test/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()
print('done!')
