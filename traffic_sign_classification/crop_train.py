from matplotlib import pyplot as plt

import os
import json
import cv2

ROOT_DIR= "C:/Users/yasemin/Desktop/internvL/ann/"
json_names=os.listdir(ROOT_DIR)
print(json_names)

def return_image_name(json_name):
  return json_name[:-8]+"jpg"

i=0
for jsn in json_names:
  JSON_PATH=os.path.join(ROOT_DIR,jsn)
  IMG_PATH="C:/Users/yasemin/Desktop/internvL/img"

  with open(JSON_PATH,'r') as f:
    jsnfile=json.load(f)
    json_obj=jsnfile['objects']
    for obj in json_obj:
      if obj['classTitle']=="Traffic Sign":
        img_name=return_image_name(jsn)
        img_path=os.path.join(IMG_PATH,img_name)

        print(img_path)
    
        obj_class_pts = obj['points']['exterior']
        x_0=obj_class_pts[0][0]
        y_0=obj_class_pts[0][1]
        x_1=obj_class_pts[1][0]
        y_1=obj_class_pts[1][1]

        img = cv2.imread(img_path)

        w = x_1 - x_0
        h = y_1 - y_0

       
        try:
            crop_img = img[y_0:y_0+h, x_0:x_0+w]
            plt.imshow(crop_img)
            out_path=os.path.join("C:/Users/yasemin/Desktop/internvL/cropped",str(i)+".png")
            cv2.imwrite(out_path,crop_img)
            i+=1
        except ValueError:
            pass