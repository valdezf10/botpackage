#!/usr/bin/env python 

import rospy
import os 
import roslaunch
from time import sleep
from randommap import mainProg
#Iterative Simulation Parameters
#plannerList = ['false', 'true'] # Dijkstra: true=on, false=off
plannerList = ['true','false'] # Dijkstra: true=on, false=off
doorOpen = [True, False]

laserRanges= [.5, 1.5 ,3.5, 5]
laserRate = [1, 5 , 20, 40,]
imuRate = [100, 200, 400, 500 ] 

def setDoor(val):
	if val== True:
		mainProg(100)
	elif val ==False:
		mainProg(0)
	


def Set_Default_Param():
	os.environ['LASER_RANGE_VAL']=str(3.5)
	os.environ['LASER_UPDATE_RATE']=str(5)
	os.environ['IMU_UPDATE_RATE']=str(200)
	#print os.system("echo $LASER_RANGE_VAL")
	#print os.system("echo $LASER_UPDATE_RATE")
	#print os.system("echo $IMU_UPDATE_RATE")
	
	
def Set_Env_Var(name, value):
	os.environ[str(name)]=str(value)
	sleep(1)

def startSim():
	os.system("roslaunch botpackage SimLaunch_timeout.launch")
        

	
def killSim():
	#os.system("rosnode kill -a")
	os.system("^C")
	
	
setParam = True 
timeout =0 
	
if __name__=="__main__":
	if setParam ==True:
		Set_Default_Param()   # Set Default Parameters 
		setParam== False      
	setDoor(True)

	for planner in plannerList:			# Iterate over global planners
		Set_Env_Var("USE_DIJKSTRA",planner) # Set planner env var
		os.system("echo Dijkstra Value:")
		os.system("echo $USE_DIJKSTRA") 	# debug print 
					
		
		try: 
			startSim()	#begin Simulation
		
				
		except Exception:
			print("exception made")
			killSim()
			continue











