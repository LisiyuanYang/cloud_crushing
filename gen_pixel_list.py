import numpy as np

blob_colden_file_base = '/nas/astro-th/lyang/nonSorted_ColDen_23/blob0.5/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'

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

def get_all_pixels(run, redshift, timenum, direction, HM_index):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, 0, 0.5396, timenum, run_name, round(10 * direction))
    pixel_indices = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',', usecols=0)
    pixel_indices = pixel_indices.astype(int)
    return pixel_indices

if __name__ == '__main__':
    sample_rate = 0.1
    timenum_list = [0, 1, 2, 3]
    #redshift_list = [0.1006, 0.5396, 1.053, 2.013]
    redshift_list = [3.017, 4.895]
    #direction_list = [0.5, 0.00001, 1 - 1e-10]
    direction_list = [0.5, 0.00001, 1 - 1e-10, 0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]
    #HM_index_list = [0]
    HM_index_list = np.arange(-4, 5)

    for timenum in timenum_list:
        for direction in direction_list:
            for redshift in redshift_list:
                for HM_index in HM_index_list:
                    for run in runlist:
                        run_name = run['Name']
                        full_pixel_id_list = get_all_pixels(run, redshift, timenum, direction, HM_index)
                        rng = np.random.default_rng(seed = full_pixel_id_list[10])
                        pixel_id_list = rng.choice(full_pixel_id_list, round(len(full_pixel_id_list) * sample_rate), replace=False)
                        savepath = '/nas/astro-th/lyang/projectedColumns-main/spectra23/blob0.5/HM_1e%d/spectral_lines_%s/z%g/t%d/' % (HM_index, run_name, redshift, timenum)
                        saved_list = np.zeros((len(pixel_id_list), (len(ionlist) + 1)))
                        saved_list[:, 0] = pixel_id_list
                        for i in range(len(ionlist)):
                            ion = ionlist[i]
                            absorber_file = savepath + 'absorbers_%s_%d_z%g_%s.txt' % (run_name, round(10 * direction), redshift, ion['ion'].replace(' ', '_'))
                            pixel_id_thision = np.loadtxt(absorber_file, usecols=0, dtype=int)
                            for j in range(len(pixel_id_list)):
                                pixel_id = pixel_id_list[j]
                                ind = np.where(pixel_id_thision == pixel_id)[0]
                                if len(ind) > 0:
                                    saved_list[j, i + 1] = ind[0] * 100 + len(ind)

                        np.savetxt(savepath + 'pixel_info_%d.txt' % (round(10 * direction)), saved_list, fmt='%d', header='%d %d' % (len(full_pixel_id_list), len(pixel_id_list)))
