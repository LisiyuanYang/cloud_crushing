from multiprocessing import Pool
import numpy as np
import h5py
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import yt
import os

run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Formal_name':'T0.3_v1000_chi300_cond_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132'],
        'f_list_full':['0013', '0038', '0080', '0132']}

run2 = { 'Name':'T3_v3000_chi3000_cond',
        'Formal_name':'T3_v3000_chi3000_cond_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.6,
        'tcc':1.8,
        'velocity':3000,
        'f_list':['0001', '0004', '0007', '0010'],
        'f_list_full':['0001', '0004', '0007', '0010']}

run3 = { 'Name':'T1_v1700_chi1000_cond',
        'Formal_name':'T1_v1700_chi1000_cond_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.5,
        'tcc':1.8,
        'velocity':1700,
        'f_list':['0002', '0010', '0017', '0028'],
        'f_list_full':['0002', '0010', '0017', '0028']}

run4 = { 'Name':'T0.3_v1000_chi300',
        'Formal_name':'T0.3_v1000_chi300_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0025', '0033', '0042', '0058'],
        'f_list_full':['0025', '0033', '0042', '0058']}

run5 = { 'Name':'T3_v3000_chi3000',
        'Formal_name':'T3_v3000_chi3000_old',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.6,
    'tcc':1.8,
    'velocity':3000,
    'f_list':['0021', '0030', '0040', '0062'],
    'f_list_full':sorted(set(['%04d' % i for i in range(61)[: : 5]] + ['0021', '0030', '0040', '0062']))}

run6 = { 'Name':'T1_v1700_chi1000',
        'Formal_name':'T1_v1700_chi1000_old',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.5,
    'tcc':1.8,
    'velocity':1700,
    'f_list':['0021', '0029', '0038', '0052'],
    'f_list_full':['0021', '0029', '0038', '0052']}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
         'Formal_name':'T0.3_v1700_chi300_cond_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078'],
        'f_list_full':['0003', '0020', '0046', '0078']}
    
run12 = { 'Name':'T0.3_v3000_chi300_cond',
         'Formal_name':'T0.3_v3000_chi300_cond_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0001', '0004', '0014', '0035'],
        'f_list_full':['0001', '0004', '0014', '0035']}

run16 = { 'Name':'T0.3_v1700_chi300',
         'Formal_name':'T0.3_v1700_chi300_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085'],
        'f_list_full':sorted(set(['%04d' % i for i in range(106)[: : 5]] + ['0022', '0032', '0053', '0085']))}

run17 = { 'Name':'T0.3_v3000_chi300',
         'Formal_name':'T0.3_v3000_chi300_old',
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

runy1 = { 'Name':'T0.1_v150_chi100_ld2',
         'Formal_name':'T0.1_v150_chi100',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':1.0,
        'tcc':35.3,
        'velocity':150,
        'f_list':['0010', '0013', '0018', '0024'],
        'f_list_full':['%04d' % i for i in range(89)]}

runy2 = { 'Name':'T0.1_v150_chi100_cond_0.1_ld2',
         'Formal_name':'T0.1_v150_chi100',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':1.0,
        'tcc':35.3,
        'velocity':150,
        'f_list':['0016', '0022', '0041', '0055'],
        'f_list_full':['%04d' % i for i in range(96)]}

tcc = 1

runlist = []
##add only the 3 different conduction levels

#runlist.append(run4)    #T0.3_v1000_chi300
#runlist.append(runx2)   #T0.3_v1000_chi300_ld2
#runlist.append(run1)   #T0.3_v1000_chi300_cond
#runlist.append(runx14)   #T0.3_v1000_chi300_cond_0.1_ld2
#runlist.append(runx8)   #T0.3_v1000_chi300_cond_ld2

#runlist.append(run16)  #T0.3_v1700_chi300
runlist.append(runx4)   #T0.3_v1700_chi300_ld2
#runlist.append(run11)  #T0.3_v1700_chi300_cond
runlist.append(runx16)   #T0.3_v1700_chi300_cond_0.1_ld2
runlist.append(runx10)  #T0.3_v1700_chi300_cond_lds

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
#runlist.append(runy2)   #T0.1_v150_chi100_cond_0.1_ld2

blob_cut_list = [0.9, 0.85, 0.82, 0.8, 0.75, 0.5]
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

def main(i):
    #snapnum_x1 = 12
    #snapnum_4 = 33
    '''
    run = run17
    savepath = 'figures/%s/slice_z/' % run['Name']
    os.makedirs(savepath, exist_ok=True)
    
    for snapnum in range(0, 136, 5):
        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  '%04d' % snapnum)
        allDataRegion = data.all_data()
        cm = allDataRegion.quantities.center_of_mass()
        if 'ld' in run['Name']:
            slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((8.2, 'kpc'), (5.8, 'kpc')))
            slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
        else:
            slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')))
            slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))

        slc.annotate_title('%04d' % snapnum)
        slc.save(savepath + '%s_%04d' % (run['Name'], snapnum))
    '''
    
    #run = runx6
    blob_cut = blob_cut_list[i]
    for run in runlist:
        #savepath_density = 'figures/%s/cloud_slice_z/' % run['Name']
        #savepath_temperature = 'figures/%s/cloud_temperature_z/' % run['Name']
        #savepath_cooling_time = 'figures/%s/cloud_cooling_time_z/' % run['Name']

        savepath_density = 'figures/%s/cloud_slice_z_blob%g/' % (run['Name'], blob_cut)
        savepath_temperature = 'figures/%s/cloud_temperature_z_blob%g/' % (run['Name'], blob_cut)
        savepath_cooling_time = 'figures/%s/cloud_cooling_time_z_blob%g/' % (run['Name'], blob_cut)

        os.makedirs(savepath_density, exist_ok=True)
        os.makedirs(savepath_temperature, exist_ok=True)
        os.makedirs(savepath_cooling_time, exist_ok=True)

        tcc = run['tcc']

        aux_file = run['Dir'] + run['Name'] + '/%s.aux' % run['Name']
        cloud_mass = np.loadtxt(aux_file, usecols=2)
        #cloud_mass = np.loadtxt(aux_file, usecols=3)
        snapnum_list = np.loadtxt(aux_file, usecols=0, dtype=int)

        for i in range(len(snapnum_list)):
            if cloud_mass[i] > 0.04:
                snapnum = snapnum_list[i]
                data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  '%04d' % snapnum)
                data.add_field(('gas', 'cooling_time'), function = _cooling_time, sampling_type='cell', force_override=True, take_log=True)
                allDataRegion = data.all_data()
                cm = allDataRegion.quantities.center_of_mass()
                #cloud_region = allDataRegion.cut_region(['obj["blob"] >= 0.82'])
                cloud_region = allDataRegion.cut_region(['obj["blob"] >= %g' % blob_cut])
                #if 'ld' in run['Name']:
                #    cloud_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-27'])
                #else:
                #    cloud_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])

                if 'ld' in run['Name']:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((8.2, 'kpc'), (5.8, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
                else:
                    slc = yt.SlicePlot(data, 'z', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))
                
                slc.annotate_title(r'$C_{\mathrm{cloud}} > %g$' % blob_cut)
                slc.set_font_size(40)
                slc.save(savepath_density + '%s_density_blob%g_%04d' % (run['Name'], blob_cut, snapnum))

                if 'ld' in run['Name']:
                    slc = yt.SlicePlot(data, 'z', ("gas", "temperature"), center=cm, width=((8.2, 'kpc'), (5.8, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'temperature'), zmin=(5e3, 'K'), zmax=(1e8, 'K'))
                else:
                    slc = yt.SlicePlot(data, 'z', ("gas", "temperature"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'temperature'), zmin=(5e3, 'K'), zmax=(1e8, 'K'))

                slc.annotate_title(r'$C_{\mathrm{cloud}} > %g$' % blob_cut)
                slc.set_font_size(40)
                slc.save(savepath_temperature + '%s_temperature_blob%g_%04d' % (run['Name'], blob_cut, snapnum))

                if 'ld' in run['Name']:
                    slc = yt.SlicePlot(data, 'z', ("gas", "cooling_time"), center=cm, width=((8.2, 'kpc'), (5.8, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'cooling_time'), zmin=0.005, zmax=500)
                else:
                    slc = yt.SlicePlot(data, 'z', ("gas", "cooling_time"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')), data_source=cloud_region)
                    slc.set_zlim(('gas', 'cooling_time'), zmin=0.005, zmax=500)

                slc.annotate_title(r'$C_{\mathrm{cloud}} > %g$' % blob_cut)
                slc.set_font_size(40)
                slc.save(savepath_cooling_time + '%s_cooling_time_blob%g_%04d' % (run['Name'], blob_cut, snapnum))
            else:
                break

if __name__ == '__main__':
    with Pool(len(blob_cut_list)) as p:
        p.map(main, list(range(len(blob_cut_list))))
