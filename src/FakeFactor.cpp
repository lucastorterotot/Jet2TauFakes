
#include "HTT-utilities/Jet2TauFakes/interface/FakeFactor.h"

#include <iostream>

//ClassImp(FakeFactor)

/*****************************************************************/
FakeFactor::~FakeFactor()
/*****************************************************************/
{
    for(auto fct : m_nodes)
    {
        delete fct;
    }
}


/*****************************************************************/
double FakeFactor::value(const std::vector<double>& xs, size_t index)
/*****************************************************************/
{
    // TODO: add xs size check
    const auto& indices = m_indices[index];
    if(indices.size()>1) // Node
    {
        std::vector<double> values;
        values.reserve(indices.size());
        for(size_t i : indices) values.push_back( value(xs,i) );
        auto& node = m_nodes[index];
        std::cout<<node->name()<<" = "<<node->value(values)<<"\n";
        return node->value(values);
    }
    else // Leaf
    {
        auto& leaf = m_nodes[index];
        const auto& inputs = m_nodeInputs[index];
        std::vector<double> xssubset;
        xssubset.reserve(inputs.size());
        for(size_t i : inputs) xssubset.push_back( xs[i] );
        std::cout<<leaf->name()<<" = "<<leaf->value(xssubset)<<"\n";
        return leaf->value(xssubset);
    }
}


/*****************************************************************/
bool FakeFactor::addNode(IFunctionWrapper* fct, const std::vector<size_t>& sons, const std::vector<size_t>& vars)
/*****************************************************************/
{
    if(!fct)
    {
        std::cout<<"[FakeFactor] ERROR: Trying to add a nullptr\n";
        return false;
    }
    // require that the son indices already exist (avoid cycles)
    for(size_t i : sons) 
    {
        if(i>=m_nodes.size())
        {
            std::cout<<"[FakeFactor] ERROR: Trying to add a node with non-existing sons\n";
            return false;
        }
    }
    m_nodes.push_back(fct);
    m_indices.push_back(sons);
    m_nodeInputs.push_back(vars);
    return true;
}
