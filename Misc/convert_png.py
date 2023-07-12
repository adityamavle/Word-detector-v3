import os
from PIL import Image
import sys

def convert_to_png(image_folder, output_folder):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        else:
            print(f'A folder named {output_folder} already exists!')
        images = os.listdir(image_folder)
        # print(images)
        for image in images:
            img = Image.open(f'{image_folder}/{image}')
            cleaned_name = os.path.splitext(image)[0]
            img.save(f'{output_folder}/{cleaned_name}.png', 'png')

        print("Done!")

        input_directory = 'input_images'
        output_directory = 'output_images'

convert_to_png("C:/Users/adity/docTR-v1-finetune/merged_newdata/",r"C:/Users/adity/docTR-v3-finetune/merged_pngs/")
