import os
import shutil
import xml.etree.ElementTree as ET

def change_class_names(xml_file, class_mapping):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        name = obj.find('name').text
        if name in class_mapping:
            new_class_name = class_mapping[name]
            obj.find('name').text = new_class_name

    return tree


def change_filename(tree, output_file):
    root = tree.getroot()

    filename_element = root.find('filename')
    filename = filename_element.text

    if filename.endswith('.png'):
        new_filename = filename[:-4] + '.jpg'
        filename_element.text = new_filename

    tree.write(output_file)


def process_folder(input_folder, output_folder, class_mapping):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file_name in os.listdir(input_folder):
        print(file_name)
        if file_name.endswith('.xml'):
            input_xml = os.path.join(input_folder, file_name)
            output_xml = os.path.join(output_folder, file_name)

            tree_class = change_class_names(input_xml, class_mapping)
            change_filename(tree_class, output_xml)



# Example usage
input_folder = '/home/stayros/Desktop/sea_drones_val_xml/annotations'

output_folder = '/home/stayros/Desktop/sea_drones_val_xml/val-final'

class_mapping = {
    '1': 'person',
    '2': 'person',
    '3': 'boat'
}

process_folder(input_folder, output_folder, class_mapping)

print('\nEnd of proccess!')