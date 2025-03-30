import os 
import cv2 

def crop_image_by_percentage(img, percent,green_x1, green_x2, green_y1, green_y2,crop_folder,file_name,file_type):

    # Get the image dimensions
    height, width, _ = img.shape
    
    # Calculate the percentage of the image to crop
    scale_crop_w = int(percent * 0.01 * width) 
    scale_crop_h = int(percent * 0.01 * height) 

    #print
    print(f'\nscale_crop_w: {scale_crop_w}')
    print(f'scale_crop_h: {scale_crop_h}')
    
    
    if scale_crop_h >= green_y1:
        scale_crop_h1 =green_y1 #;print('scale_crop_h1: ',scale_crop_h1)
    else:
        scale_crop_h1 =scale_crop_h #;print('scale_crop_h1: ',scale_crop_h1)

    if scale_crop_w >= green_x1:
        scale_crop_w1 = green_x1
    else :
        scale_crop_w1 = scale_crop_w

    if  height-scale_crop_h <=  green_y2:  
        scale_crop_h2 =green_y2
    else:
        scale_crop_h2 = height-scale_crop_h

    if width-scale_crop_w <= green_x2:
        scale_crop_w2 = green_x2
    else:
        scale_crop_w2 = width-scale_crop_w 

    # Crop the image
    scale_x1 = scale_crop_w1 
    scale_y1 = scale_crop_h1 
    scale_x2 = scale_crop_w2 
    scale_y2 = scale_crop_h2 

    # print(f'\nscale_x1: {scale_x1}')
    # print(f'scale_y1: {scale_y1}')
    # print(f'scale_x2: {scale_x2}')
    # print(f'scale_y1: {scale_y2}')

    # image_cropped = img[scale_crop_h:height-scale_crop_h, scale_crop_w:width-scale_crop_w, :]
    image_cropped = img[scale_y1:scale_y2,scale_x1:scale_x2]
    cropped_img_h,cropped_img_w, _ = image_cropped.shape[:3]
    print(f'\ncropped image size: {image_cropped.shape}')

    
    #path =                 crop_folder dir    + image name  + extention        
    path = os.path.join(f'{crop_folder}', file_name + f'_crop_{percent}.{file_type}')
    # print(f'\n\npath: {path}')
    print(f'\nImage cropped: {file_name}.{file_type} with {percent}%')
    cv2.imwrite(path, image_cropped)

    # Return the cropped image
    return image_cropped,scale_x1, scale_x2, scale_y1, scale_y2,cropped_img_w,cropped_img_h

