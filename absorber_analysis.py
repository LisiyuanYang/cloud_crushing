import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import os

spectra_file_base = '/nas/astro-th/lyang/projectedColumns-main/spectra23/blob%g/HM_1e%d/spectral_lines_%s/z%g/t%d/'
spectra_file_base_varz = '/nas/astro-th/lyang/projectedColumns-main/spectra23/blob%g_varz/HM_1e%d/spectral_lines_%s/z%g/t%d/'
pixel_list_base = spectra_file_base + 'pixel_list_%d.txt'
absorber_list_base = spectra_file_base + 'absorbers_%s_%d_z%g_%s.txt'
absorber_list_base_tempfloor = spectra_file_base + 'TF%g/absorbers_%s_%d_z%g_%s.txt'
absorber_list_base_tempfloor_denfloor = spectra_file_base + 'TF%g_rho%g/absorbers_%s_%d_z%g_%s.txt'

absorber_list_base_varz = spectra_file_base_varz + 'absorbers_%s_%d_z%g_%s.txt'


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

runz1 = { 'Name':'T0.02_v100_chi20_Z',
         'Formal_name':'T0.02_v100_chi20_Z',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':1.5,
        'tcc':23.7,
        'velocity':100,
        'f_list':['0030', '0039', '0049', '0057'],
        'f_list_full':['%04d' % i for i in range(75)]}

ion1 = {'ion':'O VI',
    'fieldname':'O_p5_number_density',
    'ionfolder': '/OVI/',
    'rest_wave': 1031.91,
    'sigma': 1.1776e-18,
    'massNum': 16.0}
ion2 = {'ion':'C IV',
    'fieldname':'C_p3_number_density',
    'ionfolder': '/CIV/',
    'rest_wave': 1548.18,
    'sigma': 2.5347e-18,
    'massNum': 12.0}
ion3 = {'ion':'N V',
    'fieldname':'N_p4_number_density',
    'ionfolder': '/NV/',
    'rest_wave': 1242.8,
    'sigma': 8.3181e-19,
    'massNum': 14.0}
ion4 = {'ion':'C II',
    'fieldname':'C_p1_number_density',
    'ionfolder': '/CII/',
    'rest_wave': 1335.66,
    'sigma': 1.4555e-19,
    'massNum': 12.0}
ion5 = {'ion': 'Ne VIII',
        'fieldname': 'Ne_p7_number_density',
        'ionfolder':'/NeVIII/',
        'rest_wave': 770.406,
        'sigma': 6.74298e-19,
        'massNum': 20.0}
ion6 = {'ion': 'C III',
        'fieldname': 'C_p2_number_density',
        'ionfolder':'/CIII/',
        'rest_wave': 977.02,
        'sigma': 6.359e-18,
        'massNum': 12.0}
ion7 = {'ion': 'Mg II',
        'fieldname': 'Mg_p1_number_density',
        'ionfolder':'/MgII/',
        'rest_wave': 2796.35,
        'sigma': 6.60717e-21,
        'massNum': 24.0}
ion8 = {'ion': 'Si III',
        'fieldname': 'Si_p2_number_density',
        'ionfolder':'/SiIII/',
        'rest_wave': 1206.5,
        'sigma': 2.2258e-20,
        'massNum': 28.0}
ion9 = {'ion': 'Si IV',
        'fieldname': 'Si_p3_number_density',
        'ionfolder':'/SiIV/',
        'rest_wave': 1393.8,
        'sigma': 3.0694e-18,
        'massNum': 28.0}
ion10 = {'ion': 'H I',
        'fieldname': 'H_p0_number_density',
        'ionfolder':'/HI/',
        'rest_wave': 1215.67,
        'sigma': 4.3394e-18,
        'massNum': 1.0}
ion11 = {'ion': 'H II',
        'fieldname': 'H_p1_number_density',
        'ionfolder':'/HII/',
        'rest_wave': 1215.67,
        #'sigma': 4.3394e-18,
        'massNum': 1.0}
ion12 = {'ion': 'He II',
        'fieldname': 'He_p1_number_density',
        'ionfolder':'/HeII/',
        'rest_wave': 303.918,
        #'sigma': 4.3394e-18,
        'massNum': 4.0}
ion13 = {'ion': 'O IV',
        'fieldname': 'O_p3_number_density',
        'ionfolder':'/OIV/',
        'rest_wave': 787.711,
        #'sigma': 4.3394e-18,
        'massNum': 16.0}
ion14 = {'ion': 'Si II',
        'fieldname': 'Si_p1_number_density',
        'ionfolder':'/SiII/',
        'rest_wave': 1260.422,
        #'sigma': 4.3394e-18,
        'massNum': 28.0}
ion15 = {'ion': 'O VII',
        'fieldname': 'O_p6_number_density',
        'ionfolder':'/OVII/',
        'rest_wave': 21.602,
        #'sigma': 4.3394e-18,
        'massNum': 16.0}
ion16 = {'ion': 'O VIII',
        'fieldname': 'O_p7_number_density',
        'ionfolder':'/OVIII/',
        'rest_wave': 18.969,
        #'sigma': 4.3394e-18,
        'massNum': 16.0}
ion17 = {'ion': 'O I',
        'fieldname': 'O_p0_number_density',
        'ionfolder':'/OI/',
        'rest_wave': 1302.1685,
        #'sigma': 4.3394e-18,
        'massNum': 16.0}
ion18 = {'ion': 'O II',
        'fieldname': 'O_p1_number_density',
        'ionfolder':'/OII/',
        'rest_wave': 834.4655,
        #'sigma': 4.3394e-18,
        'massNum': 16.0}
ion19 = {'ion': 'O III',
        'fieldname': 'O_p2_number_density',
        'ionfolder':'/OIII/',
        'rest_wave': 702.332,
        #'sigma': 4.3394e-18,
        'massNum': 16.0}

runlist = []
##add only the 3 different conduction levels

#runlist.append(run4)    #T0.3_v1000_chi300
runlist.append(runx2)   #T0.3_v1000_chi300_ld2
#runlist.append(run1)   #T0.3_v1000_chi300_cond
runlist.append(runx14)   #T0.3_v1000_chi300_cond_0.1_ld2
#runlist.append(runx8)   #T0.3_v1000_chi300_cond_ld2

#runlist.append(run16)  #T0.3_v1700_chi300
#runlist.append(runx4)   #T0.3_v1700_chi300_ld2
#runlist.append(run11)  #T0.3_v1700_chi300_cond
#runlist.append(runx16)   #T0.3_v1700_chi300_cond_0.1_ld2
#runlist.append(runx10)  #T0.3_v1700_chi300_cond_lds

#runlist.append(run17)  #T0.3_v3000_chi300
#runlist.append(runx5)   #T0.3_v3000_chi300_ld2
#runlist.append(run12)  #T0.3_v3000_chi300_cond
#runlist.append(runx17)   #T0.3_v3000_chi300_cond_0.1_ld2
#runlist.append(runx11)  #T0.3_v3000_chi300_cond_ld2

#runlist.append(run6)   #T1_v1700_chi1000
#runlist.append(runx3)   #T1_v1700_chi1000_ld2
#runlist.append(run3)   #T1_v1700_chi1000_cond
#runlist.append(runx13)   #T1_v1700_chi1000_cond_0.1_ld2
#runlist.append(runx9)   #T1_v1700_chi1000_cond_ld2

#runlist.append(run5)   #T3_v3000_chi3000
#runlist.append(runx6)   #T3_v3000_chi3000_ld2
#runlist.append(run2)   #T3_v3000_chi3000_cond
#runlist.append(runx15)   #T3_v3000_chi3000_cond_0.1_ld2
#runlist.append(runx12)   #T3_v3000_chi3000_cond_ld2

#runlist.append(runy1)   #T0.1_v150_chi100_ld2
#runlist.append(runy2)   #T0.1_v150_chi100_cond_0.1_ld2
#runlist.append(runz1)   #T0.02_v100_chi20_Z

ionlist = []
ionlist.append(ion10)   #H I
##ionlist.append(ion17)   #O I
#ionlist.append(ion7)    #Mg II
##ionlist.append(ion14)   #Si II
##ionlist.append(ion4)    #C II
#ionlist.append(ion18)   #O II
ionlist.append(ion8)    #Si III
#ionlist.append(ion6)    #C III
#ionlist.append(ion19)   #O III
ionlist.append(ion2)    #C IV
#ionlist.append(ion13)   #O IV
ionlist.append(ion1)    #O VI
#ionlist.append(ion5)    #Ne VIII

#colors = ['blue', 'cyan', 'green', 'lime', 'red', 'orange', 'pink']
#colors = ['blue', 'green', 'orange', 'red']
colors = ['blue', 'green', 'red', 'orange', 'brown']
#colors = ['blue', 'green', 'red']
#colors = ['blue', 'red']
#linestyles = [':', '-.', '--', '-']
linestyles = ['-', '--']
#colors = ['red', 'orange']
labels_times = ['t90', 't75', 't50', 't25']
labels_conduction = ['no conduction', 'weak conduction', 'full conduction']
#labels_times = ['t50', 't25', 't20', 't15']
#labels_times = ['t75', 't50', 't25']
#HI_density_range = (12, 21)
HI_density_range = (11, 20)
#density_range = (12, 18)
density_range = (11, 17)
linewidth_range = (0, 100)
linewidth_range_scatter = (0, 50)

width_density_cut = 12
Nbins = 75

dvlim = 10

old_new_conversion = -1.267

def get_absorber_list(run, redshift, HM_index, time_num, direction, ion, blob_cut=0.5, tempfloor=None, denfloor=None, varz=False):
    run_name = run['Name']
    ion_name = ion['ion']
    if tempfloor == None:
        if varz == False:
            absorber_list_file = absorber_list_base % (blob_cut, HM_index, run_name, redshift, time_num, run_name, round(10 * direction), redshift, ion_name.replace(' ', '_'))
        else:
            absorber_list_file = absorber_list_base_varz % (blob_cut, HM_index, run_name, redshift, time_num, run_name, round(10 * direction), redshift, ion_name.replace(' ', '_'))
    elif denfloor == None:
        absorber_list_file = absorber_list_base_tempfloor % (blob_cut, HM_index, run_name, redshift, time_num, tempfloor, run_name, round(10 * direction), redshift, ion_name.replace(' ', '_'))
    else:
        absorber_list_file = absorber_list_base_tempfloor_denfloor % (blob_cut, HM_index, run_name, redshift, time_num, tempfloor, denfloor, run_name, round(10 * direction), redshift, ion_name.replace(' ', '_'))
    #print(absorber_list_file)
    if os.path.getsize(absorber_list_file) > 0:
        pixel_id, absorber_colden, absorber_linewidth, absorber_offset = np.loadtxt(absorber_list_file, unpack=True)
    else:
        pixel_id, absorber_colden, absorber_linewidth, absorber_offset = ([], [], [], [])
    return pixel_id, absorber_colden, absorber_linewidth, absorber_offset

def absorber_distributions(runlist, timelist, redshift, HM_index, direction):
    savepath = 'figures/%s/' % (runlist[0]['Name'])
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        for time_num in timelist:
            log_colden_list_thistime = []
            linewidth_list_thistime = []
            for ion in ionlist:
                ion_name = ion['ion']
                pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
                log_colden_list_thistime.append(np.log10(absorber_colden) + colden_scale_factor)
                linewidth_list_thistime.append(absorber_linewidth)

            log_colden_list_thisrun.append(log_colden_list_thistime)
            linewidth_list_thisrun.append(linewidth_list_thistime)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            for k in range(len(timelist)):
                if 'ld' in run_name:
                    pixel_size = 10
                    area_scale_factor = 1
                else:
                    pixel_size = 2
                    area_scale_factor = 29.3
                weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][k][i])
                if i == 0:
                    binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                    weights /= binsize
                    ax.hist(log_colden_list_allruns[j][k][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[j], linestyle=linestyles[k], label=runlist[j]['Formal_name'] if k == len(timelist) - 1 else None, weights=weights)
                    #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
                else:
                    binsize = (density_range[1] - density_range[0]) / Nbins
                    weights /= binsize
                    _, _, hist_colden = ax.hist(log_colden_list_allruns[j][k][i], bins=Nbins, range=density_range, histtype='step', color=colors[j], linestyle=linestyles[k], label=labels_times[k] if j == 0 else None, weights=weights)
                    #if k == len(timelist) - 1:
                    if j == 0:
                        handles_colden.append(hist_colden[0])
        
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for j in range(len(runlist)):
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            for k in range(len(timelist)):#
                if k % 2 != 0:
                    significant_list = np.where(log_colden_list_allruns[j][k][i] > width_density_cut)[0]
                    #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
                    _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][k][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[j], linestyle=linestyles[k], label=runlist[j]['Formal_name'] if k == len(timelist) - 1 else None)
                    if k == len(timelist) - 1:
                        handles_linewidth.append(hist_linewidth[0])

        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right')

    #plt.tight_layout()
    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'absorber_distributions_%d_z%g.pdf' % (round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def compare_mach(runlist, time_num, redshift, HM_index, direction):
    savepath = 'figures/'
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        if run == runx11:
            continue

        if 'ld' in run['Name']:
            HM_index = 0
            colden_scale_factor = 0
        else:
            HM_index = 2
            colden_scale_factor = old_new_conversion

        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisrun.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thisrun.append(absorber_linewidth)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue

            run_name = runlist[j]['Name']
            
            if 'ld' in run_name:
                pixel_size = 10
                area_scale_factor = 1
            else:
                pixel_size = 2
                area_scale_factor = 29.3

            weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[int(j/2)],\
                         linestyle=linestyles[j%2], weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                log_colden_list_allruns[j][i]
                _, _, hist_colden = ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=density_range, histtype='step', color=colors[int(j/2)],\
                                             linestyle=linestyles[j%2], label=runlist[2 * int(j/2)]['Formal_name'] if j % 2 == 0 else '_none_', weights=weights)
                handles_colden.append(hist_colden[0])
        
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_allruns[j][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[int(j/2)],\
                                           linestyle=linestyles[j%2], label=labels_conduction[j%2] if int(j/2) == 0 else '_none_')
            handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    #plt.tight_layout()
    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'compare_mach_t%d_%d_z%g.pdf' % (time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def show_phew_runs(runlist, time_num, redshift, HM_index, direction):
    savepath = 'figures/'
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:        
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        if run == runx11:
            continue

        #if 'ld' in run['Name']:
        HM_index = 0
        colden_scale_factor = 0

        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisrun.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thisrun.append(absorber_linewidth)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue

            run_name = runlist[j]['Name']
            
            #if 'ld' in run_name:
            pixel_size = 10
            area_scale_factor = 1

            weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[int(j/2)],\
                         linestyle=linestyles[j%2], weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                log_colden_list_allruns[j][i]
                _, _, hist_colden = ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=density_range, histtype='step', color=colors[int(j/2)],\
                                             linestyle=linestyles[j%2], label=runlist[2 * int(j/2)]['Formal_name'] if j % 2 == 0 else '_none_', weights=weights)
                handles_colden.append(hist_colden[0])
        
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_allruns[j][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            if len(significant_list) > 0:
                _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[int(j/2)],\
                                            linestyle=linestyles[j%2], label=labels_conduction[j%2] if int(j/2) == 0 else '_none_')
                handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    #plt.tight_layout()
    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'phew_runs_%s_t%d_%d_z%g.pdf' % (runlist[-1]['Name'], time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def compare_conduction(runlist, time_num, redshift, HM_index, direction):
    savepath = 'figures/'
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        if run == runx11:
            continue

        if 'ld' in run['Name']:
            HM_index = 0
            colden_scale_factor = 0
        else:
            HM_index = 2
            colden_scale_factor = old_new_conversion

        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisrun.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thisrun.append(absorber_linewidth)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue

            run_name = runlist[j]['Name']
            
            if 'ld' in run_name:
                pixel_size = 10
                area_scale_factor = 1
            else:
                pixel_size = 2
                area_scale_factor = 29.3

            weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[j], weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                _, _, hist_colden = ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=density_range, histtype='step', color=colors[j], weights=weights)
                handles_colden.append(hist_colden[0])
        
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_allruns[j][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[j], label=labels_conduction[j])
            handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    #ax = plt.subplot(len(ionlist) + 1, 2, 2 * len(ionlist) + 1)
    #ax.axis('off')
    #ax.legend(handles = handles_colden, fontsize=13, loc='upper right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'compare_conduction_%s_t%d_%d_z%g.pdf' % (runlist[0]['Name'], time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def compare_scaling(runlist, time_num, redshift, direction):
    savepath = 'figures/%s/' % runlist[-1]['Name']
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        if 'ld' in run['Name']:
            HM_index = 0
            colden_scale_factor = 0
        else:
            HM_index = 2
            colden_scale_factor = old_new_conversion

        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisrun.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thisrun.append(absorber_linewidth)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    plt.figure(figsize=(11, 16))
    for i in range(len(ionlist)):
        ion = ionlist[i]

        ax = plt.subplot(len(ionlist) + 1, 2, 2 * i + 1)
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            run_name = runlist[j]['Name']
            if 'ld' in run_name:
                pixel_size = 10
                area_scale_factor = 1
            else:
                pixel_size = 2
                area_scale_factor = 29.3

            weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[j], label=runlist[j]['Formal_name'], weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                _, _, hist_colden = ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=density_range, histtype='step', color=colors[j], label=runlist[j]['Formal_name'], weights=weights)
                handles_colden.append(hist_colden[0])
        
        ax.set_title(ion['ion'], fontsize=13)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
            ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)

        ax = plt.subplot(len(ionlist) + 1, 2, 2 * i + 2)
        for j in range(len(runlist)):
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_allruns[j][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[j])
            handles_linewidth.append(hist_linewidth[0])

        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
            ax.set_ylabel(r'$\mathrm{d}P/\mathrm{d}b$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)

    ax = plt.subplot(len(ionlist) + 1, 2, 2 * len(ionlist) + 2)
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='upper right')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    plt.savefig(savepath + 'compare_scaling_%s_t%d_%d_z%g.pdf' % (runlist[-1]['Name'], time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def compare_directions(runlist, time_num, redshift, HM_index, direction_list):
    savepath = 'figures/%s/' % (runlist[0]['Name'])
    os.makedirs(savepath, exist_ok=True)

    labels_direction = [r'$\theta = %d ^{\circ}$' % round(np.rad2deg(np.arccos(direction))) for direction in direction_list]
    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        for direction in direction_list:
            log_colden_list_thisdirection = []
            linewidth_list_thisdirection = []
            for ion in ionlist:
                ion_name = ion['ion']
                pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
                log_colden_list_thisdirection.append(np.log10(absorber_colden) + colden_scale_factor)
                linewidth_list_thisdirection.append(absorber_linewidth)
            
            log_colden_list_thisrun.append(log_colden_list_thisdirection)
            linewidth_list_thisrun.append(linewidth_list_thisdirection)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            run_name = runlist[j]['Name']
            for k in range(len(direction_list)):
                if 'ld' in run_name:
                    pixel_size = 10
                    area_scale_factor = 1
                else:
                    pixel_size = 2
                    area_scale_factor = 29.3

                weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][k][i])
                if i == 0:
                    binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                    weights /= binsize
                    ax.hist(log_colden_list_allruns[j][k][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[j], lw=0.6, linestyle=linestyles[k], label=run_name, weights=weights)
                    #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
                else:
                    binsize = (density_range[1] - density_range[0]) / Nbins
                    weights /= binsize
                    _, _, hist_colden = ax.hist(log_colden_list_allruns[j][k][i], bins=Nbins, range=density_range, histtype='step', color=colors[j], lw=0.6, linestyle=linestyles[k], label=labels_direction[k], weights=weights)
                    #if k == len(direction_list) - 1:
                    if j == 0:
                        handles_colden.append(hist_colden[0]) #Doing fruitless work unless i = len(ionlist) - 1
        
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for j in range(len(runlist)):
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            for k in range(len(direction_list)):
                if k % 2 != 0:
                    significant_list = np.where(log_colden_list_allruns[j][k][i] > width_density_cut)[0]
                    #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
                    _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][k][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[j], lw=0.6, linestyle=linestyles[k], label=run_name)
                    #if j == 0:
                    if k == len(direction_list) - 1:
                        handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    #plt.tight_layout()
    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'compare_direction_t%d_z%g.pdf' % (time_num, redshift), bbox_inches='tight')
    plt.close()

def compare_chi(runlist, time_num, redshift, HM_index, direction):
    savepath = 'figures/'
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list_allruns = []
    linewidth_list_allruns = []

    for run in runlist:
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        if run == runx11:
            continue

        if 'ld' in run['Name']:
            HM_index = 0
            colden_scale_factor = 0
        else:
            HM_index = 2
            colden_scale_factor = old_new_conversion

        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisrun.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thisrun.append(absorber_linewidth)
        
        log_colden_list_allruns.append(log_colden_list_thisrun)
        linewidth_list_allruns.append(linewidth_list_thisrun)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue

            run_name = runlist[j]['Name']
            
            if 'ld' in run_name:
                pixel_size = 10
                area_scale_factor = 1
            else:
                pixel_size = 2
                area_scale_factor = 29.3

            weights = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_list_allruns[j][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[int(j/2)],\
                         linestyle=linestyles[j%2], weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                log_colden_list_allruns[j][i]
                _, _, hist_colden = ax.hist(log_colden_list_allruns[j][i], bins=Nbins, range=density_range, histtype='step', color=colors[int(j/2)],\
                                             linestyle=linestyles[j%2], label=runlist[2 * int(j/2)]['Formal_name'] if j % 2 == 0 else '_none_', weights=weights)
                handles_colden.append(hist_colden[0])
        
        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for j in range(len(runlist)):
            if runlist[j] == runx11:
                continue
            run_name = runlist[j]['Name']
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_allruns[j][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list_allruns[j][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[int(j/2)],\
                                           linestyle=linestyles[j%2], label=labels_conduction[j%2] if int(j/2) == 0 else '_none_')
            handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'compare_chi_t%d_%d_z%g.pdf' % (time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def compare_redshift(run, time_num, redshift_list, HM_index_list, direction):
    run_name = run['Name']
    savepath = 'figures/%s/' % run_name
    os.makedirs(savepath, exist_ok=True)

    log_colden_list_allzs = []
    linewidth_list_allzs = []

    for i in range(len(redshift_list)):
        redshift = redshift_list[i]
        HM_index = HM_index_list[i]
        #colden_scale_factor = -2/3 * HM_index
        colden_scale_factor = 0

        log_colden_list_thisz = []
        linewidth_list_thisz = []
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisz.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thisz.append(absorber_linewidth)
        
        log_colden_list_allzs.append(log_colden_list_thisz)
        linewidth_list_allzs.append(linewidth_list_thisz)
    
    log_colden_nuv = []
    linewidth_nuv = []
    for ion in ionlist:
        ion_name = ion['ion']
        pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, 0.1006, -100, time_num, direction, ion)
        log_colden_nuv.append(np.log10(absorber_colden) + colden_scale_factor)
        linewidth_nuv.append(absorber_linewidth)
    
    if 'ld' in run_name:
        pixel_size = 10
    else:
        pixel_size = 2

    plt.figure(figsize=(10, 16))
    for i in range(len(ionlist)):
        ion = ionlist[i]

        ax = plt.subplot(len(ionlist) + 1, 2, 2 * i + 1)
        handles_colden = []
        handles_linewidth = []
        for j in range(len(redshift_list)):
            redshift = redshift_list[j]
            weights = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_allzs[j][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_allzs[j][i], bins=Nbins, range=HI_density_range, histtype='step', color=colors[j], label='z=%g' % redshift, weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                _, _, hist_colden = ax.hist(log_colden_list_allzs[j][i], bins=Nbins, range=density_range, histtype='step', color=colors[j], label='z=%g' % redshift, weights=weights)
                handles_colden.append(hist_colden[0])

        weights = pixel_size ** 2 * 10 * np.ones_like(log_colden_nuv[i])
        if i == 0:
            binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
            weights /= binsize
            ax.hist(log_colden_nuv[i], bins=Nbins, range=HI_density_range, histtype='step', color='black', label='zero_background', weights=weights)
            #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
        else:
            binsize = (density_range[1] - density_range[0]) / Nbins
            weights /= binsize
            _, _, hist_colden = ax.hist(log_colden_nuv[i], bins=Nbins, range=density_range, histtype='step', color='black', label='zero_background', weights=weights)
            handles_colden.append(hist_colden[0])

        ax.set_title(ion['ion'], fontsize=13)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
            ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)

        ax = plt.subplot(len(ionlist) + 1, 2, 2 * i + 2)
        for j in range(len(redshift_list)):
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_allzs[j][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list_allzs[j][i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color=colors[j])
            handles_linewidth.append(hist_linewidth[0])
        
        #for j in range(2 * (i % 2), len(time_list)):
        significant_list = np.where(log_colden_nuv[i] > width_density_cut)[0]
        #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
        _, _, hist_linewidth = ax.hist(linewidth_nuv[i][significant_list], bins=Nbins, range=linewidth_range, density=True, histtype='step', color='black')
        handles_linewidth.append(hist_linewidth[0])

        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
            ax.set_ylabel(r'$\mathrm{d}P/\mathrm{d}b$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)

    ax = plt.subplot(len(ionlist) + 1, 2, 2 * len(ionlist) + 2)
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='upper right')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    plt.savefig(savepath + 'compare_redshift_%s_t%d_%d.pdf' % (run['Name'], time_num, round(10 * direction)), bbox_inches='tight')
    plt.close()


def compare_tempfloor_group(runlist, time_num, redshift, HM_index, direction):
    savepath = 'figures/%s/' % runlist[0]['Name']
    os.makedirs(savepath, exist_ok=True)
    
    log_colden_list = []
    linewidth_list = []

    log_colden_list_tempfloor = []
    linewidth_list_tempfloor = []

    log_colden_list_tempfloor_2 = []
    linewidth_list_tempfloor_2 = []

    for run in runlist:
        run_name = run['Name']
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []

        log_colden_list_thisrun_tempfloor = []
        linewidth_list_thisrun_tempfloor = []

        log_colden_list_thisrun_tempfloor_2 = []
        linewidth_list_thisrun_tempfloor_2 = []

        for ion in ionlist:
            ion_name = ion['ion']

            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thisrun.append(np.log10(absorber_colden))
            linewidth_list_thisrun.append(absorber_linewidth)

            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion, 3e4)
            log_colden_list_thisrun_tempfloor.append(np.log10(absorber_colden))
            linewidth_list_thisrun_tempfloor.append(absorber_linewidth)

            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion, 3e4, 3.3e-27)
            log_colden_list_thisrun_tempfloor_2.append(np.log10(absorber_colden))
            linewidth_list_thisrun_tempfloor_2.append(absorber_linewidth)
        
        log_colden_list.append(log_colden_list_thisrun)
        linewidth_list.append(linewidth_list_thisrun)

        log_colden_list_tempfloor.append(log_colden_list_thisrun_tempfloor)
        linewidth_list_tempfloor.append(linewidth_list_thisrun_tempfloor)

        log_colden_list_tempfloor_2.append(log_colden_list_thisrun_tempfloor_2)
        linewidth_list_tempfloor_2.append(linewidth_list_thisrun_tempfloor_2)

    fig = plt.figure(figsize=(10.5, 14))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for k in range(len(runlist)):
            run = runlist[k]

            if 'ld' in run_name:
                pixel_size = 10
            else:
                pixel_size = 2

            weights = pixel_size ** 2 * 10 * np.ones_like(log_colden_list[k][i])
            weights_tempfloor = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_tempfloor[k][i])
            weights_tempfloor_2 = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_tempfloor_2[k][i])

            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                weights_tempfloor /= binsize
                weights_tempfloor_2 /= binsize
                ax.hist(log_colden_list[k][i], bins=Nbins, range=HI_density_range, linestyle=linestyles[k], histtype='step', color='blue', label=r'$T_{\mathrm{f}}=0$', weights=weights)
                ax.hist(log_colden_list_tempfloor[k][i], bins=Nbins, range=HI_density_range, linestyle=linestyles[k], histtype='step', color='red', label=r'$T_{\mathrm{f}}=3\times 10^4$', weights=weights_tempfloor)
                ax.hist(log_colden_list_tempfloor_2[k][i], bins=Nbins, range=HI_density_range, linestyle=linestyles[k], histtype='step', color='green', label=r'low density $T_{\mathrm{f}}$', weights=weights_tempfloor_2)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                weights_tempfloor /= binsize
                weights_tempfloor_2 /= binsize
                _, _, hist_colden = ax.hist(log_colden_list[k][i], bins=Nbins, range=density_range, linestyle=linestyles[k], histtype='step', color='blue', label=r'$T_{\mathrm{f}}=0$' , weights=weights)
                if k == 0:
                    handles_colden.append(hist_colden[0])
                _, _, hist_colden = ax.hist(log_colden_list_tempfloor[k][i], bins=Nbins, range=density_range, linestyle=linestyles[k], histtype='step', color='red', label=r'$T_{\mathrm{f}}=3\times 10^4$', weights=weights_tempfloor)
                if k == 0:
                    handles_colden.append(hist_colden[0])
                _, _, hist_colden = ax.hist(log_colden_list_tempfloor_2[k][i], bins=Nbins, range=density_range, linestyle=linestyles[k], histtype='step', color='green', label=r'low density $T_{\mathrm{f}}$', weights=weights_tempfloor_2)
                if k == 0:
                    handles_colden.append(hist_colden[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for k in range(len(runlist)):
            significant_list = np.where(log_colden_list[k][i] > width_density_cut)[0]
            significant_list_tempfloor = np.where(log_colden_list_tempfloor[k][i] > width_density_cut)[0]
            significant_list_tempfloor_2 = np.where(log_colden_list_tempfloor_2[k][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list[k][i][significant_list], bins=Nbins, range=linewidth_range, linestyle=linestyles[k], label=runlist[k]['Formal_name'], density=True, histtype='step', color='blue')
            ax.hist(linewidth_list_tempfloor[k][i][significant_list_tempfloor], bins=Nbins, range=linewidth_range, linestyle=linestyles[k], density=True, histtype='step', color='red')
            ax.hist(linewidth_list_tempfloor_2[k][i][significant_list_tempfloor_2], bins=Nbins, range=linewidth_range, linestyle=linestyles[k], density=True, histtype='step', color='green')
            handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right', ncol=2)

    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'compare_tempfloor_t%d_%d_z%g.pdf' % (time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def compare_redshift_group(runlist, time_num, redshift_list, HM_index_list, direction):
    savepath = 'figures/%s/' % runlist[0]['Name']
    os.makedirs(savepath, exist_ok=True)
    
    log_colden_list = []
    linewidth_list = []
    log_colden_list_nuv = []
    linewidth_list_nuv = []

    for run in runlist:
        run_name = run['Name']
        log_colden_list_allzs = []
        linewidth_list_allzs = []

        for i in range(len(redshift_list)):
            redshift = redshift_list[i]
            HM_index = HM_index_list[i]
            #colden_scale_factor = -2/3 * HM_index
            colden_scale_factor = 0

            log_colden_list_thisz = []
            linewidth_list_thisz = []
            for ion in ionlist:
                ion_name = ion['ion']
                pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
                log_colden_list_thisz.append(np.log10(absorber_colden) + colden_scale_factor)
                linewidth_list_thisz.append(absorber_linewidth)
            
            log_colden_list_allzs.append(log_colden_list_thisz)
            linewidth_list_allzs.append(linewidth_list_thisz)
        
        log_colden_nuv = []
        linewidth_nuv = []
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, 0.1006, -100, time_num, direction, ion)
            log_colden_nuv.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_nuv.append(absorber_linewidth)

        log_colden_list.append(log_colden_list_allzs)
        linewidth_list.append(linewidth_list_allzs)
        log_colden_list_nuv.append(log_colden_nuv)
        linewidth_list_nuv.append(linewidth_nuv)

    fig = plt.figure(figsize=(10.5, 7))
    nrows = len(ionlist) + 2
    spec = fig.add_gridspec(nrows=nrows, ncols=2, height_ratios = [1, 0.25] + [1] * (nrows - 3) + [1.15])
    for i in range(len(ionlist)):
        ion = ionlist[i]
        if i == 0:
            ax = fig.add_subplot(spec[i, 0])
        else:
            ax = fig.add_subplot(spec[i + 1, 0])
        handles_colden = []
        handles_linewidth = []
        for k in range(len(runlist)):
            run = runlist[k]

            if 'ld' in run_name:
                pixel_size = 10
            else:
                pixel_size = 2

            for j in range(len(redshift_list)):
                redshift = redshift_list[j]
                weights = pixel_size ** 2 * 10 * np.ones_like(log_colden_list[k][j][i])
                if i == 0:
                    binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                    weights /= binsize
                    ax.hist(log_colden_list[k][j][i], bins=Nbins, range=HI_density_range, linestyle=linestyles[k], histtype='step', color=colors[j], label='z=%g' % redshift, weights=weights)
                    #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
                else:
                    binsize = (density_range[1] - density_range[0]) / Nbins
                    weights /= binsize
                    _, _, hist_colden = ax.hist(log_colden_list[k][j][i], bins=Nbins, range=density_range, linestyle=linestyles[k], histtype='step', color=colors[j], label='z=%g' % redshift, weights=weights)
                    if k == 0:
                        handles_colden.append(hist_colden[0])

            weights = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_nuv[k][i])
            if i == 0:
                binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
                weights /= binsize
                ax.hist(log_colden_list_nuv[k][i], bins=Nbins, range=HI_density_range, linestyle=linestyles[k], histtype='step', color='black', label='zero_background', weights=weights)
                #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=Nbins, range=(12, 20), histtype='step', color=colors[j], linestyle=linestyles[k], weights=weights)
            else:
                binsize = (density_range[1] - density_range[0]) / Nbins
                weights /= binsize
                _, _, hist_colden = ax.hist(log_colden_list_nuv[k][i], bins=Nbins, range=density_range, linestyle=linestyles[k], histtype='step', color='black', label='zero_background', weights=weights)
                if k == 0:
                    handles_colden.append(hist_colden[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
        ax.set_ylabel(r'$\log\left(\frac{\mathrm{d}A}{\mathrm{d}\log N}\ /\mathrm{pc^2}\right)$', fontsize=13)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)
        ax.set_yticks([1e4, 1e5, 1e6, 1e7])
        ax.set_yticklabels(['4', '5', '6', '7'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

        if i == 0:
            ax = fig.add_subplot(spec[i, 1])
        else:
            ax = fig.add_subplot(spec[i + 1, 1])
        for k in range(len(runlist)):
            for j in range(len(redshift_list)):
                if j != 2 and j != 4:
                    #for j in range(2 * (i % 2), len(time_list)):
                    significant_list = np.where(log_colden_list[k][j][i] > width_density_cut)[0]
                    #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
                    _, _, hist_linewidth = ax.hist(linewidth_list[k][j][i][significant_list], bins=Nbins, range=linewidth_range, linestyle=linestyles[k], density=True, histtype='step', color=colors[j])
                    #handles_linewidth.append(hist_linewidth[0])
            
            #for j in range(2 * (i % 2), len(time_list)):
            significant_list = np.where(log_colden_list_nuv[k][i] > width_density_cut)[0]
            #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
            _, _, hist_linewidth = ax.hist(linewidth_list_nuv[k][i][significant_list], bins=Nbins, range=linewidth_range, linestyle=linestyles[k], label=runlist[k]['Formal_name'], density=True, histtype='step', color='black')
            handles_linewidth.append(hist_linewidth[0])

        ax.set_title(ion['ion'], fontsize=15, loc='center', y=0.7)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
        ax.set_ylabel(r'$\log(\mathrm{d}P/\mathrm{d}b)$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.minorticks_off()
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)
        ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])
        ax.set_yticklabels(['-4', '-3', '-2', '-1'])
        if i > 1 and i < len(ionlist) - 1:
            ax.set_xticklabels([])
        if i <= 1:
            ax.xaxis.tick_top()

    ax = fig.add_subplot(spec[nrows - 1, 0])
    ax.axis('off')
    ax.legend(handles = handles_linewidth, fontsize=13, loc='lower right')

    ax = fig.add_subplot(spec[nrows - 1, 1])
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='lower right', ncol=2)

    plt.tight_layout(pad=0.01, h_pad=0.01, w_pad=0.01)
    plt.subplots_adjust(wspace=0.2, hspace=0.05)
    plt.savefig(savepath + 'compare_redshift_%s_t%d_%d.pdf' % (runlist[0]['Name'], time_num, round(10 * direction)), bbox_inches='tight')
    plt.close()

def compare_cut(run, time_num, redshift, HM_index, direction):
    run_name = run['Name']
    savepath = 'figures/%s/' % run_name
    os.makedirs(savepath, exist_ok=True)

    log_colden_list_blob = []
    linewidth_list_blob = []
    log_colden_list_varz = []
    linewidth_list_varz = []
    log_colden_list_blob_varz = []
    linewidth_list_blob_varz = []
    for ion in ionlist:
        ion_name = ion['ion']
        pixel_id, absorber_colden_blob, absorber_linewidth_blob, absorber_offset_blob = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
        log_colden_list_blob.append(np.log10(absorber_colden_blob))
        linewidth_list_blob.append(absorber_linewidth_blob)    

        pixel_id, absorber_colden_varz, absorber_linewidth_varz, absorber_offset_varz = get_absorber_list(run, redshift, HM_index, time_num, direction, ion, varz=True, blob_cut=0)
        log_colden_list_varz.append(np.log10(absorber_colden_varz))
        linewidth_list_varz.append(absorber_linewidth_varz)

        pixel_id, absorber_colden_blob_varz, absorber_linewidth_blob_varz, absorber_offset_blob_varz = get_absorber_list(run, redshift, HM_index, time_num, direction, ion, varz=True, blob_cut=0.5)
        log_colden_list_blob_varz.append(np.log10(absorber_colden_blob_varz))
        linewidth_list_blob_varz.append(absorber_linewidth_blob_varz)

    pixel_size = 10
    plt.figure(figsize=(10, 16))
    for i in range(len(ionlist)):
        ion = ionlist[i]

        ax = plt.subplot(len(ionlist) + 1, 2, 2 * i + 1)
        handles_colden = []
        weights_blob = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_blob[i])
        weights_varz = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_varz[i])
        weights_blob_varz = pixel_size ** 2 * 10 * np.ones_like(log_colden_list_blob_varz[i])
        if i == 0:
            binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
            weights_blob /= binsize
            weights_varz /= binsize
            weights_blob_varz /= binsize
            ax.hist(log_colden_list_blob[i], bins=Nbins, range=HI_density_range, histtype='step', color='red', label='blob>0.5', weights=weights_blob)
            ax.hist(log_colden_list_varz[i], bins=Nbins, range=HI_density_range, histtype='step', color='green', label='real Z', weights=weights_varz)
            ax.hist(log_colden_list_blob_varz[i], bins=Nbins, range=HI_density_range, histtype='step', color='blue', label='blob>0.5, real Z', weights=weights_blob_varz)
        else:
            binsize = (density_range[1] - density_range[0]) / Nbins
            weights_blob /= binsize
            weights_varz /= binsize
            weights_blob_varz /= binsize
            _, _, hist_colden = ax.hist(log_colden_list_blob[i], bins=Nbins, range=density_range, histtype='step', color='red', label='blob>0.5', weights=weights_blob)
            handles_colden.append(hist_colden[0])
            _, _, hist_colden = ax.hist(log_colden_list_varz[i], bins=Nbins, range=density_range, histtype='step', color='green', label='real Z', weights=weights_varz)
            handles_colden.append(hist_colden[0])
            _, _, hist_colden = ax.hist(log_colden_list_blob_varz[i], bins=Nbins, range=density_range, histtype='step', color='blue', label='blob>0.5, real Z', weights=weights_blob_varz)
            handles_colden.append(hist_colden[0])
        ax.set_title(ion['ion'], fontsize=13)
        #if i == len(ionlist) - 1:
        #    ax.legend(fontsize=13)
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
            ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)

        ax = plt.subplot(len(ionlist) + 1, 2, 2 * i + 2)
        #for j in range(2 * (i % 2), len(time_list)):
        significant_list_blob = np.where(log_colden_list_blob[i] > width_density_cut)[0]
        significant_list_varz = np.where(log_colden_list_varz[i] > width_density_cut)[0]
        significant_list_blob_varz = np.where(log_colden_list_blob_varz[i] > width_density_cut)[0]
        #weights = 40 / (10 ** colden_scale_factor) * np.ones_like(significant_list)
        if len(significant_list_blob) > 0:
            ax.hist(linewidth_list_blob[i][significant_list_blob], bins=Nbins, range=linewidth_range, density=True, histtype='step', color='red')
        if len(significant_list_varz) > 0:
            ax.hist(linewidth_list_varz[i][significant_list_varz], bins=Nbins, range=linewidth_range, density=True, histtype='step', color='green')
        if len(significant_list_blob_varz) > 0:
            ax.hist(linewidth_list_blob_varz[i][significant_list_blob_varz], bins=Nbins, range=linewidth_range, density=True, histtype='step', color='blue')
        ax.set_yscale('log')
        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
            ax.set_ylabel(r'$\mathrm{d}P/\mathrm{d}b$', fontsize=15)
        #ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log (N\ /\mathrm{pc^2})$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e-4, 7e-1)

    ax = plt.subplot(len(ionlist) + 1, 2, 2 * len(ionlist) + 2)
    ax.axis('off')
    ax.legend(handles = handles_colden, fontsize=13, loc='upper right')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.5)
    plt.savefig(savepath + 'compare_cut_%s_t%d_%d.pdf' % (run['Name'], time_num, round(10 * direction)), bbox_inches='tight')
    plt.close()

def N_b_distribution(run, timelist, redshift, HM_index, direction):
    savepath = 'figures/%s/' % (run['Name'])
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    log_colden_list = []
    linewidth_list = []
    
    for time_num in timelist:
        log_colden_list_thistime = []
        linewidth_list_thistime = []
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden_list_thistime.append(np.log10(absorber_colden) + colden_scale_factor)
            linewidth_list_thistime.append(absorber_linewidth)
        
        log_colden_list.append(log_colden_list_thistime)
        linewidth_list.append(linewidth_list_thistime)
    
    plt.figure(figsize=(20, 7), dpi=300)
    for i in range(len(ionlist)):
        ion = ionlist[i]
        ax = plt.subplot(2, np.ceil(len(ionlist) / 2).astype(int), i + 1)
        for k in range(len(timelist)):
            ax.scatter(log_colden_list[k][i], linewidth_list[k][i], s=1.2, alpha=0.7, c=colors[2 * k], label=labels_times[k] if i == len(ionlist) - 1 else None, rasterized=True)
        ax.set_title(ion['ion'], fontsize=22)
        if i == len(ionlist) - 1:
            ax.legend(fontsize=20)
        
        if i == 0:
            ax.set_xlim(HI_density_range)
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=22)
            ax.set_ylabel(r'$b/\mathrm{km/s}$', fontsize=22)
        else:
            ax.set_xlim(density_range)
        
        ax.set_ylim(linewidth_range_scatter)
        ax.tick_params(axis='both', direction='in', labelsize=20, right=True, top=True)
    
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.2, hspace=0.4)
    plt.savefig(savepath + 'N_b_%d_z%g.pdf' % (round(10 * direction), redshift))
    plt.close()

def match_offset(offset_list_1, offset_list_2, dvlim, index_offset_1=0, index_offset_2=0): #Not the fastest way, but should work anyways
    if len(offset_list_1) == 0 or len(offset_list_2) == 0:
        return []
    
    twin_index_list = []
    
    startpoint_2 = 0
    for i in range(len(offset_list_1)):
        offset_1 = offset_list_1[i]
        for j in range(startpoint_2, len(offset_list_2)):
            offset_2 = offset_list_2[j]
            if abs(offset_1 - offset_2) < dvlim:
                twin_index_list.append([i + index_offset_1, j + index_offset_2])
                startpoint_2 = j + 1
                break
    return twin_index_list

def find_matching_ions(pixel_list_1, pixel_list_2, full_offset_list_1, full_offset_list_2, dvlim):
    matching_index_list = []
    unique_indices = np.unique(pixel_list_1, return_index=True)[1]
    unique_id_1 = pixel_list_1[np.sort(unique_indices)]
    for pixel_id in unique_id_1:
        indices_1 = np.where(pixel_list_1 == pixel_id)[0]
        indices_2 = np.where(pixel_list_2 == pixel_id)[0]
        if len(indices_1) == 0 or len(indices_2) == 0:
            continue
        else:
            offset_list_1 = full_offset_list_1[indices_1]
            offset_list_2 = full_offset_list_2[indices_2]
            matching_indices = match_offset(offset_list_1, offset_list_2, dvlim)
            for i in range(len(matching_indices)):
                matching_index_list.append([indices_1[matching_indices[i][0]], indices_2[matching_indices[i][1]]])
    
    return np.array(matching_index_list)

def find_matching_ions_reverse(pixel_list_1, pixel_list_2, full_offset_list_1, full_offset_list_2, dvlim):
    matching_index_list = []
    unique_indices = np.unique(pixel_list_1, return_index=True)[1]
    unique_id_1 = pixel_list_1[np.sort(unique_indices)]
    for pixel_id in unique_id_1:
        indices_1 = np.where(pixel_list_1 == pixel_id)[0][::-1]
        indices_2 = np.where(pixel_list_2 == pixel_id)[0][::-1]
        if len(indices_1) == 0 or len(indices_2) == 0:
            continue
        else:
            offset_list_1 = full_offset_list_1[indices_1]
            offset_list_2 = full_offset_list_2[indices_2]
            matching_indices = match_offset(offset_list_1, offset_list_2, dvlim)
            for i in range(len(matching_indices)):
                matching_index_list.append([indices_1[matching_indices[i][0]], indices_2[matching_indices[i][1]]])
    
    return np.array(matching_index_list)

def ion_correlation(run, time_num=2, redshift=0.5396, HM_index=2, direction=0.5):
    savepath = 'figures/%s/' % (run['Name'])
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0
    pixel_id_list_1 = []
    log_colden_list_1 = []
    linewidth_list_1 = []
    offset_list_1 = []

    pixel_id_list_2 = []
    log_colden_list_2 = []
    linewidth_list_2 = []
    offset_list_2 = []
    
    for ion in ionlist:
        ion_name = ion['ion']
        pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
        log_colden = np.log10(absorber_colden) + colden_scale_factor
        valid_list_1 = np.where(log_colden > 12)[0]
        log_colden_list_1.append(log_colden[valid_list_1])
        pixel_id_list_1.append(pixel_id[valid_list_1])
        linewidth_list_1.append(absorber_linewidth[valid_list_1])
        offset_list_1.append(absorber_offset[valid_list_1])

        valid_list_2 = np.where(log_colden > 13)[0]
        log_colden_list_2.append(log_colden[valid_list_2])
        pixel_id_list_2.append(pixel_id[valid_list_2])
        linewidth_list_2.append(absorber_linewidth[valid_list_2])
        offset_list_2.append(absorber_offset[valid_list_2])
    
    plt.figure(figsize=(20, 20), dpi=300)
    for i in range(len(ionlist)):
        for j in range(i):
            matching_indices_1 = find_matching_ions(pixel_id_list_1[i], pixel_id_list_1[j], offset_list_1[i], offset_list_1[j], dvlim=10)
            #print(matching_indices)
            reverse_matching_indices_1 = find_matching_ions_reverse(pixel_id_list_1[i], pixel_id_list_1[j], offset_list_1[i], offset_list_1[j], dvlim=10)
            if len(matching_indices_1 > 0):
                matched_colden_i_1 = log_colden_list_1[i][matching_indices_1[:, 0]]
                matched_linewidth_i_1 = linewidth_list_1[i][matching_indices_1[:, 0]]

                matched_colden_j_1 = log_colden_list_1[j][matching_indices_1[:, 1]]
                matched_linewidth_j_1 = linewidth_list_1[j][matching_indices_1[:, 1]]

                reverse_matched_colden_i_1 = log_colden_list_1[i][reverse_matching_indices_1[:, 0]]
                reverse_matched_linewidth_i_1 = linewidth_list_1[i][reverse_matching_indices_1[:, 0]]

                reverse_matched_colden_j_1 = log_colden_list_1[j][reverse_matching_indices_1[:, 1]]
                reverse_matched_linewidth_j_1 = linewidth_list_1[j][reverse_matching_indices_1[:, 1]]

                matched_colden_i_1 = np.concatenate((matched_colden_i_1, reverse_matched_colden_i_1))
                matched_linewidth_i_1 = np.concatenate((matched_linewidth_i_1, reverse_matched_linewidth_i_1))

                matched_colden_j_1 = np.concatenate((matched_colden_j_1, reverse_matched_colden_j_1))
                matched_linewidth_j_1 = np.concatenate((matched_linewidth_j_1, reverse_matched_linewidth_j_1))
            else:
                matched_colden_i_1 = []
                matched_linewidth_i_1 = []
                matched_colden_j_1 = []
                matched_linewidth_j_1 = []
            '''
            matching_indices_2 = find_matching_ions(pixel_id_list_2[i], pixel_id_list_2[j], offset_list_2[i], offset_list_2[j], dvlim=10)
            #print(matching_indices)
            reverse_matching_indices_2 = find_matching_ions_reverse(pixel_id_list_2[i], pixel_id_list_2[j], offset_list_2[i], offset_list_2[j], dvlim=10)
            if len(matching_indices_2 > 0):
                matched_colden_i_2 = log_colden_list_2[i][matching_indices_2[:, 0]]
                matched_linewidth_i_2 = linewidth_list_2[i][matching_indices_2[:, 0]]

                matched_colden_j_2 = log_colden_list_2[j][matching_indices_2[:, 1]]
                matched_linewidth_j_2 = linewidth_list_2[j][matching_indices_2[:, 1]]

                reverse_matched_colden_i_2 = log_colden_list_2[i][reverse_matching_indices_2[:, 0]]
                reverse_matched_linewidth_i_2 = linewidth_list_2[i][reverse_matching_indices_2[:, 0]]

                reverse_matched_colden_j_2 = log_colden_list_2[j][reverse_matching_indices_2[:, 1]]
                reverse_matched_linewidth_j_2 = linewidth_list_2[j][reverse_matching_indices_2[:, 1]]

                matched_colden_i_2 = np.concatenate((matched_colden_i_2, reverse_matched_colden_i_2))
                matched_linewidth_i_2 = np.concatenate((matched_linewidth_i_2, reverse_matched_linewidth_i_2))

                matched_colden_j_2 = np.concatenate((matched_colden_j_2, reverse_matched_colden_j_2))
                matched_linewidth_j_2 = np.concatenate((matched_linewidth_j_2, reverse_matched_linewidth_j_2))
            else:
                matched_colden_i_2 = []
                matched_linewidth_i_2 = []
                matched_colden_j_2 = []
                matched_linewidth_j_2 = []
            '''
            ax = plt.subplot(len(ionlist) - 1, len(ionlist) - 1, (i - 1) * (len(ionlist) - 1) + j + 1)
            ax.scatter(matched_colden_j_1, matched_colden_i_1, s=1.2, alpha=0.7, rasterized=True)
            #ax.scatter(matched_colden_j_2, matched_colden_i_2, s=1.2, alpha=0.7, rasterized=True)

            ax.tick_params(which='both', direction='in', labelsize=18, right=True, top=True)
            if j == 0:
                ax.set_xlim(HI_density_range)
                ax.set_ylabel(r'$\log N(\mathrm{%s})$' % (ionlist[i]['ion']), fontsize=20)
            else:
                ax.set_xlim(density_range)
                ax.axes.yaxis.set_ticklabels([])
            
            ax.set_ylim(density_range)
            if i == len(ionlist) - 1:
                ax.set_xlabel(r'$\log N(\mathrm{%s})$' % (ionlist[j]['ion']), fontsize=20)
            else:
                ax.axes.xaxis.set_ticklabels([])
            
            ax.set_box_aspect(1)

    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    plt.tight_layout()
    plt.savefig(savepath + 'colden_correlation_t%d_%d_z%g.pdf' % (time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

    ref_bj_list = np.arange(linewidth_range_scatter[0], linewidth_range_scatter[1], 1)
    plt.figure(figsize=(20, 20), dpi=300)
    for i in range(len(ionlist)):
        for j in range(i):
            ref_bi_list_1 = ref_bj_list
            ref_bi_list_2 = ref_bj_list * np.sqrt(ionlist[j]['massNum'] / ionlist[i]['massNum'])

            matching_indices_1 = find_matching_ions(pixel_id_list_1[i], pixel_id_list_1[j], offset_list_1[i], offset_list_1[j], dvlim=10)
            #print(matching_indices)
            reverse_matching_indices_1 = find_matching_ions_reverse(pixel_id_list_1[i], pixel_id_list_1[j], offset_list_1[i], offset_list_1[j], dvlim=10)

            if len(matching_indices_1 > 0):
                matched_colden_i_1 = log_colden_list_1[i][matching_indices_1[:, 0]]
                matched_linewidth_i_1 = linewidth_list_1[i][matching_indices_1[:, 0]]

                matched_colden_j_1 = log_colden_list_1[j][matching_indices_1[:, 1]]
                matched_linewidth_j_1 = linewidth_list_1[j][matching_indices_1[:, 1]]

                reverse_matched_colden_i_1 = log_colden_list_1[i][reverse_matching_indices_1[:, 0]]
                reverse_matched_linewidth_i_1 = linewidth_list_1[i][reverse_matching_indices_1[:, 0]]

                reverse_matched_colden_j_1 = log_colden_list_1[j][reverse_matching_indices_1[:, 1]]
                reverse_matched_linewidth_j_1 = linewidth_list_1[j][reverse_matching_indices_1[:, 1]]

                matched_colden_i_1 = np.concatenate((matched_colden_i_1, reverse_matched_colden_i_1))
                matched_linewidth_i_1 = np.concatenate((matched_linewidth_i_1, reverse_matched_linewidth_i_1))

                matched_colden_j_1 = np.concatenate((matched_colden_j_1, reverse_matched_colden_j_1))
                matched_linewidth_j_1 = np.concatenate((matched_linewidth_j_1, reverse_matched_linewidth_j_1))
            else:
                matched_colden_i_1 = []
                matched_linewidth_i_1 = []
                matched_colden_j_1 = []
                matched_linewidth_j_1 = []

            matching_indices_2 = find_matching_ions(pixel_id_list_2[i], pixel_id_list_2[j], offset_list_2[i], offset_list_2[j], dvlim=10)
            #print(matching_indices)
            reverse_matching_indices_2 = find_matching_ions_reverse(pixel_id_list_2[i], pixel_id_list_2[j], offset_list_2[i], offset_list_2[j], dvlim=10)

            if len(matching_indices_2 > 0):
                matched_colden_i_2 = log_colden_list_2[i][matching_indices_2[:, 0]]
                matched_linewidth_i_2 = linewidth_list_2[i][matching_indices_2[:, 0]]

                matched_colden_j_2 = log_colden_list_2[j][matching_indices_2[:, 1]]
                matched_linewidth_j_2 = linewidth_list_2[j][matching_indices_2[:, 1]]

                reverse_matched_colden_i_2 = log_colden_list_2[i][reverse_matching_indices_2[:, 0]]
                reverse_matched_linewidth_i_2 = linewidth_list_2[i][reverse_matching_indices_2[:, 0]]

                reverse_matched_colden_j_2 = log_colden_list_2[j][reverse_matching_indices_2[:, 1]]
                reverse_matched_linewidth_j_2 = linewidth_list_2[j][reverse_matching_indices_2[:, 1]]

                matched_colden_i_2 = np.concatenate((matched_colden_i_2, reverse_matched_colden_i_2))
                matched_linewidth_i_2 = np.concatenate((matched_linewidth_i_2, reverse_matched_linewidth_i_2))

                matched_colden_j_2 = np.concatenate((matched_colden_j_2, reverse_matched_colden_j_2))
                matched_linewidth_j_2 = np.concatenate((matched_linewidth_j_2, reverse_matched_linewidth_j_2))
            else:
                matched_colden_i_2 = []
                matched_linewidth_i_2 = []
                matched_colden_j_2 = []
                matched_linewidth_j_2 = []

            ax = plt.subplot(len(ionlist) - 1, len(ionlist) - 1, (i - 1) * (len(ionlist) - 1) + j + 1)
            ax.scatter(matched_linewidth_j_1, matched_linewidth_i_1, s=1.2, alpha=0.7, rasterized=True)
            ax.scatter(matched_linewidth_j_2, matched_linewidth_i_2, s=1.2, alpha=0.7, rasterized=True)
            ax.plot(ref_bj_list, ref_bi_list_1, lw=1, alpha=0.6, linestyle='--', label='Equal linewidth')
            ax.plot(ref_bj_list, ref_bi_list_2, lw=1, alpha=0.6, linestyle='--', label='Equal temperature')
            ax.tick_params(which='both', direction='in', labelsize=18, right=True, top=True)

            ax.set_xlim(linewidth_range_scatter)
            ax.set_ylim(linewidth_range_scatter)

            if j == 0:
                ax.set_ylabel(r'$b(\mathrm{%s})/km/s$' % (ionlist[i]['ion']), fontsize=20)
                #if i == 1:
                #    ax.legend(fontsize=18)
            else:
                ax.axes.yaxis.set_ticklabels([])
            
            if i == len(ionlist) - 1:
                ax.set_xlabel(r'$b(\mathrm{%s})/km/s$' % (ionlist[j]['ion']), fontsize=20)
            else:
                ax.axes.xaxis.set_ticklabels([])
            
            ax.set_box_aspect(1)

    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    plt.tight_layout()
    plt.savefig(savepath + 'linewidth_correlation_t%d_%d_z%g.pdf' % (time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def ion_correlation_compare_run(runlist, time_num=2, redshift=0.5396, HM_index=0, direction=0.5):
    savepath = 'figures/%s/' % (runlist[0]['Name'])
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0

    pixel_id_list = []
    log_colden_list = []
    linewidth_list = []
    offset_list = []

    for run in runlist:
        pixel_id_list_thisrun = []
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        offset_list_thisrun = []
        
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden = np.log10(absorber_colden) + colden_scale_factor
            valid_list = np.where(log_colden > 12)[0]
            log_colden_list_thisrun.append(log_colden[valid_list])
            pixel_id_list_thisrun.append(pixel_id[valid_list])
            linewidth_list_thisrun.append(absorber_linewidth[valid_list])
            offset_list_thisrun.append(absorber_offset[valid_list])

        pixel_id_list.append(pixel_id_list_thisrun)
        log_colden_list.append(log_colden_list_thisrun)
        linewidth_list.append(linewidth_list_thisrun)
        offset_list.append(offset_list_thisrun)
    
    plt.figure(figsize=(20, 20), dpi=300)
    for i in range(len(ionlist)):
        for j in range(i):
            ax = plt.subplot(len(ionlist) - 1, len(ionlist) - 1, (i - 1) * (len(ionlist) - 1) + j + 1)
            for k in range(len(runlist)):
                matching_indices = find_matching_ions(pixel_id_list[k][i], pixel_id_list[k][j], offset_list[k][i], offset_list[k][j], dvlim=10)
                #print(matching_indices)
                reverse_matching_indices = find_matching_ions_reverse(pixel_id_list[k][i], pixel_id_list[k][j], offset_list[k][i], offset_list[k][j], dvlim=10)
                if len(matching_indices > 0):
                    matched_colden_i = log_colden_list[k][i][matching_indices[:, 0]]
                    matched_linewidth_i = linewidth_list[k][i][matching_indices[:, 0]]

                    matched_colden_j = log_colden_list[k][j][matching_indices[:, 1]]
                    matched_linewidth_j = linewidth_list[k][j][matching_indices[:, 1]]

                    reverse_matched_colden_i = log_colden_list[k][i][reverse_matching_indices[:, 0]]
                    reverse_matched_linewidth_i = linewidth_list[k][i][reverse_matching_indices[:, 0]]

                    reverse_matched_colden_j = log_colden_list[k][j][reverse_matching_indices[:, 1]]
                    reverse_matched_linewidth_j = linewidth_list[k][j][reverse_matching_indices[:, 1]]

                    matched_colden_i = np.concatenate((matched_colden_i, reverse_matched_colden_i))
                    matched_linewidth_i = np.concatenate((matched_linewidth_i, reverse_matched_linewidth_i))

                    matched_colden_j = np.concatenate((matched_colden_j, reverse_matched_colden_j))
                    matched_linewidth_j = np.concatenate((matched_linewidth_j, reverse_matched_linewidth_j))
                else:
                    matched_colden_i = []
                    matched_linewidth_i = []
                    matched_colden_j = []
                    matched_linewidth_j = []
                
                if k % 2:
                    pcolor = 'red'
                else:
                    pcolor = 'blue'
                
                sct = ax.scatter(matched_colden_j, matched_colden_i, c=pcolor, label=runlist[k]['Name'], s=1.2, alpha=0.7, rasterized=True)
                #ax.scatter(matched_colden_j_2, matched_colden_i_2, s=1.2, alpha=0.7, rasterized=True)

                ax.tick_params(which='both', direction='in', labelsize=18, right=True, top=True)
                if j == 0:
                    ax.set_xlim(12, 20)
                    ax.set_ylabel(r'$\log N(\mathrm{%s})$' % (ionlist[i]['ion']), fontsize=20)
                else:
                    ax.set_xlim(12, 16.5)
                    ax.axes.yaxis.set_ticklabels([])
                
                ax.set_ylim(12, 16.5)
                if i == len(ionlist) - 1:
                    ax.set_xlabel(r'$\log N(\mathrm{%s})$' % (ionlist[j]['ion']), fontsize=20)
                else:
                    ax.axes.xaxis.set_ticklabels([])
                
                ax.set_box_aspect(1)
            
    ax = plt.subplot(3, 3, 3)
    for k in range(len(runlist)):
        ax.scatter([], [], s=8, label=runlist[k]['Name'])
    ax.axis('off')
    ax.legend(fontsize=20)

    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    #plt.tight_layout()
    plt.savefig(savepath + 'colden_correlation_%s_t%d_%d_z%g.pdf' % (runlist[0]['Name'], time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

    ref_bj_list = np.arange(linewidth_range_scatter[0], linewidth_range_scatter[1], 1)
    plt.figure(figsize=(20, 20), dpi=300)
    for i in range(len(ionlist)):
        for j in range(i):
            ax = plt.subplot(len(ionlist) - 1, len(ionlist) - 1, (i - 1) * (len(ionlist) - 1) + j + 1)
            for k in range(len(runlist)):
                ref_bi_list_1 = ref_bj_list
                ref_bi_list_2 = ref_bj_list * np.sqrt(ionlist[j]['massNum'] / ionlist[i]['massNum'])

                matching_indices = find_matching_ions(pixel_id_list[k][i], pixel_id_list[k][j], offset_list[k][i], offset_list[k][j], dvlim=10)
                #print(matching_indices)
                reverse_matching_indices = find_matching_ions_reverse(pixel_id_list[k][i], pixel_id_list[k][j], offset_list[k][i], offset_list[k][j], dvlim=10)

                if len(matching_indices > 0):
                    matched_colden_i = log_colden_list[k][i][matching_indices[:, 0]]
                    matched_linewidth_i = linewidth_list[k][i][matching_indices[:, 0]]

                    matched_colden_j = log_colden_list[k][j][matching_indices[:, 1]]
                    matched_linewidth_j = linewidth_list[k][j][matching_indices[:, 1]]

                    reverse_matched_colden_i = log_colden_list[k][i][reverse_matching_indices[:, 0]]
                    reverse_matched_linewidth_i = linewidth_list[k][i][reverse_matching_indices[:, 0]]

                    reverse_matched_colden_j = log_colden_list[k][j][reverse_matching_indices[:, 1]]
                    reverse_matched_linewidth_j = linewidth_list[k][j][reverse_matching_indices[:, 1]]

                    matched_colden_i = np.concatenate((matched_colden_i, reverse_matched_colden_i))
                    matched_linewidth_i = np.concatenate((matched_linewidth_i, reverse_matched_linewidth_i))

                    matched_colden_j = np.concatenate((matched_colden_j, reverse_matched_colden_j))
                    matched_linewidth_j = np.concatenate((matched_linewidth_j, reverse_matched_linewidth_j))
                else:
                    matched_colden_i = []
                    matched_linewidth_i = []
                    matched_colden_j = []
                    matched_linewidth_j = []
                
                if k % 2:
                    pcolor = 'red'
                else:
                    pcolor = 'blue'

                ax.scatter(matched_linewidth_j, matched_linewidth_i, c=pcolor, s=1.2, alpha=0.7, rasterized=True)
                #ax.scatter(matched_linewidth_j_2, matched_linewidth_i_2, s=1.2, alpha=0.7, rasterized=True)
                ax.plot(ref_bj_list, ref_bi_list_1, lw=1, alpha=0.6, linestyle='--', label='Equal linewidth')
                ax.plot(ref_bj_list, ref_bi_list_2, lw=1, alpha=0.6, linestyle='--', label='Equal temperature')
                ax.tick_params(which='both', direction='in', labelsize=20, right=True, top=True)

                ax.set_xlim(linewidth_range_scatter)
                ax.set_ylim(linewidth_range_scatter)

                ax.set_xticks([20, 40])
                ax.set_yticks([0, 20, 40])

                if j == 0:
                    ax.set_ylabel(r'$b(\mathrm{%s})/\mathrm{km/s}$' % (ionlist[i]['ion']), fontsize=20)
                    #if i == 1:
                    #    ax.legend(fontsize=18)
                else:
                    ax.axes.yaxis.set_ticklabels([])
                
                if i == len(ionlist) - 1:
                    ax.set_xlabel(r'$b(\mathrm{%s})/\mathrm{km/s}$' % (ionlist[j]['ion']), fontsize=20)
                else:
                    ax.axes.xaxis.set_ticklabels([])
                
                ax.set_box_aspect(1)
    
    ax = plt.subplot(3, 3, 3)
    for k in range(len(runlist)):
        ax.scatter([], [], s=8, label=runlist[k]['Name'])
    ax.axis('off')
    ax.legend(fontsize=20)

    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    #plt.tight_layout()
    plt.savefig(savepath + 'linewidth_correlation_%s_t%d_%d_z%g.pdf' % (runlist[0]['Name'], time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

def HI_correlation_compare_run(runlist, time_num=2, redshift=0.5396, HM_index=0, direction=0.5):
    savepath = 'figures/%s/' % (runlist[0]['Name'])
    os.makedirs(savepath, exist_ok=True)

    #colden_scale_factor = -2/3 * HM_index
    colden_scale_factor = 0

    pixel_id_list = []
    log_colden_list = []
    linewidth_list = []
    offset_list = []

    for run in runlist:
        pixel_id_list_thisrun = []
        log_colden_list_thisrun = []
        linewidth_list_thisrun = []
        offset_list_thisrun = []
        
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden = np.log10(absorber_colden) + colden_scale_factor
            valid_list = np.where(log_colden > 12)[0]
            log_colden_list_thisrun.append(log_colden[valid_list])
            pixel_id_list_thisrun.append(pixel_id[valid_list])
            linewidth_list_thisrun.append(absorber_linewidth[valid_list])
            offset_list_thisrun.append(absorber_offset[valid_list])

        pixel_id_list.append(pixel_id_list_thisrun)
        log_colden_list.append(log_colden_list_thisrun)
        linewidth_list.append(linewidth_list_thisrun)
        offset_list.append(offset_list_thisrun)

    ref_bHI_list = np.arange(linewidth_range_scatter[0], linewidth_range_scatter[1], 1)
    
    plt.figure(figsize=(20, 5.7), dpi=300)
    for i in range(1, len(ionlist)):
        ax1 = plt.subplot(2, len(ionlist) - 1, i)
        ax2 = plt.subplot(2, len(ionlist) - 1, len(ionlist) - 1 + i)
        for k in range(len(runlist)):
            matching_indices = find_matching_ions(pixel_id_list[k][0], pixel_id_list[k][i], offset_list[k][0], offset_list[k][i], dvlim=10)
            #print(matching_indices)
            reverse_matching_indices = find_matching_ions_reverse(pixel_id_list[k][0], pixel_id_list[k][i], offset_list[k][0], offset_list[k][i], dvlim=10)
            if len(matching_indices > 0):
                matched_colden_HI = log_colden_list[k][0][matching_indices[:, 0]]
                matched_linewidth_HI = linewidth_list[k][0][matching_indices[:, 0]]

                matched_colden_i = log_colden_list[k][i][matching_indices[:, 1]]
                matched_linewidth_i = linewidth_list[k][i][matching_indices[:, 1]]

                reverse_matched_colden_HI = log_colden_list[k][0][reverse_matching_indices[:, 0]]
                reverse_matched_linewidth_HI = linewidth_list[k][0][reverse_matching_indices[:, 0]]

                reverse_matched_colden_i = log_colden_list[k][i][reverse_matching_indices[:, 1]]
                reverse_matched_linewidth_i = linewidth_list[k][i][reverse_matching_indices[:, 1]]

                matched_colden_HI = np.concatenate((matched_colden_HI, reverse_matched_colden_HI))
                matched_linewidth_HI = np.concatenate((matched_linewidth_HI, reverse_matched_linewidth_HI))

                matched_colden_i = np.concatenate((matched_colden_i, reverse_matched_colden_i))
                matched_linewidth_i = np.concatenate((matched_linewidth_i, reverse_matched_linewidth_i))
            else:
                matched_colden_HI = []
                matched_linewidth_HI = []
                matched_colden_i = []
                matched_linewidth_i = []
            
            if k % 2:
                pcolor = 'red'
            else:
                pcolor = 'blue'
            
            sct = ax1.scatter(matched_colden_i, matched_colden_HI, c=pcolor, label=runlist[k]['Name'], s=1.2, alpha=0.7, rasterized=True)
            ax2.scatter(matched_linewidth_i, matched_linewidth_HI, c=pcolor, s=1.2, alpha=0.7, rasterized=True)
            #ax.scatter(matched_colden_j_2, matched_colden_i_2, s=1.2, alpha=0.7, rasterized=True)

        ax1.tick_params(which='both', direction='in', labelsize=18, right=True, top=True)
        ax1.set_xlim(12, 16.5)
        ax1.set_ylim(12, 20)
        ax1.set_xlabel(r'$\log N(\mathrm{%s})$' % (ionlist[i]['ion']), fontsize=20)
        if i == 1:
            ax1.set_ylabel(r'$\log N(\mathrm{HI})$', fontsize=20)
        else:
            ax1.axes.yaxis.set_ticklabels([])
        ax1.set_box_aspect(1)

        ref_bi_list_1 = ref_bHI_list
        ref_bi_list_2 = ref_bHI_list * np.sqrt(ionlist[i]['massNum'])
        ax2.plot(ref_bHI_list, ref_bi_list_1, lw=1, alpha=1, linestyle='--', label='Equal linewidth')
        ax2.plot(ref_bHI_list, ref_bi_list_2, lw=1, alpha=1, linestyle='--', label='Equal temperature')

        ax2.tick_params(which='both', direction='in', labelsize=18, right=True, top=True)
        ax2.set_xlim(linewidth_range_scatter)
        ax2.set_ylim(linewidth_range_scatter)

        ax2.set_xticks([20, 40])
        ax2.set_yticks([0, 20, 40])

        ax2.set_xlabel(r'$b(\mathrm{%s})/\mathrm{km/s}$' % (ionlist[i]['ion']), fontsize=20)
        if i == 1:
            ax2.set_ylabel(r'$b(\mathrm{HI})/\mathrm{km/s}$', fontsize=20)
            #if i == 1:
            #    ax.legend(fontsize=18)
        else:
            ax2.axes.yaxis.set_ticklabels([])                
        ax2.set_box_aspect(1)
    
    #ax = plt.subplot(3, len(ionlist) - 1, 3 * (len(ionlist) - 1))
    #for k in range(len(runlist)):
    #    ax.scatter([], [], s=8, label=runlist[k]['Name'])
    #ax.axis('off')
    #ax.legend(fontsize=20)

    plt.subplots_adjust(hspace=0.5, wspace=0.1)
    #plt.tight_layout()
    plt.savefig(savepath + 'HI_correlation_%s_t%d_%d_z%g.pdf' % (runlist[0]['Name'], time_num, round(10 * direction), redshift), bbox_inches='tight')
    plt.close()

'''
def matching_probability(runlist, time_num=2, redshift=0.5396, HM_index=2, direction=0.5):
    savepath = 'figures/'
    os.makedirs(savepath, exist_ok=True)
    matching_probabilities_list = []
    for run in runlist:
        #colden_scale_factor = -2/3 * HM_index
        colden_scale_factor = 0
        pixel_id_list = []
        log_colden_list = []
        linewidth_list = []
        offset_list = []
        
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden = np.log10(absorber_colden) + colden_scale_factor
            valid_list = np.where(log_colden > 13)[0]
            log_colden_list.append(log_colden[valid_list])
            pixel_id_list.append(pixel_id[valid_list])
            linewidth_list.append(absorber_linewidth[valid_list])
            offset_list.append(absorber_offset[valid_list])
        
        matching_probabilities = np.ones((len(ionlist), len(ionlist)))
    
        for i in range(len(ionlist)):
            for j in range(len(ionlist)):
                if j != i:
                    matching_indices = find_matching_ions(pixel_id_list[i], pixel_id_list[j], offset_list[i], offset_list[j], dvlim=10)
                    #print(matching_indices)
                    reverse_matching_indices = find_matching_ions_reverse(pixel_id_list[i], pixel_id_list[j], offset_list[i], offset_list[j], dvlim=10)

                    matching_probabilities[i, j] = (len(matching_indices[:, 0]) + len(reverse_matching_indices[:, 0])) / (2 * len(pixel_id_list[i]))

        matching_probabilities_list.append(matching_probabilities)

    x_edges = np.arange(len(ionlist) + 1)
    y_edges = np.arange(len(ionlist) + 1)

    x_center = x_edges[:-1] + 0.5
    y_center = y_edges[:-1] + 0.5

    plt.figure(figsize=(24, 8.5))
    for i in range(len(runlist)):
        run = runlist[i]
        ax = plt.subplot(2, 5, i + 1)
        pc = ax.pcolormesh(x_edges, y_edges, matching_probabilities_list[i].T, vmin=0, vmax=1, cmap='jet')
        ax.set_xticks(ticks=x_center, labels=[ion['ion'].replace(' ', '\n') for ion in ionlist], fontsize=19)
        ax.set_yticks(ticks=y_center, labels=[ion['ion'] for ion in ionlist], fontsize=19)
        ax.tick_params(which='both', direction='in', right=True, top=True)
        #if i == 9:
        cb = plt.colorbar(pc)
        cb.ax.tick_params(labelsize=21)
        cb.ax.set_title(r'$P$', fontsize=21)

        ax.set_title('%s' % (runlist[i]['Name']), fontsize=21, loc='right')
        ax.set_box_aspect(1)
    plt.tight_layout()
    plt.savefig(savepath + 'matching_probability.pdf', bbox_inches='tight')
    plt.close()
'''
def matching_probability(runlist, time_num=2, redshift=0.5396, HM_index=0, direction=0.5):
    savepath = 'figures/%s/' % runlist[0]['Name'] 
    os.makedirs(savepath, exist_ok=True)
    matching_probabilities_list = []
    for run in runlist:
        #colden_scale_factor = -2/3 * HM_index
        colden_scale_factor = 0
        pixel_id_list = []
        log_colden_list = []
        linewidth_list = []
        offset_list = []
        
        for ion in ionlist:
            ion_name = ion['ion']
            pixel_id, absorber_colden, absorber_linewidth, absorber_offset = get_absorber_list(run, redshift, HM_index, time_num, direction, ion)
            log_colden = np.log10(absorber_colden) + colden_scale_factor
            valid_list = np.where(log_colden > 12)[0]
            log_colden_list.append(log_colden[valid_list])
            pixel_id_list.append(pixel_id[valid_list])
            linewidth_list.append(absorber_linewidth[valid_list])
            offset_list.append(absorber_offset[valid_list])
        
        matching_probabilities = np.ones((len(ionlist), len(ionlist)))
    
        for i in range(len(ionlist)):
            for j in range(len(ionlist)):
                if j != i:
                    matching_indices = find_matching_ions(pixel_id_list[i], pixel_id_list[j], offset_list[i], offset_list[j], dvlim=10)
                    #print(matching_indices)
                    reverse_matching_indices = find_matching_ions_reverse(pixel_id_list[i], pixel_id_list[j], offset_list[i], offset_list[j], dvlim=10)
                    if len(matching_indices) > 0:
                        matching_probabilities[i, j] = (len(matching_indices[:, 0]) + len(reverse_matching_indices[:, 0])) / (2 * len(pixel_id_list[i]))
                    else:
                        matching_probabilities[i, j] = 0

        matching_probabilities_list.append(matching_probabilities)

    x_edges = np.arange(len(ionlist) + 1)
    y_edges = np.arange(len(ionlist) + 1)

    x_center = x_edges[:-1] + 0.5
    y_center = y_edges[:-1] + 0.5

    fig = plt.figure(figsize=(14.5, 8.5))
    spec = fig.add_gridspec(nrows=2, ncols=4, height_ratios = [1, 1], width_ratios=[1, 1, 1, 0.08])
    for i in range(len(runlist)):
        run = runlist[i]
        ax = fig.add_subplot(spec[i % 2, int(i / 2)])
        pc = ax.pcolormesh(x_edges, y_edges, matching_probabilities_list[i].T, vmin=0, vmax=1, cmap='jet')
        ax.set_xticks(ticks=x_center, labels=[ion['ion'].replace(' ', '\n') for ion in ionlist], fontsize=14)
        ax.set_yticks(ticks=y_center, labels=[ion['ion'] for ion in ionlist], fontsize=14)
        ax.tick_params(which='both', direction='in', right=True, top=True)
        ax.set_title(runlist[i]['Formal_name'], fontsize=14, loc='center', c='red')
        ax.set_box_aspect(1)
    ax = fig.add_subplot(spec[:, 3])
    cb = plt.colorbar(pc, cax=ax)
    cb.ax.tick_params(labelsize=14)
    cb.ax.set_title(r'$P$', fontsize=14)
    plt.subplots_adjust(hspace=0.3, wspace=0.15)
    #plt.tight_layout()
    plt.savefig(savepath + 'matching_probability_%s.pdf' % runlist[0]['Name'], bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    redshift_list = [0.1006, 0.5396, 1.053, 2.013, 4.895]
    #redshift_list = [0.5396]
    #redshift_list = [0.1006, 0.5396]
    HM_list = [0, 0, 0, 0, 0]
    #timelist = [0, 1, 2, 3]
    timelist = [2]
    #timelist = [2, 3, 4, 5]
    #timelist = [1, 2, 3]
    direction = 0.5
    direction_list = [0, 0.5, 0.9, 1]
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    absorber_distributions(runlist, timelist, redshift, HM_index, direction)
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    compare_mach(runlist, 2, redshift, HM_index, direction)
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    show_phew_runs(runlist, 2, redshift, HM_index, direction)
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    compare_conduction(runlist, 2, redshift, HM_index, direction)
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    compare_tempfloor_group(runlist, 2, redshift, HM_index, direction)
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    for time in timelist:
    #        compare_scaling(runlist, time, redshift, direction)
    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    compare_chi(runlist, 2, redshift, HM_index, direction)

    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    compare_directions(runlist, 2, redshift, HM_index, direction_list)

    #for i in range(len(redshift_list)):
    #    redshift = redshift_list[i]
    #    HM_index = HM_list[i]
    #    for run in runlist:
    #        N_b_distribution(run, timelist, redshift, HM_index, direction)

    #for run in runlist:
    #    for time in timelist:
    #        ion_correlation(run, HM_index=0, time_num=time)
    #ion_correlation_compare_run(runlist)
    #HI_correlation_compare_run(runlist, redshift=0.1006)
    #runlist = [run4, run16, run17, run6, run5, run1, run11, run12, run3, run2]
    #runlist = [run4, run6, run5, run1, run3, run2]
    #matching_probability(runlist)
    #for run in runlist:
    #    for time in timelist:
    #        compare_redshift(run, time, redshift_list, HM_list, 0.5)
    #for time in timelist:
    #    compare_cut(runz1, time, 0.5396, 0, 0.5)
    for time in timelist:
        compare_redshift_group(runlist, time, redshift_list, HM_list, 0.5)
