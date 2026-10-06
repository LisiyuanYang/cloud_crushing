import numpy as np
import h5py
import yt
import sys
from multiprocessing import Pool
from cloud_util import runs

#runlist = [runx2, runx4, runx5, runx3, runx6, run4, run16, run17, run6, run5]
#runlist = [runx7, runx8, runx9, runx10, runx11, runx12]
#runlist = [runx2, runx4, runx5, runx3, runx6, runx8, runx9, runx10, runx11, runx12, runx13, runx14, runx15, runx16, runx17, runy1, runy2]
#runlist = [runx13]
#runlist = [runx14, runx15]
#runlist = [runx16, runx17]
#runlist = [runx16t2]
#runlist = [runy1, runy2]
runlist = []
runlist.append(runs['run1'])
runlist.append(runs['run2'])
runlist.append(runs['run3'])
runlist.append(runs['run11'])
runlist.append(runs['run12'])
#runlist.append(runs['runp1'])
#runlist.append(runs['runp2'])
#runlist += ([runs['runp%d' % i] for i in range(1, 16)])
#runlist.append(runs['runp9'])
#runlist.append(runs['runp14'])
#runlist.append(runs['runp16'])
#runlist.append(runs['runp17'])
#runlist.append(runs['runp18'])

def main(run):
    run_name = run['Name']
    directory = run['Dir']
    timeNum_list = list(range(len(run['f_list_full'])))
    tcc = run['tcc']

    #if 'ld' in run_name:
    #    init_cloud_mass = 1.951e38 * yt.units.g
    #else:
    #    init_cloud_mass = 1.23067e38 * yt.units.g
    init_cloud_mass = (run['init_mass'] * yt.units.Msun).to('g')
    
    aux_file = directory + run_name + '/%s.dat' % run_name
    distance = 0
    previous_time = 0
    previous_vblob = 0
    with open(aux_file, 'w') as f:
        f.write('#snapnum t/tcc f_blob_0.82 f_blob_0.5 f_rho xc yc zc v_blob v_rho d vol\n')
        for timeNum in timeNum_list:
            snapnum = int(run['f_list_full'][timeNum])
            data = yt.load(directory + run_name + '/KH_hdf5_chk_' +  run['f_list_full'][timeNum])
            print(run_name, snapnum)
            sys.stdout.flush()
            current_time = data.current_time.to('Myr').value
            dtime = current_time - previous_time
            previous_time = current_time
            allDataRegion = data.all_data()
            blobcut_region_1 = allDataRegion.cut_region(['obj["blob"] >= 0.82'])
            blobcut_region_2 = allDataRegion.cut_region(['obj["blob"] >= 0.5'])

            #if 'ld' in run_name:
            #    densitycut_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-27'])
            #else:
            #    densitycut_region = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])
            densitycut_region = allDataRegion.cut_region(['obj["density"] >= %g' % (run['rho_0'] / 3)])

            undisturbed_ambient = allDataRegion.cut_region(['obj["blob"] <= 1e-3'])
            
            f_blob_1 = (blobcut_region_1.quantities.total_mass()[0] / init_cloud_mass).value
            f_blob_2 = (blobcut_region_2.quantities.total_mass()[0] / init_cloud_mass).value
            f_rho = (densitycut_region.quantities.total_mass()[0] / init_cloud_mass).value
            c = allDataRegion.quantities.center_of_mass().to('pc').value
            v_blob = blobcut_region_2.quantities.weighted_average_quantity('velocity_y', weight='cell_mass').to('km/s').value
            v_rho = densitycut_region.quantities.weighted_average_quantity('velocity_y', weight='cell_mass').to('km/s').value
            v_amb = undisturbed_ambient.quantities.weighted_average_quantity('velocity_y', weight='cell_mass').to('km/s').value
            v_frame = run['velocity'] - v_amb
            v_blob += v_frame
            v_rho += v_frame
            distance += dtime * (run['velocity'] - (previous_vblob + v_blob) / 2) * 1.022e-3 #in kpc
            previous_vblob = v_blob
            volume_cloud = np.sum(blobcut_region_2['gas', 'cell_volume']).to('kpc**3')

            #with h5py.File(directory + run_name + '/KH_hdf5_chk_' +  run['f_list_full'][timeNum], 'r') as g:
            #    velframe = g['real scalars'][7][1] / 1e5
            #
            #v_blob += velframe
            #v_rho += velframe        

            f.write('%d\t%9.2f\t%9.4f\t%9.4f\t%9.4f\t%9.3f\t%9.3f\t%9.3f\t%9.2f\t%9.2f\t%9.2f\t%9.2f\n' % (snapnum, current_time / tcc, f_blob_1, f_blob_2, f_rho, c[0], c[1], c[2], v_blob, v_rho, distance, volume_cloud))
            f.flush()

if __name__ == '__main__':
    with Pool() as p:
        p.map(main, runlist)
    #for run in runlist:
    #    main(run)
