from imutils.video import VideoStream		#videostram-displays video from a local stream 
import argparse  #argparse- to write user friendly command line interfaces
import datetime		#datetime- for current date and time stamp 
import imutils     #imutils- used for basic image processing   
import time   #time- for time
import cv2   #c2- open cv2- for real time computer vision


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	vs = VideoStream(src=0).start()
	time.sleep(2.0)

# otherwise, we are reading from a video file
else:
	vs = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	# text
	frame = vs.read()
	frame = frame if args.get("video", None) is None else frame[1]
	text = "Unoccupied" 

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	if frame is None:
		break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)     #resize- resizing the frame
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)		#cvtColor- convert the colour of an image from one colour space to another
	gray = cv2.GaussianBlur(gray, (21, 21), 0)			#GaussianBlur- removes high frequency components and blurs it

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue

	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)			#dilate- it processes image according to its shape 
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,	#findContours- detects change in image color and marks it as contour
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)		#grab_contours- used to grab all the points along the image contours

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

	# draw the text and timestamp on the frame
	cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF  		#waitkey(1)- will show a frame for atleast 1ms
										#waitkey(0)- will show a frame infinitely until any keypress 

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):       #ord- accepts string of length 1 and returns unicode code point representation
		break

# cleanup the camera and close any open windows
vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()    #destroyAllWindows- closes and deatroys all windows created
