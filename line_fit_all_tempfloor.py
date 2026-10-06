import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
from contextlib import redirect_stderr
import sys
import os
import logging
from mpi4py import MPI
import yt
import trident
from trident.absorption_spectrum.absorption_spectrum_fit import generate_total_fit

#logging.getLogger("yt").setLevel(logging.WARNING)
#logging.getLogger("trident").setLevel(logging.WARNING)


comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank   = comm.Get_rank()

#ionTable_base = '/work/pi_nsk_umass_edu/lyang/newTridentTables/HM_shu/hm-1e%d-z%g/HM_1e%d.h5'
ionTable_base = '/work/pi_nsk_umass_edu/lyang/newTridentTables/Cloudy23/hm-1e%d-z%g/HM_1e%d.h5'
blob_colden_file_base = '/nas/astro-th/lyang/nonSorted_ColDen_23/blob0.5/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'

ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])
ion_indices = np.array([0, 10, 4, 6, 9]) #HI, Mg II, C IV, O VI, Ne VIII; indices in the colden files
np.set_printoptions(linewidth=np.inf)
tempfloor = 3e4
denfloor = 3.3e-27


run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Formal_name':'T0.3_v1000_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132'],
        'f_list_full':['0013', '0038', '0080', '0132']}

run2 = { 'Name':'T3_v3000_chi3000_cond',
        'Formal_name':'T3_v3000_chi3000_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.6,
        'tcc':1.8,
        'velocity':3000,
        'f_list':['0001', '0004', '0007', '0010'],
        'f_list_full':['0001', '0004', '0007', '0010']}

run3 = { 'Name':'T1_v1700_chi1000_cond',
        'Formal_name':'T1_v1700_chi1000_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.5,
        'tcc':1.8,
        'velocity':1700,
        'f_list':['0002', '0010', '0017', '0028'],
        'f_list_full':['0002', '0010', '0017', '0028']}

run4 = { 'Name':'T0.3_v1000_chi300',
        'Formal_name':'T0.3_v1000_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0025', '0033', '0042', '0058'],
        'f_list_full':['0025', '0033', '0042', '0058']}

run5 = { 'Name':'T3_v3000_chi3000',
        'Formal_name':'T3_v3000_chi3000_hcol',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.6,
    'tcc':1.8,
    'velocity':3000,
    'f_list':['0021', '0030', '0040', '0062'],
    'f_list_full':sorted(set(['%04d' % i for i in range(61)[: : 5]] + ['0021', '0030', '0040', '0062']))}

run6 = { 'Name':'T1_v1700_chi1000',
        'Formal_name':'T1_v1700_chi1000_hcol',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.5,
    'tcc':1.8,
    'velocity':1700,
    'f_list':['0021', '0029', '0038', '0052'],
    'f_list_full':['0021', '0029', '0038', '0052']}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
         'Formal_name':'T0.3_v1700_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078'],
        'f_list_full':['0003', '0020', '0046', '0078']}
    
run12 = { 'Name':'T0.3_v3000_chi300_cond',
         'Formal_name':'T0.3_v3000_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0001', '0004', '0014', '0035'],
        'f_list_full':['0001', '0004', '0014', '0035']}

run16 = { 'Name':'T0.3_v1700_chi300',
         'Formal_name':'T0.3_v1700_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085'],
        'f_list_full':sorted(set(['%04d' % i for i in range(106)[: : 5]] + ['0022', '0032', '0053', '0085']))}

run17 = { 'Name':'T0.3_v3000_chi300',
         'Formal_name':'T0.3_v3000_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0028', '0044', '0065', '0110'],
        'f_list_full':sorted(set(['%04d' % i for i in range(136)[: : 5]] + ['0028', '0044', '0065', '0110']))}

runx2 = { 'Name':'T0.3_v1000_chi300_ld2',
         'Formal_name':'T0.3_v1000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0026', '0036', '0057', '0077'],
        'f_list_full':['%04d' % i for i in range(105)]}

runx3 = { 'Name':'T1_v1700_chi1000_ld2',
         'Formal_name':'T1_v1700_chi1000',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0023', '0033', '0055', '0070'],
        'f_list_full':['%04d' % i for i in range(114)]}

runx4 = { 'Name':'T0.3_v1700_chi300_ld2',
         'Formal_name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0026', '0031', '0035', '0042', '0051', '0074'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(101)]}

runx5 = { 'Name':'T0.3_v3000_chi300_ld2',
         'Formal_name':'T0.3_v3000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0022', '0027', '0038', '0080'],
        'f_list_full':['%04d' % i for i in range(82)]}

runx6 = { 'Name':'T3_v3000_chi3000_ld2',
         'Formal_name':'T3_v3000_chi3000',
        'Dir':'/nas/astro-th/lyang/',
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
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0007', '0011', '0023', '0036'],
        'f_list_full':['%04d' % i for i in range(61)]}

runx9 = { 'Name':'T1_v1700_chi1000_cond_ld2',
         'Formal_name':'T1_v1700_chi1000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0005', '0006', '0010', '0015'],
        'f_list_full':['%04d' % i for i in range(35)]}

runx10 = { 'Name':'T0.3_v1700_chi300_cond_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0007', '0010', '0019', '0039'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(75)]}

runx11 = { 'Name':'T0.3_v3000_chi300_cond_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0007', '0009', '0012', '0013'],
        'f_list_full':['%04d' % i for i in range(20)]}

runx12 = { 'Name':'T3_v3000_chi3000_cond_ld2',
         'Formal_name':'T3_v3000_chi3000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0003', '0005', '0007', '0010'],
        'f_list_full':['%04d' % i for i in range(31)]}

runx13 = { 'Name':'T1_v1700_chi1000_cond_0.1_ld2',
         'Formal_name':'T1_v1700_chi1000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0005', '0010', '0019', '0030'],
        'f_list_full':['%04d' % i for i in range(72)]}

runx14 = { 'Name':'T0.3_v1000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0010', '0026', '0048', '0071'],
        'f_list_full':['%04d' % i for i in range(131)]}

runx15 = { 'Name':'T3_v3000_chi3000_cond_0.1_ld2',
         'Formal_name':'T3_v3000_chi3000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0004', '0005', '0010', '0013'],
        'f_list_full':['%04d' % i for i in range(27)]}

runx16 = { 'Name':'T0.3_v1700_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0008', '0016', '0046', '0066'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(125)]}

runx17 = { 'Name':'T0.3_v3000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0007', '0009', '0013', '0018'],
        'f_list_full':['%04d' % i for i in range(79)]}

runy1 = { 'Name':'T0.1_v150_chi100_ld2',
         'Formal_name':'T0.1_v150_chi100',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':1.0,
        'tcc':35.3,
        'velocity':150,
        'f_list':['0021', '0023', '0031', '0043'],
        'f_list_full':['%04d' % i for i in range(89)]}

runy2 = { 'Name':'T0.1_v150_chi100_cond_0.1_ld2',
         'Formal_name':'T0.1_v150_chi100_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':1.0,
        'tcc':35.3,
        'velocity':150,
        'f_list':['0022', '0030', '0051', '0064'],
        'f_list_full':['%04d' % i for i in range(96)]}

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

#add the runs to the list that will have columns ranked
runlist = []
##add only the 3 different conduction levels
#runlist.append(run4)    #T0.3_v1000_chi300
#runlist.append(runx2)   #T0.3_v1000_chi300_ld2
#runlist.append(run1)   #T0.3_v1000_chi300_cond
#runlist.append(runx14)   #T0.3_v1000_chi300_cond_0.1_ld2
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

runlist.append(runy1)   #T0.1_v150_chi100_ld2
runlist.append(runy2)   #T0.1_v150_chi100_cond_0.1_ld2


ionlist = []
ionlist.append(ion10)   #H I
ionlist.append(ion17)   #O I
ionlist.append(ion7)    #Mg II
ionlist.append(ion14)   #Si II
ionlist.append(ion4)    #C II
ionlist.append(ion8)    #Si III
ionlist.append(ion18)   #O II
ionlist.append(ion9)    #Si IV
ionlist.append(ion6)    #C III
ionlist.append(ion19)   #O III
ionlist.append(ion2)    #C IV
ionlist.append(ion13)   #O IV
ionlist.append(ion1)    #O VI
ionlist.append(ion5)    #Ne VIII

ldb = trident.LineDatabase('lines.txt')
lines = ldb.parse_subset(['%s %d' % (ion['ion'], round(ion['rest_wave'])) for ion in ionlist])

def _metallicity(field, data):
    factor = 1.0 # 1.0 solar metallicity
    return (
        data.ds.arr(np.ones_like(data["gas", "density"]), 'Zsun') * factor
    )

def _altTemp(field, data):
    temp = data['temperature']
    den = data['density']
    lowtemps = np.where((temp < tempfloor) & (den < denfloor))[0]
    temp[lowtemps] = tempfloor   #sets all temps below tempfloor to tempfloor
    return temp

def _gas_blob(field, data):
    return data['flash', 'blob']

def ravel_map(indices, unravelled_map, Npix_x, Npix_y):
    if max(indices) >= Npix_x * Npix_y:
        print('Error! Index %d out of range for a %d * %d map.' % (max(indices), Npix_x, Npix_y))
        sys.stdout.flush()
        sys.exit(1)
    
    if len(indices) != len(unravelled_map):
        print('Error! Size of indices list must equal size of unravelled map.')
        sys.stdout.flush()
        sys.exit(1)

    indices = np.array(indices, dtype=int)
    Npix_x = int(Npix_x)
    Npix_y = int(Npix_y)

    ravelled_map = np.zeros((Npix_x, Npix_y))
    indices_x = np.floor_divide(indices, Npix_x)
    indices_y = indices % Npix_x
    ravelled_map[indices_x, indices_y] = unravelled_map
    return ravelled_map

def deproject(projected_coord, angle):
    return np.array([-projected_coord[0] * np.cos(angle), projected_coord[0] * np.sin(angle), projected_coord[1]])

def get_all_pixels(run, redshift, timenum, direction, HM_index):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, 0, 0.5396, timenum, run_name, round(10 * direction))
    pixel_indices = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',', usecols=0)
    pixel_indices = pixel_indices.astype(int)
    return pixel_indices

def choose_random_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(np.any(colden[:, 1:] > 3e12, axis=1))[0]

    rng = np.random.default_rng(seed = pixel_indices[10])
    return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)

def choose_OVI_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(colden[:, 3] > 1e13)[0]
    if len(valid_pixels) > Npixels:
        rng = np.random.default_rng(seed = pixel_indices[20])
        return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)
    else:
        return pixel_indices[valid_pixels]

def choose_MgII_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(colden[:, 1] > 1e13)[0]
    if len(valid_pixels) > Npixels:
        rng = np.random.default_rng(seed = pixel_indices[30])
        return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)
    else:
        return pixel_indices[valid_pixels]

def choose_CIV_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(colden[:, 2] > 1e13)[0]
    if len(valid_pixels) > Npixels:
        rng = np.random.default_rng(seed = pixel_indices[40])
        return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)
    else:
        return pixel_indices[valid_pixels]

def gen_line_dict(line, minz, maxz,init_N, init_b, maxN, maxb):
    line_name = line.name
    ion_parameters = {'name': line_name,
                      'f': [line.f_value],
                      'Gamma': [line.gamma],
                      'wavelength': [line.wavelength],
                      'numLines': 1,
                      'maxN': maxN,
                      'minN': 1e8,
                      'maxb': maxb,
                      'minb': 0.1,
                      'maxz': maxz,
                      'minz': minz,
                      'init_b': init_b,
                      'init_N': init_N}
    speciesDicts = {line_name: ion_parameters}
    return speciesDicts

def write_spectra_header(spectra_file, Npixels, vmin, vmax, dvel):
    spectra_file.write('%d %g %g %g\n' % (Npixels, vmin, vmax, dvel))
    spectra_file.flush()

def write_spectra(spectra_file, pixel_id, taulist):
    spectra_file.write('%d' % pixel_id)
    for tau in taulist:
        spectra_file.write(' %.3e' % tau)
    spectra_file.write('\n')
    spectra_file.flush()
    return

def write_absorber(absorber_file, pixel_id, fitted_lines, line, los_mean_vel):
    line_name = line.name
    Nlist = fitted_lines[line_name]['N']
    significant_list = np.where(Nlist > 1e9)[0]
    if len(significant_list) > 0:
        centroid_order = significant_list[np.argsort(fitted_lines[line_name]['z'][significant_list])]
        for index in centroid_order:
            N = Nlist[index]
            b = fitted_lines[line_name]['b'][index]
            z = fitted_lines[line_name]['z'][index]
            centroid = z * yt.units.physical_constants.c.to('km/s').value - los_mean_vel
            absorber_file.write('%d %g %g %g\n' % (pixel_id, N, b, centroid))
    absorber_file.flush()
    return

if __name__ == '__main__':
    sample_rate = 0.1
    timenum_list = [2]
    #timenum_list = [2]
    #direction_list = [0.5, 0.00001, 1 - 1e-10, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
    #direction_list = [0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
    direction_list = [0.5]
    for timenum in timenum_list:
        for direction in direction_list:
            Npix = 400
            pixel_size = 10
            redshift_list = [0.1006, 0.5396, 1.053, 2.013]
            #redshift_list = [0.1006, 0.5396, 1.053, 2.013, 3.017, 4.895]
            #redshift_list = [0.1006]
            #HM_index_list = [-4, -3, -2, -1, 0, 1, 2, 3, 4]
            #HM_index_list = [-100]
            HM_index_list = [0]
            #HM_index_list = [1, 2, 3, 4]
            #HM_index_list = [-100]


        #    redshift_list = [0.5396]
        #    HM_index_list = [2]
            #blob_cut = 0.82
            blob_cut = 0.5
            #init_N_list = [1e12, 1e12, 3e12, 3e12, 1e13, 1e13, 3e13, 3e13, 1e14, 1e14, 3e14, 3e14]
            #init_b_list = [10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40]
            #init_b_list_MgII = [1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10]

            init_N_list = [1e13]
            init_b_list = [6]
            #init_b_list_MgII = [1, 10, 1, 10, 1, 10]
            init_b_list_HI = [12]

            projected_ylist = -(np.arange(0, Npix * pixel_size, pixel_size) - (0.5 * Npix * pixel_size) + 0.5 * pixel_size)
            projected_zlist = np.arange(0, Npix * pixel_size, pixel_size) - (0.5 * Npix * pixel_size) + 0.5 * pixel_size

            ion_field_list = []
            for j in range(len(ionlist)):
                ion = ionlist[j]
                field_name = ion['fieldname']
                ion_field_list.append(field_name)
            
            if ion10 not in ionlist:
                ion_field_list.append(ion10['fieldname'])

            for k in range(len(redshift_list)):
                for HM_index in HM_index_list:
                    redshift = redshift_list[k]
                    #HM_index = HM_index_list[k]
                    ionTable = ionTable_base % (HM_index, redshift, HM_index)
                    colden_scaling_factor = 10 ** (-2/3 * HM_index)

                    trident.ion_balance.table_store = {} #Force trident to reload ionization tables
                    for run in runlist:
                        run_name = run['Name']
                        full_pixel_id_list = get_all_pixels(run, redshift, timenum, direction, HM_index)
                        rng = np.random.default_rng(seed = full_pixel_id_list[10])
                        pixel_id_list = rng.choice(full_pixel_id_list, round(len(full_pixel_id_list) * sample_rate), replace=False)

                        if rank == 0:
                            print(redshift, HM_index, run_name, timenum, direction)
                            sys.stdout.flush()
                        
                        data = yt.load(run['Dir'] + run_name + '/KH_hdf5_chk_' + run['f_list'][timenum])
                        data.add_field(('gas', 'metallicity'), function=_metallicity, sampling_type='cell', display_name='Metallicity', units='Zsun')
                        data.add_field(('gas', 'temperature_alt'), function=_altTemp, sampling_type='cell', units='K', display_name = 'Temperature Alt')

                        allDataRegion = data.all_data()
                        c = allDataRegion.quantities.center_of_mass() #Can avoid cutting off the tail
                        trident.add_ion_fields(data, ions=[ion['ion'] for ion in ionlist], ionization_table=ionTable)

                        if ion10 not in ionlist:
                            trident.add_ion_fields(data, ions=[ion10['ion']], ionization_table=ionTable)

                        vel_range = yt.units.YTQuantity(150, 'km/s')
                        dvel = yt.units.YTQuantity(5, 'km/s')
                        vlist = yt.YTArray(np.arange(-vel_range, vel_range + 0.5 * dvel, dvel), 'km/s')
                        #savepath = '/nas/astro-th/lyang/projectedColumns-main/spectra/HM_1e%d/spectral_lines_%s/z%g/t%d/' % (HM_index, run_name, redshift, timenum)
                        #savepath = '/nas/astro-th/lyang/projectedColumns-main/spectra23/blob0.5/HM_1e%d/spectral_lines_%s/z%g/t%d/TF%g/' % (HM_index, run_name, redshift, timenum, tempfloor)
                        savepath = '/nas/astro-th/lyang/projectedColumns-main/spectra23/blob0.5/HM_1e%d/spectral_lines_%s/z%g/t%d/TF%g_rho%g/' % (HM_index, run_name, redshift, timenum, tempfloor, denfloor)
                        os.makedirs(savepath, exist_ok=True)
                        if rank == 0:
                            np.savetxt(savepath + 'pixel_list_%d.txt' % (round(10 * direction)), pixel_id_list, fmt='%d', header='%d %d' % (len(full_pixel_id_list), len(pixel_id_list)))

                        if rank < len(pixel_id_list):
                            pixel_id_list_local = pixel_id_list[rank : : nprocs]
                        else:
                            pixel_id_list_local = []

                        tmp_spectra_file_name = savepath + 'tmp_spectra_%d_%s.txt'
                        tmp_absorber_file_name = savepath + 'tmp_absorber_%d_%s.txt'

                        #tmp_spectra_file_list = [open(tmp_spectra_file_name % (rank, ion['ion']), 'w') for ion in ionlist]
                        tmp_absorber_file_list = [open(tmp_absorber_file_name % (rank, ion['ion']), 'w') for ion in ionlist]

                        for ind in range(len(pixel_id_list_local)):
                            pixel_id = pixel_id_list_local[ind]
                            #print(redshift, run_name, pixel_id)
                            projected_yindex = pixel_id % Npix
                            projected_zindex = int(pixel_id / Npix)
                            projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                            angle = np.arccos(direction)
                            norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.

                            los_center = c + deproject(projected_coord, angle) * yt.units.pc
                            los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                            los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc

                            ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray_%d_tf.h5' % rank, fields=[('flash', 'blob'), ('gas', 'metallicity'), ('gas', 'density')] + ion_field_list)
                            cloud_section = ray.all_data()
                            ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                            cloud_section['gas', 'density'][ambient_indices] = 0

                            ultra_cool = np.where(cloud_section['gas', 'temperature'] < 1000)[0]
                            cloud_section['gas', 'temperature'][ultra_cool] = 1000

                            heated_section = np.where((cloud_section['gas', 'temperature'] < tempfloor) & (cloud_section['gas', 'density'] < denfloor))[0]
                            cloud_section['gas', 'temperature'][heated_section] = tempfloor
                            
                            los_log_coldens = []
                            for ion_field in ion_field_list:
                                cloud_section['gas', ion_field][ambient_indices] = 0
                                #cloud_section['gas', ion_field] *= colden_scaling_factor
                                los_log_coldens.append(np.log10(np.dot(cloud_section['gas', ion_field], cloud_section['dl']))) #unit: cm^-2

                            if np.any(cloud_section['gas','H_p0_number_density'].value):
                                los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section['gas','H_p0_number_density'])
                            elif np.any(cloud_section['gas','density'].value):
                                los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section['gas','density'])
                            else:
                                continue
                                
                            vmin = los_mean_vel - vel_range
                            vmax = los_mean_vel + vel_range
                            minz = (vmin / yt.units.physical_constants.c).value
                            maxz = (vmax / yt.units.physical_constants.c).value

                            for j in range(len(ionlist)):
                                ion = ionlist[j]
                                line = lines[j]
                                linename = line.name
                                rest_lambda = line.wavelength

                                lambda_min = rest_lambda * (1 + minz)
                                lambda_max = rest_lambda * (1 + maxz)
                                dlambda = rest_lambda * (dvel / yt.units.physical_constants.c).value
                                sg = trident.SpectrumGenerator(lambda_min=lambda_min, lambda_max=lambda_max, dlambda=dlambda)

                                try:
                                    sg.make_spectrum(cloud_section, lines=[linename], min_tau=1e-8, ly_continuum=False)
                                    fluxes = np.exp(-sg.tau_field)
                                    lambda_field = sg.lambda_field

                                    max_tau = max(sg.tau_field)
                                    tau_scaling_factor = 1
                                    if max_tau > 1e-4:
                                        tau_scaling_factor = 4 / max_tau
                                    else:
                                        continue
                                    rescaled_tau = sg.tau_field * tau_scaling_factor #Scale the optical depths to avoid saturation
                                    rescaled_fluxes = np.exp(-rescaled_tau)

                                    fitted_lines_local = []
                                    err = []
                                    for l in range(len(init_N_list)):
                                        init_N = init_N_list[l]
                                        init_b = init_b_list[l]
                                        if linename == 'H I 1216':
                                            init_b = init_b_list_HI[l]
                                        if tau_scaling_factor != 1:
                                            max_N = 1.1 * 10 ** los_log_coldens[j] * tau_scaling_factor
                                        else:
                                            max_N = 1e14

                                        max_b = 250
                                        speciesDicts = gen_line_dict(line, minz, maxz, init_N, init_b, max_N, max_b)
                                        try:
                                            fitted_lines, fitted_flux = generate_total_fit(lambda_field, rescaled_fluxes, orderFits=[linename], speciesDicts=speciesDicts, complexLim=0.9995, fitLim=0.994)
                                            fitted_lines_local.append(fitted_lines)
                                            err.append(np.sum((fitted_flux - fluxes) ** 2))
                                        except:
                                            pass
                                    
                                    if len(err) > 0:
                                        best_set = np.argmin(err)
                                        best_fitted_lines = fitted_lines_local[best_set]
                                        best_fitted_lines[linename]['N'] /= tau_scaling_factor
                                        write_absorber(tmp_absorber_file_list[j], pixel_id, best_fitted_lines, line, los_mean_vel.to('km/s').value)

                                    '''
                                    speciesDicts = gen_line_dict(line, minz, maxz)
                                    fitted_lines, fitted_flux = generate_total_fit(lambda_field, fluxes, orderFits=[linename], speciesDicts=speciesDicts, complexLim=0.9995, fitLim=0.994, output_file=\
                                                                                savepath + '%s_%d_%d_%s_fit.h5' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                                    fitted_list.append(fitted_flux)
                                    '''
                                
                                    #write_spectra(tmp_spectra_file_list[j], pixel_id, sg.tau_field)
                                except:
                                    #write_spectra(tmp_spectra_file_list[j], pixel_id, np.zeros_like(vlist)) #If the spectrum generator is somehow broken, just write all 0's.
                                    pass

                                sg.clear_spectrum()
                                
                            #if ind % 50 == 0 or ind == len(pixel_id_list_local) - 1:
                            #    print('process %d: %d/%d' % (rank, ind, len(pixel_id_list_local)))
                        
                        for files in tmp_absorber_file_list:
                            files.close()
                        
                        #for files in tmp_spectra_file_list:
                        #    files.close()
                        
                        #print('process %d: tmp files closed' % rank)

                        comm.Barrier()
                        
                        if rank == 0:
                            for i in range(len(ionlist)):
                                ion = ionlist[i]
                                tau_file_name = savepath + 'tau_%s_%d_z%g_%s.txt' % (run_name, round(10 * direction), redshift, ion['ion'].replace(' ', '_'))
                                absorber_file_name = savepath + 'absorbers_%s_%d_z%g_%s.txt' % (run_name, round(10 * direction), redshift, ion['ion'].replace(' ', '_'))

                                #with open(tau_file_name, 'w') as tau_file:
                                #    write_spectra_header(tau_file, len(pixel_id_list), -vel_range, vel_range, dvel)
                                #    for process in range(nprocs):
                                #        with open(tmp_spectra_file_name % (process, ion['ion']), 'r') as tmp:
                                #            tau_file.write(tmp.read())

                                with open(absorber_file_name, 'w') as absorber_file:
                                    for process in range(nprocs):
                                        with open(tmp_absorber_file_name % (process, ion['ion']), 'r') as tmp:
                                            absorber_file.write(tmp.read())
                            
                            for ion in ionlist:
                                for process in range(nprocs):
                                    try:
                                        #os.remove(tmp_spectra_file_name % (process, ion['ion']))
                                        os.remove(tmp_absorber_file_name % (process, ion['ion']))
                                    except:
                                        pass

                        comm.Barrier()
