#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2 as cv
from cv_bridge import CvBridge
import time
import pytesseract
import re

class ImgSubscriber(Node):

    def __init__(self):
        super().__init__('img_sub_scriber')
        self.subscription = self.create_subscription(
            CompressedImage,
            'botcam',
            self.listener_callback,
            10)
        self.subscription  
        self.start = None
        self.quarter1 = None
        self.quarter2 = None
        self.quarter3 = None
        self.finish = None
        self.lap_record = None


    def listener_callback(self, msg):
        bridge = CvBridge()
        get_image = bridge.compressed_imgmsg_to_cv2(msg)
        get_image = cv.rotate(get_image,cv.ROTATE_180)
        now = time.time()
        cv.imwrite(f'./bot_camera_gather/rapa{str(now)}.jpg', get_image)
        get_text = pytesseract.image_to_string(get_image)

        if 'START' in get_text:
            self.start = now
        elif 'FIRST' in get_text:
            self.quarter1 = now
        elif 'SECOND' in get_text:
            self.quarter2 = now
        elif 'THIRD' in get_text:
            self.quarter3 = now 
        elif 'FINISH' in get_text:
            self.finish = now   

        
        if cv.waitKey(10) == 27:
            get_image.release()

        if self.start and self.quarter1: 
            cv.putText(get_image, f"point1: {self.quarter1 - self.start:.2f} sec", (15, 45), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
        if self.start and self.quarter2: 
            cv.putText(get_image, f"point2: {self.quarter2 - self.start:.2f} sec", (15, 90), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
        if self.start and self.quarter3: 
            cv.putText(get_image, f"point1: {self.quarter3 - self.start:.2f} sec", (15, 135), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)

        if self.start and self.quarter1 and self.quarter2 and self.quarter3 and self.finish :
            self.lap_record = self.finish - self.start
            cv.putText(get_image, f"LAP Record: {self.lap_record:.2f} sec", (15, 180), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
            self.get_logger().info(f'LAP Record: {self.lap_record:.2f}')
        cv.imshow('bot_camera',get_image)

def main(args=None):
    rclpy.init(args=args)
    basic_subcriber = ImgSubscriber()
    rclpy.spin(basic_subcriber)

    basic_subcriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()