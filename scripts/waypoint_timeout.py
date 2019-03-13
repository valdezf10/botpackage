#!/usr/bin/env python

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import bag2csv
import time
import os
import csv
import actionlib
import rospy
import roslib
roslib.load_manifest('botpackage')


def waypoint_goal():
    sac = actionlib.SimpleActionClient('move_base', MoveBaseAction)

    goal = MoveBaseGoal()

    inputcoords = os.path.dirname(os.path.realpath(__file__))[
        :-7] + "waypointset.csv"
    with open(inputcoords, 'rb') as csvfile:
        creader = csv.reader(csvfile)
        allcoords = list(creader)
    rownum = 0

    for row in allcoords:
        rownum += 1
        x = float(row[0])
        y = float(row[1])  # swapped for some reason

        # set goal
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1.0
        goal.target_pose.header.frame_id = '/map'
        goal.target_pose.header.stamp = rospy.Time.now()

        # start listner
        sac.wait_for_server()

        # send goal
        sac.send_goal(goal)

        # finish
        sac.wait_for_result(rospy.Duration(60*8))

        #print result
        print("Arrived at waypoint(" + str(rownum) + "/" +
                      str(len(allcoords)) + "):" + str(x) + ", " + str(y))


if __name__ == '__main__':
    rospy.init_node('timeout_goal')

    try:
        print("TIME OUT SIMULATION")
        waypoint_goal()
        bag2csv.go()  # runs "bag2csv.py" for data export
        os.system("rosnode kill -a")
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"
    except Exception:
        bag2csv.go()     # runs "bag2csv.py" for data export
        os.system("rosnode kill -a")
        os.system("^C")
