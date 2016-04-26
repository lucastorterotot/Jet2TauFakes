from HTTutilities.Jet2TauFakes.Utilities import Leaf, Node, fill, FakeFactor, replace_nodes
import ROOT
import os

## Meta-data
version = '20160425'
tag     = 'v0.1.3'

# Individual fake factors
ff_qcd_os = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mu_iso'])
ff_qcd_ss = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mu_iso'])
ff_w      = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis', 'mt'])
ff_tt     = FakeFactor(vars=['tau_pt', 'tau_decay', 'mvis'])
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
# Define systematics
qcd_ss_up = replace_nodes(
    qcd_ss, 
    {'ff_qcd_ss':
     Node(
         name='ff_qcd_ss_up',
         formula='(1.+{sys_qcd_up})*{ff_qcd_ss}',
         leaves=[
             Leaf(
                 name='sys_qcd_up',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_QCD_SS_MVis_Iso_up',
                 vars=['mvis', 'mu_iso']
             ),
             qcd_ss.find('ff_qcd_ss')
         ]
     )
    }
)
qcd_ss_down = replace_nodes(
    qcd_ss, 
    {'ff_qcd_ss':
     Node(
         name='ff_qcd_ss_down',
         formula='max(0.,1.-{sys_qcd_down})*{ff_qcd_ss}',
         leaves=[
             Leaf(
                 name='sys_qcd_down',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_QCD_SS_MVis_Iso_down',
                 vars=['mvis', 'mu_iso']
             ),
             qcd_ss.find('ff_qcd_ss')
         ]
     )
    }
)
qcd_os_up = replace_nodes(
    qcd_os, 
    {'ff_qcd_os':
     Node(
         name='ff_qcd_os_up',
         formula='(1.+{sys_qcd_up})*{ff_qcd_os}',
         leaves=[
             Leaf(
                 name='sys_qcd_up',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_QCD_MVis_Iso_SS2OS_up',
                 vars=['mvis', 'mu_iso']
             ),
             qcd_os.find('ff_qcd_os')
         ]
     )
    }
)
qcd_os_down = replace_nodes(
    qcd_os, 
    {'ff_qcd_os':
     Node(
         name='ff_qcd_os_down',
         formula='max(0.,1.-{sys_qcd_down})*{ff_qcd_os}',
         leaves=[
             Leaf(
                 name='sys_qcd_down',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_QCD_MVis_Iso_SS2OS_down',
                 vars=['mvis', 'mu_iso']
             ),
             qcd_os.find('ff_qcd_os')
         ]
     )
    }
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
# Define systematics
w_up = replace_nodes(
    w, 
    {'ff_w':
     Node(
         name='ff_w_up',
         formula='(1.+{sys_w_up})*{ff_w}',
         leaves=[
             Leaf(
                 name='sys_w_up',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_W_MVis_MT_up',
                 vars=['mvis', 'mt']
             ),
             w.find('ff_w')
         ]
     )
    }
)
w_down = replace_nodes(
    w, 
    {'ff_w':
     Node(
         name='ff_w_down',
         formula='max(0.,1.-{sys_w_down})*{ff_w}',
         leaves=[
             Leaf(
                 name='sys_w_down',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_W_MVis_MT_down',
                 vars=['mvis', 'mt']
             ),
             w.find('ff_w')
         ]
     )
    }
)


### TTbar fake factors
tt = Leaf(
    name='ff_tt',
    file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/ff_tt.root'.format(HOME=home,VERSION=version),
    object='c_t_2d',
    vars=['tau_pt','tau_decay']
)
# Define systematics
tt_up = Node(
         name='ff_tt_up',
         formula='(1.+{sys_tt})*{ff_tt}',
         leaves=[
             Leaf(
                 name='sys_tt',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/sys_TT_J_nonclosure_mvis.root'.format(HOME=home,VERSION=version),
                 object='sys',
                 vars=['mvis']
             ),
             tt.find('ff_tt')
         ]
     )
tt_down = Node(
         name='ff_tt_down',
         formula='max(0.,1.-{sys_tt})*{ff_tt}',
         leaves=[
             tt_up.find('sys_tt'),
             tt.find('ff_tt')
         ]
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
# Define systematics
comb_qcd_up = replace_nodes(
    comb, 
    {'ff_qcd_os':
     Node(
         name='ff_qcd_os_up',
         formula='(1.+{sys_qcd_up})*{ff_qcd_os}',
         leaves=[
             Leaf(
                 name='sys_qcd_up',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_QCD_MVis_Iso_SS2OS_up',
                 vars=['mvis', 'mu_iso']
             ),
             comb.find('ff_qcd_os')
         ]
     )
    }
)
comb_qcd_down = replace_nodes(
    comb, 
    {'ff_qcd_os':
     Node(
         name='ff_qcd_os_down',
         formula='max(0.,1.-{sys_qcd_down})*{ff_qcd_os}',
         leaves=[
             Leaf(
                 name='sys_qcd_down',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_QCD_MVis_Iso_SS2OS_down',
                 vars=['mvis', 'mu_iso']
             ),
             comb.find('ff_qcd_os')
         ]
     )
    }
)
comb_w_up = replace_nodes(
    comb, 
    {'ff_w':
     Node(
         name='ff_w_up',
         formula='(1.+{sys_w_up})*{ff_w}',
         leaves=[
             Leaf(
                 name='sys_w_up',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_W_MVis_MT_up',
                 vars=['mvis', 'mt']
             ),
             comb.find('ff_w')
         ]
     )
    }
)
comb_w_down = replace_nodes(
    comb, 
    {'ff_w':
     Node(
         name='ff_w_down',
         formula='max(0.,1.-{sys_w_down})*{ff_w}',
         leaves=[
             Leaf(
                 name='sys_w_down',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/uncertainties_QCD_W.root'.format(HOME=home,VERSION=version),
                 object='uncertainties_W_MVis_MT_down',
                 vars=['mvis', 'mt']
             ),
             comb.find('ff_w')
         ]
     )
    }
)
comb_tt_up = replace_nodes(
    comb, 
    {'ff_tt':
     Node(
         name='ff_tt_up',
         formula='(1.+{sys_tt})*{ff_tt}',
         leaves=[
             Leaf(
                 name='sys_tt',
                 file='{HOME}/public/Htautau/FakeRate/{VERSION}/pieces/sys_TT_J_nonclosure_mvis.root'.format(HOME=home,VERSION=version),
                 object='sys',
                 vars=['mvis']
             ),
             comb.find('ff_tt')
         ]
     )
    }
)
comb_tt_down = replace_nodes(
    comb, 
    {'ff_tt':
     Node(
         name='ff_tt_down',
         formula='max(0.,1.-{sys_tt})*{ff_tt}',
         leaves=[
             comb_tt_up.find('sys_tt'),
             comb.find('ff_tt')
         ]
     )
    }
)


## Fill fake factors
fill(ff_qcd_ss, qcd_ss)
fill(ff_qcd_ss, qcd_ss_up,   sys='ff_qcd_up')
fill(ff_qcd_ss, qcd_ss_down, sys='ff_qcd_down')
fill(ff_qcd_os, qcd_os)
fill(ff_qcd_os, qcd_os_up,   sys='ff_qcd_up')
fill(ff_qcd_os, qcd_os_down, sys='ff_qcd_down')
fill(ff_w     , w)
fill(ff_w, w_up,   sys='ff_w_up')
fill(ff_w, w_down, sys='ff_w_down')
fill(ff_tt    , tt)
fill(ff_tt, tt_up,   sys='ff_tt_up')
fill(ff_tt, tt_down, sys='ff_tt_down')
fill(ff_comb  , comb)
fill(ff_comb, comb_qcd_up,   sys='ff_qcd_up')
fill(ff_comb, comb_qcd_down, sys='ff_qcd_down')
fill(ff_comb, comb_w_up,     sys='ff_w_up')
fill(ff_comb, comb_w_down,   sys='ff_w_down')
fill(ff_comb, comb_tt_up,    sys='ff_tt_up')
fill(ff_comb, comb_tt_down,  sys='ff_tt_down')


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
