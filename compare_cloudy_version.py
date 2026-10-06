import numpy as np
from matplotlib import pyplot as plt
import os

spectra_17_base = '/nas/astro-th/lyang/projectedColumns-main/spectra/HM_1e%d/spectral_lines_%s/z%g/t%d/'
spectra_23_base = '/nas/astro-th/lyang/projectedColumns-main/spectra23/HM_1e%d/spectral_lines_%s/z%g/t%d/'

absorber_17_base = spectra_17_base + 'absorbers_%s_%d_z%g_%s.txt'
absorber_23_base = spectra_23_base + 'absorbers_%s_%d_z%g_%s.txt'

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
        'f_list':['0022', '0033', '0053', '0073'],
        'f_list_full':['%04d' % i for i in range(105)]}

runx3 = { 'Name':'T1_v1700_chi1000_ld2',
         'Formal_name':'T1_v1700_chi1000',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0022', '0031', '0053', '0068'],
        'f_list_full':['%04d' % i for i in range(114)]}

runx4 = { 'Name':'T0.3_v1700_chi300_ld2',
         'Formal_name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        #'f_list':['0021', '0025', '0031', '0038', '0046', '0070'],
        'f_list':['0021', '0025', '0031', '0038'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(101)]}

runx5 = { 'Name':'T0.3_v3000_chi300_ld2',
         'Formal_name':'T0.3_v3000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0018', '0024', '0034', '0080'],
        'f_list_full':['%04d' % i for i in range(82)]}

runx6 = { 'Name':'T3_v3000_chi3000_ld2',
         'Formal_name':'T3_v3000_chi3000',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0022', '0026', '0032', '0044'],
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
        'f_list':['0006', '0010', '0022', '0035'],
        'f_list_full':['%04d' % i for i in range(61)]}

runx9 = { 'Name':'T1_v1700_chi1000_cond_ld2',
         'Formal_name':'T1_v1700_chi1000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0003', '0006', '0010', '0014'],
        'f_list_full':['%04d' % i for i in range(35)]}

runx10 = { 'Name':'T0.3_v1700_chi300_cond_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0005', '0008', '0017', '0038'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(75)]}

runx11 = { 'Name':'T0.3_v3000_chi300_cond_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0004', '0006', '0010', '0013'],
        'f_list_full':['%04d' % i for i in range(20)]}

runx12 = { 'Name':'T3_v3000_chi3000_cond_ld2',
         'Formal_name':'T3_v3000_chi3000_cond',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0003', '0004', '0006', '0010'],
        'f_list_full':['%04d' % i for i in range(31)]}

runx13 = { 'Name':'T1_v1700_chi1000_cond_0.1_ld2',
         'Formal_name':'T1_v1700_chi1000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0004', '0010', '0019', '0030'],
        'f_list_full':['%04d' % i for i in range(72)]}

runx14 = { 'Name':'T0.3_v1000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.8,
        'tcc':9.17,
        'velocity':1000,
        'f_list':['0010', '0026', '0047', '0070'],
        'f_list_full':['%04d' % i for i in range(131)]}

runx15 = { 'Name':'T3_v3000_chi3000_cond_0.1_ld2',
         'Formal_name':'T3_v3000_chi3000_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0003', '0005', '0009', '0013'],
        'f_list_full':['%04d' % i for i in range(27)]}

runx16 = { 'Name':'T0.3_v1700_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v1700_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0007', '0015', '0045', '0065'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(125)]}

runx17 = { 'Name':'T0.3_v3000_chi300_cond_0.1_ld2',
         'Formal_name':'T0.3_v3000_chi300_cond_0.1',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0005', '0008', '0012', '0018'],
        'f_list_full':['%04d' % i for i in range(79)]}

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
runlist.append(runx4)   #T0.3_v1700_chi300_ld2

ionlist = []
ionlist.append(ion10)   #H I
#ionlist.append(ion17)   #O I
ionlist.append(ion7)    #Mg II
#ionlist.append(ion14)   #Si II
#ionlist.append(ion4)    #C II
ionlist.append(ion8)    #Si III
ionlist.append(ion18)   #O II
ionlist.append(ion6)    #C III
#ionlist.append(ion19)   #O III
ionlist.append(ion2)    #C IV
ionlist.append(ion13)   #O IV
ionlist.append(ion1)    #O VI
ionlist.append(ion5)    #Ne VIII

HI_density_range = (11, 20)
#density_range = (12, 18)
density_range = (11, 17)
linewidth_range = (0, 100)
linewidth_range_scatter = (0, 50)

width_density_cut = 12
Nbins = 75

def compare_cloudy_version(run, time_num, redshift, HM_index, direction):
    run_name = run['Name']
    savepath = 'figures/%s/' % run_name
    os.makedirs(savepath, exist_ok=True)

    log_colden_17 = []
    linewidth_17 = []
    
    log_colden_23 = []
    linewidth_23 = []
    for ion in ionlist:
        data_17 = np.loadtxt(absorber_17_base % (HM_index, run_name, redshift, time_num, run_name, 10 * direction, redshift, ion['ion'].replace(' ', '_')))
        log_colden_17.append(np.log10(data_17[:, 1]))
        linewidth_17.append(data_17[:, 2])

        data_23 = np.loadtxt(absorber_23_base % (HM_index, run_name, redshift, time_num, run_name, 10 * direction, redshift, ion['ion'].replace(' ', '_')))
        log_colden_23.append(np.log10(data_23[:, 1]))
        linewidth_23.append(data_23[:, 2])
    
    plt.figure(figsize=(11, 15))
    for i in range(len(ionlist)):
        ion = ionlist[i]

        ax = plt.subplot(len(ionlist), 2, 2 * i + 1)
        if 'ld' in run_name:
            pixel_size = 10
            area_scale_factor = 1
        else:
            pixel_size = 2
            area_scale_factor = 29.3

        weights_17 = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_17[i])
        weights_23 = pixel_size ** 2 * area_scale_factor * 10 * np.ones_like(log_colden_23[i])

        if i == 0:
            binsize = (HI_density_range[1] - HI_density_range[0]) / Nbins
            weights_17 /= binsize
            weights_23 /= binsize
            ax.hist(log_colden_17[i], bins=Nbins, range=HI_density_range, histtype='step', weights=weights_17)
            ax.hist(log_colden_23[i], bins=Nbins, range=HI_density_range, histtype='step', weights=weights_23)
        else:
            binsize = (density_range[1] - density_range[0]) / Nbins
            weights_17 /= binsize
            weights_23 /= binsize
            ax.hist(log_colden_17[i], bins=Nbins, range=density_range, histtype='step', weights=weights_17)
            ax.hist(log_colden_23[i], bins=Nbins, range=density_range, histtype='step', weights=weights_23)
        
        ax.set_title(ion['ion'], fontsize=13)
        ax.set_yscale('log')

        if i == len(ionlist) - 1:
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
        #if i == 0:
            ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$', fontsize=15)
        ax.tick_params(which='both', direction='in', labelsize=13, right=True, top=True)
        ax.set_ylim(1e4, 2e7)

        ax = plt.subplot(len(ionlist), 2, 2 * i + 2)
        significant_list_17 = np.where(log_colden_17[i] > width_density_cut)[0]
        significant_list_23 = np.where(log_colden_23[i] > width_density_cut)[0]

        ax.hist(linewidth_17[i][significant_list_17], bins=Nbins, range=linewidth_range, density=True, histtype='step', label='Cloudy17')
        ax.hist(linewidth_23[i][significant_list_23], bins=Nbins, range=linewidth_range, density=True, histtype='step', label='Cloudy23')

        if i == 0:
            ax.legend(fontsize=13)
    plt.tight_layout()
    plt.savefig(savepath + 'compare_cloudy_versions.pdf', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    run = runx4
    time_num = 2
    redshift = 0.5396
    HM_index = 0
    direction = 0.5
    compare_cloudy_version(run, time_num, redshift, HM_index, direction)
