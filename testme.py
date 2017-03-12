# -*- coding utf-8 -*-
import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split
import random
import tensorflow as tf

def read_data(img_path, image_h = 64, image_w = 64):
    image_data = []
    label_data = []
    image = cv2.imread(img_path)
    #cv2.namedWindow("Image")
    #cv2.imshow("Image",image)
    #cv2.waitKey(0)
    h,w,_ = image.shape
    longest_edge = max(h,w)
    top, bottom, left, right = (0, 0, 0, 0)
    dh,dw = (0,0)
    if h < longest_edge:
        dh = longest_edge - h
        top = dh // 2
        bottom = dh - top
    elif w < longest_edge:
        dw = longest_edge - w
        left = dw // 2
        right = dw - left
    else:
        pass
    image_pad = cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
    image = cv2.resize(image_pad, (image_h, image_w))

    image_data.append(image)
    label_data.append(img_path)
    image_data = np.array(image_data)
    train_x, test_x, train_y, test_y = train_test_split(image_data, label_data, test_size=0.05,
                                                        random_state=random.randint(0, 100))
    X = tf.placeholder(tf.float32,[None, 64, 64, 3])
    Y = tf.placeholder(tf.float32, [None, 2])
    return Y

#img_path = '4833.jpg'
#print(read_data(img_path))

x_data = np.float32(np.random.rand(2,100))
y_data = np.dot([0.100, 0.200], x_data) + 0.300

b = tf.Variable(tf.zeros([1]), name='B')
W = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0), name='W')
y = tf.add(tf.matmul(W, x_data, name='MatMul'), b ,name='add')

loss = tf.reduce_mean(tf.square(tf.subtract(y, y_data, name='Sub'), name='Square'), name='ReduceMean')
optimizer = tf.train.GradientDescentOptimizer(0.001, name='Optimizer')
train = optimizer.minimize(loss, name='minimize')

summaries = [tf.summary.histogram('W',W), tf.summary.histogram('b', b), tf.summary.scalar('loss', loss)]
summary_op = tf.summary.merge(summaries)
print(summary_op)