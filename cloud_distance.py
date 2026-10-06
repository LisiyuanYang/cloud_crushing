import numpy as np
import yt
from extract_projections import read_colden
import sqlite3
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm

run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Formal_name':'T0.3_v1000_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'conduction':'full',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132'],
        'f_list_full':['0013', '0038', '0080', '0132']}

run2 = { 'Name':'T3_v3000_chi3000_cond',
        'Formal_name':'T3_v3000_chi3000_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'conduction':'full',
        'Mach':3.6,
        'tcc':1.8,
        'velocity':3000,
        'f_list':['0001', '0004', '0007', '0010'],
        'f_list_full':['0001', '0004', '0007', '0010']}

run3 = { 'Name':'T1_v1700_chi1000_cond',
        'Formal_name':'T1_v1700_chi1000_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'conduction':'full',
        'Mach':3.5,
        'tcc':1.8,
        'velocity':1700,
        'f_list':['0002', '0010', '0017', '0028'],
        'f_list_full':['0002', '0010', '0017', '0028']}

run4 = { 'Name':'T0.3_v1000_chi300',
        'Formal_name':'T0.3_v1000_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'conduction':'none',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0025', '0033', '0042', '0058'],
        'f_list_full':['0025', '0033', '0042', '0058']}

run5 = { 'Name':'T3_v3000_chi3000',
        'Formal_name':'T3_v3000_chi3000_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'conduction':'none',
        'Mach':3.6,
        'tcc':1.8,
        'velocity':3000,
        'f_list':['0021', '0030', '0040', '0062'],
        'f_list_full':sorted(set(['%04d' % i for i in range(61)[: : 5]] + ['0021', '0030', '0040', '0062']))}

run6 = { 'Name':'T1_v1700_chi1000',
        'Formal_name':'T1_v1700_chi1000_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'conduction':'none',
        'Mach':3.5,
        'tcc':1.8,
        'velocity':1700,
        'f_list':['0021', '0029', '0038', '0052'],
        'f_list_full':['0021', '0029', '0038', '0052']}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
         'Formal_name':'T0.3_v1700_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'conduction':'full',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078'],
        'f_list_full':['0003', '0020', '0046', '0078']}
    
run12 = { 'Name':'T0.3_v3000_chi300_cond',
         'Formal_name':'T0.3_v3000_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'conduction':'full',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0001', '0004', '0014', '0035'],
        'f_list_full':['0001', '0004', '0014', '0035']}

run16 = { 'Name':'T0.3_v1700_chi300',
         'Formal_name':'T0.3_v1700_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'conduction':'none',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085'],
        'f_list_full':sorted(set(['%04d' % i for i in range(106)[: : 5]] + ['0022', '0032', '0053', '0085']))}

run17 = { 'Name':'T0.3_v3000_chi300',
         'Formal_name':'T0.3_v3000_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'conduction':'none',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0028', '0044', '0065', '0110'],
        'f_list_full':sorted(set(['%04d' % i for i in range(136)[: : 5]] + ['0028', '0044', '0065', '0110']))}

runx2 = { 'Name':'T0.3_v1000_chi300_ld2',
         'Formal_name':'T0.3_v1000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'none',
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0026', '0036', '0057', '0077'],
        'f_list_full':['%04d' % i for i in range(105)]}

runx3 = { 'Name':'T1_v1700_chi1000_ld2',
         'Formal_name':'T1_v1700_chi1000',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'none',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0023', '0033', '0055', '0070'],
        'f_list_full':['%04d' % i for i in range(114)]}

runx4 = { 'Name':'T0.3_v1700_chi300_ld2',
         'Formal_name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'none',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0026', '0031', '0035', '0042', '0051', '0074'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(101)]}

runx5 = { 'Name':'T0.3_v3000_chi300_ld2',
         'Formal_name':'T0.3_v3000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'none',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0022', '0027', '0038', '0080'],
        'f_list_full':['%04d' % i for i in range(82)]}

runx6 = { 'Name':'T3_v3000_chi3000_ld2',
         'Formal_name':'T3_v3000_chi3000',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'none',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0022', '0027', '0032', '0045'],
        'f_list_full':['%04d' % i for i in range(52)]}

'''
runx7 = { 'Name':'T0.3_v3000_chi300_cond_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0017', '0023', '0034', '0079'],
        'f_list_full':['%04d' % i for i in range(7)]}
'''

runx8 = { 'Name':'T0.3_v1000_chi300_cond_ld2',
         'Formal_name':'T0.3_v1000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'full',
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0007', '0011', '0023', '0036'],
        'f_list_full':['%04d' % i for i in range(61)]}

runx9 = { 'Name':'T1_v1700_chi1000_cond_ld2',
         'Formal_name':'T1_v1700_chi1000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'full',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0005', '0006', '0010', '0015'],
        'f_list_full':['%04d' % i for i in range(35)]}

runx10 = { 'Name':'T0.3_v1700_chi300_cond_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'full',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0007', '0010', '0019', '0039'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(75)]}

runx11 = { 'Name':'T0.3_v3000_chi300_cond_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'full',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0007', '0009', '0012', '0013'],
        'f_list_full':['%04d' % i for i in range(20)]}

runx12 = { 'Name':'T3_v3000_chi3000_cond_ld2',
         'Formal_name':'T3_v3000_chi3000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'full',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0003', '0005', '0007', '0010'],
        'f_list_full':['%04d' % i for i in range(31)]}

runx13 = { 'Name':'T1_v1700_chi1000_cond_0.1_ld2',
         'Formal_name':'T1_v1700_chi1000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'weak',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0005', '0010', '0019', '0030'],
        'f_list_full':['%04d' % i for i in range(72)]}

runx14 = { 'Name':'T0.3_v1000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'weak',
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0010', '0026', '0048', '0071'],
        'f_list_full':['%04d' % i for i in range(131)]}

runx15 = { 'Name':'T3_v3000_chi3000_cond_0.1_ld2',
         'Formal_name':'T3_v3000_chi3000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'weak',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0004', '0005', '0010', '0013'],
        'f_list_full':['%04d' % i for i in range(27)]}

runx16 = { 'Name':'T0.3_v1700_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'weak',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0008', '0016', '0046', '0066'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(125)]}

runx17 = { 'Name':'T0.3_v3000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'weak',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0007', '0009', '0013', '0018'],
        'f_list_full':['%04d' % i for i in range(79)]}

runy1 = { 'Name':'T0.1_v150_chi100_ld2',
         'Formal_name':'T0.1_v150_chi100',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'none',
        'Mach':1.0,
        'tcc':35.3,
        'velocity':150,
        'f_list':['0021', '0023', '0031', '0043'],
        'f_list_full':['%04d' % i for i in range(89)]}

runy2 = { 'Name':'T0.1_v150_chi100_cond_0.1_ld2',
         'Formal_name':'T0.1_v150_chi100_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'conduction':'weak',
        'Mach':1.0,
        'tcc':35.3,
        'velocity':150,
        'f_list':['0022', '0030', '0051', '0064'],
        'f_list_full':['%04d' % i for i in range(96)]}

runlist = []
##add only the 3 different conduction levels

#runlist.append(run4)    #T0.3_v1000_chi300
runlist.append(runx2)   #T0.3_v1000_chi300_ld2
#runlist.append(run1)   #T0.3_v1000_chi300_cond
runlist.append(runx14)   #T0.3_v1000_chi300_cond_0.1_ld2
runlist.append(runx8)   #T0.3_v1000_chi300_cond_ld2

#runlist.append(run16)  #T0.3_v1700_chi300
runlist.append(runx4)   #T0.3_v1700_chi300_ld2
#runlist.append(run11)  #T0.3_v1700_chi300_cond
runlist.append(runx16)   #T0.3_v1700_chi300_cond_0.1_ld2
runlist.append(runx10)  #T0.3_v1700_chi300_cond_lds

#runlist.append(run17)  #T0.3_v3000_chi300
runlist.append(runx5)   #T0.3_v3000_chi300_ld2
#runlist.append(run12)  #T0.3_v3000_chi300_cond
runlist.append(runx17)   #T0.3_v3000_chi300_cond_0.1_ld2
runlist.append(runx11)  #T0.3_v3000_chi300_cond_ld2

#runlist.append(run6)   #T1_v1700_chi1000
runlist.append(runx3)   #T1_v1700_chi1000_ld2
#runlist.append(run3)   #T1_v1700_chi1000_cond
runlist.append(runx13)   #T1_v1700_chi1000_cond_0.1_ld2
runlist.append(runx9)   #T1_v1700_chi1000_cond_ld2

#runlist.append(run5)   #T3_v3000_chi3000
runlist.append(runx6)   #T3_v3000_chi3000_ld2
#runlist.append(run2)   #T3_v3000_chi3000_cond
runlist.append(runx15)   #T3_v3000_chi3000_cond_0.1_ld2
runlist.append(runx12)   #T3_v3000_chi3000_cond_ld2

runlist.append(runy1)   #T0.1_v150_chi100_ld2
runlist.append(runy2)   #T0.1_v150_chi100_cond_0.1_ld2


if __name__ == '__main__':
    outfile = 'cloud_distance.txt'
    f = open(outfile, 'w')
    for run in runlist:
        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  run['f_list'][3])
        print(run['Name'], run['f_list'][3])
        current_time = data.current_time
        velocity = yt.units.km / yt.units.s * run['velocity']
        distance = (current_time * velocity).to('kpc').value
        f.write('%s %g\n' % (run['Formal_name'].ljust(28), distance))
    f.close()
