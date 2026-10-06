import numpy as np
import yt
import h5py
import os
from multiprocessing import Pool

run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Formal_name':'T0.3_v1000_chi300_cond_old',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132'],
        'f_list_full':['0013', '0038', '0080', '0132']}

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
        'f_list':['0020', '0032', '0052', '0073'],
        'f_list_full':['%04d' % i for i in range(105)]}

runx3 = { 'Name':'T1_v1700_chi1000_ld2',
         'Formal_name':'T1_v1700_chi1000',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.5,
        'tcc':9.85,
        'velocity':1700,
        'f_list':['0021', '0030', '0052', '0068'],
        'f_list_full':['%04d' % i for i in range(114)]}

runx4 = { 'Name':'T0.3_v1700_chi300_ld2',
         'Formal_name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':5.40,
        'velocity':1700,
        'f_list':['0021', '0025', '0031', '0038', '0046', '0070'],
        #'f_list':['0020', '0025', '0029', '0035'],
        'f_list_full':['%04d' % i for i in range(101)]}

runx5 = { 'Name':'T0.3_v3000_chi300_ld2',
         'Formal_name':'T0.3_v3000_chi300',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':11.4,
        'tcc':3.06,
        'velocity':3000,
        'f_list':['0017', '0023', '0034', '0079'],
        'f_list_full':['%04d' % i for i in range(82)]}

runx6 = { 'Name':'T3_v3000_chi3000_ld2',
         'Formal_name':'T3_v3000_chi3000',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':3.6,
        'tcc':9.67,
        'velocity':3000,
        'f_list':['0021', '0026', '0031', '0044'],
        'f_list_full':['%04d' % i for i in range(52)]}

tcc = 1
runlist = [runx2, runx3, runx4, runx5, runx6, run4, run16, run17, run6, run5]

cooling_table_file = '/work/pi_nsk_umass_edu/lyang/CoolingTables/z_0.000.hdf5'

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

def main(run):
    savepath_rho_tcc = 'figures/%s/rho_tcc/' % run['Name']
    savepath_rho_T = 'figures/%s/rho_T/' % run['Name']
    os.makedirs(savepath_rho_tcc, exist_ok=True)
    os.makedirs(savepath_rho_T, exist_ok=True)

    tcc = run['tcc']
    print('%s, tcc=%g' % (run['Name'], tcc))

    aux_file = run['Dir'] + run['Name'] + '/%s.aux' % run['Name']
    #cloud_mass = np.loadtxt(aux_file, usecols=2)
    #snapnum_list = np.loadtxt(aux_file, usecols=0, dtype=int)
    snapnum_list = np.array(run['f_list'], dtype=int)

    for i in range(len(snapnum_list)):
        snapnum = snapnum_list[i]
        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  '%04d' % snapnum)
        data.add_field(('gas', 'cooling_time'), function = _cooling_time, sampling_type='cell', force_override=True, take_log=True)
        allDataRegion = data.all_data()
        cm = allDataRegion.quantities.center_of_mass()
        cloud_region = allDataRegion.cut_region(['obj["blob"] >= 0.82'])

        phs = yt.PhasePlot(cloud_region, x_field=('gas', 'density'), y_field=('gas', 'cooling_time'), z_fields=('gas', 'mass'), weight_field=None)
        if 'ld' in run['Name']:
            phs.set_xlim(1e-30, 5e-25)
        else:
            phs.set_xlim(1e-28, 5e-23)
        
        phs.set_ylim(0.005, 5000)
        phs.annotate_title('%04d' % snapnum)
        phs.set_font_size(40)
        phs.save(savepath_rho_tcc + '%s_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 400})

        phs = yt.PhasePlot(cloud_region, x_field=('gas', 'density'), y_field=('gas', 'temperature'), z_fields=('gas', 'mass'), weight_field=None)
        if 'ld' in run['Name']:
            phs.set_xlim(1e-30, 5e-25)
        else:
            phs.set_xlim(1e-28, 5e-23)
        
        phs.set_ylim(5e3, 1e8)
        phs.annotate_title('%04d' % snapnum)
        phs.set_font_size(40)
        phs.save(savepath_rho_T + '%s_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 400})

if __name__ == '__main__':
    with Pool(len(runlist)) as p:
        p.map(main, runlist)
