from picamera2 import Picamera2, Preview
import time
from fractions import Fraction
import datetime
from PIL import Image
import cv2
import os
import numpy as np

tmp_path = "images_tmp"
img_path = "images"
height = 1080
width = 1920

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (width, height)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
#picam2.shutter_speed = 10000000
picam2.controls.ExposureTime = 10000
picam2.start()
time.sleep(2)

for i in range(0,4):
	tmpfile = tmp_path+"/img%s.jpg" % (i)
	print("Capturing image img"+str(i))
	picam2.capture_file(tmpfile)

#outImg = Image.new("RGBA", (1920, 1080), (255, 255, 255))

#for j in range(0,4):
#	img = Image.open(tmp_path+"/img%s.jpg" % (j)).convert("RGBA")
#	outImg = Image.alpha_composite(outImg, img)

jpeg_list = os.listdir(tmp_path)
outImg = np.zeros((height,width,3), np.uint8)
#outImg = cv2.imread(tmp_path+"/"+jpeg_list[i])
print(outImg.shape)
for i in range(len(jpeg_list)):
	print("Reading file: " + jpeg_list[i])
	next_img = cv2.imread(tmp_path+"/"+jpeg_list[i])
	outImg = cv2.addWeighted(outImg, 0.5, next_img, 0.5, 0)

cur_time = datetime.datetime.now()
stub = cur_time.strftime("%Y%m%d_%H%M%S_low")
outfile = img_path+"/%s.jpg" % (stub)
print("Combining images as "+stub)
cv2.imwrite(outfile, outImg)

