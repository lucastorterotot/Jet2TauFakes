
#ifndef Jet2TauFakes_FakeFactor_h
#define Jet2TauFakes_FakeFactor_h

#include "HTT-utilities/Jet2TauFakes/interface/IFunctionWrapper.h"

#include <memory>
#include <vector>
#include <string>


class FakeFactor
{

    public:
        FakeFactor() {};
        virtual ~FakeFactor();

        double value(const std::vector<double>& xs)
        {
            return value(xs, m_nodes.size()-1); // evaluate the root
        }
        bool addNode(IFunctionWrapper*, const std::vector<size_t>&, const std::vector<size_t>&);

    private:
        double value(const std::vector<double>&, size_t);

        std::vector<std::string> m_inputs;

        std::vector<IFunctionWrapper*> m_nodes; // FIXME: raw pointer. Should consider smart pointer
        std::vector<std::vector<size_t>> m_indices;
        std::vector<std::vector<size_t>> m_nodeInputs;


    private:
        ClassDef(FakeFactor,1)
};


#endif
