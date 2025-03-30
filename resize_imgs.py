from PIL import Image
import glob

image_list = []
resized_images = []
path = '/home/stayros/Desktop/asd/test_original'

for filename in glob.glob(f'{path}\\*.jpg'):
    print(filename)
    img = Image.open(filename)
    image_list.append(img)

for image in image_list:
    image = image.resize((640, 480))
    resized_images.append(image)

for (i, new) in enumerate(resized_images):
    new.save(f'{path}\\', {i+1}, '.jpg')

print('\nFinished')