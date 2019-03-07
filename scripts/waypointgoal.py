#!/usr/bin/env python

import roslib
roslib.load_manifest('botpackage')
import rospy
import actionlib
import csv
import os

#move_base_msgs
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def waypoint_goal():
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction )

    #create goal
    goal = MoveBaseGoal()

    inputcoords = os.path.dirname(os.path.realpath(__file__))[:-7] + "waypointset.csv"
    with open(inputcoords, 'rb') as csvfile:
        creader = csv.reader(csvfile)
        allcoords= list(creader)
    rownum = 0

    for row in allcoords:
        rownum += 1
        x = float(row[0])
        y = float(row[1]) #swapped for some reason

        #set goal
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1.0
        goal.target_pose.header.frame_id = '/map'
        goal.target_pose.header.stamp = rospy.Time.now()

        #start listner
        sac.wait_for_server()

        #send goal
        sac.send_goal(goal)

        #finish
        sac.wait_for_result()

        #print result
        rospy.loginfo("Arrived at waypoint(" + str(rownum) + "/" + str(len(allcoords)) + "):" + str(x) + ", " + str(y))

if __name__ == '__main__':
    rospy.init_node('waypoint_goal')
    try:
        waypoint_goal()
        os.system("rosnode kill -a")
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"