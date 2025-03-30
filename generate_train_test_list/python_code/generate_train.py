import os

image_files = []
# os.chdir(os.path.join("data", "train", "all_train"))
# os.chdir(os.path.join("data-orf-7Shield", "train"))

path = "/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train/train_YOLO_with_img"

# for filename in os.listdir(os.getcwd()):
for filename in os.listdir(path):
    if filename.endswith(".jpg"):
        image_files.append("data/obj/" + filename)

os.chdir("..")

with open("train.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")

print("\nDone! \nTrain path created")