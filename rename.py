import os
import glob

'''

count = 0
# path = "/home/stayros/Desktop/ibm dataset/photos1_p2_mission"

for i in os.listdir():
    os.rename(i,str(count)+ '.'+ i.split('.')[-1])
    count+=1

'''



# folderPath = "/home/stayros/Desktop/ibm dataset/photos1_p2_mission"


os.chdir(r"/home/stayros/Desktop/ibm dataset/photos1_p2_mission")

for index, oldfile in enumerate(glob.glob("*.jpg"), start=1):
    newfile = '{}.jpg'.format(index)
    os.rename (oldfile,newfile)