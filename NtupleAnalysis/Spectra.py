import ROOT
import numpy

import sys
sys.path.append('/mnt/c/Users/marratia/Linux/PionHadronCorr/CompareHistograms')
#from AtlasCommonUtils import *
#from Legend import Legend
#from astroML.plotting import hist
from ROOT import TLatex
#SetAtlasStyle()

#fMC = ROOT.TFile("fout_16c3b.root")
fMC = ROOT.TFile("fout_MC.root")
#fMC = ROOT.TFile("fout_MCGamma.root")
fMC.Print()
eff_NN = fMC.Get("eff_NN_bin")
eff_NN_other = fMC.Get("eff_NN")
eff_NN.Print()
eff_Lambda = fMC.Get("eff_Lambda")
eff_Lambda.Print()
purity_NN = fMC.Get("Purity_NN")
purity_Lambda = fMC.Get("Purity_Lambda")

closure_NN = fMC.Get("ClosureTest_NN")
closure_Lambda = fMC.Get("ClosureTest_Lambda")

#fdata = ROOT.TFile("fout_195783.root")
fdata = ROOT.TFile("fout_DATA.root")
DeepPionSpectra = fdata.Get("DeepPionSpectra")
MergedPionLambdaSpectra = fdata.Get("MergedPionLambdaSpectra")
MergedPionLambdaSpectra.Print()


c = ROOT.TCanvas("c","c")

#l = Legend("")
purity_NN.SetLineColorAlpha(2,0.85)
purity_Lambda.SetLineColorAlpha(4,0.85)

purity_NN.SetMarkerColorAlpha(2,0.85)
purity_Lambda.SetMarkerColorAlpha(4,0.85)

#l.Add(purity_NN, "NN>0.85", "L")
#l.Add(purity_Lambda,"#lambda_{0}^{2} > 0.27", "L")
purity_NN.SetTitle("; p_{T} cluster [GeV]; purity");
purity_NN.GetXaxis().SetRangeUser(8.0,25.0);
purity_NN.SetMaximum(1.0)
purity_NN.SetMinimum(0.0)
purity_NN.Draw()
purity_Lambda.Draw("same")
purity_NN.SetLineColorAlpha(2,0.85)
purity_Lambda.SetLineColorAlpha(4,0.85)
#l.Draw(.2,.35)
c.SaveAs("purity.pdf")

c.Clear()
closure_NN.SetTitle("; p_{T} cluster [GeV]; closure test")
closure_NN.SetLineColorAlpha(2,0.65)
closure_Lambda.SetLineColorAlpha(4,0.65)
closure_NN.SetMarkerStyle(20)
closure_NN.SetLineWidth(2)
closure_Lambda.SetMarkerStyle(20)
closure_Lambda.SetLineWidth(2)
closure_NN.SetMarkerColorAlpha(2, 0.85)
closure_Lambda.SetMarkerColorAlpha(4, 0.85)
closure_NN.Draw()
closure_Lambda.Draw("same")
#l.Draw(.2,.35)
closure_NN.GetXaxis().SetRangeUser(8.0,25.0);
c.SaveAs("closureTest.pdf")

c.Clear()

eff_NN.SetLineColorAlpha(2,0.85)
eff_Lambda.SetLineColorAlpha(4,0.85)

eff_NN.SetMarkerColorAlpha(2,0.85)
eff_Lambda.SetMarkerColorAlpha(4,0.85)

eff_NN.SetTitle("; p_{T} cluster [GeV]; efficiency");
eff_NN.SetMaximum(1.3)
eff_NN.SetMinimum(0.0)
eff_NN.Draw("AP")
eff_Lambda.Draw("same")
#l.Draw(.2,.95)
eff_NN.GetXaxis().SetRangeUser(8.0,25.0);
c.SaveAs("efficiency.pdf")


c.Clear()

DeepPionSpectra.SetLineColorAlpha(2,0.85)
MergedPionLambdaSpectra.SetLineColorAlpha(4,0.85)
DeepPionSpectra.SetMarkerColorAlpha(2,0.85)
MergedPionLambdaSpectra.SetMarkerColorAlpha(4,0.85)

DeepPionSpectra.Draw()
MergedPionLambdaSpectra.Draw("same")
#l.Draw(.2,.95)
ROOT.gPad.SetLogy()
c.SaveAs("spectra_beforecorrection.pdf")


DeepPionSpectra.Divide(eff_NN_other)
DeepPionSpectra.Divide(purity_NN)
MergedPionLambdaSpectra.Divide(eff_Lambda)
MergedPionLambdaSpectra.Divide(purity_Lambda)

DeepPionSpectra.Draw()
DeepPionSpectra.GetXaxis().SetRangeUser(8.0,25.0);
MergedPionLambdaSpectra.Draw("same")
#l.Draw(.2,.35)
ROOT.gPad.SetLogy()
c.SaveAs("spectra_aftercorrection.pdf")


c.Clear()
DeepPionSpectra.Divide(MergedPionLambdaSpectra)
DeepPionSpectra.SetTitle("; cluster p_{T} GeV; ratio")
DeepPionSpectra.SetMarkerColor(1)
DeepPionSpectra.SetLineColor(1)
DeepPionSpectra.Draw()
DeepPionSpectra.GetXaxis().SetRangeUser(8.0,25.0);
ROOT.gPad.SetLogy(0)

c.SaveAs("ratio.pdf")
c.Clear()
ROOT.gPad.SetLogy(0)

hstack = {}
hstack["NN"] = []
hstack["Lambda"] = []
hstack["b5x5"] = []

h = {}
h["NN"] = {}
h["Lambda"] = {}
h["b5x5"] = {}

h["NN"]["data"] = []
h["NN"]["MC"]   = []
h["Lambda"]["data"] = []
h["Lambda"]["MC"]   = []
h["b5x5"]["data"] = []
h["b5x5"]["MC"]   = []

colors = [1,2,4,ROOT.kGreen+2,ROOT.kOrange+2,8,9,12] #[2,4,6,33,25]
tags = [ "", "#pi^{0} 2 showers", "#pi^{0} 1 shower", "#eta BKG", "Other BKG"]
#label = Legend("")


limits = {}
limits["NN"] = [32,40]
limits["Lambda"] = [8,40]
limits["b5x5"]  = [8,40]

ptbins = [10.0, 12.0, 14.0, 16.0,18.0,20.0,22.0,24.0,26.0,28.0]


for var in ["NN","Lambda","b5x5"]:
    for ipt in range(len(ptbins)-1):
        print ipt
        
        h[var]["MC"].append(fMC.Get("h_%s_ptbin%i_class0"%(var,ipt)))
        h[var]["data"].append(fdata.Get("h_%s_ptbin%i_class0"%(var,ipt)))
        
        hs = ROOT.THStack("hs_ptbin%i"%ipt,"hs")
        scalefactor = h[var]["data"][ipt].Integral(limits[var][0],limits[var][1])/h[var]["MC"][ipt].Integral(limits[var][0],limits[var][1])
        
        
        for iclass in range(1,5):
            histo = fMC.Get("h_%s_ptbin%i_class%i"%(var,ipt,iclass))
            histo.SetLineColorAlpha(colors[iclass],0.6)
            histo.SetLineWidth(0)
            histo.SetFillColorAlpha(colors[iclass],0.6)
            histo.Scale(scalefactor)
            #if ipt==1 and var=="NN":
                #label.Add(histo, tags[iclass], "L")
            
            
            hs.Add(histo)
        hstack[var].append(hs)


#adding labels:

co = {}
co["NN"] =  2
co["Lambda"] = 4
co["b5x5"] =4



for var in ["NN","Lambda","b5x5"]:
    for ipt in range(len(ptbins)-1):
        h[var]["MC"][ipt].Scale(h[var]["data"][ipt].Integral(limits[var][0],limits[var][1])/h[var]["MC"][ipt].Integral(limits[var][0],limits[var][1]))
        c.Clear()
        #l2 = Legend("%2.0f< p_{T}^{clus} < %2.0f GeV" %(ptbins[ipt],ptbins[ipt+1]))
        h[var]["MC"][ipt].Draw("e1")
        h[var]["data"][ipt].SetLineColorAlpha(1,0.75)
        h[var]["MC"][ipt].SetLineColorAlpha(2,0.75)
        h[var]["data"][ipt].SetMarkerColorAlpha(1,0.75)
        h[var]["MC"][ipt].SetMarkerColorAlpha(2,0.75)
        h[var]["data"][ipt].SetMarkerStyle(20)
        h[var]["MC"][ipt].SetMarkerStyle(20)
        #l2.Add(h[var]["data"][ipt],"Data","P")
        #l2.Add(h[var]["MC"][ipt],"MC","P")
        h[var]["data"][ipt].Draw("e1same")
        #l2.Draw(.5,.85)
        c.SaveAs("try%i_%s.pdf"%(ipt,var))



for var in ["NN","Lambda","b5x5"]:
    for ipt in range(len(ptbins)-1):
        
        hstack[var][ipt].Draw("hist")
        if(var=="NN"): hstack[var][ipt].SetTitle("; NN output (2#gamma); entries");
        else: hstack[var][ipt].SetTitle("; #sigma_{long}^{2}; entries");
        hstack[var][ipt].GetYaxis().SetNdivisions(5)
        hstack[var][ipt].GetXaxis().SetNdivisions(10)
        
        h[var]["data"][ipt].SetMarkerSize(1)
        h[var]["data"][ipt].SetMarkerStyle(20)
        h[var]["data"][ipt].SetLineColor(1)
        
        h[var]["data"][ipt].Draw("e1x0same")
        
        
        #labeldata = Legend("%2.0f< p_{T}^{clus} < %2.0f GeV" %(ptbins[ipt],ptbins[ipt+1]))
        #labeldata.Add(h[var]["data"][ipt],"data, pPb", "P")
        #labeldata.Draw(0.45,0.85)
        #label.Draw(0.45,.8)
        
        c.SaveAs("stack_ptbin%i_%s.pdf"%(ipt,var))
        if var =="Lambda":
            ROOT.gPad.SetLogy()
            #c.SaveAs("stack_ptbin%i_%s_LOG.pdf"%(ipt,var))
            ROOT.gPad.SetLogy(0) 
