from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import cv2
import os

image_dir = 'cropped_images'

image_extensions = ['.jpeg', '.jpg']

correct = 0


for target in os.listdir(image_dir):
        
    with Image.open(f"cropped_images/{target}") as img:
        div = img.size[1] / 500
        img = img.resize((int(img.size[0]/div), int(img.size[1] / div)))
        
        img_np = np.array(img)
        pallet = np.zeros(img_np.shape[:2])
        
        for y in range(img.width):
            for x in range(img.height):
                rgb = img_np[x, y]
                if rgb[1] > rgb[0] * 1.1 and rgb[1] > rgb[2] * 1.1:
                    pallet[x,y] = rgb[1]


    transposed_img = pallet.transpose()

    siluet=[]

    for idx, row in enumerate(transposed_img):
        indices = np.where(row != 0)
        
        try:
            siluet.append(indices[0][-1])
        except:
            if len(indices[0]) == 0:
                siluet.append(0)
                
    final = np.zeros(transposed_img.transpose().shape)

    for x in range(final.shape[1]):
        if siluet[x] > img.size[1] / 3:
            final[siluet[x], x] = 255
            
    max_values = []

    for i in ['0','-15','-30','15','30']:
        with Image.open(f"kernels/degree{i}.png") as degree:
            kernel = np.array(degree)
            a = cv2.filter2D(final, -1, kernel)
            max_values.append(np.max(a))

    answer = ['0','-15','-30','15','30'][np.argmax(max_values)]

    with Image.open(f"kernels/degree{answer}.png") as degree:
        kernel = np.array(degree)
        a = cv2.filter2D(final, -1, kernel)
        
    
    if (answer == '0') and (target.split(".")[0].split("_")[-1]) == '1':
        correct += 1
    elif (answer != '0') and (target.split(".")[0].split("_")[-1]) == '0':
        correct += 1
    else:
        print(f"[check] answer: {answer} degrees, filename: {target}, real(0: tilted, 1: straight): {target.split('.')[0].split('_')[-1]}")
        
print(f"accuracy: {correct / len(os.listdir(image_dir)) * 100}%")