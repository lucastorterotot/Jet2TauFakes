# Install
This has been tested on CMSSW_7_6_3  

git clone https://github.com/CMS-HTT/Jet2TauFakes.git HTTutilities/Jet2TauFakes  
scram b -j4   

# Tests
cd HTTutilities/Jet2TauFakes/test   

## C++
root   
 .x loadLibrary.C   
 .L test2.C   
 test2()   

## Python
python test.py  


