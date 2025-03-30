import os
from random import choice
import shutil




trainImagePath = '/home/stayros/Desktop/certh/Callisto/Dataset/Callisto_dataset_v4/train/train_images'
trainLabelPath = '/home/stayros/Desktop/certh/Callisto/Dataset/Callisto_dataset_v4/train/train_Labels_YoloFormat'

testImagePath = '/home/stayros/Desktop/certh/Callisto/Dataset/Callisto_dataset_v4/test/test_images'
testLabelPath = '/home/stayros/Desktop/certh/Callisto/Dataset/Callisto_dataset_v4/test/test_Labels_YoloFormat'



# Count the number of files are in a directory.
#For train and test set

count_train = 0
# Iterate directory
for path in os.listdir(trainImagePath):
    # check if current path is a file
    if os.path.isfile(os.path.join(trainImagePath, path)):
        count_train += 1
print('Train image count:', count_train)


count_test = 0
# Iterate directory
for path in os.listdir(testImagePath):
    # check if current path is a file
    if os.path.isfile(os.path.join(testImagePath, path)):
        count_test += 1
print('Test image count:', count_test)








for x in range(count_train):

    fileJpg = choice(imgs) # get name of random image from origin dir
    fileXml = fileJpg[:-4] +'.txt' # get name of corresponding annotation file

    #move both files into train dir
    #shutil.move(os.path.join(crsPath, fileJpg), os.path.join(trainimagePath, fileJpg))
    #shutil.move(os.path.join(crsPath, fileXml), os.path.join(trainlabelPath, fileXml))
    shutil.copy(os.path.join(crsPath, fileJpg), os.path.join(trainimagePath, fileJpg))
    shutil.copy(os.path.join(crsPath, fileXml), os.path.join(trainlabelPath, fileXml))


    #remove files from arrays
    imgs.remove(fileJpg)
    xmls.remove(fileXml)



#cycle for test dir   
for x in range(countForVal):

    fileJpg = choice(imgs) # get name of random image from origin dir
    fileXml = fileJpg[:-4] +'.txt' # get name of corresponding annotation file

    #move both files into train dir
    #shutil.move(os.path.join(crsPath, fileJpg), os.path.join(valimagePath, fileJpg))
    #shutil.move(os.path.join(crsPath, fileXml), os.path.join(vallabelPath, fileXml))
    shutil.copy(os.path.join(crsPath, fileJpg), os.path.join(valimagePath, fileJpg))
    shutil.copy(os.path.join(crsPath, fileXml), os.path.join(vallabelPath, fileXml))
    
    #remove files from arrays
    imgs.remove(fileJpg)
    xmls.remove(fileXml)

#rest of files will be validation files, so rename origin dir to val dir
#os.rename(crsPath, valPath)
shutil.move(crsPath, valPath) 