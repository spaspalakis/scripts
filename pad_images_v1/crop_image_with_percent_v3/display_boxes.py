import cv2 

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



def find_min(left_list, top_list, right_list,bottom_list):

    final_min_list =[]

    left_list = min(left_list) #; 
    top_list = min(top_list) #; 
    right_list = max(right_list) #; 
    bottom_list = max(bottom_list) #; 

    #print
    #print (f'\nmin left_list: {left_list}')
    # print (f'min top_list: {top_list}')
    # print(f'max right_list: {right_list}')
    # print(f'max bottom_list: {bottom_list}')

    final_min_list = [left_list, top_list, right_list, bottom_list]    
    # print(f'\nfinal min list: {final_min_list}\n')

    return final_min_list



def green_rec(img, final_min_list,left_list,top_list,right_list,bottom_list,disp_green_box):

    img_with_green_rec = img.copy()

    # print(f'\n----- Green Box ------\n')

    green_h, green_w, _ = img_with_green_rec.shape # w, h arxikis eikonas
    
    # print(f'green_w: {green_w}\ngreen_h: {green_h}\n')

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

    #display green box
    if disp_green_box : 
        cv2.rectangle(img_with_green_rec, (green_x1, green_y1), (green_x2, green_y2), (0, 255, 0), 2)
        cv2.imshow('img_with_green_rec', img_with_green_rec)
            
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return green_x1, green_x2, green_y1, green_y2


def display_boxes(img, data,disp_green_box):
    
    init_img = img.copy()

    img_h, img_w, _ = init_img.shape # w, h for initial image
    # print(f'\nimg_w: {img_w}\nimg_h: {img_h}\n')

    left_list = []
    top_list= []
    right_list = []
    bottom_list = []
    # final_min_list =[]
    diff_x = []
    diff_y =[]


    # Read every object into .txt file 
    for i, dt in enumerate(data):

        # print(f'\n---------------------\nObject: {i} | class: {dt[0]}\n')

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
        #cv2.rectangle(init_img, (left, top), (right, bottom), (0, 0, 255), 1)
    
    # display image
    # cv2.imshow('img_with_init_bboxes', img_with_initial_bboxes)

    """
    So after we saved x1,y1,x2,y2 for every object.
    Now we try to detect which bbox/object is the most left and the most right into the image
    In order to create the cropped bbox
    """

    #print(f'\n------ All listes -----\n\nleft_list: {left_list}\ntop_list: {top_list}\nright_list: {right_list}\nbottom_list: {bottom_list}')    

    # Find_min function, finds min(x1,y1) and max(x2,y2) in order to create green box/cropped window
    # final_min_list  is the list with those coordinates
    final_min_list = find_min(left_list, top_list, right_list,bottom_list)
    #print(f'\nfinal min list: {final_min_list}\n')

    # Print 
    #print (f'diff X: {diff_x}') # x2-x1 
    #print (f'diff Y: {diff_y}') # y2 -y1
    
    # Green_rec is the function which creats the new window with coordinates min(x1,y1) kai max(x2,y2)
    green_x1, green_x2, green_y1, green_y2 = green_rec(img, final_min_list,left_list,top_list,right_list,bottom_list,disp_green_box)

    # cv2.rectangle(init_img, (green_x1, green_y1), (green_x2, green_y2), (0, 255, 0), 1)
    # cv2.imshow('img_with_green_rec', init_img)
    
    return green_x1, green_x2, green_y1, green_y2, diff_x, diff_y, final_min_list, left_list, top_list