from multiprocessing import Pool
import numpy as np
import h5py
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import yt
import os

Npix = 400
pixel_size = 10 #in pc

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

runz1 = { 'Name':'T0.02_v100_chi20_Z',
         'Formal_name':'T0.02_v100_chi20_Z',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':1.5,
        'tcc':23.7,
        'velocity':100,
        'f_list':['0030', '0039', '0051', '0059'],
        'f_list_full':['%04d' % i for i in range(75)]}

tcc = 1

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

#runlist.append(runy1)   #T0.1_v150_chi100_ld2
runlist.append(runy2)   #T0.1_v150_chi100_cond_0.1_ld2

#blob_cut_list = [0.9, 0.85, 0.82, 0.8, 0.75, 0.5]
blob_cut_list = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
rho_cut_list = [1, 0.33, 0.1]
temp_cut_list = [1e5, 3e5, 5e5]
#blob_cut_list = [0.5]
cooling_table_file = '/work/pi_nsk_umass_edu/lyang/CoolingTables/z_0.000.hdf5'

with h5py.File(cooling_table_file) as f:
    cooling_table = np.array(f['Solar/Net_cooling'][:])
    temp_bins = np.array(f['Solar/Temperature_bins'][:])
    nh_bins = np.array(f['Solar/Hydrogen_density_bins'][:])

def find_temperature_index(temperature):
    return abs(temperature - temp_bins).argmin()
find_temperature_indices = np.vectorize(find_temperature_index)

def find_nh_index(nh):
    return abs(nh - nh_bins).argmin()
find_nh_indices = np.vectorize(find_nh_index)

def _cooling_time(field, data):
    density = data['gas', 'density'].to('g/cm**3').value
    nh = density / 2.338e-24
    temperature = data['gas', 'temperature'].to('K').value
    temp_index = find_temperature_indices(temperature)
    nh_index = find_nh_indices(nh)
    cooling_rate = cooling_table[temp_index, nh_index]
    cooling_time = (1.51e-29 * temperature / (cooling_rate * nh)) / tcc
    return cooling_time

def compare_slices():
    timenum_list = [2]
    for run in runlist:
        savepath = 'figures/%s/' % run['Name']
        os.makedirs(savepath, exist_ok=True)

        tcc = run['tcc']
        snapnum_list = np.array(run['f_list'], dtype=int)

        if 'ld' in run['Name']:
            init_cloud_mass = 1.951e38 * yt.units.g
        else:
            init_cloud_mass = 1.23067e38 * yt.units.g

        for i in range(len(timenum_list)):
            snapnum = snapnum_list[timenum_list[i]]
            data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  '%04d' % snapnum)
            data.add_field(('gas', 'cooling_time'), function = _cooling_time, sampling_type='cell', force_override=True, take_log=True)
            allDataRegion = data.all_data()
            cm = allDataRegion.quantities.center_of_mass()
            slc_list_blob = []
            mass_list_blob = []
            for blob_cut in blob_cut_list:
                cloud_region = allDataRegion.cut_region(['obj["blob"] > %g' % blob_cut])
                mass_list_blob.append((cloud_region.quantities.total_mass()[0] / init_cloud_mass).value)

                if 'ld' in run['Name']:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((7.0, 'kpc'), (5.8, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
                else:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))
                slc_list_blob.append(slc)
            
            slc_list_rho = []
            mass_list_rho = []
            for rho_cut in rho_cut_list:
                if 'ld' in run['Name']:
                    cloud_region = allDataRegion.cut_region(['obj["density"] > %g' % (1e-26 * rho_cut)])
                else:
                    cloud_region = allDataRegion.cut_region(['obj["density"] > %g' % (1e-24 * rho_cut)])

                mass_list_rho.append((cloud_region.quantities.total_mass()[0] / init_cloud_mass).value)
                
                if 'ld' in run['Name']:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((7.0, 'kpc'), (5.8, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
                else:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))
                slc_list_rho.append(slc)
            
            slc_list_temp = []
            mass_list_temp = []
            for temp_cut in temp_cut_list:
                cloud_region = allDataRegion.cut_region(['obj["temperature"] < %g' % temp_cut])
                mass_list_temp.append((cloud_region.quantities.total_mass()[0] / init_cloud_mass).value)
                
                if 'ld' in run['Name']:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((7.0, 'kpc'), (5.8, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
                else:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))
                slc_list_temp.append(slc)
        
            fig = plt.figure()
            grid = AxesGrid(fig, (0.075, 0.075, 0.85, 0.85), nrows_ncols=(4, 3), axes_pad=0.05, label_mode="L", share_all=True,\
                 cbar_location="right", cbar_mode="single", cbar_size="3%", cbar_pad="0%")
            for j in range(6):
                plot = slc_list_blob[j].plots[("gas", "density")]
                plot.figure = fig
                plot.axes = grid[j].axes
                plot.cax = grid.cbar_axes[j]
                slc_list_blob[j].render()
                grid[j].text(0.5, 0.1, r'$C_{\mathrm{cloud}} > %g$' % blob_cut_list[j], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=grid[j].transAxes)
                grid[j].text(0.5, 0.8, r'$M/M_0 = %.2f$' % mass_list_blob[j], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=grid[j].transAxes)

            for j in range(3):
                plot = slc_list_rho[j].plots[("gas", "density")]
                plot.figure = fig
                plot.axes = grid[j + 6].axes
                plot.cax = grid.cbar_axes[j + 6]
                slc_list_rho[j].render()
                grid[j + 6].text(0.5, 0.1, r'$\rho/\rho_0 > %g$' % rho_cut_list[j], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=grid[j + 6].transAxes)
                grid[j + 6].text(0.5, 0.8, r'$M/M_0 = %.2f$' % mass_list_rho[j], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=grid[j + 6].transAxes)
            
            for j in range(3):
                plot = slc_list_temp[j].plots[("gas", "density")]
                plot.figure = fig
                plot.axes = grid[j + 9].axes
                plot.cax = grid.cbar_axes[j + 9]
                slc_list_temp[j].render()
                grid[j + 9].text(0.5, 0.1, r'$T<%.2e$' % temp_cut_list[j], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=grid[j + 9].transAxes)
                grid[j + 9].text(0.5, 0.8, r'$M/M_0 = %.2f$' % mass_list_temp[j], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=grid[j + 9].transAxes)

            plt.savefig(savepath + 'compare_cuts_%s_t%d.png' % (run['Name'], timenum_list[i]), dpi=400)
            plt.close()
            del(slc)

def compare_ions(run):
    blob_colden_file_high = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
    blob_colden_file_low = '/nas/astro-th/lyang/nonSorted_ColDen_23/blob0.5/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
    ion_list = ['H I', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV', 'N V']
    ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])
    indices = [0, 10, 3, 4, 6, 9] #HI, Mg II, C III, C IV, O VI, Ne VIII

    run_name = run['Name']
    direction = 0
    redshift = 0.5396
    time = 3
    #time_list = [0, 1, 2, 3]
    #time_list = [1, 2]
    #HM_list = np.arange(3, 5)
    HM_value = 0
    #linestyles = [':', '--', '-']
    #linestyles = [':', '-.', '--', '-']
    labels_run = [run['Name'] for run in runlist]
    #labels_direction = [r'$\cos \theta = %.1f$' % direction for direction in direction_list]
    #labels_times = ['t75', 't50', 't25']
    #labels_times = ['t90', 't50', 't25']
    #labels_times = ['t75', 't50', 't25']\
    xlist = np.arange(0, (Npix + 1) * pixel_size, pixel_size)
    ylist = np.arange(0, (Npix + 1) * pixel_size, pixel_size)

    savepath = 'figures/%s/' % (run_name)
    os.makedirs(savepath, exist_ok=True)
    log_coldens_high = np.full((Npix ** 2, len(ion_list)), -10.)
    log_coldens_low = np.full((Npix ** 2, len(ion_list)), -10.)
    #thermal_fraction = []

    coldens_high = np.loadtxt(blob_colden_file_high % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
    cloud_indices_high = coldens_high[:, 0].astype(int)
    log_coldens_high[cloud_indices_high] = np.log10(coldens_high[:, 1:])

    coldens_low = np.loadtxt(blob_colden_file_low % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
    cloud_indices_low = coldens_low[:, 0].astype(int)
    log_coldens_low[cloud_indices_low] = np.log10(coldens_low[:, 1:])

    for l in range(len(indices)):
        null_pixels_high = np.where(log_coldens_high[:, indices[l]] < 11)[0]
        log_coldens_high[null_pixels_high, indices[l]] = np.nan

        null_pixels_low = np.where(log_coldens_low[:, indices[l]] < 11)[0]
        log_coldens_low[null_pixels_low, indices[l]] = np.nan
    

    fig = plt.figure(figsize=(15.3, 9.5), dpi=450)
    nrows = int(np.ceil(len(indices) / 2))
    ncols = 7
    spec = fig.add_gridspec(nrows=nrows, ncols=ncols, width_ratios=([4, 4, 1] + [0.7] + [4, 4, 1]))
    for l in range(nrows):
        for k in range(2):
            ax = fig.add_subplot(spec[l, k * 4])
            ion_index = l * 2 + k
            if l == 0 and k == 0:
                im = ax.pcolormesh(ylist, xlist, np.flip(log_coldens_low[:, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=21, rasterized=True)
            else:
                im = ax.pcolormesh(ylist, xlist, np.flip(log_coldens_low[:, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=17, rasterized=True)

            #if i == 0:
            ax.set_title(ion_list[indices[ion_index]], fontsize=15, y=0.05)
            ax.text(0.5, 0.9, r'$C_{\mathrm{cloud}}>0.5$', c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.tick_params(which='both', direction='in', labelsize=14, right=True, top=True)
            ax.set_yticks([1000, 2000, 3000])
            ax.set_yticklabels(['-1', '0', '1'])
            ax.axis('scaled')
            ax.set_xlim(0, 4000)
            ax.set_xticks([1000, 2000, 3000])
            ax.set_xticklabels(['-1', '0', '1'])
            ax.set_ylim(0, 4000)
            if l == nrows - 1:
                ax.set_xlabel('x/kpc', fontsize=15)
            else:
                ax.set_xticklabels([])
            if k == 0:
                ax.set_ylabel('y/kpc', fontsize=15)
            else:
                ax.set_yticklabels([])
            
            ax = fig.add_subplot(spec[l, k * 4 + 1])
            ion_index = l * 2 + k
            if l == 0 and k == 0:
                im = ax.pcolormesh(ylist, xlist, np.flip(log_coldens_high[:, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=21, rasterized=True)
            else:
                im = ax.pcolormesh(ylist, xlist, np.flip(log_coldens_high[:, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=17, rasterized=True)

            #if i == 0:
            ax.set_title(ion_list[indices[ion_index]], fontsize=15, y=0.05)
            ax.text(0.5, 0.9, r'$C_{\mathrm{cloud}}>0.82$', c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
            ax.tick_params(axis='y', labelleft=False, labelright=True)
            ax.tick_params(which='both', direction='in', labelsize=14, right=True, top=True)
            ax.set_yticks([1000, 2000, 3000])
            ax.set_yticklabels(['-1', '0', '1'])
            ax.axis('scaled')
            ax.set_xlim(0, 4000)
            ax.set_xticks([1000, 2000, 3000])
            ax.set_xticklabels(['-1', '0', '1'])
            ax.set_ylim(0, 4000)

            if l == nrows - 1:
                ax.set_xlabel('x/kpc', fontsize=15)
            else:
                ax.set_xticklabels([])

            ax.set_yticklabels([])
    
            cax = fig.add_subplot(spec[l, k * 4 + 2], box_aspect=15)
            plt.colorbar(im, cax=cax, location='left')
            cax.set_ylabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
            if l == 0 and k == 0:
                cax.set_yticks([14, 16, 18, 20])
            else:
                cax.set_yticks([13, 14, 15, 16])
            cax.yaxis.set_label_position("left")
            cax.tick_params(labelleft=False, labelright=True)
            cax.tick_params(which='both', direction='in', labelsize=15)
    
    spec.update(hspace=0.05, wspace=0.15)
    #plt.tight_layout()
    plt.savefig(savepath + 'compare_cuts_ions_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
    #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
    #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    #compare_ions(runx4)
    compare_slices()
