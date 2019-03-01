#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState

pub = rospy.Publisher('initialpose', PoseWithCovarianceStamped, queue_size=10)
rospy.init_node('create_turtle')

def setrobotpos(x,y):
##### Will set the position of the turtlebot in Gazebo #####
    rospy.wait_for_service('/gazebo/set_model_state')
    model_pose = Pose()
    model_pose.position.x = x
    model_pose.position.y = y
    model_pose.position.z = 0
    modelstate = ModelState()
    modelstate.model_name = 'turtlebot3'
    modelstate.reference_frame = 'world'
    modelstate.pose = model_pose
    set_model_srv = rospy.ServiceProxy('gazebo/set_model_state', SetModelState)
    set_model_srv.call(modelstate)

##### Will set the localization for amcl #####
    new_pose = PoseWithCovarianceStamped()
    new_pose.pose = model_pose
    pub.publish(new_pose)


if __name__ == "__main__":
    setrobotpos(0,0)