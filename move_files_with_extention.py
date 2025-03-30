import os
import shutil


sourcepath='/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/val/val_XML_with_img'

sourcefiles = os.listdir(sourcepath)

destinationpath = '/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/val/val_YOLO_with_img'


for file in sourcefiles:
    if file.endswith('.txt'):
        shutil.move(os.path.join(sourcepath,file), os.path.join(destinationpath,file))

print("Done!")