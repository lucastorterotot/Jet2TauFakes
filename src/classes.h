#define G__DICTIONARY

#include "HTTutilities/Jet2TauFakes/interface/IFunctionWrapper.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTFormula.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTGraph.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTH2F.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"




namespace 
{
    struct HTTutilities_Jet2TauFakes 
    {
        IFunctionWrapper ifctw;
        WrapperTGraph wtgr;
        WrapperTFormula wtfo;
        WrapperTH2F wth2f;
        FakeFactor ff;
    };
}
