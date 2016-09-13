#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

void test_Sep2016(TString fname="/afs/cern.ch/user/j/jbrandst/public/Htautau/FakeRate/20160913/mt/incl/fakeFactors_20160913.root"){

  // Retrieve the fake factor
  TFile* ff_file = TFile::Open(fname);
  FakeFactor* ff    = (FakeFactor*)ff_file->Get("ff_comb");
  FakeFactor* ff_tt = (FakeFactor*)ff_file->Get("ff_tt");
  FakeFactor* ff_w = (FakeFactor*)ff_file->Get("ff_w");
  FakeFactor* ff_qcd = (FakeFactor*)ff_file->Get("ff_qcd_os");

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
  double ff_nom_tt = ff_tt->value(inputs); // nominal fake factor tt
  double ff_nom_w = ff_w->value(inputs);
  double ff_nom_qcd = ff_qcd->value(inputs);

  double frac_w = ff_w->value(inputs,"frac_w");
  double frac_dy = ff_w->value(inputs,"frac_dy");
  double frac_qcd = ff_qcd->value(inputs,"frac_qcd");
  double frac_tt = ff_tt->value(inputs,"frac_tt");

  double syst_qcd_up = ff_qcd->value(inputs, "ff_qcd_syst_up");
  double syst_qcd_down = ff_qcd->value(inputs, "ff_qcd_syst_down");
  double syst_w_up = ff_w->value(inputs, "ff_w_syst_up");
  double syst_w_down = ff_w->value(inputs, "ff_w_syst_down");
  double syst_tt_up = ff_tt->value(inputs, "ff_tt_syst_up");
  double syst_tt_down = ff_tt->value(inputs, "ff_tt_syst_down");

  double stat_qcd_up = ff_qcd->value(inputs, "ff_qcd_stat_up");
  double stat_qcd_down = ff_qcd->value(inputs, "ff_qcd_stat_down");
  double stat_w_up = ff_w->value(inputs, "ff_w_stat_up");
  double stat_w_down = ff_w->value(inputs, "ff_w_stat_down");
  double stat_tt_up = ff_tt->value(inputs, "ff_tt_stat_up");
  double stat_tt_down = ff_tt->value(inputs, "ff_tt_stat_down");
  
  cout << "pt= " << inputs[0] << "\t dm= " << inputs[1] << "\t njet= " << inputs[2] << "\t mvis= " << inputs[3] << "\t mt= " << inputs[4] << "\t muiso= " << inputs[5] << endl;
  cout << "ff= " << ff_nom << ", ff(tt)= " << ff_nom_tt  << ", ff(w)= " << ff_nom_w << ", ff(qcd)= " << ff_nom_qcd  << endl;
  cout << "frac(tt)= " << frac_tt  << ", frac(w)= " << frac_w << ", frac(dy)= " << frac_dy << ", frac_qcd= " << frac_qcd  << endl;
  cout << "Combined fake factor: " << ff_nom_tt*frac_tt+ff_nom_w*(frac_w+frac_dy)+ff_nom_qcd*frac_qcd << endl;
  cout << " ----- Systematic uncertainties ----- " << endl;
  cout << "Uncertainties on corrections: " << endl;
  cout << "syst(tt)= " << (syst_tt_up-ff_nom_tt)/ff_nom_tt*100 << "%, syst(w)= " << (syst_w_up-ff_nom_w)/ff_nom_w*100 << "%, syst(dy)= " << (syst_w_up-ff_nom_w)/ff_nom_w*100 << "%, syst(qcd)= " << (syst_qcd_up-ff_nom_qcd)/ff_nom_qcd*100 << "%" <<  endl;
  cout << "Uncertainties on fake factors: " << endl;
  cout << "stat(tt)= " << (stat_tt_up-ff_nom_tt)/ff_nom_tt*100 << "%, stat(w)= " << (stat_w_up-ff_nom_w)/ff_nom_w*100 << "%, stat(dy)= " << (stat_w_up-ff_nom_w)/ff_nom_w*100 << "%, stat(qcd)= " << (stat_qcd_up-ff_nom_qcd)/ff_nom_qcd*100 << "%" << endl;


  delete ff;
  delete ff_tt;
  delete ff_w;
  delete ff_qcd;
  ff_file->Close();

}
