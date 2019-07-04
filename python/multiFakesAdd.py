from FakesAdd import FakesAdd
import os
import glob
from functools import partial
import multiprocessing as mp

def get_options():
    import os
    import sys
    from optparse import OptionParser
    usage = "usage: %prog [options] <src_dir>"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--cores", dest = "ncores",
                      default=20,
                      help='Number of cores on which to parralelise harvesting')
    parser.add_option("-C", "--channel", dest = "channel",
                      default='tt',
                      help='Channel to process: tt, mt or et')
    parser.add_option("-s", "--systematics", dest = "systematics",
                      default=False,
                      help='Systematics')
    parser.add_option("-g", "--grep", dest = "cut_on_sample_names",
                      default="''",
                      help='Process only samples containing this string.')
    parser.add_option("-d", "--directory", dest = "source_dir",
                      default="''",
                      help='Directory containing samples to process.')
    
    (options,args) = parser.parse_args()
    return options, args

def multithreadmap(f,X,ncores=20, **kwargs):
    """
    multithreading map of a function, default on 20 cpu cores.
    """
    func = partial(f, **kwargs)
    p=mp.Pool(ncores)
    Xout = p.map(func,X)
    p.terminate()
    return(Xout)

options, args = get_options()
subd = [f for f in glob.glob(options.source_dir+'/*') if 'HiggsSUSY' not in f]
files_to_process = ['{}/NtupleProducer/tree.root'.format(f) for f in subd if not os.path.isfile('{}//NtupleProducer/tree_fakes.root'.format(f))]
files_to_process = [f for f in files_to_process if options.cut_on_sample_names in f]

print ''
for tree in files_to_process:
    print tree
start_add_FF = None
while start_add_FF not in ['y','n']:
    start_add_FF = raw_input('Add FF to these trees? [y/n]')
if start_add_FF == 'y':
    print 'Starting to add fake factors.'
    multithreadmap(FakesAdd, files_to_process, ncores=options.ncores, systematics=options.systematics, channel=options.channel)
else:
    print 'Aborting.'
