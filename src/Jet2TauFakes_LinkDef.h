#include "../interface/IFunctionWrapper.h"
#include "../interface/WrapperTGraph.h"
#include "../interface/WrapperTFormula.h"
#include "../interface/WrapperTH2F.h"
#include "../interface/FakeFactor.h"

#include <memory>

#ifdef __CINT__
#pragma link off all globals;
#pragma link off all classes;
#pragma link off all functions;

#pragma link C++ class IFunctionWrapper+;
//#pragma link C++ class std::unique_ptr<IFunctionWrapper>+;
#pragma link C++ class WrapperTGraph+;
#pragma link C++ class WrapperTFormula+;
#pragma link C++ class WrapperTH2F+;
#pragma link C++ class FakeFactor+;
 

#endif
