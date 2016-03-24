#define G__DICTIONARY

#include "HTTutilities/Jet2TauFakes/interface/IFunctionWrapper.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTFormula.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTGraph.h"
#include "HTTutilities/Jet2TauFakes/interface/WrapperTH2F.h"
#include "HTTutilities/Jet2TauFakes/interface/FakeFactor.h"

#include <map>
#include <vector>
#include <string>


namespace 
{
    struct HTTutilities_Jet2TauFakes 
    {
        IFunctionWrapper ifctw;
        WrapperTGraph wtgr;
        WrapperTFormula wtfo;
        WrapperTH2F wth2f;

        std::map<std::string, std::vector<size_t>> m1;
        std::map<std::string, std::vector<std::vector<size_t>>> m2;

        FakeFactor ff;
    };
}
