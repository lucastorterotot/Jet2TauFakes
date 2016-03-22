
#ifndef Jet2TauFakes_FakeFactor_h
#define Jet2TauFakes_FakeFactor_h

#include "HTTutilities/Jet2TauFakes/interface/IFunctionWrapper.h"

#include <memory>
#include <vector>
#include <string>
#include <map>


class FakeFactor
{
    private:
        // some aliases
        using WrapperPtr = IFunctionWrapper*;
        using WrapperItr = std::vector<WrapperPtr>::iterator;

    public:
        FakeFactor() 
        {
            m_nodes.insert( std::make_pair("", std::vector<WrapperItr>()) );
            m_indices.insert( std::make_pair("", std::vector<std::vector<size_t>>()) );
            m_nodeInputs.insert( std::make_pair("", std::vector<std::vector<size_t>>()) )
        };
        virtual ~FakeFactor();

        double value(size_t size, const double* xs, const std::string& sys="")
        {
            std::vector<double> vxs(xs, xs+size);
            auto& sys_nodes = m_nodes.find(sys);
            if(sys_nodes==m_nodes.end())
            {
                std::cout<<"[FakeFactor] ERROR: Non registered systematic "<<sys<<"\n";
                return 1.;
            }
            auto& sys_indices = m_indices.find(sys);
            auto& sys_inputs = m_inputs.find(sys);
            return value(vxs, sys_nodes->second, sys_indice->second, sys_input->second, sys_nodes->second.size()-1); // evaluate the root
        }
        double value(const std::vector<double>& xs, const std::string& sys="")
        {
            auto& sys_nodes = m_nodes.find(sys);
            if(sys_nodes==m_nodes.end())
            {
                std::cout<<"[FakeFactor] ERROR: Non registered systematic "<<sys<<"\n";
                return 1.;
            }
            auto& sys_indices = m_indices.find(sys);
            auto& sys_inputs = m_inputs.find(sys);
            return value(xs, sys_nodes->second, sys_indice->second, sys_input->second, sys_nodes->second.size()-1); // evaluate the root
        }
        bool addNode(WrapperPtr fct, size_t sonsSize, const size_t* sons, size_t varsSize, const size_t* vars, const std::string& sys="")
        {
            std::vector<size_t> vsons(sons, sons+sonsSize);
            std::vector<size_t> vvars(vars, vars+varsSize);
            return addNode(fct, vsons, vvars, sys);
        }
        bool addNode(WrapperPtr, const std::vector<size_t>&, const std::vector<size_t>&, const std::string& sys="");
        bool replaceNode(const std::string& name, WrapperPtr fct, size_t sonsSize, const size_t* sons, size_t varsSize, const size_t* vars, const std::string& sys="")
        {
            std::vector<size_t> vsons(sons, sons+sonsSize);
            std::vector<size_t> vvars(vars, vars+varsSize);
            return replaceNode(name, fct, vsons, vvars, sys);
        }
        bool replaceNode(const std::string&, WrapperPtr, const std::vector<size_t>&, const std::string& sys="");

        void registerSystematic(const std::string& name)
        {
            // initialize with nominal objects
            m_nodes.insert( std::make_pair(name, m_nodes[""]) );
            m_indices.insert( std::make_pair(name, m_indices[""]) );
            m_nodeInputs.insert( std::make_pair(name, m_nodeInputs[""]) );
        }

    private:
        double value(const std::vector<double>&, std::vector<WrapperItr>&, std::vector<std::vector<size_t>>&, std::vector<std::vector<size_t>>&, size_t);

        std::vector<std::string> m_inputs;

        std::vector<WrapperPtr> m_wrappers; 

        std::map<std::string, std::vector<WrapperItr>> m_nodes;
        std::map<std::string, std::vector<std::vector<size_t>>> m_indices;
        std::map<std::string, std::vector<std::vector<size_t>>> m_nodeInputs;


    //private:
        //ClassDef(FakeFactor,1)
};


#endif
