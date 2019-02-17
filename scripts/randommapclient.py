#!/usr/bin/env python
import sys
import rospy
from randommap.srv import *


def random_map_client(prob):
    rospy.wait_for_service('random_map')
    try:
        randommap_handle = rospy.ServiceProxy('random_map', probability)
        resp1 = randommap_handle(prob)
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    if len(sys.argv) == 2:
        prob = int(sys.argv[1])
    else:

        sys.exit(1)
    print "Requesting %s"%(prob)
    random_map_client(prob)