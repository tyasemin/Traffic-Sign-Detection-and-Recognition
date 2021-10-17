from matplotlib.pyplot import get
from sklearn.metrics import classification_report
from keras import models 
import pandas as pd
import os
import cv2
from PIL import Image
import numpy as np
import matplotlib.pylab as plt

def get_sign_name(i):
    class_names =[
    'Speed Limit 20 km/h',
    'Speed Limit 30 km/h',
    'Speed Limit 50 km/h',
    'Speed Limit 60 km/h',
    'Speed Limit 70 km/h',
    'Speed Limit 80 km/h',
    'End of Speed Limit 80 km/h',
    'Speed Limit 100 km/h',
    'Speed Limit 120 km/h',
    'No Passing',
    'Overtaking Prohibited for Trucks',
    'Side Roads to Right and Left',
    'Piority Road Ahead',
    'Give Way to All Traffic',
    'Stop',
    'Entry Not Allowed / Forbidden',
    'Lorries - Trucks Forbidden',
    'No Entry (One-Way Traffic)',
    'Warning',
    'Road Ahead Curves to the Left Side',
    'Road Bends to the Right',
    'Double Curve Ahead to the Left Then to the Right',
    'Poor Road Surface Ahead',
    'Slippery Road Surface Ahead',
    'Road Gets Narrow On the Right Side',
    'Roadworks Ahead Warning',
    'Traffic Light Ahead',
    'Warning for Pedestrians',
    'Warning for Children And Minors',
    'Warning for Bikes And Cyclists',
    'Warning for Snow And Sleet',
    'Deer Crossing in Area - Road',
    'End of All Prohibitions and Restrictions',
    'Turning Right Compulsory',
    'Left Turn Mandatory',
    'Ahead Only',
    'Driving Straight Ahead or Turning Right Mandatory',
    'Driving Straight Ahead or Turning Left Mandatory',
    'Pass on Right Only',
    'Passing Left Compulsory',
    'Direction of Traffic on Roundabout',
    'End of the Overtaking Prohibition',
    'End of the Overtaking Prohibition for Trucks']

    return class_names[i]

def return_ids(ROOT):
    path=os.path.join(ROOT,"DATASET")
    csv=pd.read_csv(os.path.join(path,"Test.csv"))
    id=csv["ClassId"].values
    return id

def prepare_test_set(ROOT):
    path=os.path.join(ROOT,"DATASET")
    csv=pd.read_csv(os.path.join(path,"Test.csv"))
    img_paths=csv["Path"].values

    test_images=[]
    for i_path in img_paths:
        image=cv2.imread(os.path.join(path,i_path))
        #print(os.path.join(path,i_path))
        image = Image.fromarray(image, 'RGB')
        image = image.resize((32, 32))
        test_images.append(np.array(image))
    
    test_images=(np.array(test_images))/255 #normalize set
    return test_images

def get_prediction(ROOT):
    test_set=prepare_test_set(ROOT) #get test images

    #load model
    try:
        model=models.load_model(os.path.join(ROOT,"classification_model.h5"))
        prediction=np.argmax(model.predict(test_set),axis=1)
    except:
        print("Error while loading the model")

    return prediction

def visualization(ROOT):
    model_prediction=get_prediction(ROOT) #get predictions
    id=return_ids(ROOT) #get labels
    test_set=prepare_test_set(ROOT) #get images

    fig = plt.figure(figsize=(20,14))
    rows = 4
    columns = 4
    ii=1
    for i in range(1,17):
        image = test_set[i]
        fig.add_subplot(rows, columns, ii)
        plt.subplots_adjust(top = 0.9, bottom=0.1, hspace=1, wspace=0.4)
        ii+=1
        plt.imshow(image)
        plt.axis('off')
        plt.title("Class id(prediction): {pred}".format(pred=model_prediction[i])+"\n"+
                   get_sign_name(model_prediction[i])+"\n"+
                   "Ground Truth: {gt}".format(gt=id[i]),fontsize=10)
    plt.show()



visualization(".../FOv1")    
