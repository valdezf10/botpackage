#!/usr/bin/env python 

import rospy
import os 
from time import sleep


plannerList = ['true', 'false'] # true = Dijkstra Planner, false = A*
sensorList = [1,2,3] # Number of sensors to change 

os.environ["WAITFORIT"]="true"
print("sofarsogood")
for counter in range(1,4):
		if counter == 1:
			os.environ['LASER_RANGE_VAL']=str(1.35)
			print("if ONE") 
		        sleep(5)
			print("done sleeping")	
		elif counter == 2: 
			os.environ['LASER_RANGE_VAL']=str(3.5)
			print("if TWO")
	 	elif counter == 3: 
			os.environ['LASER_RANGE_VAL']=str(5) 
			print("if THREE")
			
		for planner in plannerList:
			commandString = "roslaunch botpackage Sim_Launch_Compact.launch use_dijkatra:="
			commandString += planner
			os.system(commandString)
			testval =0
			while os.environ["WAITFORIT"] == true:
				if testval ==0:
					print("I am Waiting for Action to finish")
					testval +=1
			print("OUTSIDE OF WHILE")

