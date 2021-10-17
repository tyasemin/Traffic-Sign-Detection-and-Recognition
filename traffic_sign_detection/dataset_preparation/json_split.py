import os
import tqdm
import json

#get labels and paths
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

file=open(os.path.join(__location__,"allLabel_modified.txt"))
allLabel=file.readlines()
file.close()

#writes label paths to one file
def write_paths(allLabel):
    PATH_DIR=os.path.join(__location__,"all_path.txt")
    img_path_file=open(PATH_DIR,"w")
    for line in allLabel:
        line=line.strip()

        img_path=line.split(" ")[0]
        img_path=img_path+"\n"

        
        img_path_file.write(img_path)
    
    img_path_file.close()


#modifies labels for required order
def modify_label_order(lbl_raw):
    x_min,y_min,x_max,y_max,id=lbl_raw.split(",")
    width=int(int(x_max)-int(x_min))
    height=int(int(y_max)-int(y_min))
    x_center=int(int(x_min)+width/2)
    y_center=int(int(y_min)+height/2)


    lbl_mod=str(id)+" "+str(x_center/1920)+" "+str(y_center/1208)+" "+str(width/1920)+" "+str(height/1208)+"\n"
    return lbl_mod

def create_label(allLabel):
    #get image names
    IMG_DIR=os.path.join(__location__,"img")
    LABEL_OUT_DIR=os.path.join(__location__,"labels")
    
    #get image paths for names
    img_path_file=open(os.path.join(__location__,"all_path.txt"),"r")
    img_paths=img_path_file.readlines()
    img_path_file.close()

    for i in range(len(allLabel)):
        #find image name
        
        img_name=img_paths[i][29:-4]
        img_name=img_name+"txt"

        label_out_path=os.path.join(LABEL_OUT_DIR,img_name) #initialize label out path 

        #create label file
        label_file=open(label_out_path,"w")

        label_raw=allLabel[i].strip()
        label_raw=label_raw.split(" ")[1:] #take only labels

        for label in label_raw:
            label_file.write(modify_label_order(label)) #write modified format
        label_file.close()

write_paths(allLabel)
create_label(allLabel)

file.close()
