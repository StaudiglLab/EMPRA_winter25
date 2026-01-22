from plotPsychometry import plotAll
from testHypothesis import testHypothesis1,testHypothesis2And3

#whichExp='contrast'
whichExp='shape'

plotAll(whichExp=whichExp)
testHypothesis1()
testHypothesis2And3(whichExp=whichExp,whichComparision='No Blank')
testHypothesis2And3(whichExp=whichExp,whichComparision='Blank')

