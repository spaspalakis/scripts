import os
import cv2
import numpy as np
# from pad_txt import *
# from pad_txt2 import *

def pad_image(image, new_width, new_height):
    # print(image)
    
    # Get the original image size
    height, width, _ = image.shape

    # Calculate the padding sizes
    pad_width = max(new_width - width, 0) 
    pad_height = max(new_height - height, 0) 
    left_pad = pad_width // 2
    top_pad = pad_height // 2
    right_pad = pad_width - left_pad
    bottom_pad = pad_height - top_pad

    # print(f'\npad_width: {pad_width}')
    # print(f'pad_height: {pad_height}')
    # print(f'left_pad: {left_pad}')
    # print(f'top_pad: {top_pad}')

    # Create a new image with the desired dimensions and black background
    padded_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)     # This is for WHITE bg --> np.ones((new_height, new_width, 3), dtype=np.uint8) *255
                                                                                # This is for BLACK bg --> np.zeros((new_height, new_width, 3), dtype=np.uint8)               
    # Calculate the coordinates for pasting the original image
    x_start = left_pad
    x_end = left_pad + width
    y_start = top_pad
    y_end = top_pad + height

    # Paste the original image in the center of the padded image
    padded_image[y_start:y_end, x_start:x_end, :] = image

    return padded_image,left_pad,top_pad


def padding_func(file,cropped_img,pad_dir_folder,file_type):
    
    file_name = os.path.splitext(file)[0]   #; print(f'\nFile_name: {file_name}')

    # Example usage
    # image_path = "input_image.jpg"  # Replace with your own image path
    new_width = 640  # Desired width of the padded image
    new_height = 480  # Desired height of the padded image

    padded_image,left_pad,top_pad = pad_image(cropped_img, new_width, new_height)

    if file.endswith(".jpg"): 
        
        file_type = 'jpg'
        
        # Save the padded JPG image
        output_path = os.path.join(pad_dir_folder, f"{file_name}_pad.{file_type}")
        cv2.imwrite(output_path, padded_image)
        print(f"\nPadded image saved as '{output_path}'")
        

    elif file.endswith(".png"):

        file_type = 'png'

        # Save the padded PNG image
        output_path = os.path.join(pad_dir_folder, f"{file_name}_pad.{file_type}")
        cv2.imwrite(output_path, padded_image)
        print(f"\nPadded image [ {file_name} ] created")


    return padded_image, left_pad,top_pad 