#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
import cv2 as cv
from cv_bridge import CvBridge
import time

class ImgSubscriber(Node):

    def __init__(self):
        super().__init__('img_sub_scriber')
        self.subscription = self.create_subscription(
            CompressedImage,
            'botcam',
            self.listener_callback,
            10)
        self.subscription  


    def listener_callback(self, msg):
        bridge = CvBridge()
        get_image = bridge.compressed_imgmsg_to_cv2(msg)
        get_image = cv.rotate(get_image,cv.ROTATE_180)
        cv.imshow('bot_camera',get_image)
        if cv.waitKey(10) == 27:
            get_image.release()
        self.get_logger().info('이미지 받아옴')
        now = time.time()
        cv.imwrite(f'./bot_camera_gather/rapa{now}.jpg', get_image)


def main(args=None):
    rclpy.init(args=args)
    basic_subcriber = ImgSubscriber()
    rclpy.spin(basic_subcriber)

    basic_subcriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()