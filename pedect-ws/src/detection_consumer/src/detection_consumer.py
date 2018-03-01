#!/usr/bin/env python3

""" Image topic subscriber

This node subscribes to topic "my_camera_frame" sensor_msgs/Image
messages, converts messages to OpenCV images and shows them.

"""
import rospy
import message_filters
import cv2
import random
import json
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from obj_detector.msg import DetectedBoxes


# BGR!
color_codes = [
    (0, 0, 255),  # red
    (0, 255, 0),  # lime
    (255, 0, 255),  # magenta
    (128, 0, 128),  # purple
    (0, 215, 255),  # gold
    (238, 130, 238),  # violet
    (0, 255, 255),  # yellow
    (0, 69, 255),  # orange red
    (127, 255, 0)  # spring green
]


class SubBoxDraw:
    def __init__(self, camera_topic, detection_topic):
        """
        Initializes double subscriber with synchronization

        :param camera_topic:
        :param detection_topic:
        """
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber(camera_topic, Image)
        self.bboxes_sub = rospy.Subscriber(detection_topic, DetectedBoxes)
        self.ts = message_filters.TimeSynchronizer([self.image_sub, self.bboxes_sub], 5)
        self.ts.registerCallback(self.callback)

    def callback(self, img_msg, detect_msg):
        """

        :param img_msg:
        :param detect_msg:
        :return:
        """
        try:
            cv_image = self.bridge.imgmsg_to_cv2(img_msg, "bgr8")
        except CvBridgeError as e:
            print(e)
            return

        bboxes = json.loads(detect_msg.dictionary)  # Parsing string back to dictionary

        # Drawing boxes
        for box in bboxes.values():
            color = random.choice(color_codes)
            x1 = box['topleft']['x']
            y1 = box['topleft']['y']
            x2 = box['bottomright']['x']
            y2 = box['bottomright']['y']
            font = cv2.FONT_HERSHEY_PLAIN
            img = cv2.rectangle(cv_image, (x1, y1), (x2, y2), color, thickness=2)
            img = cv2.putText(img, box['label'] + ' ' + str(box['confidence']) + ' %', (x1, y1), font, 1, color,
                              thickness=2)

        cv2.imshow("Camera stream", img)
        cv2.waitKey(10)


if __name__ == '__main__':
    rospy.init_node('Detection_consumer', anonymous=True)
    sync_sub = SubBoxDraw("/my_camera_frame", "/my_boxes")
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
        cv2.destroyAllWindows()
