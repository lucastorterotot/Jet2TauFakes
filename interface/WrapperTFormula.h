
#ifndef Jet2TauFakes_WrapperTFormula_h
#define Jet2TauFakes_WrapperTFormula_h

#include "HTT-utilities/Jet2TauFakes/interface/IFunctionWrapper.h"

#include "TFormula.h"

class WrapperTFormula : public IFunctionWrapper
{

    public:
        WrapperTFormula():IFunctionWrapper() {};
        WrapperTFormula(const TFormula& f, const std::string& name):IFunctionWrapper(name),m_formula(f) {};
        virtual ~WrapperTFormula();

        double value(const std::vector<double>& xs) override
        {
            return m_formula.EvalPar(&xs[0]);
        }

    private:
        TFormula m_formula;


    private:
        ClassDef(WrapperTFormula,1)
};


#endif
