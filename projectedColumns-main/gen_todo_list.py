import numpy as np
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory's path
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from cloud_util import runs, ions

if __name__ == '__main__':
    find = False
    outfile = 'slurm-9976488.out'
    output = 'todolist_0.6.txt'
    #HM_list = np.arange(0, 5)
    HM_list = [0]
    #HM_list = [-100]
    #redshift_list = [0.1006, 0.5396, 1.053, 2.013, 3.017, 4.895]
    #redshift_list = [0.1006, 0.5396]
    redshift_list = [0.5396]
    #redshift_list = [0.1006]
    #redshift_list = [2.013, 3.017, 4.895]
    run_list = []
    ##add only the 3 different conduction levels
    #runList.append(runs['run1'])
    #runList.append(runs['run2'])
    #runList.append(runs['run3'])
    #runList.append(runs['run4'])
    #runList.append(runs['run5'])
    #runList.append(runs['run6'])
    #runList.append(runs['run11'])
    #runList.append(runs['run12'])
    ##runList.append(runs['run13'])
    ##runList.append(runs['run14'])
    ##runList.append(runs['run15'])
    #runList.append(runs['run16'])
    #runList.append(runs['run17'])
    #runList.append(runs['runx2'])
    #runList.append(runs['runx3'])
    #runList.append(runs['runx4'])
    #runList.append(runs['runx5'])
    #runList.append(runs['runx6'])

    #runList.append(runs['runx8'])
    #runList.append(runs['runx9'])
    #runList.append(runs['runx10'])
    #runList.append(runs['runx11'])
    #runList.append(runs['runx12'])
    #runList.append(runs['runx13'])
    #runList.append(runs['runx14'])
    #runList.append(runs['runx15'])
    #runList.append(runs['runx16'])
    #runList.append(runs['runx17'])
    #runList.append(runs['runy1'])
    #runList.append(runs['runy2'])
    #run_list.append(runs['runz1'])
    #run_list.append(runs['runp1'])
    #run_list.append(runs['runp2'])
    #run_list.append(runs['runp3'])
    #run_list.append(runs['runp4'])
    #run_list.append(runs['runp5'])
    #run_list.append(runs['runp6'])
    #run_list.append(runs['runp7'])
    #run_list.append(runs['runp8'])
    run_list.append(runs['runp9'])
    #run_list.append(runs['runp9b'])
    #run_list.append(runs['runp10'])
    #run_list.append(runs['runp11'])
    #run_list.append(runs['runp12'])
    #run_list.append(runs['runp13'])
    #run_list.append(runs['runp14'])
    #run_list.append(runs['runp15'])
    #run_list.append(runs['runp16'])
    #run_list.append(runs['runp17'])
    #run_list.append(runs['runp18'])

    ion_list = [ion for ion in ions.values()]

    vlist = np.arange(4)
    #vlist = [2]
    #vlist = np.arange(4)
    #vlist = [4, 5]
    #rlist = [1.0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
    rlist = [0.5, 0.0]
    #rlist = [0.5]
    #rlist = [0.0]
    finish_phrase_tempelate = 'finished: %s %d %s %.1f %d %g'
    if find == True:
        with open(outfile) as f:
            lines = [line.strip() for line in f if 'finished' in line]
    
        print('Finished reading: %s' % outfile)

    with open(output, 'w') as out:
        for redshift in redshift_list:
            for run in run_list:
                run_name = run['Name']
                for HM_index in HM_list:
                    #print('Searching: %s, z=%g, HM1e%d' % (run_name, redshift, HM_index))
                    for v in vlist:
                        for ion in ion_list:
                            for r in rlist:
                                finish_phrase = finish_phrase_tempelate % (run_name, HM_index, ion['ion'], r, v, redshift)
                                if find == True:
                                    if finish_phrase not in lines:
                                        out.write(finish_phrase[10:] + '\n')
                                else:
                                    out.write(finish_phrase[10:] + '\n')
