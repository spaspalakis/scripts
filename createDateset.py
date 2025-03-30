
"""
-----------
DISCLAIMER 
-----------
This .py file reads a .txt file which contains the image set from a dataset (e.g. the train set)
and then stores into a new folder all the images and annotations are related to this set

Details:
1. Reads a .txt file with the image set (e.g. train/test.txt)
2. Reads the folder path which contains images and annotations
3. Create a new folder to store the images and annotations (e.g. train/test folder)
4. Copy every image and .xml to the new folder


The user must assign/change:
1. the .txt path 
2. The folder path where the images are contained
3. The folder path where the annotations are contained
4. The name of the new folder
"""

import glob
import os
import shutil

# Read .txt file with which contains the image set
TXT_PATH = '/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train/image_sets' #set the path
TXT_FILE= 'train.txt' #set the file name

# Folder path for images and annotations 
ALL_IMG_PATH = '/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train/images' # path which contains all images
ALL_XML_PATH = '/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train/annotations' # path which contains all xml files

# We need to create a new folder path where we store the new folder 
# Destination path.
#  Folder path where images and annotations would be stored
NEW_FOLDER_PATH= '/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train'   ## Put path without '/' at the end

# Destination path.
#  Folder path where images and annotations would be stored
# DST_PATH = '/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train'  ## Put path without '/' at the end



def copy_images(lines,idx_l,all_img_path,dst_img_path):
      for i in glob.glob(f"{all_img_path}/*.jpg"): #read all images 
        img_name = i.split('/')[-1].split('.')[0] ;  print(img_name) # get the name of the image
        img_ext = '.'+i.split('.')[-1]  ;  print(img_ext) # get the extension (.jpg)
        # print(i)
        if lines[idx_l] == img_name: # check if corresponding img from .txt exists in allImage folder
            # print(dst_img_path+img_name+img_ext)
            shutil.copy(i,dst_img_path+img_name+img_ext) #copy image to new folder



# The same happens with the annoations 
def copy_annot(lines,idx_l,all_xml_path,dst_img_path):
      for i in glob.glob(f"{all_xml_path}/*.xml"):
        annot_name = i.split('/')[-1].split('.')[0]
        annot_ext = '.'+i.split('.')[-1]
        # print(f"\nannot_name: {annot_name}\n annot_ext: {annot_ext}:")
        # print(i)
        if lines[idx_l] == annot_name:
            # print(dst_img_path+annot_name+annot_ext)
            shutil.copy(i,dst_img_path+annot_name+annot_ext)



if __name__ == '__main__':

    
    with open(f'{TXT_PATH}/{TXT_FILE}') as file:
        lines = file.readlines()
        lines = [l.rstrip() for l in lines] # lines is a list type e.g. [...,'21652', '21664']
        
  
    # Create a new folder to store the train/test set
    # Name the new folder
    new_folder =input('\nGive folder name: ') # eg. 'crossroad_test'
    
    if not os.path.exists(f'{NEW_FOLDER_PATH}/'+ new_folder): #if the folder doesn't exists it will be created automatically
        os.makedirs(f'{NEW_FOLDER_PATH}/'+ new_folder)
        print(f'\nNew folder: [{new_folder}] just created!')
        input("\nPress Enter to continue...")

    else:
        print('\nFolder already exist') 
        input("\nPress Enter to continue...")



    dst_img_path = f'{NEW_FOLDER_PATH}/'+ new_folder +'/'
    print(f'\nDestination of the new folder: {dst_img_path}')

    for idx_l,l in enumerate(lines): # Read each row from .txt with the image set
        # print(idx_l,l)
        # print(lines[idx],images[idx])
        print(f'\nrow item : ',lines[idx_l]) 

        copy_images(lines,idx_l,ALL_IMG_PATH,dst_img_path) # copy corresponding images
        
        copy_annot(lines,idx_l,ALL_XML_PATH,dst_img_path) # copy corresponding xml
        
        
    print('\nProcess Finished!')