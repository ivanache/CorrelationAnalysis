// This program takes as arguments a ROOT file and names of the signal and background histograms, the name that will be give to the resultant file, along with purity and its uncertainty and processes it as follows: (hSR-hBR*(1-p))/p
// hSR: signal histogram
// hBR: background histogram
// p: purity
// The results are then loaded into a separate ROOT file
// Precondition: signal and background histograms have the same dimensions, purity is not 0
// Author: Ivan Chernyshev; Date: 7/18/2018

#include <TFile.h>
#include <TTree.h>
#include <TLorentzVector.h>

#include <TROOT.h>
#include <TApplication.h>
#include <TCanvas.h>
#include <TStyle.h>
#include <TH2D.h>
#include <THStack.h>
#include <TProfile.h>
#include <iostream>
#include <fstream>
#include <TGraphAsymmErrors.h>

#define NTRACK_MAX (1U << 15)

#include <vector>
#include <math.h>
#include <set>

// Executes the formula in the program description on a pair of 1D histograms
// Precondition: the two histograms must have the same x-dimensions
TH1D* purityadjustment_histograms1D(TH1D* sig_graph, TH1D* bkg_graph, double purity, double deltapurity){
    // Make the 1D histogram to contain the result and find minimum and maximum bins along both axes
    TH1D* result = new TH1D(*sig_graph);
    double x_bin_min = result->GetXaxis()->FindBin(result->GetXaxis()->GetXmin());
    double x_bin_max = result->GetXaxis()->FindBin(result->GetXaxis()->GetXmax());
    
    // Loop over all bins, set the result's bins to the formula. Manually propogate the error
    for(int i = x_bin_min; i <= x_bin_max; i++){
        double sig = sig_graph->GetBinContent(i);
        double bkg = bkg_graph->GetBinContent(i);
        result->SetBinContent(i, (sig - ((1-purity)*bkg) )/purity );
        
        // Error propogation
        double deltasig = result->GetBinError(i);
        double deltabkg = result->GetBinError(i);
        double deltares = TMath::Sqrt( (( (deltasig*deltasig) + (bkg*bkg*deltapurity*deltapurity) + (purity*purity*deltabkg*deltabkg) )/(purity*purity)) + (( ((sig-((1-purity)*bkg))) * ((sig-((1-purity)*bkg))) *deltapurity*deltapurity)/(purity*purity*purity*purity)) );
        result->SetBinError(i, deltares);
    }
    
    
    return result;
}

int main(int argc, char *argv[]) {
    if(argc < 6){
        std::cout << "Syntax is [command to execute program] [ROOT file with histograms] [signal histogram name] [background histogram name] [result histogram name] [purity] [purity uncertainty]" << std::endl;
        exit(EXIT_FAILURE);
    }
    
    // Get the file, signal, background, and purity
    TFile *fdata = new TFile(argv[1], "READ");
    
    if (fdata == NULL) {
        std::cout << " fail; could not open file" << std::endl;
        exit(EXIT_FAILURE);
    }
    fdata->Print();
    
    TH1D* signal = 0;
    TH1D* background = 0;
    fdata->GetObject((TString)argv[2], signal);
    fdata->GetObject((TString)argv[3], background);
    if(signal == NULL) {
        std::cout << " fail; could not open signal histogram" << std::endl;
        exit(EXIT_FAILURE);
    }
    if(background == NULL) {
        std::cout << " fail; could not open background histogram" << std::endl;
        exit(EXIT_FAILURE);
    }
    
    std::string resultname = (std::string)argv[4];
    
    double purity = atof(argv[5]);
    
    double deltapurity = 0;
    if(argc > 6)
        deltapurity = atof(argv[6]);
    
    TH1D* processResult = purityadjustment_histograms1D(signal, background, purity, deltapurity);
    processResult->SetName(resultname.c_str());
    
    TFile *fout = new TFile("subtraction_FOUT.root", "CREATE");
    
    processResult->Write();
    
    fdata->Close();
    
    return EXIT_SUCCESS;
}
