
Motion-detection
Problem Statement:-Motion detection using Opencv

Introduction:- Surveillance is the monitoring of the behavior, activities, or other changing information, usually of people for the purpose of influencing, managing, directing, or protecting them. Motion Detector takes input from video sources such as network cameras, web cams, files, etc. and makes intelligent decisions based on analyzing frames. The primary focus of Motion Detector is efficient video processing, fault tolerance and extensibility. Motion sensing is a process of change in position of the object related to its surrounding or vice versa. Motion Detection of human has a very wide area of applications. In many applications based on machine vision, motion detection is used. For example, when we want to count the people who pass by a certain place or how many cars have passed through a toll. In all these cases, the first thing we have to do is extract the people or vehicles that are at the scene.

Requirements:

Python integrated development environment
OpenCV(libraries) OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine learning software library. OpenCV was built to provide a common infrastructure for computer vision applications and to accelerate the use of machine perception in the commercial products.
Pandas(libraries) Pandas is a high-level data manipulation tool developed by Wes McKinney. It is built on the Numpy package and its key data structure is called the DataFrame. DataFrames allow you to store and manipulate tabular data in rows of observations and columns of variables.
Imutils(liberaries) imutils are a series of convenience functions to make basic image processing functions such as translation, rotation, resizing, skeletonization, and displaying Matplotlib images easier with OpenCV
Our project mainly includes 3 modules:- A)Motion detection B)Background subtraction C)Colorspaces

import necessary packages. All of these should look pretty familiar, except perhaps the imutils package, which is a set of convenience functions that I have created to make basic image processing tasks easier. If you do not already have imutils installed on your system, you can install it via pip: pip install imutils . Next up, We define two switches here. The first, --video , is optional. It simply defines a path to a pre-recorded video file that we can detect motion in. If you do not supply a path to a video file, then OpenCV will utilize your webcam to detect motion.

We also define --min-area , which is the minimum size (in pixels) for a region of an image to be considered actual “motion”. we’ll often find small regions of an image that have changed substantially, likely due to noise or changes in lighting conditions. In reality, these small regions are not actual motion at all — so we define a minimum size of a region to combat and filter out these false-positives.

Later we handle grabbing a reference to our vs object. In the case that a video file path is not supplied, we have to grab a reference to the webcam and wait for it to warm up. And if a video file is supplied, then we’ll create a pointer to it. Lastly, we end this code snippet by defining a variable called firstFrame,it stores the first frame of the video file/webcam stream

Assumption: The first frame of our video file will contain no motion and just background — therefore, we can model the background of our video stream using only the first frame of the video.

So now that we have a reference to our video file/webcam stream, we can start looping over each of the frames on.A call to vs.read() on a frame that we ensure we are grabbing properly on.We also define a string named text and initialize it to indicate that the room we are monitoring is “Unoccupied”. If there is indeed activity in the room, we can update this string.And in the case that a frame is not successfully read from the video file, we’ll break from the loop

Now we can start processing our frame and preparing it for motion analysis. We first resize it down to have a width of 500 pixels — there is no need to process the large, raw images straight from the video stream. We’ll also convert the image to grayscale since color has no bearing on our motion detection algorithm. Finally, we’ll apply Gaussian blurring to smooth our images.It’s important to understand that even consecutive frames of a video stream will not be identical!Due to tiny variations in the digital camera sensors, no two frames will be 100% the same — some pixels will most certainly have different intensity values. That said, we need to account for this and apply Gaussian smoothing to average pixel intensities across an 21 x 21 region. This helps smooth out high frequency noise that could throw our motion detection algorithm off. As I mentioned above, we need to model the background of our image somehow. Again, we make the assumption that the first frame of the video stream contains no motion and is a good example of what our background looks like. If the firstFrame is not initialized, we store it for reference and continue on to processing the next frame of the video stream

Now that we have our background modeled via the firstFrame variable, we can utilize it to compute the difference between the initial frame and subsequent new frames from the video stream.Computing the difference between two frames is a simple subtraction, where we take the absolute value of their corresponding pixel intensity differences delta = |background_model – current_frame|

We threshold the frameDelta on to reveal regions of the image that only have significant changes in pixel intensity values. If the delta is less, we discard the pixel and set it to black (i.e. background). If the delta is greater than 25, we’ll set it to white (i.e. foreground). An example of our thresholded delta image can be seen belowAgain, note that the background of the image is black, whereas the foreground (and where the motion is taking place) is white.Given this thresholded image, it’s simple to apply contour detection to to find the outlines of these white regions We start looping over each of the contours, where we’ll filter the small, irrelevant contours

If the contour area is larger than our supplied --min-area , we’ll draw the bounding box surrounding the foreground and motion region. We also update our text status string to indicate that the room is “Occupied”.

The remainder of this example simply wraps everything up. We draw the room status on the image in the top-left corner, followed by a timestamp (to make it feel like “real” security footage) on the bottom-left. display the results of our work, allowing us to visualize if any motion was detected in our video, along with the frame delta and thresholded image so we can debug our script.

Note: If you download the code to this post and intend to apply it to your own video files, you’ll likely need to tune the values for cv2.threshold and the --min-area argument to obtain the best results for your lighting conditions.

Finally, at last we cleanup and release the video stream pointer.

Conclusion:- So as you can see, our motion detection system is performing fairly well despite how simplistic it is! We can able to detect an entire room without a problem.However, to be realistic, the results are far from perfect. We get multiple bounding boxes even though there is only one person moving around the room — this is far from ideal. And we can clearly see that small changes to the lighting, such as shadows and reflections on the wall, trigger false-positive motion detections.
