from flask import Flask, jsonify, request

from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("syrus-hackathon-p1-wmbglw-firebase-adminsdk-zb1cj-30dabc741e.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'gs://syrus-hackathon-p1-wmbglw.appspot.com'})

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
import re
import os
# import sklearn
import tqdm
from tqdm import tqdm 
# import nltk
import warnings
warnings.filterwarnings("ignore") 
# import cv2
from sklearn.model_selection import train_test_split
import PIL
from PIL import Image
import time

import tensorflow as tf
import keras
from keras.layers import Input,Dense,Conv2D,concatenate,Dropout,LSTM
from keras import Model
# from tensorflow.keras import activations
import warnings
warnings.filterwarnings("ignore")
# import nltk.translate.bleu_score as bleu

# load the dataset 
data = pd.read_csv('data.csv')
# Load train features and test featurs
# train_features=np.load(r"D:\Syrus24\test_image_features.npy")
# test_features=np.load(r"D:\Syrus24\train_image_features.npy")
train_features=np.load("train_image_features.npy")
test_features=np.load("test_image_features.npy")


'''
First we need to load the chexnet nodel (DenseNet121),
'''
from tensorflow.keras.applications import DenseNet121

    


# Image Feature Extraction N

def image_feature_extraction_n(image1, image2):
    image_1 = Image.open(image1)
    image_1 = np.asarray(image_1.convert("RGB"))

    image_2 = Image.open(image2)
    image_2 = np.asarray(image_2.convert("RGB"))

    # normalize the values of the image
    image_1 = image_1 / 255
    image_2 = image_2 / 255

    # resize all image into (224, 224)
    image_1 = cv2.resize(image_1, (224, 224))
    image_2 = cv2.resize(image_2, (224, 224))

    image_1 = np.expand_dims(image_1, axis=0)
    image_2 = np.expand_dims(image_2, axis=0)

    # now we have read two images per patient. These are given to the chexnet model for feature extraction
    image_1_out = final_chexnet_model(image_1)
    image_2_out = final_chexnet_model(image_2)

    # concatenate along the width
    conc = np.concatenate((image_1_out, image_2_out), axis=2)

    # reshape into (no. of images passed, length * breadth * depth)
    image_feature = tf.reshape(conc, (conc.shape[0], -1, conc.shape[-1]))

    # reshape for attention mechanism
    
    # image_feature_reshaped = tf.reshape(image_feature, (image_feature.shape[0], -1, image_feature.shape[-1]))
    image_feature_reshaped = tf.reshape(image_feature, (image_feature.shape[0], -1, 2048))

    return image_feature_reshaped


# Image Feature Extraction

def image_feature_extraction(image1, image2):
    image_1 = Image.open(image1)
    image_1 = np.asarray(image_1.convert("RGB"))

    image_2 = Image.open(image2)
    image_2 = np.asarray(image_2.convert("RGB"))

    # normalize the values of the image
    image_1 = image_1 / 255
    image_2 = image_2 / 255

    # resize all image into (224, 224)
    image_1 = cv2.resize(image_1, (224, 224))
    image_2 = cv2.resize(image_2, (224, 224))

    image_1 = np.expand_dims(image_1, axis=0)
    image_2 = np.expand_dims(image_2, axis=0)

    # now we have read two images per patient. These are given to the chexnet model for feature extraction
    image_1_out = final_chexnet_model(image_1)
    image_2_out = final_chexnet_model(image_2)

    # concatenate along the width
    conc = np.concatenate((image_1_out, image_2_out), axis=2)

    # reshape into (no. of images passed, length * breadth * depth)
    image_feature = tf.reshape(conc, (conc.shape[0], -1, conc.shape[-1]))

    # reshape for attention mechanism
    
    image_feature_reshaped = tf.reshape(image_feature, (image_feature.shape[0], -1, image_feature.shape[-1]))
    # image_feature_reshaped = tf.reshape(image_feature, (image_feature.shape[0], -1, 2048))

    return image_feature_reshaped

'''
Modify the reports as <sos> report text <eos>. This format is useful for the decoder while predicting the next word
'''
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
train_report=["<sos> "+text+" <eos>" for text in train["report"].values]
train_report_in=["<sos> "+text for text in train["report"].values]
train_report_out=[text+" <eos>" for text in train["report"].values]

test_report=["<sos> " +text+" <eos>" for text in test["report"].values]
test_report_in=["<sos> " +text for text in test["report"].values]
test_report_out=[text+" <eos>" for text in test["report"].values]  

bs=10
max_len=80

#Obtaining the text embeddings of the report
# we use the tensorflow tokenizer to convert the text into tokens
#we also pad the sequences to a length 300 which is around the 90th percentile of the lengths of the report

token=tf.keras.preprocessing.text.Tokenizer(filters='' )

token.fit_on_texts(train_report)
vocab_size=len(token.word_index)+1 

seq=token.texts_to_sequences(train_report_in)
train_padded_inp=tf.keras.preprocessing.sequence.pad_sequences(seq,maxlen=max_len,padding="post")


seq=token.texts_to_sequences(train_report_out)
train_padded_out=tf.keras.preprocessing.sequence.pad_sequences(seq,maxlen=max_len,padding="post")

seq=token.texts_to_sequences(test_report_in)
test_padded_inp=tf.keras.preprocessing.sequence.pad_sequences(seq,maxlen=max_len,padding="post")


seq=token.texts_to_sequences(test_report_out)
test_padded_out=tf.keras.preprocessing.sequence.pad_sequences(seq,maxlen=max_len,padding="post")


#now we prepare the data set with the image fetaures and the reports
train_dataset = tf.data.Dataset.from_tensor_slices((train_features,train_padded_inp,train_padded_out)).shuffle(500)
train_dataset = train_dataset.batch(bs, drop_remainder=True)

test_dataset = tf.data.Dataset.from_tensor_slices((test_features,test_padded_inp,test_padded_out)).shuffle(500)
test_dataset = test_dataset.batch(bs,drop_remainder=True) 






enc_units=64
embedding_dim=300
dec_units=64 
att_units=64



#  Encoder_n
#encoder model

class Encoder_n(tf.keras.Model):
  def __init__(self,units):
    super().__init__()
    self.units=units
    
  
  def build(self,input_shape):
    # self.dense1=Dense(self.units,activation="relu",name="encoder_dense")
    self.dense1=Dense(2048,activation="relu",name="encoder_dense")
      
       
    self.maxpool=tf.keras.layers.Dropout(0.5)

  def call(self, input_):
        try:
            enc_out = self.maxpool(input_)
            enc_out = self.dense1(enc_out)
            return enc_out
        except Exception as e:
            raise ValueError(f"Error in Encoder layer with input shape {input_.shape}: {str(e)}")
    
  def initialize_states(self,batch_size):
      '''
      Given a batch size it will return intial hidden state
      If batch size is 32- Hidden state shape is [32,units]
      '''
      forward_h=tf.zeros((batch_size,self.units))
      back_h=tf.zeros((batch_size,self.units))
      return forward_h,back_h

#encoder model
'''
here the input will be image features with size (96,1024). We can consider this tensor as the encoder output.
But here we add another dense layer that will reduce the depth of this feature from 1024 to a low value
'''

class Encoder(tf.keras.Model):
  def __init__(self,units):
    super().__init__()
    self.units=units
    
  
  def build(self,input_shape):
    self.dense1=Dense(self.units,activation="relu",name="encoder_dense")
    # self.dense1=Dense(2048,activation="relu",name="encoder_dense")
      
       
    self.maxpool=tf.keras.layers.Dropout(0.5)

  def call(self, input_):
        try:
            enc_out = self.maxpool(input_)
            enc_out = self.dense1(enc_out)
            return enc_out
        except Exception as e:
            raise ValueError(f"Error in Encoder layer with input shape {input_.shape}: {str(e)}")
    
  def initialize_states(self,batch_size):
      '''
      Given a batch size it will return intial hidden state
      If batch size is 32- Hidden state shape is [32,units]
      '''
      forward_h=tf.zeros((batch_size,self.units))
      back_h=tf.zeros((batch_size,self.units))
      return forward_h,back_h

'''
this is the attention class. 
Here the input to the decoder and the gru hidden state at the pevious time step are given, and the context vector is calculated

This context vector is calculated uisng the attention weights. This context vector is then passed to the decoder model

Here conact function is used for calaculating the attention weights

'''

class Attention(tf.keras.layers.Layer):

  def __init__(self,att_units):

    super().__init__()
    
    self.att_units=att_units

  def build(self,input_shape):
    self.wa=tf.keras.layers.Dense(self.att_units)
    self.wb=tf.keras.layers.Dense(self.att_units)
    self.v=tf.keras.layers.Dense(1)
  
    
  def call(self,decoder_hidden_state,encoder_output):
   
    x=tf.expand_dims(decoder_hidden_state,1)
    
    # print(x.shape)
    # print(encoder_output.shape)
      
    alpha_dash=self.v(tf.nn.tanh(self.wa(encoder_output)+self.wb(x)))
    
    alphas=tf.nn.softmax(alpha_dash,1)

    # print("en",encoder_output.shape)
    # print("al",alphas.shape)
    
    context_vector=tf.matmul(encoder_output,alphas,transpose_a=True)[:,:,0]
    # context_vector = alphas*encoder_output
    # print("c",context_vector.shape)


    return (context_vector,alphas)
  

'''
This class will perform the decoder task.
The main decoder will call this onestep decoder at every time step. This one step decoder in turn class the atention model and return the ouptput 
at time step t.
This output is passed through the final softmax layer with output size =vocab size, and pass this result to the main decoder model

'''

class One_Step_Decoder(tf.keras.Model):
  def __init__(self,vocab_size, embedding_dim, input_length, dec_units ,att_units):

      # Initialize decoder embedding layer, LSTM and any other objects needed
    super().__init__()
    
    self.att_units=att_units
    self.vocab_size=vocab_size
    self.embedding_dim=embedding_dim
    self.input_length=input_length
    
    self.dec_units=dec_units
    self.attention=Attention(self.att_units)
  #def build(self,inp_shape):
    self.embedding=tf.keras.layers.Embedding(self.vocab_size,output_dim=self.embedding_dim,
                                             input_length=self.input_length,mask_zero=True,trainable=False,weights=[embedding_matrix])

    self.gru= tf.keras.layers.Bidirectional(tf.keras.layers.GRU(self.dec_units,return_sequences=True, return_state=True))
    self.dense=tf.keras.layers.Dense(self.vocab_size,name="decoder_final_dense") 
    self.dense_2=tf.keras.layers.Dense(self.embedding_dim,name="decoder_dense2")

  def call(self,input_to_decoder, encoder_output, for_h,bac_h):
    
    embed=self.embedding(input_to_decoder)
    state_h=tf.keras.layers.Add()([for_h,bac_h])
    

    context_vector,alpha=self.attention(state_h,encoder_output)
    context_vector=self.dense_2(context_vector)

    result=tf.concat([tf.expand_dims(context_vector, axis=1),embed],axis=-1)
    
   
    output,forward_h,back_h=self.gru(result,initial_state=[for_h,bac_h])
    out=tf.reshape(output,(-1,output.shape[-1]))

    out=tf.keras.layers.Dropout(0.5)(out)
    
    dense_op=self.dense(out)
    
    return dense_op,forward_h,back_h,alpha
  

'''
For every input sentence, each output word is generated using one step decoder. Each output word is stored using the final decoder model and the
final output sentence is returned

'''

class Decoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, output_length, dec_units,att_units):
      super().__init__()
      #Intialize necessary variables and create an object from the class onestepdecoder
      self.onestep=One_Step_Decoder(vocab_size, embedding_dim, output_length, dec_units,att_units)


        
    def call(self, input_to_decoder,encoder_output,state_1,state_2):

        #Initialize an empty Tensor array, that will store the outputs at each and every time step
        #Create a tensor array as shown in the reference notebook
        
        #Iterate till the length of the decoder input
            # Call onestepdecoder for each token in decoder_input
            # Store the output in tensorarray
        # Return the tensor array
        
        all_outputs=tf.TensorArray(tf.float32,input_to_decoder.shape[1],name="output_array")
        for step in range(input_to_decoder.shape[1]):
          output,state_1,state_2,alpha=self.onestep(input_to_decoder[:,step:step+1],encoder_output,state_1,state_2)

          all_outputs=all_outputs.write(step,output)
        all_outputs=tf.transpose(all_outputs.stack(),[1,0,2])
        
        return all_outputs
    
import warnings
warnings.filterwarnings("ignore")

class encoder_decoder(tf.keras.Model):
  def __init__(self,enc_units,embedding_dim,vocab_size,output_length,dec_units,att_units,batch_size):
        super().__init__()

        
        self.batch_size=batch_size
        self.encoder =Encoder(enc_units)
        self.decoder=Decoder(vocab_size,embedding_dim,output_length,dec_units,att_units)
        
  
    #Coompute the image features using feature extraction model and pass it to the encoder
    # This will give encoder ouput
   # Pass the decoder sequence,encoder_output,initial states to Decoder
    # return the decoder output

  
  def call(self, data):
        features,report  = data[0], data[1]
        
        encoder_output= self.encoder(features)
        state_h,back_h=self.encoder.initialize_states(self.batch_size)
        
        output= self.decoder(report, encoder_output,state_h,back_h)
      
        return output      
  


def custom_lossfunction(y_true, y_pred):
    #getting mask value
    mask = tf.math.logical_not(tf.math.equal(y_true, 0))
    
    #calculating the loss
    loss_ = loss_function(y_true, y_pred)
    
    #converting mask dtype to loss_ dtype
    mask = tf.cast(mask, dtype=loss_.dtype)
    
    #applying the mask to loss
    loss_ = loss_*mask
    
    #getting mean over all the values
    loss_ = tf.reduce_mean(loss_)
    return loss_ 


# code set separated
image_shape= (224,224,3)
image_input= Input(shape=(224,224,3))

base=DenseNet121(include_top=False,input_tensor=image_input,input_shape=image_shape)
pred=Dense(14,"sigmoid")(base.output)

chexnet_model=Model(inputs=base.input,outputs=pred)
chexnet_model.load_weights("chexnet.h5")
print('chexnet_model loaded')

# chexnet_model.summary()
final_chexnet_model=Model(inputs=chexnet_model.inputs,outputs=chexnet_model.layers[-2].output,name="Chexnet_model")


#https://machinelearningmastery.com/use-word-embedding-layers-deep-learning-keras/
embeddings_index=dict()
f = open('glove.6B.300d.txt', encoding='utf-8')
for line in f:
  values = line.split()
  word = values[0]
  coefs = np.asarray(values[1:], dtype='float32')
  embeddings_index[word] = coefs
f.close()
print("Done")

# create a weight matrix for words in training docs

embedding_matrix = np.zeros((vocab_size, 300))
for word, i in tqdm(token.word_index.items()):
  embedding_vector = embeddings_index.get(word)
  if embedding_vector is not None:
    embedding_matrix[i] = embedding_vector 

input_img=Input(shape=(98,1024),name="image_fetaures")
# input_img=Input(shape=(None,1,1024),name="image_fetaures")
input_txt=Input(shape=(max_len),name="text_input")

#encoder model
en_out=Dense(enc_units,activation="relu",name="encoder_dense")(input_img)
enc_out=tf.keras.layers.Dropout(0.5)(en_out)

state1= Input(shape=(bs,enc_units),name="state1")
state2= Input(shape=(bs,enc_units),name="state2")
state_h=tf.keras.layers.Add()([state1,state2])
#decoder model with attention

emb_out=tf.keras.layers.Embedding(vocab_size,output_dim=300,input_length=max_len,mask_zero=True,trainable=False,weights=[embedding_matrix])(input_txt)
weights=tf.keras.layers.AdditiveAttention()([state_h,en_out])
context_vector=tf.matmul(en_out,weights,transpose_b=True)[:,:,0]
context_vector=Dense(embedding_dim)(context_vector)
result=tf.concat([tf.expand_dims(context_vector, axis=1),emb_out],axis=1)
gru_out,state_1,state_2=tf.keras.layers.Bidirectional(tf.keras.layers.GRU(dec_units,return_sequences=True, return_state=True,name="Bidirectional_GRU"))(result)
out=tf.keras.layers.Dense(vocab_size,name="decoder_final_dense")(gru_out)
en_de=Model(inputs=[input_txt,input_img,state1,state2],outputs=out)



model  = encoder_decoder(enc_units,embedding_dim,vocab_size,max_len,dec_units,att_units,bs)

optimizer = tf.keras.optimizers.Adam()

loss_function = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True, reduction='auto')

# model.compile(optimizer=optimizer,loss=custom_lossfunction)
model.compile(optimizer=optimizer,loss=custom_lossfunction)


from tensorflow.keras.models import load_model
# Load the model with custom_objects parameter
model = load_model("model2wts/ckpt", custom_objects={"custom_lossfunction": custom_lossfunction,"Encoder": Encoder, "Decoder": Decoder})
print('model loaded')




# @app.route('/api/process_image', methods=['POST'])
# def process_image():
#     # Check if the POST request has a file part
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})

#     file = request.files['file']

#     # Check if the file is empty
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     # Check if the file is allowed (you may want to check the file type and size)
#     # For simplicity, it is assumed that any file is allowed in this example.

#     # Perform image processing
#     image = Image.open(file)
#     processed_result = process_image_with_model(image)

#     return jsonify({'processed_result': processed_result})

# def process_image_with_model(image):
    # Convert image to the format expected by your model
    # Perform any necessary pre-processing
    # image = image.resize((224, 224))  # Adjust the size according to your model's input size
    # image_array = img_to_array(image)
    # image_array = preprocess_input(image_array)

    # # Perform inference with your Bidirectional GRU model
    # # Replace this with the actual inference for your model
    # # Assuming model.predict returns the processed result
    # result = model.predict(np.expand_dims(image_array, axis=0))

    # # Example: Convert result to a string
    # processed_result = str(result[0][0])

    # return processed_result

if __name__ == '__main__':
    app.run(debug=True)

    