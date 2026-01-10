import numpy as np
import matplotlib.pyplot as plt
#loading only first three columns
ts,left_x,left_y,right_x,right_y=np.loadtxt('exampleEyetrackerData.csv',usecols=[0,1,2,4,5],unpack=True,skiprows=1,delimiter=',')

#plt.plot(ts,left_x,label='x ')
#plt.plot(ts,left_y,label='y')
plt.plot(left_x,left_y)
plt.xlim((0,1920))
plt.ylim((0,1080))
plt.xlabel("x")
plt.ylabel("y")
#plt.xlabel("Time (seconds)")
#plt.ylabel("gaze (x-coordinate in pixels)")
plt.legend()
plt.show()

#TODO in class: plot each variable one at a time

#TODO in class: understand "gaps" in data; understand data quality from plot

#TODO in class: plot each variable as a function of time

#TODO in class: plot a "meaningful" time axes; first intro to array operations
