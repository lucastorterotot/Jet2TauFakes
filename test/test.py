import ROOT
import os
from array import array


cmsswBase = os.environ["CMSSW_BASE"]
scram_arch = os.environ["SCRAM_ARCH"]
ROOT.gSystem.AddDynamicPath("{0}/lib/{1}/".format(cmsswBase, scram_arch))
ROOT.gSystem.Load("libHTTutilitiesJet2TauFakes.so") 



# graph
xs = [1,2,3]
ys = [1,2,3]
g = ROOT.TGraph(len(xs), array('d',xs), array('d',ys))
graph = ROOT.WrapperTGraph(g, "graph")

# histo
h = ROOT.TH2F("histo","histo",10,0,10, 10,0,10);
for bx in xrange(1,11):
    x = h.GetXaxis().GetBinCenter(bx)
    for by in xrange(1,11):
        y = h.GetYaxis().GetBinCenter(by)
        h.SetBinContent(bx,by, x*y)
histo = ROOT.WrapperTH2F(h, "histo")

# formula
f = ROOT.TFormula("form", "x[0]+x[1]")
form = ROOT.WrapperTFormula(f, "form")

# fake factor
factor = ROOT.FakeFactor()
factor.addNode(graph, 0, array('L',[0]), 1, array('L',[0])) ## dummy arrays if size = 0 (empty arrays are not properly converted)
factor.addNode(histo, 0, array('L',[0]), 2, array('L',[1,2])) 
factor.addNode(form, 2, array('L',[0,1]), 0, array('L',[0]))


factor.value(3, array('d',[2,5.5,5.5]))

file = ROOT.TFile.Open("test.root", "recreate")
file.WriteObject(factor, "ff")
file.Close()
print "Done"



