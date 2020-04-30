#!/usr/bin/env python

import rosbag
import csv
import os
import numpy as np


# convert to coordinates to path length
def odomdata(currenttopic, endtimes):
    poselist = []
    for subtopic, msg, t in currenttopic:
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        currenttime = float(msg.header.stamp.nsecs) / \
            float(10**9) + msg.header.stamp.secs
        poselist.append([x, y, currenttime])
    splitlengths = []
    lastendtime = 0.0
    for endtime in endtimes:
        split = []
        for counter, x in enumerate(poselist):
            if lastendtime <= poselist[counter][2] <= endtime:
                split.append(poselist[counter])
        lastendtime = endtime
        posearray = np.array(split)
        pathdiff = np.diff(posearray, axis=0)
        pathabs = np.abs(pathdiff)
        totalpath = np.sum(pathabs, axis=0)
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
        finishtime = float(msg.header.stamp.nsecs) / \
            float(10**9) + msg.header.stamp.secs
        timelist.append(finishtime)
    timearray = np.array(timelist)
    timediff = np.diff(timearray, axis=0)
    return timediff, timelist[1:]


def go():
    # get list of only bag files in current dir.
    listOfBagFiles = sorted([f for f in os.listdir(os.path.dirname(
        os.path.realpath(__file__))[:-8] + "/bag") if f[-4:] == ".bag"])
    try:
        bagFile = listOfBagFiles[-1]  # use last file created
    except IndexError:
        print("No bag files.")
        return
    print "Reading file: " + bagFile
    # access bag
    bag = rosbag.Bag(os.path.dirname(os.path.realpath(__file__))[
                     :-8] + "/bag/" + bagFile)

    # add header if file is empty
    writeheader = False
    headerrow = ["File", "Odom Distance (m)", "Goal Distance (m)", "Time to waypoint (s)", "Average Velocity Over Waypoint (m/s)",
                 "Standardized Waypoint Deviation (m/m)", "Lidar Range", "Lidar Rate", "IMU Rate", "Planner", "Door Probability", "Laser Noise", "Gyro Noise", "Accel Noise", "Dijkstra"]
    if os.path.isfile(os.path.dirname(os.path.realpath(__file__))[:-8] + "/csv/result.csv"):
        if os.stat(os.path.dirname(os.path.realpath(__file__))[:-8] + "/csv/result.csv").st_size == 0:
            writeheader = True
    else:
        writeheader = True

    result, endtimes = resultdata(bag.read_messages('/move_base/result'))
    odom = np.array(odomdata(bag.read_messages(
        '/odom'), endtimes))[:len(result)]
    goal = goaldata(bag.read_messages('/move_base/goal'))[:len(result)]
    avgvel = odom/result
    stdwpt = odom/goal
    # tested with variables, unsure what will happen if they are unset
    try:
        lidarrange = [os.environ['LASER_RANGE_VAL']] * len(result)
        lidarrate = [os.environ['LASER_UPDATE_RATE']] * len(result)
        imurate = [os.environ['IMU_UPDATE_RATE']] * len(result)
        planner = [os.environ['PLANNER']] * len(result)
        door = [os.environ['DOOR_PROB']] * len(result)
        lasernoise = [os.environ['LASER_NOISE_STDDEV']] * len(result)
        imugyronoise = [os.environ['IMU_GYRO_NOISE_STDDEV']] * len(result)
        imuaccelnoise = [os.environ['IMU_ACCEL_NOISE_STDDEV']] * len(result)
        dijkstra = [os.environ["USE_DIJKSTRA"]] * len(result)
        bagFilecolumn = [bagFile] * len(result)
    except KeyError:
        lidarrange = [""] * len(result)
        lidarrate = [""] * len(result)
        imurate = [""] * len(result)
        planner = [""] * len(result)
        door = [""] * len(result)
        lasernoise = [""] * len(result)
        imugyronoise = [""] * len(result)
        imuaccelnoise = [""] * len(result)
        dijkstra = [""] * len(result)
        bagFilecolumn = [""] * len(result)
        print("Keys not set correctly")

    # change to 'a' for append
    with open(os.path.dirname(os.path.realpath(__file__))[:-8] + "/csv/result.csv", 'a') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        if writeheader:
            filewriter.writerow(headerrow)
        filewriter.writerows(np.column_stack(
            (bagFilecolumn, odom, goal, result, avgvel, stdwpt, lidarrange, lidarrate, imurate, planner, door, lasernoise, imugyronoise, imuaccelnoise, dijkstra)))
    bag.close()
    print "Done reading bag file."


if __name__ == "__main__":
    go()
