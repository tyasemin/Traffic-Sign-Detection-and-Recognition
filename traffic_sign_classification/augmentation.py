import os
import numpy as np
from PIL import Image,ImageEnhance,ImageFilter
import random
import tqdm
#finds max size in dataset
def find_max_size(arr):
    return np.amax(arr)

#takes class size in train set
def get_class_sizes(arr,ROOT):
    class_names=os.listdir(ROOT)
    for cname in class_names:
        class_path=os.path.join(ROOT,cname)
        csize=len(os.listdir(class_path))
        arr.append(csize)
    return arr

#applys random augmentation method to the image 
def apply_augmentation(img):

    rnd=random.randint(0,7)

    #rotates img 15 degree
    if rnd==0:
        rotated = img.rotate(15)
        return rotated

    #rotates img 30 degree
    if rnd==1:
        rotated=img.rotate(30)
        return rotated

    #increases brightness
    if rnd==2:
        enhancer = ImageEnhance.Brightness(img)
        im_output = enhancer.enhance(1.25)
        return im_output
    
    #decreases brightness
    if rnd==3:
        enhancer = ImageEnhance.Brightness(img)
        im_output = enhancer.enhance(0.75)
        return im_output

    #adds noise 
    if rnd==4:
        im_output = img.filter(ImageFilter.GaussianBlur(1))
        return im_output
    
    #changes color saturation
    if rnd==5:
        converter = ImageEnhance.Color(img)
        im_output = converter.enhance(0.5)
        return im_output
    
    if rnd==6:
        converter = ImageEnhance.Color(img)
        im_output = converter.enhance(1)
        return im_output

    if rnd==7:
        converter = ImageEnhance.Color(img)
        im_output = converter.enhance(2)
        return im_output


#finds smaller sets and implements augmentation
def augmentation(path):
    ROOT=path
    class_sizes=[]
    class_sizes=get_class_sizes(class_sizes,ROOT)
    tmp_sizes=class_sizes
    class_names=os.listdir(ROOT)
    max_size=np.amax(tmp_sizes)
    
    for i in tqdm.tqdm(range(len(class_sizes))):

        #augmentation
        if class_sizes[i]<max_size:
            class_path=os.path.join(ROOT,class_names[i])
            
            #finds image names in the class
            img_names=os.listdir(class_path)
            
            #opens images in the class
            id=0
            ii=0
            process_size=max_size-tmp_sizes[i]
            while ii <=process_size:
                img_path=os.path.join(class_path,img_names[ii])
                img_out_path=os.path.join(class_path,str(id)+"a.png")
                print(img_path)
                
                #implements augmentation
                img=Image.open(img_path)
                aug_img=apply_augmentation(img)
                aug_img.save(img_out_path)
                id+=1
                ii+=1
                #if after augmentation, class size is still smaller than max size, repeat process
                if ii==class_sizes[i]:
                    img_names=os.listdir(class_path)
                    class_sizes[i]=len(img_names)
                


