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
inputdbfile = "/home/dimeco/calibTools/padme-fw/UserAnalysis/config/run_level_offline_db_2022_witherr_patch_RIGHT_periods_lgcorr.txt"
#runpath = "/data9Vd1/padme/leonardi/padme/daq/2022/reco"

runpath = "root://atlasse.lnf.infn.it//dpm/lnf.infn.it/home/vo.padme.org/daq/2022/recodata/repro20240516"


# FullRunName = (commands.getstatusoutput("gfal-ls "+Address+"| grep "+FullRunNumber))[1]
# DataToRead = Address+FullRunName

# Read run information from the input database file
runs=[]

with open(inputdbfile, 'r') as f:
    i=0
    for line in f:
        fields = line.strip().split()
        if  (float(fields[6]) > 0 and int(fields[5])>200) and int(fields[0])<50325: #int(fields[0])>50498 and int(fields[0])<50501:#(
            runs.append(int(fields[0]))
            print(line)
        else:
            runs.append(0)
        
        #print(runs[i])
        i+=1

# List files in the run directory
runlist = subprocess.Popen(['gfal-ls', runpath], stdout=subprocess.PIPE)

for line in runlist.stdout:
    line = line.strip()
    
    if line.startswith('run_') and line.endswith('20240516'):
        rundir = line
        
        runnr = int(rundir.split('_')[1])
        
        if runnr in runs:

            print(runnr)
            outdir = "/data9Vd1/padme/dimeco/{}".format(runnr)
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            if not os.path.exists("{}/lists".format(outdir)):
                os.makedirs("{}/lists".format(outdir))

            filelist = subprocess.Popen(['gfal-ls', '{}/{}/'.format(runpath, rundir)], stdout=subprocess.PIPE)
            #print(filelist.stdout)
            outscript = open("{}/esegui.sh".format(outdir), 'w')

            numberOfFiles = 0
            listid = 0
            outlist = None

            for filename in filelist.stdout:
                
                filename = filename.strip()
                if filename.endswith(".00"):  continue
                print(filename)
                if numberOfFiles % nqueues == 0:
                    if outlist:
                        outlist.close()
                    outlist = open("{}/lists/outlist{}.list".format(outdir, listid), 'w')
                    outscript.write("cd /home/dimeco/calibTools/padme-fw/UserAnalysis\n")
                    outscript.write("nohup ./PadmeAnalysis -l {}/lists/outlist{}.list -r {} -o {}/lists/outlist{}.root > {}/lists/log{}.log &\n".format(outdir, listid,runnr, outdir, listid, outdir, listid))
                    
                    listid += 1
                outlist.write("{}/{}/{}\n".format(runpath, rundir, filename))
                #print("{}/{}/{}\n".format(runpath, rundir, filename))
                numberOfFiles += 1

            outlist.close()
            # if numberOfFiles % nqueues != 0:
            #     pass  # You can add some handling if the number of files is not divisible by nqueues

            print("Run {} has {} files divided into {} lists".format(runnr, numberOfFiles, listid))
            #outscript.write("exit 1\n")
            outscript.close()
            os.chmod("{}/esegui.sh".format(outdir), 0777)

            command = "source {}/esegui.sh".format(outdir)

            #print("ho scritto {}".format(command))

        
            while True:
                numberOfRunningJobs = int(subprocess.check_output(["ps", "-fu", "dimeco"]).count("PadmeAnalysis"))  # Count PadmeAnalysis processes
                if numberOfRunningJobs < 10:
                    break
                else:
                    print("Presently {} jobs are running, wait 1 min".format(numberOfRunningJobs))
                    time.sleep(60)

            
            
            subprocess.call(command, shell=True)
            time.sleep(2)
