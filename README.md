# Install
## Base install
This has been tested on CMSSW_7_6_3  

`git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes`  
`scram b -j4`   
Add data file :
`git clone data ssh://git@gitlab.cern.ch:7999/cms-htt/Jet2TauFakesFiles.git`

## For HTT analysis
Add the `cmgtools-lite` repository and init the environment. In the CMSSW_BASE/src directory:
```
git clone -o colin git@github.com:cbernet/cmgtools-lite.git -b htt_9_4_11_cand1_v1 CMGTools
cd CMGTools/H2TauTau/
source ./init.sh
```

# Tests
`cd HTTutilities/Jet2TauFakes/test`   

## C++
`root`   
 `.x loadLibrary.C`   
 `.L test2.C`   
 `test2()`   

## Python
Test direct access to fake-factor objects:  
`python test.py`  
Test python utilities for more user-friendly access:  
`python test_utilities.py`  
Test systematic definitions:  
`python test_sys.py` 


