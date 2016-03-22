
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

#include <iostream>

//ClassImp(FakeFactor)

/*****************************************************************/
FakeFactor::~FakeFactor()
/*****************************************************************/
{
    for(auto fct : m_wrappers)
    {
        delete fct;
    }
}


/*****************************************************************/
double FakeFactor::value(const std::vector<double>& xs, std::vector<WrapperItr>& nodes, std::vector<std::vector<size_t>>& indicesVec, std::vector<std::vector<size_t>>& inputsVec, size_t index)
/*****************************************************************/
{
    // TODO: add xs size check
    const auto& indices = indicesVec[index];
    if(indices.size()>1) // Node
    {
        std::vector<double> values;
        values.reserve(indices.size());
        for(size_t i : indices) values.push_back( value(xs,i) );
        auto& node = *nodes[index];
        //std::cout<<node->name()<<" = "<<node->value(values)<<"\n";
        return node->value(values);
    }
    else // Leaf
    {
        auto& leaf = *nodes[index];
        const auto& inputs = inputsVec[index];
        std::vector<double> xssubset;
        xssubset.reserve(inputs.size());
        for(size_t i : inputs) xssubset.push_back( xs[i] );
        //std::cout<<leaf->name()<<" = "<<leaf->value(xssubset)<<"\n";
        return leaf->value(xssubset);
    }
}


/*****************************************************************/
bool FakeFactor::addNode(WrapperPtr fct, const std::vector<size_t>& sons, const std::vector<size_t>& vars, const std::string& sys)
/*****************************************************************/
{
    if(!fct)
    {
        std::cout<<"[FakeFactor] ERROR: Trying to add a nullptr\n";
        return false;
    }
    auto& sys_nodes = m_nodes.find(sys);
    if(sys_wrapper==m_nodes.end())
    {
        std::cout<<"[FakeFactor] ERROR: Non registered systematic "<<sys<<"\n";
        return false;
    }
    auto& sys_indices = m_indices.find(sys);
    auto& sys_inputs = m_nodeInputs.find(sys);
    // require that the son indices already exist (avoid cycles)
    for(size_t i : sons) 
    {
        if(i>=sys_nodes->second.size())
        {
            std::cout<<"[FakeFactor] ERROR: Trying to add a node with non-existing sons\n";
            return false;
        }
    }
    m_wrappers.push_back(fct);
    sys_nodes->second.push_back(m_wrappers.end()-1);
    sys_indices->second.push_back(sons);
    sys_inputs->second.push_back(vars);
    return true;
}


/*****************************************************************/
bool FakeFactor::replaceNode(const std::string& sys, const std::string& node, WrapperPtr fct, const std::vector<size_t>& sons)
/*****************************************************************/
{
    if(!fct)
    {
        std::cout<<"[FakeFactor] ERROR: Trying to add a nullptr\n";
        return false;
    }
    auto& sys_nodes = m_sysNodes.find(sys);
    if(sys_wrapper==m_sysNodes.end())
    {
        std::cout<<"[FakeFactor] ERROR: Non registered systematic "<<sys<<"\n";
        return false;
    }
    // require that the son indices already exist
    for(size_t i : sons) 
    {
        if(i>=sys_nodes->second.size())
        {
            std::cout<<"[FakeFactor] ERROR: Trying to add a node with non-existing sons\n";
            return false;
        }
    }
}
