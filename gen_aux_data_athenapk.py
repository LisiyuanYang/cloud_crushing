import numpy as np
import h5py
import yt
import sys
from multiprocessing import Pool

run1 = { 'Name':'T0.3_v1700_chi300',
         'Formal_name':'T0.3_v1700_chi300_old',
         'Snapshot_name':'KH_hdf5_chk_%04d',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085'],
        'f_list_full':sorted(set(['%04d' % i for i in range(106)[: : 5]] + ['0022', '0032', '0053', '0085']))}

run2 = { 'Name':'T0.3_v1700_chi300_cond',
         'Formal_name':'T0.3_v1700_chi300_cond_old',
         'Snapshot_name':'KH_hdf5_chk_%04d',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078'],
        'f_list_full':['0003', '0020', '0046', '0078']}

run3 = { 'Name':'cloud_chi300beta100v1700transcond',
         'Formal_name':'T0.3_v1700_chi300_beta100_transcond',
         'Snapshot_name':'parthenon.restart.%05d.rhdf',
        'Dir':'/nas/astro-th/lyang/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['00003', '00020', '00039', '00050'],
        'f_list_full':['%05d' % i for i in range(51)]}


runlist = []
runlist.append(run3)

def _blob(field, data):
    density = np.array(data['parthenon','Density'].to('code_mass/code_length**3'))
    scalar_0 = np.array(data['parthenon','Scalar_0'])
    blob = scalar_0 / density
    return (
        data.ds.arr(blob, 'dimensionless')
    )

def main(run):
    run_name = run['Name']
    directory = run['Dir']
    timeNum_list = list(range(len(run['f_list_full'])))
    tcc = run['tcc'] * 3.156e13

    #if 'ld' in run_name:
    #    init_cloud_mass = 1.951e38 * yt.units.g
    #else:
    #    init_cloud_mass = 1.23067e38 * yt.units.g
    #init_cloud_mass = 1.951e38 * yt.units.g
    
    aux_file = directory + run_name + '/%s.aux' % run_name
    with open(aux_file, 'w') as f:
        f.write('#snapnum t/tcc f_blob_0.82 f_blob_0.5 f_rho xc yc zc v_blob v_rho\n')
        for timeNum in timeNum_list:
            snapnum = int(run['f_list_full'][timeNum])
            data = yt.load(directory + run_name + '/%s' % (run['Snapshot_name'] % snapnum))
            print(run_name, snapnum)
            sys.stdout.flush()
            current_time = data.current_time.to('s').value
            data.add_field(('parthenon','blob'), function=_blob, sampling_type='cell', display_name='C_cloud', units='dimensionless')
            allDataRegion = data.all_data()
            blobcut_region_1 = allDataRegion.cut_region(['obj[("parthenon", "blob")] >= 0.82'])
            blobcut_region_2 = allDataRegion.cut_region(['obj[("parthenon", "blob")] >= 0.5'])

            #if 'ld' in run_name:
            #    densitycut_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-27'])
            #else:
            #    densitycut_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])
            densitycut_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])

            if timeNum == 0:
                init_cloud_mass = densitycut_region.quantities.total_mass()[0]

            f_blob_1 = (blobcut_region_1.quantities.total_mass()[0] / init_cloud_mass).value
            f_blob_2 = (blobcut_region_2.quantities.total_mass()[0] / init_cloud_mass).value
            f_rho = (densitycut_region.quantities.total_mass()[0] / init_cloud_mass).value
            c = allDataRegion.quantities.center_of_mass().to('pc').value
            v_blob = blobcut_region_2.quantities.weighted_average_quantity('velocity_y', weight='cell_mass').to('km/s').value
            v_rho = densitycut_region.quantities.weighted_average_quantity('velocity_y', weight='cell_mass').to('km/s').value

            #with h5py.File(directory + run_name + '/KH_hdf5_chk_' +  run['f_list_full'][timeNum], 'r') as g:
            #    velframe = g['real scalars'][7][1] / 1e5
            #
            #v_blob += velframe
            #v_rho += velframe        

            f.write('%d\t%9.2f\t%9.4f\t%9.4f\t%9.4f\t%9.3f\t%9.3f\t%9.3f\t%9.2f\t%9.2f\n' % (snapnum, current_time / tcc, f_blob_1, f_blob_2, f_rho, c[0], c[1], c[2], v_blob, v_rho))
            f.flush()

if __name__ == '__main__':
    #with Pool(len(runlist)) as p:
    #    p.map(main, runlist)
    for run in runlist:
        main(run)
