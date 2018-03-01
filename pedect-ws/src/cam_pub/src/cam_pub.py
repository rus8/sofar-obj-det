#!/usr/bin/env python

""" Simple camera frame publisher

This node reads frames from camera, converts them to
sensor_msgs/Image message and publishes under topic
"my_camera_frame".

WARNING: It's assumed that camera is normal, so
OpenCV gets BGR images.
"""

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def cam_pub():
    pub = rospy.Publisher('my_camera_frame', Image, queue_size=5)
    rospy.init_node('cam_pub')
    rate = rospy.Rate(1)  # 1 Hz
    cap = cv2.VideoCapture(0)  # Init source of frames
    bridge = CvBridge()  # Init message constructor

    # While roscore is running and while camera is able to return frames
    retv, frame = cap.read()
    while (not rospy.is_shutdown()) and retv:
        retv, frame = cap.read()
        try:
            image_message = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            pub.publish(image_message)
        except CvBridgeError as e:
            print(e)

        rate.sleep()


if __name__ == "__main__":
    try:
        cam_pub()
    except rospy.ROSInterruptException:
        pass


