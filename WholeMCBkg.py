import os
import numpy
import commands
#import pandas as pd

# df = pd.read_csv("config/run_level_offline_db_2022.txt", sep=" ", header=None)
# df.columns = ["RunID", "runStartTime", "runStopTime", "DHSTB01Energy", "DHSTB02Energy","nFiles", "runPOT", "bunchLength", "beamStart", "tgx", "tgy", "cogx", "cogy", "corrQuadTL", "corrQuadTR", "corrQuadBR", "corrQuadBL"]


# os.system("make -j8")

# for i in df[RunID]

#!/usr/bin/env python

#import os
import subprocess
import time

nqueues = 20
inputdbfile = "/home/dimeco/calibTools/padme-fw/UserAnalysis/config/periods_db.txt"
#runpath = "/data9Vd1/padme/leonardi/padme/daq/2022/reco"

# runpath = "root://atlasse.lnf.infn.it//dpm/lnf.infn.it/home/vo.padme.org/daq/2022/recodata/repro20240219"
runpath = "root://atlasse.lnf.infn.it//dpm/lnf.infn.it/home/vo.padme.org/mc/prodrun3_20240430/"
# root://atlasse.lnf.infn.it//dpm/lnf.infn.it/home/vo.padme.org/mc/prodrun3_20240430/bkg_20240530
outdir = "/data9Vd1/padme/dimeco/outBkg_periodo_morestat"
os.system("mkdir {}".format(outdir))
os.system("mkdir {}/logs".format(outdir))
# FullRunName = (commands.getstatusoutput("gfal-ls "+Address+"| grep "+FullRunNumber))[1]
# DataToRead = Address+FullRunName

# Read run information from the input database file
runs=[]
runnum= []

with open(inputdbfile, 'r') as f:
    i=0
    for line in f:
        fields = line.strip().split()
        runs.append(str(fields[0]))
        runnum.append(int(fields[7]))

        i+=1

# List files in the run directory
mclist = commands.getstatusoutput("gfal-ls "+runpath+ " | grep bkg_20240430")[1]
mclist=mclist.split('\n')

#mclist = subprocess.Popen(['gfal-ls', runpath], stdout=subprocess.PIPE)
print(mclist)
for ip,periodo in enumerate(mclist):
    print(periodo)
    if ip>10: break
    #if periodo.startswith('bkg_20240514_{}'.format(runs[ip])):

    lsCommand = "gfal-ls "+runpath+periodo+"/rec/repro20240522 | grep bkg_20240430"
    RootFileList = commands.getstatusoutput(lsCommand)[1]

    rootFileList=RootFileList.split('\n')

    with open("/data9Vd1/padme/dimeco/{}.list".format(periodo),"w") as filelist:
        for RootFile in rootFileList:
            filelist.write(runpath+periodo+"/rec/repro20240522/"+RootFile+"\n")
    filelist.close()   
    #se ps -fu PadmeAnalysis < 22 -> processo
    while True:
            numberOfRunningJobs = int(subprocess.check_output(["ps", "-fu", "dimeco"]).count("PadmeAnalysis"))  # Count PadmeAnalysis processes
            if numberOfRunningJobs < 20:
                break
            else:
                print("Presently {} jobs are running, wait 1 min".format(numberOfRunningJobs))
                time.sleep(30)

    print("nohup ./PadmeAnalysis -l /data9Vd1/padme/dimeco/{}.list -r {} -o {}/full_{:.1f}.root > {}/logs/log{}.log &\n".format(periodo, runnum[ip],outdir,float(runs[ip]), outdir, runs[ip]))
    os.system("nohup ./PadmeAnalysis -l /data9Vd1/padme/dimeco/{}.list -r {} -o {}/full_{:.1f}.root > {}/logs/log{}.log &\n".format(periodo, runnum[ip],outdir,float(runs[ip]), outdir, runs[ip]))
        