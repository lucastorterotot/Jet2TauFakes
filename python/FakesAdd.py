import ROOT
import os
from array import array
from functools import partial
import multiprocessing as mp

def multithreadmap(f,X,ncores=20, **kwargs):
    """
    multithreading map of a function, default on 20 cpu cores.
    """
    func = partial(f, **kwargs)
    p=mp.Pool(ncores)
    Xout = p.map(func,X)
    p.terminate()
    return(Xout)


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

def FakesAdd(oldfilename, systematics=False):

    inclfile = ROOT.TFile('$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/tt/fakeFactors.root')
    inclff = inclfile.Get('ff_comb')

    f = ROOT.TFile("/afs/cern.ch/work/j/jbechtel/public/htt_ff_fractions_2017_incl.xroot")
    w = f.Get("w")
    f.Close()
    
    oldfile = ROOT.TFile(oldfilename)
    oldtree = oldfile.Get('events')
    f = ROOT.TFile(oldfilename.replace('.root','_fakes.root'),'recreate')
    tree = oldtree.CloneTree(0)
    l1_fakeweight = array('d',[1.])
    l1_fakesbranch = tree.Branch('l1_fakeweight',l1_fakeweight,'l1_fakeweight/D')
    l2_fakeweight = array('d',[1.])
    l2_fakesbranch = tree.Branch('l2_fakeweight',l2_fakeweight,'l2_fakeweight/D')
    if systematics:
        l1_fakeweight_up = array('d',[1.])
        l1_fakesbranch_up = tree.Branch('l1_fakeweight_up',l1_fakeweight_up,'l1_fakeweight_up/D')
        l2_fakeweight_up = array('d',[1.])
        l2_fakesbranch_up = tree.Branch('l2_fakeweight_up',l2_fakeweight_up,'l2_fakeweight_up/D')
        l1_fakeweight_down = array('d',[1.])
        l1_fakesbranch_down = tree.Branch('l1_fakeweight_down',l1_fakeweight_down,'l1_fakeweight_down/D')
        l2_fakeweight_down = array('d',[1.])
        l2_fakesbranch_down = tree.Branch('l2_fakeweight_down',l2_fakeweight_down,'l2_fakeweight_down/D')
    for event in oldtree:
        l1_fakeweight[0] = fake_factor_fullyhadronic(event.l1_pt,
                                                  event.l2_pt,
                                                  event.l1_decay_mode,
                                                  event.n_jets_pt30,
                                                  event.m_vis, aisoregion=1,ff=inclff, w=w)
        l2_fakeweight[0] = fake_factor_fullyhadronic(event.l2_pt,
                                                  event.l1_pt,
                                                  event.l2_decay_mode,
                                                  event.n_jets_pt30,
                                                  event.m_vis, aisoregion=2,ff=inclff, w=w)
        if systematics:
            l1_fakeweight_up[0] = fake_factor_fullyhadronic(event.l1_pt,
                                                         event.l2_pt,
                                                         event.l1_decay_mode,
                                                         event.n_jets_pt30,
                                                         event.m_vis,
                                                         'up', aisoregion=1,ff=inclff, w=w)
            l2_fakeweight_up[0] = fake_factor_fullyhadronic(event.l2_pt,
                                                         event.l1_pt,
                                                         event.l2_decay_mode,
                                                         event.n_jets_pt30,
                                                         event.m_vis,
                                                         'up', aisoregion=2,ff=inclff, w=w)
            l1_fakeweight_down[0] = fake_factor_fullyhadronic(event.l1_pt,
                                                           event.l2_pt,
                                                           event.l1_decay_mode,
                                                           event.n_jets_pt30,
                                                           event.m_vis,
                                                           'down', aisoregion=1,ff=inclff, w=w)
            l2_fakeweight_down[0] = fake_factor_fullyhadronic(event.l2_pt,
                                                           event.l1_pt,
                                                           event.l2_decay_mode,
                                                           event.n_jets_pt30,
                                                           event.m_vis,
                                                           'down', aisoregion=2,ff=inclff, w=w)
        tree.Fill()
    tree.Write()
    f.Close()


if __name__ == '__main__':

    
    files_to_process = ['Embedded2017B_tt',
                        'Embedded2017C_tt',
                        'Embedded2017D_tt',
                        'Embedded2017E_tt',
                        'Embedded2017F_tt',
                        # 'TBar_tWch',
                        # 'TBar_tch',
                        # 'T_tWch',
                        # 'T_tch',
                        # 'WW',
                        # 'WZ',
                        # 'ZZ',
                        # 'DYJetsToLL_M50',
                        # 'DYJetsToLL_M50_ext',
                        # 'WJetsToLNu_LO',
                        # 'WJetsToLNu_LO_ext',
                        # 'TTHad_pow',
                        # 'TTSemi_pow',
                        # 'TTLep_pow',
                        # 'Tau_Run2017B_31Mar2018',
                        # 'Tau_Run2017C_31Mar2018',
                        # 'Tau_Run2017D_31Mar2018',
                        # 'Tau_Run2017E_31Mar2018',
                        # 'Tau_Run2017F_31Mar2018',
                        ]
    # for f in files_to_process:
    #     print 'adding fakes to' , f
    #     FakesAdd('trees/{}/NtupleProducer/tree.root'.format(f))
    files_to_process = []

    os.system('ls trees/ > trees.out')

    with open('trees.out') as f:
        for l in f.readlines():
            files_to_process.append(l[:-1])

    files_to_process = ['trees/{}/tree.root'.format(f) for f in files_to_process]
    multithreadmap(FakesAdd, files_to_process)
