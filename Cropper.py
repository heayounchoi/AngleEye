# This module will crop dumpsters from images.
# Improves accuracy in during the angle check process.

import os
from PIL import Image

images_folder_path = 'images'
annotations_folder_path = 'annotations'
output_folder_path = 'cropped_images'

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

txt_files = [file for file in os.listdir(annotations_folder_path) if file.endswith('.txt')]

for txt_file in txt_files:
    with open(os.path.join(annotations_folder_path, txt_file), 'r') as file:
        annotation_dict = eval(file.read())
        
    image_name = annotation_dict['image_name']
    box_coordinates = annotation_dict['box_coordinates']

    input_image_path = os.path.join(images_folder_path, image_name)
    image = Image.open(input_image_path)
    x1, y1, x2, y2 = box_coordinates
    cropped_image = image.crop((x1, y1, x2, y2))

    output_image_path = os.path.join(output_folder_path, txt_file.replace('.txt', '.jpg'))
    cropped_image.save(output_image_path)

print("Images have been cropped and saved.")

