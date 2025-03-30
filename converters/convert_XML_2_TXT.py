from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict
import os

class XMLHandler:
    def __init__(self, xml_path: str or Path):
        self.xml_path = Path(xml_path)
        self.root = self.__open()

    def __open(self):
        with self.xml_path.open() as opened_xml_file:
            self.tree = ET.parse(opened_xml_file)
            return self.tree.getroot()

    def return_boxes_class_as_dict(self) -> Dict[int, Dict]:
        """
        Returns Dict with class name and bounding boxes.
        Key number is box number

        :return:
        """

        boxes_dict = {}
        for index, sg_box in enumerate(self.root.iter('object')):
            boxes_dict[index] = {"name": sg_box.find("name").text,
                                 "xmin": int(sg_box.find("bndbox").find("xmin").text),
                                 "ymin": int(sg_box.find("bndbox").find("ymin").text),
                                 "xmax": int(sg_box.find("bndbox").find("xmax").text),
                                 "ymax": int(sg_box.find("bndbox").find("ymax").text)}

        return boxes_dict


# def converter(xml_files, output_folder) :
def converter(xml_files: str, output_folder: str) -> None:
    """
    Function converts pascal voc formatted files into ODM-File format

    :param xml_files: Path to folder with xml files
    :param output_folder: Path where results files should be written
    :return:
    """
    xml_files = sorted(list(Path(xml_files).rglob("*.xml")))
    # xmlPaths = glob(xml_files + "/*.xml")
    # print(xmlPaths)

    ext = '.txt'
    for xml_index, xml_path in enumerate(xml_files, start=1):
        
        print(f'xml_path: {xml_path}, type: {type(xml_path)}, str: {str(xml_path)}')   # /home/spaspalakis/Desktop/certh/Callisto/Dataset/Callisto_dataset_v2/callisto_train/24479005_15_1.xml
        print(f'xml_index: {xml_index}, type: {type(xml_path)}') #filename_path: /home/spaspalakis/Desktop/certh/Callisto/Dataset/Callisto_dataset_v2/train_txt/000000849.txt

        filename = os.path.splitext(str(os.path.basename(xml_path))[:-4])[0]
        # filename = f"{xml_index:09}.txt"
        print(f'filename: {filename}\n')
        
        # # filename_path = Path(output_folder) / filename
        filename_path = output_folder + '/' +filename
        print(f'filename_path: {filename_path}\n')

        # print(f'filename_path: {filename_path}')
        xml_content = XMLHandler(xml_path)
        # print(f'\nxml_content :{xml_content}')
        boxes = xml_content.return_boxes_class_as_dict()
        # print(f'boxes: {boxes}')

        with open(filename_path + '.txt', "w") as f:
            for box_index in boxes:
                box = boxes[box_index]
                box_content = f"{box['name']} {box['xmin']} {box['ymin']} {box['xmax']} {box['ymax']}\n"
                f.write(box_content)

  
    print(f"\nConverted {len(xml_files)} files!")

    
if __name__ == '__main__':
    
    XML_FOLDER = "/home/stayros/Documents/certh/projects/TREEADS/Dataset/TREEADS_dataset_v4_filtered/val/annotations"
    OUTPUT_FOLDER =  "/home/stayros/Documents/certh/projects/TREEADS/Dataset/TREEADS_dataset_v4_filtered/val/labels"
    converter(XML_FOLDER, OUTPUT_FOLDER)

    # all_img_path = '/home/spaspalakis/Desktop/certh/Callisto/Dataset/Callisto_dataset_v2'
    # all_xml_path = "/home/spaspalakis/Desktop/certh/Callisto/Dataset/Callisto_dataset_v2/callisto_train"
    # output_folder = "/home/spaspalakis/Desktop/certh/Callisto/Dataset/Callisto_dataset_v2/train_txt"
    # converter(all_xml_path, output_folder)
    
