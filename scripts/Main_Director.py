#!/usr/bin/env python

import os
from time import sleep
import randommap
import datetime



# Iterative Simulation Parameters
plannerList = ['false','true']  # Dijkstra: true=on, false=off
doorOpen = [True, False]

laserRanges = [3.5,.5]
laser_noise_range = [.01, .1]  # Standard Deviations of Params Listed
imu_gyro_range = [.0002, .01]
imu_accel_range = [.017, .85]


def setDoor(val):
    if val == True:
        randommap.mainProg(100)
        Set_Env_Var("DOOR_PROB", "100")
        print("Door Probability = 100%")
    elif val == False:
        randommap.mainProg(0)
        Set_Env_Var("DOOR_PROB", "85")
        print("Door Probability = 85%")


def Set_Default_Param():
    Set_Env_Var('LASER_RANGE_VAL', str(3.5))
    Set_Env_Var('LASER_NOISE_STDDEV', str(.01))
    Set_Env_Var('IMU_GYRO_NOISE_STDDEV', str(.0002))
    Set_Env_Var('IMU_ACCEL_NOISE_STDDEV', str(.017))


def Set_Env_Var(name, value):
    os.environ[str(name)] = str(value)
    sleep(1)


def startSim():
    os.system("roslaunch botpackage SimLaunch_timeout.launch")
    sleep(5)


def killSim():
    os.system("^C")


if __name__ == "__main__":
    Set_Default_Param()

    for p1 in laserRanges:
        Set_Env_Var("LASER_RANGE_VAL", p1)

        for p2 in laser_noise_range:
            Set_Env_Var("LASER_NOISE_STDDEV", p2)

            for p3 in range(2):  # both IMU properties change Simultaneously
                Set_Env_Var("IMU_GYRO_NOISE_STDDEV", imu_gyro_range[p3])
                Set_Env_Var("IMU_ACCEL_NOISE_STDDEV", imu_accel_range[p3])

                for doorState in doorOpen:     # loop through open and mostly open door stats
                    setDoor(doorState)
                    for planner in plannerList:  # loop through path planners
                        if planner == 'true':
                            Set_Env_Var("PLANNER", "Dijkstra")
                            print("Export Planner env Var as Dijkstra")
                        elif planner == 'false':
                            Set_Env_Var("PLANNER", "A*")
                            print("Export Planner env Var as A*")
                        # Set planner env var
                        Set_Env_Var("USE_DIJKSTRA", planner)
                        os.system("echo Dijkstra Value:")
                        os.system("echo $USE_DIJKSTRA")

                        try:
                            startSim()

                        except Exception:
                            print("exception in Director" + str(datetime.datetime.now()))
                            killSim()
                            continue
