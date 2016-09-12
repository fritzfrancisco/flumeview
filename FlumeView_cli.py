import argparse
import sys
import datetime
import imutils
import numpy as np
import time
import csv
import cv2
import os.path
import FlumeView_analyser as fv
import FlumeView_stats as stats
# import matplotlib.pyplot as plt

from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot


divide_x = 0
divide_y = 0
channel_A = 0
channel_B = 0
area_A = 0
area_B = 0

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=100, help="minimum area size")
ap.add_argument("-x","--x-value",type=float,default=0.5, help="x coordinate of center")
ap.add_argument("-y","--y-value",type=float,default=0.5, help="y coordinate of center")
ap.add_argument("-w","--wait",type=int,default=1, help="seconds waited,before initiation")
ap.add_argument("-c","--click",type=bool,default=False, help="definition of center by clicking on first frame displayed in window")
ap.add_argument("-t","--timelimit",type=int,default=sys.maxint,help="define timelimit")
ap.add_argument("-s","--show",type=bool,default=False,help="show frames")
ap.add_argument("-r","--refresh",type=int,default=1,help="refresh every n frames")
#ap.add_argument("-s","--shape",type=str,default="rectangle",help="shape of test arena")
args = vars(ap.parse_args())
print(args)

# division function (divide_frame)
if args["click"] == False:

    divide_x = args["x_value"]
    divide_y = args["y_value"]

else:
# new capture for center selection
    mcapture = fv.set_input(args["video"])
    (divide_x,divide_y)=fv.fix_point(mcapture)

# get functions from FlumeView_analyser
#capture = fv.set_input(args["video"])
analyser = fv.analyser(args["video"],args["x_value"],args["y_value"],args["wait"],args["min_area"],args["timelimit"],args["refresh"],args["show"])

# new class for accepting data from analyser
class fish_data(QObject):

    def __init__(self,analyser):
        QObject.__init__(self)
        analyser.newData.connect(self.on_newData)
        analyser.newFrame.connect(self.on_newFrame)
        #analyser.newData.connect(self.on_calculate)

# Not quite shure about this yet. Implementation to integrate video output option with args["show"]
    def on_newFrame(self,frame):

        if args["show"] == True:
            cv2.namedWindow("FlumeView")
            cv2.imshow("FlumeView",frame)


    def on_newData(self,x,y):
        global divide_x,divide_y,args

        stats.calculate(x,y,divide_x,divide_y)

        if args["refresh"] > 0 and args["show"] == True:

            stats.plot_xy(x,y,args["refresh"])

    # def on_calculate(self,x,y):
    #     global divide_x,divide_y
    #     stats.calculate(x,y,divide_x,divide_y)

# if args["show"] == True:
#     cv2.namedWindow("FlumeView")
#     cv2.imshow("FlumeView",frame)


#while capture.isOpened() == True:

# Why do I need this?
fish = fish_data(analyser)

analyser.start()
#
# analyser.euclideanDist()
