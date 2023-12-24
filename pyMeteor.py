from picamera2 import Picamera2
import time
import datetime
import cv2
import os
import numpy as np

tmp_path = "images_tmp"
img_path = "images"
height = 1080
width = 1920

#Check if image paths exist, create if not
if not os.path.exists(tmp_path):
	os.makedirs(tmp_path)

if not os.path.exists(img_path):
	os.makedirs(img_path)

#set camera settings
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (width, height)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
#picam2.shutter_speed = 10000000
picam2.controls.ExposureTime = 10000
picam2.start()
time.sleep(2)

#Capture still images
for i in range(0,4):
	tmpfile = tmp_path+"/img%s.jpg" % (str(i).rjust(5, '0'))
	print("Capturing image "+tmpfile)
	picam2.capture_file(tmpfile)

#Get directory list of captured images
jpeg_list = sorted(os.listdir(tmp_path))

#Create blank (black) image as the base
outImg = np.zeros((height,width,3), np.uint8)

#Loop through image list and overlay them
for i in range(len(jpeg_list)):
	print("reading image: " + jpeg_list[i])
	next_img = cv2.imread(tmp_path+"/"+jpeg_list[i])
	outImg = cv2.addWeighted(outImg, 0.5, next_img, 0.5, 0)

#Get timestamp and create filename for composite image
cur_time = datetime.datetime.now()
stub = cur_time.strftime("%Y%m%d_%H%M%S_low")
outfile = img_path+"/%s.jpg" % (stub)
print("Combining images as "+stub)

#Write composite image to disk
cv2.imwrite(outfile, outImg)

