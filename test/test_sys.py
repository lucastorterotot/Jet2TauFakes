from HTTutilities.Jet2TauFakes.Utilities import Leaf, Node, fill, FakeFactor, replace_nodes, print_tree
import ROOT


dir = '/afs/cern.ch/work/j/jsauvan/public/HTauTau/FakeFactors/'

ff_comb = FakeFactor(vars=['tau_pt', 'tau_decay', 'mt', 'mvis'])

## Define nominal fake factor
############################
comb = Node(
    name='ff_comb',
    formula='{frac_qcd}*{ff_qcd}+({frac_w}+{frac_tt}+{frac_zj}+{frac_vv})*{ff_w_corr}',
    leaves=[
        ## Background fractions
        Leaf(
            name='frac_qcd',
            file=dir+'/backgroundFraction_Iso_Medium_mvis_vs_mt.root',
            object='h_backgroundFraction_Iso_Medium_mvis_vs_mt_QCD_Nom',
            vars=['mvis','mt']
        ),
        Leaf(
            name='frac_w',
            file=dir+'/backgroundFraction_Iso_Medium_mvis_vs_mt.root',
            object='h_backgroundFraction_Iso_Medium_mvis_vs_mt_W_Nom',
            vars=['mvis','mt']
        ),
        Leaf(
            name='frac_tt',
            file=dir+'/backgroundFraction_Iso_Medium_mvis_vs_mt.root',
            object='h_backgroundFraction_Iso_Medium_mvis_vs_mt_TT_Nom',
            vars=['mvis','mt']
        ),
        Leaf(
            name='frac_zj',
            file=dir+'/backgroundFraction_Iso_Medium_mvis_vs_mt.root',
            object='h_backgroundFraction_Iso_Medium_mvis_vs_mt_ZJ_Nom',
            vars=['mvis','mt']
        ),
        Leaf(
            name='frac_vv',
            file=dir+'/backgroundFraction_Iso_Medium_mvis_vs_mt.root',
            object='h_backgroundFraction_Iso_Medium_mvis_vs_mt_VV_Nom',
            vars=['mvis','mt']
        ),
        ## QCD and W fake factors
        Leaf(
            name='ff_qcd',
            file=dir+'/FakeFactors_Data_QCDSS_2D.root',
            object='FakeFactors_Data_QCDSS_2D_SS_Iso_Medium_SS_InvertIso_Medium_tau_pt_vs_decayMode',
            vars=['tau_pt','tau_decay']
        ),
        Node(
            name='ff_w_corr',
            formula='{corr_mt}*{ff_w}',
            leaves=[
                Leaf(
                    name='ff_w',
                    file=dir+'/FakeFactors_Data_HighMT_2D.root',
                    object='FakeFactors_Data_HighMT_2D_Iso_Medium_InvertIso_Medium_tau_pt_vs_decayMode',
                    vars=['tau_pt','tau_decay']
                ),
                Leaf(
                    name='corr_mt',
                    file=dir+'/mtCorrections.root',
                    object='mt_correction',
                    vars=['mt']
                )
            ]
        )
    ]
)

#print_tree(comb)

fill(ff_comb, comb)

## Define systematics
############################

comb_sys_nonclosure_qcd = replace_nodes(
    comb, 
    {'ff_qcd':
     Node(
         name='ff_qcd_sys_nonclosure',
         formula='{ff_qcd_nonclosure}*{ff_qcd}',
         leaves=[
             Leaf(
                 name='ff_qcd_nonclosure',
                 file=dir+'/nonClosures.root',
                 object='QCDSS_Histo_Smooth_Ratio',
                 vars=['mvis']
             ),
             comb.find('ff_qcd')
         ]
     )
    }
)


comb_sys_nonclosure_w = replace_nodes(
    comb, 
    {'ff_w_corr':
     Node(
         name='ff_w_corr_sys_nonclosure',
         formula='{ff_w_nonclosure}*{ff_w_corr}',
         leaves=[
             Leaf(
                 name='ff_w_nonclosure',
                 file=dir+'/nonClosures.root',
                 object='HighMT_Histo_Smooth_Ratio',
                 vars=['mvis']
             ),
             comb.find('ff_w_corr')
         ]
     )
    }
)

comb_sys_highmt_stat_up = replace_nodes(
    comb, 
    {'corr_mt':
     Leaf(
         name='corr_mt_stat_up',
         file=dir+'/mtCorrections.root',
         object='mt_correction_statup',
         vars=['mt']
     ),
    }
)
comb_sys_highmt_stat_down = replace_nodes(
    comb, 
    {'corr_mt':
     Leaf(
         name='corr_mt_stat_down',
         file=dir+'/mtCorrections.root',
         object='mt_correction_statdown',
         vars=['mt']
     ),
    }
)

#print_tree(comb_sys_nonclosure_qcd)
#print_tree(comb_sys_nonclosure_w)
#print_tree(comb_sys_highmt_stat_up)


fill(ff_comb, comb_sys_nonclosure_qcd, sys='nonclosure_qcd')
fill(ff_comb, comb_sys_nonclosure_w, sys='nonclosure_w')
fill(ff_comb, comb_sys_highmt_stat_up, sys='highmt_stat_up')
fill(ff_comb, comb_sys_highmt_stat_down, sys='highmt_stat_down')

sys_names = ff_comb.systematics()
print 'List of systematics defined in the fake factor object:'
for s in sys_names:
    print "  '"+s+"'"


## Save fake factors
file = ROOT.TFile.Open("fakeFactor_sys.root", "recreate")
file.WriteObject(ff_comb.fakefactor, "ff_comb")
file.Close()
