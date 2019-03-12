import matplotlib.pyplot as plt
import csv
import os

odom = []
goal = []
time2wpt = []
avgvel = []
wptdev = []

with open(os.path.dirname(os.path.realpath(__file__))[:-8] + "/csv/result.csv",'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        odom.append(int(row[0]))
        goal.append(int(row[1]))
        time2wpt.append(int(row[2]))
        avgvel.append(int(row[3]))
        wptdev.append(int(row[4]))

plt.plot(odom,goal, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()