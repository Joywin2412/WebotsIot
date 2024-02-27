

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import to_categorical
from keras.preprocessing.image import  img_to_array

import numpy as np
import cv2
import os
from PIL import Image
from sklearn.model_selection import train_test_split
m,n = 32,32
x=[]
y=[]
import joblib
model = joblib.load("model_latest.pkl")
def predict(image):
    # print(len(image))
    target_size = (32,32)
    image = np.array(image)
    image = cv2.resize(image.astype(float),target_size,interpolation=cv2.INTER_CUBIC)
    image = image/255.0
    x = []
    x.append(image)
    x = np.array(x)
    return np.argmax(model.predict(x))
    # print(image)
    # image = Image/.fromarray(image)

   
