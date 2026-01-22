## Introduction

This folder of the repository contains the data (except the raw eyetracker data) and the analysis codes for experiment conducted as part of EMPRA 2025 (winter semester).

## Data exclusion

- We excluded trials that where the average horizontal eye velocity over -10 ms to +10 ms around the stimulus onset was less than 150 deg/sec. This was done to ensure that there was indeed a horizontal saccade during the stimulus update. 
- After the above trial exclusion criteria, three subjects (Sub_01, Sub_19, and Sub_23) had total number of trials that were less than 80 in each of the three conditions (see data_derived/trialCountSummary.csv). These participants thus did not meet our preregistered criterion for inclusion and were thus excluded from all further analysis.
- In additional the data acquisition for one participant (Sub_10) could not be completed due to technical issues.
- Overall, four participants were excluded from the data analysis. The final cohort thus has a size of N=20, with N=9 for the experiment with shape-change and N=11 for the experiment with contrast-change.
## Description of files
- Each directory within the *data* directory contains the raw data files for a single subject of the experiment. The raw eyetracker data is not uploaded here due to size constraints.
- The *data_derived* directory contains files that were generated using the raw data.
    -  *data_derived/contrast* contains files for the contrast group.
    - *data_derived/shape* contains files for the shape group.

- Each of the shape and contrast directories inside data_derived contains .csv files, one for each subject and conditions.

    - Each .csv file contains three columns: (1) Displacement (2) The number of forward responses for that displacement (3) The total number of trials for that displacement. 
    - Dividing the second column by the third would give you the the ratio of forward responses. This is what is typically plotted as a function of displacement. (e.g. Figure 2 of Tas & Parker 2023)
    - These files were generated from the raw data files using the code *getPsychometry.py*

## Generating figures and statistic for the report

- run *generateAll.py*
    - if you're part of the contrast group run with *whichExp='contrast'*
    - if you're part of the shape group run it with *whichExp='shape'*



