#!/usr/bin/python

import os
import commands

nqueues = 16
# inputdbfile = "/home/spadaro/PADME/UserAnalysis/config/addo"
inputdbfile = "/home/dimeco/calibTools/padme-fw/UserAnalysis/config/run_level_offline_db_2022_witherr_patch_RIGHT_periods.txt"


runs=[]
# runs used for the scan
with open(inputdbfile, 'r') as f:
    i=0
    for line in f:
        fields = line.strip().split()
        if  (float(fields[6]) > 0 and int(fields[5])>200): #int(fields[0])>50498 and int(fields[0])<50501:
            runs.append((fields[0]))
            
        else:
            runs.append("0")
        
        print(runs[i])
        i+=1



print("Looking in dirin")
dirin = "/data9Vd1/padme/dimeco"
for runnr in os.listdir(dirin):
    print(runnr)
    
    if runnr in runs:  # it's a run for the scan
        print("found {}".format(runnr))
        fileout = os.path.join(dirin, runnr, "fullRun{}_encal.root".format(runnr))
        if os.path.exists(fileout):
            print("File {} already exists".format(fileout))
        command_merge = "hadd -f {}".format(fileout)
        dirlist_path = os.path.join(dirin, runnr, "lists")
        for fileout in os.listdir(dirlist_path):
            if fileout.startswith("outlist") and fileout.endswith(".root"):
                command_merge += " {}".format(os.path.join(dirlist_path, fileout))
        command_merge += "\n"
        os.system(command_merge)
