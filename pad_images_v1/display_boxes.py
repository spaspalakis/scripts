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


def display_boxes(img, data):
    
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


    
    return  diff_x, diff_y, left_list, top_list