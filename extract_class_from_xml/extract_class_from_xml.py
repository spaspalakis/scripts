from curses import doupdate
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict
import hashlib

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
            boxes_dict[index] = {"name": sg_box.find("name").text}

        return boxes_dict



def converter(xml_files: str) -> None:
    """
    Function converts pascal voc formatted files into ODM-File format

    :param xml_files: Path to folder with xml files
    :param output_folder: Path where results files should be written
    :return:
    """
    xml_files = sorted(list(Path(xml_files).rglob("*.xml")))

    for xml_index, xml in enumerate(xml_files, start=1):
        filename = f"{xml_index:09}.txt"
        # filename_path = Path(output_folder) / filename
        xml_content = XMLHandler(xml)
        boxes = xml_content.return_boxes_class_as_dict()

        print(f"boxes : {boxes[0]['name']}")

        f = open("all_classes.txt", "a")            
        f.write(boxes[0]['name'] + "\n")
        f.close()

       
                
        # with open(filename_path, "a") as file:
        #     for box_index in boxes:
        #         box = boxes[box_index]
        #         box_content = f"{box['name']} {box['xmin']} {box['ymin']} {box['xmax']} {box['ymax']}\n"
        #         file.write(box_content)

    print(f"Converted {len(xml_files)} files!")


def dublicate(input_file_path,output_file_path):


        #2
        completed_lines_hash = set()

        #3
        output_file = open(output_file_path, "w")

        #4
        for line in open(input_file_path, "r"):
        #5
            hashValue = hashlib.md5(line.rstrip().encode('utf-8')).hexdigest()
        #6
            if hashValue not in completed_lines_hash:
                output_file.write(line)
                completed_lines_hash.add(hashValue)
        #7
        output_file.close()


if __name__ == '__main__':
    
    #xml annotation path
    XML_FOLDER = "/home/stayros/Documents/certh/projects/TREEADS/TREEADS_dataset_v1_filtered/train/annotations"
    converter(XML_FOLDER)

    #dimiourgw ena path (txt arxeio) pou apothikeuei oles tis klasseis pou yparxoun sta arxeia twn xml
    input_file_path = "./all_classes.txt"
    
    #dimiourgw ena teliko arxeio pou tha apothikeutoun en teli oles oi classes xwris duplicates  
    output_file_path = "./classes_out.txt"
    dublicate(input_file_path,output_file_path) 