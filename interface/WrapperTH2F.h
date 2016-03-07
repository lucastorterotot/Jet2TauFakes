
#ifndef Jet2TauFakes_WrapperTH2F_h
#define Jet2TauFakes_WrapperTH2F_h

#include "HTT-utilities/Jet2TauFakes/interface/IFunctionWrapper.h"

#include "TH2F.h"

class WrapperTH2F : public IFunctionWrapper
{

    public:
        WrapperTH2F():IFunctionWrapper() {};
        WrapperTH2F(const TH2F& h, const std::string& name):IFunctionWrapper(name),m_histo(h) {};
        virtual ~WrapperTH2F();

        double value(const std::vector<double>& xs) override
        {
            if(xs.size()<2) return 0.;
            // FIXME: don't use overflow bins
            int bx = m_histo.GetXaxis()->FindBin(xs[0]);
            int by = m_histo.GetYaxis()->FindBin(xs[1]);
            return m_histo.GetBinContent(bx,by);
        }

    private:
        TH2F m_histo;


    private:
        ClassDef(WrapperTH2F,1)
};


#endif
