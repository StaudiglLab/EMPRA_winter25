import numpy as np
#from numpy import *
#loading only first three columns
ts,left_x,left_y=np.loadtxt('exampleEyetrackerData.csv',usecols=[0,1,2],unpack=True,skiprows=1,delimiter=',')
#print(ts)
#print(len(ts))
#print(len(left_x))
#print(len(left_y))


def avgSamples(nSamples):
    s=0
    counter=0
    for num in range(0,nSamples):
        #data=left_x[num]
        if(not np.isnan(left_x[num])):
            s=s+left_x[num]
            counter=counter+1
        #print(num,left_x[num],s)
    return s/counter
#TODO in class. Show how to look at the size of the array and how to retrieve elements in the array (contraints on what indexes can be)

print(avgSamples(10))
print(avgSamples(100))
print(avgSamples(10000))