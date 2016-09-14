import argparse
import sys
import datetime
import imutils
import numpy as np
import time
import csv
import cv2
import os.path
import datetime
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
frame_list = []


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=100, help="minimum area size")
ap.add_argument("-x","--x-value",type=float,default=0.5, help="x coordinate of center")
ap.add_argument("-y","--y-value",type=float,default=0.5, help="y coordinate of center")
ap.add_argument("-w","--wait",type=int,default=0, help="seconds waited,before initiation")
ap.add_argument("-c","--click",type=bool,default=False, help="definition of center by clicking on first frame displayed in window")
ap.add_argument("-t","--timelimit",type=int,default=sys.maxint,help="define timelimit")
ap.add_argument("-s","--show",type=bool,default=False,help="show frames")
ap.add_argument("-r","--refresh",type=int,default=10,help="refresh every n frames")
ap.add_argument("-p","--print",type=str,default="",help="save data to given file")
ap.add_argument("-i","--image",type=str,default="",help="save live view to given image file")
ap.add_argument("-d","--dump",type=str,default="",help="save all data to given file")
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
analyser = fv.analyser(args["video"],divide_x,divide_y,args["wait"],args["min_area"],args["timelimit"],args["refresh"],args["show"])

# new class for accepting data from analyser
class fish_data(QObject):

    def __init__(self,analyser):
        QObject.__init__(self)
        analyser.newData.connect(self.on_newData)
        analyser.newFrame.connect(self.on_newFrame)
        analyser.countSig.connect(self.on_countSig)
        analyser.framecount.connect(self.on_framecount)
        #analyser.newData.connect(self.on_calculate)

# Not quite shure about this yet. Implementation to integrate video output option with args["show"]
    def on_newFrame(self,frame):

        if args["show"] == True:
            cv2.namedWindow("FlumeView")
            cv2.imshow("FlumeView",frame)

    def on_framecount(self,frame_count):
    #
    #     #self.frame_list = []
        self.frame_count = frame_count
    #     self.frame_list.append(frame_count)
    #     #self.frame_list [1] = max(self.frame_list)
        #self.frame_list [0] = min(self.frame_list)


    def on_newData(self,x,y,frame_count):
        #global divide_x,divide_y,args
        frame_list.append([x,y,frame_count])

        if self.count_start == True:

            stats.calculate(x,y,divide_x,divide_y)

        if args["refresh"] > 0 and args["show"] == True:

            stats.plot_xy(x,y,args["refresh"])

        #print data
        print("Total Time [s]:	"+"{0:.2f}".format(self.frame_count/analyser.fps - args["wait"]))
        print("Channel_A [s]:	"+"{0:.2f}".format(stats.channel_A/analyser.fps))
        print("Channel_B [s]:	"+"{0:.2f}".format(stats.channel_B/analyser.fps))
        print("Area_A [s]:	"+"{0:.2f}".format(stats.area_A/analyser.fps))
        print("Area_B [s]:	"+"{0:.2f}".format(stats.area_B/analyser.fps))

        # Print data to file (data.csv)
        # Write file and header if file does not already exist
        # If file exists data is inserted in a new row and no header is added
        # lineterminator = '\n' to remove blank line between rows when program is restarted


    def on_countSig(self,count_start):

        self.count_start = count_start

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


# Save data to file:
# timestamp_exists=os.path.isfile("FV_argument_timestamp.csv")
#
# with open("FV_argument_timestamp.csv",'a') as csvfile:
#     dw=csv.DictWriter(csvfile,delimiter=',',fieldnames=["datatime","videofile","x-coord","y-coord","min_area","click","dump","image","print","refresh","show frame","timelimit","wait"],lineterminator='\n')
#     writer=csv.writer(csvfile)
#
#     if timestamp_exists == True:
#         writer.writerow([datetime.datetime.now(),args.get("video"),args["divide_x"],args["divide_y"],args["min_area"],args["click"],args["dump"],args["image"],args["print"],args["refresh"],args["show"],args["timelimit"],args["wait"]])
#
#     else:
#         dw.writeheader()
#         writer.writerow(datetime.datetime.now(),[args.get("video"),args["divide_x"],args["divide_y"],args["min_area"],args["click"],args["dump"],args["image"],args["print"],args["refresh"],args["show"],args["timelimit"],args["wait"]])

if args["print"] != "":

    file_exists=os.path.isfile(args["print"])

    with open(args["print"],'a') as csvfile:
        dw=csv.DictWriter(csvfile,delimiter=',',fieldnames=["File","Total Time [s]","Channel_A [s]","Channel_B [s]","Area_A [s]","Area_B [s]"],lineterminator='\n')
        writer=csv.writer(csvfile)

        if file_exists == True:
            writer.writerow([args.get("video"),"{0:.2f}".format((analyser.frame_count/analyser.fps) - args["wait"]),"{0:.2f}".format(stats.channel_A/analyser.fps),"{0:.2f}".format(stats.channel_B/analyser.fps),"{0:.2f}".format(stats.area_A/analyser.fps),"{0:.2f}".format(stats.area_B/analyser.fps)])

        else:
            dw.writeheader()
            writer.writerow([args.get("video"),"{0:.2f}".format((analyser.frame_count/analyser.fps)-args["wait"]),"{0:.2f}".format(stats.channel_A/analyser.fps),"{0:.2f}".format(stats.channel_B/analyser.fps),"{0:.2f}".format(stats.area_A/analyser.fps),"{0:.2f}".format(stats.area_B/analyser.fps)])

if args["dump"] != "":

    #dump_exists=os.path.isfile(args["dump"])

    with open(args["dump"],'w') as csvfile:
        dw=csv.DictWriter(csvfile,delimiter=',',fieldnames=["File","x_Coord","Y_Coord","Frame_number"],lineterminator='\n')
        writer=csv.writer(csvfile)
        dw.writeheader()

        for singleframe in frame_list:

            writer.writerow([args.get("video"),singleframe[0],singleframe[1],singleframe[2]])

if args["image"] != "":

    cv2.imwrite(args["image"],analyser.lastframe)
