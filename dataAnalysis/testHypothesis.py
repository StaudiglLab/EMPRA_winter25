import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import ttest_1samp


def readParams(whichExp,whichParam='bias'):
    if(whichParam=='bias'):
        col=1
    else:
        col=2
    paramNoBlank=np.loadtxt("./outfiles/fitParams_%s_NoBlank.csv"%whichExp,usecols=[col],delimiter=',')
    paramBlank=np.loadtxt("./outfiles/fitParams_%s_Blank.csv"%whichExp,usecols=[col],delimiter=',')
    paramChange=np.loadtxt("./outfiles/fitParams_%s_Change.csv"%whichExp,usecols=[col],delimiter=',')
    if(whichParam=='bias'):
        return paramNoBlank,paramBlank,paramChange
    else:
        factor=scipy.stats.norm.ppf(0.75)
        return factor*paramNoBlank,factor*paramBlank,factor*paramChange

def plotComparisions(paramsCond1,paramsCond2,labels,ylabel):
    ttestres=ttest_1samp(paramsCond1-paramsCond2,0)
    print("Result of paired t test")
    print("t-value= %.2f; p-value= %.5f; dof= %d"%(ttestres.statistic,ttestres.pvalue,len(paramsCond1)-1))
    plt.figure(figsize=(4,4))
    bxplot=plt.boxplot([paramsCond1,paramsCond2],widths=[0.5,0.5],labels=labels,
                       showfliers=False,patch_artist=True,meanline=True,
                       medianprops=dict(color='black',linewidth=2.5))
    colors=['C0','C1']
    for patch, color in zip(bxplot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)
    for i in range(len(paramsCond1)):
        plt.plot(1+np.arange(2)+np.random.randn(2)*0.02,[paramsCond1[i],paramsCond2[i]],c='gray',lw=0.5,marker='o',ms=3,zorder=-999)
        if(ttestres.pvalue<0.05):
            plt.plot([1,2],np.zeros(2)+1.15*np.max([paramsCond1,paramsCond2]),lw=0.5,marker='|',c='black')

            plt.scatter(1.5,1.2*np.max([paramsCond1,paramsCond2]),marker='*',s=100,c='black')
    plt.ylabel(ylabel)

#difference in perceptual performance between no blanking and blanking conditions
#done in pooled data
def testHypothesis1(whichParam='jnd'):
    paramNoBlank_C,paramBlank_C,paramChange_C=readParams(whichExp='contrast',whichParam=whichParam)
    paramNoBlank_S,paramBlank_S,paramChange_S=readParams(whichExp='shape',whichParam=whichParam)
    #pooling data together
    paramNoBlank=np.append(paramNoBlank_S,paramNoBlank_C)
    paramBlank=np.append(paramBlank_S,paramBlank_C)

    if(whichParam=='jnd'):
        ylabel='JND (degrees)'
    elif(whichParam=='bias'):
        ylabel='bias (degrees)'
    print("-------------")
    print("Comparing %s of no blank and blank conditions"%whichParam)
    print("-------------")

    print("Mean of %s for No Blank:%.2f"%(whichParam,np.mean(paramNoBlank)))
    print("Standard Deviation of %s for No Blank:%.2f"%(whichParam,np.std(paramNoBlank)))

    print("Mean of %s for Blank:%.2f"%(whichParam,np.mean(paramBlank)))
    print("Standard Deviation of %s for Blank:%.2f"%(whichParam,np.std(paramBlank)))

    plotComparisions(paramNoBlank,paramBlank,labels=['No Blank','Blank'],ylabel=ylabel)
    print("-------------")

    plt.savefig("figures/%s_NoBlank_Blank.png"%whichParam,bbox_inches='tight',dpi=300.0)

#difference in perceptual performance between shape/contrast change and either
#      (i) blanking condition (whichComparision='Blank')
# or, (ii) no blanking condition (whichComparision='NoBlank')
# done seperately for each cohort
def testHypothesis2And3(whichExp,whichParam='jnd',whichComparision='Blank'):
    paramNoBlank,paramBlank,paramChange=readParams(whichExp=whichExp,whichParam=whichParam)
    if(whichComparision=='Blank'):
        param1=paramBlank
    else:
        param1=paramNoBlank
    if(whichParam=='jnd'):
        ylabel='JND (degrees)'
    elif(whichParam=='bias'):
        ylabel='bias (degrees)'
    print("-------------")
    print("Comparing %s of %s and %s-change conditions"%(whichParam,whichComparision,whichExp))
    print("-------------")

    print("Mean of %s for %s condition:%.2f"%(whichParam,whichComparision,np.mean(paramNoBlank)))
    print("Standard Deviation of %s for %s condition:%.2f"%(whichParam,whichComparision,np.std(paramNoBlank)))

    print("Mean of %s for %s-change condition:%.2f"%(whichParam,whichExp,np.mean(paramBlank)))
    print("Standard Deviation of %s for %s-change condition:%.2f"%(whichParam,whichExp,np.std(paramBlank)))

    plotComparisions(param1,paramChange,labels=[whichComparision,'%s-change'%whichExp],ylabel=ylabel)
    print("-------------")

    plt.savefig("figures/%s_%s_%s.png"%(whichParam,whichExp,whichComparision),bbox_inches='tight',dpi=300.0)




