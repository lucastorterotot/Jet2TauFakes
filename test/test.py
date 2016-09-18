import ROOT
from array import array

ff_fname="/afs/cern.ch/user/j/jbrandst/public/Htautau/FakeRate/20160913/mt/incl/fakeFactors_20160914.root"

#Retrieve the fake factor
ff_file = ROOT.TFile.Open(ff_fname)
ff      = ff_file.Get("ff_comb")

#Input names
#Currently: tau_pt, tau_decay, njet, mvis, mt, muon_iso
inputNames = ff.inputs() #this returns a ROOT.vector<string> object

#Fill inputs
inputs = [30,0,1,40,10,0.00]

ff_nom = ff.value( len(inputs),array('d',inputs) ) # nominal fake factor

syst_qcd_up = ff.value( len(inputs),array('d',inputs),"ff_qcd_syst_up" );
syst_qcd_down = ff.value( len(inputs),array('d',inputs),"ff_qcd_syst_down" );
syst_w_up = ff.value( len(inputs),array('d',inputs),"ff_w_syst_up" );
syst_w_down = ff.value( len(inputs),array('d',inputs),"ff_w_syst_down" );
syst_tt_up = ff.value( len(inputs),array('d',inputs),"ff_tt_syst_up" );
syst_tt_down = ff.value( len(inputs),array('d',inputs),"ff_tt_syst_down" );

stat_qcd_up = ff.value( len(inputs),array('d',inputs),"ff_qcd_stat_up" );
stat_qcd_down = ff.value( len(inputs),array('d',inputs),"ff_qcd_stat_down" );
stat_w_up = ff.value( len(inputs),array('d',inputs),"ff_w_stat_up" );
stat_w_down = ff.value( len(inputs),array('d',inputs),"ff_w_stat_down" );
stat_tt_up = ff.value( len(inputs),array('d',inputs),"ff_tt_stat_up" );
stat_tt_down = ff.value( len(inputs),array('d',inputs),"ff_tt_stat_down" );

print 'pt= {0}; dm= {1}; njet= {2}; mvis= {3}; mt= {4}; muiso= {5}'.format(inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5])
print 'ff= {0:.6g}'.format(ff_nom)
print ' ----- Systematic uncertainties ----- '
print 'Uncertainties on corrections:'
print 'syst(tt) = {0:.6g}%, syst(w+dy) = {1:.6g}%, syst(qcd) = {2:.6g}%'.format( (syst_tt_up-ff_nom)/ff_nom*100, (syst_w_up-ff_nom)/ff_nom*100, (syst_qcd_up-ff_nom)/ff_nom*100  )
print 'Uncertainties on fake factors:'
print 'stat(tt) = {0:.6g}%, stat(w+dy) = {1:.6g}%, stat(qcd) = {2:.6g}%'.format( (stat_tt_up-ff_nom)/ff_nom*100, (stat_w_up-ff_nom)/ff_nom*100, (stat_qcd_up-ff_nom)/ff_nom*100  )

  
ff.Delete()
ff_file.Close()

