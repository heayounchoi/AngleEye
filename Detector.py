# This module detects object from an image.
# Only draws boxes around objects with the highest scores.
# Save the annotations if the model detects dumpsters correctly.
# Saved annotations will be used to crop images in Cropper.py.

import os
import torch
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw

model = fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

image_dir = 'images'
annotation_dir = 'annotations'

if not os.path.exists(annotation_dir):
    os.makedirs(annotation_dir)

image_extensions = ['.jpeg', '.jpg']

for filename in os.listdir(image_dir):
    if any(filename.endswith(ext) for ext in image_extensions):
        image_path = os.path.join(image_dir, filename)
        image = Image.open(image_path)

        image_tensor = F.to_tensor(image).unsqueeze(0)

        with torch.no_grad():
            predictions = model(image_tensor)

        boxes = predictions[0]['boxes'].tolist()
        scores = predictions[0]['scores'].tolist()

        if len(boxes) > 0:
            max_score_index = scores.index(max(scores))
            best_box = boxes[max_score_index]

            annotation_data = {
                'image_name': filename,
                'box_coordinates': best_box
            }

            draw = ImageDraw.Draw(image)
            draw.rectangle(best_box, outline='red', width=3)

            image.show()
            user_input = input(f"Do you want to save bounding box annotation for {filename}? (y/n): ").strip().lower()

            if user_input == 'y':
                annotation_filename = os.path.splitext(filename)[0] + '.txt'
                annotation_path = os.path.join(annotation_dir, annotation_filename)
                with open(annotation_path, 'w') as annotation_file:
                    annotation_file.write(str(annotation_data))

            image.close()
        else:
            print(f"No object detected in {filename}")

print("Annotation process completed.")