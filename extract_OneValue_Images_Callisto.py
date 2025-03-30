"""
DISCLAIMER
------------
This script access the .txt of every class and extract the images with value 1.
The it creates another .txt file only with those images

MORE DETAILS
-------------

Firstly we read the inital .txt file with the corresponding class we want to extract.
The result is stored into Lines value.
Lines is a list of all the rows of the dataset seperated with comma ','

e.g. Line = ['00001 -1\n', '00002 -1\n', '00017 -1\n', ...]

Then we write the path of the new .txt file we want to save the images of the spesific class.
If the file does not exixt it will be created automatically, just typing the path and the name of the file.txt

We access the dataset file with the for loop.
We split every row of the dataset (split_lines) and create new lists for every row (list_of_rows)

e.g. list_of_rows = ['00001', '-1']  ['00001', '-1']

The first value correspond to the image number and the second value corresponds to a binary 1 or -1 
1 means that the images contains the class -1 means tha does nto contained

For every dataset we want to extract, we store only the images with the 1 value contained
"""


# Read dataset that you want to extract e.g. bridge, crossroad etc.
# This changes every time
with open('/home/spaspalakis/Desktop/TGRS-HRRSD-Dataset/OPT2017/ImageSets/Main/crossroad_train.txt', 'r') as file:
    Lines = file.readlines()
    print('\nClass file was read')


# Create the new .txt file that you want to store the values. If the file doesn't exist, it will be created automatically
# This changes every time
with open('/home/spaspalakis/Desktop/TGRS-HRRSD-Dataset/crossroad_train_ones.txt', 'w') as f:
    
    for idx, l in enumerate (Lines):

        split_lines = l.split(",") # Splits every line from the Lines file and seperates attributes e.g. 21759 -1, 21761 -1
        # print(split_lines[0])
        
        list_of_rows = split_lines[0].split() # Create seperate list for each attribute which contains each row values
        # print(list_of_words)                   # e.g. ['21759', '-1']  ['21761', '-1']
        
        first_value = list_of_rows[0] #first value is string. Here we store the number of the image e.g.21759, 21761 etc.
        # print(type(first_value))
        # print(f'first_value',first_value)

        sec_value = list_of_rows[1] # Get the second value its -1 or 1
        # print(f'sec_word',sec_value)

        if sec_value == '1':
            # print(idx,l)
                f.write(first_value)
                f.write('\n')
    
    print('\nProcess ended.\nOnes file created')
f.close()


