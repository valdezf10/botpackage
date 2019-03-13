#!/usr/bin/env python

import rospy
import csv
from geometry_msgs.msg import PoseWithCovarianceStamped


def callback(gotpose):
    gotx = gotpose.pose.pose.position.x
    goty = gotpose.pose.pose.position.y
    with open('coords.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        print('got point')
        writer.writerow([gotx, goty])

    csvFile.close()


def listener():
    rospy.init_node('coord_listener')
    rospy.Subscriber("/initialpose", PoseWithCovarianceStamped, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == "__main__":
    listener()
