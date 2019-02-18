#!/usr/bin/env python
import rospy
import sys
import os 
import random
import xml.etree.ElementTree as ET
from randommap.srv import *


def randommapcallback(prob):    
    #RNG init
    seed = random.randrange(sys.maxsize)
    random.seed(a=seed) # TODO: add something to send a seed for testing

    #get xml handling started
    inputxml = os.path.dirname(os.path.realpath(__file__))[:-7] + "/models/Bainer_Hall_FP/model.sdf"
    tree = ET.parse(inputxml)
    root = tree.getroot()
    dooropenprob = prob.probability

    #loop through doors
    for objects in root.iter('link'):
        if objects.attrib['name'][:4] == 'Door':
            if random.random() <= dooropenprob/100:
                chunks = objects.find('pose').text.split()
                chunks[2] = '-3'                                  #put it 3m in the ground
                objects.find('pose').text = ' '.join(chunks)
    tree.write(inputxml[:-4] + 'random.sdf')
    return seed

def random_map_server():
    rospy.init_node('random_map_server')
    s = rospy.Service('random_map', probability, randommapcallback)
    print "Ready to generate map."
    rospy.spin()
    
if __name__ == '__main__':
    random_map_server()