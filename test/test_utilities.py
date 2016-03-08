from HTTutilities.Jet2TauFakes.Utilities import Leaf, Node, fill, FakeFactor
import ROOT
from array import array


ff = FakeFactor(['tau_pt', 'tau_decay', 'mt'])

leaf1 = Leaf(
    name='ff_W',
    file='/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/Studies/FakeRate/ComputeFakeRates/plots/FakeFactors_Data_HighMT_2D/FakeFactors_Data_HighMT_2D.root',
    object='FakeFactors_Data_HighMT_2D_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode',
    vars=['tau_pt','tau_decay']
)
leaf2 = Leaf(
    name='corr_mt',
    file='/afs/cern.ch/user/j/jsauvan/workspace/Projects/Htautau_Run2/Studies/FakeRate/ComputeMTCorrection/results/mtCorrections.root',
    object='mt_correction',
    vars=['mt']
)
node = Node(
    name='ff_W_corr',
    formula='{corr_mt}*{ff_W}',
    leaves=[leaf1,leaf2]
)

fill(ff, node)
print ff.value([30,1,10])
