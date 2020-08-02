#!/usr/bin/python

import rospy, math
from std_msgs.msg import Int32MultiArray

#global angle

xycar_msg = Int32MultiArray()

def callback(msg):
    print(msg)
    if msg.data[2] > 150:
        angle = 90
        xycar_msg.data = [angle, 50]
        motor_pub.publish(xycar_msg)
        print("1 : ", angle)
    else:
        angle = 0
        xycar_msg.data = [angle, 50]
        motor_pub.publish(xycar_msg)
        print("2 : ", angle)

rospy.init_node('guide')
ultra_sub = rospy.Subscriber('ultrasonic', Int32MultiArray, callback)
motor_pub = rospy.Publisher('xycar_motor_msg', Int32MultiArray, queue_size=1)

while not rospy.is_shutdown():
    a = 1
