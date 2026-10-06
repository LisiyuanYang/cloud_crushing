import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os
from multiprocessing import Pool
from cloud_util import runs

#ion_list = ['H I 1215', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV', 'N V']
ion_list = ['H I', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV', 'N V']
ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])
indices = [0, 10, 3, 4, 6, 9] #HI, Mg II, C III, C IV, O VI, Ne VIII
cmap=matplotlib.colormaps['viridis']
scaling_factor_metal = 0 #Assuming fixed cloud mass, this number should be -2/3 times the background boost factor.
scaling_factor_HI = 0
Npix = 600
#pixel_size = 2 #in pc

run_list = []
#run_list.append(runs['runy2'])
#run_list.append(runs['runz1'])
run_list.append(runs['runp1'])
run_list.append(runs['runp2'])
run_list.append(runs['runp3'])
run_list.append(runs['runp4'])
run_list.append(runs['runp5'])
run_list.append(runs['runp6'])
run_list.append(runs['runp7'])
run_list.append(runs['runp8'])
run_list.append(runs['runp9b'])
run_list.append(runs['runp10'])
run_list.append(runs['runp11'])
run_list.append(runs['runp12'])
run_list.append(runs['runp13'])
#run_list.append(runs['runp14'])
run_list.append(runs['runp15'])
run_list.append(runs['runp16'])
run_list.append(runs['runp17'])
run_list.append(runs['runp18'])

#colors = ['blue', 'cyan', 'green', 'lime', 'red', 'orange', 'pink']
colors = ['blue', 'cyan']
#colors = ['red', 'orange']
#run_list = [run1, run4]

#do this to limit to conductive runs and preserve the colors
#run_list = [run_list[i] for i in [1, 3, 5]]
#colors = [colors[i] for i in [1, 3, 5]]

#data_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e4/TF1.0/%s_colden_%d.csv'
#blob_colden_file = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
#blob_width_file = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/HM_1e%d/TF0.6/z%g/t%d/%s_width_%d.csv'
#blob_thermal_width_file = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/HM_1e%d/TF0.6/z%g/t%d/%s_thermal_width_%d.csv'
#blob_kinematic_width_file = '/nas/astro-th/lyang/nonSorted_ColDen_23/%s/HM_1e%d/TF0.6/z%g/t%d/%s_kinematic_width_%d.csv'
blob_colden_file = '%s/nonSorted_ColDen_23/HM_1e%d/TF0.6/z%g/t%d/%s_colden_%d.csv'
blob_width_file = '%s/nonSorted_ColDen_23/HM_1e%d/TF0.6/z%g/t%d/%s_width_%d.csv'
blob_thermal_width_file = '%s/nonSorted_ColDen_23/HM_1e%d/TF0.6/z%g/t%d/%s_thermal_width_%d.csv'
blob_kinematic_width_file = '%s/nonSorted_ColDen_23/HM_1e%d/TF0.6/z%g/t%d/%s_kinematic_width_%d.csv'

def ion_maps(run, redshift):
    run_name = run['Name']
    direction = 0
    time_list = [0, 1, 2, 3]
    #time_list = [2]
    #time_list = [1, 2]
    #HM_list = np.arange(3, 5)
    HM_list = [0]
    #linestyles = [':', '--', '-']
    #linestyles = [':', '-.', '--', '-']
    #labels_run = [run['Name'] for run in run_list]
    #labels_direction = [r'$\cos \theta = %.1f$' % direction for direction in direction_list]
    #labels_times = ['t75', 't50', 't25']
    #labels_times = ['t90', 't50', 't25']
    #labels_times = ['t75', 't50', 't25']\
    pixel_size = 12 * run['radius'] / Npix #in pc
    xlist = np.arange(0, (Npix + 1) * pixel_size, pixel_size)
    ylist = np.arange(0, (Npix + 1) * pixel_size, pixel_size)

    for HM_value in HM_list:
        savepath = 'figures/%s/ion_maps/' % (run['Name'])
        os.makedirs(savepath, exist_ok=True)
        log_coldens = np.full((len(time_list), Npix ** 2, len(ion_list)), -10.)
        log_widths = np.full((len(time_list), Npix ** 2, len(ion_list)), -10.) #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
        log_temperatures = np.full((len(time_list), Npix ** 2, len(ion_list)), -10.)
        #thermal_fraction = []

        for i in range(len(time_list)):
            time = time_list[i]
            coldens = np.loadtxt(blob_colden_file % (run['Dir'] + run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            cloud_indices = coldens[:, 0].astype(int)
            log_coldens[i, cloud_indices] = np.log10(coldens[:, 1:]) + scaling_factor_metal
            log_coldens[i, :, 0] += scaling_factor_HI - scaling_factor_metal

            widths = np.loadtxt(blob_width_file % (run['Dir'] + run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            log_widths[i, cloud_indices] = np.log10(widths[:, 1:] / 1e5)

            thermal_widths = np.loadtxt(blob_thermal_width_file % (run['Dir'] + run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            #log_thermal_widths = np.log10(thermal_widths[:, 1:])
            log_temperatures[i, cloud_indices] = np.log10(6.0574e-9 * thermal_widths[:, 1:]**2 * ion_weight_list)

            for l in range(len(indices)):
                invalid_pixels = np.where(log_coldens[i, :, indices[l]] < 13)[0]
                null_pixels = np.where(log_coldens[i, :, indices[l]] < 11)[0]
                log_coldens[i, null_pixels, indices[l]] = np.nan
                log_widths[i, invalid_pixels, indices[l]] = np.nan
                log_temperatures[i, invalid_pixels, indices[l]] = np.nan
        

        fig = plt.figure(figsize=(12, 15), dpi=450)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(time_list) + 1, width_ratios=([1] * len(time_list) + [0.1]))
        for l in range(len(indices)):
            for i in range(len(time_list)):
                ax = fig.add_subplot(spec[l, i])
                if l == 0:
                    im = ax.pcolormesh(ylist, xlist, np.flip(log_coldens[i, :, indices[l]].reshape((Npix, Npix))).T, vmin=11, vmax=20, rasterized=True)
                else:
                    im = ax.pcolormesh(ylist, xlist, np.flip(log_coldens[i, :, indices[l]].reshape((Npix, Npix))).T, vmin=11, vmax=16, rasterized=True)

                if i == 0:
                    ax.set_title(ion_list[indices[l]], fontsize=15, y=0.1)
                if l == len(indices) - 1:
                    ax.set_xlabel('x/pc', fontsize=15)
                else:
                    ax.set_xticklabels([])
                ax.set_ylabel('y/pc', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                ax.set_box_aspect(1)
            
            cax = fig.add_subplot(spec[l, len(time_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_ylabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=14)
            cax.tick_params(which='both', direction='in', labelsize=13)
        
        plt.subplots_adjust(hspace=0.1, wspace=0.05)
        #plt.tight_layout()
        plt.savefig(savepath + 'ion_colden_maps_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(12, 15), dpi=300)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(time_list) + 1, width_ratios=([1] * len(time_list) + [0.06]))
        for l in range(len(indices)):
            for i in range(len(time_list)):
                ax = fig.add_subplot(spec[l, i])
                im = ax.pcolormesh(ylist, xlist, np.flip(log_widths[i, :, indices[l]].reshape((Npix, Npix))).T, vmin=0.3, vmax=2.7, rasterized=True)
                if i == 0:
                    ax.set_title(ion_list[indices[l]], fontsize=15)

                ax.set_xlabel('x/pc', fontsize=15)
                ax.set_ylabel('y/pc', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                ax.set_box_aspect(1)
            
            cax = fig.add_subplot(spec[l, len(time_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_title(r'$\log[b_{\mathrm{total}}/(\mathrm{km/s})]$', fontsize=14)
            cax.tick_params(which='both', direction='in', labelsize=13)
        
        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'ion_width_maps_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(12, 15), dpi=300)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(time_list) + 1, width_ratios=([1] * len(time_list) + [0.06]))
        for l in range(len(indices)):
            for i in range(len(time_list)):
                ax = fig.add_subplot(spec[l, i])
                im = ax.pcolormesh(ylist, xlist, np.flip(log_temperatures[i, :, indices[l]].reshape((Npix, Npix))).T, vmin=3.8, vmax=7, rasterized=True)
                if i == 0:
                    ax.set_title(ion_list[indices[l]], fontsize=15)

                ax.set_xlabel('x/pc', fontsize=15)
                ax.set_ylabel('y/pc', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                ax.set_box_aspect(1)
            
            cax = fig.add_subplot(spec[l, len(time_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_title(r'$\log(T/\mathrm{K})$', fontsize=14)
            cax.tick_params(which='both', direction='in', labelsize=13)
        
        plt.subplots_adjust(hspace=0.01, wspace=0.01)
        plt.tight_layout()
        plt.savefig(savepath + 'ion_temp_maps_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()

def ion_maps_compare_conduction(run_list, time, redshift):
    direction = 0
    #time_list = [0, 1, 2, 3]
    #time_list = [1, 2]
    #HM_list = np.arange(3, 5)
    HM_list = [0]
    #linestyles = [':', '--', '-']
    #linestyles = [':', '-.', '--', '-']
    labels_run = [run['Name'] for run in run_list]
    #labels_direction = [r'$\cos \theta = %.1f$' % direction for direction in direction_list]
    #labels_times = ['t75', 't50', 't25']
    #labels_times = ['t90', 't50', 't25']
    #labels_times = ['t75', 't50', 't25']\
    xlist = []
    ylist = []

    for HM_value in HM_list:
        savepath = 'figures/HM_1e%d/' % (HM_value)
        os.makedirs(savepath, exist_ok=True)
        log_coldens = np.full((len(run_list), Npix ** 2, len(ion_list)), -10.)
        log_widths = np.full((len(run_list), Npix ** 2, len(ion_list)), -10.) #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
        log_temperatures = np.full((len(run_list), Npix ** 2, len(ion_list)), -10.)
        #thermal_fraction = []

        for i in range(len(run_list)):
            run = run_list[i]
            run_name = run['Name']
            pixel_size = 12 * run['radius'] / Npix #in pc
            xlist.append(np.arange(0, (Npix + 1) * pixel_size, pixel_size))
            ylist.append(np.arange(0, (Npix + 1) * pixel_size, pixel_size))

            coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            cloud_indices = coldens[:, 0].astype(int)
            log_coldens[i, cloud_indices] = np.log10(coldens[:, 1:]) + scaling_factor_metal
            log_coldens[i, :, 0] += scaling_factor_HI - scaling_factor_metal

            widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            log_widths[i, cloud_indices] = np.log10(widths[:, 1:] / 1e5)

            thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            #log_thermal_widths = np.log10(thermal_widths[:, 1:])
            log_temperatures[i, cloud_indices] = np.log10(6.0574e-9 * thermal_widths[:, 1:]**2 * ion_weight_list)

            for l in range(len(indices)):
                invalid_pixels = np.where(log_coldens[i, :, indices[l]] < 13)[0]
                null_pixels = np.where(log_coldens[i, :, indices[l]] < 11)[0]
                log_coldens[i, null_pixels, indices[l]] = np.nan
                log_widths[i, invalid_pixels, indices[l]] = np.nan
                log_temperatures[i, invalid_pixels, indices[l]] = np.nan
        

        fig = plt.figure(figsize=(16.3, 12), dpi=450)
        nrows = int(np.ceil(len(indices) / 2))
        ncols = 2 * len(run_list) + 3
        spec = fig.add_gridspec(nrows=nrows, ncols=ncols, width_ratios=([5, 1.5, 1.5, 1] + [0.8] + [5, 1.5, 1.5, 1]))
        for l in range(nrows):
            for k in range(2):
                for i in range(len(run_list)):
                    ax = fig.add_subplot(spec[l, k * (len(run_list) + 2) + i])
                    ion_index = l * 2 + k
                    if l == 0 and k == 0:
                        im = ax.pcolormesh(ylist[i], xlist[i], np.flip(log_coldens[i, :, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=21, rasterized=True)
                    else:
                        im = ax.pcolormesh(ylist[i], xlist[i], np.flip(log_coldens[i, :, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=17, rasterized=True)

                    #if i == 0:
                    if l == 0:
                        ax.text(0.5, 1.01, run_list[i]['conduction'], c='red', fontsize=14, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
                    if i == len(run_list) - 1:
                        ax.text(0.5, 0.01, ion_list[indices[ion_index]], fontsize=14, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
                        ax.tick_params(axis='y', labelleft=False, labelright=True)
                    ax.tick_params(which='both', direction='in', labelsize=14, right=True, top=True)
                    if i!= 0 and i != len(run_list) - 1:
                        ax.set_yticklabels([])
                    else:
                        ax.set_yticks([1000, 2000, 3000])
                        ax.set_yticklabels(['-1', '0', '1'])
                    ax.axis('scaled')
                    if 'cond' in run_list[i]['Name']:
                        ax.set_xlim(1400, 2600)
                        ax.set_xticks([1500, 2500])
                        ax.set_xticklabels(['-0.5', '0.5'])
                    else:
                        ax.set_xlim(0, 4000)
                        ax.set_xticks([1000, 2000, 3000])
                        ax.set_xticklabels(['-1', '0', '1'])
                    ax.set_ylim(0, 4000)
                    if l == nrows - 1:
                        ax.set_xlabel('x/kpc', fontsize=15)
                    else:
                        ax.set_xticklabels([])
                    if i == 0 and k == 0:
                        ax.set_ylabel('y/kpc', fontsize=15)
                    else:
                        ax.set_yticklabels([])
        
                cax = fig.add_subplot(spec[l, k * (len(run_list) + 2) + len(run_list)], box_aspect=15)
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
        plt.savefig(savepath + 'ion_colden_maps_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()
        '''
        fig = plt.figure(figsize=(8, 21), dpi=150)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(run_list) + 1, width_ratios=([5, 1.5, 1.5, 0.3]))
        for l in range(len(indices)):
            for i in range(len(run_list)):
                ax = fig.add_subplot(spec[l, i])
                im = ax.pcolormesh(ylist[i], xlist[i], log_widths[i, :, indices[l]].reshape((Npix, Npix)).transpose(), vmin=0.3, vmax=2.7, rasterized=True)
                #if i == 0:
                ax.set_title(ion_list[indices[l]], fontsize=15)
                ax.text(0.5, 0.9, run_list[i]['conduction'], c='red', fontsize=17, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

                ax.set_xlabel('x/pc', fontsize=17)
                ax.set_ylabel('y/pc', fontsize=17)
                ax.tick_params(which='both', direction='in', labelsize=17, right=True, top=True)
                ax.axis('scaled')
                if 'cond' in run_list[i]['Name']:
                    ax.set_xlim(1500, 2500)
                    ax.set_xticks([1500, 2500])
                else:
                    ax.set_xlim(0, 4000)
                ax.set_ylim(0, 4000)

            cax = fig.add_subplot(spec[l, len(run_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_title(r'$\log[b_{\mathrm{total}}/(\mathrm{km/s})]$', fontsize=15)
            cax.tick_params(which='both', direction='in', labelsize=15)
        
        plt.subplots_adjust(hspace=0.01, wspace=0.01)
        plt.tight_layout()
        plt.savefig(savepath + 'ion_width_maps_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(8, 21), dpi=450)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(run_list) + 1, width_ratios=([5, 1.5, 1.5, 0.3]))
        for l in range(len(indices)):
            for i in range(len(run_list)):
                ax = fig.add_subplot(spec[l, i])
                im = ax.pcolormesh(ylist[i], xlist[i], log_temperatures[i, :, indices[l]].reshape((Npix, Npix)).transpose(), vmin=3.8, vmax=7, rasterized=True)
                #if i == 0:
                ax.set_title(ion_list[indices[l]], fontsize=15)
                ax.text(0.5, 0.9, run_list[i]['conduction'], c='red', fontsize=17, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

                ax.set_xlabel('x/pc', fontsize=17)
                ax.set_ylabel('y/pc', fontsize=17)
                ax.tick_params(which='both', direction='in', labelsize=17, right=True, top=True)
                ax.axis('scaled')
                if 'cond' in run_list[i]['Name']:
                    ax.set_xlim(1500, 2500)
                    ax.set_xticks([1500, 2500])
                else:
                    ax.set_xlim(0, 4000)
                ax.set_ylim(0, 4000)
         
            cax = fig.add_subplot(spec[l, len(run_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_title(r'$\log(T/\mathrm{K})$', fontsize=15)
            cax.tick_params(which='both', direction='in', labelsize=15)
        
        plt.subplots_adjust(hspace=0.01, wspace=0.01)
        plt.tight_layout()
        plt.savefig(savepath + 'ion_temp_maps_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()
        '''    

def ion_maps_compare_runs(run_list, time, redshift):
    direction = 0
    #time_list = [0, 1, 2, 3]
    #time_list = [1, 2]
    #HM_list = np.arange(3, 5)
    HM_list = [0]
    #linestyles = [':', '--', '-']
    #linestyles = [':', '-.', '--', '-']
    labels_run = [run['Name'] for run in run_list]
    #labels_direction = [r'$\cos \theta = %.1f$' % direction for direction in direction_list]
    #labels_times = ['t75', 't50', 't25']
    #labels_times = ['t90', 't50', 't25']
    #labels_times = ['t75', 't50', 't25']\
    xlist = []
    ylist = []

    for HM_value in HM_list:
        savepath = 'figures/HM_1e%d/' % (HM_value)
        os.makedirs(savepath, exist_ok=True)
        log_coldens = np.full((len(run_list), Npix ** 2, len(ion_list)), -10.)
        log_widths = np.full((len(run_list), Npix ** 2, len(ion_list)), -10.) #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
        log_temperatures = np.full((len(run_list), Npix ** 2, len(ion_list)), -10.)
        #thermal_fraction = []

        for i in range(len(run_list)):
            run = run_list[i]
            run_name = run['Name']
            pixel_size = 12 * run['radius'] / Npix #in pc
            xlist.append(np.arange(0, (Npix + 1) * pixel_size, pixel_size))
            ylist.append(np.arange(0, (Npix + 1) * pixel_size, pixel_size))
            coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            cloud_indices = coldens[:, 0].astype(int)
            log_coldens[i, cloud_indices] = np.log10(coldens[:, 1:]) + scaling_factor_metal
            log_coldens[i, :, 0] += scaling_factor_HI - scaling_factor_metal

            widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            log_widths[i, cloud_indices] = np.log10(widths[:, 1:] / 1e5)

            thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            #log_thermal_widths = np.log10(thermal_widths[:, 1:])
            log_temperatures[i, cloud_indices] = np.log10(6.0574e-9 * thermal_widths[:, 1:]**2 * ion_weight_list)

            for l in range(len(indices)):
                invalid_pixels = np.where(log_coldens[i, :, indices[l]] < 13)[0]
                null_pixels = np.where(log_coldens[i, :, indices[l]] < 11)[0]
                log_coldens[i, null_pixels, indices[l]] = np.nan
                log_widths[i, invalid_pixels, indices[l]] = np.nan
                log_temperatures[i, invalid_pixels, indices[l]] = np.nan
        
        fig = plt.figure(figsize=(11, 12), dpi=450)
        nrows = int(np.ceil(len(indices) / 2))
        ncols = 2 * len(run_list) + 3
        spec = fig.add_gridspec(nrows=nrows, ncols=ncols, width_ratios=([1.5, 1.5, 1.5, 1] + [0.8] + [1.5, 1.5, 1.5, 1]))
        for l in range(nrows):
            for k in range(2):
                for i in range(len(run_list)):
                    ax = fig.add_subplot(spec[l, k * (len(run_list) + 2) + i])
                    ion_index = l * 2 + k
                    if l == 0 and k == 0:
                        im = ax.pcolormesh(ylist[i], xlist[i], np.flip(log_coldens[i, :, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=21, rasterized=True)
                    else:
                        im = ax.pcolormesh(ylist[i], xlist[i], np.flip(log_coldens[i, :, indices[ion_index]].reshape((Npix, Npix)).transpose(), axis=0), vmin=12, vmax=17, rasterized=True)

                    if l == 0:
                        ax.text(0.5, 1.01, 'v%d' % run_list[i]['velocity'], c='red', fontsize=14, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
                    #ax.text(0.5, 0.9, run_list[i]['conduction'], c='red', fontsize=14, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                    if i == len(run_list) - 1:
                        ax.text(0.5, 0.01, ion_list[indices[ion_index]], fontsize=14, horizontalalignment='center', verticalalignment='bottom', transform=ax.transAxes)
                        ax.tick_params(axis='y', labelleft=False, labelright=True)
                    ax.tick_params(which='both', direction='in', labelsize=14, right=True, top=True)
                    if i!= 0 and i != len(run_list) - 1:
                        ax.set_yticklabels([])
                    else:
                        ax.set_yticks([1000, 2000, 3000])
                        ax.set_yticklabels(['-1', '0', '1'])
                    ax.axis('scaled')
                    if 'cond' in run_list[i]['Name']:
                        ax.set_xlim(1400, 2600)
                        ax.set_xticks([1500, 2500])
                        ax.set_xticklabels(['-0.5', '0.5'])
                    else:
                        ax.set_xlim(0, 4000)
                        ax.set_xticks([1000, 2000, 3000])
                        ax.set_xticklabels(['-1', '0', '1'])
                    ax.set_ylim(0, 4000)
                    if l == nrows - 1:
                        ax.set_xlabel('x/kpc', fontsize=15)
                    else:
                        ax.set_xticklabels([])
                    if i == 0 and k == 0:
                        ax.set_ylabel('y/kpc', fontsize=15)
                    else:
                        ax.set_yticklabels([])
        
                cax = fig.add_subplot(spec[l, k * (len(run_list) + 2) + len(run_list)], box_aspect=15)
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
        plt.savefig(savepath + 'ion_colden_maps_runs_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()

        '''
        fig = plt.figure(figsize=(8, 21), dpi=150)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(run_list) + 1, width_ratios=([5, 1.5, 1.5, 0.3]))
        for l in range(len(indices)):
            for i in range(len(run_list)):
                ax = fig.add_subplot(spec[l, i])
                im = ax.pcolormesh(ylist[i], xlist[i], log_widths[i, :, indices[l]].reshape((Npix, Npix)).transpose(), vmin=0.3, vmax=2.7, rasterized=True)
                #if i == 0:
                ax.set_title(ion_list[indices[l]], fontsize=15)
                ax.text(0.5, 0.9, run_list[i]['conduction'], c='red', fontsize=17, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

                ax.set_xlabel('x/pc', fontsize=17)
                ax.set_ylabel('y/pc', fontsize=17)
                ax.tick_params(which='both', direction='in', labelsize=17, right=True, top=True)
                ax.axis('scaled')
                if 'cond' in run_list[i]['Name']:
                    ax.set_xlim(1500, 2500)
                    ax.set_xticks([1500, 2500])
                else:
                    ax.set_xlim(0, 4000)
                ax.set_ylim(0, 4000)

            cax = fig.add_subplot(spec[l, len(run_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_title(r'$\log[b_{\mathrm{total}}/(\mathrm{km/s})]$', fontsize=15)
            cax.tick_params(which='both', direction='in', labelsize=15)
        
        plt.subplots_adjust(hspace=0.01, wspace=0.01)
        plt.tight_layout()
        plt.savefig(savepath + 'ion_width_maps_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()

        fig = plt.figure(figsize=(8, 21), dpi=450)
        spec = fig.add_gridspec(nrows=len(indices), ncols=len(run_list) + 1, width_ratios=([5, 1.5, 1.5, 0.3]))
        for l in range(len(indices)):
            for i in range(len(run_list)):
                ax = fig.add_subplot(spec[l, i])
                im = ax.pcolormesh(ylist[i], xlist[i], log_temperatures[i, :, indices[l]].reshape((Npix, Npix)).transpose(), vmin=3.8, vmax=7, rasterized=True)
                #if i == 0:
                ax.set_title(ion_list[indices[l]], fontsize=15)
                ax.text(0.5, 0.9, run_list[i]['conduction'], c='red', fontsize=17, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

                ax.set_xlabel('x/pc', fontsize=17)
                ax.set_ylabel('y/pc', fontsize=17)
                ax.tick_params(which='both', direction='in', labelsize=17, right=True, top=True)
                ax.axis('scaled')
                if 'cond' in run_list[i]['Name']:
                    ax.set_xlim(1500, 2500)
                    ax.set_xticks([1500, 2500])
                else:
                    ax.set_xlim(0, 4000)
                ax.set_ylim(0, 4000)
         
            cax = fig.add_subplot(spec[l, len(run_list)], box_aspect=15)
            plt.colorbar(im, cax=cax)
            cax.set_title(r'$\log(T/\mathrm{K})$', fontsize=15)
            cax.tick_params(which='both', direction='in', labelsize=15)
        
        plt.subplots_adjust(hspace=0.01, wspace=0.01)
        plt.tight_layout()
        plt.savefig(savepath + 'ion_temp_maps_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
        #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
        plt.close()
        '''

def compare_redshift(redshift_list, HM_list):
    linestyles = ['-',  '--', '-.', ':']
    savepath = 'figures/'
    direction_list = [0.5]
    time_list = [2]
    labels_run = [run['Name'] for run in run_list]
    labels_direction = [r'$\theta = %d ^{\circ}$' % np.rad2deg(np.arccos(direction)) for direction in direction_list]
    labels_redshift = [r'$z=%g,\log(n/n_{\mathrm{ref}})=%d$' % (redshift_list[i], HM_list[i]) for i in range(len(redshift_list))]
    #labels_times = ['t90', 't75', 't50', 't25']
    labels_times = ['t90', 't50', 't25']

    for direction in direction_list:
        for time in time_list:
            log_coldens = []
            log_widths = [] #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
            log_temperatures = []
            thermal_fraction = []
            for run in run_list:
                run_name = run['Name']
                log_coldens.append([])
                log_widths.append([])
                log_temperatures.append([])
                thermal_fraction.append([])

                for i in range(len(redshift_list)):
                    HM_value = HM_list[i]
                    redshift = redshift_list[i]
                    local_scaling_factor_metal = -2/3 * HM_value
                    local_scaling_factor_HI = -2/3 * HM_value

                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1].append(np.log10(coldens[:, 1:]) + local_scaling_factor_metal)
                    log_coldens[-1][-1][:, 0] += local_scaling_factor_HI - local_scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1].append(widths[:, 1:] / 1e5)
                    
                    ion_temp = (6.0574e-9 * widths[:, 1:]**2 * ion_weight_list)
                    log_temperatures[-1].append(np.log10(ion_temp))

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])


            plt.figure(figsize=(18, 20))
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 1)
                for i in range(len(run_list)):
                    for k in range(len(redshift_list)):
                        local_scaling_factor_metal = -2/3 * HM_list[k]
                        weights = 4 / (10 ** local_scaling_factor_metal) * np.ones_like(log_coldens[i][k][:, indices[l]])
                        if l == 0:
                            ax.hist(log_coldens[i][k][:, indices[l]], bins=75, range=(11, 20), histtype='step', color=colors[i], ls=linestyles[k], weights=weights, label=labels_run[i] if k == 0 else None)
                        else:
                            ax.hist(log_coldens[i][k][:, indices[l]], bins=75, range=(11, 16.5), histtype='step', color=colors[i], ls=linestyles[k], weights=weights)

                    ax.set_title(ion_list[indices[l]], fontsize=15)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                    ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$')
                    ax.tick_params(axis='x', labelsize=15)
            
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 2)
                for i in range(len(run_list)):
                    for k in range(len(redshift_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        local_scaling_factor_metal = -2/3 * HM_list[k]
                        weights = 4 / (10 ** local_scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(log_widths[i][k][valid_pixels, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], ls=linestyles[k], label=labels_redshift[k] if i == 0 else None, weights=weights)
                if l == 0:
                    ax.legend(fontsize=13)
                ax.set_yscale('log')
                ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
                ax.tick_params(axis='x', labelsize=15)
            
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 3)
                for i in range(len(run_list)):
                    for k in range(len(redshift_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        local_scaling_factor_metal = -2/3 * HM_list[k]
                        weights = 4 / (10 ** local_scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(log_temperatures[i][k][valid_pixels, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[k], weights=weights)

                ax.set_yscale('log')
                ax.set_xlabel(r'$\log(T/\mathrm{K})$', fontsize=15)
                ax.tick_params(axis='x', labelsize=15)
            
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 4)
                for i in range(len(run_list)):
                    for k in range(len(redshift_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        local_scaling_factor_metal = -2/3 * HM_list[k]
                        weights = 4 / (10 ** local_scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(thermal_fraction[i][k][valid_pixels, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[k], weights=weights)
                ax.set_yscale('log')
                ax.set_xlabel(r'$b_{\mathrm{thermal}}/b_{\mathrm{total}}$', fontsize=15)
                ax.tick_params(axis='x', labelsize=15)
            plt.tight_layout()
            plt.savefig(savepath + 'redshift_comparisons_%s_%d_t%d.pdf' % (run_list[0]['Name'], 10 * direction, time), bbox_inches='tight')
            plt.close()

def histograms(redshift):
    direction_list = [0, 0.5, 1.0]
    #time_list = [2]
    time_list = [0, 1, 2, 3]
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    #linestyles = [':', '--', '-']
    linestyles = [':', '-.', '--', '-']
    #linestyles = ['-']
    labels_run = [run['Name'] for run in run_list]
    labels_direction = [r'$\cos \theta = %.1f$' % direction for direction in direction_list]
    labels_times = ['t90', 't75', 't50', 't25']
    #labels_times = ['t75', 't50', 't25']
    #labels_times = ['t90', 't50', 't25']
    #labels_times = ['t75', 't50', 't25']

    for HM_value in HM_list:
        savepath = 'figures/HM_1e%d/' % (HM_value)
        os.makedirs(savepath, exist_ok=True)
        log_coldens = []
        log_widths = [] #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
        log_temperatures = []
        thermal_fraction = []
        for run in run_list:
            run_name = run['Name']

            log_coldens.append([])
            log_widths.append([])
            log_temperatures.append([])
            thermal_fraction.append([])

            for time in time_list:
                log_coldens[-1].append([])
                log_widths[-1].append([])
                log_temperatures[-1].append([])
                thermal_fraction[-1].append([])

                for direction in direction_list:
                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1][-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                    log_coldens[-1][-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1][-1].append(widths[:, 1:] / 1e5)
                    
                    ion_temp = (6.0574e-9 * widths[:, 1:]**2 * ion_weight_list)
                    log_temperatures[-1][-1].append(np.log10(ion_temp))

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1][-1].append(thermal_widths[:, 1:] / widths[:, 1:])
        
        for k in range(len(direction_list)):
            plt.figure(figsize=(18, 20))
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 1)
                for i in range(len(run_list)):
                    #for j in range(2 * (i % 2), len(time_list)):
                    for j in range(len(time_list)):
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][j][k][:, indices[l]])
                        if l == 0:
                            ax.hist(log_coldens[i][j][k][:, indices[l]], bins=75, range=(12, 20), histtype='step', color=colors[i], ls=linestyles[j], label=labels_times[j] if i == 0 else None, weights=weights)
                            #ax.hist(log_coldens[i][j][k][:, indices[l]], bins=75, range=(12, 20), histtype='step', color=colors[i], ls=linestyles[j], weights=weights)
                        else:
                            ax.hist(log_coldens[i][j][k][:, indices[l]], bins=75, range=(11, 16.5), histtype='step', color=colors[i], ls=linestyles[j], weights=weights)

                ax.set_title(ion_list[indices[l]], fontsize=15)
                if l == 0:
                    ax.legend(fontsize=15)
                ax.set_yscale('log')
                ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 2)
                for i in range(len(run_list)):
                    #for j in range(2 * (i % 2), len(time_list)):
                    for j in range(len(time_list)):
                        valid_pixels = np.where(log_coldens[i][j][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][j][k][valid_pixels, indices[l]])
                        ax.hist(log_widths[i][j][k][valid_pixels, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], ls=linestyles[j], label=labels_run[i] if j == len(time_list) - 1 and l == 0 else None, weights=weights)
                if l == 0:
                    ax.legend(fontsize=13)
                ax.set_yscale('log')
                ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 3)
                for i in range(len(run_list)):
                    #for j in range(2 * (i % 2), len(time_list)):
                    for j in range(len(time_list)):
                        valid_pixels = np.where(log_coldens[i][j][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][j][k][valid_pixels, indices[l]])
                        ax.hist(log_temperatures[i][j][k][valid_pixels, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[j], weights=weights)
                ax.set_yscale('log')
                ax.set_xlabel(r'$\log(T_{\mathrm{eff}}/\mathrm{K})$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 4)
                for i in range(len(run_list)):
                    #for j in range(2 * (i % 2), len(time_list)):
                    for j in range(len(time_list)):
                        valid_pixels = np.where(log_coldens[i][j][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][j][k][valid_pixels, indices[l]])
                        ax.hist(thermal_fraction[i][j][k][valid_pixels, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[j], weights=weights)
                ax.set_yscale('log')
                ax.set_xlabel(r'$b_{\mathrm{thermal}}/b_{\mathrm{total}}$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            plt.tight_layout()
            plt.savefig(savepath + 'histograms_%s_%d_z%g.pdf' % (run_list[0]['Name'], 10 * direction_list[k], redshift), bbox_inches='tight')
            #plt.savefig(savepath + 'histograms_t%d_%d_z%g.pdf' % (time_list[0], 10 * direction_list[k], redshift), bbox_inches='tight')
            #plt.savefig(savepath + 'histograms_%d.pdf' % (10 * direction_list[k]), bbox_inches='tight')
            #plt.savefig(savepath + 'histograms_%d.png' % (10 * direction_list[k]), dpi=400, bbox_inches='tight')
            plt.close()

def phase_space(redshift):
    direction_list = np.arange(0, 1.1, 0.1)
    time_list = [1, 2, 3]
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    linestyles = [':', '--', '-']
    labels_run = [run['Name'] for run in run_list]
    labels_direction = [r'$\cos \theta = %.1f$' % direction for direction in direction_list]
    #labels_times = ['t90', 't75', 't50', 't25']
    labels_times = ['t75', 't50', 't25']

    for HM_value in HM_list:
        log_coldens = []
        log_widths = [] #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
        log_temperatures = []
        thermal_fraction = []
        savepath = 'figures/HM_1e%d/' % HM_value
        for run in run_list:
            run_name = run['Name']

            log_coldens.append([])
            log_widths.append([])
            log_temperatures.append([])
            thermal_fraction.append([])

            for time in time_list:
                log_coldens[-1].append([])
                log_widths[-1].append([])
                log_temperatures[-1].append([])
                thermal_fraction[-1].append([])

                for direction in direction_list:
                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1][-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                    log_coldens[-1][-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1][-1].append(np.log10(widths[:, 1:] / 1e5))
                    
                    ion_temp = (6.0574e-9 * widths[:, 1:]**2 * ion_weight_list)
                    log_temperatures[-1][-1].append(np.log10(ion_temp))

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1][-1].append(thermal_widths[:, 1:] / widths[:, 1:])
        
        for i in range(len(run_list)):

            log_coldens_concatenated = []
            log_width_concatenated = []
            thermal_fraction_concatenated = []
            for j in range(len(time_list)):#change to loop over direction when comparing directions
                log_coldens_concatenated.append(np.concatenate(log_coldens[i][j], axis=0))
                log_width_concatenated.append(np.concatenate(log_widths[i][j], axis=0))
                thermal_fraction_concatenated.append(np.concatenate(thermal_fraction[i][j], axis=0))
            
            os.makedirs(savepath, exist_ok=True)
            plt.figure(figsize=(13, 20), dpi=300)
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 3, 3 * l + 1)
                for j in range(len(time_list)):
                    ax.scatter(log_coldens_concatenated[j][:, indices[l]], log_width_concatenated[j][:, indices[l]], s=1.2, alpha=0.7, c=colors[2 * j], label=labels_times[j] if l == 0 else None, rasterized=True)
                ax.set_title(ion_list[indices[l]], fontsize=15)
                if l == 0:
                    ax.legend(fontsize=15)
                    ax.set_xlim(12, 20)
                else:
                    ax.set_xlim(12, 16.5)
                ax.set_ylim(0.3, 2.7)
                ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                ax.set_ylabel(r'$\log[b_{\mathrm{tot}}/(\mathrm{km/s})]$', fontsize=15)
                ax.tick_params(axis='both', labelsize=15)
        
                ax = plt.subplot(len(indices), 3, 3 * l + 2)
                for j in range(len(time_list)):
                    ax.scatter(log_coldens_concatenated[j][:, indices[l]], log_width_concatenated[j][:, indices[l]] * thermal_fraction_concatenated[j][:, indices[l]], s=1.2, alpha=0.7, c=colors[2 * j], rasterized=True)
                if l == 0:
                    ax.set_xlim(12, 20)
                else:
                    ax.set_xlim(12, 16.5)
                ax.set_ylim(0.3, 2.7)
                ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                ax.set_ylabel(r'$\log[b_{\mathrm{thermal}}/(\mathrm{km/s})]$', fontsize=15)
                ax.tick_params(axis='both', labelsize=15)
            
                ax = plt.subplot(len(indices), 3, 3 * l + 3)
                for j in range(len(time_list)):
                    ax.scatter(log_coldens_concatenated[j][:, indices[l]], log_width_concatenated[j][:, indices[l]] * np.sqrt(1 - thermal_fraction_concatenated[j][:, indices[l]] ** 2), s=1.2, alpha=0.7, c=colors[2 * j], rasterized=True)
                if l == 0:
                    ax.set_xlim(12, 20)
                else:
                    ax.set_xlim(12, 16.5)
                ax.set_ylim(0.3, 2.7)
                ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                ax.set_ylabel(r'$\log[b_{\mathrm{kin}}/(\mathrm{km/s})]$', fontsize=15)
                ax.tick_params(axis='both', labelsize=15)

            plt.tight_layout()
            plt.savefig(savepath + 'pd_%s_z%g.pdf' % (run_list[i]['Name'], redshift), bbox_inches='tight')
            plt.close()


def compare_scaling_factors(redshift): #comparing clouds with the same mass but different density, and hence different ionization parameter
    direction_list = [0, 1.0]
    time_list = np.arange(4)
    HM_list = np.arange(0, 6)
    linestyles = [':', '--', '-']
    labels_run = [run['Name'] for run in run_list]
    labels_direction = [r'$\theta = %d ^{\circ}$' % np.rad2deg(np.arccos(direction)) for direction in direction_list]
    labels_HM = [r'$\log(n/n_{\mathrm{ref}})=%d$' % (-HM_value) for HM_value in HM_list]
    #labels_times = ['t90', 't75', 't50', 't25']
    labels_times = ['t90', 't50', 't25']

    for time in time_list:
        for run in run_list:
            run_name = run['Name']
            savepath = 'figures/%s/' % (run_name)
            os.makedirs(savepath, exist_ok=True)

            log_coldens = []
            log_widths = [] #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
            log_temperatures = []
            thermal_fraction = []

            for HM_value in HM_list:
                log_coldens.append([])
                log_widths.append([])
                log_temperatures.append([])
                thermal_fraction.append([])
                for direction in direction_list:
                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal - 2/3 * HM_value)
                    log_coldens[-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1].append(widths[:, 1:] / 1e5)
                    
                    ion_temp = (6.0574e-9 * widths[:, 1:]**2 * ion_weight_list)
                    log_temperatures[-1].append(np.log10(ion_temp))

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])

            for k in range(len(direction_list)):
                plt.figure(figsize=(18, 20))
                for l in range(len(indices)):
                    ax = plt.subplot(len(indices), 4, 4 * l + 1)
                    for i in range(len(HM_list)):
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][:, indices[l]])
                        if l == 0:
                            ax.hist(log_coldens[i][k][:, indices[l]], bins=75, range=(12, 20), histtype='step', color=colors[i], weights=weights)
                        else:
                            ax.hist(log_coldens[i][k][:, indices[l]], bins=75, range=(12, 16.5), histtype='step', color=colors[i], weights=weights)

                    ax.set_title(ion_list[indices[l]], fontsize=15)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                    ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$')
                    ax.tick_params(axis='x', labelsize=15)
                
                for l in range(len(indices)):
                    ax = plt.subplot(len(indices), 4, 4 * l + 2)
                    for i in range(len(HM_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(log_widths[i][k][valid_pixels, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], label=labels_HM[i], weights=weights)
                    if l == 0:
                        ax.legend(fontsize=13)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
                    ax.tick_params(axis='x', labelsize=15)
                
                for l in range(len(indices)):
                    ax = plt.subplot(len(indices), 4, 4 * l + 3)
                    for i in range(len(HM_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(log_temperatures[i][k][valid_pixels, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[k + 1], weights=weights)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$\log(T/\mathrm{K})$', fontsize=15)
                    ax.tick_params(axis='x', labelsize=15)
                
                for l in range(len(indices)):
                    ax = plt.subplot(len(indices), 4, 4 * l + 4)
                    for i in range(len(HM_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(thermal_fraction[i][k][valid_pixels, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[k + 1], weights=weights)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$b_{\mathrm{thermal}}/b_{\mathrm{total}}$', fontsize=15)
                    ax.tick_params(axis='x', labelsize=15)
                plt.tight_layout()
                plt.savefig(savepath + 'scaling_factor_comparisons_%d_t%d.pdf' % (10 * direction_list[k], time), bbox_inches='tight')
                plt.close()

def compare_density_cuts(redshift):
    direction_list = [0, 1.0]
    time_list = [0, 2]
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    linestyles = [':', '--', '-']
    labels_run = [run['Name'] for run in run_list]
    labels_direction = [r'$\theta = %d ^{\circ}$' % np.rad2deg(np.arccos(direction)) for direction in direction_list]
    #labels_times = ['t90', 't75', 't50', 't25']
    labels_times = ['t90', 't50', 't25']
    labels_cuts = ['11<logN<12', '12<logN<13', 'logN>13']

    for time in time_list:
        for HM_value in HM_list:
            savepath = 'figures/HM_1e%d/' % (HM_value)
            os.makedirs(savepath, exist_ok=True)
            log_coldens = []
            log_widths = [] #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
            log_temperatures = []
            thermal_fraction = []
            for run in run_list:
                run_name = run['Name']

                log_coldens.append([])
                log_widths.append([])
                log_temperatures.append([])
                thermal_fraction.append([])
                for direction in direction_list:
                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                    log_coldens[-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1].append(widths[:, 1:] / 1e5)
                    
                    ion_temp = (6.0574e-9 * widths[:, 1:]**2 * ion_weight_list)
                    log_temperatures[-1].append(np.log10(ion_temp))

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])

            for k in range(len(direction_list)):
                plt.figure(figsize=(13, 20))
                for l in range(len(indices)):                
                    ax = plt.subplot(len(indices), 3, 3 * l + 1)
                    for i in range(len(run_list)):
                        valid_pixels_1 = np.where((log_coldens[i][k][:, indices[l]] > 11) & (log_coldens[i][k][:, indices[l]] < 12))[0]
                        valid_pixels_2 = np.where((log_coldens[i][k][:, indices[l]] > 12) & (log_coldens[i][k][:, indices[l]] < 13))[0]
                        valid_pixels_3 = np.where(log_coldens[i][k][:, indices[l]] > 13)[0]

                        #weights_1 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_1, indices[l]])
                        #weights_2 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_2, indices[l]])
                        #weights_3 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_3, indices[l]])

                        ax.hist(log_widths[i][k][valid_pixels_1, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], ls=linestyles[0], label=labels_run[i] if l == 0 else None, density=True)
                        ax.hist(log_widths[i][k][valid_pixels_2, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], ls=linestyles[1], density=True)
                        ax.hist(log_widths[i][k][valid_pixels_3, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], ls=linestyles[2], density=True)
                    if l == 0:
                        ax.legend(fontsize=13)
                    ax.set_title(ion_list[indices[l]], fontsize=15)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
                    ax.tick_params(axis='x', labelsize=15)
                
                    ax = plt.subplot(len(indices), 3, 3 * l + 2)
                    for i in range(len(run_list)):
                        valid_pixels_1 = np.where((log_coldens[i][k][:, indices[l]] > 11) & (log_coldens[i][k][:, indices[l]] < 12))[0]
                        valid_pixels_2 = np.where((log_coldens[i][k][:, indices[l]] > 12) & (log_coldens[i][k][:, indices[l]] < 13))[0]
                        valid_pixels_3 = np.where(log_coldens[i][k][:, indices[l]] > 13)[0]

                        #weights_1 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_1, indices[l]])
                        #weights_2 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_2, indices[l]])
                        #weights_3 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_3, indices[l]])

                        ax.hist(log_temperatures[i][k][valid_pixels_1, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[0], label=labels_cuts[0] if l == 0 and i == 0 else None, density=True)
                        ax.hist(log_temperatures[i][k][valid_pixels_2, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[1], label=labels_cuts[1] if l == 0 and i == 0 else None, density=True)
                        ax.hist(log_temperatures[i][k][valid_pixels_3, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[2], label=labels_cuts[2] if l == 0 and i == 0 else None, density=True)
                    if l == 0:
                        ax.legend(fontsize=13)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$\log(T/\mathrm{K})$', fontsize=15)
                    ax.tick_params(axis='x', labelsize=15)
                
                    ax = plt.subplot(len(indices), 3, 3 * l + 3)
                    for i in range(len(run_list)):
                        valid_pixels_1 = np.where((log_coldens[i][k][:, indices[l]] > 11) & (log_coldens[i][k][:, indices[l]] < 12))[0]
                        valid_pixels_2 = np.where((log_coldens[i][k][:, indices[l]] > 12) & (log_coldens[i][k][:, indices[l]] < 13))[0]
                        valid_pixels_3 = np.where(log_coldens[i][k][:, indices[l]] > 13)[0]

                        #weights_1 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_1, indices[l]])
                        #weights_2 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_2, indices[l]])
                        #weights_3 = 4 * np.ones_like(log_coldens[i][k][valid_pixels_3, indices[l]])

                        ax.hist(thermal_fraction[i][k][valid_pixels_1, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[0], density=True)
                        ax.hist(thermal_fraction[i][k][valid_pixels_2, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[1], density=True)
                        ax.hist(thermal_fraction[i][k][valid_pixels_3, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[2], density=True)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$b_{\mathrm{thermal}}/b_{\mathrm{total}}$', fontsize=15)
                    ax.tick_params(axis='x', labelsize=15)
                plt.tight_layout()
                plt.savefig(savepath + 'density_cut_comparison_%d_t%d.pdf' % (10 * direction_list[k], time), bbox_inches='tight')
                plt.close()
    
def compare_directions(redshift):
    direction_list = [0, 0.5, 1.0]
    time_list = [0, 1, 2, 3]
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    linestyles = [':', '--', '-']
    labels_run = [run['Name'] for run in run_list]
    labels_direction = [r'$\theta = %d ^{\circ}$' % np.rad2deg(np.arccos(direction)) for direction in direction_list]
    #labels_times = ['t90', 't75', 't50', 't25']
    labels_times = ['t90', 't75', 't50', 't25']

    for time in time_list:
        for HM_value in HM_list:
            savepath = 'figures/HM_1e%d/' % (HM_value)
            os.makedirs(savepath, exist_ok=True)
            log_coldens = []
            log_widths = [] #Well, I'm going to retain the name for convenience, but this is really the line widths themselves, not the logs.
            log_temperatures = []
            thermal_fraction = []
            for run in run_list:
                run_name = run['Name']

                log_coldens.append([])
                log_widths.append([])
                log_temperatures.append([])
                thermal_fraction.append([])
                for direction in direction_list:
                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                    log_coldens[-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1].append(widths[:, 1:] / 1e5)
                    
                    ion_temp = (6.0574e-9 * widths[:, 1:]**2 * ion_weight_list)
                    log_temperatures[-1].append(np.log10(ion_temp))

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])

            plt.figure(figsize=(18, 20))
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 1)
                for k in range(len(direction_list)):
                    for i in range(len(run_list)):
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][:, indices[l]])
                        if l == 0:
                            ax.hist(log_coldens[i][k][:, indices[l]], bins=75, range=(12, 20), histtype='step', color=colors[i], ls=linestyles[k], label=labels_direction[k] if i == 0 else None, weights=weights)
                        else:
                            ax.hist(log_coldens[i][k][:, indices[l]], bins=75, range=(12, 16.5), histtype='step', color=colors[i], ls=linestyles[k], weights=weights)

                ax.set_title(ion_list[indices[l]], fontsize=15)
                if l == 0:
                    ax.legend(fontsize=15)
                ax.set_yscale('log')
                ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=15)
                ax.set_ylabel(r'$\mathrm{d}A/\mathrm{d}\log N\ /\mathrm{pc^2}$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 2)
                for k in range(len(direction_list)):
                    for i in range(len(run_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(log_widths[i][k][valid_pixels, indices[l]], bins=75, range=(0, 250), histtype='step', color=colors[i], ls=linestyles[k], label=labels_run[i] if k == len(direction_list) - 1 and l == 0 else None, weights=weights)
                if l == 0:
                    ax.legend(fontsize=13)
                ax.set_yscale('log')
                ax.set_xlabel(r'$b/\mathrm{km/s}$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 3)
                for k in range(len(direction_list)):
                    for i in range(len(run_list)):
                        valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                        weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                        ax.hist(log_temperatures[i][k][valid_pixels, indices[l]], bins=75, range=(3.8, 8), histtype='step', color=colors[i], ls=linestyles[k], weights=weights)
                ax.set_yscale('log')
                ax.set_xlabel(r'$\log(T/\mathrm{K})$', fontsize=15)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                
            for l in range(len(indices)):
                ax = plt.subplot(len(indices), 4, 4 * l + 4)
                for k in range(len(direction_list)):
                    for i in range(len(run_list)):
                            valid_pixels = np.where(log_coldens[i][k][:, indices[l]] > 12)[0]
                            weights = 4 / (10 ** scaling_factor_metal) * np.ones_like(log_coldens[i][k][valid_pixels, indices[l]])
                            ax.hist(thermal_fraction[i][k][valid_pixels, indices[l]], bins=75, range=(0, 1), histtype='step', color=colors[i], ls=linestyles[k], weights=weights)
                    ax.set_yscale('log')
                    ax.set_xlabel(r'$b_{\mathrm{thermal}}/b_{\mathrm{total}}$', fontsize=15)
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
            plt.tight_layout()
            plt.savefig(savepath + 'direction_comparisons_t%d_z%g.pdf' % (time, redshift), bbox_inches='tight')
            plt.close()

def separate_plot(run, redshift):
    run_name = run['Name']
    direction_list = np.arange(0, 1.1, 0.1)
    time_list = np.arange(4)
    #HM_list = np.arange(3, 5)
    HM_list = [2]

    for HM_value in HM_list:
        for time in time_list:
            savepath = 'figures/%s/HM_1e%d/t%d/' % (run_name, HM_value, time)
            os.makedirs(savepath, exist_ok=True)
            for direction in direction_list:
                coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_coldens = np.log10(coldens[:, 1:])

                widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_widths = np.log10(widths[:, 1:])

                thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_thermal_widths = np.log10(thermal_widths[:, 1:])

                thermal_fraction = thermal_widths[:, 1:] / widths[:, 1:]

                #kinematic_widths = np.loadtxt(blob_kinematic_width_file % (run_name, HM_value, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_kinematic_widths = np.log10(kinematic_widths[:, 1:])

                
                plt.figure(figsize=(20, 21), dpi=300)
                for i in range(len(indices)):
                    width_norm = matplotlib.colors.Normalize(5.3, 7.7)
                    for j in range(len(indices)):
                        if j != i:
                            ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                            ax.scatter(log_coldens[:, indices[j]], log_coldens[:, indices[i]], s=1.2, alpha=0.7, c=log_widths[:, indices[j]], cmap=cmap, norm=width_norm, rasterized=True)
                            if j == 0:
                                ax.set_xlim(12, 19)
                            else:
                                ax.set_xlim(12, 16.5)
                            if i == 0:
                                ax.set_ylim(12, 19)
                            else:
                                ax.set_ylim(12, 16.5)
                        else:
                            ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + i + 1)
                            if i == 0:
                                ax.hist(log_coldens[:, indices[i]], bins=100, range=(12, 19), facecolor="None", edgecolor='blue', linewidth=0.2)
                            else:
                                ax.hist(log_coldens[:, indices[i]], bins=100, range=(12, 16.5), facecolor="None", edgecolor='blue', linewidth=0.2)
                            #ax.tick_params(axis='both', labelsize=14)
                        
                        if (j != 0 and i != 0) or (j > 1 and i == 0):
                            ax.axes.yaxis.set_ticklabels([])
                        else:
                            ax.tick_params(axis='y', labelsize=14)
                            if j != 1 or i != 0:
                                ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                        if i != len(indices) - 1:
                            ax.tick_params(axis='x', labelsize=14)
                            ax.axes.xaxis.set_ticklabels([])
                        else:
                            ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                        ax.set_box_aspect(1)

                cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
                sm = matplotlib.cm.ScalarMappable(norm=width_norm, cmap=cmap)
                cax.set_title('b/(cm/s)')
                plt.colorbar(sm, cax=cax, orientation='horizontal')

                plt.subplots_adjust(hspace=0.05, wspace=0.05)
                plt.tight_layout()
                plt.savefig(savepath + 'colden_dist_%d.png' % (10 * direction), dpi=500, bbox_inches='tight')
                plt.savefig(savepath + 'colden_dist_%d.pdf' % (10 * direction), bbox_inches='tight')
                plt.clf()
                plt.close()

                plt.figure(figsize=(20, 18), dpi=300)
                for i in range(len(indices)):
                    colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
                    colden_norm_H = matplotlib.colors.Normalize(12, 19)
                    for j in range(len(indices)):
                        if j != i:
                            ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                            if j == 0:
                                ax.scatter(log_widths[:, indices[j]], log_widths[:, indices[i]], s=1.2, alpha=0.7, c=log_coldens[:, indices[j]], cmap=cmap, norm=colden_norm_H, rasterized=True)
                            else:
                                ax.scatter(log_widths[:, indices[j]], log_widths[:, indices[i]], s=1.2, alpha=0.7, c=log_coldens[:, indices[j]], cmap=cmap, norm=colden_norm_metal, rasterized=True)
                            ax.set_xlim(5.3, 7.7)
                            ax.set_ylim(5.3, 7.7)

                        else:
                            ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + i + 1)
                            ax.hist(log_widths[:, indices[i]], bins=100, range=(5.3, 7.7), facecolor="None", edgecolor='blue', linewidth=0.2)
                            #ax.tick_params(axis='both', labelsize=12)

                        if (j != 0 and i != 0) or (j > 1 and i == 0):
                            ax.axes.yaxis.set_ticklabels([])
                        else:
                            ax.tick_params(axis='y', labelsize=14)
                            if j != 1 or i != 0:
                                ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                        if i != len(indices) - 1:
                            ax.tick_params(axis='x', labelsize=14)
                            ax.axes.xaxis.set_ticklabels([])
                        else:
                            ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                        ax.set_box_aspect(1)
                cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
                sm = matplotlib.cm.ScalarMappable(norm=colden_norm_H, cmap=cmap)
                cax.set_title(r'$N_{\mathrm{H}}/(\mathrm{cm^{-2}})$')
                plt.colorbar(sm, cax=cax, orientation='horizontal')

                cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 2, box_aspect=0.06)
                sm = matplotlib.cm.ScalarMappable(norm=colden_norm_metal, cmap=cmap)
                cax.set_title(r'$N_{\mathrm{metal}}/(\mathrm{cm^{-2}})$')
                plt.colorbar(sm, cax=cax, orientation='horizontal')

                plt.subplots_adjust(hspace=0.05, wspace=0.05)
                plt.tight_layout()
                plt.savefig(savepath + 'width_dist_%d.png' % (10 * direction), dpi=500, bbox_inches='tight')
                plt.savefig(savepath + 'width_dist_%d.pdf' % (10 * direction), bbox_inches='tight')
                plt.clf()
                plt.close()


                plt.figure(figsize=(20, 18), dpi=300)
                for i in range(len(indices)):
                    thermal_fraction_norm = matplotlib.colors.Normalize(0, 1)
                    for j in range(len(indices)):
                        if j != i:
                            ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                            ax.scatter(log_coldens[:, indices[j]], log_coldens[:, indices[i]], s=1.2, alpha=0.7, c=thermal_fraction[:, indices[j]], cmap=cmap, norm=thermal_fraction_norm, rasterized=True)
                            if j == 0:
                                ax.set_xlim(12, 19)
                            else:
                                ax.set_xlim(12, 16.5)
                            if i == 0:
                                ax.set_ylim(12, 19)
                            else:
                                ax.set_ylim(12, 16.5)
                                
                        else:
                            ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + i + 1)
                            ax.hist(thermal_fraction[:, indices[i]], bins=100, range=(0, 1), facecolor="None", edgecolor='blue', linewidth=0.2)
                            #ax.tick_params(axis='both', labelsize=12)
                        
                        if (j != 0 and i != 0) or (j > 1 and i == 0):
                            ax.axes.yaxis.set_ticklabels([])
                        else:
                            ax.tick_params(axis='y', labelsize=14)
                            if j != 1 or i != 0:
                                ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                        if i != len(indices) - 1:
                            ax.tick_params(axis='x', labelsize=14)
                            ax.axes.xaxis.set_ticklabels([])
                        else:
                            ax.set_xlabel(ion_list[indices[j]], fontsize=16)
                        
                        ax.set_box_aspect(1)
                            
                cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
                sm = matplotlib.cm.ScalarMappable(norm=thermal_fraction_norm, cmap=cmap)
                cax.set_title('b_thermal/b_total')
                plt.colorbar(sm, cax=cax, orientation='horizontal')

                plt.subplots_adjust(hspace=0.05, wspace=0.05)
                plt.tight_layout()
                plt.savefig(savepath + 'thermal_fraction_%d.png' % (10 * direction), dpi=500, bbox_inches='tight')
                plt.savefig(savepath + 'thermal_fraction_%d.pdf' % (10 * direction), bbox_inches='tight')
                plt.clf()
                plt.close()


def combined_plot_time(run, redshift):
    run_name = run['Name']
    #direction_list = np.arange(0, 1.1, 0.1)
    direction_list = [0, 1.0]
    time_list = np.arange(4)
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    labels = ['t90', 't80', 't50', 't25']

    for HM_value in HM_list:
        savepath = 'figures/%s/HM_1e%d/' % (run_name, HM_value)

        log_coldens = []
        log_widths = []
        thermal_fraction = []

        for time in time_list:
            os.makedirs(savepath, exist_ok=True)
            log_coldens.append([])
            log_widths.append([])
            thermal_fraction.append([])

            for direction in direction_list:
                coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_coldens[-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                log_coldens[-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_widths[-1].append(np.log10(widths[:, 1:]))

                #thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                #thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])
        log_coldens_concatenated = []
        log_width_concatenated = []
        thermal_fraction_concatenated = []
        for k in range(len(time_list)):#change to loop over direction when comparing directions
            log_coldens_concatenated.append(np.concatenate(log_coldens[k], axis=0))
            log_width_concatenated.append(np.concatenate(log_widths[k], axis=0))
            #thermal_fraction_concatenated.append(np.concatenate(thermal_fraction[k], axis=0))
                #kinematic_widths = np.loadtxt(blob_kinematic_width_file % (run_name, HM_value, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_kinematic_widths = np.log10(kinematic_widths[:, 1:])

                
        plt.figure(figsize=(20, 21), dpi=300)
        for i in range(len(indices)):
            width_norm = matplotlib.colors.Normalize(5.3, 7.7)
            for j in range(len(indices)):
                ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=log_width_concatenated[k][:, indices[j]], cmap=cmap, norm=width_norm, rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 19)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 19)
                    else:
                        ax.set_ylim(12, 16.5)
                else:
                    for k in range(len(time_list)):
                        if i == 0:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 19), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                        else:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 16.5), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=14)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=width_norm, cmap=cmap)
        cax.set_title('b/(cm/s)')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'colden_dist.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'colden_dist.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 19)
            for j in range(len(indices)):
                ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        if j == 0:
                            ax.scatter(log_width_concatenated[k][:, indices[j]], log_width_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=log_coldens_concatenated[k][:, indices[j]], cmap=cmap, norm=colden_norm_H, rasterized=True)
                        else:
                            ax.scatter(log_width_concatenated[k][:, indices[j]], log_width_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=log_coldens_concatenated[k][:, indices[j]], cmap=cmap, norm=colden_norm_metal, rasterized=True)
                    ax.set_xlim(5.3, 7.7)
                    ax.set_ylim(5.3, 7.7)

                else:
                    for k in range(len(time_list)):
                        if i == 0:
                            ax.hist(log_width_concatenated[k][:, indices[i]], bins=100, range=(5.3, 7.7), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                        else:
                            ax.hist(log_width_concatenated[k][:, indices[i]], bins=100, range=(5.3, 7.7), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=12)

                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)
        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=colden_norm_H, cmap=cmap)
        cax.set_title(r'$N_{\mathrm{H}}/(\mathrm{cm^{-2}})$')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 2, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=colden_norm_metal, cmap=cmap)
        cax.set_title(r'$N_{\mathrm{metal}}/(\mathrm{cm^{-2}})$')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'width_dist.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'width_dist.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()

        '''
        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            thermal_fraction_norm = matplotlib.colors.Normalize(0, 1)
            for j in range(len(indices)):
                ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=thermal_fraction_concatenated[k][:, indices[j]], cmap=cmap, norm=thermal_fraction_norm, rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 19)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 19)
                    else:
                        ax.set_ylim(12, 16.5)
                        
                else:
                    for k in range(len(time_list)):
                        if i == 0:
                            ax.hist(thermal_fraction_concatenated[k][:, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                        else:
                            ax.hist(thermal_fraction_concatenated[k][:, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=12)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)
                
                ax.set_box_aspect(1)
                    
        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=thermal_fraction_norm, cmap=cmap)
        cax.set_title('b_thermal/b_total')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'thermal_fraction.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'thermal_fraction.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()
        '''

def combined_plot_time_colored(run, redshift):
    run_name = run['Name']
    direction_list = np.arange(0, 1.1, 0.1)

    if run_name == 'T0.3_v1000_chi300_cond' or run_name == 'T0.3_v1700_chi300_cond':
        colors_local = ['green', 'red', 'orange']
        #direction_list = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        time_list = np.arange(1, 4)
        labels = ['t75', 't50', 't25']
    elif run_name == 'T0.3_v3000_chi300_cond':
        colors_local = ['red', 'orange']
        #direction_list = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        time_list = np.arange(2, 4)
        labels = ['t50', 't25']
    else:
        colors_local = ['blue', 'green', 'red', 'orange']
        #direction_list = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        time_list = np.arange(4)
        labels = ['t90', 't75', 't50', 't25']
    #HM_list = np.arange(3, 5)
    HM_list = [2]

    standard_temp_1 = 1e4
    standard_temp_2 = 1e5
    standard_temp_3 = 3e6
    standard_bk_list = np.logspace(-1.0, 2.7, 150)
    standard_b_list_1 = []
    standard_b_list_2 = []
    standard_b_list_3 = []
    for i in range(len(indices)):
        standard_b_list_1.append(0.5 * np.log10(standard_bk_list ** 2 + 0.0165 * standard_temp_1 / ion_weight_list[indices[i]]))
        standard_b_list_2.append(0.5 * np.log10(standard_bk_list ** 2 + 0.0165 * standard_temp_2 / ion_weight_list[indices[i]]))
        standard_b_list_3.append(0.5 * np.log10(standard_bk_list ** 2 + 0.0165 * standard_temp_3 / ion_weight_list[indices[i]]))

    for HM_value in HM_list:
        savepath = 'figures/HM_1e%d/' % HM_value

        log_coldens = []
        log_widths = []
        thermal_fraction = []
        log_thermal_temperatures = []

        for time in time_list:
            os.makedirs(savepath, exist_ok=True)
            log_coldens.append([])
            log_widths.append([])
            thermal_fraction.append([])
            log_thermal_temperatures.append([])

            for direction in direction_list:
                coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_coldens[-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                log_coldens[-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_widths[-1].append(np.log10(widths[:, 1:]) - 5)

                thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                ion_thermal_temp = (6.0574e-9 * thermal_widths[:, 1:]**2 * ion_weight_list)
                #log_thermal_widths = np.log10(thermal_widths[:, 1:])
                log_thermal_temperatures[-1].append(np.log10(ion_thermal_temp))


                thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])

        log_coldens_concatenated = []
        log_width_concatenated = []
        thermal_fraction_concatenated = []
        log_thermal_temperatures_concatenated = []
        for k in range(len(time_list)):#change to loop over direction when comparing directions
            log_coldens_concatenated.append(np.concatenate(log_coldens[k], axis=0))
            log_width_concatenated.append(np.concatenate(log_widths[k], axis=0))
            thermal_fraction_concatenated.append(np.concatenate(thermal_fraction[k], axis=0))
            log_thermal_temperatures_concatenated.append(np.concatenate(log_thermal_temperatures[k], axis=0))
            #kinematic_widths = np.loadtxt(blob_kinematic_width_file % (run_name, HM_value, time, run_name, 10 * direction), delimiter=',', skiprows=1)
            #log_kinematic_widths = np.log10(kinematic_widths[:, 1:]

                
        plt.figure(figsize=(20, 20), dpi=300)
        for i in range(len(indices)):
            width_norm = matplotlib.colors.Normalize(5.3, 7.7)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors_local[k], rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 20)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 20)
                    else:
                        ax.set_ylim(12, 16.5)
                else:
                    for k in range(len(time_list)):
                        if i == 0:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 20), histtype='step', color=colors_local[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$N/(\mathrm{cm^{-2}})$', fontsize=14)
                        else:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 16.5), histtype='step', color=colors_local[k])
                    #ax.tick_params(axis='both', labelsize=14)
                
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                elif j != 1 or i != 0:
                    ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=width_norm, cmap=cmap)
        #cax.set_title('b/(cm/s)')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        #plt.savefig(savepath + 'colden_dist_colored.png', dpi=500, bbox_inches='tight')
        if len(direction_list) == 1:
            plt.savefig(savepath + 'colden_dist_colored_%s_%d_z%g.pdf' % (run_name, 10 * direction_list[0], redshift), bbox_inches='tight')
        else:
            plt.savefig(savepath + 'colden_dist_colored_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 20)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        valid_pixels = np.where((log_coldens_concatenated[k][:, indices[i]] > 12) & (log_coldens_concatenated[k][:, indices[j]] > 12))[0]
                        ax.scatter(log_width_concatenated[k][valid_pixels, indices[j]], log_width_concatenated[k][valid_pixels, indices[i]], s=1.2, alpha=0.7, c=colors_local[k], rasterized=True)
                    
                    ax.plot(standard_b_list_1[j], standard_b_list_1[i], c='cyan', ls='--', label='T=%.0eK' % standard_temp_1)
                    ax.plot(standard_b_list_2[j], standard_b_list_2[i], c='magenta', ls='--', label='T=%.0eK' % standard_temp_2)
                    ax.plot(standard_b_list_3[j], standard_b_list_3[i], c='lime', ls='--', label='T=%.0eK' % standard_temp_3)

                    ax.set_xlim(0.3, 2.7)
                    ax.set_ylim(0.3, 2.7)

                else:
                    for k in range(len(time_list)):
                        valid_pixels = np.where(log_coldens_concatenated[k][:, indices[i]] > 12)[0]
                        if i == 0:
                            ax.hist(log_width_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0.3, 2.7), histtype='step', color=colors_local[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$\log [b/\mathrm{(km/s)}]$', fontsize=14)
                        else:
                            ax.hist(log_width_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0.3, 2.7), histtype='step', color=colors_local[k])
                    #ax.tick_params(axis='both', labelsize=12)

                if j == 0 and i == 1:
                    ax.legend(fontsize=14, framealpha=0.6)
                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                elif j != 1 or i != 0:
                    ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)
        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=colden_norm_H, cmap=cmap)
        #cax.set_title(r'$N_{\mathrm{H}}/(\mathrm{cm^{-2}})$')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 2, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=colden_norm_metal, cmap=cmap)
        #cax.set_title(r'$N_{\mathrm{metal}}/(\mathrm{cm^{-2}})$')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        #plt.savefig(savepath + 'width_dist_colored.png', dpi=500, bbox_inches='tight')
        if len(direction_list) == 1:
            plt.savefig(savepath + 'width_dist_colored_%s_%d_z%g.pdf' % (run_name, 10 * direction_list[0], redshift), bbox_inches='tight')
        else:
            plt.savefig(savepath + 'width_dist_colored_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')

        plt.clf()
        plt.close()

        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 20)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        valid_pixels = np.where((log_coldens_concatenated[k][:, indices[i]] > 12) & (log_coldens_concatenated[k][:, indices[j]] > 12))[0]
                        ax.scatter(log_thermal_temperatures_concatenated[k][valid_pixels, indices[j]], log_thermal_temperatures_concatenated[k][valid_pixels, indices[i]], s=1.2, alpha=0.7, c=colors_local[k], rasterized=True)

                    ax.set_xlim(3.8, 6.5)
                    ax.set_ylim(3.8, 6.5)

                else:
                    for k in range(len(time_list)):
                        valid_pixels = np.where(log_coldens_concatenated[k][:, indices[i]] > 12)[0]
                        if i == 0:
                            ax.hist(log_thermal_temperatures_concatenated[k][valid_pixels, indices[i]], bins=100, range=(3.8, 6.5), histtype='step', color=colors_local[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$\log (T/\mathrm{K})$', fontsize=14)
                        else:
                            ax.hist(log_thermal_temperatures_concatenated[k][valid_pixels, indices[i]], bins=100, range=(3.8, 6.5), histtype='step', color=colors_local[k])
                    #ax.tick_params(axis='both', labelsize=12)

                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                elif j != 1 or i != 0:
                    ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        #plt.savefig(savepath + 'width_dist_colored.png', dpi=500, bbox_inches='tight')
        if len(direction_list) == 1:
            plt.savefig(savepath + 'thermal_temp_dist_colored_%s_%d_z%g.pdf' % (run_name, 10 * direction_list[0], redshift), bbox_inches='tight')
        else:
            plt.savefig(savepath + 'thermal_temp_dist_colored_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')

        plt.clf()
        plt.close()
        '''
        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 20)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        valid_pixels = np.where((log_coldens_concatenated[k][:, indices[i]] > 12) & (log_coldens_concatenated[k][:, indices[j]] > 12))[0]
                        ax.scatter(log_width_concatenated[k][valid_pixels, indices[j]] + 0.5 * np.log10(1 - thermal_fraction_concatenated[k][valid_pixels, indices[j]] ** 2),\
                                    log_width_concatenated[k][valid_pixels, indices[i]] + 0.5 * np.log10(1 - thermal_fraction_concatenated[k][valid_pixels, indices[i]] ** 2),\
                                          s=1.2, alpha=0.7, c=colors_local[k], rasterized=True)

                    ax.set_xlim(0.3, 2.7)
                    ax.set_ylim(0.3, 2.7)

                else:
                    for k in range(len(time_list)):
                        valid_pixels = np.where(log_coldens_concatenated[k][:, indices[i]] > 12)[0]
                        if i == 0:
                            ax.hist(log_width_concatenated[k][valid_pixels, indices[i]] + 0.5 * np.log10(1 - thermal_fraction_concatenated[k][valid_pixels, indices[i]] ** 2),\
                                     bins=100, range=(0.3, 2.7), histtype='step', color=colors_local[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$\log [b_{\mathrm{kin}}/\mathrm{(km/s)}]$', fontsize=14)
                        else:
                            ax.hist(log_width_concatenated[k][valid_pixels, indices[i]] + 0.5 * np.log10(1 - thermal_fraction_concatenated[k][valid_pixels, indices[i]] ** 2),\
                                     bins=100, range=(0.3, 2.7), histtype='step', color=colors_local[k])
                    #ax.tick_params(axis='both', labelsize=12)

                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                elif j != 1 or i != 0:
                    ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        #plt.savefig(savepath + 'width_dist_colored.png', dpi=500, bbox_inches='tight')
        if len(direction_list) == 1:
            plt.savefig(savepath + 'kinematic_width_dist_colored_%s_%d_%g.pdf' % (run_name, 10 * direction_list[0], redshift), bbox_inches='tight')
        else:
            plt.savefig(savepath + 'kinematic_width_dist_colored_%s_%g.pdf' % (run_name, redshift), bbox_inches='tight')

        plt.clf()
        plt.close()
        '''
        
        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            thermal_fraction_norm = matplotlib.colors.Normalize(0, 1)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(time_list)):
                        valid_pixels = np.where((log_coldens_concatenated[k][:, indices[i]] > 12) & (log_coldens_concatenated[k][:, indices[j]] > 12))[0]
                        ax.scatter(log_coldens_concatenated[k][valid_pixels, indices[j]], log_coldens_concatenated[k][valid_pixels, indices[i]], s=1.2, alpha=0.7, c=colors_local[k], rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 20)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 20)
                    else:
                        ax.set_ylim(12, 16.5)
                        
                else:
                    for k in range(len(time_list)):
                        valid_pixels = np.where(log_coldens_concatenated[k][:, indices[i]] > 12)[0]
                        if i == 0:
                            ax.hist(thermal_fraction_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors_local[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel('b_thermal/b_total', fontsize=14)
                        else:
                            ax.hist(thermal_fraction_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors_local[k])
                    #ax.tick_params(axis='both', labelsize=12)

                ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                elif j != 1 or i != 0:
                    ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)
                
                ax.set_box_aspect(1)
                    
        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=thermal_fraction_norm, cmap=cmap)
        #cax.set_title('b_thermal/b_total')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        #plt.savefig(savepath + 'thermal_fraction_colored_%s.png' % run_name, dpi=500, bbox_inches='tight')
        if len(direction_list) == 1:
            plt.savefig(savepath + 'thermal_fraction_colored_%s_%d_z%g.pdf' % (run_name, 10 * direction_list[0], redshift), bbox_inches='tight')
        else:
            plt.savefig(savepath + 'thermal_fraction_colored_%s_z%g.pdf' % (run_name, redshift), bbox_inches='tight')

        plt.clf()
        plt.close()
        

def combined_plot_direction(run, redshift):
    run_name = run['Name']
    #direction_list = [0, 1.0]
    direction_list = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    time_list = np.arange(4)
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    labels = [r'$\cos \theta=%.1f$' % direction for direction in direction_list]

    for HM_value in HM_list:
        savepath = 'figures/HM_1e%d/' % HM_value

        log_coldens = []
        log_widths = []
        thermal_fraction = []

        for time in time_list:
            os.makedirs(savepath, exist_ok=True)
            log_coldens.append([])
            log_widths.append([])
            thermal_fraction.append([])

            for direction in direction_list:
                coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_coldens[-1].append(np.log10(coldens[:, 1:]))

                widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_widths[-1].append(np.log10(widths[:, 1:]))

                #thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                #thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])
        log_coldens_concatenated = []
        log_width_concatenated = []
        thermal_fraction_concatenated = []
        for k in range(len(direction_list)):#change to loop over direction when comparing directions
            log_coldens_concatenated.append(np.concatenate([log_coldens[l][k] for l in range(len(time_list))], axis=0))
            log_width_concatenated.append(np.concatenate([log_widths[l][k] for l in range(len(time_list))], axis=0))
            #thermal_fraction_concatenated.append(np.concatenate([thermal_fraction[l][k] for l in range(len(time_list))], axis=0))
                #kinematic_widths = np.loadtxt(blob_kinematic_width_file % (run_name, HM_value, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_kinematic_widths = np.log10(kinematic_widths[:, 1:])

        
        plt.figure(figsize=(20, 21), dpi=300)
        for i in range(len(indices)):
            width_norm = matplotlib.colors.Normalize(5.3, 7.7)
            for j in range(len(indices)):
                ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(direction_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=log_width_concatenated[k][:, indices[j]], cmap=cmap, norm=width_norm, rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 19)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 19)
                    else:
                        ax.set_ylim(12, 16.5)
                else:
                    for k in range(len(direction_list)):
                        if i == 0:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 19), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                        else:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 16.5), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=14)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=width_norm, cmap=cmap)
        cax.set_title('b/(cm/s)')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'colden_dist_direction.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'colden_dist_direction.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 19)
            for j in range(len(indices)):
                ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(direction_list)):
                        if j == 0:
                            ax.scatter(log_width_concatenated[k][:, indices[j]], log_width_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=log_coldens_concatenated[k][:, indices[j]], cmap=cmap, norm=colden_norm_H, rasterized=True)
                        else:
                            ax.scatter(log_width_concatenated[k][:, indices[j]], log_width_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=log_coldens_concatenated[k][:, indices[j]], cmap=cmap, norm=colden_norm_metal, rasterized=True)
                    ax.set_xlim(5.3, 7.7)
                    ax.set_ylim(5.3, 7.7)

                else:
                    for k in range(len(direction_list)):
                        if i == 0:
                            ax.hist(log_width_concatenated[k][:, indices[i]], bins=100, range=(5.3, 7.7), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                        else:
                            ax.hist(log_width_concatenated[k][:, indices[i]], bins=100, range=(5.3, 7.7), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=12)

                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)
        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=colden_norm_H, cmap=cmap)
        cax.set_title(r'$N_{\mathrm{H}}/(\mathrm{cm^{-2}})$')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 2, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=colden_norm_metal, cmap=cmap)
        cax.set_title(r'$N_{\mathrm{metal}}/(\mathrm{cm^{-2}})$')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'width_dist_direction.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'width_dist_direction.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()
        '''
        
        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            thermal_fraction_norm = matplotlib.colors.Normalize(0, 1)
            for j in range(len(indices)):
                ax = plt.subplot(len(indices) + 1, len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(direction_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=thermal_fraction_concatenated[k][:, indices[j]], cmap=cmap, norm=thermal_fraction_norm, rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 19)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 19)
                    else:
                        ax.set_ylim(12, 16.5)
                        
                else:
                    for k in range(len(direction_list)):
                        if i == 0:
                            ax.hist(thermal_fraction_concatenated[k][:, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                        else:
                            ax.hist(thermal_fraction_concatenated[k][:, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=12)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)
                
                ax.set_box_aspect(1)
                    
        cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        sm = matplotlib.cm.ScalarMappable(norm=thermal_fraction_norm, cmap=cmap)
        cax.set_title('b_thermal/b_total')
        plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'thermal_fraction_direction.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'thermal_fraction_direction.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()
        '''

def combined_plot_direction_colored(run, redshift):
    run_name = run['Name']
    direction_list = [0, 1.0]
    #direction_list = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    time_list = np.arange(4)
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    labels = [r'$\cos \theta=%.1f$' % direction for direction in direction_list]

    for HM_value in HM_list:
        savepath = 'figures/%s/HM_1e%d/' % (run_name, HM_value)

        log_coldens = []
        log_widths = []
        thermal_fraction = []

        for time in time_list:
            os.makedirs(savepath, exist_ok=True)
            log_coldens.append([])
            log_widths.append([])
            thermal_fraction.append([])

            for direction in direction_list:
                coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_coldens[-1].append(np.log10(coldens[:, 1:]))

                widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                log_widths[-1].append(np.log10(widths[:, 1:]))

                thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])

        log_coldens_concatenated = []
        log_width_concatenated = []
        thermal_fraction_concatenated = []
        for k in range(len(direction_list)):#change to loop over direction when comparing directions
            log_coldens_concatenated.append(np.concatenate([log_coldens[l][k] for l in range(len(time_list))], axis=0))
            log_width_concatenated.append(np.concatenate([log_widths[l][k] for l in range(len(time_list))], axis=0))
            thermal_fraction_concatenated.append(np.concatenate([thermal_fraction[l][k] for l in range(len(time_list))], axis=0))
                #kinematic_widths = np.loadtxt(blob_kinematic_width_file % (run_name, HM_value, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                #log_kinematic_widths = np.log10(kinematic_widths[:, 1:])

        '''
        plt.figure(figsize=(20, 21), dpi=300)
        for i in range(len(indices)):
            width_norm = matplotlib.colors.Normalize(5.3, 7.7)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(direction_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 19)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 19)
                    else:
                        ax.set_ylim(12, 16.5)
                else:
                    for k in range(len(direction_list)):
                        if i == 0:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 19), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$N/(\mathrm{cm^{-2}})$', fontsize=14)
                        else:
                            ax.hist(log_coldens_concatenated[k][:, indices[i]], bins=100, range=(12, 16.5), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=14)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=width_norm, cmap=cmap)
        #cax.set_title('b/(cm/s)')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'colden_dist_direction_colored.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'colden_dist_direction_colored.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 19)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(direction_list)):
                        if j == 0:
                            ax.scatter(log_width_concatenated[k][:, indices[j]], log_width_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                        else:
                            ax.scatter(log_width_concatenated[k][:, indices[j]], log_width_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                    ax.set_xlim(5.3, 7.7)
                    ax.set_ylim(5.3, 7.7)

                else:
                    for k in range(len(direction_list)):
                        if i == 0:
                            ax.hist(log_width_concatenated[k][:, indices[i]], bins=100, range=(5.3, 7.7), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel('b/(cm/s)', fontsize=14)
                        else:
                            ax.hist(log_width_concatenated[k][:, indices[i]], bins=100, range=(5.3, 7.7), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=12)

                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)
        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=colden_norm_H, cmap=cmap)
        #cax.set_title(r'$N_{\mathrm{H}}/(\mathrm{cm^{-2}})$')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 2, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=colden_norm_metal, cmap=cmap)
        #cax.set_title(r'$N_{\mathrm{metal}}/(\mathrm{cm^{-2}})$')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'width_dist_direction_colored.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'width_dist_direction_colored.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()

        '''
        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            thermal_fraction_norm = matplotlib.colors.Normalize(0, 1)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(direction_list)):
                        ax.scatter(log_coldens_concatenated[k][:, indices[j]], log_coldens_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 19)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 19)
                    else:
                        ax.set_ylim(12, 16.5)
                        
                else:
                    for k in range(len(direction_list)):
                        if i == 0:
                            ax.hist(thermal_fraction_concatenated[k][:, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel('b_thermal/b_total', fontsize=14)
                        else:
                            ax.hist(thermal_fraction_concatenated[k][:, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k])
                    #ax.tick_params(axis='both', labelsize=12)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                else:
                    ax.tick_params(axis='y', labelsize=14)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(axis='x', labelsize=14)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)
                
                ax.set_box_aspect(1)
                    
        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=thermal_fraction_norm, cmap=cmap)
        #cax.set_title('b_thermal/b_total')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig(savepath + 'thermal_fraction_direction_colored.png', dpi=500, bbox_inches='tight')
        plt.savefig(savepath + 'thermal_fraction_direction_colored.pdf', bbox_inches='tight')
        plt.clf()
        plt.close()
        

def combined_plot_run_colored(redshift):
    direction_list = [0, 1.0]
    time_list = np.arange(4)
    #HM_list = np.arange(3, 5)
    HM_list = [2]
    labels = [run['Name'] for run in run_list]

    for HM_value in HM_list:
        log_coldens_double_concatenated = []
        log_width_double_concatenated = []
        thermal_fraction_double_concatenated = []
        for run in run_list:
            run_name = run['Name']            

            log_coldens = []
            log_widths = []
            thermal_fraction = []

            for time in time_list:
                log_coldens.append([])
                log_widths.append([])
                thermal_fraction.append([])

                for direction in direction_list:
                    coldens = np.loadtxt(blob_colden_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_coldens[-1].append(np.log10(coldens[:, 1:]) + scaling_factor_metal)
                    log_coldens[-1][-1][:, 0] += scaling_factor_HI - scaling_factor_metal

                    widths = np.loadtxt(blob_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    log_widths[-1].append(np.log10(widths[:, 1:]) - 5)

                    thermal_widths = np.loadtxt(blob_thermal_width_file % (run_name, HM_value, redshift, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_thermal_widths = np.log10(thermal_widths[:, 1:])

                    thermal_fraction[-1].append(thermal_widths[:, 1:] / widths[:, 1:])
            log_coldens_concatenated = []
            log_width_concatenated = []
            thermal_fraction_concatenated = []
            for k in range(len(time_list)):#change to loop over direction when comparing directions
                log_coldens_concatenated.append(np.concatenate(log_coldens[k], axis=0))
                log_width_concatenated.append(np.concatenate(log_widths[k], axis=0))
                thermal_fraction_concatenated.append(np.concatenate(thermal_fraction[k], axis=0))
                    #kinematic_widths = np.loadtxt(blob_kinematic_width_file % (run_name, HM_value, time, run_name, 10 * direction), delimiter=',', skiprows=1)
                    #log_kinematic_widths = np.log10(kinematic_widths[:, 1:]

            log_coldens_double_concatenated.append(np.concatenate(log_coldens_concatenated, axis=0))
            log_width_double_concatenated.append(np.concatenate(log_width_concatenated, axis=0))
            thermal_fraction_double_concatenated.append(np.concatenate(thermal_fraction_concatenated, axis=0))
                        
        plt.figure(figsize=(20, 20), dpi=300)
        for i in range(len(indices)):
            width_norm = matplotlib.colors.Normalize(5.3, 7.7)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(run_list) - 1, -1, -1):
                        ax.scatter(log_coldens_double_concatenated[k][:, indices[j]], log_coldens_double_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                    if j == 0:
                        ax.set_xlim(11, 20)
                    else:
                        ax.set_xlim(11, 16.5)
                    if i == 0:
                        ax.set_ylim(11, 20)
                    else:
                        ax.set_ylim(11, 16.5)
                else:
                    for k in range(len(run_list) - 1, -1, -1):
                        if i == 0:
                            ax.hist(log_coldens_double_concatenated[k][:, indices[i]], bins=100, range=(12, 20), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$N/(\mathrm{cm^{-2}})$')
                            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                        else:
                            ax.hist(log_coldens_double_concatenated[k][:, indices[i]], bins=100, range=(12, 16.5), histtype='step', color=colors[k])
                            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    #ax.tick_params(axis='both', labelsize=14)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                else:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)

        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=width_norm, cmap=cmap)
        #cax.set_title('b/(cm/s)')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig('figures/colden_dist_colored_HM1e%d.png' % HM_value, dpi=500, bbox_inches='tight')
        plt.savefig('figures/colden_dist_colored_HM1e%d.pdf' % HM_value, bbox_inches='tight')
        plt.clf()
        plt.close()

        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            colden_norm_metal = matplotlib.colors.Normalize(12, 16.5)
            colden_norm_H = matplotlib.colors.Normalize(12, 19)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(run_list) - 1, -1, -1):
                        valid_pixels = np.where((log_coldens_double_concatenated[k][:, indices[i]] > 12) & (log_coldens_double_concatenated[k][:, indices[j]] > 12))[0]
                        ax.scatter(log_width_double_concatenated[k][valid_pixels, indices[j]], log_width_double_concatenated[k][valid_pixels, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                    ax.set_xlim(0.5, 2.7)
                    ax.set_ylim(0.5, 2.7)

                else:
                    for k in range(len(run_list) - 1, -1, -1):
                        if i == 0:
                            valid_pixels = np.where(log_coldens_double_concatenated[k][:, indices[i]] > 12)[0]
                            ax.hist(log_width_double_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0.5, 2.7), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel(r'$\log(b/(\mathrm{km/s}))$', fontsize=15)
                            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                        else:
                            valid_pixels = np.where(log_coldens_double_concatenated[k][:, indices[i]] > 12)[0]
                            ax.hist(log_width_double_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0.5, 2.7), histtype='step', color=colors[k])
                            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    #ax.tick_params(axis='both', labelsize=12)

                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                else:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.axes.xaxis.set_ticklabels([])
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)

                ax.set_box_aspect(1)
        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=colden_norm_H, cmap=cmap)
        #cax.set_title(r'$N_{\mathrm{H}}/(\mathrm{cm^{-2}})$')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 2, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=colden_norm_metal, cmap=cmap)
        #cax.set_title(r'$N_{\mathrm{metal}}/(\mathrm{cm^{-2}})$')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig('figures/width_dist_colored_HM1e%d.png' % HM_value, dpi=500, bbox_inches='tight')
        plt.savefig('figures/width_dist_colored_HM1e%d.pdf' % HM_value, bbox_inches='tight')
        plt.clf()
        plt.close()

        
        plt.figure(figsize=(20, 18), dpi=300)
        for i in range(len(indices)):
            thermal_fraction_norm = matplotlib.colors.Normalize(0, 1)
            for j in range(i + 1):
                ax = plt.subplot(len(indices), len(indices), i * len(indices) + j + 1)
                if j != i:
                    for k in range(len(run_list) - 1, -1, -1):
                        ax.scatter(log_coldens_double_concatenated[k][:, indices[j]], log_coldens_double_concatenated[k][:, indices[i]], s=1.2, alpha=0.7, c=colors[k], rasterized=True)
                    if j == 0:
                        ax.set_xlim(12, 20)
                    else:
                        ax.set_xlim(12, 16.5)
                    if i == 0:
                        ax.set_ylim(12, 20)
                    else:
                        ax.set_ylim(12, 16.5)
                        
                else:
                    for k in range(len(run_list) - 1, -1, -1):
                        if i == 0:
                            valid_pixels = np.where(log_coldens_double_concatenated[k][:, indices[i]] > 12)[0]
                            ax.hist(thermal_fraction_double_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k], label=labels[k])
                            ax.legend(fontsize=14, framealpha=0.6)
                            ax.set_xlabel('b_thermal/b_total', fontsize=14)
                            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                        else:
                            valid_pixels = np.where(log_coldens_double_concatenated[k][:, indices[i]] > 12)[0]
                            ax.hist(thermal_fraction_double_concatenated[k][valid_pixels, indices[i]], bins=100, range=(0, 1), histtype='step', color=colors[k])
                            ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    #ax.tick_params(axis='both', labelsize=12)
                
                if (j != 0 and i != 0) or (j > 1 and i == 0):
                    ax.axes.yaxis.set_ticklabels([])
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                else:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    if j != 1 or i != 0:
                        ax.set_ylabel(ion_list[indices[i]], fontsize=16)
                if i != len(indices) - 1:
                    ax.tick_params(which='both', direction='in', labelsize=15, right=True, top=True)
                    ax.axes.xaxis.set_ticklabels([])
                else:
                    ax.set_xlabel(ion_list[indices[j]], fontsize=16)
                
                ax.set_box_aspect(1)
                    
        #cax = plt.subplot(len(indices) + 1, len(indices), len(indices) ** 2 + 1, box_aspect=0.06)
        #sm = matplotlib.cm.ScalarMappable(norm=thermal_fraction_norm, cmap=cmap)
        #cax.set_title('b_thermal/b_total')
        #plt.colorbar(sm, cax=cax, orientation='horizontal')

        plt.subplots_adjust(hspace=0.05, wspace=0.05)
        plt.tight_layout()
        plt.savefig('figures/thermal_fraction_colored_HM1e%d.png' % HM_value, dpi=500, bbox_inches='tight')
        plt.savefig('figures/thermal_fraction_colored_HM1e%d.pdf' % HM_value, bbox_inches='tight')
        plt.clf()
        plt.close()
        

if __name__ == '__main__':
    redshift = 0.5396
    redshift_list = [0.1006, 0.5396, 1.053, 2.013]
    HM_list = [2, 2, 2, 2]
    #compare_redshift(redshift_list, HM_list)
    #with Pool(len(run_list)) as p:
    #    p.map(combined_plot_time_colored, run_list)
    #histograms(redshift)
    #combined_plot_run_colored()
    #compare_directions(redshift)
    #for run in run_list:
    #    combined_plot_time_colored(run, redshift)
    for run in run_list:
        ion_maps(run, redshift)
    #run_list = [run16, run1, run11, run12]
    #time = 2
    #ion_maps_compare_conduction(run_list, time, redshift)
    #ion_maps_compare_runs(run_list, time, redshift)
    #phase_space(redshift)
    #compare_scaling_factors()
    #compare_density_cuts()