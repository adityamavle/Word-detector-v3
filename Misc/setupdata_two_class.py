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
                    type=str, default="D:\Robust-Detector-Dataset-Prep\clipped_new_data")
parser.add_argument("--pathr",
                    help="Path to recall json",
                    type=str, default="./jsons/clipped_recall_list.json")
parser.add_argument("--pathj",
                    help="Path to gt json",
                    type=str, default="./jsons/clipped_newdata.json")
parser.add_argument("--paths",
                    help="Path to save files",
                    type=str, default=r"D:\Robust-Detector-Dataset-Prep\test_setup")
# ground truth's are in the merged newdata.json
# as well as recallistsimage_recall_list #not using the original structure of 'GT/docvisor_consortium_gt/Assamese.json' that is language wise
parser.add_argument("--ext",
                    help="Extension of files to be considered (supports one at this moment)",
                    type=str, default='png')
parser.add_argument("--cutoffs",
                    help='list of two cutoffs for dividing into easy and hard',
                    nargs='+', type=float, default=[10, 40])  # cutoff scores to divide the 3 categories
# parser.add_argument("--languages",
#                     help='list of languages in dataset/to be used in current run',
#                     nargs='+', type=str, default=["Assamese", "Bangla", "Gujarati", "Gurumukhi", "Hindi", "Kannada", "Malayalam", "Manipuri", "Marathi", "Oriya", "Tamil", "Telugu", "Urdu"])
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
path_to_recall_json = args.pathr

# path_to_groundtruth = args.pathg
path_to_save = args.paths
# iou values to consider
cutoffs = args.cutoffs
# languages under consideration for current run
# languages = args.languages
# reg under consideration. Either word or line
regiondecision = args.region
split = args.split
# loading all ground truths for languages
print('Loading ground truths....')
data = {}
# for language in languages:
#     path_to_groundtruth = "GT/docvisor_consortium_gt/"+language + ".json"
#     f = open(path_to_groundtruth)
#     data[language] = json.load(f)
with open(path_to_json, 'r') as file:
    data = json.load(file)  # will give a list of list
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
        # print(type(readable_hash))

    # ans_key = ""

    test_img_path = os.path.basename(impath)

    # for language in languages:
    #     image_keys = list(data[language].keys())
    #     for k in image_keys:
    #         path = os.path.basename(data[language][k]["imagePath"])
    #         if path == test_img_path:
    #             ans_key = k
    #             break

    #     if ans_key != "":
    #         break

    # if ans_key == "":
    #     print('something is wrong1')

    # regions = []
    # for i, region in enumerate(data[language][ans_key]["regions"]):
    #     if region["regionLabel"] == regiondecision:
    #         regions.append(region["groundTruth"])
    # print(regions)
    labels[test_img_path] = {
        'img_dimensions': dimensions,
        'img_hash': readable_hash,
        'polygons': data[test_img_path]['polygons']
    }


f = open(path_to_recall_json)
all_recalls_docs = json.load(f)
f.close()
# docs = [document_path for (recall, document_path) in all_recalls_docs] #this works for list of tuples

docs = [element[2] for element in all_recalls_docs]
print(docs[1])
print('making the files and folders...')
# if os.path.isdir(path_to_save):
#     shutil.rmtree(path_to_save)

# os.mkdir(path_to_save)
os.mkdir(path_to_save + '/train/')
os.mkdir(path_to_save + '/val/')
os.mkdir(path_to_save + '/val/images')
os.mkdir(path_to_save + '/test/')
os.mkdir(path_to_save + '/test/images')
os.mkdir(path_to_save + '/train/Easy/')
os.mkdir(path_to_save + '/train/Hard/')
os.mkdir(path_to_save + '/train/Easy/images')
os.mkdir(path_to_save + '/train/Hard/images')

# cutoffs contains the index numbers for the respective value cutoffs for the document difficulty.
# docs is a list from cut off pts of docs[0 to 10] i.e docs[0]
# easylist = all_recalls_docs[:cutoffs[0]]
# # mediumlist = docs[cutoffs[0]:cutoffs[1]]
# hardlist = all_recalls_docs[cutoffs[1]:]

cut_off = 0.7
easylist = [item[2] for item in all_recalls_docs if item[0] > cut_off]
hardlist = [item[2] for item in all_recalls_docs if item[0] <= cut_off]

random.shuffle(easylist)
# random.shuffle(mediumlist)
random.shuffle(hardlist)
print('Check contents of hard list', hardlist[0:10])
with open('jsons/hardlist.json', "w") as file:
    json.dump(hardlist, file)

traineasy = easylist[:math.floor(len(easylist)*split[0]/100)]
val = easylist[math.floor(len(easylist)*split[0]/100)               :math.floor(len(easylist)*(split[0]+split[1])/100)]
test = easylist[math.floor(len(easylist)*(split[0]+split[1])/100):]

# the splits are made such that both the difficulties easy and hard,however their percentage have a equal split of train,test,val
# trainmedium = mediumlist[:math.floor(len(mediumlist)*split[0]/100)]
# val = val + mediumlist[math.floor(len(mediumlist)*split[0]/100)
#                                   :math.floor(len(mediumlist)*(split[0]+split[1])/100)]
# test = test + mediumlist[math.floor(len(mediumlist)*(split[0]+split[1])/100):]

trainhard = hardlist[:math.floor(len(hardlist)*split[0]/100)]
val = val + hardlist[math.floor(len(hardlist)*split[0]/100)
                                :math.floor(len(hardlist)*(split[0]+split[1])/100)]
test = test + hardlist[math.floor(len(hardlist)*(split[0]+split[1])/100):]
print('Check contents of trainhard', trainhard[0:10])

with open('jsons/trainhard.json', "w") as file:
    json.dump(trainhard, file)
print("starting train hard")
labels = {}
for i, tiffile in enumerate(trainhard):
    shutil.copy(os.path.join(path_to_dataset, tiffile),
                path_to_save + '/train/Hard/images')
    tiffile = os.path.join(path_to_dataset, tiffile)
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/train/Hard/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

# print("starting train medium")
# labels = {}
# for i,tiffile in enumerate(trainmedium):
#     shutil.copy(tiffile, path_to_save + '/train/Medium/images')
#     make_labels(tiffile, labels)

# outfile = open(path_to_save + '/train/Medium/labels.json', "w")
# json.dump(labels, outfile, indent=6)
# outfile.close()

print("starting train easy")
labels = {}
for i, tiffile in enumerate(traineasy):
    shutil.copy(os.path.join(path_to_dataset, tiffile),
                path_to_save + '/train/Easy/images')
    tiffile = os.path.join(path_to_dataset, tiffile)
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/train/Easy/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

print("starting val")
labels = {}
for tiffile in val:
    shutil.copy(os.path.join(path_to_dataset, tiffile),
                path_to_save + '/val/images')
    tiffile = os.path.join(path_to_dataset, tiffile)
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/val/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()

print("starting test")
labels = {}
for tiffile in test:
    shutil.copy(os.path.join(path_to_dataset, tiffile),
                path_to_save + '/test/images')
    tiffile = os.path.join(path_to_dataset, tiffile)
    make_labels(tiffile, labels, i)

outfile = open(path_to_save + '/test/labels.json', "w")
json.dump(labels, outfile, indent=6)
outfile.close()
print('done!')
