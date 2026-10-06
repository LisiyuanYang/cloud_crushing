import numpy as np
from scipy.spatial import KDTree
from numba import jit

data_path_base = '/nas/astro-th/lyang/%s/'
ionTable_base = '/work/pi_nsk_umass_edu/lyang/newTridentTables/Cloudy23/hm-1e%d-z%g/HM_1e%d.h5'
Omega_m = 0.3
Omega_baryon = 0.045
Omega_lambda = 0.7
h = 0.7
XH = 0.76
XHE = (1.0 - XH) / (4.0 * XH)
MHYDR = 1.6726e-24 #proton mass in g
KPC = 3.08568e21 #kpc in cm
Gamma = 1.66667
mu_ionized = (1 + 4 * XHE) / (2 + 3 * XHE) #Assumes full ionization
Tipsy_velocity_per_size = 34.5494149472
MAX_UINT32 = 2 ** 32 - 1
SOLAR_MASS_IN_GRAMS = 1.988e33
SOLAR_METAL_FRAC = 0.012947 #Solar metal mass fraction

run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Formal_name':'T0.3_v1000_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':3.8,
        'chi': 300,
        'tcc':1.7,
        'radius': 100,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132'],
        'f_list_full':['0013', '0038', '0080', '0132'],
        'name_template':'KH_hdf5_chk_%04d'}

run2 = { 'Name':'T3_v3000_chi3000_cond',
        'Formal_name':'T3_v3000_chi3000_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':3.6,
        'chi': 3000,
        'tcc':1.8,
        'radius': 100,
        'velocity':3000,
        'f_list':['0001', '0004', '0007', '0010'],
        'f_list_full':['0001', '0004', '0007', '0010'],
        'name_template':'KH_hdf5_chk_%04d'}

run3 = { 'Name':'T1_v1700_chi1000_cond',
        'Formal_name':'T1_v1700_chi1000_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':3.5,
        'chi': 1000,
        'tcc':1.8,
        'radius': 100,
        'velocity':1700,
        'f_list':['0002', '0010', '0017', '0028'],
        'f_list_full':['0002', '0010', '0017', '0028'],
        'name_template':'KH_hdf5_chk_%04d'}

run4 = { 'Name':'T0.3_v1000_chi300',
        'Formal_name':'T0.3_v1000_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':3.8,
        'chi': 300,
        'tcc':1.7,
        'radius': 100,
        'velocity':1000,
        'f_list':['0025', '0033', '0042', '0058'],
        'f_list_full':['0025', '0033', '0042', '0058'],
        'name_template':'KH_hdf5_chk_%04d'}

run5 = { 'Name':'T3_v3000_chi3000',
        'Formal_name':'T3_v3000_chi3000_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':3.6,
        'chi': 3000,
        'tcc':1.8,
        'radius': 100,
        'velocity':3000,
        'f_list':['0021', '0030', '0040', '0062'],
        'f_list_full':sorted(set(['%04d' % i for i in range(61)[: : 5]] + ['0021', '0030', '0040', '0062'])),
        'name_template':'KH_hdf5_chk_%04d'}

run6 = { 'Name':'T1_v1700_chi1000',
        'Formal_name':'T1_v1700_chi1000_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':3.5,
        'chi': 1000,
        'tcc':1.8,
        'radius': 100,
        'velocity':1700,
        'f_list':['0021', '0029', '0038', '0052'],
        'f_list_full':['0021', '0029', '0038', '0052'],
        'name_template':'KH_hdf5_chk_%04d'}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
         'Formal_name':'T0.3_v1700_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':6.5,
        'chi': 300,
        'tcc':1.0,
        'radius': 100,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078'],
        'f_list_full':['0003', '0020', '0046', '0078'],
        'name_template':'KH_hdf5_chk_%04d'}
    
run12 = { 'Name':'T0.3_v3000_chi300_cond',
         'Formal_name':'T0.3_v3000_chi300_cond_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':11.4,
        'chi': 300,
        'tcc':0.56,
        'radius': 100,
        'velocity':3000,
        'f_list':['0001', '0004', '0014', '0035'],
        'f_list_full':['0001', '0004', '0014', '0035'],
        'name_template':'KH_hdf5_chk_%04d'}

run16 = { 'Name':'T0.3_v1700_chi300',
         'Formal_name':'T0.3_v1700_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':6.5,
        'chi': 300,
        'tcc':1.0,
        'radius': 100,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085'],
        'f_list_full':sorted(set(['%04d' % i for i in range(106)[: : 5]] + ['0022', '0032', '0053', '0085'])),
        'name_template':'KH_hdf5_chk_%04d'}

run17 = { 'Name':'T0.3_v3000_chi300',
         'Formal_name':'T0.3_v3000_chi300_hcol',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'init_mass': 6.19e4, #in solar mass
        'rho_0': 1e-24,
        'Mach':11.4,
        'chi': 300,
        'tcc':0.56,
        'radius': 100,
        'velocity':3000,
        'f_list':['0028', '0044', '0065', '0110'],
        'f_list_full':sorted(set(['%04d' % i for i in range(136)[: : 5]] + ['0028', '0044', '0065', '0110'])),
        'name_template':'KH_hdf5_chk_%04d'}

runx2 = { 'Name':'T0.3_v1000_chi300_ld2',
         'Formal_name':'T0.3_v1000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.8,
        'chi': 300,
        'tcc':9.17,
        'radius': 545,
        'velocity':1000,
        'f_list':['0026', '0036', '0057', '0077'],
        'f_list_full':['%04d' % i for i in range(105)],
        'name_template':'KH_hdf5_chk_%04d'}

runx3 = { 'Name':'T1_v1700_chi1000_ld2',
         'Formal_name':'T1_v1700_chi1000',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.5,
        'chi': 1000,
        'tcc':9.85,
        'radius': 545,
        'velocity':1700,
        'f_list':['0023', '0033', '0055', '0070'],
        'f_list_full':['%04d' % i for i in range(114)],
        'name_template':'KH_hdf5_chk_%04d'}

runx4 = { 'Name':'T0.3_v1700_chi300_ld2',
         'Formal_name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':6.5,
        'chi': 300,
        'tcc':5.40,
        'radius': 545,
        'velocity':1700,
        'f_list':['0026', '0031', '0035', '0042', '0051', '0074'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(101)],
        'name_template':'KH_hdf5_chk_%04d'}

runx5 = { 'Name':'T0.3_v3000_chi300_ld2',
         'Formal_name':'T0.3_v3000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':11.4,
        'chi': 300,
        'tcc':3.06,
        'radius': 545,
        'velocity':3000,
        'f_list':['0022', '0027', '0038', '0080'],
        'f_list_full':['%04d' % i for i in range(82)],
        'name_template':'KH_hdf5_chk_%04d'}

runx6 = { 'Name':'T3_v3000_chi3000_ld2',
         'Formal_name':'T3_v3000_chi3000',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.6,
        'chi': 3000,
        'tcc':9.67,
        'radius': 545,
        'velocity':3000,
        'f_list':['0022', '0027', '0032', '0045'],
        'f_list_full':['%04d' % i for i in range(52)],
        'name_template':'KH_hdf5_chk_%04d'}

'''
runx7 = { 'Name':'T0.3_v3000_chi300_cond_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':11.4,
        'chi': 300,
        'tcc':3.06,
        'radius': 545,
        'velocity':3000,
        'f_list':['0017', '0023', '0034', '0079'],
        'f_list_full':['%04d' % i for i in range(7)],
        'name_template':'KH_hdf5_chk_%04d'}
'''

runx8 = { 'Name':'T0.3_v1000_chi300_cond_ld2',
         'Formal_name':'T0.3_v1000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.8,
        'chi': 300,
        'tcc':9.17,
        'radius': 545,
        'velocity':1000,
        'f_list':['0007', '0011', '0023', '0036'],
        'f_list_full':['%04d' % i for i in range(61)],
        'name_template':'KH_hdf5_chk_%04d'}

runx9 = { 'Name':'T1_v1700_chi1000_cond_ld2',
         'Formal_name':'T1_v1700_chi1000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.5,
        'chi': 1000,
        'tcc':9.85,
        'radius': 545,
        'velocity':1700,
        'f_list':['0005', '0006', '0010', '0015'],
        'f_list_full':['%04d' % i for i in range(35)],
        'name_template':'KH_hdf5_chk_%04d'}

runx10 = { 'Name':'T0.3_v1700_chi300_cond_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':6.5,
        'chi': 300,
        'tcc':5.40,
        'radius': 545,
        'velocity':1700,
        'f_list':['0007', '0010', '0019', '0039'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(75)],
        'name_template':'KH_hdf5_chk_%04d'}

runx11 = { 'Name':'T0.3_v3000_chi300_cond_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':11.4,
        'chi': 300,
        'tcc':3.06,
        'radius': 545,
        'velocity':3000,
        'f_list':['0007', '0009', '0012', '0013'],
        'f_list_full':['%04d' % i for i in range(20)],
        'name_template':'KH_hdf5_chk_%04d'}

runx12 = { 'Name':'T3_v3000_chi3000_cond_ld2',
         'Formal_name':'T3_v3000_chi3000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.6,
        'chi': 3000,
        'tcc':9.67,
        'radius': 545,
        'velocity':3000,
        'f_list':['0003', '0005', '0007', '0010'],
        'f_list_full':['%04d' % i for i in range(31)],
        'name_template':'KH_hdf5_chk_%04d'}

runx13 = { 'Name':'T1_v1700_chi1000_cond_0.1_ld2',
         'Formal_name':'T1_v1700_chi1000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.5,
        'chi': 1000,
        'tcc':9.85,
        'radius': 545,
        'velocity':1700,
        'f_list':['0005', '0010', '0019', '0030'],
        'f_list_full':['%04d' % i for i in range(72)],
        'name_template':'KH_hdf5_chk_%04d'}

runx14 = { 'Name':'T0.3_v1000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.8,
        'chi': 300,
        'tcc':9.17,
        'radius': 545,
        'velocity':1000,
        'f_list':['0010', '0026', '0048', '0071'],
        'f_list_full':['%04d' % i for i in range(131)],
        'name_template':'KH_hdf5_chk_%04d'}

runx15 = { 'Name':'T3_v3000_chi3000_cond_0.1_ld2',
         'Formal_name':'T3_v3000_chi3000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':3.6,
        'chi': 3000,
        'tcc':9.67,
        'radius': 545,
        'velocity':3000,
        'f_list':['0004', '0005', '0010', '0013'],
        'f_list_full':['%04d' % i for i in range(27)],
        'name_template':'KH_hdf5_chk_%04d'}

runx16 = { 'Name':'T0.3_v1700_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':6.5,
        'chi': 300,
        'tcc':5.40,
        'radius': 545,
        'velocity':1700,
        'f_list':['0008', '0016', '0046', '0066'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(125)],
        'name_template':'KH_hdf5_chk_%04d'}

runx17 = { 'Name':'T0.3_v3000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':11.4,
        'chi': 300,
        'tcc':3.06,
        'radius': 545,
        'velocity':3000,
        'f_list':['0007', '0009', '0013', '0018'],
        'f_list_full':['%04d' % i for i in range(79)],
        'name_template':'KH_hdf5_chk_%04d'}

runy1 = { 'Name':'T0.1_v150_chi100_ld2',
         'Formal_name':'T0.1_v150_chi100',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':1.0,
        'chi': 100,
        'tcc':35.3,
        'radius': 545,
        'velocity':150,
        'f_list':['0021', '0023', '0031', '0043'],
        'f_list_full':['%04d' % i for i in range(89)],
        'name_template':'KH_hdf5_chk_%04d'}

runy2 = { 'Name':'T0.1_v150_chi100_cond_0.1_ld2',
         'Formal_name':'T0.1_v150_chi100_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':1.0,
        'chi': 100,
        'tcc':35.3,
        'radius': 545,
        'velocity':150,
        'f_list':['0022', '0030', '0051', '0064'],
        'f_list_full':['%04d' % i for i in range(96)],
        'name_template':'KH_hdf5_chk_%04d'}

runz1 = { 'Name':'T0.02_v100_chi20_Z',
         'Formal_name':'T0.02_v100_chi20',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':1.5,
        'chi': 20,
        'tcc':23.7,
        'radius': 545,
        'velocity':100,
        'f_list':['0030', '0039', '0049', '0057'],
        'f_list_full':['%04d' % i for i in range(75)],
        'name_template':'KH_hdf5_chk_%04d'}

runa1 = { 'Name':'T0.3_v1700_chi300_apk',
        'Formal_name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':6.5,
        'chi': 300,
        'tcc':5.40,
        'velocity':1700,
        'tracer': ("parthenon", "prim_scalar_0"),
        'f_list':['0013', '0038', '0080', '0132'],
        'f_list_full':['%05d' % i for i in range(90)],
        'name_template':'parthenon.prim.%05d.phdf'}

runp1 = { 'Name':'T0.002_v30_rho30',
         'Formal_name':'T0.002_v30_rho30',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-27,
        'Mach':1.58,
        'chi': 1.78,
        'tcc':23.1,
        'velocity':30,
        'radius': 800,
        'f_list':['0070', '0084', '0098', '0111'],
        'f_list_full':['%04d' % i for i in range(201)],
        'name_template':'KH_hdf5_chk_%04d'}

runp2 = { 'Name':'T0.005_v20_rho3',
         'Formal_name':'T0.005_v20_rho3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-28,
        'Mach':0.63,
        'chi': 5.01,
        'tcc':176.8,
        'velocity':21.3,
        'radius': 1722.,
        'f_list':['0020', '0022', '0024', '0027'],
        'f_list_full':['%04d' % i for i in range(129)],
        'name_template':'KH_hdf5_chk_%04d'}

runp3 = { 'Name':'T0.005_v20_rho1',
         'Formal_name':'T0.005_v20_rho1',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-28,
        'Mach':0.63,
        'chi': 5.01,
        'tcc':259.5,
        'velocity':21.3,
        'radius': 2528.,
        'f_list':['0023', '0025', '0027', '0031'],
        'f_list_full':['%04d' % i for i in range(101)],
        'name_template':'KH_hdf5_chk_%04d'}

runp4 = { 'Name':'T0.005_v20_rho0.3',
         'Formal_name':'T0.005_v20_rho0.3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-29,
        'Mach':0.63,
        'chi': 5.01,
        'tcc':380.9,
        'velocity':21.3,
        'radius': 3710.,
        'f_list':['0022', '0025', '0028', '0031'],
        'f_list_full':['%04d' % i for i in range(101)],
        'name_template':'KH_hdf5_chk_%04d'}

runp5 = { 'Name':'T0.005_v50_rho3',
         'Formal_name':'T0.005_v50_rho3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-28,
        'Mach':1.58,
        'chi': 5.01,
        'tcc':70.4,
        'velocity':53.6,
        'radius': 1722.,
        'f_list':['0032', '0038', '0045', '0054'],
        'f_list_full':['%04d' % i for i in range(201)],
        'name_template':'KH_hdf5_chk_%04d'}

runp6 = { 'Name':'T0.005_v50_rho1',
         'Formal_name':'T0.005_v50_rho1',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-28,
        'Mach':1.58,
        'chi': 5.01,
        'tcc':103.3,
        'velocity':53.6,
        'radius': 2528.,
        'f_list':['0034', '0039', '0048', '0058'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp7 = { 'Name':'T0.005_v50_rho0.3',
         'Formal_name':'T0.005_v50_rho0.3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-29,
        'Mach':1.58,
        'chi': 5.01,
        'tcc':151.6,
        'velocity':53.6,
        'radius': 3710.,
        'f_list':['0041', '0046', '0053', '0063'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp8 = { 'Name':'T0.025_v50_rho3',
         'Formal_name':'T0.025_v50_rho3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-28,
        'Mach':0.63,
        'chi': 25.12,
        'tcc':176.8,
        'velocity':47.8,
        'radius': 1722.,
        'f_list':['0019', '0021', '0023', '0026'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp9 = { 'Name':'T0.025_v50_rho1',
         'Formal_name':'T0.025_v50_rho1',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-28,
        'Mach':0.63,
        'chi': 25.12,
        'tcc':259.5,
        'velocity':47.8,
        'radius': 2528.,
        'f_list':['0022', '0024', '0028', '0032'],
        'f_list_full':['%04d' % i for i in range(201)],
        'name_template':'KH_hdf5_chk_%04d'}

runp9b = { 'Name':'T0.025_v50_rho1_old',
         'Formal_name':'T0.025_v50_rho1_old',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-28,
        'Mach':0.63,
        'chi': 25.12,
        'tcc':259.5,
        'velocity':47.8,
        'radius': 2528.,
        'f_list':['0023', '0025', '0027', '0032'],
        'f_list_full':['%04d' % i for i in range(201)],
        'name_template':'KH_hdf5_chk_%04d'}

runp10 = { 'Name':'T0.025_v50_rho0.3',
         'Formal_name':'T0.025_v50_rho0.3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-29,
        'Mach':0.63,
        'chi': 25.12,
        'tcc':380.9,
        'velocity':47.8,
        'radius': 3710.,
        'f_list':['0030', '0034', '0042', '0045'],
        'f_list_full':['%04d' % i for i in range(201)],
        'name_template':'KH_hdf5_chk_%04d'}

runp11 = { 'Name':'T0.025_v120_rho3',
         'Formal_name':'T0.025_v120_rho3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-28,
        'Mach':1.58,
        'chi': 25.12,
        'tcc':70.4,
        'velocity':120.,
        'radius': 1722.,
        'f_list':['0034', '0037', '0045', '0061'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp12 = { 'Name':'T0.025_v120_rho1',
         'Formal_name':'T0.025_v120_rho1',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-28,
        'Mach':1.58,
        'chi': 25.12,
        'tcc':103.3,
        'velocity':120.,
        'radius': 2528.,
        'f_list':['0035', '0038', '0050', '0073'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp13 = { 'Name':'T0.025_v120_rho0.3',
         'Formal_name':'T0.025_v120_rho0.3',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 3.16e-29,
        'Mach':1.58,
        'chi': 25.12,
        'tcc':151.6,
        'velocity':120.,
        'radius': 3710.,
        'f_list':['0036', '0066', '0044', '0050'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp14 = { 'Name':'T0.1_v240_rho100',
         'Formal_name':'T0.1_v240_rho100',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1e-26,
        'Mach':1.58,
        'chi': 100.,
        'tcc':22.3,
        'velocity':239.,
        'radius': 545.,
        'f_list':['0032', '0039', '0078', '0093'],
        'f_list_full':['%04d' % i for i in range(102)],
        'name_template':'KH_hdf5_chk_%04d'}

runp15 = { 'Name':'T0.005_v100_rho15',
         'Formal_name':'T0.005_v100_rho15',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1.58e-27,
        'Mach':2.82,
        'chi': 5.01,
        'tcc':23.1,
        'velocity':95.3,
        'radius': 1006.,
        'f_list':['0045', '0068', '0116', '0154'],
        'f_list_full':['%04d' % i for i in range(202)],
        'name_template':'KH_hdf5_chk_%04d'}

runp16 = { 'Name':'T0.001_v40_rho80',
         'Formal_name':'T0.001_v40_rho80',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 7.94e-27,
        'Mach':2.51,
        'chi': 1.26,
        'tcc':15.2,
        'velocity':42.6,
        'radius': 587.,
        'f_list':['0072', '0103', '0127', '0151'],
        'f_list_full':['%04d' % i for i in range(200)],
        'name_template':'KH_hdf5_chk_%04d'}

runp17 = { 'Name':'T0.05_v170_rho15',
         'Formal_name':'T0.05_v170_rho15',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1.58e-27,
        'Mach':1.58,
        'chi': 50.1,
        'tcc':41.1,
        'velocity':169.,
        'radius': 1010.,
        'f_list':['0029', '0039', '0049', '0061'],
        'f_list_full':['%04d' % i for i in range(78)],
        'name_template':'KH_hdf5_chk_%04d'}

runp18 = { 'Name':'T0.05_v70_rho15',
         'Formal_name':'T0.05_v70_rho15',
        'Dir':'/scratch/workspace/lyang_umass_edu-cloud_crushing/',
        'init_mass': 1e5, #in solar mass
        'rho_0': 1.58e-27,
        'Mach':0.63,
        'chi': 50.1,
        'tcc':103.3,
        'velocity':67.4,
        'radius': 1010.,
        'f_list':['0022', '0023', '0026', '0028'],
        'f_list_full':['%04d' % i for i in range(46)],
        'name_template':'KH_hdf5_chk_%04d'}

runs = {}
runs['run1'] = run1
runs['run2'] = run2
runs['run3'] = run3
runs['run4'] = run4
runs['run5'] = run5
runs['run6'] = run6
runs['run11'] = run11
runs['run12'] = run12
runs['run16'] = run16
runs['run17'] = run17
runs['runx2'] = runx2
runs['runx3'] = runx3
runs['runx4'] = runx4
runs['runx5'] = runx5
runs['runx6'] = runx6
runs['runx8'] = runx8
runs['runx9'] = runx9
runs['runx10'] = runx10
runs['runx11'] = runx11
runs['runx12'] = runx12
runs['runx13'] = runx13
runs['runx14'] = runx14
runs['runx15'] = runx15
runs['runx16'] = runx16
runs['runx17'] = runx17
runs['runy1'] = runy1
runs['runy2'] = runy2
runs['runz1'] = runz1
runs['runa1'] = runa1
runs['runp1'] = runp1
runs['runp2'] = runp2
runs['runp3'] = runp3
runs['runp4'] = runp4
runs['runp5'] = runp5
runs['runp6'] = runp6
runs['runp7'] = runp7
runs['runp8'] = runp8
runs['runp9'] = runp9
runs['runp9b'] = runp9b
runs['runp10'] = runp10
runs['runp11'] = runp11
runs['runp12'] = runp12
runs['runp13'] = runp13
runs['runp14'] = runp14
runs['runp15'] = runp15    
runs['runp16'] = runp16    
runs['runp17'] = runp17    
runs['runp18'] = runp18    

Upsi_g_temp_list = np.array([4., 4.5, 5., 5.5, 6.])#From Piacitelli et al. (2022)
ion1 = {'ion':'O VI',
        'fieldname':'O_p5_number_density',
        'ionfolder': '/OVI/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 1031.91,
        'sigma': 1.1776e-18,
        'massNum': 16.0,
        'gizmo_index': 4,
        'Upsi_g': np.array([1.65, 1.68, 1.76, 1.95, 2.3])}
ion2 = {'ion':'C IV',
        'fieldname':'C_p3_number_density',
        'ionfolder': '/CIV/',
        'SolarAbundance': 2.45e-04,
        'rest_wave': 1548.18,
        'sigma': 2.5347e-18,
        'massNum': 12.0,
        'gizmo_index': 2,
        'Upsi_g': np.array([2.86, 2.97, 3.25, 3.82, 4.83])}
ion3 = {'ion':'N V',
        'fieldname':'N_p4_number_density',
        'ionfolder': '/NV/',
        'SolarAbundance': 8.51e-05,
        'rest_wave': 1242.8,
        'sigma': 8.3181e-19,
        'massNum': 14.0,
        'gizmo_index': 3,
        'Upsi_g': np.array([2.16, 2.21, 2.34, 2.66, 3.21])}
ion4 = {'ion':'C II',
        'fieldname':'C_p1_number_density',
        'ionfolder': '/CII/',
        'SolarAbundance': 2.45e-04,
        'rest_wave': 1335.66,
        'sigma': 1.4555e-19,
        'massNum': 12.0,
        'gizmo_index': 2}
ion5 = {'ion': 'Ne VIII',
        'fieldname': 'Ne_p7_number_density',
        'ionfolder':'/NeVIII/',
        'SolarAbundance': 1.00e-04,
        'rest_wave': 770.406,
        'sigma': 6.74298e-19,
        'massNum': 20.0,
        'gizmo_index': 5}
ion6 = {'ion': 'C III',
        'fieldname': 'C_p2_number_density',
        'ionfolder':'/CIII/',
        'SolarAbundance': 2.45e-04,
        'rest_wave': 977.02,
        'sigma': 6.359e-18,
        'massNum': 12.0,
        'gizmo_index': 2,
        'Upsi_g': np.array([3.19, 3.42, 3.99, 5.27, 7.54])}
ion7 = {'ion': 'Mg II',
        'fieldname': 'Mg_p1_number_density',
        'ionfolder':'/MgII/',
        'SolarAbundance': 3.47e-05,
        'rest_wave': 2796.35,
        'sigma': 6.60717e-21,
        'massNum': 24.0,
        'gizmo_index': 6}
ion8 = {'ion': 'Si III',
        'fieldname': 'Si_p2_number_density',
        'ionfolder':'/SiIII/',
        'SolarAbundance': 3.47e-05,
        'rest_wave': 1206.5,
        'sigma': 2.2258e-20,
        'massNum': 28.0,
        'gizmo_index': 7,
        'Upsi_g': np.array([5.81, 7., 8.76, 12.6, 19.1])}
ion9 = {'ion': 'Si IV',
        'fieldname': 'Si_p3_number_density',
        'ionfolder':'/SiIV/',
        'SolarAbundance': 3.47e-05,
        'rest_wave': 1393.8,
        'sigma': 3.0694e-18,
        'massNum': 28.0,
        'gizmo_index': 7,
        'Upsi_g': np.array([5.2, 5.3, 5.75, 7.05, 9.5])}
ion10 = {'ion': 'H I',
        'fieldname': 'H_p0_number_density',
        'ionfolder':'/HI/',
        'SolarAbundance': 1.00e+00,
        'rest_wave': 1215.67,
        'sigma': 4.3394e-18,
        'massNum': 1.0,
        'gizmo_index': -1}
ion11 = {'ion': 'H II',
        'fieldname': 'H_p1_number_density',
        'ionfolder':'/HII/',
        'SolarAbundance': 1.00e+00,
        'rest_wave': 1215.67,
        #'sigma': 4.3394e-18,
        'massNum': 1.0,
        'gizmo_index': -1}
ion12 = {'ion': 'He II',
        'fieldname': 'He_p1_number_density',
        'ionfolder':'/HeII/',
        'SolarAbundance': 1.00e-01,
        'rest_wave': 303.918,
        #'sigma': 4.3394e-18,
        'massNum': 4.0,
        'gizmo_index': 1}
ion13 = {'ion': 'O IV',
        'fieldname': 'O_p3_number_density',
        'ionfolder':'/OIV/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 787.711,
        #'sigma': 4.3394e-18,
        'massNum': 16.0,
        'gizmo_index': 4}
ion14 = {'ion': 'Si II',
        'fieldname': 'Si_p1_number_density',
        'ionfolder':'/SiII/',
        'SolarAbundance': 3.47e-05,
        'rest_wave': 1260.422,
        #'sigma': 4.3394e-18,
        'massNum': 28.0,
        'gizmo_index': 7}
ion15 = {'ion': 'O VII',
        'fieldname': 'O_p6_number_density',
        'ionfolder':'/OVII/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 21.602,
        #'sigma': 4.3394e-18,
        'massNum': 16.0,
        'gizmo_index': 4}
ion16 = {'ion': 'O VIII',
        'fieldname': 'O_p7_number_density',
        'ionfolder':'/OVIII/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 18.969,
        #'sigma': 4.3394e-18,
        'massNum': 16.0,
        'gizmo_index': 4}
ion17 = {'ion': 'O I',
        'fieldname': 'O_p0_number_density',
        'ionfolder':'/OI/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 1302.1685,
        #'sigma': 4.3394e-18,
        'massNum': 16.0,
        'gizmo_index': 4}
ion18 = {'ion': 'O II',
        'fieldname': 'O_p1_number_density',
        'ionfolder':'/OII/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 834.4655,
        #'sigma': 4.3394e-18,
        'massNum': 16.0,
        'gizmo_index': 4}
ion19 = {'ion': 'O III',
        'fieldname': 'O_p2_number_density',
        'ionfolder':'/OIII/',
        'SolarAbundance': 4.90e-04,
        'rest_wave': 702.332,
        #'sigma': 4.3394e-18,
        'massNum': 16.0,
        'gizmo_index': 4}

ions = {}
ions['O VI'] = ion1
ions['C IV'] = ion2
ions['N V'] = ion3
ions['C II'] = ion4
ions['Ne VIII'] = ion5
ions['C III'] = ion6
ions['Mg II'] = ion7
ions['Si III'] = ion8
ions['Si IV'] = ion9
ions['H I'] = ion10
ions['H II'] = ion11
ions['He II'] = ion12
ions['O IV'] = ion13
ions['Si II'] = ion14
ions['O VII'] = ion15
ions['O VIII'] = ion16
ions['O I'] = ion17
ions['O II'] = ion18
ions['O III'] = ion19

@jit
def cosine_angle(vec1=np.array([1., 0., 0.]), vec2=np.array([0., 1., 0.]), zeros=1.0):
    dot_product = np.dot(vec1, vec2)
    modulus = np.sqrt(np.sum(vec1 ** 2) * np.sum(vec2 ** 2))
    if modulus == 0:
        return zeros
    else:
        return dot_product / modulus

@jit
def cosine_angle_list(veclist1=np.array([[1., 0., 0.]]), veclist2=np.array([[0., 1., 0.]]), zeros=1.0):
    assert len(veclist1) == len(veclist2)
    Nvecs = len(veclist1)
    cosine_list = np.full(Nvecs, zeros)
    for i in range(Nvecs):
        cosine_list[i] = cosine_angle(veclist1[i], veclist2[i], zeros)
    return cosine_list

@jit
def point_rotate(point=np.array([0., 0., 0.]), new_z=np.array([0., 0., 1.])):
    radius2 = np.sum(new_z ** 2)
    if radius2 == 0:
        return point
    
    phi = np.arctan2(new_z[1], new_z[0])
    
    theta = np.arccos(new_z[2] / np.sqrt(radius2))
    rotation_matrix = np.array([[np.cos(theta) * np.cos(phi), np.cos(theta) * np.sin(phi), -np.sin(theta)],
                                [-np.sin(phi), np.cos(phi), 0],
                                [np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)]])
    return np.dot(rotation_matrix, point)

@jit
def point_rotate_list(point_list=np.array([[0., 0., 0.]]), new_z_list=np.array([[0., 0., 1.]])):
    Npoints = len(point_list)
    assert Npoints == len(new_z_list)

    new_coord_list = np.zeros((Npoints, 3))
    for i in range(Npoints):
        new_coord_list[i] = point_rotate(point_list[i], new_z_list[i])
    return new_coord_list

def binned_particles(coords, xlower, xupper, ylower, yupper, Nbins):
    inr = np.where((coords[:, 0] >= xlower) & (coords[:, 0] < xupper) & (coords[:, 1] >= ylower) & (coords[:, 1] < yupper))[0]
    xbins = np.linspace(xlower, xupper, Nbins + 1, endpoint=True)
    ybins = np.linspace(ylower, yupper, Nbins + 1, endpoint=True)
    x_indices = np.digitize(coords[:, 0], xbins) - 1
    y_indices = np.digitize(coords[:, 1], ybins) - 1
    indices_map = [[[] for i in range(Nbins)] for j in range(Nbins)]

    for i in inr:
        indices_map[x_indices[i]][y_indices[i]].append(i)
    return indices_map

def find_ngb_list(target_coord_list, candidate_coord_list, boxsize, padding=0, workers=1):#returns the indices of the closest neighbors
    tree = KDTree(candidate_coord_list, boxsize=boxsize)
    indices_list = tree.query(target_coord_list, workers=workers)[1]
    return indices_list

def add_metallicity(field, data):#Add a metallicity data field to yt datasets
    factor = 1.0 # 1.0 solar metallicity
    return (
        data.ds.arr(np.ones_like(data["gas", "density"]), 'Zsun') * factor
    )

def add_metallicity_variable(field, data):#Used when the metallicity is proportional to the blob factor
    return (
        data.ds.arr(np.array(data["flash", "blob"]), 'Zsun')
    )
