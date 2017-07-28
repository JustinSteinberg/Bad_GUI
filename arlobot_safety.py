#!/usr/bin/env python
import rospy
from arlobot_msgs.msg import arloSafety

class ArlobotSafety(object):
    def __init__(self):
        rospy.init_node('arlobot_safety')

        self._safetyStatusPublisher = rospy.Publisher('safetyStatus', arloSafety, queue_size=1)

        rospy.Subscriber('arlo_status',arloStatus,self.RSSI_Safety)

        rospy.spin()

    def RSSI_Safety(self,msg):
         safety_status = arloSafety()

        if(msg.safeToProceed or msg.safeToRecede): 
            safety_status.safeToGo = True
            safety_status.safeToOperate = True
        
        else:
            safety_status.safeToGo = False
            safety_status.safeToOperate = True
        
        self._safetyStatusPublisher.publish(safety_status)

if __name__ == '__main__':
    node = ArlobotSafety()
    
    