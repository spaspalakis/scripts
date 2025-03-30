import os
import xml.etree.ElementTree as ET


def read_class_mapping(mapping_file):
    class_mapping = {}
    with open(mapping_file, 'r') as file:
        for index, line in enumerate(file):
            class_name = line.strip()
            class_mapping[class_name] = index
    return class_mapping


def convert_voc_to_yolo(xml_file, output_folder, class_mapping):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    image_name = os.path.splitext(os.path.basename(xml_file))[0]
    image_width = int(root.find('size/width').text)
    image_height = int(root.find('size/height').text)

    txt_file_path = os.path.join(output_folder, image_name + '.txt')
    with open(txt_file_path, 'w') as txt_file:
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in class_mapping:
                continue

            class_id = class_mapping[class_name]

            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            x_center = (xmin + xmax) / (2 * image_width)
            y_center = (ymin + ymax) / (2 * image_height)
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            line = f"{class_id} {x_center} {y_center} {width} {height}\n"
            txt_file.write(line)


def convert_folder_voc_to_yolo(input_folder, output_folder, class_mapping_file):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    class_mapping = read_class_mapping(class_mapping_file)

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.xml'):
            xml_file = os.path.join(input_folder, file_name)
            convert_voc_to_yolo(xml_file, output_folder, class_mapping)


# Example usage
input_folder = '/home/stayros/Desktop/sea_drones_val_xml/val-final'
output_folder = '/home/stayros/Desktop/sea_drones_val_xml/val-yolo'
class_mapping_file = '/home/stayros/Desktop/sea_drones_val_xml/classes.txt'

convert_folder_voc_to_yolo(input_folder, output_folder, class_mapping_file)
