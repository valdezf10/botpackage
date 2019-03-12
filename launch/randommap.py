#!/usr/bin/env python

import sys
import os 
import random
import xml.etree.ElementTree as ET
import csv


def randomcoords():    
    ### generate random waypoints ###
    inputcoords = os.path.dirname(os.path.realpath(__file__))[:-7] + "coords.csv"
    outputcoords = os.path.dirname(os.path.realpath(__file__))[:-7] + "waypointset.csv"
    with open(inputcoords, 'rb') as csvfile:
        creader = csv.reader(csvfile)
        allcoords= list(creader)
    newcoords = random.sample(allcoords,10) # change 10 at some point
    
    with open(outputcoords, 'w') as csvfile:
        cwriter = csv.writer(csvfile)
        cwriter.writerows(newcoords)

def randommap(prob):
    #RNG init
    seed = random.randrange(sys.maxsize)
    random.seed(a=seed)

    ### Generate random open doors ###
    inputxml = os.path.dirname(os.path.realpath(__file__))[:-7] + "/models/Bainer_Hall_FP/model.sdf"
    tree = ET.parse(inputxml)
    root = tree.getroot()
    dooropenprob = prob

    for objects in root.iter('link'):
        if objects.attrib['name'][:4] == 'Door':
            if random.random() <= dooropenprob/100.0:
                chunks = objects.find('pose').text.split()
                chunks[2] = '-3'                                  #put it 3m in the ground
                objects.find('pose').text = ' '.join(chunks)
    tree.write(inputxml[:-4] + 'random.sdf')
    return seed

def mainProg(val):
 #   if len(sys.argv) == 2:
  #      prob = float(sys.argv[1])
   # else:
    #    prob = 100
    #print(randommap(prob))
    if val <= 100 and val >=0:
        prob = val
    else:
        prob = 100
    print(randommap(prob))


