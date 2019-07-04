import ROOT
import os
from array import array

FF_file = '$CMSSW_BASE/src/HTTutilities/Jet2TauFakes/data/SM2017/tight/vloose/{}/fakeFactors.root'
frac_file = "/home/cms/torterotot/public/htt_ff_fractions_2017.root"

def get_event_fake_factor(event, channel, leg=2, sys='', ff=None, w=None):
    '''Interface function to retrieve the fake factors from
    the rootfile for the given channel.
    
    @param sys : if '' -> nominal value, else can be 'up' or 'down'
    '''
    inputs = get_FF_inputs(event, channel, leg, w)
    if sys:
        ffval =  ff.value(len(inputs), array('d',inputs),sys)
    else:
        ffval = ff.value(len(inputs), array('d',inputs))
    return ffval

FF_inputs_from_event = {
    'tt1' : ['l1_pt', 'l2_pt', 'l1_decay_mode', 'n_jets_pt30', 'm_vis'],
    'tt2' : ['l2_pt', 'l1_pt', 'l2_decay_mode', 'n_jets_pt30', 'm_vis'],
    'mt' : ['l2_pt', 'l2_decay_mode', 'n_jets_pt30', 'm_vis', 'mt_tot', 'l1_iso'],
    'et' : ['l2_pt', 'l2_decay_mode', 'n_jets_pt30', 'm_vis', 'mt_tot', 'l1_iso']
}

# For tt channel, inputs = [tau_pt, tau2_pt, tau_decayMode, njets, mvis, frac_qcd, frac_w, frac_tt ]
# For et and mt channels, inputs = [tau_pt, tau_decayMode, njets, mvis, mt, muon_iso, frac_qcd, frac_w, frac_tt]
# Last 3 fractions, common and in same order for all 4 possibilities, are added later in get_FF_inputs

def get_FF_inputs(event, channel, leg, w):
    w.var("m_vis").setVal(event.m_vis)
    w.var("njets").setVal(event.n_jets_pt30)
    w.var("aiso").setVal( leg )
    frac_qcd = w.function("t_frac_qcd").getVal()
    if frac_qcd < 0.:
        frac_qcd = 0.
    frac_w  = w.function("t_frac_w").getVal()
    frac_tt = w.function("t_frac_tt").getVal()
    renorm_factor = 1./(frac_qcd+frac_w+frac_tt)
    inputs = []
    if channel == 'tt':
        channel += str(leg)
    if not all([hasattr(event, attribute) for attribute in FF_inputs_from_event[channel]]):
        raise AttributeError('Please check that events have these attributes:\n   {}'.format(FF_inputs_from_event[channel]))
    else:
        for attribute in FF_inputs_from_event[channel]:
            inputs.append(getattr(event, attribute))
        for frac in [frac_qcd, frac_w, frac_tt ]:
            inputs.append(frac*renorm_factor)
        return inputs

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
                      default=False,
                      help='Systematics')
    
    (options,args) = parser.parse_args()
    return options, args
    
def FakesAdd(oldfile, newfile, systematics=False, channel='tt'):
    inclfile = ROOT.TFile(FF_file.format(channel))
    inclff = inclfile.Get('ff_comb')

    f = ROOT.TFile(frac_file)
    w = f.Get("w")
    f.Close()
    
    oldtree = oldfile.Get('events')
    # f = ROOT.TFile(oldfilename.replace('.root','_fakes.root'),'recreate')
    newfile.cd() #TODO test
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
            l1_fakeweight[0] = get_event_fake_factor(event, channel=channel, leg=1, ff=inclff, w=w)
        l2_fakeweight[0] = get_event_fake_factor(event, channel=channel, leg=2, ff=inclff, w=w)
        if systematics:
            if channel == 'tt':
                l1_fakeweight_up[0] = get_event_fake_factor(event, channel=channel, leg=1, sys='up', ff=inclff, w=w)
            l2_fakeweight_up[0] = get_event_fake_factor(event, channel=channel, leg=2, sys='up', ff=inclff, w=w)
            if channel == 'tt':
                l1_fakeweight_down[0] = get_event_fake_factor(event, channel=channel, leg=1, sys='down', ff=inclff, w=w)
            l2_fakeweight_down[0] = get_event_fake_factor(event, channel=channel, leg=2, sys='down', ff=inclff, w=w)
        tree.Fill()
    tree.Write()
    #f.Close()


if __name__ == '__main__':

    options, args = get_options()
    src = args[0]
    FakesAdd(src, systematics=options.systematics, channel=options.channel)
