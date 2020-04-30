# botpackage
This is a ROS package that will test turtlebot3's performance with different planners and sensor packages.

## Structure
Director file:
* generate new waypoints and new random map `randommap.py`:
  * takes input "probability" (probability a given door is open, start with ~80)
* loop over physical parameters and planners with env variables
  * launch openmap files with given robot setup `*.launch`:
    * use modelopen.config
  * check if ros is running
  * build csv results file `bag2csv.py`:
  * launch randomdoor file with given robot setup `*.launch`:
    * use modelrandom.config
    * need to explore robot behavior if room is blocked
  * check if ros is running
  * build csv results file `bag2csv.py`:
