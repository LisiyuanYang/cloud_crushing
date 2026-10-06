import numpy as np
from matplotlib import pyplot as plt
import os

blob_colden_file_base = '/nas/astro-th/lyang/nonSorted_ColDen/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
blob_width_file_base = '/nas/astro-th/lyang/nonSorted_ColDen/%s/HM_1e%d/TF0.6/z%g/t%d/%s_width_%d.csv'
absorber_file_base = '/nas/astro-th/lyang/projectedColumns-main/spectra/HM_1e%d/spectral_lines_%s/z%g/t%d/absorbers_%s_%d_z%g_%s.txt'

ion_list = ['H I', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV', 'N V']
ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])

indices = np.array([0, 10, 12, 3, 4, 6, 9]) #HI, Mg II, Si III, C III, C IV, O VI, Ne VIII

run1 = { 'Name':'T0.3_v1000_chi300_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':3.8,
    'tcc':1.7,
    'velocity':1000,
    'f_list':['0013', '0038', '0080', '0132']}
run2 = { 'Name':'T3_v3000_chi3000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':3.6,
    'tcc':1.8,
    'velocity':3000,
    'f_list':['0001', '0004', '0007', '0010']}
run3 = { 'Name':'T1_v1700_chi1000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':3.5,
    'tcc':1.8,
    'velocity':1700,
    'f_list':['0002', '0010', '0017', '0028']}
run4 = { 'Name':'T0.3_v1000_chi300',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.8,
    'tcc':1.7,
    'velocity':1000,
    'f_list':['0025', '0033', '0042', '0058']}
run5 = { 'Name':'T3_v3000_chi3000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.6,
    'tcc':1.8,
    'velocity':3000,
    'f_list':['0021', '0030', '0040', '0062']}
run6 = { 'Name':'T1_v1700_chi1000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.5,
    'tcc':1.8,
    'velocity':1700,
    'f_list':['0021', '0029', '0038', '0052']}
run7 = { 'Name':'HC_v1000_chi300_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':3.8,
    'tcc':1.8,
    'velocity':1000,
    'f_list':['0054', '0060', '0080', '0107']}
run8 = { 'Name':'HC_v1700_chi1000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':3.5,
    'tcc':1.8,
    'velocity':1700,
    'f_list':['0024', '0050', '0082', '0083']}
run9 = { 'Name':'HC_v3000_chi3000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':3.6,
    'tcc':1.8,
    'velocity':3000,
    'f_list':['0007', '0015', '0026', '0049']}
run10 = { 'Name':'LowCond_v1700_chi300_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':6.5,
    'tcc':1.0,
    'velocity':1700,
    'f_list':['0016', '0075', '0115', '0184']}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':6.5,
    'tcc':1.0,
    'velocity':1700,
    'f_list':['0003', '0020', '0046', '0078']}
    #'f_list':['0078']}

run12 = { 'Name':'T0.3_v3000_chi300_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':11.4,
    'tcc':0.56,
    'velocity':3000,
    'f_list':['0001', '0004', '0014', '0035']}
run13 = { 'Name':'T3_v860_chi3000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':1.0,
    'tcc':6.2,
    'velocity':860,
    'f_list':['0001', '0003', '0006', '0010']}
run14 = { 'Name':'T10_v1500_chi10000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':1.0,
    'tcc':6.5,
    'velocity':1500,
    'f_list':['0001', '0002', '0004', '0008']}
run15 = { 'Name':'T1_v480_chi1000_cond',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':1.0,
    'tcc':6.4,
    'velocity':480,
    'f_list':['0002', '0009', '0017', '0031']}

run16 = { 'Name':'T0.3_v1700_chi300',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':6.5,
    'tcc':1.0,
    'velocity':1700,
    'f_list':['0022', '0032', '0053', '0085']}
run17 = { 'Name':'T0.3_v3000_chi300',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':11.4,
    'tcc':0.56,
    'velocity':3000,
    'f_list':['0028', '0044', '0065', '0110']}
run18 = { 'Name':'T3_v430_chi3000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':0.5,
    'velocity':430,
    'tcc':12.5,
    'f_list':['0010', '0011', '0016', '0024']}
run19 = { 'Name':'T3_v860_chi3000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':1.0,
    'velocity':860,
    'tcc':6.2,
    'f_list':['0010', '0018', '0030', '0038']}
run20 = { 'Name':'T1_v3000_chi1000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':6.2,
    'velocity':3000,
    'tcc':1.0,
    'f_list':['0022', '0032', '0048', '0095']}
run21 = { 'Name':'T10_v1500_chi10000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':1.0,
    'velocity':1500,
    'tcc':6.5,
    'f_list':['0014', '0021', '0029', '0044']}
run22 = { 'Name':'T1_v480_chi1000',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':1.0,
    'velocity':480,
    'tcc':6.4,
    'f_list':['0009', '0013', '0024', '0035']}
#run23 = { 'Name':'T1_v1700_chi1000_lref6',
#    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
#    'Mach':3.5,
#    'velocity':1700,
#    'tcc':1.8,
#    'f_list':['0021', '0029', '0038']}
run24 = { 'Name':'CoolFloor2e4',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
    'Mach':6.5,
    'velocity':1700,
    'tcc':1.0,
    'f_list':['0010', '0020', '0098', '0103']}

run25 = { 'Name':'T0.5_v340_chi500',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':1.0,
    'velocity':340,
    'tcc':6.4,
    'f_list':['0010', '0020', '0098', '0103']}

#add the runs to the list that will have columns ranked
runlist = []
##add only the 3 different conduction levels
runlist.append(run1)
runlist.append(run4)
runlist.append(run11)
runlist.append(run12)
runlist.append(run16)
runlist.append(run17)

#colors = ['blue', 'cyan', 'green', 'lime', 'red', 'orange', 'pink']
colors = ['blue', 'cyan']
HI_density_range = (11, 20)
density_range = (11, 16.5)
width_range = (-0.3, 2.5)

if __name__ == '__main__':
    redshift = 0.1006
    HM_index = 2
    scaling_factor_metal = -2/3 * HM_index #Assuming fixed cloud mass, this number should be -2/3 times the background boost factor.

    for j in range(len(runlist)):
        run = runlist[j]
        run_name = run['Name']
        direction = 0.5
        timenum = 2

        savepath = 'figures/HM_1e%d/compare_densities/z%g/' % (HM_index, redshift)
        os.makedirs(savepath, exist_ok=True)

        real_colden_list = np.loadtxt(blob_colden_file_base % (run_name, HM_index, redshift, timenum, run_name, 10 * direction), skiprows=1, delimiter=',')[:, indices + 1]
        real_width_list = np.loadtxt(blob_width_file_base % (run_name, HM_index, redshift, timenum, run_name, 10 * direction), skiprows=1, delimiter=',')[:, indices + 1]
        real_colden_list *= 10 ** scaling_factor_metal

        log_real_colden_list = np.log10(real_colden_list)
        log_real_width_list = np.log10(real_width_list) - 5

        log_absorber_colden_list = []
        log_absorber_width_list = []

        for i in range(len(indices)):
            ion_index = indices[i]
            ion_name = ion_list[ion_index]

            absorber_file = absorber_file_base % (HM_index, run_name, redshift, timenum, run_name, 10 * direction, redshift, ion_name.replace(' ', '_'))
            absorber_colden, absorber_width = np.loadtxt(absorber_file, usecols=(1, 2), unpack=True)

            log_absorber_colden_list.append(np.log10(absorber_colden) + scaling_factor_metal)
            log_absorber_width_list.append(np.log10(absorber_width))

        plt.figure(figsize=(8, 18))
        for i in range(len(indices)):
            ion_index = indices[i]
            ion_name = ion_list[ion_index]
            weights_real = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_real_colden_list[:, i])
            weights_absorber = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_absorber_colden_list[i]) * 10
            
            ax = plt.subplot(len(indices), 2, 2 * i + 1)
            
            if i == 0:
                ax.hist(log_real_colden_list[:, i], bins=75, range=HI_density_range, histtype='step', weights=weights_real, label='real')
                ax.hist(log_absorber_colden_list[i], bins=75, range=HI_density_range, histtype='step', weights=weights_absorber, label='fitted')
                ax.legend(fontsize=15)
            else:
                ax.hist(log_real_colden_list[:, i], bins=75, range=density_range, histtype='step', weights=weights_real)
                ax.hist(log_absorber_colden_list[i], bins=75, range=density_range, histtype='step', weights=weights_absorber)
                
            ax.set_title(ion_name, fontsize=15)
            ax.set_yscale('log')
            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)

            ax = plt.subplot(len(indices), 2, 2 * i + 2)

            significant_list_real = np.where(log_real_colden_list[:, i] > 12)[0]
            significant_list_absorber = np.where(log_absorber_colden_list[i] > 12)[0]

            ax.hist(log_real_width_list[significant_list_real, i], bins=75, range=width_range, histtype='step', weights=weights_real[significant_list_real])
            ax.hist(log_absorber_width_list[i][significant_list_absorber], bins=75, range=width_range, histtype='step', weights=weights_absorber[significant_list_absorber], label='fitted')

            ax.set_yscale('log')
            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            ax.set_xlabel(r'$\log(b/\mathrm{km/s})$', fontsize=15)
        
        plt.tight_layout()
        plt.savefig(savepath + '%s_%d_z%g_t%d.pdf' % (run_name, 10 * direction, redshift, timenum))
