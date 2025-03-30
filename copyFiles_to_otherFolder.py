import glob, os, shutil


SOURCE_DIR = r'/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/val/images/'    #needs '/' at the end of the path

DEST_DIR = r'/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/val/val_YOLO_with_img/'    #needs '/' at the end of the path

EXTENSION = '.jpg'

files = glob.iglob(os.path.join(SOURCE_DIR,f"*{EXTENSION}"))
for file in files:
    if os.path.isfile(file):
        shutil.copy2(file, DEST_DIR)

print('\nProcess is finished!')