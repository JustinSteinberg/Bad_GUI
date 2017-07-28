#!/usr/bin/python

import serial 
import threading
import rospy
from sensor_msgs.msg import Joy

Button = [joy.A(),joy.B(),joy.Y(),joy.leftBumper(),joy.rightBumper(),joy.Back(),joy.Start(),joy.Guide(),
		  joy.leftThumbstick(),joy.rightThumbstick(),joy.dpadLef(),joy.dpadRight(),joy.dpadUp(),joy.dpadDown()]

Axis = [fmtFloat(joy.leftX()),fmtFloat(joy.leftY()),fmtFloat(joy.leftTrigger()),fmtFloat(joy.rightX()),
	    fmtFloat(joy.rightY()),fmtFloat(joy.rightTrigger())]

def listen():
    line = ''
    msg = Joy()
    while True:
        try:
            c = ser.readline()
            print c
            if line or c == '[':
              line = line + c
            else:
              continue
            if c == '\n':
                statuses = yaml.safe_load(line)
                line = ''
                now = rospy.get_rostime()
                msg.header.stamp = now
                msg.button = Button
                msg.axis = Axis
                         
            pub.publish(msg)
        except Exception as e:
        	print(e)
            

def talker():
	s = serial.Serial('/dev/tty.usbserial-DN02PI7H', 115200, timeout = 10.0)
	pub = rospy.Publisher('joy',Joy)
	rospy.init_node('joy_talker')
	tStat = threading.Thread(target=listen,name='Status Thread')
	tStat.daemon = True
	tStat.start()
	rospy.spin() 
   
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass