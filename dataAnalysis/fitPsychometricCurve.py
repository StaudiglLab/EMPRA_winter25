from scipy.stats import norm
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


def plotPsychometricCurve(subID,whichExp,whichCondition):
    displacement,nFwd,nTrials=np.loadtxt('./data_derived/%s/Sub_%02d_%s.csv'%(whichExp,subID,whichCondition),delimiter=',',unpack=True,skiprows=1)
    fractionFwd=nFwd/nTrials.astype("float")
    #using scipy function curve fit to fit a cumulative gaussian distribution function (https://en.wikipedia.org/wiki/Normal_distribution)
    #to the measurements of the psychometric curve 
    popt,pcov=curve_fit(norm.cdf,displacement,fractionFwd,p0=[0,1]) 
   

    #plotting individual curves for vizualization
    plt.figure(figsize=(4,4))
    plt.plot(displacement,100*nFwd/nTrials,marker='o',label='data points')
    plt.plot(np.arange(-1.5,1.5,0.001),100*norm.cdf(np.arange(-1.5,1.5,0.001),popt[0],popt[1]),label='sigmoidal fit')
    plt.axhline(50,c='gray',ls='--')
    plt.axvline(0.0,c='gray',ls='--')

    plt.plot([-2.0,popt[0]],[50,50],c='black')
    plt.plot([popt[0],popt[0]],[50,-5],c='black')
    factor=norm.ppf(0.75)*popt[1]
    plt.plot([-2.0,popt[0]+factor],[75,75],c='black')
    plt.plot([popt[0]+factor,popt[0]+factor],[75,-5],c='black')
    plt.xlim((-1.65,1.65))
    plt.ylim((-5,105))
    plt.xlabel("Displacement (degrees)")
    plt.ylabel("Percent Forward Response")
    plt.legend()
    plt.savefig("figures/indvFits/Sub%02d_%s_%s.png"%(int(subID),whichExp,whichCondition),bbox_inches='tight',dpi=300.0)

    #np.diag(np.sqrt(pcov)) is the standard error on the fit parameters
    return popt,np.diag(np.sqrt(pcov))
def getFitParams(whichExp,whichCondition):

    if(whichExp=='contrast'):
        subIDs=[2,3,4,8,9,14,15,16,18,20,21]
    else:
        subIDs=[5,6,7,11,12,13,22,24,25]
    
    fitParams=np.zeros((len(subIDs),2))
    fitParamsEr=np.zeros_like(fitParams)

    #save fit parameters to file
    for iSub in range(len(subIDs)):
        fitParams[iSub],fitParamsEr[iSub]=plotPsychometricCurve(subIDs[iSub],whichExp,whichCondition)
    np.savetxt("./outfiles/fitParams_%s_%s.csv"%(whichExp,whichCondition),np.column_stack((subIDs,fitParams,fitParamsEr)),fmt='%02d,%.5e,%.5e,%.5e,%.5e',delimiter=',',header='subID,loc,scale,loc_er,scale_er')

for condition in ['NoBlank','Blank','Change']:
    getFitParams('contrast',condition)  
    getFitParams('shape',condition)  