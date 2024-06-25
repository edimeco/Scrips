import os 
os.system()
import ROOT
import numpy
import pandas as pd

df = pd.read_csv("/home/dimeco/calibTools/padme-fw/UserAnalysis/config/periods_db.txt", sep=" ", header=None, usecols=[0,1,2,3,4,5,6,7])#, usecols=[0,1,2,3,4,5,6,7])

df.columns = ["period", "MagEn", "CurrEn", "cogx", "cogy","POT", "unknown", "RunID"]


ROOT.gROOT.LoadMacro("/data9Vd1/padme/dimeco/rootlogon.C")
DataFolder= "/data9Vd1/padme/dimeco/outMerged_period"
SignFolder= "/data9Vd1/padme/dimeco/outSig_periodo"
BkgFolder= "/data9Vd1/padme/dimeco/outBkg_periodo"
Me =  0.511 #MeV
OutFolder = "/data9Vd1/padme/dimeco/graphTom"
sqrtsval = []
def MakeGraphs(inFolder, OutName, histoName1, histoName2, fileName1, fileName2=0, sqrtsflag=0):
    gg = ROOT.TGraphErrors(len(df.period))
    gg.SetName(OutName)
    
    for i,per in enumerate(df.period):
        Sqrts = ROOT.TMath.Sqrt(2.*Me*Me + 2.*df.MagEn[i]*Me)
        sqrtsval.append(Sqrts)
        if sqrtsflag==0:
            fileIn = ROOT.TFile(f"{inFolder}/{fileName1}_{per:.1f}.root")
            histo1= fileIn.Get(f"ECalSel/{histoName1}").Clone()
            h2Val =0
            if fileName2==0:
                histo2 = fileIn.Get(f"ECalSel/{histoName2}").Clone()
                h2Val= histo2.Integral()
            else:
                histo2 = fileIn.Get(f"NPoTAnalysis/{histoName2}").Clone()
                h2Val= histo2.Integral()*3000

            ROOT.gROOT.cd()
            gg.SetPoint(i, Sqrts , histo1.Integral()/h2Val)
            if(OutFolder == "outMerged_bkg"):
                gg.SetPointError(i, 0., ROOT.TMath.Sqrt(histo1.Integral())/h2Val)
            elif(OutFolder== "outMerged_data"):
                gg.SetPointError(i, 0., ROOT.TMath.Sqrt(histo1.Integral())/h2Val) #Non chiaro

        
        else:
            gg.SetPoint(i, per,Sqrts)
            gg.SetPointError(i, 0., 0.)
    gg.GetXaxis().SetTitle("Period")
    gg.GetYaxis().SetTitle(f"{OutName}")

    gg.Draw("ap")
    input()
    gg.SaveAs(f"{OutFolder}/{OutName}.root")
    


MakeGraphs(DataFolder, "DataYield", "ECal_SC_E1plusE2", "NPoTLGCorr", "full")
MakeGraphs(BkgFolder, "BackgroundYield", "ECal_SC_E1plusE2", "NPoT", "full", "full_hsto")
# MakeGraphs(DataFolder, "Sqrts", "aaa", "aaa", "full", "full_hsto", 1)




# # Signal Fill a th1d with num e one with deno, teff
# # Bkg TGraph with error sqrt(entries)/NPoT
# # Data ?? 


# # def MakeSignGraph(inFolder, OutName, histoName1, histoName2, fileName1):
     
# #     hnum = ROOT.TH2D("num", "num",len(df.period), min(sqrtsval), max(sqrtsval))
# #     hdeno = ROOT.TH2D("deno", "deno",len(df.period), min(sqrtsval), max(sqrtsval), 150, 0,0.15)
# #     for i,per in enumerate(df.period):
        
# #             fileIn = ROOT.TFile(f"{inFolder}/{fileName1}_{per:.1f}.root")
# #             histo1= fileIn.Get(f"ECalSel/{histoName1}").Clone()
# #             histo2 = fileIn.Get(f"ECalSel/{histoName2}").Clone()
            
# #             ROOT.gROOT.cd()
            
# #             hnum.SetBinContent(i+1,histo1.Integral())
# #             hdeno.SetBinContent(i+1,histo2.Integral())

# #     eff = ROOT.TEfficiency(hnum, hdeno)
# #     eff.GetXaxis().SetTitle("Period")
# #     eff.GetYaxis().SetTitle(f"{OutName}")

# #     eff.Draw("ap")    
# #     input()
# #     eff.SaveAs(f"{OutFolder}/{OutName}.root")


#MakeGraphs(SignFolder, "SignalYield", "ECal_SC_E1plusE2_Bhabha", "NPoT", "full", "full_hsto")



def MakeSignGraph(inFolder, OutName, histoName1, histoName2, fileName1):
    hnum = ROOT.TH1D("num", "num",len(df.period), 0, len(df.period)-1)
    hdeno = ROOT.TH1D("deno", "deno",len(df.period), 0, len(df.period)-1)

    for i,per in enumerate(df.period):
        
            fileIn = ROOT.TFile(f"{inFolder}/{fileName1}_{per:.1f}.root")
            histo1= fileIn.Get(f"ECalSelMCTruth/{histoName1}").Clone()
            histo2 = fileIn.Get(f"ECalSel/{histoName2}").Clone()
            
            ROOT.gROOT.cd()
            
            hnum.SetBinContent(i+1,histo1.Integral())
            hdeno.SetBinContent(i+1,histo2.Integral())

    eff = ROOT.TEfficiency(hnum, hdeno)
    # eff.GetXaxis().SetTitle("Period")
    # eff.GetYaxis().SetTitle(f"{OutName}")

    eff.Draw("ap")    
    input()
    eff.SaveAs(f"{OutFolder}/{OutName}.root")


MakeGraphs(SignFolder, "SignalYield", "ECal_SC_E1plusE2_Bhabha", "EnSignalBhabha", "full")


# def MakeGraphsCR(inFolder, OutName, histoName1, histoName2, fileName1, fileName2=0, sqrtsflag=0):
#     gg = ROOT.TGraphErrors(len(df.period))
#     gg.SetName(OutName)
#     ff= ROOT.TF1("ff", "gaus", 0, 25)

#     for i,per in enumerate(df.period):
#         Sqrts = ROOT.TMath.Sqrt(2.*Me*Me + 2.*df.MagEn[i]*Me)
#         sqrtsval.append(Sqrts)
#         if sqrtsflag==0:
#             fileIn = ROOT.TFile(f"{inFolder}/{fileName1}_{per:.1f}.root")
#             histo1= fileIn.Get(f"ECalCalib22/{histoName1}").Clone()
            

#             ROOT.gROOT.cd()
#             histo1.Fit(ff, "REMQ")
#             gg.SetPoint(i, per , ff.GetParameter(1))
#             gg.SetPointError(i, 0., ff.GetParError(1))
            
        
#         else:
#             gg.SetPoint(i, per,Sqrts)
#             gg.SetPointError(i, 0., 0.)
#     gg.GetXaxis().SetTitle("Period")
#     gg.GetYaxis().SetTitle(f"{OutName}")

#     gg.Draw("ap")
#     input()
#     gg.SaveAs(f"{OutFolder}/{OutName}.root")

# CRFolder = "/data9Vd1/padme/dimeco/TagAndProbeOut/logs"

# MakeGraphsCR(CRFolder, "MPV", "CRMPV", "aaa", "full_out")
