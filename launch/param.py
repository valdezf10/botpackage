import os 



	
if __name__ =="__main__":
	os.environ["LASER_RANGE_VAL"]=str(3.5)
	os.environ["LASER_UPDATE_RATE"]=str(5)
	os.environ["IMU_UPDATE_RATE"]=str(200)
	#print os.system("echo $LASER_RANGE_VAL")
	#print os.system("echo $LASER_UPDATE_RATE")
	#print os.system("echo $IMU_UPDATE_RATE")
	os.environ["WAITFORIT"]="true"
	os.environ["USE_DIJKSTRA"]="true"
