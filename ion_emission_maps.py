import numpy as np
import os
import yt
from mpi4py import MPI
import trident
from cloud_util import runs, h, data_path_base, ionTable_base, MHYDR, SOLAR_METAL_FRAC, XH, XHE, binned_particles, ions, add_metallicity, add_metallicity_variable
from line_emission import get_emission_individual

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank   = comm.Get_rank()

electron_abundance = 1 + 2 * XHE
#HM_index_list = np.arange(-4, 5)
HM_index_list = np.array([0])
#timenum_list = np.array([0, 1, 2, 3])
timenum_list = np.array([2])
#redshift_list = np.array([0.1006, 0.5396, 1.053, 2.013, 3.017, 4.895])
#redshift_list = np.array([0.1006, 0.5396, 1.053])
redshift_list = np.array([0.5396])
ion = ions['O VI']
init_cloud_mass = 1.99e38 * yt.units.g #1e5 solar mass
Npixels = np.array([400, 500])
width = np.array([4, 5, 10]) * yt.units.kpc
#pixel_size = width / Npixels


run_list = []
##add only the 3 different conduction levels
#run_list.append(run4)    #T0.3_v1000_chi300
#run_list.append(runs['runx2'])   #T0.3_v1000_chi300_ld2
#run_list.append(runs['run1'])   #T0.3_v1000_chi300_cond
#run_list.append(runs['runx14'])   #T0.3_v1000_chi300_cond_0.1_ld2
#run_list.append(runs['runx8'])   #T0.3_v1000_chi300_cond_ld2

#run_list.append(runs['run16'])  #T0.3_v1700_chi300
#run_list.append(runs['runx4'])   #T0.3_v1700_chi300_ld2
#run_list.append(runs['run11'])  #T0.3_v1700_chi300_cond
#run_list.append(runs['runx16'])   #T0.3_v1700_chi300_cond_0.1_ld2
#run_list.append(runs['runx10'])  #T0.3_v1700_chi300_cond_lds

#run_list.append(runs['run17'])  #T0.3_v3000_chi300
#run_list.append(runs['runx5'])   #T0.3_v3000_chi300_ld2
#run_list.append(runs['run12'])  #T0.3_v3000_chi300_cond
#run_list.append(runs['runx17'])   #T0.3_v3000_chi300_cond_0.1_ld2
#run_list.append(runs['runx11'])  #T0.3_v3000_chi300_cond_ld2

#run_list.append(runs['run6'])   #T1_v1700_chi1000
#run_list.append(runs['runx3'])   #T1_v1700_chi1000_ld2
#run_list.append(runs['run3'])   #T1_v1700_chi1000_cond
#run_list.append(runs['runx13'])   #T1_v1700_chi1000_cond_0.1_ld2
#run_list.append(runs['runx9'])   #T1_v1700_chi1000_cond_ld2

#run_list.append(runs['run5'])   #T3_v3000_chi3000
#run_list.append(runs['runx6'])   #T3_v3000_chi3000_ld2
#run_list.append(runs['run2'])   #T3_v3000_chi3000_cond
#run_list.append(runs['runx15'])   #T3_v3000_chi3000_cond_0.1_ld2
#run_list.append(runs['runx12'])   #T3_v3000_chi3000_cond_ld2

#run_list.append(runs['runy1'])   #T0.1_v150_chi100_ld2
run_list.append(runs['runy2'])   #T0.1_v150_chi100_cond_0.1_ld2

run_list.append(runs['runz1'])   #T0.1_v150_chi100_cond_0.1_ld2


if __name__ == '__main__':
    def _emission_cell(field, data):
        mH = data['gas', 'mass'].to('solar_mass').value
        ni = data['gas', ion['fieldname']].to('cm**-3').value
        temp = data['gas', 'temperature'].to('K').value
        vol = data['gas', 'volume'].to('kpc**2*cm').value
        emission_cell = get_emission_individual(ion, temp, ion['rest_wave'], ni, mH, electron_abundance, Bfactor=1) / vol #in 1/(cm^3*s*arcsec^2)
        return data.ds.arr(emission_cell, '1 / (cm**3*arcsec**2*s)')

    if rank < len(run_list):
        runlist_local = run_list[rank : : nprocs]
        for k in range(len(runlist_local)):
            run = runlist_local[k]
            run_name = run['Name']
            emission_map_table = np.zeros((len(timenum_list), len(redshift_list), len(HM_index_list), *Npixels))
            column_density_map_table = np.zeros((len(timenum_list), len(redshift_list), len(HM_index_list), *Npixels))
            for i in range(len(redshift_list)):
                redshift = redshift_list[i]
                for j in range(len(HM_index_list)):
                    HM_index = HM_index_list[j]
                    trident.ion_balance.table_store = {} #Force trident to reload ionization tables
                    ionTable = ionTable_base % (HM_index, redshift, HM_index)            
                    for l in range(len(timenum_list)):
                        timenum = timenum_list[l]
                        print('%s z=%g HM_index=%g t=%d' % (run_name, redshift, HM_index, timenum), flush=True)
                        data = yt.load(run['Dir'] + run_name + '/KH_hdf5_chk_' + run['f_list'][timenum])
                        if 'Z' in run_name:
                            data.add_field(('gas', 'metallicity'), function=add_metallicity_variable, sampling_type='cell', display_name='Metallicity', units='Zsun')
                        else:
                            data.add_field(('gas', 'metallicity'), function=add_metallicity, sampling_type='cell', display_name='Metallicity', units='Zsun')
                        
                        trident.add_ion_fields(data, ions=[ion['ion']], ionization_table=ionTable)
                        data.add_field(('gas', 'emission_cell'), function=_emission_cell, sampling_type='cell', display_name='Emission', units='1 / (cm**3*arcsec**2*s)')
                        
                        allDataRegion = data.all_data()
                        #mH = allDataRegion['gas', 'mass'].to('solar_mass').value
                        #ni = allDataRegion['gas', ion['fieldname']].to('cm**-3').value
                        #temp = allDataRegion['gas', 'temperature'].to('K').value
                        #emission_cell = get_emission_individual(ion, temp, ion['rest_wave'], ni, mH, electron_abundance, Bfactor=1) #in kpc^2/(cm^2*s*arcsec^2)
                        
                        cloud_region = allDataRegion.cut_region(['obj["blob"] >= 0.5'])
                        c = cloud_region.quantities.center_of_mass() #Can avoid cutting off the tail
                        c = [0.5 * (np.max(cloud_region['x']) + np.min(cloud_region['x'])), 
                            0.5 * (np.max(cloud_region['y']) + np.min(cloud_region['y'])),
                            0.5 * (np.max(cloud_region['z']) + np.min(cloud_region['z']))] #Can avoid cutting off the tail
                        #mcloud = (cloud_region.quantities.total_mass()[0] / init_cloud_mass).value
                        #density = cloud_region['gas', 'density'].to('g/cm**3').value
                        #head_density = np.percentile(density, 99)
                        #mean_density = (cloud_region.quantities.total_quantity(('gas', 'mass')) / cloud_region.quantities.total_quantity(('gas', 'cell_volume'))).to('g/cm**3').value

                        emission_map = yt.off_axis_projection(cloud_region, center=c, normal_vector=np.array([1, 0, 0]), width=width, resolution=Npixels, item=('gas', 'emission_cell'), north_vector=[0, 1, 0])
                        column_density_map = yt.off_axis_projection(cloud_region, center=c, normal_vector=np.array([1, 0, 0]), width=width, resolution=Npixels, item=('gas', ion['fieldname']), north_vector=[0, 1, 0])
                        #emission_map /= pixel_size ** 2
                        emission_map_table[l, i, j] = emission_map.to('cm**-2 * arcsec**-2 * s**-1').value
                        column_density_map_table[l, i, j] = column_density_map.to('cm**-2').value
        
            savepath = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/' % run_name
            os.makedirs(savepath, exist_ok=True)

            np.savez(savepath + '%s_emission_maps_2.npz' % ion['ion'].replace(' ', '_'), redshift_list=redshift_list, HM_index_list=HM_index_list,\
                timenum_list=timenum_list, emission_map_table=emission_map_table, column_density_map_table=column_density_map_table)

