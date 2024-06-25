import os
import ROOT

def filltgraph(directory, tgraph, th1, datatype):
    # Create a dictionary to store the count of values
    iP=0
    # Loop through all txt files in the directory
    for filename in os.listdir(directory):
        if filename.startswith(f"IntegratedEfficiency_{datatype}_full_") and filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                # Read each line in the file
                for line in file:
                    # Split the line by whitespace and take the first value
                    period = line.split()[0]
                    energy = line.split()[1]
                    cogx = line.split()[2]
                    cogy = line.split()[3]
                    num = line.split()[4]
                    errnum = line.split()[5]
                    den = line.split()[6]
                    errden = line.split()[7]
                    eff = line.split()[8]
                    erreff = line.split()[9]
                    th1.Fill(float(eff))
                    tgraph.SetPoint(iP, float(period), float(eff))
                    tgraph.SetPointError(iP, 0., float(erreff))
                    iP+=1

    return 

def filltgraphCOG(directory, tgraph, th1, dir):
    # Create a dictionary to store the count of values
    iP=0
    # Loop through all txt files in the directory
    for filename in os.listdir(directory):
        if filename.startswith("IntegratedEfficiency_full") and filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                # Read each line in the file
                for line in file:
                    print(line)
                    # Split the line by whitespace and take the first value
                    period = line.split()[0]
                    energy = line.split()[1]
                    cogx = line.split()[2]
                    cogy = line.split()[3]
                    num = line.split()[4]
                    errnum = line.split()[5]
                    den = line.split()[6]
                    errden = line.split()[7]
                    eff = line.split()[8]
                    erreff = line.split()[9]
                    th1.Fill(float(eff))
                    if dir == "x":
                        tgraph.SetPoint(iP, float(cogx), float(eff))
                    else:
                        tgraph.SetPoint(iP, float(cogy), float(eff))

                    tgraph.SetPointError(iP, 0., float(erreff))
                    iP+=1

                

    return 

def main():
    # Set the directory containing the txt files
    ROOT.gROOT.LoadMacro("/home/dimeco/rootlogon.C")
    directoryDATA = "/data9Vd1/padme/dimeco/TagAndProbeOut/DATAout"
    # Process txt files to get the count of values
    tgraphDATA = ROOT.TGraphErrors(52)
    effdata = ROOT.TH1D("effdata", "effdata", 30, 0.7,1.)
    filltgraph(directoryDATA, tgraphDATA, effdata, "DATA")
    tgraphDATA.GetXaxis().SetTitle("Beam Energy [MeV]")
    tgraphDATA.GetYaxis().SetTitle("TP efficiency")
    effdata.GetXaxis().SetTitle("DATA TP efficiency")

    # Create a TH2D histogram from the value counts
    
    # Draw the histogram
    # canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    # tgraphDATA.Draw("ap")
    # input()
    # effdata.Draw("")
    # input()


    directoryDATA = "/data9Vd1/padme/dimeco/TagAndProbeOut/DATAout"
    # Process txt files to get the count of values
    tgraphDATA = ROOT.TGraphErrors(52)
    effdata = ROOT.TH1D("effdata", "effdata", 30, 0.7,1.)
    filltgraph(directoryDATA, tgraphDATA, effdata, "DATA")
    tgraphDATA.GetXaxis().SetTitle("Beam Energy [MeV]")
    tgraphDATA.GetYaxis().SetTitle("TP efficiency")
    effdata.GetXaxis().SetTitle("DATA TP efficiency")


    dir = "x"
    tgraphDATACogX = ROOT.TGraphErrors(52)
    tgraphDATACogX.GetXaxis().SetTitle("X_{COG} [mm]")
    tgraphDATACogX.GetYaxis().SetTitle("TP efficiency")
   

    filltgraphCOG(directoryDATA, tgraphDATACogX, effdata, dir)

    dir = "y"
    tgraphDATACogY = ROOT.TGraphErrors(52)
    

    filltgraphCOG(directoryDATA, tgraphDATACogY, effdata, dir)

    tgraphDATACogY.GetXaxis().SetTitle("Y_{COG} [mm]")
    tgraphDATACogY.GetYaxis().SetTitle("TP efficiency")
   
    # directoryMC = "/data9Vd1/padme/dimeco/TagAndProbeOut/MCout"
    # # Process txt files to get the count of values
    tgraphMC = ROOT.TGraphErrors(52)
    effMC = ROOT.TH1D("effMC", "effMC", 30, 0.7,1.)
    filltgraph(directoryDATA, tgraphMC, effMC, "MC")
    tgraphMC.GetXaxis().SetTitle("Beam Energy [MeV]")
    tgraphMC.GetYaxis().SetTitle("TP efficiency")
    effMC.GetXaxis().SetTitle("MC TP efficiency")
    # tgraphMC.SetMarkerColor(ROOT.kRed)
    # tgraphMC.SetLineColor(ROOT.kRed)

    # Create a TH2D histogram from the value counts
    
    canvas1 = ROOT.TCanvas("canvas1", "canvas1", 800, 600)
    tgraphDATACogX.SetMarkerColor(ROOT.kRed)
    tgraphDATACogX.SetLineColor(ROOT.kRed)
    tgraphDATACogX.Draw("ap")
    input()

    tgraphDATACogY.SetMarkerColor(ROOT.kBlue)
    tgraphDATACogY.SetMarkerColor(ROOT.kBlue)
    tgraphDATACogY.Draw("ap")
    input()

    # Draw the histogram
    canvas = ROOT.TCanvas("canvas", "canvas", 800, 600)
    tgraphDATA.Draw("ap")
    # tgraphMC.Draw("samep")
    input()
    
    # effMC.Draw("")
    # input()
    #canvas.SaveAs("tgraphDATA.C")

if __name__ == "__main__":
    #ROOT.gROOT.SetBatch(ROOT.kTRUE) # To avoid opening a window for plotting
    main()
