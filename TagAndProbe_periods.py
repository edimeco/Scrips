import os
import numpy as np
import sys
import subprocess
import pandas as pd
import ROOT
import time

df = pd.read_csv("/home/dimeco/calibTools/padme-fw/UserAnalysis/config/periods_db.txt", sep=" ", header=None, usecols=[0,1,2,3,4,5,6,7])#, usecols=[0,1,2,3,4,5,6,7])

df.columns = ["period", "MagEn", "CurrEn", "cogx", "cogy","POT", "unknown", "RunID"]

isMC = False

DIR="/data9Vd1/padme/dimeco/"

if isMC is True:
  inMerged =  DIR+"outBkg_periodo"
else: 
  inMerged = DIR+"outMerged_period"

outMerged = "/data9Vd1/padme/dimeco/TagAndProbeOut"

os.system(f"mkdir {outMerged}")


for i,per in enumerate(df.period):
  run = df.RunID[i]
  if isMC is False:
    command = f"nohup ./PadmeAnalysis -l {DIR}{run}/lists/outlist0.list -r {run} -m {inMerged}/full_{per:.1f}.root -o {outMerged}/logs/full_out_{per:.1f}.root >  {outMerged}/logs/DATAlogs/log_{per:.1f}.log &"
  else:
    if(i<10):
      command = f"nohup ./PadmeAnalysis -l {inMerged}/lists/bkg_20240514_0{per}_{df.MagEn[i]:.2f}_{df.CurrEn[i]:.2f}.list -r {run} -m {inMerged}/full_{per:.1f}.root -o {outMerged}/logs/full_out_{per:.1f}.root >  {outMerged}/logs/DATAlogs/log_{per:.1f}.log &" 
    else:
      command = f"nohup ./PadmeAnalysis -l {inMerged}/lists/bkg_20240514_{per}_{df.MagEn[i]:.2f}_{df.CurrEn[i]:.2f}.list -r {run} -m {inMerged}/full_{per:.1f}.root -o {outMerged}/logs/full_out_{per:.1f}.root >  {outMerged}/logs/MClogs/log_{per:.1f}.log &" 

  if df.RunID.iloc[i] == run:
     print(command)
 

