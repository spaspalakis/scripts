
from os.path import join, isfile
from os import listdir
import glob
import os
import cv2
import numpy as np
from PIL import Image
import imageio

def compare_names(sort_first,sort_second,folder1_name,folder2_name):


    for i,_ in enumerate(sort_first):

        name1 = sort_first[i].split('/')[-1].split('.')[0] #.rsplit('.', 1)[0]  ; print(name1)
        name2 = sort_second[i].split('/')[-1].split('.')[0] #.rsplit('.', 1)[0]  ; print(name2)

        if name1 == name2:  # This is True for this exact case
            print(f'\n{i}. {name1} exist in both folders')
        else:
            print('\nSome name does not exit!\nBreak!')
            print(f'\nFile: {name1} in folder {folder1_name}  &\nFile: {name2} in foler {folder2_name}\n\nDoes not exist on other fodler or vice versa')
            break



if __name__ == '__main__':

    orignObjects = []
    rembgObjects = []

    FIRST_DIR = '/home/stayros/Desktop/asd/test_original'

    SECOND_DIR = '/home/stayros/Desktop/asd/test'

    folder1_name = os.path.splitext(FIRST_DIR)[0]   ; print(f'\nFile_name: {folder1_name}')
    folder2_name = os.path.splitext(SECOND_DIR)[0]   ; print(f'\nFile_name: {folder2_name}')

    first_folder  = [
        join( FIRST_DIR, fn )                    # Create full paths to images
        for fn in listdir( FIRST_DIR )           # For each item in the image folder
        if isfile( join( FIRST_DIR, fn ) )       # If the item is indeed a file
        and fn.lower().endswith(('.jpg')) # Which ends with an image suffix (can add more types here if needed)
    ]

    sort_first = sorted(first_folder) #; print('\n',sort_oring)

    second_folder  = [
        join( SECOND_DIR, fn )                    # Create full paths to images
        for fn in listdir( SECOND_DIR )           # For each item in the image folder
        if isfile( join( SECOND_DIR, fn ) )       # If the item is indeed a file
        and fn.lower().endswith(('.png')) # Which ends with an image suffix (can add more types here if needed)
    ]

    sort_second = sorted(second_folder) #; print('\n',sort_rembg



    compare_names(sort_first,sort_second,folder1_name,folder2_name)


    print('\nAll files exist in both folders')


# sorted_files = sorted( imageObjects )
# print('\n',sorted_files) 
