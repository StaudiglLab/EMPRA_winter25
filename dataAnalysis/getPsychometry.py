import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy

def getPsychometricCurve(subID,whichTask='Blank'):
    
    df=pd.read_csv("./data/%s_s1_TSD/task_TSD_%s_s1_trialSequence.csv"%(subID,subID))
    
    #exclude trials where no saccades where made
    df=df[df['response'].values!='NoSaccadeMade']
    selmask= np.loadtxt("./data_derived/trialSelection/%s.txt"%subID)>0.5
    df=df[selmask]
    #select trials with correct task type
    df=df[np.logical_and(df['trialType']==whichTask,df['displacement']!=np.nan)]  

    #get direction of saccade: positive for right and negative for left      
    saccadeDirection=np.sign(df['targetPosition']-df['fixPosition'])
    displacement=df['displacement'].values*saccadeDirection
    displacement=np.round(displacement,decimals=2) #rounding off dispacement values
    displacement[displacement==-0.0]=0.0

    #use direction of saccades to find whether the response
    #was towards the direction of the saccade (forward response)
    response=np.zeros(len(displacement))
    response[np.logical_and(df['response']=='LeftResponse',saccadeDirection==-1)]=1
    response[np.logical_and(df['response']=='RightResponse',saccadeDirection==1)]=1

    #count number of trials and responses as a function of displacement
    uniqDisplacement=np.unique(displacement)
    nForward=np.zeros_like(uniqDisplacement,dtype=int)
    nTrials=np.zeros_like(uniqDisplacement,dtype=int)
    for i in range(0,len(uniqDisplacement)):
        nForward[i]=np.sum(response[displacement==uniqDisplacement[i]])
        nTrials[i]=np.sum(displacement==uniqDisplacement[i])
    return uniqDisplacement,nForward,nTrials

def writeAllPsychometry(whichExp='shape'):
    subIDs_C=[2,3,4,8,9,14,15,16,18,20,21]
    subIDs_S=[5,6,7,11,12,13,22,24,25]
    if(whichExp=='shape'):
        subIDs=subIDs_S
    elif(whichExp=='contrast'):
        subIDs=subIDs_C

    #iterate over all subjects and write out the response counts.
    for i in range(len(subIDs)):
        subID="Sub_%02d"%subIDs[i]
        for cond in ['Blank','Step','Change']:
            df=pd.DataFrame()
            uniqDisp,nFwd,nTrials=getPsychometricCurve(subID,whichTask=cond)
            df['displacement']=uniqDisp
            df['nForward']=nFwd
            df['nTrials']=nTrials
            if(cond=='Step'):
                cond='NoBlank'
            df.to_csv('./data_derived/%s/%s_%s.csv'%(whichExp,subID,cond),index=False)


writeAllPsychometry('shape')
writeAllPsychometry('contrast')