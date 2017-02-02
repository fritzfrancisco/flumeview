import argparse
import datetime
import imutils
import numpy as np
import time
import csv
import cv2
import os.path
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import FlumeView_analyser as fv
import math
# from frigeometry import FriGeometry


# from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot

# def __init__(self,x,y,height,width):
#     QObject.__init__(self)

xar = []
yar = []
cnts = []

channel_A = 0
channel_B = 0
area_A = 0
area_B = 0

plt.axis()
plt.xlim(0.0,1.0)
plt.ylim(1,0)
plt.ion()
counter = 0

def plot_xy(x,y,refresh):
    global xar,yar, counter

    counter = counter + 1
    xar.append(x)
    yar.append(y)
    plt.show()

    if counter % refresh == 0:
         plt.scatter(xar,yar)
         plt.draw()

    #print(x,y)
    # polar plot for magnetic orientation

def calculate(x,y,divide_x,divide_y,click,frag):
    global channel_A,channel_B,area_A,area_B,counter,cnts

    if sum(cnts) == 0:
        cnts = [0]*frag

    if click is True:

        if fv.geometryObject.within([x,y]) == True:

            counter = counter + 1
            point_x = (x-divide_x)
            point_y = (y-divide_y)

            A = pow(point_x,2)
            B = pow(point_y,2)
            C = A + B
            rad = math.acos(point_x /math.sqrt(C))
            deg = math.degrees(rad)

            if point_y < 0:
                deg = 360 - deg

            for i in range(frag):
                if (float(i)/float(frag))*360 < deg < (float(i+1)/float(frag))*360:
                    cnts[i] += 1
                    # print cnts,(float(i)/float(frag))*360 ,(float(i+1)/float(frag))*360
                    return cnts
        else:

            return

    else:
            #
            # if x < divide_x and y < divide_y:
            #     channel_A += 1
            # if x > divide_x and y < divide_y:
            #     area_A += 1
            # if x < divide_x and y > divide_y:
            #     channel_B += 1
            # if x > divide_x and y > divide_y:
            #     area_B += 1

            # else:
            #
            return
