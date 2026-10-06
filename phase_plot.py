import numpy as np
import h5py
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import AxesGrid
import yt
from cloud_util import runs
import os

Npix = 400
pixel_size = 10 #in pc


runlist = []
##add only the 3 different conduction levels

#runlist.append(runs['run4'])    #T0.3_v1000_chi300
#runlist.append(runs['runx2'])   #T0.3_v1000_chi300_ld2
#runlist.append(runs['run1'])   #T0.3_v1000_chi300_cond
#runlist.append(runs['runx14'])   #T0.3_v1000_chi300_cond_0.1_ld2
#runlist.append(runs['runx8'])   #T0.3_v1000_chi300_cond_ld2

#runlist.append(runs['run16'])  #T0.3_v1700_chi300
runlist.append(runs['runx4'])   #T0.3_v1700_chi300_ld2
#runlist.append(runs['run11'])  #T0.3_v1700_chi300_cond
#runlist.append(runs['runx16'])   #T0.3_v1700_chi300_cond_0.1_ld2
#runlist.append(runs['runx10'])  #T0.3_v1700_chi300_cond_lds

#runlist.append(runs['run17'])  #T0.3_v3000_chi300
#runlist.append(runs['runx5'])   #T0.3_v3000_chi300_ld2
#runlist.append(runs['run12'])  #T0.3_v3000_chi300_cond
#runlist.append(runs['runx17'])   #T0.3_v3000_chi300_cond_0.1_ld2
#runlist.append(runs['runx11'])  #T0.3_v3000_chi300_cond_ld2

#runlist.append(runs['run6'])   #T1_v1700_chi1000
#runlist.append(runs['runx3'])   #T1_v1700_chi1000_ld2
#runlist.append(runs['run3'])   #T1_v1700_chi1000_cond
#runlist.append(runs['runx13'])   #T1_v1700_chi1000_cond_0.1_ld2
#runlist.append(runs['runx9'])   #T1_v1700_chi1000_cond_ld2

#runlist.append(runs['run5'])   #T3_v3000_chi3000
#runlist.append(runs['runx6'])   #T3_v3000_chi3000_ld2
#runlist.append(runs['run2'])   #T3_v3000_chi3000_cond
#runlist.append(runs['runx15'])   #T3_v3000_chi3000_cond_0.1_ld2
#runlist.append(runs['runx12'])   #T3_v3000_chi3000_cond_ld2

#runlist.append(runs['runy1'])
#runlist.append(runs['runy2'])
#runlist.append(runs['runz1'])
runlist.append(runs['runa1'])   #T0.3_v1700_chi300_apk

if __name__  == '__main__':
    timenum = 2
    snapnum_list = [41, 80]
    phs_list = []
    density_hist_list = []
    temperature_hist_list = []
    savepath = 'figures/'
    realtime_list = []
    os.makedirs(savepath, exist_ok=True)
    for i in range(len(runlist)):
        run = runlist[i]
        #savepath_run = savepath + run['Name'] + '/'
        #os.makedirs(savepath_run, exist_ok=True)
        #snapnum = int(run['f_list'][timenum])
        snapnum = snapnum_list[i]
        times = np.loadtxt(run['Dir'] + run['Name'] + '/%s.aux' % run['Name'], usecols=1)
        realtime_list.append(times[snapnum] * run['tcc'])
        data = yt.load(run['Dir'] + run['Name'] + '/' + run['name_template'] % snapnum)
        allDataRegion = data.all_data()
        if 'apk' in run['Name']:
            cloud_region = allDataRegion.cut_region(['obj["parthenon", "prim_scalar_0"] >= 0.5'])
        else:
            cloud_region = allDataRegion.cut_region(['obj["blob"] >= 0.5'])
        phs = yt.PhasePlot(cloud_region, x_field=('gas', 'density'), y_field=('gas', 'temperature'), z_fields=('gas', 'mass'), weight_field=None)
        phs.set_xlim(3e-30, 9.9e-25)
        phs.set_ylim(4e3, 6e7)
        phs.set_zlim(('gas', 'mass'), 1e31, 1e36)
        phs_list.append(phs)

        density_hist = yt.ProfilePlot(cloud_region, ('gas', 'density'), ('gas', 'mass'), weight_field=None)
        density_hist.set_xlim(1e-29, 1e-24)
        density_hist.set_ylim(('gas', 'mass'), 1e33, 6e37)
        density_hist_list.append(density_hist)

        temperature_hist = yt.ProfilePlot(cloud_region, ('gas', 'temperature'), ('gas', 'mass'), weight_field=None)
        temperature_hist.set_xlim(4e3, 6e7)
        temperature_hist.set_ylim(('gas', 'mass'), 1e33, 6e37)
        temperature_hist_list.append(temperature_hist)
        #phs.save(savepath_run, mpl_kwargs={'dpi': 400})
    '''
    fig = plt.figure()
    grid = AxesGrid(fig, (0.075, 0.075, 0.85, 0.95), nrows_ncols=(3, 3), direction='column', axes_pad=0.05, label_mode="L", share_all=True,\
                 cbar_location="right", cbar_mode="single", cbar_size="3%", cbar_pad="0%", aspect=False)
    for i in range(9):
        plot = phs_list[i].plots[('gas', 'mass')]
        plot.figure = fig
        plot.axes = grid[i].axes
        if i == 0:
            plot.cax = grid.cbar_axes[i]
        phs_list[i].render()
        grid[i].text(0.97, 0.9, '%s\nt=%g Myr' % (runlist[i]['Formal_name'], realtime_list[i]), c='red', fontsize=13, horizontalalignment='right', verticalalignment='center', multialignment='right', transform=grid[i].transAxes)
    
    plt.savefig(savepath + 'phase_space_%s.png' % runlist[0]['Name'], dpi=400, bbox_inches='tight')
    plt.close()
    '''
    fig = plt.figure()
    grid = AxesGrid(fig, (0.075, 0.075, 0.85, 0.95), nrows_ncols=(1, 2), direction='column', axes_pad=0.05, label_mode="L", share_all=True,\
                 cbar_location="right", cbar_mode="single", cbar_size="3%", cbar_pad="0%", aspect=False)
    for i in range(2):
        plot = phs_list[i].plots[('gas', 'mass')]
        plot.figure = fig
        plot.axes = grid[i].axes
        if i == 0:
            plot.cax = grid.cbar_axes[i]
        phs_list[i].render()
        grid[i].text(0.97, 0.9, '%s\nt=%g Myr' % (runlist[i]['Name'], realtime_list[i]), c='red', fontsize=13, horizontalalignment='right', verticalalignment='center', multialignment='right', transform=grid[i].transAxes)
    
    plt.savefig(savepath + 'phase_space_%s.png' % runlist[0]['Name'], dpi=400, bbox_inches='tight')
    plt.close()

    fig = plt.figure()
    grid = AxesGrid(fig, (0.075, 0.075, 0.85, 0.95), nrows_ncols=(1, 2), direction='column', axes_pad=0.05, label_mode="L", share_all=True,\
                 cbar_location="right", cbar_mode="single", cbar_size="3%", cbar_pad="0%", aspect=False)
    for i in range(2):
        plot = density_hist_list[i].plots[('gas', 'mass')]
        plot.figure = fig
        plot.axes = grid[i].axes
        if i == 0:
            plot.cax = grid.cbar_axes[i]
        density_hist_list[i].render()
        grid[i].text(0.97, 0.9, '%s\nt=%g Myr' % (runlist[i]['Name'], realtime_list[i]), c='red', fontsize=13, horizontalalignment='right', verticalalignment='center', multialignment='right', transform=grid[i].transAxes)
    
    plt.savefig(savepath + 'density_hist_%s.png' % runlist[0]['Name'], dpi=400, bbox_inches='tight')
    plt.close()

    fig = plt.figure()
    grid = AxesGrid(fig, (0.075, 0.075, 0.85, 0.95), nrows_ncols=(1, 2), direction='column', axes_pad=0.05, label_mode="L", share_all=True,\
                 cbar_location="right", cbar_mode="single", cbar_size="3%", cbar_pad="0%", aspect=False)
    for i in range(2):
        plot = temperature_hist_list[i].plots[('gas', 'mass')]
        plot.figure = fig
        plot.axes = grid[i].axes
        if i == 0:
            plot.cax = grid.cbar_axes[i]
        temperature_hist_list[i].render()
        grid[i].text(0.97, 0.9, '%s\nt=%g Myr' % (runlist[i]['Name'], realtime_list[i]), c='red', fontsize=13, horizontalalignment='right', verticalalignment='center', multialignment='right', transform=grid[i].transAxes)
    
    plt.savefig(savepath + 'temperature_hist_%s.png' % runlist[0]['Name'], dpi=400, bbox_inches='tight')
    plt.close()
