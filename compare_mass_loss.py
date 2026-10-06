import numpy as np
import yt
from matplotlib import pyplot as plt
from cloud_util import runs

run_list = []
run_list.append(runs['runx4'])
run_list.append(runs['runa1'])

box_left = np.array([-4, -1, -4]) * yt.units.kpc
box_right = np.array([4, 5, 4]) * yt.units.kpc

if __name__ == '__main__':
    time_list = []
    mass_list = []

    for run in run_list:
        run_name = run['Name']
        directory = run['Dir']
        timeNum_list = list(range(len(run['f_list_full'])))
        tcc = run['tcc']
        init_cloud_mass = 1.951e38 * yt.units.g
        time_list.append([])
        mass_list.append([])

        for i in timeNum_list:
            snapnum = int(run['f_list_full'][i])
            data = yt.load(run['Dir'] + run['Name'] + '/%s' % (run['name_template'] % snapnum))
            current_time = data.current_time.to('Myr').value
            time_list[-1].append(current_time)

            allDataRegion = data.all_data()
            cloud_center = allDataRegion.argmax(('gas', 'density'))

            box_region = allDataRegion.region(cloud_center, cloud_center + box_left, cloud_center + box_right)

            blobcut_region_1 = box_region.cut_region(['obj["blob"] >= 0.82'])

