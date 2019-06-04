from FakesAdd import FakesAdd
import os
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
                      default='False',
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
os.system('ls {} | grep {} > files.out'.format(options.source_dir, options.cut_on_sample_names))

# Select trees
files_to_process = []
with open('files.out') as f:
    for l in f.readlines():
        command = 'find '+options.source_dir+'/'+l[:-1]+'/'+' -type f -name tree.root'
        files_to_add = os.popen(command).read()[:-1].split('\n')
        files_to_process += files_to_add
os.system('rm files.out')

print ''
for tree in files_to_process:
    print tree
start_add_FF = None
while start_add_FF not in ['y','n']:
    start_add_FF = raw_input('Add FF to this trees? [y/n]')
if start_add_FF == 'y':
    print 'Starting to add fake factors.'
    multithreadmap(FakesAdd, files_to_process, ncores=options.ncores, systematics=options.systematics, channel=options.channel)
else:
    print 'Aborting.'
