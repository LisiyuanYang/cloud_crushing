import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import sys
import os
import yt
import trident
from trident.absorption_spectrum.absorption_spectrum_fit import generate_total_fit
from trident.absorption_spectrum.absorption_line import tau_profile
from cloud_util import runs, ions

ionTable_base = '/work/pi_nsk_umass_edu/lyang/newTridentTables/Cloudy23/hm-1e%d-z%g/HM_1e%d.h5'
#blob_colden_file_base = '/nas/astro-th/lyang/nonSorted_ColDen_23/blob0.5/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
#blob_colden_file_base = '/nas/astro-th/lyang/nonSorted_ColDen_23/blob0.5_bk/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
blob_colden_file_base = '%s/nonSorted_ColDen_23/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'

ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])
ion_indices = np.array([0, 10, 4, 6, 9]) #HI, Mg II, C IV, O VI, Ne VIII; indices in the colden files

#add the runs to the list that will have columns ranked
run_list = []
##add only the 3 different conduction levels
#runlist.append(runs['run4'])    #T0.3_v1000_chi300
#runlist.append(runs['runx2'])   #T0.3_v1000_chi300_ld2
#runlist.append(runs['run1'])   #T0.3_v1000_chi300_cond
#runlist.append(runs['runx14'])   #T0.3_v1000_chi300_cond_0.1_ld2
#runlist.append(runs['runx8'])   #T0.3_v1000_chi300_cond_ld2

#runlist.append(runs['run16'])  #T0.3_v1700_chi300
#runlist.append(runs['runx4'])   #T0.3_v1700_chi300_ld2
#runlist.append(runs['run11'])  #T0.3_v1700_chi300_cond
#runlist.append(runs['runx16'])   #T0.3_v1700_chi300_cond_0.1_ld2
#runlist.append(runs['runx10'])  #T0.3_v1700_chi300_cond_lds

#runlist.append(runs['run17'])  #T0.3_v3000_chi300
#runlist.append(runs['runx5'])   #T0.3_v3000_chi300_ld2
#runlist.append(runs['run12'])  #T0.3_v3000_chi300_cond
#runlist.append(runs['runx17'])   #T0.3_v3000_chi300_cond_0.1_ld2
#runlist.append(runs['runx11'])  #T0.3_v3000_chi300_cond_ld2

#runlist.append(runs['run6'])   #T1_v1700_chi1000
#runlist.append(runs['runx3'])   #T1_v1700_chi1000_ld2
#runlist.append(runs['run3'])   #T1_v1700_chi1000_cond
#runlist.append(runs['runx13'])   #T1_v1700_chi1000_cond_0.1_ld2
#runlist.append(runs['runx9'])   #T1_v1700_chi1000_cond_ld2

#runlist.append(runs['run5'])   #T3_v3000_chi3000
#runlist.append(runs['runx6'])   #T3_v3000_chi3000_ld2
#runlist.append(runs['run2'])   #T3_v3000_chi3000_cond
#runlist.append(runs['runx15'])   #T3_v3000_chi3000_cond_0.1_ld2
#runlist.append(runs['runx12'])   #T3_v3000_chi3000_cond_ld2

#runlist.append(runs['runy1'])   #T0.1_v150_chi100_ld2
#runlist.append(runs['runy2'])   #T0.1_v150_chi100_cond_0.1_ld2

#runlist.append(runs['runz1'])   #T0.1_v150_chi100_cond_0.1_ld2
run_list.append(runs['runp1'])
run_list.append(runs['runp2'])
run_list.append(runs['runp3'])
run_list.append(runs['runp4'])
run_list.append(runs['runp5'])
run_list.append(runs['runp6'])
run_list.append(runs['runp7'])
run_list.append(runs['runp8'])
run_list.append(runs['runp9'])
#run_list.append(runs['runp9b'])
run_list.append(runs['runp10'])
run_list.append(runs['runp11'])
run_list.append(runs['runp12'])
run_list.append(runs['runp13'])
#run_list.append(runs['runp14'])
run_list.append(runs['runp15'])
run_list.append(runs['runp16'])
run_list.append(runs['runp17'])
run_list.append(runs['runp18'])

ionlist = []
ionlist.append(ions['H I'])   #H I
ionlist.append(ions['O I'])   #O I
ionlist.append(ions['Mg II'])    #Mg II
ionlist.append(ions['Si II'])   #Si II
ionlist.append(ions['C II'])    #C II
ionlist.append(ions['Si III'])    #Si III
ionlist.append(ions['O II'])   #O II
ionlist.append(ions['Si IV'])    #Si IV
ionlist.append(ions['C III'])    #C III
ionlist.append(ions['O III'])   #O III
ionlist.append(ions['C IV'])    #C IV
ionlist.append(ions['O IV'])   #O IV
ionlist.append(ions['O VI'])    #O VI
ionlist.append(ions['Ne VIII'])    #Ne VIII

ldb = trident.LineDatabase('lines.txt')
lines = ldb.parse_subset(['%s %d' % (ion['ion'], round(ion['rest_wave'])) for ion in ionlist])

def _metallicity(field, data):
    factor = 1.0 # 1.0 solar metallicity
    return (
        data.ds.arr(np.ones_like(data["gas", "density"]), 'Zsun') * factor
    )

def _metallicity_variable(field, data):
    return (
        data.ds.arr(np.array(data["flash", "metl"]), 'Zsun')
    )

def _gas_blob(field, data):
    return data['flash', 'blob']

def ravel_map(indices, unravelled_map, Npix_x, Npix_y):
    if max(indices) >= Npix_x * Npix_y:
        print('Error! Index %d out of range for a %d * %d map.' % (max(indices), Npix_x, Npix_y), file=sys.stderr, flush=True)
        sys.exit(1)
    
    if len(indices) != len(unravelled_map):
        print('Error! Size of indices list must equal size of unravelled map.', file=sys.stderr, flush=True)
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
    blob_colden_file = blob_colden_file_base % (run['Dir'] + run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    #colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(np.any(colden[:, 1:] > 1e13, axis=1))[0]
    if len(valid_pixels) > Npixels:
        rng = np.random.default_rng(seed = pixel_indices[10])
        return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)
    else:
        return pixel_indices[valid_pixels]

def choose_OVI_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run['Dir'] + run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    #colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(colden[:, 3] > 1e13)[0]
    if len(valid_pixels) > Npixels:
        rng = np.random.default_rng(seed = pixel_indices[20])
        return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)
    else:
        return pixel_indices[valid_pixels]

def choose_MgII_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run['Dir'] + run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    #colden *= 10 ** (-2/3 * HM_index)
    valid_pixels = np.where(colden[:, 1] > 1e13)[0]
    if len(valid_pixels) > Npixels:
        rng = np.random.default_rng(seed = pixel_indices[30])
        return rng.choice(pixel_indices[valid_pixels], Npixels, replace=False)
    else:
        return pixel_indices[valid_pixels]

def choose_CIV_pixels(run, redshift, timenum, direction, HM_index, Npixels):
    run_name = run['Name']
    blob_colden_file = blob_colden_file_base % (run['Dir'] + run_name, HM_index, 0.5396, timenum, run_name, round(10 * direction))
    colden = np.loadtxt(blob_colden_file, skiprows=1, delimiter=',')
    pixel_indices = colden[:, 0].astype(int)
    colden = colden[:, ion_indices + 1]
    
    #colden *= 10 ** (-2/3 * HM_index)
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

def make_individual_line(line, colden, z, b, vlist):#b is in km/s
    voffset = z * yt.units.physical_constants.c.to('cm/s').value
    rest_lambda = line.wavelength
    lambda_bins = rest_lambda * (1 + vlist / yt.units.physical_constants.c.to('km/s').value)
    return tau_profile(line.wavelength, line.f_value, line.gamma, b * 1e5, colden, delta_v=voffset, lambda_bins=lambda_bins)[1]

if __name__ == '__main__':
    #timelist = np.arange(4)
    timelist = [2]
    Npix = 600
    
    direction = 1 - 1e-10
    #direction = 0.00001
    redshift_list = [0.1006, 0.5396]
    #HM_index_list = [0, 0]
    HM_index_list = [0]

    #redshift_list = [0.1006]
#    HM_index_list = [2]
    #blob_cut = 0.82
    #blob_cut = 0.5
    blob_cut = 0
    #blob_cut = -1
    #init_N_list = [1e12, 1e12, 3e12, 3e12, 1e13, 1e13, 3e13, 3e13, 1e14, 1e14, 3e14, 3e14]
    #init_b_list = [10, 40, 10, 40, 10, 40, 10, 40, 10, 40, 10, 40]
    #init_b_list_MgII = [1, 10, 1, 10, 1, 10, 1, 10, 1, 10, 1, 10]

    init_N_list = [1e13]
    init_b_list = [6]
    init_b_list_HI = [12]

    vel_range = yt.units.YTQuantity(150, 'km/s')
    dvel = yt.units.YTQuantity(5, 'km/s')
    dvel_fine = yt.units.YTQuantity(5, 'km/s')
    vlist = yt.YTArray(np.arange(-vel_range, vel_range + 0.5 * dvel, dvel), 'km/s')
    vlist_fine = yt.YTArray(np.arange(-vel_range, vel_range + 0.5 * dvel_fine, dvel_fine), 'km/s')

    ion_field_list = []
    for j in range(len(ionlist)):
        ion = ionlist[j]
        field_name = ion['fieldname']
        ion_field_list.append(field_name)

    for k in range(len(redshift_list)):
        redshift = redshift_list[k]
        for l in range(len(HM_index_list)):
            HM_index = HM_index_list[l]
            ionTable = ionTable_base % (HM_index, redshift, HM_index)
            #colden_scaling_factor = 10 ** (-2/3 * HM_index)
            colden_scaling_factor = 1

            trident.ion_balance.table_store = {} #Force trident to reload ionization tables
            for run in run_list:
                pixel_size = 12 * run['radius'] / Npix
                projected_ylist = -(np.arange(0, Npix * pixel_size, pixel_size) - (0.5 * Npix * pixel_size) + 0.5 * pixel_size)
                projected_zlist = np.arange(0, Npix * pixel_size, pixel_size) - (0.5 * Npix * pixel_size) + 0.5 * pixel_size
                for timenum in timelist:
                    run_name = run['Name']
                    pixel_id_list = choose_random_pixels(run, redshift, timenum, direction, HM_index, 10)
                    pixel_id_OVI_list = choose_OVI_pixels(run, redshift, timenum, direction, HM_index, 10)
                    pixel_id_MgII_list = choose_MgII_pixels(run, redshift, timenum, direction, HM_index, 10)
                    pixel_id_CIV_list = choose_CIV_pixels(run, redshift, timenum, direction, HM_index, 10)

                    print(redshift, run_name, flush=True)
                    data = yt.load(run['Dir'] + run_name + '/%s' % (run['name_template'] % int(run['f_list'][timenum])))
                    #data.add_field(('gas', 'metallicity'), function=_metallicity, sampling_type='cell', display_name='Metallicity', units='Zsun')
                    data.add_field(('gas', 'metallicity'), function=_metallicity_variable, sampling_type='cell', display_name='Metallicity', units='Zsun')

                    allDataRegion = data.all_data()
                    #c = allDataRegion.quantities.center_of_mass() #Can avoid cutting off the tail
                    c = data.domain_center
                    trident.add_ion_fields(data, ions=[ion['ion'] for ion in ionlist], ionization_table=ionTable)

                    for pixel_id in pixel_id_list:
                        projected_yindex = pixel_id % Npix
                        projected_zindex = int(pixel_id / Npix)
                        projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                        angle = np.arccos(direction)
                        norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.

                        los_center = c + deproject(projected_coord, angle) * yt.units.pc
                        los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        
                        ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity'), ('gas', 'density')] + ion_field_list)
                        cloud_section = ray.all_data()

                        los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section['gas','H_p0_number_density'])
                        ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                        #ambient_indices = np.where(abs(cloud_section['gas','velocity_los'] - los_mean_vel) > vel_range)[0]

                        cloud_section['gas', 'density'][ambient_indices] = 0
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
                        
                        savepath = 'figures/HM_1e%d/spectral_lines_%s/t%d/%d/normal/%d/z%g/' % (HM_index, run_name, timenum, round(10 * direction), pixel_id, redshift)
                        os.makedirs(savepath, exist_ok=True)

                        vmin = los_mean_vel - vel_range
                        vmax = los_mean_vel + vel_range
                        minz = (vmin / yt.units.physical_constants.c).value
                        maxz = (vmax / yt.units.physical_constants.c).value

                        spectrum_list = []
                        fitted_flux_list = []
                        fitted_line_list = []

                        for j in range(len(ionlist)):
                            ion = ionlist[j]
                            line = lines[j]
                            linename = line.name
                            rest_lambda = line.wavelength

                            #spec_los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section[line.field])
                            #spec_los_mean_vel2 = np.average(cloud_section['gas','velocity_los'] ** 2, weights=cloud_section[line.field])
                            #spec_los_sigma_2 = (spec_los_mean_vel2 - spec_los_mean_vel ** 2).to('cm**2/s**2').value
        #
                            #spec_los_mean_temp = np.average(cloud_section['gas', 'temperature'], weights=cloud_section[line.field]).value

                            lambda_min = rest_lambda * (1 + minz)
                            lambda_max = rest_lambda * (1 + maxz)
                            dlambda = rest_lambda * (dvel / yt.units.physical_constants.c).value
                                                
                            sg = trident.SpectrumGenerator(lambda_min=lambda_min, lambda_max=lambda_max, dlambda=dlambda)
                            sg.make_spectrum(cloud_section, lines=[linename], min_tau=1e-8, ly_continuum=False)
                            fluxes = np.exp(-sg.tau_field * colden_scaling_factor)
                            lambda_field = sg.lambda_field
                            spectrum_list.append(fluxes)

                            max_tau = max(sg.tau_field)
                            tau_scaling_factor = 1
                            if max_tau > 1e-4:
                                tau_scaling_factor = 4 / max_tau
                            rescaled_tau = sg.tau_field * tau_scaling_factor #Scale the optical depths to avoid saturation
                            rescaled_fluxes = np.exp(-rescaled_tau)

                            #vlist.append(sg.lambda_field)
                            #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            #sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))

                            #Fit the spectrum
                            fitted_flux_local = []
                            fitted_lines_local = []
                            err = []
                            for l in range(len(init_N_list)):
                                init_N = init_N_list[l]
                                init_b = init_b_list[l]
                                tolerance = 1e-4
                                if linename == 'H I 1216':
                                    init_b = init_b_list_HI[l]
                                    tolerance = 1e-7
                                if tau_scaling_factor != 1:
                                    max_N = 1.1 * 10 ** los_log_coldens[j] * tau_scaling_factor
                                else:
                                    max_N = 1e14
                                max_b = 250
                                try:
                                    speciesDicts = gen_line_dict(line, minz, maxz, init_N, init_b, max_N, max_b)
                                    fitted_lines, fitted_flux = generate_total_fit(lambda_field, rescaled_fluxes, orderFits=[linename], speciesDicts=speciesDicts, minError=tolerance, complexLim=0.9995, fitLim=0.994, maxNumComps=12)
                                    fitted_flux_local.append(fitted_flux)
                                    fitted_lines_local.append(fitted_lines)
                                    err.append(np.sum((fitted_flux - rescaled_fluxes) ** 2))
                                except:
                                    pass
                            
                            if len(fitted_flux_local) > 0:
                                best_set = np.argmin(err)

                                fitted_flux_list.append(fitted_flux_local[best_set] ** (colden_scaling_factor / tau_scaling_factor))
                                fitted_lines = fitted_lines_local[best_set]
                                fitted_lines[linename]['N'] /= tau_scaling_factor

                                if len(fitted_lines[linename]['N']) == 0:
                                    fitted_line_list.append([])
                                else:
                                    fitted_line_list.append(fitted_lines)
                            else:
                                fitted_flux_list.append([])
                                fitted_line_list.append([])
                            '''
                            speciesDicts = gen_line_dict(line, minz, maxz)
                            fitted_lines, fitted_flux = generate_total_fit(lambda_field, fluxes, orderFits=[linename], speciesDicts=speciesDicts, complexLim=0.9995, fitLim=0.994, output_file=\
                                                                        savepath + '%s_%d_%d_%s_fit.h5' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            fitted_list.append(fitted_flux)
                            '''
                            sg.clear_spectrum()
                        
                        plt.figure()
                        gap = 1.1
                        for i in range(len(ionlist)):
                            offset = (len(ionlist) - i - 1) * gap
                            label = '%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i] + np.log10(colden_scaling_factor))
                            line = lines[i]
                            linename = line.name
                            fitted_lines_saved = fitted_line_list[i]
                            individual_spectra_list = []
                            if fitted_lines_saved != []:
                                lines_sorted = np.argsort(-fitted_lines_saved[linename]['N'])
                                Nlist = fitted_lines_saved[linename]['N'][lines_sorted] * colden_scaling_factor
                                blist = fitted_lines_saved[linename]['b'][lines_sorted]
                                zlist = fitted_lines_saved[linename]['z'][lines_sorted]
                                centroid_list = zlist * yt.units.physical_constants.c.to('km/s').value - los_mean_vel.to('km/s').value
                                label += ', %.2f (' % np.log10(np.sum(Nlist))

                                for line_ind in range(len(Nlist)):
                                    individual_spectra_list.append(np.exp(-make_individual_line(line, Nlist[line_ind], zlist[line_ind], blist[line_ind], (vlist_fine + los_mean_vel).value)))
                                    #label += '%.2f' % np.log10(Nlist[line_ind])
                                    label += r'$^{%.2f}_{%.1f}$' % (np.log10(Nlist[line_ind]), centroid_list[line_ind])
                                    if line_ind != len(Nlist) - 1:
                                        label += ', '
                                    else:
                                        label += ')'

                            myplot, = plt.step(vlist, spectrum_list[i] + offset, where='mid', lw=1.5, label=label)
                            if fitted_lines_saved != []:
                                plt.step(vlist, fitted_flux_list[i] + offset, where='mid', lw=1, ls='--', c=myplot.get_color())
                                for individual_spectrum in individual_spectra_list:
                                    plt.step(vlist_fine, individual_spectrum + offset, where='mid', lw=1, ls=':', c=myplot.get_color())
                        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=15)
                        plt.yticks([])
                        plt.xlabel('v/km/s', fontsize=12)
                        plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, round(10 * direction), pixel_id, redshift), bbox_inches='tight')
                        plt.close()
                    
                    for pixel_id in pixel_id_OVI_list:
                        #print(redshift, run_name, pixel_id)
                        projected_yindex = pixel_id % Npix
                        projected_zindex = int(pixel_id / Npix)
                        projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                        angle = np.arccos(direction)
                        norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.

                        los_center = c + deproject(projected_coord, angle) * yt.units.pc
                        los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        
                        ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity'), ('gas', 'density')] + ion_field_list)
                        cloud_section = ray.all_data()
                        
                        los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section['gas','H_p0_number_density'])
                        ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                        #ambient_indices = np.where(abs(cloud_section['gas','velocity_los'] - los_mean_vel) > vel_range)[0]

                        cloud_section['gas', 'density'][ambient_indices] = 0
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
                        
                        savepath = 'figures/HM_1e%d/spectral_lines_%s/t%d/OVI/%d/z%g/' % (HM_index, run_name, timenum, pixel_id, redshift)
                        os.makedirs(savepath, exist_ok=True)

                        vmin = los_mean_vel - vel_range
                        vmax = los_mean_vel + vel_range
                        minz = (vmin / yt.units.physical_constants.c).value
                        maxz = (vmax / yt.units.physical_constants.c).value

                        spectrum_list = []
                        fitted_flux_list = []
                        fitted_line_list = []

                        for j in range(len(ionlist)):
                            ion = ionlist[j]
                            line = lines[j]
                            linename = line.name
                            rest_lambda = line.wavelength

                            #spec_los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section[line.field])
                            #spec_los_mean_vel2 = np.average(cloud_section['gas','velocity_los'] ** 2, weights=cloud_section[line.field])
                            #spec_los_sigma_2 = (spec_los_mean_vel2 - spec_los_mean_vel ** 2).to('cm**2/s**2').value
        #
                            #spec_los_mean_temp = np.average(cloud_section['gas', 'temperature'], weights=cloud_section[line.field]).value

                            lambda_min = rest_lambda * (1 + minz)
                            lambda_max = rest_lambda * (1 + maxz)
                            dlambda = rest_lambda * (dvel / yt.units.physical_constants.c).value
                                                
                            sg = trident.SpectrumGenerator(lambda_min=lambda_min, lambda_max=lambda_max, dlambda=dlambda)
                            sg.make_spectrum(cloud_section, lines=[linename], min_tau=1e-8, ly_continuum=False)
                            fluxes = np.exp(-sg.tau_field * colden_scaling_factor)
                            lambda_field = sg.lambda_field
                            spectrum_list.append(fluxes)

                            max_tau = max(sg.tau_field)
                            tau_scaling_factor = 1
                            if max_tau > 1e-4:
                                tau_scaling_factor = 4 / max_tau
                            rescaled_tau = sg.tau_field * tau_scaling_factor #Scale the optical depths to avoid saturation
                            rescaled_fluxes = np.exp(-rescaled_tau)

                            #vlist.append(sg.lambda_field)
                            #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            #sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))

                            #Fit the spectrum
                            fitted_flux_local = []
                            fitted_lines_local = []
                            err = []
                            for l in range(len(init_N_list)):
                                init_N = init_N_list[l]
                                init_b = init_b_list[l]
                                tolerance = 1e-4
                                if linename == 'H I 1216':
                                    init_b = init_b_list_HI[l]
                                    tolerance = 1e-7
                                if tau_scaling_factor != 1:
                                    max_N = 1.1 * 10 ** los_log_coldens[j] * tau_scaling_factor
                                else:
                                    max_N = 1e14
                                max_b = 250
                                try:
                                    speciesDicts = gen_line_dict(line, minz, maxz, init_N, init_b, max_N, max_b)
                                    fitted_lines, fitted_flux = generate_total_fit(lambda_field, rescaled_fluxes, orderFits=[linename], speciesDicts=speciesDicts, minError=tolerance, complexLim=0.9995, fitLim=0.994, maxNumComps=12)
                                    fitted_flux_local.append(fitted_flux)
                                    fitted_lines_local.append(fitted_lines)
                                    err.append(np.sum((fitted_flux - rescaled_fluxes) ** 2))
                                except:
                                    pass
                            
                            if len(fitted_flux_local) > 0:
                                best_set = np.argmin(err)

                                fitted_flux_list.append(fitted_flux_local[best_set] ** (colden_scaling_factor / tau_scaling_factor))
                                fitted_lines = fitted_lines_local[best_set]
                                fitted_lines[linename]['N'] /= tau_scaling_factor

                                if len(fitted_lines[linename]['N']) == 0:
                                    fitted_line_list.append([])
                                else:
                                    fitted_line_list.append(fitted_lines)
                            else:
                                fitted_flux_list.append([])
                                fitted_line_list.append([])
                            '''
                            speciesDicts = gen_line_dict(line, minz, maxz)
                            fitted_lines, fitted_flux = generate_total_fit(lambda_field, fluxes, orderFits=[linename], speciesDicts=speciesDicts, complexLim=0.9995, fitLim=0.994, output_file=\
                                                                        savepath + '%s_%d_%d_%s_fit.h5' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            fitted_list.append(fitted_flux)
                            '''
                            sg.clear_spectrum()
                        
                        plt.figure()
                        gap = 1.1
                        for i in range(len(ionlist)):
                            offset = (len(ionlist) - i - 1) * gap
                            label = '%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i] + np.log10(colden_scaling_factor))
                            line = lines[i]
                            linename = line.name
                            fitted_lines_saved = fitted_line_list[i]
                            individual_spectra_list = []
                            if fitted_lines_saved != []:
                                lines_sorted = np.argsort(-fitted_lines_saved[linename]['N'])
                                Nlist = fitted_lines_saved[linename]['N'][lines_sorted] * colden_scaling_factor
                                blist = fitted_lines_saved[linename]['b'][lines_sorted]
                                zlist = fitted_lines_saved[linename]['z'][lines_sorted]
                                centroid_list = zlist * yt.units.physical_constants.c.to('km/s').value - los_mean_vel.to('km/s').value
                                label += ', %.2f (' % np.log10(np.sum(Nlist))

                                for line_ind in range(len(Nlist)):
                                    individual_spectra_list.append(np.exp(-make_individual_line(line, Nlist[line_ind], zlist[line_ind], blist[line_ind], (vlist_fine + los_mean_vel).value)))
                                    label += r'$^{%.2f}_{%.1f}$' % (np.log10(Nlist[line_ind]), centroid_list[line_ind])
                                    if line_ind != len(Nlist) - 1:
                                        label += ', '
                                    else:
                                        label += ')'

                            myplot, = plt.step(vlist, spectrum_list[i] + offset, where='mid', lw=1.5, label=label)
                            if fitted_lines_saved != []:
                                plt.step(vlist, fitted_flux_list[i] + offset, where='mid', lw=1, ls='--', c=myplot.get_color())
                                for individual_spectrum in individual_spectra_list:
                                    plt.step(vlist_fine, individual_spectrum + offset, where='mid', lw=1, ls=':', c=myplot.get_color())
                        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=15)
                        plt.yticks([])
                        plt.xlabel('v/km/s', fontsize=12)
                        plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, round(10 * direction), pixel_id, redshift), bbox_inches='tight')
                        plt.close()
                    
                        
                    for pixel_id in pixel_id_MgII_list:
                        #print(redshift, run_name, pixel_id)
                        projected_yindex = pixel_id % Npix
                        projected_zindex = int(pixel_id / Npix)
                        projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                        angle = np.arccos(direction)
                        norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.

                        los_center = c + deproject(projected_coord, angle) * yt.units.pc
                        los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        
                        ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity'), ('gas', 'density')] + ion_field_list)
                        cloud_section = ray.all_data()

                        los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section['gas','H_p0_number_density'])
                        ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                        #ambient_indices = np.where(abs(cloud_section['gas','velocity_los'] - los_mean_vel) > vel_range)[0]

                        cloud_section['gas', 'density'][ambient_indices] = 0
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
                        
                        savepath = 'figures/HM_1e%d/spectral_lines_%s/t%d/MgII/%d/z%g/' % (HM_index, run_name, timenum, pixel_id, redshift)
                        os.makedirs(savepath, exist_ok=True)

                        vmin = los_mean_vel - vel_range
                        vmax = los_mean_vel + vel_range
                        minz = (vmin / yt.units.physical_constants.c).value
                        maxz = (vmax / yt.units.physical_constants.c).value

                        spectrum_list = []
                        fitted_flux_list = []
                        fitted_line_list = []

                        for j in range(len(ionlist)):
                            ion = ionlist[j]
                            line = lines[j]
                            linename = line.name
                            rest_lambda = line.wavelength

                            #spec_los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section[line.field])
                            #spec_los_mean_vel2 = np.average(cloud_section['gas','velocity_los'] ** 2, weights=cloud_section[line.field])
                            #spec_los_sigma_2 = (spec_los_mean_vel2 - spec_los_mean_vel ** 2).to('cm**2/s**2').value
        #
                            #spec_los_mean_temp = np.average(cloud_section['gas', 'temperature'], weights=cloud_section[line.field]).value

                            lambda_min = rest_lambda * (1 + minz)
                            lambda_max = rest_lambda * (1 + maxz)
                            dlambda = rest_lambda * (dvel / yt.units.physical_constants.c).value
                                                
                            sg = trident.SpectrumGenerator(lambda_min=lambda_min, lambda_max=lambda_max, dlambda=dlambda)
                            sg.make_spectrum(cloud_section, lines=[linename], min_tau=1e-8, ly_continuum=False)
                            fluxes = np.exp(-sg.tau_field * colden_scaling_factor)
                            lambda_field = sg.lambda_field
                            spectrum_list.append(fluxes)

                            max_tau = max(sg.tau_field)
                            tau_scaling_factor = 1
                            if max_tau > 1e-4:
                                tau_scaling_factor = 4 / max_tau
                            rescaled_tau = sg.tau_field * tau_scaling_factor #Scale the optical depths to avoid saturation
                            rescaled_fluxes = np.exp(-rescaled_tau)

                            #vlist.append(sg.lambda_field)
                            #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            #sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))

                            #Fit the spectrum
                            fitted_flux_local = []
                            fitted_lines_local = []
                            err = []
                            for l in range(len(init_N_list)):
                                init_N = init_N_list[l]
                                init_b = init_b_list[l]
                                tolerance = 1e-4
                                if linename == 'H I 1216':
                                    init_b = init_b_list_HI[l]
                                    tolerance = 1e-7
                                if tau_scaling_factor != 1:
                                    max_N = 1.1 * 10 ** los_log_coldens[j] * tau_scaling_factor
                                else:
                                    max_N = 1e14
                                max_b = 250
                                try:
                                    speciesDicts = gen_line_dict(line, minz, maxz, init_N, init_b, max_N, max_b)
                                    fitted_lines, fitted_flux = generate_total_fit(lambda_field, rescaled_fluxes, orderFits=[linename], speciesDicts=speciesDicts, minError=tolerance, complexLim=0.9995, fitLim=0.994, maxNumComps=12)
                                    fitted_flux_local.append(fitted_flux)
                                    fitted_lines_local.append(fitted_lines)
                                    err.append(np.sum((fitted_flux - rescaled_fluxes) ** 2))
                                except:
                                    pass
                            
                            if len(fitted_flux_local) > 0:
                                best_set = np.argmin(err)

                                fitted_flux_list.append(fitted_flux_local[best_set] ** (colden_scaling_factor / tau_scaling_factor))
                                fitted_lines = fitted_lines_local[best_set]
                                fitted_lines[linename]['N'] /= tau_scaling_factor

                                if len(fitted_lines[linename]['N']) == 0:
                                    fitted_line_list.append([])
                                else:
                                    fitted_line_list.append(fitted_lines)
                            else:
                                fitted_flux_list.append([])
                                fitted_line_list.append([])
                            '''
                            speciesDicts = gen_line_dict(line, minz, maxz)
                            fitted_lines, fitted_flux = generate_total_fit(lambda_field, fluxes, orderFits=[linename], speciesDicts=speciesDicts, complexLim=0.9995, fitLim=0.994, output_file=\
                                                                        savepath + '%s_%d_%d_%s_fit.h5' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            fitted_list.append(fitted_flux)
                            '''
                            sg.clear_spectrum()
                        
                        plt.figure()
                        gap = 1.1
                        for i in range(len(ionlist)):
                            offset = (len(ionlist) - i - 1) * gap
                            label = '%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i] + np.log10(colden_scaling_factor))
                            line = lines[i]
                            linename = line.name
                            fitted_lines_saved = fitted_line_list[i]
                            individual_spectra_list = []
                            if fitted_lines_saved != []:
                                lines_sorted = np.argsort(-fitted_lines_saved[linename]['N'])
                                Nlist = fitted_lines_saved[linename]['N'][lines_sorted] * colden_scaling_factor
                                blist = fitted_lines_saved[linename]['b'][lines_sorted]
                                zlist = fitted_lines_saved[linename]['z'][lines_sorted]
                                centroid_list = zlist * yt.units.physical_constants.c.to('km/s').value - los_mean_vel.to('km/s').value
                                label += ', %.2f (' % np.log10(np.sum(Nlist))

                                for line_ind in range(len(Nlist)):
                                    individual_spectra_list.append(np.exp(-make_individual_line(line, Nlist[line_ind], zlist[line_ind], blist[line_ind], (vlist_fine + los_mean_vel).value)))
                                    label += r'$^{%.2f}_{%.1f}$' % (np.log10(Nlist[line_ind]), centroid_list[line_ind])
                                    if line_ind != len(Nlist) - 1:
                                        label += ', '
                                    else:
                                        label += ')'

                            myplot, = plt.step(vlist, spectrum_list[i] + offset, where='mid', lw=1.5, label=label)
                            if fitted_lines_saved != []:
                                plt.step(vlist, fitted_flux_list[i] + offset, where='mid', lw=1, ls='--', c=myplot.get_color())
                                for individual_spectrum in individual_spectra_list:
                                    plt.step(vlist_fine, individual_spectrum + offset, where='mid', lw=1, ls=':', c=myplot.get_color())
                        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=15)
                        plt.yticks([])
                        plt.xlabel('v/km/s', fontsize=12)
                        plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, round(10 * direction), pixel_id, redshift), bbox_inches='tight')
                        plt.close()
                    
                    
                    for pixel_id in pixel_id_CIV_list:
                        #print(redshift, run_name, pixel_id)
                        projected_yindex = pixel_id % Npix
                        projected_zindex = int(pixel_id / Npix)
                        projected_coord = np.array([projected_ylist[projected_yindex], projected_zlist[projected_zindex]])

                        angle = np.arccos(direction)
                        norm_vector = np.array([np.sin(angle), np.cos(angle), 0]) #Computing cos wastes a little time, but it looks nicer this way.

                        los_center = c + deproject(projected_coord, angle) * yt.units.pc
                        los_start = los_center - 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        los_end = los_center + 1.5 * Npix * pixel_size * norm_vector * yt.units.pc
                        
                        ray = trident.make_simple_ray(data, start_position=los_start, end_position=los_end, data_filename='tmp_ray.h5', fields=[('flash', 'blob'), ('gas', 'metallicity'), ('gas', 'density')] + ion_field_list)
                        cloud_section = ray.all_data()

                        los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section['gas','H_p0_number_density'])
                        ambient_indices = np.where(cloud_section['blob'] < blob_cut)[0]
                        #ambient_indices = np.where(abs(cloud_section['gas','velocity_los'] - los_mean_vel) > vel_range)[0]

                        cloud_section['gas', 'density'][ambient_indices] = 0
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
                        
                        savepath = 'figures/HM_1e%d/spectral_lines_%s/t%d/CIV/%d/z%g/' % (HM_index, run_name, timenum, pixel_id, redshift)
                        os.makedirs(savepath, exist_ok=True)

                        vmin = los_mean_vel - vel_range
                        vmax = los_mean_vel + vel_range
                        minz = (vmin / yt.units.physical_constants.c).value
                        maxz = (vmax / yt.units.physical_constants.c).value

                        spectrum_list = []
                        fitted_flux_list = []
                        fitted_line_list = []

                        for j in range(len(ionlist)):
                            ion = ionlist[j]
                            line = lines[j]
                            linename = line.name
                            rest_lambda = line.wavelength

                            #spec_los_mean_vel = np.average(cloud_section['gas','velocity_los'], weights=cloud_section[line.field])
                            #spec_los_mean_vel2 = np.average(cloud_section['gas','velocity_los'] ** 2, weights=cloud_section[line.field])
                            #spec_los_sigma_2 = (spec_los_mean_vel2 - spec_los_mean_vel ** 2).to('cm**2/s**2').value
        #
                            #spec_los_mean_temp = np.average(cloud_section['gas', 'temperature'], weights=cloud_section[line.field]).value

                            lambda_min = rest_lambda * (1 + minz)
                            lambda_max = rest_lambda * (1 + maxz)
                            dlambda = rest_lambda * (dvel / yt.units.physical_constants.c).value
                                                
                            sg = trident.SpectrumGenerator(lambda_min=lambda_min, lambda_max=lambda_max, dlambda=dlambda)
                            sg.make_spectrum(cloud_section, lines=[linename], min_tau=1e-8, ly_continuum=False)
                            fluxes = np.exp(-sg.tau_field * colden_scaling_factor)
                            lambda_field = sg.lambda_field
                            spectrum_list.append(fluxes)

                            max_tau = max(sg.tau_field)
                            tau_scaling_factor = 1
                            if max_tau > 1e-4:
                                tau_scaling_factor = 4 / max_tau
                            rescaled_tau = sg.tau_field * tau_scaling_factor #Scale the optical depths to avoid saturation
                            rescaled_fluxes = np.exp(-rescaled_tau)

                            #vlist.append(sg.lambda_field)
                            #sg.plot_spectrum(savepath + '%s_%d_%d_%s.png' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            #sg.save_spectrum(savepath + '%s_%d_%d_%s.txt' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))

                            #Fit the spectrum
                            fitted_flux_local = []
                            fitted_lines_local = []
                            err = []
                            for l in range(len(init_N_list)):
                                init_N = init_N_list[l]
                                init_b = init_b_list[l]
                                tolerance = 1e-4
                                if linename == 'H I 1216':
                                    init_b = init_b_list_HI[l]
                                    tolerance = 1e-7
                                if tau_scaling_factor != 1:
                                    max_N = 1.1 * 10 ** los_log_coldens[j] * tau_scaling_factor
                                else:
                                    max_N = 1e14
                                max_b = 250
                                try:
                                    speciesDicts = gen_line_dict(line, minz, maxz, init_N, init_b, max_N, max_b)
                                    fitted_lines, fitted_flux = generate_total_fit(lambda_field, rescaled_fluxes, orderFits=[linename], speciesDicts=speciesDicts, minError=tolerance, complexLim=0.9995, fitLim=0.994, maxNumComps=12)
                                    fitted_flux_local.append(fitted_flux)
                                    fitted_lines_local.append(fitted_lines)
                                    err.append(np.sum((fitted_flux - rescaled_fluxes) ** 2))
                                except:
                                    pass
                            
                            if len(fitted_flux_local) > 0:
                                best_set = np.argmin(err)

                                fitted_flux_list.append(fitted_flux_local[best_set] ** (colden_scaling_factor / tau_scaling_factor))
                                fitted_lines = fitted_lines_local[best_set]
                                fitted_lines[linename]['N'] /= tau_scaling_factor

                                if len(fitted_lines[linename]['N']) == 0:
                                    fitted_line_list.append([])
                                else:
                                    fitted_line_list.append(fitted_lines)
                            else:
                                fitted_flux_list.append([])
                                fitted_line_list.append([])
                            '''
                            speciesDicts = gen_line_dict(line, minz, maxz)
                            fitted_lines, fitted_flux = generate_total_fit(lambda_field, fluxes, orderFits=[linename], speciesDicts=speciesDicts, complexLim=0.9995, fitLim=0.994, output_file=\
                                                                        savepath + '%s_%d_%d_%s_fit.h5' % (run_name, round(10 * direction), pixel_id, ion['ion'].replace(' ', '_')))
                            fitted_list.append(fitted_flux)
                            '''
                            sg.clear_spectrum()
                        
                        plt.figure()
                        gap = 1.1
                        for i in range(len(ionlist)):
                            offset = (len(ionlist) - i - 1) * gap
                            label = '%s, %.2f' % (ionlist[i]['ion'], los_log_coldens[i] + np.log10(colden_scaling_factor))
                            line = lines[i]
                            linename = line.name
                            fitted_lines_saved = fitted_line_list[i]
                            individual_spectra_list = []
                            if fitted_lines_saved != []:
                                lines_sorted = np.argsort(-fitted_lines_saved[linename]['N'])
                                Nlist = fitted_lines_saved[linename]['N'][lines_sorted] * colden_scaling_factor
                                blist = fitted_lines_saved[linename]['b'][lines_sorted]
                                zlist = fitted_lines_saved[linename]['z'][lines_sorted]
                                centroid_list = zlist * yt.units.physical_constants.c.to('km/s').value - los_mean_vel.to('km/s').value
                                label += ', %.2f (' % np.log10(np.sum(Nlist))

                                for line_ind in range(len(Nlist)):
                                    individual_spectra_list.append(np.exp(-make_individual_line(line, Nlist[line_ind], zlist[line_ind], blist[line_ind], (vlist_fine + los_mean_vel).value)))
                                    label += r'$^{%.2f}_{%.1f}$' % (np.log10(Nlist[line_ind]), centroid_list[line_ind])
                                    if line_ind != len(Nlist) - 1:
                                        label += ', '
                                    else:
                                        label += ')'

                            myplot, = plt.step(vlist, spectrum_list[i] + offset, where='mid', lw=1.5, label=label)
                            if fitted_lines_saved != []:
                                plt.step(vlist, fitted_flux_list[i] + offset, where='mid', lw=1, ls='--', c=myplot.get_color())
                                for individual_spectrum in individual_spectra_list:
                                    plt.step(vlist_fine, individual_spectrum + offset, where='mid', lw=1, ls=':', c=myplot.get_color())
                        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left', fontsize=15)
                        plt.yticks([])
                        plt.xlabel('v/km/s', fontsize=12)
                        plt.savefig(savepath + '%s_%d_%d_z%g_spectra.pdf' % (run_name, round(10 * direction), pixel_id, redshift), bbox_inches='tight')
                        plt.close()
            