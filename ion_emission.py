import numpy as np
import os
import yt
import trident
from cloud_util import runs, h, data_path_base, ionTable_base, MHYDR, SOLAR_METAL_FRAC, XH, XHE, binned_particles, ions, add_metallicity, add_metallicity_variable
from line_emission import get_emission_intensity

HM_index_list = np.arange(-4, 5)
#HM_index_list = np.array([0])
timenum_list = np.array([0, 1, 2, 3])
#redshift_list = np.array([0.1006, 0.5396, 1.053, 2.013, 3.017, 4.895])
redshift_list = np.array([0.1006, 0.5396, 1.053])
#redshift_list = np.array([0.1006])
ion = ions['O VI']
run_list = []
run_list.append(runs['runy2'])
run_list.append(runs['runz1'])
init_cloud_mass = 1.99e38 * yt.units.g #1e5 solar mass

if __name__ == '__main__':
    emission_table = np.zeros((len(run_list), len(timenum_list), len(redshift_list), len(HM_index_list)))
    mcloud_list = np.zeros((len(run_list), len(timenum_list)))
    head_density_list = np.zeros((len(run_list), len(timenum_list)))
    mean_density_list = np.zeros((len(run_list), len(timenum_list)))
    for i in range(len(redshift_list)):
        redshift = redshift_list[i]
        for j in range(len(HM_index_list)):
            HM_index = HM_index_list[j]
            trident.ion_balance.table_store = {} #Force trident to reload ionization tables
            ionTable = ionTable_base % (HM_index, redshift, HM_index)
            for k in range(len(run_list)):
                run = run_list[k]
                run_name = run['Name']    
                for l in range(len(timenum_list)):
                    timenum = timenum_list[l]
                    print('%s z=%g HM_index=%g t=%d' % (run_name, redshift, HM_index, timenum), flush=True)
                    data = yt.load(run['Dir'] + run_name + '/KH_hdf5_chk_' + run['f_list'][timenum])
                    if 'Z' in run_name:
                        data.add_field(('gas', 'metallicity'), function=add_metallicity_variable, sampling_type='cell', display_name='Metallicity', units='Zsun')
                    else:
                        data.add_field(('gas', 'metallicity'), function=add_metallicity, sampling_type='cell', display_name='Metallicity', units='Zsun')
                    
                    allDataRegion = data.all_data()
                    cloud_region = allDataRegion.cut_region(['obj["blob"] >= 0.5'])
                    mcloud = (cloud_region.quantities.total_mass()[0] / init_cloud_mass).value
                    density = cloud_region['gas', 'density'].to('g/cm**3').value
                    head_density = np.percentile(density, 99)
                    mean_density = (cloud_region.quantities.total_quantity(('gas', 'mass')) / cloud_region.quantities.total_quantity(('gas', 'cell_volume'))).to('g/cm**3').value

                    mH = cloud_region['gas', 'mass'].to('solar_mass').value
                    electron_abundance = 1 + 2 * XHE
                    trident.add_ion_fields(data, ions=[ion['ion']], ionization_table=ionTable)
                    ni = cloud_region['gas', ion['fieldname']].to('cm**-3').value
                    temp = cloud_region['gas', 'temperature'].to('K').value
                    emission = get_emission_intensity(ion, temp, ion['rest_wave'], ni, mH, electron_abundance, 1) #in kpc^2/(cm^2*s*arcsec^2)
                    print(' %g %g %g' % (mcloud, head_density, emission), flush=True)
                    mcloud_list[k, l] = mcloud
                    head_density_list[k, l] = head_density
                    mean_density_list[k, l] = mean_density
                    emission_table[k, l, i, j] = emission
    
    savepath = '/nas/astro-th/lyang/nonSorted_ColDen_23/'
    os.makedirs(savepath, exist_ok=True)

    run_list = np.array(run_list, dtype=object)
    np.savez(savepath + '%s_emission.npz' % ion['ion'].replace(' ', '_'), run_list=run_list, redshift_list=redshift_list, HM_index_list=HM_index_list,\
         timenum_list=timenum_list, mcloud_list=mcloud_list, head_density_list=head_density_list, mean_density_list=mean_density_list, emission_table=emission_table)

