import itertools
import numpy as np
import matplotlib.pyplot as plt


def plotPsychometricCurve(whichExp,whichCondition):

    marker = itertools.cycle(('P', 's', 'v', 'o', '*')) 
    plt.figure(figsize=(4,4))
       
    
    if(whichExp=='contrast' or whichExp=='pooled'):    
        subIDs=[2,3,4,8,9,14,15,16,18,20,21]
        for subID in subIDs:
            displacement,nFwd,nTrials=np.loadtxt('./data_derived/contrast/Sub_%02d_%s.csv'%(subID,whichCondition),delimiter=',',unpack=True,skiprows=1)
            plt.plot(displacement,100*(nFwd/nTrials.astype("float")),marker=next(marker))

    if(whichExp=='shape' or whichExp=='pooled'):   
        subIDs=[5,6,7,11,12,13,22,24,25] 
        for subID in subIDs:
            displacement,nFwd,nTrials=np.loadtxt('./data_derived/shape/Sub_%02d_%s.csv'%(subID,whichCondition),delimiter=',',unpack=True,skiprows=1)
            plt.plot(displacement,100*(nFwd/nTrials.astype("float")),marker=next(marker))

    plt.axhline(50,c='gray',ls='--')
    plt.axvline(0.0,c='gray',ls='--')

    #plt.title(whichExp+", "+whichCondition)

    plt.xlabel("Displacement (degrees)")

    plt.ylabel("Percent Forward Response")
    plt.savefig("figures/psychometry_%s_%s.png"%(whichExp,whichCondition),bbox_inches='tight')


def plotAll(whichExp):
    #call function for appropriate plot
    plotPsychometricCurve(whichExp='pooled',whichCondition='Blank')
    plotPsychometricCurve(whichExp='pooled',whichCondition='NoBlank')
    
    plotPsychometricCurve(whichExp=whichExp,whichCondition='Blank')
    plotPsychometricCurve(whichExp=whichExp,whichCondition='NoBlank')
    plotPsychometricCurve(whichExp=whichExp,whichCondition='Change')

    ##plt.legend()
