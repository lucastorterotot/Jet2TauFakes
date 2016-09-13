#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

void test(TString fname="/afs/cern.ch/user/j/jbrandst/public/Htautau/FakeRate/20160913/mt/incl/fakeFactors_20160913.root"){

  // Retrieve the fake factor
  TFile* ff_file = TFile::Open(fname);
  FakeFactor* ff    = (FakeFactor*)ff_file->Get("ff_comb");

  // Fill inputs
  std::vector<double> inputs(6);
  inputs[0] = 30; //tau_pt;
  inputs[1] = 0;  //tau_decayMode;
  inputs[2] = 1;  //njet
  inputs[3] = 40; //mvis;
  inputs[4] = 10; //mt;
  inputs[5] = 0.00; //muon_iso;

  // Retrieve fake factors
  double ff_nom = ff->value(inputs); // nominal fake factor

  double syst_qcd_up = ff->value(inputs, "ff_qcd_syst_up");
  double syst_qcd_down = ff->value(inputs, "ff_qcd_syst_down");
  double syst_w_up = ff->value(inputs, "ff_w_syst_up");
  double syst_w_down = ff->value(inputs, "ff_w_syst_down");
  double syst_tt_up = ff->value(inputs, "ff_tt_syst_up");
  double syst_tt_down = ff->value(inputs, "ff_tt_syst_down");

  double stat_qcd_up = ff->value(inputs, "ff_qcd_stat_up");
  double stat_qcd_down = ff->value(inputs, "ff_qcd_stat_down");
  double stat_w_up = ff->value(inputs, "ff_w_stat_up");
  double stat_w_down = ff->value(inputs, "ff_w_stat_down");
  double stat_tt_up = ff->value(inputs, "ff_tt_stat_up");
  double stat_tt_down = ff->value(inputs, "ff_tt_stat_down");
  
  cout << "pt= " << inputs[0] << "\t dm= " << inputs[1] << "\t njet= " << inputs[2] << "\t mvis= " << inputs[3] << "\t mt= " << inputs[4] << "\t muiso= " << inputs[5] << endl;
  cout << "ff= " << ff_nom << endl;
  cout << " ----- Systematic uncertainties ----- " << endl;
  cout << "Uncertainties on corrections: " << endl;
  cout << "syst(tt)= " << (syst_tt_up-ff_nom)/ff_nom << "%, syst(w+dy)= " << (syst_w_up-ff_nom)/ff_nom*100 << "%, syst(qcd)= " << (syst_qcd_up-ff_nom)/ff_nom*100 << "%" <<  endl;
  cout << "Uncertainties on fake factors: " << endl;
  cout << "stat(tt)= " << (stat_tt_up-ff_nom)/ff_nom*100 << "%, stat(w+dy)= " << (stat_w_up-ff_nom)/ff_nom*100 << "%, stat(qcd)= " << (stat_qcd_up-ff_nom)/ff_nom*100 << "%" << endl;

  delete ff;
  ff_file->Close();

}
