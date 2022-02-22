#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2 as cv
from cv_bridge import CvBridge
import numpy as np

class BotCamPublisher(Node):

    def __init__(self):
        super().__init__('bot_cam_publisher')
        self.publisher_ = self.create_publisher(CompressedImage, 'botcam', 10)

    def img_publisher(self,cv_img):
        self.publisher_.publish(cv_img)

def main(args=None):
    rclpy.init(args=args)
    pub = BotCamPublisher()
    bridge = CvBridge()
    
    cap = cv.VideoCapture(0)
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        cv_img = bridge.cv2_to_compressed_imgmsg(img)

        pub.img_publisher(cv_img)
    cap.release()

if __name__ == '__main__':
    main()