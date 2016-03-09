
#ifndef Jet2TauFakes_WrapperTGraph_h
#define Jet2TauFakes_WrapperTGraph_h

#include "HTTutilities/Jet2TauFakes/interface/IFunctionWrapper.h"

#include "TGraph.h"

class WrapperTGraph : public IFunctionWrapper
{

    public:
        WrapperTGraph():IFunctionWrapper() {};
        WrapperTGraph(const TGraph& g, const std::string& name):IFunctionWrapper(name),m_graph(g) {};
        virtual ~WrapperTGraph();

        double value(size_t size, const double* xs) override
        {
            return (size>0 ? m_graph.Eval(xs[0]) : 0.);
        }
        double value(const std::vector<double>& xs) override
        {
            return value(xs.size(), xs.data());
        }

    private:
        TGraph m_graph;


    //private:
        //ClassDef(WrapperTGraph,1)
};


#endif
