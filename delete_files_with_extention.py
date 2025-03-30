import os

dir_name = "/home/stayros/Desktop/jetson_test_dataset/crop_imgs"
test = os.listdir(dir_name)
for item in test:
    if item.endswith(".txt"):
        os.remove(os.path.join(dir_name, item))

print(f'Done!')