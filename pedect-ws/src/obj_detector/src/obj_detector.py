#!/usr/bin/env python

""" Example of using object detector

This node subscribes to topic with images and applies detector
to find objects. It publishes detected bounding boxes with a
time stamp of image using custom message type DetectedBoxes.
"""

import rospy
import cv2
import json
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from objdet.pure_tf_detector import Detector
from detect_msg.msg import DetectedBoxes

class ObjDetector:
    def __init__(self, camera_topic, detection_topic, pb_path, meta_path, threshold):
        """
        Initializes detector

        :param camera_topic: Name of topic to subscribe.
        """
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(camera_topic, Image, self.img_callback)
        self.bboxes_pub = rospy.Publisher(detection_topic, DetectedBoxes, queue_size=5)

        self.bridge = CvBridge()

        self.detector = Detector(pb_path, meta_path)
        self.threshold = threshold

    def img_callback(self, img_msg):
        """Image topic callback

        Performs detection on image from topic, constructs msg with detection result and publishes it.
        :param img_msg: sensor_msgs/Image message
        """
        try:
            cv_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        except CvBridgeError as e:
            print(e)

        boxes_list = self.detector.return_predict(cv_image, self.threshold)

        msg_to_pub = self.msg_constructor(img_msg, boxes_list)
        self.bboxes_pub.publish(msg_to_pub)

    def msg_constructor(self, img_msg, boxes_list):
        """
        Construct DetectedBoxes message.

        :param img_msg: Image message used for detection (required to copy header)
        :param boxes_list: List of predicted bounding boxes with labels.
        :return: DetectedBoxes message.
        """
        detect_msg = DetectedBoxes()
        detect_msg.header = img_msg.header # reuse header of image to have same timestamp

        res_dict = dict()
        i = 0
        for box in boxes_list:
            box['confidence'] = int(box['confidence'] * 100)  # Confidence in percents without decimals
            res_dict[str(i)] = box
            i += 1

        detect_msg.dictionary = json.dumps(res_dict) # Creating a string from dictionary and put in msg field

        return detect_msg

if __name__ == "__main__":

    net_files_path = '/home/rr/Desktop/built_graph/'

    pb_file = net_files_path + 'tiny-yolo-voc.pb'
    meta_file = net_files_path + 'tiny-yolo-voc.meta'

    threshold = 0.5

    rospy.init_node('detection_consumer', anonymous=True)
    detector = ObjDetector("/my_camera_frame", "my_boxes", pb_file, meta_file, threshold)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()


