from picamera import PiCamera 
from time import sleep 
import os
import sys 
import datetime as dt
date = ' ' 

def RunCamera():
	camera = PiCamera() 

	camera.rotation = 180
	camera.start_preview()
	for i in range(1):
		sleep(1)

		for t in range(3,0,-1): 
			camera.annotate_text = "%s" % t
			#camera.annotate_foreground = Color('white')
			#camera.annotate_background = Color('black')
			camera.annotate_text_size = 120 
			sleep(1)
 		camera.annotate_text = " "
		global date 
		date = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		camera.capture('/home/pi/PiPictures/Image%s.jpg' % date)
	camera.stop_preview() 
	return date 



