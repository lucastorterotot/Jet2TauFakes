import ROOT
import os
from array import array

def fake_factor_et(elept, taupt, taudecaymode, njets, mvis, sys='', aisoregion=1, ff=None, w=None):
    '''Interface function to retrieve the fake factors from
    the rootfile for the ele+tau channel.
    
    @param sys : if '' -> nominal value, else can be 'up' or 'down'
    '''
    return 1.

def fake_factor_mt(mupt, taupt, taudecaymode, njets, mvis, sys='', aisoregion=1, ff=None, w=None):
    '''Interface function to retrieve the fake factors from
    the rootfile for the muon+tau channel.
    
    @param sys : if '' -> nominal value, else can be 'up' or 'down'
    '''
    return 1.

def fake_factor_fullyhadronic(tau1pt, tau2pt, tau1decaymode, njets, mvis, sys='', aisoregion=1, ff=None, w=None):
    '''Interface function to retrieve the fake factors from
    the rootfile for the fully hadronic channel.
    
    @param sys : if '' -> nominal value, else can be 'up' or 'down'
    '''
    w.var("m_vis").setVal(mvis)
    w.var("njets").setVal(njets)
    w.var("aiso").setVal( aisoregion )
    frac_qcd = w.function("t_frac_qcd").getVal()
    if frac_qcd < 0.:
        frac_qcd = 0.
    frac_w  = w.function("t_frac_w").getVal()
    frac_tt = w.function("t_frac_tt").getVal()
    renorm_factor = 1./(frac_qcd+frac_w+frac_tt)
    inputs = [tau1pt,
              tau2pt, 
              tau1decaymode, 
              njets,
              mvis,
              frac_qcd*renorm_factor,
              frac_w*renorm_factor,
              frac_tt*renorm_factor]
    if sys:
        ffval =  ff.value(len(inputs), array('d',inputs),sys)
    else:
        ffval = ff.value(len(inputs), array('d',inputs))
    return ffval

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] <src_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-C", "--channel", dest = "channel",
                      default='tt',
                      help='Channel to process: tt, mt or et')
    parser.add_option("-s", "--systematics", dest = "systematics",
                      default='False',
                      help='Systematics')
    
    (options,args) = parser.parse_args()
    return options, args

fake_factor_fcts_channel = {
    'tt' : fake_factor_fullyhadronic,
    'mt' : fake_factor_mt,
    'et' : fake_factor_et
}
    
def FakesAdd(oldfilename, systematics=False, channel='tt'):
    fake_factor_fct = fake_factor_fcts_channel[channel]
        
    inclfile = ROOT.TFile('$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/'+channel+'/fakeFactors.root')
    inclff = inclfile.Get('ff_comb')

    f = ROOT.TFile("/afs/cern.ch/work/j/jbechtel/public/htt_ff_fractions_2017_incl.xroot")
    w = f.Get("w")
    f.Close()
    
    oldfile = ROOT.TFile(oldfilename)
    oldtree = oldfile.Get('events')
    f = ROOT.TFile(oldfilename.replace('.root','_fakes.root'),'recreate')
    tree = oldtree.CloneTree(0)
    if channel == 'tt':
        l1_fakeweight = array('d',[1.])
        l1_fakesbranch = tree.Branch('l1_fakeweight',l1_fakeweight,'l1_fakeweight/D')
    l2_fakeweight = array('d',[1.])
    l2_fakesbranch = tree.Branch('l2_fakeweight',l2_fakeweight,'l2_fakeweight/D')
    if systematics:
        if channel == 'tt':
            l1_fakeweight_up = array('d',[1.])
            l1_fakesbranch_up = tree.Branch('l1_fakeweight_up',l1_fakeweight_up,'l1_fakeweight_up/D')
        l2_fakeweight_up = array('d',[1.])
        l2_fakesbranch_up = tree.Branch('l2_fakeweight_up',l2_fakeweight_up,'l2_fakeweight_up/D')
        if channel == 'tt':
            l1_fakeweight_down = array('d',[1.])
            l1_fakesbranch_down = tree.Branch('l1_fakeweight_down',l1_fakeweight_down,'l1_fakeweight_down/D')
        l2_fakeweight_down = array('d',[1.])
        l2_fakesbranch_down = tree.Branch('l2_fakeweight_down',l2_fakeweight_down,'l2_fakeweight_down/D')
    for event in oldtree:
        if channel == 'tt':
            l1_fakeweight[0] = fake_factor_fct(event.l1_pt,
                                                  event.l2_pt,
                                                  event.l1_decay_mode,
                                                  event.n_jets_pt30,
                                                  event.m_vis, aisoregion=1,ff=inclff, w=w)
        l2_fakeweight[0] = fake_factor_fct(event.l2_pt,
                                                  event.l1_pt,
                                                  event.l2_decay_mode,
                                                  event.n_jets_pt30,
                                                  event.m_vis, aisoregion=2,ff=inclff, w=w)
        if systematics:
            if channel == 'tt':
                l1_fakeweight_up[0] = fake_factor_fct(event.l1_pt,
                                                         event.l2_pt,
                                                         event.l1_decay_mode,
                                                         event.n_jets_pt30,
                                                         event.m_vis,
                                                         'up', aisoregion=1,ff=inclff, w=w)
            l2_fakeweight_up[0] = fake_factor_fct(event.l2_pt,
                                                         event.l1_pt,
                                                         event.l2_decay_mode,
                                                         event.n_jets_pt30,
                                                         event.m_vis,
                                                         'up', aisoregion=2,ff=inclff, w=w)
            if channel == 'tt':
                l1_fakeweight_down[0] = fake_factor_fct(event.l1_pt,
                                                           event.l2_pt,
                                                           event.l1_decay_mode,
                                                           event.n_jets_pt30,
                                                           event.m_vis,
                                                           'down', aisoregion=1,ff=inclff, w=w)
            l2_fakeweight_down[0] = fake_factor_fct(event.l2_pt,
                                                           event.l1_pt,
                                                           event.l2_decay_mode,
                                                           event.n_jets_pt30,
                                                           event.m_vis,
                                                           'down', aisoregion=2,ff=inclff, w=w)
        tree.Fill()
    tree.Write()
    f.Close()


if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    FakesAdd(src, systematics=options.systematics, channel=options.channel)
