#!/usr/bin/env python

import rosbag, sys, csv
import time
import string
import os
import shutil
import numpy as np


#convert to coordinates to path length
def odomdata(currenttopic):
	poselist = []
	for subtopic, msg, t in currenttopic:	
		x = float(msg.pose.pose.position.x)
		y = float(msg.pose.pose.position.y)
		poselist.append([x,y])
	#filewriter.writerow(values)
	posearray = np.array(poselist)
	pathlength= posearray.diff(axis=0).sum(axis=0)
	finallength = np.sqrt(pathlength[0]**2+pathlength[1]**2)
	print finallength

def goaldata(currenttopic):
	poselist = np.array([])
	for subtopic, msg, t in currenttopic:	
		x = msg.pose.pose.position.x
		y = msg.pose.pose.position.y
		np.append(poselist, [x,y])
	#filewriter.writerow(values)
	length = np.diff(poselist)
	totallength = np.sqrt(length[0]**2+length[1]**2)
	print totallength

listOfBagFiles = [f for f in os.listdir("/home/jason/252_bot/src/botpackage/bag") if f[-4:] == ".bag"]	#get list of only bag files in current dir.
numberOfFiles = str(len(listOfBagFiles))
print "reading all " + numberOfFiles + " bagfiles in current directory: \n"
for f in listOfBagFiles:
	print f

count = 0
for bagFile in listOfBagFiles:
	count += 1
	print "reading file " + str(count) + " of  " + numberOfFiles + ": " + bagFile
	#access bag
	bag = rosbag.Bag("/home/jason/252_bot/src/botpackage/bag/" + bagFile)
	bagContents = bag.read_messages()
	bagName = bag.filename
	#firstIteration = True	#allows header row

	# if firstIteration:	# header
	# 	headers = ["rosbagTimestamp"]	#first column header
	# 	for pair in instantaneousListOfData:
	# 		headers.append(pair[0])
	# 	filewriter.writerow(headers)
	# 	firstIteration = False

	#get list of topics from the bag
	listOfTopics = []
	for topic, msg, t in bagContents:
		if topic not in listOfTopics:
			listOfTopics.append(topic)

	for topicName in listOfTopics:
		if topicName == '/odom': # or '/move_base/goal':
			with open("/home/jason/252_bot/src/botpackage/csv" + topicName +".csv", 'w') as csvfile:
				filewriter = csv.writer(csvfile, delimiter = ',')
				odomdata(bag.read_messages(topicName))

	bag.close()
print "Done reading all " + numberOfFiles + " bag files."