#include <vector>
#include <iostream>
#include "TFile.h"
#include "TSystem.h"
#include "TGraph.h"
//#include "TGraphAsymmErrors.h"
#include "TFormula.h"
#include "TH2F.h"

#include "HTT-utilities/Jet2TauFakes/interface/WrapperTGraph.h"
#include "HTT-utilities/Jet2TauFakes/interface/WrapperTH2F.h"
#include "HTT-utilities/Jet2TauFakes/interface/WrapperTFormula.h"
#include "HTT-utilities/Jet2TauFakes/interface/IFunctionWrapper.h"
#include "HTT-utilities/Jet2TauFakes/interface/FakeFactor.h"

void test()
{

    TFile* fFakeFactorW  = TFile::Open("/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/Studies/FakeRate/ComputeFakeRates/plots/FakeFactors_Data_HighMT_2D/FakeFactors_Data_HighMT_2D.root");
    TFile* fFakeFactorQCD  = TFile::Open("/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/Studies/FakeRate/ComputeFakeRates/plots/FakeFactors_Data_QCDSS_2D/FakeFactors_Data_QCDSS_2D.root");
    TFile* fMtCorrection = TFile::Open("/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/Studies/FakeRate/ComputeMTCorrection/results/mtCorrections.root");
    TFile* fFractions    = TFile::Open("/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/Studies/FakeRate/ComputeBackgroundFractions/results/backgroundFraction_Iso_Medium_mvis_vs_mt.root");

    TH2F* fakeFactorW   = (TH2F*)fFakeFactorW->Get("FakeFactors_Data_HighMT_2D_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode");
    TH2F* fakeFactorQCD = (TH2F*)fFakeFactorQCD->Get("FakeFactors_Data_QCDSS_2D_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode");
    TGraph* mtCorrection = (TGraph*)fMtCorrection->Get("mt_correction");
    TH2F* fractionW = (TH2F*)fFractions->Get("h_backgroundFraction_Iso_Medium_mvis_vs_mt_W_Nom");
    TH2F* fractionQCD = (TH2F*)fFractions->Get("h_backgroundFraction_Iso_Medium_mvis_vs_mt_QCD_Nom");
    TH2F* fractionTT = (TH2F*)fFractions->Get("h_backgroundFraction_Iso_Medium_mvis_vs_mt_TT_Nom");
    TH2F* fractionVV = (TH2F*)fFractions->Get("h_backgroundFraction_Iso_Medium_mvis_vs_mt_VV_Nom");
    TH2F* fractionZJ = (TH2F*)fFractions->Get("h_backgroundFraction_Iso_Medium_mvis_vs_mt_ZJ_Nom");


    //wrappers
    WrapperTH2F* wFakeFactorW    = new WrapperTH2F(*fakeFactorW, "FF_W");
    WrapperTH2F* wFakeFactorQCD  = new WrapperTH2F(*fakeFactorQCD, "FF_QCD");
    WrapperTGraph* wMtCorrection = new WrapperTGraph(*mtCorrection, "MT_Corr");
    WrapperTH2F* wFractionW      = new WrapperTH2F(*fractionW, "f_W");
    WrapperTH2F* wFractionQCD    = new WrapperTH2F(*fractionQCD, "f_QCD");
    WrapperTH2F* wFractionTT     = new WrapperTH2F(*fractionTT, "f_TT");
    WrapperTH2F* wFractionVV     = new WrapperTH2F(*fractionVV, "f_VV");
    WrapperTH2F* wFractionZJ     = new WrapperTH2F(*fractionZJ, "f_ZJ");

    // formulas
    TFormula mtCorr("mtCorr", "x[0]*x[1]");
    WrapperTFormula* wFakeFactorWCorr = new WrapperTFormula(mtCorr, "FF_WCorr");

    TFormula combination("combination", "x[0]*x[2]+x[1]*(x[3]+x[4]+x[5]+x[6])");
    WrapperTFormula* wFakeFactorComb = new WrapperTFormula(combination, "FF_Comb");

    // fake factor
    // tau_pt = 0
    // tau_decay = 1
    // mt = 2
    // mvis = 3
    FakeFactor* factor = new FakeFactor();
    factor->addNode(wFakeFactorW, {}, {0,1});
    factor->addNode(wFakeFactorQCD, {}, {0,1});
    factor->addNode(wMtCorrection, {}, {2});
    factor->addNode(wFractionW, {}, {3,2});
    factor->addNode(wFractionQCD, {}, {3,2});
    factor->addNode(wFractionTT, {}, {3,2});
    factor->addNode(wFractionVV, {}, {3,2});
    factor->addNode(wFractionZJ, {}, {3,2});
    factor->addNode(wFakeFactorWCorr, {0,2}, {});
    factor->addNode(wFakeFactorComb, {1,8,4,3,5,6,7}, {});

    TFile* file = TFile::Open("test.root", "recreate");
    file->WriteObject(factor, "ff");
    file->Close();
    std::cout<<"Done\n";

}
