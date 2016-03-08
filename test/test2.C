
#include <vector>
#include <iostream>
#include "TFile.h"
#include "TSystem.h"
#include "TGraph.h"
#include "TFormula.h"
#include "TH2F.h"

#include "HTTutilities/Jet2TauFakes/interface/WrapperTGraph.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTH2F.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTFormula.h"
#include "HTTutilities/Jet2TauFakes/interface/IFunctionWrapper.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

void test2()
{

    // graph
    std::vector<float> xs = {1,2,3};
    std::vector<float> ys = {1,2,3};
    TGraph g(xs.size(), &xs[0], &ys[0]);
    WrapperTGraph* graph = new WrapperTGraph(g, "graph");

    // histo
    TH2F h("histo","histo",10,0,10, 10,0,10);
    for(int bx=1;bx<=10;bx++)
    {
        double x = h.GetXaxis()->GetBinCenter(bx);
        for(int by=1;by<=10;by++)
        {
            double y = h.GetYaxis()->GetBinCenter(by);
            h.SetBinContent(bx,by, x*y);
        }
    }
    WrapperTH2F* histo = new WrapperTH2F(h, "histo");

    // formula
    TFormula f("form", "x[0]+x[1]");
    WrapperTFormula* form = new WrapperTFormula(f, "form");

    // fake factor
    FakeFactor* factor = new FakeFactor();
    factor->addNode(graph, {}, {0});
    factor->addNode(histo, {}, {1,2});
    factor->addNode(form, {0,1}, {});


    factor->value({2,5.5,5.5});

    TFile* file = TFile::Open("test.root", "recreate");
    file->WriteObject(factor, "ff");
    file->Close();
    std::cout<<"Done\n";

}
