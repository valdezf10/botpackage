# botpackage
This is a ROS package that will test turtlebot3's performance with different planners and sensor packages.

## Structure
* for n trials:
  * randomize waypoints (randomwaypts_node.py)
  * for doors open/closed (randommap_node.py open.launch close.launch):
    * for sensor package (using rospy param):
      * for global planner (using rospy param):
        * for paths (waypointgoal.py):
          * record statistics (matplotlib :blush:)
