import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import sklearn
import tqdm
from tqdm import tqdm
import nltk
import warnings
warnings.filterwarnings("ignore") 
import cv2
from sklearn.model_selection import train_test_split
import PIL
from PIL import Image
import time

import tensorflow as tf
import keras
from keras.layers import Input,Dense,Conv2D,concatenate,Dropout,LSTM
from keras import Model
from tensorflow.keras import activations
import warnings
warnings.filterwarnings("ignore")
import nltk.translate.bleu_score as bleu


'''
First we need to load the chexnet nodel (DenseNet121),
The trained weight of this model is from https://github.com/brucechou1983/CheXNet-Keras

'''
#https://github.com/antoniosehk/tCheXNet/blob/master/chexnet.py
from tensorflow.keras.applications import DenseNet121

image_shape= (224,224,3)
image_input= Input(shape=(224,224,3))
base=DenseNet121(include_top=False,input_tensor=image_input,input_shape=image_shape,pooling="avg")
pred=Dense(14,"sigmoid")(base.output)

chexnet_model=Model(inputs=base.input,outputs=pred)
chexnet_model.load_weights("chexnet.h5")

# chexnet_model.summary()

final_chexnet_model=Model(inputs=chexnet_model.inputs,outputs=chexnet_model.layers[-2].output,name="Chexnet_model")

# tf.keras.utils.plot_model(final_chexnet_model,show_shapes=True,show_layer_names=True,to_file="chex.png") 
# Features Extraction of Image features from the Chexnet Model
image_1= Input(shape=(224,224,3),name="image_1_features")
image_2= Input(shape=(224,224,3),name="image_2_features")
image_1_out=final_chexnet_model(image_1)
image_2_out=final_chexnet_model(image_2)
conc=concatenate((image_1_out,image_2_out),axis=-1,name="final_image_features")
feature_extraction_model=Model(inputs=[image_1,image_2],outputs=conc)
# feature_extraction_model.summary() 


# tf.keras.utils.plot_model(feature_extraction_model,show_shapes=True,show_layer_names=True) 

#first we split the data set into train and test data sets
data=pd.read_csv("data.csv")

# train,test=train_test_split(data,test_size=0.2,random_state=1,shuffle=True)
# print(train.shape) 
# print(test.shape)
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')


'''
Obtaining the image feature for every patient using the feature extraction model which we had build earlier.
The output from this function is 2048 dimensiona vector for the x-ray set of every patient
'''

def image_feature_extraction(image1,image2):
  
 
  image_1 = Image.open(image1)
  
  image_1= np.asarray(image_1.convert("RGB"))
  
  
  image_2=Image.open(image2)
  image_2 = np.asarray(image_2.convert("RGB"))

    #normalize the values of the image
  image_1=image_1/255
  image_2=image_2/255

    #resize all image into (224,224)
  image_1 = cv2.resize(image_1,(224,224))
  image_2 = cv2.resize(image_2,(224,224))
    
  image_1= np.expand_dims(image_1, axis=0)
  image_2= np.expand_dims(image_2, axis=0)
    
    #now we have read two image per patient. this is goven to the chexnet model for feature extraction
    
  image_feature=feature_extraction_model([image_1,image_2])
  
  return image_feature

# Train the model

train_features=[]
test_features=[]
for row in tqdm(range(train.shape[0])):
  image_1=train.iloc[row]["image1"]
  image_2=train.iloc[row]["image2"]
  train_features.append(image_feature_extraction(image_1,image_2))
print("DONE")
for row in tqdm(range(test.shape[0])):
  image_1=test.iloc[row]["image1"] 
  image_2=test.iloc[row]["image2"]
  test_features.append(image_feature_extraction(image_1,image_2))


train["image_features"]=train_features
test["image_features"]=test_features

np.save("train_image_features",train_features)
np.save("test_image_features",test_features) 

train_features=np.load("train_image_features.npz")
train_features=train_features['arr_0']
test_features=np.load("test_image_features.npz")
test_features=test_features['arr_0']
print(train_features.shape)