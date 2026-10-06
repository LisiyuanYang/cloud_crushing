import numpy as np
import yt
import os
from gen_aux_data_athenapk import _blob

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

if __name__ == '__main__':
    #snapnum_x1 = 12
    #snapnum_4 = 33
    '''
    run = run17
    savepath = 'figures/%s/slice_y/' % run['Name']
    os.makedirs(savepath, exist_ok=True)
    
    for snapnum in range(0, 136, 5):
        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' +  '%04d' % snapnum)
        allDataRegion = data.all_data()
        cm = allDataRegion.quantities.center_of_mass()
        if 'ld' in run['Name']:
            slc = yt.SlicePlot(data, 'y', ("gas", "density"), center=cm, width=((8.2, 'kpc'), (5.8, 'kpc')))
            slc.set_zlim(('gas', 'density'), zmin=(1e-30, 'g/cm**3'), zmax=(5e-25, 'g/cm**3'))
        else:
            slc = yt.SlicePlot(data, 'y', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.2, 'kpc')))
            slc.set_zlim(('gas', 'density'), zmin=(1e-28, 'g/cm**3'), zmax=(5e-23, 'g/cm**3'))

        slc.annotate_title('%04d' % snapnum)
        slc.save(savepath + '%s_%04d' % (run['Name'], snapnum))
    '''
        
    #run = runx6
    for run in runlist:
        savepath_density_y = 'figures/%s/slice_y/' % run['Name']
        savepath_temperature_y = 'figures/%s/temperature_y/' % run['Name']
        savepath_pressure_y = 'figures/%s/pressure_y/' % run['Name']
        savepath_metl_y = 'figures/%s/metl_y/' % run['Name']
        savepath_radi_y = 'figures/%s/radi_y/' % run['Name']
        savepath_blob_y = 'figures/%s/blob_y/' % run['Name']

        os.makedirs(savepath_density_y, exist_ok=True)
        os.makedirs(savepath_temperature_y, exist_ok=True)
        os.makedirs(savepath_pressure_y, exist_ok=True)
        os.makedirs(savepath_metl_y, exist_ok=True)
        os.makedirs(savepath_radi_y, exist_ok=True)
        os.makedirs(savepath_blob_y, exist_ok=True)

        savepath_density_z = 'figures/%s/slice_z/' % run['Name']
        savepath_temperature_z = 'figures/%s/temperature_z/' % run['Name']
        savepath_pressure_z = 'figures/%s/pressure_z/' % run['Name']
        savepath_metl_z = 'figures/%s/metl_z/' % run['Name']
        savepath_radi_z = 'figures/%s/radi_z/' % run['Name']
        savepath_blob_z = 'figures/%s/blob_z/' % run['Name']

        os.makedirs(savepath_density_z, exist_ok=True)
        os.makedirs(savepath_temperature_z, exist_ok=True)
        os.makedirs(savepath_pressure_z, exist_ok=True)
        os.makedirs(savepath_metl_z, exist_ok=True)
        os.makedirs(savepath_radi_z, exist_ok=True)
        os.makedirs(savepath_blob_z, exist_ok=True)

        #for snapnum in range(len(run['f_list_full'])):
        for i in range(len(run['f_list_full'])):
            snapnum = int(run['f_list_full'][i])
            data = yt.load(run['Dir'] + run['Name'] + '/%s' % (run['Snapshot_name'] % snapnum))
            data.add_field(('parthenon','blob'), function=_blob, sampling_type='cell', display_name=r'$C_{\mathrm{cloud}}$', units='dimensionless')
            allDataRegion = data.all_data()
            cloudRegion = allDataRegion.cut_region(['obj[("parthenon", "blob")] >= 0.5'])
            cm = cloudRegion.quantities.center_of_mass().to('kpc')

            cm[1] += 0.25 * yt.units.kpc

            slc = yt.SlicePlot(data, 'y', ("gas", "density"), center=cm, width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
            slc.set_zlim(('gas', 'density'), zmin=(1e-27, 'g/cm**3'), zmax=(5e-24, 'g/cm**3'))
            slc.annotate_title('%04d' % snapnum)
            slc.annotate_text([0.85, 0.75], 'y=%.2g' % cm[1].to('kpc').value, coord_system='axis')
            slc.save(savepath_density_y + '%s_density_%04d' % (run['Name'], snapnum))

            slc = yt.SlicePlot(data, 'y', ("gas", "temperature"), center=cm, width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
            slc.set_zlim(('gas', 'temperature'), zmin=(1e4, 'K'), zmax=(1e6, 'K'))
            slc.annotate_title('%04d' % snapnum)
            slc.annotate_text([0.85, 0.75], 'y=%.2g' % cm[1].to('kpc').value, coord_system='axis')
            slc.save(savepath_temperature_y + '%s_temperature_%04d' % (run['Name'], snapnum))

            slc = yt.SlicePlot(data, 'y', ("gas", "pressure"), center=cm, width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
            slc.set_zlim(('gas', 'pressure'), zmin=(1e-14, 'erg/cm**3'), zmax=(1e-10, 'erg/cm**3'))
            slc.annotate_title('%04d' % snapnum)
            slc.annotate_text([0.85, 0.75], 'y=%.2g' % cm[1].to('kpc').value, coord_system='axis')
            slc.save(savepath_pressure_y + '%s_pressure_%04d' % (run['Name'], snapnum))
            '''
            try:
                slc = yt.SlicePlot(data, 'y', ("flash", "metl"), center=cm, width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
                #slc.set_log(("flash", "metl"), log=False)
                slc.set_zlim(("flash", "metl"), zmin=1e-5, zmax=1)
                slc.annotate_title('%04d' % snapnum)
                slc.save(savepath_metl_y + '%s_metl_%04d' % (run['Name'], snapnum))
            except:
                continue


            try:
                slc = yt.SlicePlot(data, 'y', ("flash", "radi"), center=cm, width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
                slc.set_zlim(("flash", "radi"), zmin=-0.3, zmax=-1e-5)
                slc.set_cmap(field=("flash", "radi"), cmap="arbre_r")
                slc.annotate_title('%04d' % snapnum)
                slc.save(savepath_radi_y + '%s_radi_%04d' % (run['Name'], snapnum))
            except:
                continue
            '''

            try:
                slc = yt.SlicePlot(data, 'y', ("parthenon", "blob"), center=cm, width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
                #slc.set_log(("parthenon", "blob"), log=False)
                slc.set_zlim(("parthenon", "blob"), zmin=1e-5, zmax=1)
                slc.annotate_title('%04d' % snapnum)
                slc.annotate_text([0.85, 0.75], 'y=%.2g' % cm[1].to('kpc').value, coord_system='axis')
                slc.save(savepath_blob_y + '%s_blob_%04d' % (run['Name'], snapnum))
            except:
                pass
            
            #cm = allDataRegion.quantities.center_of_mass()
            slc = yt.SlicePlot(data, 'z', ("gas", "density"), center='center', width=((1.5, 'kpc'), (3, 'kpc')), origin="native")
            slc.set_zlim(('gas', 'density'), zmin=(1e-27, 'g/cm**3'), zmax=(5e-24, 'g/cm**3'))
            slc.annotate_title('%04d' % snapnum)
            #slc.annotate_text([0.85, 0.75], 'z=%.2g' % cm[2].to('kpc').value, coord_system='axis')
            slc.save(savepath_density_z + '%s_density_%04d' % (run['Name'], snapnum))

            slc = yt.SlicePlot(data, 'z', ("gas", "temperature"), center='center', width=((1.5, 'kpc'), (3, 'kpc')), origin="native")
            slc.set_zlim(('gas', 'temperature'), zmin=(1e4, 'K'), zmax=(1e6, 'K'))
            slc.annotate_title('%04d' % snapnum)
            #slc.annotate_text([0.85, 0.75], 'z=%.2g' % cm[2].to('kpc').value, coord_system='axis')
            slc.save(savepath_temperature_z + '%s_temperature_%04d' % (run['Name'], snapnum))

            slc = yt.SlicePlot(data, 'z', ("gas", "pressure"), center='center', width=((1.5, 'kpc'), (3, 'kpc')), origin="native")
            slc.set_zlim(('gas', 'pressure'), zmin=(1e-14, 'erg/cm**3'), zmax=(1e-10, 'erg/cm**3'))
            slc.annotate_title('%04d' % snapnum)
            #slc.annotate_text([0.85, 0.75], 'z=%.2g' % cm[2].to('kpc').value, coord_system='axis')
            slc.save(savepath_pressure_z + '%s_pressure_%04d' % (run['Name'], snapnum))
            '''
            try:
                slc = yt.SlicePlot(data, 'z', ("flash", "metl"), center='center', width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
                #slc.set_log(("flash", "metl"), log=False)
                slc.set_zlim(("flash", "metl"), zmin=1e-5, zmax=1)
                slc.annotate_title('%04d' % snapnum)
                slc.save(savepath_metl_z + '%s_metl_%04d' % (run['Name'], snapnum))
            except:
                continue


            try:
                slc = yt.SlicePlot(data, 'z', ("flash", "radi"), center='center', width=((1.5, 'kpc'), (1.5, 'kpc')), origin="native")
                slc.set_zlim(("flash", "radi"), zmin=-0.3, zmax=-1e-5)
                slc.set_cmap(field=("flash", "radi"), cmap="arbre_r")
                slc.annotate_title('%04d' % snapnum)
                slc.save(savepath_radi_z + '%s_radi_%04d' % (run['Name'], snapnum))
            except:
                continue
            '''

            try:
                slc = yt.SlicePlot(data, 'z', ("parthenon", "blob"), center='center', width=((1.5, 'kpc'), (3, 'kpc')), origin="native")
                #slc.set_log(("parthenon", "blob"), log=False)
                slc.set_zlim(("parthenon", "blob"), zmin=1e-5, zmax=1)
                slc.annotate_title('%04d' % snapnum)
                #slc.annotate_text([0.85, 0.75], 'z=%.2g' % cm[2].to('kpc').value, coord_system='axis')
                slc.save(savepath_blob_z + '%s_blob_%04d' % (run['Name'], snapnum))
            except:
                pass

