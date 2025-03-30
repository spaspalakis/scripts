import os

def delete_jpg(files):
    for i in range(len(files)):
        if files[i].split(".")[0] + ".txt" not in files:
                # print(f"\ndeleted image:{dir+str(i)}")
                print(f"\nDeleted image: {dir}/{files[i]}")
                os.remove(dir+"/"+files[i])




if __name__ == '__main__':
    
    dir ="/home/stayros/Desktop/test"

    files = os.listdir(dir)

    all_files=len(files)
    print(f"all files : {all_files}")
    

    delete_jpg(files)

    files = os.listdir(dir)
    after_deletion = len(files)
    print(f"\nafter_deletion: {after_deletion}")

    deleted = all_files - after_deletion
    print(f"\nDeleted [ {deleted} ] files from folder")