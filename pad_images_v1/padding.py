import os 
import cv2

from pad_func import *
from pad_txt import *


def padding (use_max_padding,max_w,max_h,input_folder,pad_dir_folder,diff_dict):

    if use_max_padding:
        
        print(f'\n\n---------------- Start Padding ---------------- ')
                
        for input_file in os.listdir(input_folder): 

            print(f'\nInput File: {input_file}\n------------------------- ')
                    
            file_name = os.path.splitext(input_file)[0] 
                    
            if input_file.endswith(".jpg"): 
                        
                input_jpg = cv2.imread(f'{input_folder}/{input_file}')
                        
                file_type = 'jpg'
                padded_image, left_pad,top_pad = pad_func(input_file,input_jpg,pad_dir_folder,file_type,max_w,max_h) 
                                            
                pad_txt(input_folder,pad_dir_folder,\
                        file_name,input_jpg,padded_image, \
                        diff_dict,left_pad,top_pad)
                        # print(f'\npad_dir_folder: {pad_dir_folder}')
                    
            elif input_file.endswith(".png"): 
                
                continue
                # input_png = cv2.imread(f'{input_folder}/{input_file}')

                # file_type = 'png'

                # padded_image,left_pad,top_pad = padding_func(input_file,input_png,pad_dir_folder,file_type,max_w,max_h)

                # pad_txt(crop_folder,pad_dir_folder,\
                #         file_name,cropped_jpg,padded_image,percent, \
                #         diff_dict,left_pad,top_pad)
                #         # print(f'\npad_dir_folder: {pad_dir_folder}') 
                    
            else:         
                print('\nskip txt')
                continue #skip every file with extention .txt   
            
    # else:
    
    #     new_width = 640  # Desired width of the padded image
    #     new_height = 480  # Desired height of the padded image

    #     for cropped_file in os.listdir(crop_folder): 

    #         print(f'\n-------------------------\nCropped File: {cropped_file}\n------------------------- ')
                    
    #         file_name = os.path.splitext(cropped_file)[0] 
                    
    #         if cropped_file.endswith(".jpg"): 
                        
    #             cropped_jpg = cv2.imread(f'{crop_folder}{cropped_file}')
                        
    #             file_type = 'jpg'
    #             padded_image, left_pad,top_pad = padding_func(cropped_file,cropped_jpg,pad_dir_folder,file_type,new_width,new_height) 
                                            
    #             pad_txt(crop_folder,pad_dir_folder,\
    #                     file_name,cropped_jpg,padded_image,percent, \
    #                     diff_dict,left_pad,top_pad)
    #                     # print(f'\npad_dir_folder: {pad_dir_folder}')
                    
    #         elif cropped_file.endswith(".png"): 

    #             cropped_png = cv2.imread(f'{crop_folder}/{cropped_file}')

    #             file_type = 'png'
    #             padding_func(cropped_file,cropped_png,pad_dir_folder,file_type,new_width,new_height) 
                    
    #         else:         
    #             print('\nskip txt')
    #             continue #skip every file with extention .txt   
    
    return 