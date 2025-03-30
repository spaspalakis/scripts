
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


def crop_txt(folder_path,file_name,cropped_image,scale_x1, scale_y1,txt_data,percent,left_list, top_list,diff_x, diff_y):

    
    crop_h, crop_w, _ = cropped_image.shape 

    with open(f'{folder_path}/{file_name}_crop_{percent}.txt', 'w') as crop_txt:

        # we run every object of of txt file
        for i, dt in enumerate(txt_data):
            
            crop_bbox_x1 =  abs(scale_x1 - left_list[i]) 
            crop_bbox_y1 =  abs(scale_y1 - top_list[i]) 
            
            # Here we add the width and height of every object in order to create the appropriate bbox
            crop_bbox_x2 =  crop_bbox_x1 + diff_x[i]  
            crop_bbox_y2 =  crop_bbox_y1 + diff_y[i]  

            if crop_bbox_x1 < 0:
                crop_bbox_x1 = 0

            if crop_bbox_x2 > crop_w - 1:
                crop_bbox_x2 = crop_w - 1

            if crop_bbox_y1 < 0:
                crop_bbox_y1 = 0

            if crop_bbox_y2 > crop_h - 1:
                crop_bbox_y2 = crop_h - 1
            
            # print(f'crop_bbox_x1: {crop_bbox_x1}')
            # print(f'crop_bbox_y1: {crop_bbox_y1}')
            # print(f'crop_bbox_x2: {crop_bbox_x2}')
            # print(f'crop_bbox_y2: {crop_bbox_y2}')

            crop_bbox = (crop_bbox_x1, crop_bbox_x2, crop_bbox_y1, crop_bbox_y2)
            x,y,w,h = XY_to_YOLO((crop_w,crop_h), crop_bbox)
            
            #print(f'txt row {i}: {dt[0]} {x} {y} {w} {h}')
            crop_txt.write(f'{dt[0]} {x} {y} {w} {h}\n')

        print(f'\nTXT for cropped [ {file_name} ] created ')
    
    # crop_txt.close()

    return crop_bbox_x1,crop_bbox_y1,crop_bbox_x2,crop_bbox_y2