from HTTutilities.Jet2TauFakes.Utilities import Leaf, Node, fill, FakeFactor
import ROOT
import os

## Meta-data
version = '20160420'
tag     = '0.1.1'

# Individual fake factors
ff_qcd_os = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mu_iso'])
ff_qcd_ss = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mu_iso'])
ff_w      = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mt'])
ff_tt     = FakeFactor(vars=['tau_pt', 'tau_decay'])
# Combined fake factor
ff_comb   = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mt', 'mu_iso'])


home = os.getenv('HOME')

### QCD fake factors
qcd_ss = Node(
    name='ff_qcd_ss',
    formula='{isocorr_qcd}*{mviscorr_qcd}*{ff_raw_qcd}',
    leaves=[
        Leaf(
            name='ff_raw_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/FakeFactors_Data_QCD_2D.root'.format(HOME=home,VERSION=version),
            object='FakeFactors_Data_QCDSS_2D_SS_Iso_Medium_SS_InvertIso_Medium_tau_pt_vs_decayMode',
            vars=['tau_pt','tau_decay']
        ),
        Leaf(
            name='mviscorr_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/Correction_Data_QCD_MVis.root'.format(HOME=home,VERSION=version),
            object='QCD_SS_MuAnti_Data_FFSSMuAntiData_mvis_correction',
            vars=['mvis']
        ),
        Leaf(
            name='isocorr_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/Correction_Data_QCD_MuIso.root'.format(HOME=home,VERSION=version),
            object='QCD_SS_Data_FFSSMuMediumData_isomu_correction',
            vars=['mu_iso']
        )
    ]
)
#
qcd_os = Node(
    name='ff_qcd_os',
    formula='1.23*{isocorr_qcd}*{mviscorr_qcd}*{ff_raw_qcd}', # SS -> OS correction = 1.23
    leaves=[
        Leaf(
            name='ff_raw_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/FakeFactors_Data_QCD_2D.root'.format(HOME=home,VERSION=version),
            object='FakeFactors_Data_QCDSS_2D_SS_Iso_Medium_SS_InvertIso_Medium_tau_pt_vs_decayMode',
            vars=['tau_pt','tau_decay']
        ),
        Leaf(
            name='mviscorr_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/Correction_Data_QCD_MVis.root'.format(HOME=home,VERSION=version),
            object='QCD_SS_MuAnti_Data_FFSSMuAntiData_mvis_correction',
            vars=['mvis']
        ),
        Leaf(
            name='isocorr_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/Correction_Data_QCD_MuIso.root'.format(HOME=home,VERSION=version),
            object='QCD_SS_Data_FFSSMuMediumData_isomu_correction',
            vars=['mu_iso']
        )
    ]
)

### W fake factors
w = Node(
    name='ff_w',
    formula='{mtcorr_w}*{mviscorr_w}*{ff_raw_w}',
    leaves=[
        Leaf(
            name='ff_raw_w',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/FakeFactors_Data_W_2D.root'.format(HOME=home,VERSION=version),
            object='FakeFactors_Data_HighMT_2D_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode',
            vars=['tau_pt','tau_decay']
        ),
        Leaf(
            name='mviscorr_w',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/Correction_Data_W_MVis.root'.format(HOME=home,VERSION=version),
            object='W_OS_Data_FFOSData_mvis_correction',
            vars=['mvis']
        ),
        Leaf(
            name='mtcorr_w',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/Correction_MC_W_MT.root'.format(HOME=home,VERSION=version),
            object='W_OS_MC_FFOSMC_mt_correction',
            vars=['mt']
        )
    ]
)

### TTbar fake factors
tt = Leaf(
    name='ff_tt',
    file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/ff_tt.root'.format(HOME=home,VERSION=version),
    object='c_t_2d',
    vars=['tau_pt','tau_decay']
)


### Combined fake factors
comb = Node(
    name='ff_comb',
    formula='{frac_tt}*{ff_tt} + ({frac_w}+{frac_dy})*{ff_w} + {frac_qcd}*{ff_qcd_os}',
    leaves=[
        # Individual fake factors
        qcd_os,
        w,
        tt,
        # Fractions
        Leaf(
            name='frac_qcd',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/frac_qcd.root'.format(HOME=home,VERSION=version),
            object='h_w_2d',
            vars=['mt','tau_decay']
        ),
        Leaf(
            name='frac_w',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/frac_wjets.root'.format(HOME=home,VERSION=version),
            object='h_w_2d',
            vars=['mt','tau_decay']
        ),
        Leaf(
            name='frac_dy',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/frac_dy.root'.format(HOME=home,VERSION=version),
            object='h_w_2d',
            vars=['mt','tau_decay']
        ),
        Leaf(
            name='frac_tt',
            file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/frac_tt.root'.format(HOME=home,VERSION=version),
            object='h_w_2d',
            vars=['mt','tau_decay']
        ),
    ]
)



## Fill fake factors
fill(ff_qcd_ss, qcd_ss)
fill(ff_qcd_os, qcd_os)
fill(ff_w     , w)
fill(ff_tt    , tt)
fill(ff_comb  , comb)


file = ROOT.TFile.Open("{HOME}/public/Htautau/FakeRate/{VERSION}/fakeFactors_{VERSION}.root".format(HOME=home,VERSION=version), "recreate")
# Write meta-data
version_ts = ROOT.TString(version)
tag_ts     = ROOT.TString(tag)
file.WriteObject(version_ts , "version")
file.WriteObject(tag_ts     , "tag")
# Write fake factors
file.WriteObject(ff_qcd_ss.fakefactor  , "ff_qcd_ss")
file.WriteObject(ff_qcd_os.fakefactor  , "ff_qcd_os")
file.WriteObject(ff_w.fakefactor       , "ff_w")
file.WriteObject(ff_tt.fakefactor      , "ff_tt")
file.WriteObject(ff_comb.fakefactor    , "ff_comb")
#
file.Close()
