#!/usr/bin/env python

import rospy
import os
import cv2
import glob
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
from std_msgs.msg import Header




def main():
    rospy.init_node('stereo_image_publisher')

    left_pub = rospy.Publisher('/camera/left/image_rect_color', Image, queue_size=10)
    right_pub = rospy.Publisher('/camera/right/image_rect_color', Image, queue_size=10)

    #left_pub = rospy.Publisher('image_left/image_color_rect', Image, queue_size=10)
    #right_pub = rospy.Publisher('image_right/image_color_rect', Image, queue_size=10)
    #cam_info_pub = rospy.Publisher('/camera/left/camera_info', CameraInfo, queue_size=1)

    bridge = CvBridge()

    image_dir = rospy.get_param('~image_dir', 'camera')
    #fps = rospy.get_param('~fps', 30.0)
    rate = rospy.Rate(1)

    left_images = sorted(glob.glob(os.path.join(image_dir, 'img_rect_left_*.png')))
    right_images = sorted(glob.glob(os.path.join(image_dir, 'img_rect_right_*.png')))

    print(len(left_images))
    print(len(right_images))
    if len(left_images) != len(right_images):
        rospy.logerr("Unterschiedliche Anzahl von linken und rechten Bildern!")
        return

   
    #while not rospy.is_shutdown():
    for left_path, right_path in zip(left_images, right_images):
        ts_left = left_path.split('_')[-1].split('.')[0]
        ts_right = right_path.split('_')[-1].split('.')[0]

        
        #if ts_left != ts_right:
        #    print("No image Pair: {}, {}" %(ts_left, ts_right))
        #    continue
    


        headerLeft = Header()
        headerRight = Header()
        stamp = rospy.Time.now()


        # Links
        left_img = cv2.imread(left_path, cv2.IMREAD_GRAYSCALE)
        left_msg = bridge.cv2_to_imgmsg(left_img, encoding="mono8")
        headerLeft.frame_id = "/camera_left"
        headerLeft.stamp = stamp
        left_msg.header = headerLeft

        # Rechts
        right_img = cv2.imread(right_path, cv2.IMREAD_GRAYSCALE)
        right_msg = bridge.cv2_to_imgmsg(right_img, encoding="mono8")
        headerRight.frame_id = "/camera_right"
        headerRight.stamp = stamp
        right_msg.header = headerRight


        left_pub.publish(left_msg)
        #print(left_msg.header)
        right_pub.publish(right_msg)
        #cam_info_pub.publish(cam_info)
        #print("Sende Bild mit Zeitstempel:", header.stamp.to_sec())

        #rospy.loginfo_throttle(5, "Sende Bild mit Zeitstempel: %s", header.stamp)
        rate.sleep()

    rospy.loginfo("Fertig mit allen Bildern.")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass


