from padding import *
from pad_func import *
from display_boxes import *
from pad_txt import *

import argparse
import os
import cv2





INPUT_FOLDER =  '/home/stayros/Documents/certh/scripts/pad_images/dtset'
#'/home/spaspalakis/Desktop/certh/scripts/pad_images/dtset'

PAD_FOLDER = '/home/stayros/Documents/certh/scripts/pad_images/padded'
#'/home/spaspalakis/Desktop/certh/scripts/pad_images/padded'

# check if dir path from user which is set in args exist
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def get_arguments():
     
    parser = argparse.ArgumentParser()

    parser.add_argument('--input-dir', type=dir_path, default=INPUT_FOLDER,
                         help='Initial dir where all images exist ')

    parser.add_argument('--pad-dir', type=dir_path, default=PAD_FOLDER,
                         help='Initial dir where all images exist ')
    
    parser.add_argument('--max-padding', action='store_true',
                        help='Pad using max width and max height according to images in cropped folder')
    
    return parser.parse_args()



if __name__ == '__main__':

    #set arguments
    args = get_arguments()

    input_folder = args.input_dir
    pad_folder = args.pad_dir
    use_max_padding = args.max_padding


    files = os.listdir(input_folder)
    sorted_files = sorted(files)

    height_list = []
    width_list = []
    
    diff_dict={}

    for i,file in  enumerate(sorted_files):
        
        if file.endswith(".jpg"):   
            # read images from folder
            jpg_img = cv2.imread(f'{input_folder}/{file}') #;print(jpg_img)
            file_name = os.path.splitext(file)[0]   ; print(f'\n{i}.File_name: {file_name}')     
            
            height, width, _  =  jpg_img.shape
            print(f'image size: {jpg_img.shape}')

            width_list.append(width)
            height_list.append(height)

            # read .txt file which contains class and coordinates
            fl = open(f'{input_folder}/{file_name}.txt', 'r') 

            #txt_data contains row by row txt informantion 'class x,y,w,h' 
            txt_data = fl.readlines() #; print(f'\ntxt_data : {txt_data}')
            fl.close()

            # function to find bboxes from initial image
            diff_x, diff_y,left_list, top_list = display_boxes(jpg_img, txt_data)
            # cv2.namedWindow('asd', cv2.WINDOW_NORMAL)
            # cv2.imshow('asd',jpg_img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            diff_dict[file_name] = {'diff_x_values': diff_x, 'diff_y_values': diff_y}
            print(diff_dict)

    max_w = max(width_list) 
    max_h = max(height_list)
    print('max_w ',max_w)
    print('max_h ', max_h)

    padding(use_max_padding,max_w,max_h,input_folder,pad_folder,diff_dict)
