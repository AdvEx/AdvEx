#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 31 15:24:55 2018

@author: mancx111
"""
import numpy as np
import tensorflow as tf
import keras
import json
import pickle
import os
import scipy.io as sio
from keras.layers import Input
from keras import backend
from keras import utils
from cleverhans.attacks import FastGradientMethod
from keras.preprocessing.image import load_img,img_to_array
from keras.applications.vgg16 import VGG16,preprocess_input,decode_predictions

'''
We use VGG16 model as our template model for black box attacks
The input of this script will be clean images
The output of this script will be adversarial images of various attacks

Notice that we generate adversarial images which have the smallest perturbance that the attack method can find.
Therefore, this gives an optimistic evaluation of the model.

'''
#path='./tiny-imagenet-200/train/n01443537/images/'
path='.'
CLASS_INDEX=json.load(open('./class_index.json'))

sess = tf.Session()
keras.backend.set_session(sess)
def load_label(path):
    mylist=[]
    with open(path,'r') as f:
        for text in f:
            mylist.append(text.strip())
            
                
    return mylist


def binary_search_epsilon(model,attack,labels,binary_iter=10,attack_params=None):

    
    ##Currently, we are planning to only take 10 images per class to generate AE
    if not attack_params:
        attack_params={'eps':None}

    num=0
    adv_dict={}
    clean_dict={}
    for img in os.listdir(path):
        if not img.endswith('JPEG'):
            continue
        
        lbl=int(img.split('_')[-1].split('.')[0])-1
        class_lbl=CLASS_INDEX[labels[lbl]][0]
        if class_lbl not in adv_dict:
            adv_dict[class_lbl]=[]
            clean_dict[class_lbl]=[]
            
        iters,min_,max_=0,0.0,1.0
        image=load_img(path+'/'+img,target_size=(224,224))
        input_=img_to_array(image)
        input_=preprocess_input(input_.reshape(1,input_.shape[0],input_.shape[1],input_.shape[2]))
        
        predict=decode_predictions(model.predict(input_))[0][0]
        #print(predict[0],CLASS_INDEX[labels[lbl]][0])
        
        if predict[0]!=class_lbl:
            #print('Wrong label. Proceed')
            continue

        
        result=None
        while iters < binary_iter:
            mid=(min_+max_)/2
            attack_params['eps']=mid
            adv=attack.generate_np(input_,**attack_params)
            yhat=model.predict(adv)
            if decode_predictions(yhat)[0][0][0]==class_lbl:
                min_=mid
                #print('Noise too small',mid)
            else:
                max_=mid
                result=adv
                #print('Noise too large',mid)
            iters+=1
        
        if result is None:
            continue
        clean_dict[class_lbl].append(input_)
        adv_dict[class_lbl].append(result)
        num+=1
        
        print('Number of AE created: ',num)
        if num>=20:
            break
    
    pickle.dump(clean_dict,open('clean_set.pkl','wb'))
    pickle.dump(adv_dict,open('adv_set.pkl','wb'))
    
    


def main():
    
    ##Use pretrained parameters for VGG16
    model=VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000)
    model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
    
    attack=FastGradientMethod(model, sess=sess)
    attacks=[]
    #Load the ground truth label of the images
    labels=load_label('ILSVRC2012_validation_ground_truth.txt')
    
    #Search for the best epsilon to use
    binary_search_epsilon(model,attack,labels)

main()
    
    
    
    
    

    