import pandas as pd
import numpy as np
import seaborn as sns
import pydicom
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
import json
import cv2

# Load the image dataframe so we can get BB coords
base_path = "/kaggle/input/siim-covid19-detection/"
images_df = pd.read_csv(os.path.join(base_path,"train_image_level.csv"))

# Function to get the BB data from the images DF
def get_boxes(image_id):
    image = image_id.replace('.dcm','_image')
    ti = images_df[images_df['id'] == image]
    bx = [[],[]]
    bx[0] = [0,0,0,0,""]
    bx[1] = [0,0,0,0,""]
    
    if str(ti['boxes'].values[0]) != "nan":
        box = str(ti['boxes'].values[0]).replace("'","\"")
        boxes = json.loads(box)
        lab = ti['label'].values[0].split(" ")
        i = 0
        for b in boxes:
            bx[i] = [int(b['x']), int(b['y']), int(b['width']),int(b['height']),lab[0]]
            i = i+1
    return bx


# This function applies the crop offsets to BB coords
# We just subtract the amount cropped from the top and left from the BB coords.
def crop_offset(x,y, offset):
    x = [i - (offset[0] + offset[2]) for i in x]
    y = [i - (offset[1] + offset[3]) for i in y]
    return x, y

    
# This function draws boxes on images, one line at a time
def draw_boxes(boxes, z):

    for i in boxes:     
        # Top
        x = [i[0] - z[0], i[0] + i[2] - z[0]]        # [ x1 , x2 ]
        y = [i[1] - z[1], i[1] - z[1]]               # [ y1 , y2 ]
        plt.plot(x,y, color='#ff8838', linewidth=2)
        
        # Bottom
        y = [i[1] + i[3] - z[1], i[1] + i[3] - z[1]]
        plt.plot(x,y, color='#ff8838', linewidth=2)
        
        # Left
        x = [i[0] - z[0], i[0] - z[0]]
        y = [i[1] - z[1], i[1] + i[3] - z[1]]
        plt.plot(x,y, color='#ff8838', linewidth=2)

        # Right         
        x = [i[0] + i[2] - z[0], i[0] + i[2] - z[0]]
        plt.plot(x,y, color='#ff8838', linewidth=2)

#Load an image
# Load a random DICOM file
filename = '../input/siim-covid19-detection/train/00086460a852/9e8302230c91/65761e66de9f.dcm'
    
img = pydicom.dcmread(filename)
pixels = img.pixel_array

# Invert MONOCHROME1 the easy way for demo purposes
cmap = "gray"
if (img.PhotometricInterpretation == "MONOCHROME1"):
    cmap = "gray_r"

#Crop the left by 200 pixels and the top by 500 pixels
# Make a cropped copy of the image
crop = [200,500,0,0]   # left, top, right, bottom

w = pixels.shape[1] - (crop[0] + crop[2])
h = pixels.shape[0] - (crop[1] + crop[3])

cropped = pixels[crop[1]:crop[1] + h, crop[0]:crop[0] + w]

print("Orig size: " + str(pixels.shape[1]) + " x " + str(pixels.shape[0]))
print("Crop size: " + str(cropped.shape[1]) + " x " + str(cropped.shape[0]))

#Orig size: 2783 x 2330
#Crop size: 2583 x 1830
#Grab the BB coordinates, apply the crop offsets and draw them on the images.

# Get the BB coordinates
boxes = get_boxes(str(os.path.basename(filename)))

plt.figure(figsize=(15,5)) 

# Display the original image with no cropping
plt.subplot(1, 2, 1)
plt.title("Original: " + str(pixels.shape[1]) + " x " + str(pixels.shape[0]))

# Draw BB's. Pass the cropping values of zero.
draw_boxes(boxes, [0,0,0,0])
plt.imshow(pixels,cmap=cmap)      
plt.subplot(1, 2, 2)

# Display the cropped image
plt.title("Cropped: " + str(cropped.shape[1]) + " x " + str(cropped.shape[0]))

# Draw BB's, pass the 'crop' value we used earlier to crop the image
draw_boxes(boxes, crop)
plt.imshow(cropped,cmap=cmap)
plt.show()