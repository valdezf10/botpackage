#!/usr/bin/env python

import roslib
#roslib.load_manifest('botpackage')
import rospy
from time import sleep

def parameterChange():
	rospy.init_node('parameter_reset')
	print 'Path Planner: Grid Path w/ Dijkstra'
	paramlist = 
	printn 
	sleep(25) 
	
	
    

  

if __name__ == '__main__':
    try:
		parameterChange()
     
		rospy.set_param('use_grid_path', "False")
		print "Grid Path Turned off"
		
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"
