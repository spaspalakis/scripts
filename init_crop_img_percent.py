import cv2
import numpy as np
import os



def green_rec(img, final_min_list):

    img_with_green_rec = img.copy()

    print(f'\n----- Green Box ------\n')

    green_h, green_w, _ = img_with_green_rec.shape # w, h arxikis eikonas
    
    print(f'green_w: {green_w}\ngreen_h: {green_h}\n')

    green_x1 = int((final_min_list[0]))  # ; print(f'\ngreen Left1 (x1): {green_left}')
    green_y1 = int((final_min_list[1]))  # ; print(f'green Top1 (y1): {green_top}')

    green_x2 = int((final_min_list[2]))  # ; print(f'green Right1 (x2): {green_right}')
    green_y2 = int((final_min_list[3]))  # ; print(f'green Bottom1 (y2): {green_bottom}\n----\n')

    if green_x1 < 0:
        green_x1 = 0
    if green_x2 > green_w - 1:
        green_x2 = green_w - 1.

    if green_y1 < 0:
        green_y1 = 0
    if green_y2 > green_h - 1:
        green_y2 = green_h - 1

    print(f'\ngreen Left (x1): {green_x1}')
    print(f'green Top (y1): {green_y1}\n')

    print(f'green Right (x2): {green_x2}')
    print(f'green Bottom (y2): {green_y2}\n')

    cv2.rectangle(img_with_green_rec, (green_x1, green_y1), (green_x2, green_y2), (0, 255, 0), 1)

    center_greenX = (green_x2+ green_x1)/2 ; print(f'center_greenX: {center_greenX}')
    center_greenY = (green_y2 + green_y1)/2 ; print(f'center_greenY: {center_greenY}')

    cv2.circle(img_with_green_rec, (int(center_greenX), int(center_greenY)), 1, [0,0,255], 2)
    
    cv2.imshow('img_with_green_rec', img_with_green_rec)

    return green_x1, green_x2, green_y1, green_y2


def YOLO_to_XY(x,y,w,h,img_w,img_h):
        
    # convert YOLO coordinates to x1,y1,x2,y2 format
    left = int((x - w / 2) * img_w); print(f'\nLeft (X1): {left}')  # x1
    right = int((x + w / 2) * img_w); print(f'Right (X2): {right}')  # x2
    top = int((y - h / 2) * img_h); print(f'Top (Y1): {top}')  # y1
    bottom = int((y + h / 2) * img_h); print(f'Bottom (Y2): {bottom}\n')  # y2

    # check image boundaries
    if left < 0:
        left = 0

    if right > img_w - 1:
        right = img_w - 1

    if top < 0:
         top = 0

    if bottom > img_h - 1:
        bottom = img_h - 1
    
    return left,right,top,bottom


def XY_to_YOLO(size, box):
        
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    return x,y,w,h


def find_min(left_list, top_list, right_list,bottom_list):

    final_min_list =[]

    left_list = min(left_list) ; print (f'\nmin left_list: {left_list}')
    top_list = min(top_list) ; print (f'min top_list: {top_list}')
    right_list = max(right_list) ; print(f'max right_list: {right_list}')
    bottom_list = max(bottom_list) ; print(f'max bottom_list: {bottom_list}')
        
    final_min_list = [left_list, top_list, right_list, bottom_list]    
    # print(f'\nfinal min list: {final_min_list}\n')

    return final_min_list



def display_boxes(img, data):
    
    img_with_initial_bboxes = img.copy()

    img_h, img_w, _ = img_with_initial_bboxes.shape # w, h for initial image
    print(f'\nimg_w: {img_w}\nimg_h: {img_h}\n')

    left_list = []
    top_list= []
    right_list = []
    bottom_list = []
    # final_min_list =[]
    diff_x = []
    diff_y =[]


    # Read every object into .txt file 
    for i, dt in enumerate(data):

        print(f'\n---------------------\nObject: {i} | class: {dt[0]}\n')

        # Split string to float
        _, x, y, w, h = map(float, dt.split(' ')) #; print(f'\nx: {x}\ny: {y}\nw: {w}\nh: {h}')

        """
        Taken from https://github.com/pjreddie/darknet/blob/810d7f797bdb2f021dbe65d2524c2ff6b8ab5c8b/src/image.c#L283-L291
        via https://stackoverflow.com/questions/44544471/how-to-get-the-coordinates-of-the-bounding-box-in-yolo-object-detection#comment102178409_44592380
        """
        
        left, right, top, bottom = YOLO_to_XY(x, y, w, h, img_w, img_h)

        # diff_x andd diff_y are lists that contain the size of each bbox/object in x,y
        # there gone be used to detect the bboxes into cropped images 
        diff_x.append(right - left) ; 
        diff_y.append(bottom - top) ; 

        # append left,top,right,bottom into a list
        left_list.append(left)
        top_list.append(top)

        right_list.append(right)
        bottom_list.append(bottom)

        
        #create rec for bboxes
        cv2.rectangle(img_with_initial_bboxes, (left, top), (right, bottom), (0, 0, 255), 1)
    
    # display image
    # cv2.imshow('img_with_init_bboxes', img_with_initial_bboxes)


    """
    So after we saved x1,y1,x2,y2 for every object.
    Now we try to detect which bbox/object is the most left and the most right into the image
    In order to create the cropped bbox
    """

    print(f'\n------ All listes -----\n\nleft_list: {left_list}\ntop_list: {top_list}\nright_list: {right_list}\nbottom_list: {bottom_list}')    


    # Find_min function, finds min(x1,y1) and max(x2,y2) in order to create green box/cropped window
    # final_min_list  is the list with those coordinates
    final_min_list = find_min(left_list, top_list, right_list,bottom_list)
    print(f'\nfinal min list: {final_min_list}\n')


    # Print 
    print (f'diff X: {diff_x}') # x2-x1 
    print (f'diff Y: {diff_y}') # y2 -y1
    

    # Green_rec is the function which creats the new window with coordinates min(x1,y1) kai max(x2,y2)
    green_x1, green_x2, green_y1, green_y2 = green_rec(img, final_min_list)


    return green_x1, green_x2, green_y1, green_y2, diff_x, diff_y, final_min_list, left_list, top_list


def crop_image_by_percentage(file, img,data, percentage,green_x1, green_x2, green_y1, green_y2,CROP_DIR_FOLDER,file_name):
    # Load the image
    # image = cv2.imread(image_path)

    # Get the image dimensions
    height, width, _ = img.shape
    
    # Calculate the percentage of the image to crop
    scale_crop_w = int(percentage * 0.01 * width) #;print(f'\nscale_crop_w: {scale_crop_w}')
    scale_crop_h = int(percentage * 0.01 * height) #;print(f'scale_crop_h: {scale_crop_h}')

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

    # image_cropped = img[scale_crop_h:height-scale_crop_h, scale_crop_w:width-scale_crop_w, :]
    image_cropped = img[scale_y1:scale_y2,scale_x1:scale_x2]
        

    #path =                 crop_folder dir    + image name  + extention        
    path = os.path.join(f'{CROP_DIR_FOLDER}', file_name + f'_crop_{percent}.jpg')
    cv2.imwrite(path, image_cropped)
    # Return the cropped image
    return image_cropped,scale_x1, scale_x2, scale_y1, scale_y2



def crop_txt(image_cropped,scale_x1, scale_x2, scale_y1, scale_y2,txt_data):

    crop_h, crop_w, _ = image_cropped.shape 

    print('\ncrop_txt')
    # we run every object of of txt file
    for i, dt in enumerate(txt_data):
 
        crop_bbox = (scale_x1, scale_x2, scale_y1, scale_y2)
        x,y,w,h = XY_to_YOLO((crop_w,crop_h), crop_bbox)


        with open(f'{CROP_DIR_FOLDER}/{file_name}_crop_{percent}.txt', 'w') as crop_txt:
            print(f'\nrow: {dt[0]} {x} {y} {w} {h}')
            crop_txt.write(f'{dt[0]} {x} {y} {w} {h}\n')

    crop_txt.close()
    
    return 


if __name__ == '__main__':
    

    FOLDER_DIR = '/home/stayros/Desktop/asd' 
    CROP_DIR_FOLDER = r'/home/stayros/Desktop/asd/cropped'

    percent = int(input("Insert persen to crop: "))

    for file in  os.listdir(FOLDER_DIR):  #os.listdir(FOLDER_DIR):

        print(f'\n-------------------------\nFile: {file}\n------------------------- ')
        
        if file.endswith(".txt"): 
            print('skip')
            continue #skip every file with extention .txt
        
        else:

            if file.endswith(".jpg"):    
                # read images from file
                img = cv2.imread(f'{FOLDER_DIR}/{file}') # /home/spaspalakis/Desktop/rembg_result/0a9fe927701bb9ee.png  #/home/spaspalakis/Desktop/test_rembg3/           
                file_name = os.path.splitext(file)[0]   ; print(f'\nFile_name: {file_name}')

            # read .txt file which contains class and coordinates
            fl = open(f'{FOLDER_DIR}/{file_name}.txt', 'r') 
            #data contains row by row txt informantio 'class x,y,w,h' 
            txt_data = fl.readlines() ; print(f'\ndata : {txt_data}')
            fl.close()

            # function to find bboxes from initial image
            green_x1, green_x2, green_y1, green_y2, diff_x, diff_y, final_min_list, left_list, top_list  = display_boxes(img, txt_data)
            
            cropped_image,scale_x1, scale_x2, scale_y1, scale_y2 = crop_image_by_percentage(file,img,txt_data, percent, green_x1, green_x2, green_y1, green_y2,CROP_DIR_FOLDER,file_name)
            
            cv2.imshow('cropped',cropped_image)

            crop_txt(cropped_image,scale_x1, scale_x2, scale_y1, scale_y2,txt_data)

            

        print('\nFolder created!')

    cv2.waitKey(0)
    cv2.destroyAllWindows()




