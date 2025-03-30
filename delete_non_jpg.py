import os

path = "/home/stayros/Desktop/7Shield_orf/train"

for file in os.listdir(path) :
    if not(file.endswith('.jpg')) :
        os.remove(file) 