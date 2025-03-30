import cv2
import numpy as np
import os
import argparse

from os.path import join, isfile
from os import listdir

from display_boxes import *
from crop_image_by_percentage import *
from crop_txt import *
from fuse import *
from padding_func import *
from pad_txt import *

FOLDER_DIR = '/home/stayros/Desktop/isola-research/video_01_frames20/video_01-rembg' #'/home/stayros/Desktop/isola-research/uav123/boat6/boat6-rembg' #/home/stayros/Desktop/isola-research/all_test-5.0/dtset' # # #
CROP_DIR_FOLDER = '/home/stayros/Desktop/isola-research/video_01_frames20/video_01-cropped' #'/home/stayros/Desktop/isola-research/uav123/boat6/boat6-cropped' #'/home/stayros/Desktop/isola-research/all_test-5.0/cropped' # # #
PAD_DIR_FOLDER = '/home/stayros/Desktop/isola-research/video_01_frames20/video_01-padded' #'/home/stayros/Desktop/isola-research/uav123/boat6/boat6-padded' #'/home/stayros/Desktop/isola-research/all_test-5.0/padded' # # #
FUSED_DIR_FOLDER = '/home/stayros/Desktop/isola-research/video_01_frames20/video_01-fused' #'/home/stayros/Desktop/isola-research/uav123/boat6/boat6-fused' #'/home/stayros/Desktop/isola-research/all_test-5.0/fused' # # #

PERCENT = 25
FUSE_ORIGINAL = 0.9
FUSE_REMBG = 0.2


#check if dir path from user which is set in args exist
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_arguments():
     
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder-dir', type=dir_path, default=FOLDER_DIR,
                         help='Initial dir where all images exist ')
    
    parser.add_argument('--crop-dir-folder', type=dir_path, default=CROP_DIR_FOLDER,
                        help='Path where folders with cropped images should be stored')
    
    parser.add_argument('--pad-dir-folder', type=dir_path, default=PAD_DIR_FOLDER,
                        help='Path where padded images should be stored')
    
    parser.add_argument('--fused-dir-folder', type=dir_path, default=FUSED_DIR_FOLDER,
                        help='Path where folders with fused images should be stored')
    
    parser.add_argument('--percent', type=int, default=PERCENT,
                        help='Percentage of frame which should be cut')
    
    parser.add_argument('--fuse-org', type=float, default=FUSE_ORIGINAL,
                        help='Percentage which is multiplied with original image')
    
    parser.add_argument('--fuse-rembg', type=float, default=FUSE_REMBG,
                        help='Percentage which is multiplied with rembg image')
    
    parser.add_argument('--green-box', action='store_true',
                        help='Display green box for every image')
    


    parser.add_argument('--add-padding', action='store_true',
                        help='Pad all cropped image .jpg and .png')
    
    parser.add_argument('--add-fuse', action='store_true',
                        help='Fuse all cropped image .jpg and .png')
    
    return parser.parse_args()





if __name__ == '__main__':
    
    #set arguments
    args = get_arguments()
    
    folder_dir = args.folder_dir
    crop_dir_folder = args.crop_dir_folder
    pad_dir_folder = args.pad_dir_folder
    fused_dir_folder = args.fused_dir_folder

    percent = args.percent
    fuse_org = args.fuse_org
    fuse_rembg = args.fuse_rembg
    disp_green_box = args.green_box
    add_padding_flag = args.add_padding
    add_fuse = args.add_fuse
    
    #sort all images into folder
    files = os.listdir(folder_dir)
    sorted_files = sorted(files)

    #create crop folder
    crop_folder_name = f'cropped_{percent}/'
    crop_folder = os.path.join(crop_dir_folder,crop_folder_name)
    if not os.path.exists(crop_folder):
        os.mkdir(crop_folder)
    else:
         print('\nFolder already exists')
         pass
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(pad_dir_folder):
        os.makedirs(pad_dir_folder)

    
    #create fuse folder
    if add_padding_flag: 
        fused_folder_name = f'fused_{percent}_{fuse_org}OR_{fuse_rembg}Rembg_padded/'
        fuse_folder = os.path.join(fused_dir_folder,fused_folder_name)
        if not os.path.exists(fuse_folder):
            os.mkdir(fuse_folder)
        else:
            print('\nFolder already exists')
            pass
    else:
        fused_folder_name = f'fused_{percent}_{fuse_org}OR_{fuse_rembg}Rembg/'
        fuse_folder = os.path.join(fused_dir_folder,fused_folder_name)
        if not os.path.exists(fuse_folder):
            os.mkdir(fuse_folder)
        else:
            print('\nFolder already exists')
            pass

    
    

    for file in  sorted_files: 

        print(f'\n-------------------------\nFile: {file}\n------------------------- ')
        
        
        if file.endswith(".jpg"):   
                
                file_type = 'jpg'


                # read images from folder
                jpg_img = cv2.imread(f'{folder_dir}/{file}') #;print(jpg_img)
                file_name = os.path.splitext(file)[0]   #; print(f'\nFile_name: {file_name}')

                print(f'\noriginal image size: {jpg_img.shape}')

                # read .txt file which contains class and coordinates
                fl = open(f'{folder_dir}/{file_name}.txt', 'r') 
                
                #txt_data contains row by row txt informantion 'class x,y,w,h' 
                txt_data = fl.readlines() #; print(f'\ntxt_data : {txt_data}')
                fl.close()

                # function to find bboxes from initial image
                green_x1, green_x2, green_y1, green_y2, diff_x, diff_y,\
                      final_min_list, left_list, top_list = display_boxes(jpg_img, txt_data,disp_green_box)
                
                cropped_jpg,scale_x1, scale_x2, scale_y1, scale_y2 = crop_image_by_percentage(jpg_img, percent,\
                                                                                                green_x1, green_x2, green_y1, green_y2,\
                                                                                                    crop_folder,file_name,file_type)
                
                crop_bbox_x1,crop_bbox_y1,crop_bbox_x2,crop_bbox_y2 =crop_txt(crop_folder,file_name, cropped_jpg,\
                                                                            scale_x1, scale_y1,txt_data,percent,\
                                                                                left_list,top_list,diff_x, diff_y)
                
                if add_padding_flag:
                   
                   padded_image, left_pad,top_pad = padding_func(file,cropped_jpg,pad_dir_folder,file_type) 
                    
                   pad_txt(crop_folder,pad_dir_folder,\
                              file_name,cropped_jpg,padded_image,percent, \
                              diff_x,diff_y,left_pad,top_pad)
                    # print(f'\npad_dir_folder: {pad_dir_folder}')

        elif file.endswith(".png"): 

                file_type = 'png'

                # read images from file
                png_img = cv2.imread(f'{folder_dir}/{file}')          
                file_name = os.path.splitext(file)[0]   #; print(f'\nFile_name: {file_name}')

                # read .txt file which contains class and coordinates
                # fl = open(f'{folder_dir}/{file_name}.txt', 'r') 
                # #data contains row by row txt informantio 'class x,y,w,h' 
                # txt_data = fl.readlines() #; print(f'\ndata : {txt_data}')
                # fl.close()

                cropped_png,scale_x1, scale_x2, scale_y1, scale_y2  = crop_image_by_percentage(png_img, percent,green_x1, green_x2, green_y1, green_y2,crop_folder,file_name,file_type)
                # print('\nRemBG image cropped')

                if add_padding_flag:
                    padding_func(file,cropped_png,pad_dir_folder,file_type) 
        else:         
            print('\nskip txt')
            continue #skip every file with extention .txt   


        # cv2.rectangle(cropped_image, (crop_bbox_x1, crop_bbox_y1), (crop_bbox_x2, crop_bbox_y2), (0, 0, 255), 1)
        # cv2.imshow('cropped',cropped_image)
    


   


    if add_fuse:
        if add_padding_flag:
            fuse(pad_dir_folder,fuse_folder,fuse_org,fuse_rembg)
        else:
            fuse(crop_folder,fuse_folder,fuse_org,fuse_rembg)    

    print('\n------\nEnd of proccess!')

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()




