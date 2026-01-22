import numpy as np
import matplotlib.pyplot as plt
import mne
import pandas as pd
def getSelectedTrials(directory,subID,
                      triggerName=['TargetDisplacement','TargetRemoval'],
                      screenDistance=65.0,
                      screenWidth=53.36,
                      twindow=10e-3,
                      velmin=150):
    
    dfTriggers=pd.read_csv("./data/%s_TSD/task_TSD_%s_Triggers.csv"%(subID,subID))
    dfTriggers=dfTriggers[np.logical_or(dfTriggers['triggerName'].values==triggerName[0],dfTriggers['triggerName'].values==triggerName[1])]

    fnameEyelink=directory+"/%s_TSD/task_TSD_%s_eyelink.asc"%(subID,subID)
    
    raw=mne.io.read_raw_eyelink(fnameEyelink)
        #raw.plot(block=True)
    events,event_dict=mne.events_from_annotations(raw)
    #
    
    epochs=mne.Epochs(raw,events=events,event_id=[event_dict[np.str_(triggerName[0])],event_dict[np.str_(triggerName[1])]],tmin=-0.05,tmax=0.05,reject_by_annotation=False,baseline=None)
    epochs=epochs[dfTriggers['blockID'].values!='pract']
    data=epochs.get_data(["xpos_left","xpos_right"])
    times=epochs.times

    eyePos=np.degrees(np.arctan(screenWidth*(np.mean(data-1920/2.,axis=1)/1920.0)/screenDistance))
    #eyePos-=np.mean(eyePos[:,np.logical_and(times>-0.1,times<-0.05)],axis=1,keepdims=True)
    vel=np.diff(eyePos,axis=1)/(times[1]-times[0])
    for i in range(0,len(eyePos)):
        vel[i]=np.convolve(vel[i],np.ones(10)/10.,mode='same')
    times=(times[1:]+times[:-1])/2.
    meanVel=np.mean(np.abs(vel[:,np.logical_and(times>=-twindow,times<=twindow)]),axis=1)
    selmask=meanVel>velmin
    print(np.sum(selmask),len(selmask))
    plt.plot(1e3*times,vel[selmask].T)
    plt.plot(1e3*times,vel[np.logical_not(selmask)].T,c='gray')
    plt.xlabel("Time (milliseconds)")
    plt.ylabel("Velocity (deg/sec)")
    plt.ylim((-500,500))
    plt.savefig("./figures_raw/trials/%s.png"%subID,dpi=300)
    return selmask
def getExpType(subID):
    f=open("./data/Sub_%s_s1_TSD/task_TSD_Sub_%s_s1_mainLog.txt"%(subID,subID))
    lines=f.readlines()
    type=lines[5][-3]
    f.close()
    return type
def getTrialNumberSummary(subIDs,trialTypes=['Blank','Step','Change']):
    dfTrials=pd.DataFrame()
    for iSub in range(len(subIDs)):
        df=pd.read_csv("./data/Sub_%s_s1_TSD/task_TSD_Sub_%s_s1_trialSequence.csv"%(subIDs[iSub],subIDs[iSub]))
        df=df[df['response'].values!='NoSaccadeMade']
        selmask= np.loadtxt("outfiles/trialSelection/Sub_%s.txt"%subIDs[iSub])>0.5
        print(subIDs[iSub])
        print(len(selmask),len(df))
        dfTrials.loc[iSub,'subID']=subIDs[iSub]   
        dfTrials.loc[iSub,'expType']=getExpType(subIDs[iSub])   
        for trialType in trialTypes:
            dfTrials.loc[iSub,'nTrials_%s'%trialType]=np.sum(np.logical_and(df['trialType'].values==trialType,selmask))  
    print(dfTrials)
    dfTrials.to_csv("outfiles/trialCountSummary.csv")
subIDs=['01','02','03','04','05','06','07','08','09','11','12','13','14','15','16','18','19','20','21','22','23','24','25']
#for iSub in range(len(subIDs)):
#    selmask=getSelectedTrials("./data","Sub_%s_s1"%subIDs[iSub])
#    np.savetxt("outfiles/trialSelection/Sub_%s.txt"%subIDs[iSub],selmask,fmt='%d')
getTrialNumberSummary(subIDs)
#getExpType(subIDs[1])