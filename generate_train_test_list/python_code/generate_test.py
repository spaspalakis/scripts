import os

image_files = []
# os.chdir(os.path.join("data", "test","all_test"))
# os.chdir(os.path.join("data-orf-7Shield", "test"))

path = "/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/val/val_YOLO_with_img"
# for filename in os.listdir(os.getcwd()):
for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        image_files.append("data/test/" + filename)
os.chdir("..")
with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")

print("\nDone! \nTest path created")