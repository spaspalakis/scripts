from PIL import Image
import os

def convert_png_to_jpg(png_path, jpg_path):
    image = Image.open(png_path)
    rgb_image = image.convert('RGB')
    rgb_image.save(jpg_path, 'JPEG')

def batch_convert(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.png'):
            print(file_name)
            png_path = os.path.join(input_folder, file_name)
            jpg_path = os.path.join(output_folder, file_name.replace('.png', '.jpg'))
            convert_png_to_jpg(png_path, jpg_path)

# Example usage
input_folder = '/home/stayros/Desktop/sea_drones_val_xml/val-png'
output_folder = '/home/stayros/Desktop/sea_drones_val_xml/val-jpg'
batch_convert(input_folder, output_folder)
