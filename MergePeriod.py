import os
import numpy as np
import sys
import subprocess
import pandas as pd
import ROOT
import time


df_all = pd.read_csv("/home/dimeco/calibTools/padme-fw/UserAnalysis/config/run_level_offline_db_2022_witherr_patch_RIGHT_periods_lgcorr.txt", sep="\t", header=None)
df_all.columns = ["RunID", "runStartTime", "runStopTime", "DHSTB01Energy", "DHSTB02Energy","nFiles", "runPOT", "bunchLength", "beamStart", 
              "tgx", "tgy", "cogx", "cogy","calibEnergyFactor", "calibTimeEnergyFactor", "tempQuadTL", "corrQuadTL","tempQuadTR", "corrQuadTR", "tempQuadBL", "corrQuadBL","tempQuadBR","corrQuadBR", "errCOGX", "errCOGY", "newTargX", "newTargY", "errnewTargX", "errnewTargY", 
              "sigmaDPhi", "errsigmaDPhi", "sigmaDTheta", "errsigmaDTheta", "sigmaCOGX", "errsigmaCOGX", "sigmaCOGY", "errsigmaCOGY",
              "E1E2", "errE1E2" , "dt", "errdt", "sigmaE1E2", "errsigmaE1E2", "sigmadt", "errsigmadt", "period", "PoTcorr"]





DIR="/data9Vd1/padme/dimeco/"
outMerged = DIR+"outMerged_period_lgcorr"
os.system(f"mkdir {outMerged}")

df_cut1 = df_all[df_all.runPOT >0]
df = df_cut1[df_cut1.nFiles>200]


#DA CAMBIARE CON IL PERIODO

for i,per_all in enumerate(df.period):
  df_period = df[df.period == per_all]
  per = (df_period.period.mean())
  run = df_period.RunID.iloc[0]
  commandmerge = f"hadd -f {outMerged}/full_{per}.root "
  for irun in df_period.RunID:
      commandmerge += f" {DIR}{irun}/fullRun{irun}_encal.root"
        
  if df.RunID.iloc[i] == run:
     os.system(commandmerge)
     time.sleep(2)
