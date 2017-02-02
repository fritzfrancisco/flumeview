import argparse
import datetime
import imutils
import numpy as np
import time
import csv
import cv2
import os.path
import math

from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
from frigeometry import FriGeometry
from frirect import FriRect
from fricirc import FriCirc

geometryObject = FriGeometry()
xyreturn = None
switch = 0
crp_lst = []
p1 = (0,0)
p2 = (1,1)
geo = 0
r = 0

def divide_frame(event,x,y,flags,param):
    global xyreturn, switch, crp_lst, geo, geometryObject


    if event == cv2.EVENT_LBUTTONDOWN:
        switch = 1
        crp_lst = [(x,y)]

    elif event == cv2.EVENT_LBUTTONUP:
        switch = 0
        crp_lst.append((x,y))

    if event == cv2.EVENT_LBUTTONDBLCLK:
        xyreturn = (x,y)

    if event == cv2.EVENT_MOUSEMOVE and switch == 1:
        crp_lst.append((x,y))

    if event == cv2.EVENT_RBUTTONDOWN:

        if geo == 0:
            geo = 1
            crp_lst = [(x,y)]

        else:
            # geo = geo - 1
            crp_lst = [(x,y)]

    if geo == 1:
        #selected circle
        geometryObject = FriCirc(p1,r)
        # geometryObject = FriCirc(p1,r)

    else:
        #selected rectangle
        geometryObject = FriRect(p1,p2)


def set_input(videofile):
     """Get capture of video file.If not defined, return Webcam output """
     # if the video argument is None, then we are reading from webcam
     if videofile is None:
        return cv2.VideoCapture(0)
        time.sleep(0.25)

     else:
        return cv2.VideoCapture(videofile)

def fix_point(capture):
    global xyreturn,switch,p1,p2,geo,a,b,r
    (grabbed,frame) = capture.read()
    #frame = frame[pt1y:pt2y,pt1x:pt2x]
    height,width,channel = frame.shape
    xyreturn=None
    cv2.namedWindow("FlumeView")
    cv2.setMouseCallback("FlumeView",divide_frame)
    while xyreturn == None:

        (grabbed,frame) = capture.read()
        key = cv2.waitKey(30) & 0xFF

        if len(crp_lst) >= 1 and geo != 1:
            cv2.rectangle(frame,min(crp_lst),crp_lst[-1],(0,0,255),2)
            # geo = 0

        if len(crp_lst) >= 1 and geo == 1:
            cv2.circle(frame,min(crp_lst),int(math.hypot((crp_lst[-1][0]-min(crp_lst)[0]),(crp_lst[-1][1]-min(crp_lst)[1]))),(0,0,255),2)
            # geometryObject = (min(crp_lst),int(math.hypot((crp_lst[-1][0]-min(crp_lst)[0]),(crp_lst[-1][1]-min(crp_lst)[1]))))
        # else:
        #     crp_lst.append((0,0))
        #     crp_lst.append((int(width),int(height)))

        cv2.imshow("FlumeView",frame)

        if key == ord("c"):

            if len(crp_lst) >= 1:

                p1 = min(crp_lst)[0]/float(width),min(crp_lst)[1]/float(height)
                p2 = crp_lst[-1][0]/float(width),crp_lst[-1][1]/float(height)

                a = (crp_lst[-1][0]/float(width)-p1[0])
                b = (crp_lst[-1][1]/float(height)-p1[1])
                # r = int(math.hypot((crp_lst[-1][0]-min(crp_lst)[0]),(crp_lst[-1][1]-min(crp_lst)[1])))
                # a = ((crp_lst[-1][0]-min(crp_lst)[0])^2)/float(width)
                # b = ((crp_lst[-1][1]-min(crp_lst)[1])^2)/float(height)
                # r = math.hypot(a*float(width),b*float(height))
                # r = math.sqrt(a+b)
                # r = int(math.hypot((crp_lst[-1][0]-center[0]*float(width)),(crp_lst[-1][1]-center[1]*float(height))))
                r = (math.hypot((crp_lst[-1][0]/float(width)-p1[0]),(crp_lst[-1][1]/float(height)-p1[1])))
        #     p1 =(min(crp_lst)[0]/float(width),min(crp_lst)[1]/float(height))
        #     p2 =(crp_lst[-1][0]/float(width),crp_lst[-1][1]/float(height))
        # cv2.waitKey(30)

        if xyreturn != None:
            cv2.destroyWindow("FlumeView")

    capture.release()
    #print(xyreturn[1]/width)
    return (float(xyreturn[0])/float(width),float(xyreturn[1])/float(height))


# create class "analyser" shell for further calculations
class analyser(QObject):
    newData = pyqtSignal(float,float,int,name='newData')
    newFrame = pyqtSignal(int,name='newFrame')
    countSig = pyqtSignal(bool,name='countSignal')
    framecount = pyqtSignal(int,name='framecount')
    #frameshape = pyqtSignal(int,int,name='frameshape')

    def __init__(self,videofile,x,y,wait,min_area,timelimit,refresh,show,fragment):
        QObject.__init__(self)
        self.capture = self.set_input(videofile)
        self.divide_x = x
        self.divide_y = y
        self.wait = wait
        self.firstFrame = None
        self.min_area = min_area
        self.timelimit = timelimit
        self.refresh = refresh
        self.show = show
        self.lastframe = None
        self.fragment = fragment

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

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)

        self.frame_count = 0
        self.count_start = bool
        self.trace_xy = []
        self.dist = []
        #self.firstFrame = None
        #
        # if self.firstFrame is None:
        #     self.firstFrame = gray

        #Creating backgound subtractor
        fgbg = cv2.createBackgroundSubtractorMOG2(history = 10000, varThreshold = 30, detectShadows=False)
        kernel = np.ones((3,3))

        while True:

            if (self.frame_count/self.fps)>self.timelimit:
                self.capture.release()
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
                    print("finished")
                    return(-1,-1)


            	# resize the frame, convert it to grayscale, and blur it
                frame = self.frame
                #frame = frame[pt1y:pt2y,pt1x:pt2x]
                frame = imutils.resize(frame, width=500)
                height, width, channels = frame.shape

                if geo == 0:
                    # geometryObject.drawShape()
                    cv2.rectangle(frame,(int(p1[0]*float(width)),int(p1[1]*float(height))),(int(p2[0]*float(width)),int(p2[1]*float(height))),(0,0,255),2)
                    r = (p2[0]-p1[0])*width*(math.sqrt(2)/2)

                else:
                    r = math.hypot(a*float(width),b*float(height))
                    cv2.circle(frame,(int(p1[0]*float(width)),int(p1[1]*float(height))),int(r),(0,0,255),2)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
                # fgmask = fgbg.apply(blur)
                # erode = cv2.erode(fgmask, kernel)
                # dilate = cv2.erode(erode, kernel)

                #if self.firstFrame is None:
                if self.firstFrame is None:
                    self.firstFrame = gray

                self.frame_count += 1

            	# compute the absolute difference between the current frame and
            	# first frame
                frameDelta = cv2.absdiff(self.firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            	# dilate the thresholded image to fill in holes, then find contours
            	# on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


                if (self.frame_count/self.fps)<self.wait:
                    count_start = False

                else:
                    count_start = True

                    self.framecount.emit(self.frame_count)
                    self.countSig.emit(count_start)


            	# loop over the contours
                for c in cnts:
            		# if the contour is too small, ignore it
                    if cv2.contourArea(c) < self.min_area:
                        continue

                    if count_start == True:
                        # compute the bounding box for the contour, draw it on the frame,
            		    # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)

                        fish_x = float(x+w/2) / float(width)
                        fish_y = float(y+h/2) / float(height)

                        self.lastframe = frame

                        for i in range(0,self.fragment):

                            angle = math.radians(i*(360/self.fragment))

                            if geo == 1:
                                # Circle
                                point_x = int(p1[0]*width + int(r) * math.cos(angle))
                                point_y = int(p1[1]*height + int(r) * math.sin(angle))
                                cv2.line(frame,(point_x,point_y),(int(p1[0]*float(width)),int(p1[1]*float(height))),(255,0,0))

                            else:
                                # Rectangle
                                point_x = int(self.divide_x*width+int(r) * math.cos(angle))
                                point_y = int(self.divide_y*height+int(r) * math.sin(angle))
                                cv2.line(frame,(point_x,point_y),(int(self.divide_x*width),int(self.divide_y*height)),(255,0,0))
                                # print(point_x,point_y,r)

                        # if geo != 1:
                        #
                        #     if p2[0] >= self.divide_x >= p1[0]:
                        #         cv2.line(frame,(int(width*self.divide_x),int(p1[1]*height)),(int(width*self.divide_x),int(p2[1]*height)),(255,0,0))
                        #     else:
                        #         print("ERROR: Center divide outside of bounding area")
                        #
                        #     if p2[1] >= self.divide_y >= p1[1]:
                        #         cv2.line(frame,(int(p1[0]*width),int(self.divide_y*height)),(int(p2[0]*width),int(self.divide_y*height)),(255,0,0))
                        #     else:
                        #         print("ERROR: Center divide outside of bounding area")

                        # if geo == 1:
                        #         # cv2.line(frame,(int(self.divide_x*width),int(self.divide_y*height)-int(r)),(int(self.divide_x*width),int(self.divide_y*height)+int(r)),(255,0,0))
                        #         # cv2.line(frame,(int(self.divide_x*width)-int(r),int(self.divide_y*height)),(int(self.divide_x*width)+int(r),int(self.divide_y*height)),(255,0,0))
                        #         cv2.line(frame,(int(self.divide_x*width),int(self.divide_y)),(int(self.divide_x*width),int(height)),(255,0,0))
                        #         cv2.line(frame,(int(self.divide_x),int(self.divide_y*height)),(int(width),int(self.divide_y*height)),(255,0,0))



                        # if (float(pt1x)/float(width))<fish_x<(float(pt2x)/float(width)) and (float(pt1y)/float(height))<fish_y<(float(pt2y)/float(height)):
                        self.trace_xy.append((fish_x,fish_y))
                        self.newData.emit(fish_x,fish_y,self.frame_count)
                        #self.height,self.width,channel = frame.shape

                        for i,element in enumerate(self.trace_xy):
                            if i > 0:
                                element = (int(element[0]*width),int(element[1]*height))
                                previous_element = self.trace_xy[i-1]
                                previous_element = (int(previous_element[0]*width),int(previous_element[1]*height))

                                # Calculating euclidean distance between points:
                                dist_euclidean = np.linalg.norm(np.array(previous_element)-np.array(element))
                                self.dist.append(dist_euclidean)
                                self.dist = self.dist[-5:]
                                #dist_mean = cv2.mean(np.array(self.dist))
                                dist_mean = np.mean(self.dist)
                                #print(self.dist_mean[0])

                                #cv2.line(frame,element,previous_element,(125, 20,200),2)
                                #text = "Occupied"

                                #if dist_euclidean < dist_mean*2:

                                #cv2.line(frame,element,previous_element,((self.frame_count),0,self.frame_count-2),2)
                                cv2.line(frame,element,previous_element,(0,255,0),2)
                                #cv2.line(frame,element,previous_element,(125,20,200),2)
                                #cv2.circle(frame,element,1,(self.frame_count,255,0),1)

                    else:
                        print("Wait:"+str("{0:.2f}".format(self.frame_count/self.fps))+" s ;"+str(self.frame_count)+" frames")


            if self.show == True:
                cv2.imshow("FlumeView - Live",frame)
                cv2.waitKey(25)

            if cv2.waitKey(30) & 0xFF == 27:
                break

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
