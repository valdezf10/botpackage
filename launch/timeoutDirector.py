#!/usr/bin/env python 

import rospy
import os 
import roslaunch
from time import sleep

#Iterative Simulation Parameters
#plannerList = ['false', 'true'] # Dijkstra: true=on, false=off
plannerList = ['true','false'] # Dijkstra: true=on, false=off

laserRanges= [.5, 1.5 ,3.5, 5]
laserRate = [1, 5 , 20, 40,]
imuRate = [100, 200, 400, 500 ] 


def Set_Default_Param():
	os.environ['LASER_RANGE_VAL']=str(3.5)
	os.environ['LASER_UPDATE_RATE']=str(5)
	os.environ['IMU_UPDATE_RATE']=str(200)
	#print os.system("echo $LASER_RANGE_VAL")
	#print os.system("echo $LASER_UPDATE_RATE")
	#print os.system("echo $IMU_UPDATE_RATE")
	os.environ["WAITFORIT"]="true"
	
def Set_Env_Var(name, value):
	os.environ[str(name)]=str(value)
	sleep(1)

def startSim():
	#os.system("roslaunch botpackage slamtesting.launch")
	#os.system("roslaunch botpackage Sim_Launch_Compact.launch")
        #os.system("roslaunch botpackage SimLaunch_timeout.launch")
        os.system("roslaunch botpackage launch.launch")

	
def killSim():
	#os.system("rosnode kill -a")
	os.system("^C")
	
	
setParam = True 
timeout =0 
	
if __name__=="__main__":
	if setParam ==True:
		Set_Default_Param()   # Set Default Parameters 
		setParam== False      

	for planner in plannerList:			# Iterate over global planners
		Set_Env_Var("USE_DIJKSTRA",planner) # Set planner env var
		os.system("echo Dijkstra Value:")
		os.system("echo $USE_DIJKSTRA") 	# debug print 
		#while os.environ["WAITFORIT"]=="true":			
		
		try: 
			startSim()	#begin Simulation
		
				
		except Exception:
			print("exception made")
			killSim()
			continue
		
		
	
	
	
	
	
	
	


















 







#for counter in range(1,4):
#		if counter == 1:
#			os.environ['LASER_RANGE_VAL']=str(1.35)
#			print("if ONE") 
#
#		       
#			
#		for planner in plannerList:
#			os.environ["use_dijkstra"]=planner
#			#print(process.is_alive())
#			
#			while os.environ["WAITFORIT"] == true:
#				if testval ==0:
#					print("I am Waiting for Action to finish")
#					testval +=1
##			print("OUTSIDE OF WHILE")
#
#
#
#
