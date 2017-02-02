import argparse
import datetime
import imutils
import numpy as np
import time
import csv
import cv2
import os.path

#define variable
click_frame = False
divide_x = 0
divide_y = 0
channel_A = 0
channel_B = 0
area_A = 0
area_B = 0

#division fuction (divide_frame)
def divide_frame(event,x,y,flags,param):
	global click_frame
	global divide_x,divide_y
	global shape
	if click_frame == False and event == cv2.EVENT_LBUTTONDOWN:
		click_frame = True
		divide_x = x
		divide_y = y
		print("First frame selected")

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=100, help="minimum area size")
#ap.add_argument("-s","--shape",type=str,default="rectangle",help="shape of test arena")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	camera = cv2.VideoCapture(0)
	time.sleep(0.25)

else:
	camera = cv2.VideoCapture(args.get("video", None))

fps = camera.get(cv2.cv.CV_CAP_PROP_FPS)
frame_count = 0
firstFrame = None

#Creating window and initializing mouse callback for division
cv2.namedWindow("Security Feed")
cv2.setMouseCallback("Security Feed",divide_frame)

# After selecting firstFrame no tracking should occur for 5s
#def relay(event,flags,param)
#	while (frame_count/fps) < 5:
#		break


while True:
	# grab the current frame and initialize the occupied/unoccupied"rectangle"
	# text
	(grabbed, frame) = camera.read()
	text = "Unoccupied"

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if not grabbed:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	if firstFrame is None:
		firstFrame = gray
		cv2.imshow("Security Feed", frame)
		while click_frame == False:
			print("Selected Image")
			cv2.waitKey(25)
		continue

	frame_count += 1

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < args["min_area"]:
			continue

		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		text = "Occupied"

		fish_x = x+w/2
		fish_y = y+h/2

		if fish_x < divide_x and fish_y < divide_y:
			channel_A += 1
		if fish_x > divide_x and fish_y < divide_y:
			area_A += 1
		if fish_x < divide_x and fish_y > divide_y:
			channel_B += 1
		if fish_x > divide_x and fish_y > divide_y:
			area_B += 1

		#division lines

		#tags
		fontsize = 1
		thickness = 1
		cv2.putText(frame,"{0:.2f}".format(fps)+" fps",(25,25),cv2.FONT_HERSHEY_SIMPLEX,0.5,255)
		cv2.putText(frame,"{0:.2f}".format(channel_A/fps),(divide_x-width/4,divide_y-height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
		cv2.putText(frame,"{0:.2f}".format(channel_B/fps),(divide_x-width/4,divide_y+height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
		cv2.putText(frame,"{0:.2f}".format(area_A/fps),(divide_x+width/4,divide_y-height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
		cv2.putText(frame,"{0:.2f}".format(area_B/fps),(divide_x+width/4,divide_y+height/4),cv2.FONT_HERSHEY_SIMPLEX,fontsize,(255,255,255),thickness)
		cv2.putText(frame,"{0:.2f}".format(frame_count/fps)+" time (s)",(divide_x+width/4,25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0))

		# show the frame and record if the user presses a key
		cv2.imshow("Security Feed", frame)
		# cv2.imshow("Thresh", thresh)
		# cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the loop
		if key == ord("q"):
			break


# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()


#print data
print("Total Time [s]:	"+"{0:.2f}".format(frame_count/fps))
print("Channel_A [s]:	"+"{0:.2f}".format(channel_A/fps))
print("Channel_B [s]:	"+"{0:.2f}".format(channel_B/fps))
print("Area_A [s]:	"+"{0:.2f}".format(area_A/fps))
print("Area_B [s]:	"+"{0:.2f}".format(area_B/fps))

# Print data to file (data.csv)
# Write file and header if file does not already exist
# If file exists data is inserted in a new row and no header is added
# lineterminator = '\n' to remove blank line between rows when program is restarted
file_exists=os.path.isfile("data.csv")

with open('data.csv','a') as csvfile:
	dw=csv.DictWriter(csvfile,delimiter=',',fieldnames=["File","Total Time","Channel_A","Channel_B","Area_A","Area_B"],lineterminator='\n')
	writer=csv.writer(csvfile)

	if file_exists == True:
		writer.writerow([args.get("video"),frame_count/fps,channel_A/fps,channel_B/fps,area_A/fps,area_B/fps])

	else:
		dw.writeheader()
		writer.writerow([args.get("video"),frame_count/fps,channel_A/fps,channel_B/fps,area_A/fps,area_B/fps])
