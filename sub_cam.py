#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2 as cv
from cv_bridge import CvBridge
import time
import pytesseract



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
        self.first_img = cv.imread('./first.png')
        self.second_img = cv.imread('./second.png')
        self.third_img = cv.imread('./third.png')
        self.finish_img = cv.imread('./finish.png')


    def listener_callback(self, msg):
        bridge = CvBridge()
        get_image = bridge.compressed_imgmsg_to_cv2(msg)
        get_image = cv.rotate(get_image,cv.ROTATE_180)
        now = time.time()
        cv.imwrite(f'./bot_camera_gather/rapa{str(now)}.jpg', get_image)
        get_text = pytesseract.image_to_string(get_image)

        if self.start == None and 'START' in get_text:
            self.start = now
        elif self.quarter1 == None and 'FIRST' in get_text:
            self.quarter1 = now
        elif self.quarter2 == None and 'SECOND' in get_text:
            self.quarter2 = now
        elif self.quarter3 == None and 'THIRD' in get_text:
            self.quarter3 = now 
        elif self.finish == None and 'FINISH' in get_text:
            self.finish = now   

        
        if cv.waitKey(10) == 27:
            get_image.release()

        if self.start and self.quarter1: 
            get_image[15:60,5:248,:] = self.first_img
            cv.putText(get_image, f"{self.quarter1 - self.start:.1f}sec", (100, 45), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
        if self.start and self.quarter2: 
            get_image[65:110,5:248,:] = self.second_img
            cv.putText(get_image, f"{self.quarter2 - self.start:.1f}sec", (100, 95), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
        if self.start and self.quarter3: 
            get_image[115:160,5:248,:] = self.third_img
            cv.putText(get_image, f"{self.quarter3 - self.start:.1f}sec", (100, 145), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1, cv.LINE_AA)
        if self.start and self.quarter1 and self.quarter2 and self.quarter3 and self.finish :
            self.lap_record = self.finish - self.start
            get_image[165:210,5:295,:] = self.finish_img
            cv.putText(get_image, f"{self.lap_record:.1f}sec", (100, 195), cv.FONT_HERSHEY_DUPLEX, 0.8, (0, 255, 0), 1, cv.LINE_AA)
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