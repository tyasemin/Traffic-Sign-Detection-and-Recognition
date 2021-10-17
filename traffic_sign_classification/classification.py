import os
import cv2
from PIL import Image
import numpy as np
np.random.seed(40)
from sklearn.model_selection import train_test_split
from tensorflow import keras
import tensorflow as tf
from keras import models 
import pandas as pd
import matplotlib.pyplot as plt
from augmentation import augmentation
from tensorflow.keras.optimizers import Adam
#returs number of classes in dataset
def get_number_of_classes(path):
    return len(os.listdir(path))

def shuffle_dataset(image_arr,label_arr):
    index= np.arange(image_arr.shape[0])
    np.random.shuffle(index)
    image_arr = image_arr[index]
    label_arr = label_arr[index]

    return image_arr,label_arr

def split_data(image_arr,label_arr):
    x_train, x_val, y_train, y_val = train_test_split(image_arr, label_arr, test_size=0.3, random_state=40, shuffle=True)
    
    #normalize images
    x_train = x_train/255 
    x_val = x_val/255

    return x_train,x_val,y_train,y_val

def one_hot_encoding(y_train,y_val,number_of_classes):
    y_train = keras.utils.to_categorical(y_train, number_of_classes)
    y_val = keras.utils.to_categorical(y_val, number_of_classes)

    return y_train,y_val

#takes train dataset's path
#prepares data for training
#returns images and labels 
def prepare_data(path):
    images=[]
    labels=[]
    class_number=get_number_of_classes(path)
    for i in range(class_number):
        class_path=os.path.join(TRAIN_DIR,str(i))
        image_names = os.listdir(class_path)

        for iname in image_names:
            img=cv2.imread(os.path.join(class_path,iname))
            image_fromarray = Image.fromarray(img, 'RGB')
            resized_image = image_fromarray.resize((32,32))
            images.append(np.array(resized_image))
            labels.append(i)
    
    images=np.array(images)
    labels=np.array(labels)

    images,labels=shuffle_dataset(images,labels)
    train_x,val_x,train_y,val_y=split_data(images,labels)
    train_y,val_y=one_hot_encoding(train_y,val_y,class_number)

    return train_x,val_x,train_y,val_y

def training(path,ROOT):
    augmentation(path)
    train_x,val_x,train_y,val_y=prepare_data(path)
    model_base = tf.keras.applications.resnet_v2.ResNet50V2(weights='imagenet', include_top=False, pooling='max', input_shape = (32,32, 3))
    
    model = models.Sequential()
    #adds classifier layer to resnet50v2
    model.add(model_base)
    model.add(keras.layers.Dense(43, activation='softmax')) 

    train_step=train_x.shape[0]//32 #to find step size, the train dataset must be split with batch size. In this scenario batch size is 32

    model.compile(loss="categorical_crossentropy", optimizer=Adam(lr=0.00005), metrics = ['accuracy'])
    history = model.fit(train_x, train_y, batch_size=32, steps_per_epoch=train_step,epochs=10,validation_data=(val_x, val_y),verbose=1)
    
    model.save(os.path.join(ROOT,"classification_model.h5"))
    plt.plot(history.history['loss'],label='training loss list')
    plt.plot(history.history['val_loss'],label='validation loss list')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()

    plt.plot(history.history['accuracy'],label="accuracy")
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()

    

ROOT='.../FOv1'
DATASET_DIR=os.path.join(ROOT,"DATASET")
TRAIN_DIR=os.path.join(DATASET_DIR,"Train")

training(TRAIN_DIR,ROOT)
