#!/usr/bin/env python

import rosbag, sys, csv
import time
import string
import os
import shutil
import numpy as np


#convert to coordinates to path length
def odomdata(currenttopic, endtimes):
	poselist = []
	for subtopic, msg, t in currenttopic:	
		x = msg.pose.pose.position.x
		y = msg.pose.pose.position.y
		currenttime = float(msg.header.stamp.nsecs)/float(10**9) + msg.header.stamp.secs
		poselist.append([x,y,currenttime])
	splitlengths = []
	lastendtime = 0.0
	for endtime in endtimes:
		split = []
		for counter,x in enumerate(poselist):
			if lastendtime<= poselist[counter][2] <=endtime:
				split.append(poselist[counter])
		lastendtime = endtime
		posearray = np.array(split)
		pathdiff= np.diff(posearray, axis=0)
		totalpath = np.sum(pathdiff, axis=0)
		finallength = np.sqrt(totalpath[0]**2+totalpath[1]**2)
		splitlengths.append(finallength)
	return splitlengths

def goaldata(currenttopic):
	goallist = []
	xlast = 0.0
	ylast = 0.0
	for subtopic, msg, t in currenttopic:	
		x = msg.goal.target_pose.pose.position.x
		y = msg.goal.target_pose.pose.position.y
		finallength = np.sqrt((x-xlast)**2+(y-ylast)**2)
		goallist.append(finallength) 
		xlast = x
		ylast = y
	goallist = np.array(goallist)
	return goallist

def resultdata(currenttopic):
	timelist = [0.0]
	for subtopic, msg, t in currenttopic:	
		finishtime = float(msg.header.stamp.nsecs)/float(10**9) + msg.header.stamp.secs
		timelist.append(finishtime)
	timearray = np.array(timelist)
	timediff = np.diff(timearray, axis=0)
	return timediff, timelist[1:]

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

	result,endtimes = resultdata(bag.read_messages('/move_base/result'))
	odom = odomdata(bag.read_messages('/odom'), endtimes)
	goal = goaldata(bag.read_messages('/move_base/goal'))
	with open("/home/jason/252_bot/src/botpackage/csv/result.csv", 'a') as csvfile: #change to 'a' for append
		filewriter = csv.writer(csvfile, delimiter = ',')
		filewriter.writerows(np.column_stack((np.array(odom),goal,result)))
	bag.close()
print "Done reading all " + numberOfFiles + " bag files."