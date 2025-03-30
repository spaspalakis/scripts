from os.path import join, isfile
from os import listdir
import glob
import os
import cv2
import numpy as np
from PIL import Image
import imageio
import shutil 

def fuse(input_folder,fuse_folder,fuse_org,fuse_rembg):
    
    print('\n\n------ Fuse images ------\n\n ')

    orignObjects = []
    rembgObjects = []

    orign  = [
        join( input_folder, fn )                    # Create full paths to images
        for fn in listdir( input_folder )           # For each item in the image folder
        if isfile( join( input_folder, fn ) )       # If the item is indeed a file
        and fn.lower().endswith(('.jpg')) # Which ends with an image suffix (can add more types here if needed)
    ]

    sort_oring = sorted(orign) #; print(f'\nsort_oring: {sort_oring}')
    

    for i in sort_oring:
        image = cv2.imread(i)
        orignObjects.append(image)

    rembg  = [
        join( input_folder, fn )                    # Create full paths to images
        for fn in listdir( input_folder )           # For each item in the image folder
        if isfile( join( input_folder, fn ) )       # If the item is indeed a file
        and fn.lower().endswith(('.png')) # Which ends with an image suffix (can add more types here if needed)
    ]

    sort_rembg = sorted(rembg) #; print(f'\nsort_rembg: {sort_rembg}')


    for i in sort_rembg:
        image = cv2.imread(i)
        rembgObjects.append(image)


    print(f'images in list: {len(orignObjects)}')

    for i,_ in enumerate(orignObjects):

        file_name= sort_oring[i].split('/')[-1].split('.')[0] ; print(f'\n-------\nfuse file_name: {file_name}')

        # print(f'\nfuse_org*orignObjects[i] : {(fuse_org*orignObjects[i]).shape }')
        # print(f'\nfuse_rembg*rembgObjects[i] : {(fuse_rembg*rembgObjects[i]).shape }')

        fuse_img = fuse_org*orignObjects[i] +fuse_rembg*rembgObjects[i] 
        # print(f'\nOrign: {(fuse_org*orignObjects[i]).shape}\nRembg: {(fuse_rembg*rembgObjects[i]).shape}')
        
        fuse_img = np.clip(fuse_img, 0, 255).astype('uint8') #; print(f'\nfuze type: {type(fuse_img)}')
        # print(f'\nfused: {(fuse_img).shape}')
        # cv2.imshow('fuse_img ',fuse_img)
        
        # imageio.imwrite(f'{OUTPUT_DIR}fused_{i}.jpg',fuse_img)
        # print(f'fused path: {fuse_folder}{file_name}.jpg')
        cv2.imwrite(f'{fuse_folder}{file_name}.jpg',fuse_img)


    files = glob.iglob(os.path.join(input_folder,"*txt"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, fuse_folder)
    print('\n-------\nTXT files moved to fuse folder')
    return   
    # break






