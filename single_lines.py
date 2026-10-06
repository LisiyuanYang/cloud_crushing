import numpy as np
from matplotlib import pyplot as plt
import sys
import os
import yt
import trident

ionTable_base = '/work/pi_nsk_umass_edu/lyang/newTridentTables/HM_shu/hm-1e%d-z%g/HM_1e%d.h5'
blob_colden_file_base = '/nas/astro-th/lyang/nonSorted_ColDen/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'

ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])
ion_indices = np.array([0, 10, 4, 6, 9]) #HI, Mg II, C IV, O VI, Ne VIII; indices in the colden files

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
ion10 = {'ion': 'H I 1216',
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
runlist.append(run1)
##runList.append(run2)
##runList.append(run3)
runlist.append(run4)
runlist.append(run11)
runlist.append(run12)
##runList.append(run13)
##runList.append(run14)
##runList.append(run15)
runlist.append(run16)
runlist.append(run17)

ionlist = []
ionlist.append(ion10)
ionlist.append(ion17)   #O I
ionlist.append(ion7)    #Mg II
ionlist.append(ion14)   #Si II
ionlist.append(ion4)    #C II
ionlist.append(ion8)    #Si III
ionlist.append(ion18)   #O II
ionlist.append(ion6)    #C III
ionlist.append(ion19)   #O III
ionlist.append(ion2)    #C IV
ionlist.append(ion13)   #O IV
ionlist.append(ion1)    #O VI
ionlist.append(ion5)    #Ne VIII

def _metallicity(field, data):
    factor = 1.0 # 1.0 solar metallicity
    return (
        data.ds.arr(np.ones_like(data["gas", "density"]), 'Zsun') * factor
    )

def _gas_blob(field, data):
    return data['flash', 'blob']

def ravel_map(indices, unravelled_map, Npix_x, Npix_y):
    if max(indices) >= Npix_x * Npix_y:
        print('Error! Index %d out of range for a %d * %d map.' % (max(indices), Npix_x, Npix_y))
        sys.exit(1)
    
    if len(indices) != len(unravelled_map):
        print('Error! Size of indices list must equal size of unravelled map.')
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

def choose_random_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, 10 * direction)
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(np.any(colden[:, 1:] > 3e12, axis=1))[0]

    rng = np.random.default_rng(seed = pixel_indices[10])
    return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)

def choose_OVI_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, 10 * direction)
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
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, 10 * direction)
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
    blob_colden_file = blob_colden_file_base % (run_name, HM_index, 0.5396, timenum, run_name, 10 * direction)
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

if __name__ == '__main__':
    timenum = 2
    Npix = 400
    pixel_size = 2
    direction = 0.5
    redshift_list = [0.1006, 0.5396]
    HM_index_list = [2, 2]
    blob_cut = 0.82

    projected_ylist = -(np.arange(0, Npix * pixel_size, pixel_size) - (0.5 * Npix * pixel_size) + 0.5 * pixel_size)
    projected_zlist = np.arange(0, Npix * pixel_size, pixel_size) - (0.5 * Npix * pixel_size) + 0.5 * pixel_size

    ion_field_list = []
    for ion in ionlist:
        field_name = ion['fieldname']
        ion_field_list.append(field_name)

    for k in range(len(HM_index_list)):
        redshift = redshift_list[k]
        HM_index = HM_index_list[k]
        ionTable = ionTable_base % (HM_index, redshift, HM_index)
        colden_scaling_factor = 10 ** (-2/3 * HM_index)

        trident.ion_balance.table_store = {} #Force trident to reload ionization tables
        for run in runlist:
            run_name = run['Name']
            pixel_id_list = choose_random_pixels(run, redshift, timenum, direction, HM_index, 10)
            pixel_id_OVI_list = choose_OVI_pixels(run, redshift, timenum, direction, HM_index, 10)
            pixel_id_MgII_list = choose_MgII_pixels(run, redshift, timenum, direction, HM_index, 10)
            pixel_id_CIV_list = choose_CIV_pixels(run, redshift, timenum, direction, HM_index, 10)

            print(redshift, run_name)
            data = yt.load(run['Dir'] + run_name + '/KH_hdf5_chk_' + run['f_list'][timenum])
            data.add_field(('gas', 'metallicity'), function=_metallicity, sampling_type='cell', display_name='Metallicity', units='Zsun')

            allDataRegion = data.all_data()
            c = allDataRegion.quantities.center_of_mass() #Can avoid cutting off the tail
            trident.add_ion_fields(data, ions=[ion['ion'] for ion in ionlist], ionization_table=ionTable)

            for pixel_id in pixel_id_list:
                #print(redshift, run_name, pixel_id)
                projected_yindex = pixel_id % Npix
                projected_zindex = int(pixel_id / Npix)
                projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                angle = np.arccos(direction)
                norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.

                los_center = c + deproject(projected_coord, angle) * yt.units.pc
                los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                
                ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity')] + ion_field_list)
                cloud_section = ray.all_data()
                ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                los_mean_vel = np.average(cloud_section['gas','velocity_los'],weights=cloud_section['gas','H_p0_number_density'])
                los_log_coldens = []
                for ion_field in ion_field_list:
                    cloud_section['gas', ion_field][ambient_indices] = 0
                    cloud_section['gas', ion_field] *= colden_scaling_factor
                    los_log_coldens.append(np.log10(np.dot(cloud_section['gas', ion_field], cloud_section['dl']))) #unit: cm^-2
                
                savepath = 'figures/HM_1e%d/spectral_lines_%s/normal/%d/z%g/' % (HM_index, run_name, pixel_id, redshift)
                os.makedirs(savepath, exist_ok=True)
                dvel = yt.units.YTQuantity(150, 'km/s')
                vmin = los_mean_vel - dvel
                vmax = los_mean_vel + dvel

                spectrum_list = []
                vlist = []
                for ion in ionlist:
                    if ion == ion10:
                        linename = ion['ion']
                    else:
                        linename = '%s %d' % (ion['ion'], round(ion['rest_wave']))
                    
                    sg = trident.SpectrumGenerator(lambda_min=vmin, lambda_max=vmax, dlambda=5., bin_space='velocity')
                    sg.make_spectrum(cloud_section, lines=[linename], ly_continuum=False, output_file='test.txt')
                    spectrum_list.append(np.exp(-sg.tau_field))
                    vlist.append(sg.lambda_field)
                    #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.clear_spectrum()
                
                plt.figure()
                gap = 1.1
                for i in range(len(ionlist)):
                    offset = (len(ionlist) - i - 1) * gap
                    plt.step(vlist[i] - los_mean_vel, spectrum_list[i] + offset, where='mid', lw=0.8, label='%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i]))
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=12)
                plt.yticks([])
                plt.xlabel('v/km/s', fontsize=12)
                plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, 10 * direction, pixel_id, redshift), bbox_inches='tight')
                plt.close()

            for pixel_id in pixel_id_OVI_list:
                #print(run_name, pixel_id)
                projected_yindex = pixel_id % Npix
                projected_zindex = int(pixel_id / Npix)
                projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                angle = np.arccos(direction)
                norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.
                                
                los_center = c + deproject(projected_coord, angle) * yt.units.pc

                los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                
                ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity')] + ion_field_list)
                cloud_section = ray.all_data()
                ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                los_mean_vel = np.average(cloud_section['gas','velocity_los'],weights=cloud_section['gas','H_p0_number_density'])
                los_log_coldens = []
                for ion_field in ion_field_list:
                    cloud_section['gas', ion_field][ambient_indices] = 0
                    cloud_section['gas', ion_field] *= colden_scaling_factor
                    los_log_coldens.append(np.log10(np.dot(cloud_section['gas', ion_field], cloud_section['dl']))) #unit: cm^-2
                
                savepath = 'figures/HM_1e%d/spectral_lines_%s/OVI/%d/z%g/' % (HM_index, run_name, pixel_id, redshift)
                os.makedirs(savepath, exist_ok=True)
                dvel = yt.units.YTQuantity(200, 'km/s')
                vmin = los_mean_vel - dvel
                vmax = los_mean_vel + dvel

                spectrum_list = []
                vlist = []
                for ion in ionlist:
                    if ion == ion10:
                        linename = ion['ion']
                    else:
                        linename = '%s %d' % (ion['ion'], round(ion['rest_wave']))
                    
                    sg = trident.SpectrumGenerator(lambda_min=vmin, lambda_max=vmax, dlambda=5., bin_space='velocity')
                    sg.make_spectrum(cloud_section, lines=[linename], ly_continuum=False, output_file='test.txt')
                    spectrum_list.append(np.exp(-sg.tau_field))
                    vlist.append(sg.lambda_field)
                    #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.clear_spectrum()
                
                plt.figure()
                gap = 1.1
                for i in range(len(ionlist)):
                    offset = (len(ionlist) - i - 1) * gap
                    plt.step(vlist[i] - los_mean_vel, spectrum_list[i] + offset, where='mid', lw=0.8, label='%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i]))
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=12)
                plt.yticks([])
                plt.xlabel('v/km/s', fontsize=12)
                plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, 10 * direction, pixel_id, redshift), bbox_inches='tight')
                plt.close()
            
            for pixel_id in pixel_id_MgII_list:
                #print(run_name, pixel_id)
                projected_yindex = pixel_id % Npix
                projected_zindex = int(pixel_id / Npix)
                projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                angle = np.arccos(direction)
                norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.
                                
                los_center = c + deproject(projected_coord, angle) * yt.units.pc

                los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                
                ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity')] + ion_field_list)
                cloud_section = ray.all_data()
                ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                los_mean_vel = np.average(cloud_section['gas','velocity_los'],weights=cloud_section['gas','H_p0_number_density'])
                los_log_coldens = []
                for ion_field in ion_field_list:
                    cloud_section['gas', ion_field][ambient_indices] = 0
                    cloud_section['gas', ion_field] *= colden_scaling_factor
                    los_log_coldens.append(np.log10(np.dot(cloud_section['gas', ion_field], cloud_section['dl']))) #unit: cm^-2
                
                savepath = 'figures/HM_1e%d/spectral_lines_%s/MgII/%d/z%g/' % (HM_index, run_name, pixel_id, redshift)
                os.makedirs(savepath, exist_ok=True)
                dvel = yt.units.YTQuantity(200, 'km/s')
                vmin = los_mean_vel - dvel
                vmax = los_mean_vel + dvel

                spectrum_list = []
                vlist = []
                for ion in ionlist:
                    if ion == ion10:
                        linename = ion['ion']
                    else:
                        linename = '%s %d' % (ion['ion'], round(ion['rest_wave']))
                    
                    sg = trident.SpectrumGenerator(lambda_min=vmin, lambda_max=vmax, dlambda=5., bin_space='velocity')
                    sg.make_spectrum(cloud_section, lines=[linename], ly_continuum=False, output_file='test.txt')
                    spectrum_list.append(np.exp(-sg.tau_field))
                    vlist.append(sg.lambda_field)
                    #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.clear_spectrum()
                
                plt.figure()
                gap = 1.1
                for i in range(len(ionlist)):
                    offset = (len(ionlist) - i - 1) * gap
                    plt.step(vlist[i] - los_mean_vel, spectrum_list[i] + offset, where='mid', lw=0.8, label='%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i]))
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=12)
                plt.yticks([])
                plt.xlabel('v/km/s', fontsize=12)
                plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, 10 * direction, pixel_id, redshift), bbox_inches='tight')
                plt.close()
            
            for pixel_id in pixel_id_CIV_list:
                #print(run_name, pixel_id)
                projected_yindex = pixel_id % Npix
                projected_zindex = int(pixel_id / Npix)
                projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                angle = np.arccos(direction)
                norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.
                                
                los_center = c + deproject(projected_coord, angle) * yt.units.pc

                los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                
                ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity')] + ion_field_list)
                cloud_section = ray.all_data()
                ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                los_mean_vel = np.average(cloud_section['gas','velocity_los'],weights=cloud_section['gas','H_p0_number_density'])
                los_log_coldens = []
                for ion_field in ion_field_list:
                    cloud_section['gas', ion_field][ambient_indices] = 0
                    cloud_section['gas', ion_field] *= colden_scaling_factor
                    los_log_coldens.append(np.log10(np.dot(cloud_section['gas', ion_field], cloud_section['dl']))) #unit: cm^-2
                
                savepath = 'figures/HM_1e%d/spectral_lines_%s/CIV/%d/z%g/' % (HM_index, run_name, pixel_id, redshift)
                os.makedirs(savepath, exist_ok=True)
                dvel = yt.units.YTQuantity(200, 'km/s')
                vmin = los_mean_vel - dvel
                vmax = los_mean_vel + dvel

                spectrum_list = []
                vlist = []
                for ion in ionlist:
                    if ion == ion10:
                        linename = ion['ion']
                    else:
                        linename = '%s %d' % (ion['ion'], round(ion['rest_wave']))
                    
                    sg = trident.SpectrumGenerator(lambda_min=vmin, lambda_max=vmax, dlambda=5., bin_space='velocity')
                    sg.make_spectrum(cloud_section, lines=[linename], ly_continuum=False, output_file='test.txt')
                    spectrum_list.append(np.exp(-sg.tau_field))
                    vlist.append(sg.lambda_field)
                    #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, 10 * direction, pixel_id, ion['ion'].replace(' ', '_')))
                    sg.clear_spectrum()
                
                plt.figure()
                gap = 1.1
                for i in range(len(ionlist)):
                    offset = (len(ionlist) - i - 1) * gap
                    plt.step(vlist[i] - los_mean_vel, spectrum_list[i] + offset, where='mid', lw=0.8, label='%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i]))
                plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=12)
                plt.yticks([])
                plt.xlabel('v/km/s', fontsize=12)
                plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, 10 * direction, pixel_id, redshift), bbox_inches='tight')
                plt.close()
