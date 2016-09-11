import argparse
import datetime
import imutils
import numpy as np
import time
import csv
import cv2
import os.path

from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
from scipy.spatial import distance

xyreturn = None

def divide_frame(event,x,y,flags,param):
    global xyreturn
    if event == cv2.EVENT_LBUTTONDOWN:
        xyreturn = (x,y)
        #divide_x = x
        #divide_y = y

def set_input(videofile):
     """Get capture of video file.If not defined, return Webcam output """
     # if the video argument is None,ergewaltigungs then we are reading from webcam
     if videofile is None:
        return cv2.VideoCapture(0)
        time.sleep(0.25)

     else:
        return cv2.VideoCapture(videofile)

def fix_point(capture):
    global xyreturn
    (grabbed,frame) = capture.read()
    height,width,channel = frame.shape
    xyreturn=None
    cv2.namedWindow("FlumeView")
    cv2.setMouseCallback("FlumeView",divide_frame)
    while xyreturn == None:

        (grabbed,frame) = capture.read()
        cv2.imshow("FlumeView",frame)
        cv2.waitKey(30)

    capture.release()
    #print(xyreturn[1]/width)
    return (float(xyreturn[0])/float(width),float(xyreturn[1])/float(height))

# create class "analyser" shell for further calculations
class analyser(QObject):
    newData = pyqtSignal(float,float,name='newData')
    newFrame = pyqtSignal(int,name='newFrame')
    frameshape = pyqtSignal(int,int,name="frameshape")

    def __init__(self,videofile,x,y,wait,min_area,timelimit,refresh,show):
        QObject.__init__(self)
        self.capture = self.set_input(videofile)
        self.divide_x = x
        self.divide_y = y
        self.firstFrame = None
        self.min_area = min_area
        self.timelimit = timelimit
        self.refresh = refresh
        self.show = show


    def set_input(self, videofile):
         """Get capture of video file.If not defined, return Webcam output """
         # if the video argument is None, then we are reading from webcam
         if videofile is None:
         	return cv2.VideoCapture(0)
         	#time.sleep(0.25)

         else:
         	return cv2.VideoCapture(videofile)


    def start(self):

        #cv2.namedWindow("Security Feed")

        self.fps = self.capture.get(cv2.cv.CV_CAP_PROP_FPS)
        frame_count = 0

        self.trace_xy = []
        self.dist = []
        #self.firstFrame = None
        #
        # if self.firstFrame is None:
        #     self.firstFrame = gray

        while True:

            if (frame_count/self.fps)>self.timelimit:

                capture.release()
                return(-1,-1)

            else:
            	# grab the current frame and initialize the occupied/unoccupied
            	# text
                (grabbed, self.frame) = self.capture.read()

                #qt_image = QtWidgets.QImage(frame)
                #self.newFrame.emit(frame)

            	# if the frame could not be grabbed, then we have reached the end
            	# of the video
                if not grabbed:
                    print("end start")
                    return(-1,-1)


            	# resize the frame, convert it to grayscale, and blur it
                frame = imutils.resize(self.frame, width=500)
                height, width, channels = frame.shape
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)

                if self.firstFrame == None:
                    self.firstFrame = gray

                #if self.firstFrame is None:

                frame_count += 1

            	# compute the absolute difference between the current frame and
            	# first frame
                frameDelta = cv2.absdiff(self.firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            	# dilate the thresholded image to fill in holes, then find contours
            	# on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            	# loop over the contours
                for c in cnts:
            		# if the contour is too small, ignore it
                    if cv2.contourArea(c) < self.min_area:
                        continue

            		# compute the bounding box for the contour, draw it on the frame,
            		# and update the text
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.line(frame,(0,int(self.divide_y*height)),(width,int(self.divide_y*height)),(255,0,0))
                    cv2.line(frame,(int(width*self.divide_x),0),(int(width*self.divide_x),height),(255,0,0))

                    for i,element in enumerate(self.trace_xy):
                        if i > 0:
                            element = (int(element[0]*width),int(element[1]*height))
                            previous_element = self.trace_xy[i-1]
                            previous_element = (int(previous_element[0]*width),int(previous_element[1]*height))


                            # Calculating euclidean distance between points:
                            dist_euclidean = distance.euclidean(previous_element,element)
                            self.dist.append(dist_euclidean % 30)
                            dist = self.dist[-5:]
                            #dist_mean = cv2.mean(np.array(self.dist))
                            dist_mean = np.mean(self.dist)
                            #print(self.dist_mean[0])

                            #cv2.line(frame,element,previous_element,(125, 20,200),2)
                            #text = "Occupied"

                            if dist_euclidean < dist_mean*2:

                                cv2.line(frame,element,previous_element,((frame_count),0,frame_count-2),2)
                                #cv2.line(frame,element,previous_element,(125,20,200),2)
                                #print(frame_count)

                    fish_x = float(x+w/2) / float(width)
                    fish_y = float(y+h/2) / float(height)
                    # area_A = 0
                    # area_B = 0
                    # channel_A = 0
                    # channel_B = 0

                    self.trace_xy.append((fish_x,fish_y))

                    #return(fish_x,fish_y)
                    self.newData.emit(fish_x,fish_y)

                    self.height,self.width,channel = frame.shape

            if self.show == True:
                cv2.imshow("Security Feed",frame)
                cv2.waitKey(25)


            #matplotlib

        		# if fish_x < divide_x and fish_y < divide_y:
        		#           channel_A += 1
        		# if fish_x > divide_x and fish_y < divide_y:
        		#           area_A += 1
        		# if fish_x < divide_x and fish_y > divide_y:
        		#           channel_B += 1
        		# if fish_x > divide_x and fish_y > divide_y:
        		#           area_B += 1

        		# division lines
                    # height, width, channels = frame.shape
            		# cv2.line(frame,(0,divide_y),(width,divide_y),(255,0,0))
            		# cv2.line(frame,(divide_x,0),(divide_x,height),(255,0,0))

        		# tags
        		# fontsize = 1
        		# thickness = 1
        		# cv2.putText(frame,"{0:.2f}".format(fps)+" fps",(25,25),cv2.FONT_HERSHEY_SIMPLEX,0.5,255)
        		# cv2.putText(frame,"{0:.2f}".format(channel_A/fps),(divide_x-width/4,divide_y-height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
        		# cv2.putText(frame,"{0:.2f}".format(channel_B/fps),(divide_x-width/4,divide_y+height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
        		# cv2.putText(frame,"{0:.2f}".format(area_A/fps),(divide_x+width/4,divide_y-height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
        		# cv2.putText(frame,"{0:.2f}".format(area_B/fps),(divide_x+width/4,divide_y+height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
        		# cv2.putText(frame,"{0:.2f}".format(frame_count/fps)+" time (s)",(divide_x+width/4,25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0))


        		# show the frame and record if the user presses a key
        		# cv2.imshow("Security Feed", frame)
        		# cv2.imshow("Thresh", thresh)
        		# cv2.imshow("Frame Delta", frameDelta)
        		# key = cv2.waitKey(1) & 0xFF

        		# if the `q` key is pressed, break from the loop
        		# if key == ord("q"):
        		#	break
