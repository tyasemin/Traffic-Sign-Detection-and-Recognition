import os
import tqdm
import json

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

JSON_TXT_DIR=os.path.join(__location__,"allLabel.txt")

#read file (path and label)
file=open(JSON_TXT_DIR,"r")
allLabel_raw=file.readlines() #iterable
file.close()

allLabel=[]
file=open(os.path.join(__location__,"allLabel_modified.txt"),"w")
for line in allLabel_raw:
    line=line.strip()
    
    if line.find(" ") !=-1: #if json has bbox
        file.write(line+"\n")


file.close()
