

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
# import joblib
# model = joblib.load("model_latest.pkl")

# net = cv2.dnn.readNet("./yolov3.weights", "./darknet/cfg/yolov3.cfg")
# print(net)

def predict(image):
    target_size = (32,32)
    image = np.array(image)
    image = cv2.resize(image.astype(float),target_size,interpolation=cv2.INTER_CUBIC)
    image = image/255.0
    x = []
    x.append(image)
    x = np.array(x)
    return 1
    # return np.argmax(model.predict(x))
# def predict(image):
#     image = cv2.imread("12.png")
#     image = np.asarray(image)
#     # (height, width) = image.shape[:2]
#     # image = cv2.resize(image.astype(float),(416,416))
#     blob = cv2.dnn.blobFromImage(np.float32(image), 1 / 255.0, (416, 416), swapRB=True, crop=False)
#     net.setInput(blob)

#     output_layer_name = net.getUnconnectedOutLayersNames()
#     output_layers = net.forward(output_layer_name)

#     # Initialize list of detected people
#     # people = []

#     # Loop over the output layers
#     for output in output_layers:
#         # Loop over the detections
#         for detection in output:
#             # Extract the class ID and confidence of the current detection
#             scores = detection[5:]
#             class_id = np.argmax(scores)
#             confidence = scores[class_id]

#             # Only keep detections with a high confidence
#             print("happened")
#             if class_id == 0 and confidence > 0.5:
#                 print("true")
#                 # Object detected
#                 return True

   
