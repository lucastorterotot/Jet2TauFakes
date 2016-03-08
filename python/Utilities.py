import ROOT
import copy

class Node:
    def __init__(self, name='', formula='', leaves=[]):
        self.name    = name
        self.formula = formula
        self.leaves = leaves

    def create(self):
        formula = copy.deepcopy(self.formula)
        ## format formula
        for i,leaf in enumerate(self.leaves):
            tag = '{'+leaf.name+'}'
            if not tag in formula:
                raise StandardError(leaf.name+' is declared as leaf of node '+self.name+' but it is not part of the given formula.')
            formula = formula.replace(tag,'x[{}]'.format(i))
        ## create TFormula
        tformula = ROOT.TFormula(self.name, formula)
        wtformula = ROOT.WrapperTFormula(tformula, self.name)
        return wtformula


class Leaf:
    def __init__(self, name='', file='', object='', vars=[]):
        self.name = name
        self.file = file
        self.object = object
        self.vars = vars

    def create(self):
        file = ROOT.TFile.Open(self.file)
        if not file:
            raise StandardError('Cannot open file '+self.file+' for leaf '+self.name)
        object = file.Get(self.object)
        if not object:
            raise StandardError('Cannot load object '+self.object+' for leaf '+self.name)
        ## create wrapper according to object type
        wobject = None
        ROOT.gDirectory = ROOT.gROOT
        if isinstance(object, ROOT.TGraph):
            wobject = ROOT.WrapperTGraph(object, self.name)
        elif isinstance(object, ROOT.TH2F):
            wobject = ROOT.WrapperTH2F(object, self.name)
        else:
            raise StandardError('Undefined wrapper for object of class '+str(object.__class__))
        file.Close()
        return wobject
