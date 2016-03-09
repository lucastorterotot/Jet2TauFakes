import ROOT
import copy
from array import array

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

    def __eq__(self,other):
        return  self.name==other.name


class Leaf:
    def __init__(self, name='', file='', object='', vars=[]):
        self.name = name
        self.file = file
        self.object = object
        self.vars = vars
        self.index = 0

    def create(self):
        file = ROOT.TFile.Open(self.file)
        if not file:
            raise StandardError('Cannot open file '+self.file+' for leaf '+self.name)
        object = file.Get(self.object)
        if not object:
            raise StandardError('Cannot load object '+self.object+' for leaf '+self.name)
        ## create wrapper according to object type
        wobject = None
        if isinstance(object, ROOT.TGraph):
            wobject = ROOT.WrapperTGraph(object, self.name)
        elif isinstance(object, ROOT.TH2F):
            wobject = ROOT.WrapperTH2F(object, self.name)
        else:
            raise StandardError('Undefined wrapper for object of class '+str(object.__class__))
        file.Close()
        return wobject

    def __eq__(self,other):
        return  self.name==other.name

class FakeFactor:
    def __init__(self, vars):
        self.fakefactor = ROOT.FakeFactor()
        self.vars = vars
        self.wrapperlist = []
        self.nodelist = []

    def addNode(self, node):
        wrapper = node.create()
        leaves = [self.nodelist.index(l) for l in node.leaves] if isinstance(node, Node) else []
        vars = [self.vars.index(v) for v in node.vars] if isinstance(node, Leaf) else []
        self.fakefactor.addNode(wrapper,
                                len(leaves), array('L', leaves if len(leaves)>0 else [0]),
                                len(vars), array('L', vars if len(vars)>0 else [0])
                               )
        self.wrapperlist.append(wrapper)
        self.nodelist.append(node)

    def value(self, inputs):
        return self.fakefactor.value(len(inputs), array('d', inputs))



def fill(fakefactor, node):
    if isinstance(node, Node):
        for leaf in node.leaves:
            fill(fakefactor, leaf)
        fakefactor.addNode(node)
    elif isinstance(node, Leaf):
        fakefactor.addNode(node)
    else:
        raise StandardError('Incompatible fake factor node/leaf type '+str(node.__class__))
