import ROOT
from array import array

ff_fname="/afs/cern.ch/user/j/jbrandst/public/Htautau/FakeRate/20160913/mt/incl/fakeFactors_20160913.root"

#Retrieve the fake factor
ff_file = ROOT.TFile.Open(ff_fname)
ff      = ff_file.Get("ff_comb")
ff_tt   = ff_file.Get("ff_tt")
ff_w    = ff_file.Get("ff_w")
ff_qcd  = ff_file.Get("ff_qcd_os")

#Input names
#Currently: tau_pt, tau_decay, njet, mvis, mt, muon_iso
inputNames = ff.inputs() #this returns a ROOT.vector<string> object

#Fill inputs
inputs = [30,0,1,40,10,0.00]

ff_nom = ff.value( len(inputs),array('d',inputs) ) # nominal fake factor
ff_nom_tt = ff_tt.value( len(inputs),array('d',inputs) ) # nominal tt fake factor
ff_nom_w = ff_w.value( len(inputs),array('d',inputs) ) # nominal w fake factor
ff_nom_qcd = ff_qcd.value( len(inputs),array('d',inputs) ) # nominal qcd fake factor

frac_tt = ff_tt.value( len(inputs),array('d',inputs),"frac_tt" );
frac_w = ff_w.value( len(inputs),array('d',inputs),"frac_w" );
frac_dy = ff_w.value( len(inputs),array('d',inputs),"frac_dy" );
frac_qcd = ff_qcd.value( len(inputs),array('d',inputs),"frac_qcd" );

syst_qcd_up = ff_qcd.value( len(inputs),array('d',inputs),"ff_qcd_syst_up" );
syst_qcd_down = ff_qcd.value( len(inputs),array('d',inputs),"ff_qcd_syst_down" );
syst_w_up = ff_w.value( len(inputs),array('d',inputs),"ff_w_syst_up" );
syst_w_down = ff_w.value( len(inputs),array('d',inputs),"ff_w_syst_down" );
syst_tt_up = ff_tt.value( len(inputs),array('d',inputs),"ff_tt_syst_up" );
syst_tt_down = ff_tt.value( len(inputs),array('d',inputs),"ff_tt_syst_down" );

stat_qcd_up = ff_qcd.value( len(inputs),array('d',inputs),"ff_qcd_stat_up" );
stat_qcd_down = ff_qcd.value( len(inputs),array('d',inputs),"ff_qcd_stat_down" );
stat_w_up = ff_w.value( len(inputs),array('d',inputs),"ff_w_stat_up" );
stat_w_down = ff_w.value( len(inputs),array('d',inputs),"ff_w_stat_down" );
stat_tt_up = ff_tt.value( len(inputs),array('d',inputs),"ff_tt_stat_up" );
stat_tt_down = ff_tt.value( len(inputs),array('d',inputs),"ff_tt_stat_down" );

print 'pt= {0}; dm= {1}; njet= {2}; mvis= {3}; mt= {4}; muiso= {5}'.format(inputs[0],inputs[1],inputs[2],inputs[3],inputs[4],inputs[5])
print 'ff= {0:.6g}, ff(tt)= {1:.6g}, ff(w)= {2:.6g}, ff(qcd)={3:.6g}'.format(ff_nom,ff_nom_tt,ff_nom_w,ff_nom_qcd)
print 'frac(tt)= {0:.6g}, frac(w)= {1:.6g}, frac(dy)= {2:.6g}, frac(qcd)={3:.6g}'.format(ff_nom,ff_nom_tt,ff_nom_w,ff_nom_qcd)
print 'Combined fake factor: {0}'.format(ff_nom_tt*frac_tt+ff_nom_w*(frac_w+frac_dy)+ff_nom_qcd*frac_qcd)
print ' ----- Systematic uncertainties ----- '
print 'Uncertainties on corrections:'
print 'syst(tt) = {0:.6g}%, syst(w) = {1:.6g}%, syst(dy) = {2:.6g}%, syst(qcd) = {3:.6g}%'.format( (syst_tt_up-ff_nom_tt)/ff_nom_tt*100, (syst_w_up-ff_nom_w)/ff_nom_w*100, (syst_w_up-ff_nom_w)/ff_nom_w*100, (syst_qcd_up-ff_nom_qcd)/ff_nom_qcd*100  )
print 'stat(tt) = {0:.6g}%, stat(w) = {1:.6g}%, stat(dy) = {2:.6g}%, stat(qcd) = {3:.6g}%'.format( (stat_tt_up-ff_nom_tt)/ff_nom_tt*100, (stat_w_up-ff_nom_w)/ff_nom_w*100, (stat_w_up-ff_nom_w)/ff_nom_w*100, (stat_qcd_up-ff_nom_qcd)/ff_nom_qcd*100  )

  
ff.Delete()
ff_tt.Delete()
ff_w.Delete()
ff_qcd.Delete()
ff_file.Close()

