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

laserRanges= [.5,3.5]
laser_noise_range = [ 5, 40,] # Standard Deviations of Params Listed
imu_gyro_range = [.0002, .01]
imu_accel_range = [.017, .85]

def setDoor(val):
	if val== True:
		mainProg(100)
		os.environ["DOOR_PROB"]="100"
		print("Door Probability = 100%")    #Debug print	
	elif val ==False:
		mainProg(0)
		os.environ["DOOR_PROB"]="85"
		print("Door Probability = 85%")       # Debug print 

def Set_Default_Param():
	os.environ['LASER_RANGE_VAL']=str(3.5)
	os.environ['LASER_NOISE_STDDEV']=str(.01)
	os.environ['IMU_GYRO_NOISE_STDDEV']=str(.0002)
	os.environ['IMU_ACCEL_NOISE_STDDEV']=str(.017)
	
def Set_Env_Var(name, value):
	os.environ[str(name)]=str(value)
	sleep(1)

def startSim():
	os.system("roslaunch botpackage SimLaunch_timeout.launch")
        sleep(5)

	
def killSim():
	#os.system("rosnode kill -a")
	os.system("^C")
	
	
setParam = True 
timeout =0 
	
if __name__=="__main__":
	if setParam ==True:
		Set_Default_Param()   # Set Default Parameters 
		setParam== False 
		   
	for p1 in laserRanges:
		Set_Env_Var("LASER_RANGE_VAL",p1)
		
		for p2 in laser_noise_range:
			Set_Env_Var("LASER_NOISE_STDDEV",p2)
			
			for p3 in range(2): # both IMU properties change Simultaneously
				Set_Env_Var("IMU_GYRO_NOISE_STDDEV",imu_gyro_range[p3])
				Set_Env_Var("IMU_ACCEL_NOISE_STDDEV",imu_accel_range[p3])
 
				for doorState in doorOpen:     # loop through open and mostly open door stats
					setDoor(doorState)
					for planner in plannerList:  # loop through path planners
						if planner =='true':
							os.environ["PLANNER"]="Dijkstra"
							print("Export Planner env Var as Dijkstra")  #Debug print 
						elif planner =='false':
							os.environ["PLANNER"]="A*"
							print("Export Planner env Var as A*") # debug Print 			# Iterate over global planners
						Set_Env_Var("USE_DIJKSTRA",planner) # Set planner env var
						os.system("echo Dijkstra Value:")
						os.system("echo $USE_DIJKSTRA") 	# debug print 
									
						
						try: 
							startSim()	#begin Simulation
						
								
						except Exception:
							print("exception made")
							killSim()
							continue
