
import cv2

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

def YOLO_to_XY(x,y,w,h,img_w,img_h):
        
    # convert YOLO coordinates to x1,y1,x2,y2 format
    left = int((x - w / 2) * img_w) 
    right = int((x + w / 2) * img_w) 
    top = int((y - h / 2) * img_h)
    bottom = int((y + h / 2) * img_h) 

    #print 
    # print(f'\nLeft (X1): {left}')  # x1
    # print(f'Right (X2): {right}')  # x2
    # print(f'Top (Y1): {top}')  # y1
    # print(f'Bottom (Y2): {bottom}\n')  # y2

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


def pad_txt(crop_folder,pad_dir_folder,\
        file_name,cropped_img,padded_image,percent, \
        diff_x,diff_y,left_pad,top_pad):
    
    print('\n------ Pad TXT -------')
    cropped_txt = open(f'{crop_folder}{file_name}.txt', 'r')           
    cropped_txt_data = cropped_txt.readlines() #; print(f'\ncropped txt data : {cropped_txt_data}')
    cropped_txt.close()

    crop_h, crop_w, _ = cropped_img.shape     
    pad_h, pad_w, _ = padded_image.shape     

    print(f'{pad_dir_folder}/{file_name}_pad.txt')
    with open(f'{pad_dir_folder}/{file_name}_pad.txt', 'w') as pad_txt:

        # we run every object of of txt file
        for i, dt in enumerate(cropped_txt_data):
            
            _, x, y, w, h = map(float, dt.split(' ')) #; print(f'\nx: {x}\ny: {y}\nw: {w}\nh: {h}')
            crop_left, crop_right, crop_top, crop_bottom = YOLO_to_XY(x, y, w, h, crop_w, crop_h)

            pad_bbox_x1 = crop_left + left_pad
            pad_bbox_y1 = crop_top + top_pad
                        
            pad_bbox_x2 =  pad_bbox_x1 + diff_x[i]  
            pad_bbox_y2 =  pad_bbox_y1 + diff_y[i]  


            pad_bbox = (pad_bbox_x1, pad_bbox_x2, pad_bbox_y1, pad_bbox_y2)
            x,y,w,h = XY_to_YOLO((pad_w,pad_h), pad_bbox)
                
            #print(f'txt row {i}: {dt[0]} {x} {y} {w} {h}')
            pad_txt.write(f'{dt[0]} {x} {y} {w} {h}\n')
            # print(f'\nTXT for padded {file_name} created ')
            # pad_txt.close()

            # cv2.rectangle(padded_image, (pad_bbox_x1, pad_bbox_y1), (pad_bbox_x2, pad_bbox_y2), (0, 255, 0), 2)
            # cv2.imshow('padded', padded_image)
            
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

    return 