from os.path import join, isfile
from os import listdir
import glob
import os
import cv2
import numpy as np
from PIL import Image
import imageio

def fuse_image(orignObjects,rembgObjects,OUTPUT_DIR,sort_oring):


    for i,_ in enumerate(orignObjects):

        file_name= sort_oring[i].split('/')[-1].split('.')[0] 

        fuse_img = 0.7*orignObjects[i] +0.5*rembgObjects[i]
        
        fuse_img = np.clip(fuse_img, 0, 255).astype('uint8') #; print(f'\nfuze type: {type(fuse_img)}')
        cv2.imshow('fuse_img ',fuse_img)
        
        #
        # imageio.imwrite(f'{OUTPUT_DIR}fused_{i}.jpg',fuse_img)
        print(f'\nfused path: {OUTPUT_DIR}{file_name}.jpg')
        imageio.imwrite(f'{OUTPUT_DIR}{file_name}.jpg',fuse_img)
       
    # break



if __name__ == '__main__':

    orignObjects = []
    rembgObjects = []

    FOLDER_DIR = '/home/stayros/Desktop/fuse_folder/'

    OUTPUT_DIR = '/home/stayros/Desktop/fuse_folder/fused/'


    orign  = [
        join( FOLDER_DIR, fn )                    # Create full paths to images
        for fn in listdir( FOLDER_DIR )           # For each item in the image folder
        if isfile( join( FOLDER_DIR, fn ) )       # If the item is indeed a file
        and fn.lower().endswith(('.jpg')) # Which ends with an image suffix (can add more types here if needed)
    ]

    sort_oring = sorted(orign) #; print('\n',sort_oring)
    

    for i in sort_oring:
        image = cv2.imread(i)
        orignObjects.append(image)

    rembg  = [
        join( FOLDER_DIR, fn )                    # Create full paths to images
        for fn in listdir( FOLDER_DIR )           # For each item in the image folder
        if isfile( join( FOLDER_DIR, fn ) )       # If the item is indeed a file
        and fn.lower().endswith(('.png')) # Which ends with an image suffix (can add more types here if needed)
    ]

    sort_rembg = sorted(rembg) #; print('\n',sort_rembg)

    for i in sort_rembg:
        image = cv2.imread(i)
        rembgObjects.append(image)


    fuse_image(orignObjects,rembgObjects,OUTPUT_DIR,sort_oring)



    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print('\nEnd of process!')

# sorted_files = sorted( imageObjects )
# print('\n',sorted_files) 
