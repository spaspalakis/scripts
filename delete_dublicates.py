from curses import doupdate
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict
import hashlib



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
    
    #dimiourgw ena path (txt arxeio) pou apothikeuei oles tis klasseis pou yparxoun sta arxeia twn xml
    input_file_path = "./classes.txt"
    
    #dimiourgw ena teliko arxeio pou tha apothikeutoun en teli oles oi classes xwris duplicates  
    output_file_path = "/home/stayros/Desktop/ISOLA_orf/classes_out.txt"
    dublicate(input_file_path,output_file_path)