import numpy as np
import yt
import os
from multiprocessing import Pool
from cloud_util import runs, mu_ionized



runlist = []
#runlist.append(runs['runp1'])
#runlist.append(runs['runp2'])
#runlist += ([runs['runp%d' % i] for i in range(11, 16)])
#runlist.append(runs['runp9'])
runlist.append(runs['runp14'])
#runlist.append(runs['runp15'])
#runlist.append(runs['runp16'])
#runlist.append(runs['runp17'])
#runlist.append(runs['runp18'])

v_frame = 0

def _temp_to_energy(field, data):
    temperature = data['gas', 'temperature']
    energy = temperature.to('K').value * 8.617e-5
    return data.ds.arr(energy, 'eV')

def _kTenergy_scaled(field, data):
    return data['gas', 'kTenergy'] / 1.4

def _vely_scaled(field, data):
    return data.ds.arr(data['gas', 'velocity_y'].to('km/s').value + v_frame, 'km/s')


def main(run):
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
            slc = yt.SlicePlot(data, 'z', ("gas", "density"), center='center', width=((8.2, 'kpc'), (5.8, 'kpc')))
            slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
        else:
            slc = yt.SlicePlot(data, 'z', ("gas", "density"), center='center', width=((1.5, 'kpc'), (1.2, 'kpc')))
            slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))

        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath + '%s_%04d' % (run['Name'], snapnum))
    '''
        
    #run = runx6
    savepath_density = 'figures/%s/slice_z/' % run['Name']
    savepath_temperature = 'figures/%s/temperature_z/' % run['Name']
    savepath_pressure = 'figures/%s/pressure_z/' % run['Name']
    savepath_metl = 'figures/%s/metl_z/' % run['Name']
    savepath_radi = 'figures/%s/radi_z/' % run['Name']
    savepath_blob = 'figures/%s/blob_z/' % run['Name']
    savepath_velx = 'figures/%s/vel_x/' % run['Name']
    savepath_vely = 'figures/%s/vel_y/' % run['Name']
    savepath_velz = 'figures/%s/vel_z/' % run['Name']
    savepath_vely_T = 'figures/%s/vel_y_T/' % run['Name']

    os.makedirs(savepath_density, exist_ok=True)
    os.makedirs(savepath_temperature, exist_ok=True)
    os.makedirs(savepath_pressure, exist_ok=True)
    #os.makedirs(savepath_metl, exist_ok=True)
    #os.makedirs(savepath_radi, exist_ok=True)
    #os.makedirs(savepath_blob, exist_ok=True)
    os.makedirs(savepath_velx, exist_ok=True)
    os.makedirs(savepath_vely, exist_ok=True)
    os.makedirs(savepath_velz, exist_ok=True)
    #os.makedirs(savepath_vely_T, exist_ok=True)

    #for snapnum in range(len(run['f_list_full'])):
    cloud_radius = run['radius'] * yt.units.pc
    rho_0 = run['rho_0'] * yt.units.g / yt.units.cm ** 3
    rho_amb = rho_0 / run['chi']
    T_amb = 1e4 * yt.units.K * run['chi']
    tcc = run['tcc']
    init_pressure = (T_amb * rho_amb / (mu_ionized * yt.units.mp) * yt.units.kb).to('erg/cm**3')
    for i in range(len(run['f_list_full'])):
        snapnum = int(run['f_list_full'][i])
        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  '%04d' % snapnum)
        current_time = data.current_time.to('Myr').value
        data.add_field(('gas', 'kTenergy'), function=_temp_to_energy, sampling_type='cell', display_name='kT', units='eV')
        data.add_field(('gas', 'kTenergy_scaled'), function=_kTenergy_scaled, sampling_type='cell', display_name='kT', units='eV')
        data.add_field(('gas', 'vely_scaled'), function=_vely_scaled, sampling_type='cell', display_name='v_y', units='km/s')
        allDataRegion = data.all_data()
        cm = allDataRegion.quantities.center_of_mass()
        undisturbed_ambient = allDataRegion.cut_region(['obj["blob"] <= 1e-3'])
        v_amb = undisturbed_ambient.quantities.weighted_average_quantity('velocity_y', weight='cell_mass').to('km/s').value
        v_frame = run['velocity'] - v_amb
        #slc = yt.SlicePlot(data, 'z', ("gas", "density"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        slc = yt.SlicePlot(data, 'z', ("gas", "density"), center='center')
        slc.set_zlim(('gas', 'density'), zmin=rho_amb / 2, zmax=3 * rho_0)
        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath_density + '%s_density_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})

        #slc = yt.SlicePlot(data, 'z', ('gas', 'kTenergy'), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        #slc.set_zlim(('gas', 'kTenergy'), zmin=(0, 'eV'), zmax=(3000, 'eV'))
        #slc.set_log(('gas', 'kTenergy'), False)
        #slc.set_unit(('gas', 'kTenergy'), 'eV')
        #slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        #slc.save(savepath_temperature + '%s_temperature_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})
        #slc = yt.SlicePlot(data, 'z', ('gas', 'temperature'), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        slc = yt.SlicePlot(data, 'z', ('gas', 'temperature'), center='center')
        slc.set_zlim(('gas', 'temperature'), zmin=(6e3, 'K'), zmax=(3 * T_amb))
        #slc.set_log(('gas', 'kTenergy'), False)
        #slc.set_unit(('gas', 'kTenergy'), 'eV')
        slc.set_unit(('gas', 'temperature'), 'K')
        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath_temperature + '%s_temperature_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})
        '''
        slc = yt.SlicePlot(data, 'z', ("gas", "velocity_x"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        slc.set_zlim(('gas', 'velocity_x'), zmin=(-500, 'km/s'), zmax=(500, 'km/s'))
        slc.set_unit(('gas', 'velocity_x'), 'km/s')
        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath_velx + '%s_velocity_x_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})

        slc = yt.SlicePlot(data, 'z', ("gas", "velocity_y"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        slc.set_zlim(('gas', 'velocity_y'), zmin=(0, 'km/s'), zmax=(2500, 'km/s'))
        slc.set_unit(('gas', 'velocity_y'), 'km/s')
        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath_vely + '%s_velocity_y_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})

        slc = yt.SlicePlot(data, 'z', ("gas", "velocity_z"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        slc.set_zlim(('gas', 'velocity_z'), zmin=(-500, 'km/s'), zmax=(500, 'km/s'))
        slc.set_unit(('gas', 'velocity_z'), 'km/s')
        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath_velz + '%s_velocity_z_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})
        '''

        #phs = yt.PhasePlot(data, x_field=('gas', 'vely_scaled'), y_field=('gas', 'kTenergy'), z_fields=('gas', 'mass'), weight_field=None)
        #phs.set_log(('gas', 'kTenergy'), False)
        #phs.set_log(('gas', 'vely_scaled'), False)
        #phs.set_unit(('gas', 'vely_scaled'), 'km/s')
        #phs.set_xlim(0, 1320)
        #phs.set_ylim(0, 3640)
        #phs.save(savepath_vely_T + '%s_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})

        #slc = yt.SlicePlot(data, 'z', ("gas", "pressure"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        slc = yt.SlicePlot(data, 'z', ("gas", "pressure"), center='center')
        slc.set_zlim(('gas', 'pressure'), zmin=0.1 * init_pressure, zmax=10 * init_pressure)
        slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        slc.save(savepath_pressure + '%s_pressure_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})

        try:
            #slc = yt.SlicePlot(data, 'z', ("flash", "metl"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
            slc = yt.SlicePlot(data, 'z', ("flash", "metl"), center='center')
            slc.set_log(("flash", "metl"), log=False)
            slc.set_zlim(("flash", "metl"), zmin=0, zmax=1)
            slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
            slc.save(savepath_metl + '%s_metl_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})
        except:
            continue

        #try:
        #    slc = yt.SlicePlot(data, 'z', ("flash", "radi"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        #    slc.set_zlim(("flash", "radi"), zmin=-0.3, zmax=-1e-5)
        #    slc.set_cmap(field=("flash", "radi"), cmap="arbre_r")
        #    slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        #    slc.save(savepath_radi + '%s_radi_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})
        #except:
        #    continue

        #try:
        #    slc = yt.SlicePlot(data, 'z', ("flash", "blob"), center='center', width=(20 * cloud_radius, 14 * cloud_radius))
        #    #slc.set_log(("flash", "blob"), log=False)
        #    slc.set_zlim(("flash", "blob"), zmin=1e-5, zmax=1)
        #    slc.annotate_title(r'$t/t_{\mathrm{cc}}=%g$' % round(abs(current_time / tcc), 2))
        #    slc.save(savepath_blob + '%s_blob_%04d' % (run['Name'], snapnum), mpl_kwargs={'dpi': 600})
        #except:
        #    continue

if __name__ == '__main__':
    with Pool() as p:
        p.map(main, runlist)
