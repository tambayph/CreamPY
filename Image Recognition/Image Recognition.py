# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 14:34:33 2023

@author: Ezra
"""

import cv2
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

net = cv2.dnn.readNetFromCaffe(args['prototxt'], args['model'])

vs = VideoStream(src = 0).start()

while True:
    frame = vs.read()
    frame = imutils.resize(frame, width = 1000)
    # camera = cv2.VideoCapture('C:/Users/Ezra/Documents/1080.mp4')
    # (grabbed, frame) = camera.read()
    
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()
    
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0,0,i,2]
        
        if confidence > args["confidence"]:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

			# draw the prediction on the frame
        label = "{}: {:.2f}%".format(CLASSES[idx],
        	confidence * 100)
        cv2.rectangle(frame, (startX, startY), (endX, endY),
        	COLORS[idx], 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        cv2.putText(frame, label, (startX, y),
        	cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                        
    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break