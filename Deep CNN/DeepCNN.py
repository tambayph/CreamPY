# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:38:09 2023

@author: WF026
"""

import tensorflow as tf
import os
import cv2
import imghdr
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy
from tensorflow.keras.models import load_model

os.environ['KMP_DUPLICATE_LIB_OK']='True'

# # LIMIT PERFORMANCE
# gpus = tf.config.experimental.list_physical_devices('GPU')
# for gpu in gpus: 
#     tf.config.experimental.set_memory_growth(gpu, True)

# tf.config.list_physical_devices('GPU')

# # REMOVE FAULTY IMAGES    
data_dir = 'D:/Ezra/Python/Scripts/Deep CNN/data' 
image_exts = ['jpeg','jpg', 'bmp', 'png']

for image_class in os.listdir(data_dir): 
    for image in os.listdir(os.path.join(data_dir, image_class)):
        image_path = os.path.join(data_dir, image_class, image)
        try: 
            img = cv2.imread(image_path)
            tip = imghdr.what(image_path)
            if tip not in image_exts: 
                print('Image not in ext list {}'.format(image_path))
                os.remove(image_path)
        except Exception as e: 
            print('Issue with image {}'.format(image_path))
            # os.remove(image_path)
 
# LOAD DATA    
# Takes the path to a directory containing subdirectories of images as its argument.        
data = tf.keras.utils.image_dataset_from_directory('D:/Ezra/Python/Test/Data/DeepCNN data')

# Create an iterator object that can iterate over the dataset and yield each batch of data as NumPy arrays
data_iterator = data.as_numpy_iterator()

# Retrieve the next batch of data from the dataset
batch = data_iterator.next()

# Visualizing a small subset of the images and their corresponding labels in the dataset, which can be helpful for understanding the nature of the data and verifying that the images are being loaded and labeled correctly.
fig, ax = plt.subplots(ncols=4, figsize=(20,20))
for idx, img in enumerate(batch[0][:4]):
    ax[idx].imshow(img.astype(int))
    ax[idx].title.set_text(batch[1][idx])

# SCALE DATA 
# Scaling the pixel values to a range between 0 and 1, the model can more easily learn meaningful patterns in the data and make accurate predictions  
data = data.map(lambda x,y: (x/255, y))
data.as_numpy_iterator().next()

# SPLIT DATA
#  Ensure that the model is not overfitting to the training data, and that its performance on new, unseen data is a true reflection of its ability to generalize to new situations.
train_size = int(len(data)*.7)
val_size = int(len(data)*.2)
test_size = int(len(data)*.1)

train = data.take(train_size)
val = data.skip(train_size).take(val_size)
test = data.skip(train_size+val_size).take(test_size)

# BUILD DEEP LEARNING MODEL
model = Sequential()
model.add(Conv2D(16, (3,3), 1, activation='relu', input_shape=(256,256,3)))
model.add(MaxPooling2D())
model.add(Conv2D(32, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Conv2D(16, (3,3), 1, activation='relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])

# # TRAIN MODEL
logdir='logs'
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logdir)
hist = model.fit(train, epochs=20, validation_data=val, callbacks=[tensorboard_callback])

# # PLOT PERFORMANCE
# fig = plt.figure()
# plt.plot(hist.history['loss'], color='teal', label='loss')
# plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
# fig.suptitle('Loss', fontsize=20)
# plt.legend(loc="upper left")
# plt.show()

# fig = plt.figure()
# plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
# plt.plot(hist.history['val_accuracy'], color='orange', label='val_accuracy')
# fig.suptitle('Accuracy', fontsize=20)
# plt.legend(loc="upper left")
# plt.show()

# # EVALUATE
pre = Precision()
re = Recall()
acc = BinaryAccuracy()

for batch in test.as_numpy_iterator(): 
    X, y = batch
    yhat = model.predict(X)
    pre.update_state(y, yhat)
    re.update_state(y, yhat)
    acc.update_state(y, yhat)

print(pre.result(), re.result(), acc.result())

# # TEST
# img = cv2.imread('8iAb9k4aT.jpg')
# plt.imshow(img)
# resize = tf.image.resize(img, (256,256))
# plt.imshow(resize.numpy().astype(int))
# plt.show()

# yhat = model.predict(np.expand_dims(resize/255, 0))
# print(yhat)

# if yhat > 0.5: 
#     print('Predicted class is Sad')
# else:
#     print('Predicted class is Happy')

# # SAVE MODEL
# model.save(os.path.join('models','imageclassifier.h5'))
# new_model = load_model('D:/Ezra/Python/Scripts/Deep CNN/models/imageclassifier.h5')
# new_model.predict(np.expand_dims(resize/255, 0))


