import numpy as np
from matplotlib import pyplot as plt
import os
from cloud_util import runs, h, data_path_base, ions
from ion_emission_maps import HM_index_list, timenum_list, redshift_list, width, Npixels

ion = ions['O VI']
timenum = 0
redshift_index = 0
redshift = redshift_list[redshift_index]
#HM_index = 4
HM_index = 0
HM_coeff = HM_index_list[HM_index]
xlist = np.linspace(-500 * width[0].value, 500 * width[0].value, Npixels[0] + 1)
ylist = np.linspace(-500 * width[1].value, 500 * width[1].value, Npixels[1] + 1)

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
    map_path_base = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/'

    fig, axes = plt.subplots(2, len(run_list), figsize=(3 * len(run_list) + 1, 8))
    for i in range(len(run_list)):
        run = run_list[i]
        run_name = run['Name']
        dataset = np.load(map_path_base % run_name + '%s_emission_maps_2.npz' % ion['ion'].replace(' ', '_'))
        #for i in range(len(timenum_list)):
        emission_map = dataset['emission_map_table'][timenum, redshift_index, 0]
        ion_colume_density_map = dataset['column_density_map_table'][timenum, redshift_index, 0]

        pcm = axes[0][i].pcolormesh(xlist, ylist, np.log10(ion_colume_density_map.T), vmin=11, vmax=14, cmap='plasma', rasterized=True)
        axes[0][i].tick_params(right=True, top=True, direction='in', labelsize=16)
        axes[0][i].set_xlim(xlist[0], xlist[-1])
        axes[0][i].set_ylim(ylist[0], ylist[-1])
        axes[0][i].set_aspect('equal')
        axes[0][i].set_xticklabels([])
        if i == 0:
            #axes[0][i].text(0.05, 0.9, 'n(%s)' % ion['ion'], fontsize=16, c='red', transform=axes[0][i].transAxes)
            axes[0][i].set_ylabel('y/pc', fontsize=16)
        else:
            axes[0][i].set_yticklabels([])

        axes[0][i].set_title('%s' % run['Formal_name'], fontsize=16)
        if i == axes.shape[1] - 1:
            cbar_ax = axes[0][i].inset_axes([1.05, 0, 0.05, 1], transform=axes[0][i].transAxes)
            cb = plt.colorbar(pcm, cax=cbar_ax)
            cb.ax.tick_params(labelsize=16)
            cb.ax.set_ylabel(r'$\log[N(\mathrm{%s})/\mathrm{cm^{-2}}]$' % ion['ion'], fontsize=16)
        
        pcm = axes[1][i].pcolormesh(xlist, ylist, np.log10(emission_map.T), vmin=-11.5, vmax=-8, cmap='plasma', rasterized=True)
        axes[1][i].tick_params(right=True, top=True, direction='in', labelsize=16)
        axes[1][i].set_xlim(xlist[0], xlist[-1])
        axes[1][i].set_ylim(ylist[0], ylist[-1])
        axes[1][i].set_xlabel('x/pc', fontsize=16)
        axes[1][i].set_aspect('equal')
        if i == 0:
            #axes[1][i].text(0.05, 0.9, 'n(%s)' % ion['ion'], fontsize=16, c='red', transform=axes[1][i].transAxes)
            axes[1][i].set_ylabel('y/pc', fontsize=16)
            #axes[1][i].set_title('%s' % run['Formal_name'], fontsize=16)
        else:
            axes[1][i].set_yticklabels([])
        if i == axes.shape[1] - 1:
            cbar_ax = axes[1][i].inset_axes([1.05, 0, 0.05, 1], transform=axes[1][i].transAxes)
            cb = plt.colorbar(pcm, cax=cbar_ax)
            cb.ax.tick_params(labelsize=16)
            cb.ax.set_ylabel(r'$\log[I(%s)/\gamma\mathrm{cm^{-2}s^{-1}arcsec^{-2}}]$' % ion['ion'], fontsize=16)

    savepath = 'figures/%s/ion_maps/' % run_list[0]['Name']
    os.makedirs(savepath, exist_ok=True)
    fig.subplots_adjust(wspace=0.25, hspace=0.05)
    plt.savefig(savepath + '%s_emission_z%g.pdf' % (ion['ion'].replace(' ', '_'), redshift), bbox_inches='tight')
