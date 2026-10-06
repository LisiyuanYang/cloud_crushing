from os import read
import numpy as np
import sqlite3
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.cm import get_cmap
#from multiprocessing import Pool

run1 = { 'Name':'T0.3_v1000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132']}

run4 = { 'Name':'T0.3_v1000_chi300',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0025', '0033', '0042', '0058']}

run11 = { 'Name':'T0.3_v1700_chi300_cond',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078']}
        #'f_list':['0078']}
    
run12 = { 'Name':'T0.3_v3000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0001', '0004', '0014', '0035']}

run16 = { 'Name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085']}

run17 = { 'Name':'T0.3_v3000_chi300',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':11.4,
        'tcc':0.56,
        'velocity':3000,
        'f_list':['0028', '0044', '0065', '0110']}

run25 = { 'Name':'T0.05_v110_chi50',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':1.0,
        'velocity':110,
        'tcc':6.4,
        'f_list':['%04d' % snapnum for snapnum in range(58)]}


runlist = [run4, run1, run16, run11, run17, run12]
ion_list = ['H I 1215', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV', 'N V']
ion_weight_list = np.array([1., 4., 12., 12., 12., 16., 16., 16., 16., 20., 24., 28., 28., 28., 14.])
ionization_order = [0, 10, 2, 12, 13, 4, 6, 7, 9, 8]

projection_database = '/work/lyang_umass_edu/projectedColumns-main/data_bases/coldens_blob_1e%d.db'
projection_path = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e%d/TF1.0/blob0.825/t%d/'

if __name__ == '__main__':
    timemark = 3
    blob_cut = 0.825
    temp_floor = 1.0
    #background_values = np.arange(8)
    background_values = [4]
    background_base = 'HM_1e%d'
    xlist = np.arange(0, 801, 2)
    ylist = xlist.copy()

    #direction_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    direction_list = [0.0, 1.0]

    scaling_factor = 2e-3
    for run in runlist:
        run_name = run['Name']
        for background_value in background_values:
            for direction in direction_list:
                background = background_base % background_value
                database = projection_database % background_value
                #conn = sqlite3.connect(database, detect_types=sqlite3.PARSE_DECLTYPES)
                ion_colden_list = []
                ion_width_list = []
                ion_thermal_width_list = []
                ion_kinematic_width_list = []
                ion_temp_list = []
                ion_thermal_temp_list = []
                ion_kinematic_temp_list = []

                colden = np.loadtxt(projection_path % (run_name, background_value, timemark) + '%s_colden_%d.csv' % (run_name, 10 * direction), delimiter=',', skiprows=1)
                colden = np.nan_to_num(colden[:, 1:]) * scaling_factor
                ion_colden_list = colden.transpose()

                width = np.loadtxt(projection_path % (run_name, background_value, timemark) + '%s_width_%d.csv' % (run_name, 10 * direction), delimiter=',', skiprows=1)
                width = np.nan_to_num(width[:, 1:])
                ion_width_list = width.transpose()
                ion_temp_list = (6.0574e-9 * width**2 * ion_weight_list).transpose()

                thermal_width = np.loadtxt(projection_path % (run_name, background_value, timemark) + '%s_thermal_width_%d.csv' % (run_name, 10 * direction), delimiter=',', skiprows=1)
                thermal_width = np.nan_to_num(thermal_width[:, 1:])
                ion_thermal_width_list = thermal_width.transpose()
                ion_thermal_temp_list = (6.0574e-9 * thermal_width**2 * ion_weight_list).transpose()

                kinematic_width = np.loadtxt(projection_path % (run_name, background_value, timemark) + '%s_kinematic_width_%d.csv' % (run_name, 10 * direction), delimiter=',', skiprows=1)
                kinematic_width = np.nan_to_num(kinematic_width[:, 1:]) * 1.41421
                ion_kinematic_width_list = kinematic_width.transpose()
                ion_kinematic_temp_list = (6.0574e-9 * kinematic_width**2 * ion_weight_list).transpose()

                #useful_pixels = np.any(ion_colden_list[:, 1:] > 1e12, axis=1)
                print(background_value, direction, np.argmax(ion_temp_list[8]), np.max(ion_temp_list[8]))
                
                #conn.close()
                '''
                plt.figure(figsize=(10, 16))
                for i in range(len(ion_list)):
                    plt.subplot(len(ion_list), 4, 4*i + 1)
                    plt.pcolormesh(xlist, ylist, ion_colden_list[i].reshape((400, 400)), norm=LogNorm(), rasterized=True)
                    plt.title(ion_list[i], fontsize=14)
                    #plt.ylabel(ion_list[i], rotation=0, fontsize=14, position=(1.4, 0.5))
                    plt.gca().yaxis.set_label_coords(1.035, 0.4)
                    if np.count_nonzero(ion_temp_list[i]) > 1:
                        cb = plt.colorbar(orientation="horizontal")
                        cb.solids.set_rasterized(True)
                        cb.ax.set_ylabel(r'N/$\mathrm{cm^{-2}}$', rotation=0, fontsize=14)
                        cb.ax.yaxis.set_label_coords(1.09, 0.2)
                        cb.ax.tick_params(labelsize=14)
                    plt.xlim(-400, 400)
                    plt.ylim(-100, 100)
                    plt.gca().set_xticklabels([])
                    plt.gca().set_yticklabels([])
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.tick_params(axis='both', top=True, right=True, direction='in', labelsize=14)

                    plt.subplot(len(ion_list), 4, 4*i + 2)
                    plt.pcolormesh(xlist, ylist, ion_temp_list[i].reshape((400, 400)), norm=LogNorm(), rasterized=True)
                    plt.title('effective temperature')
                    #plt.ylabel(ion_list[i], rotation=0, fontsize=14, position=(1.4, 0.5))
                    plt.gca().yaxis.set_label_coords(1.035, 0.4)
                    if np.count_nonzero(ion_temp_list[i]) > 2:
                        cb = plt.colorbar(orientation="horizontal")
                        cb.solids.set_rasterized(True)
                        cb.ax.set_ylabel(r'T/$\mathrm{K}$', rotation=0, fontsize=14)
                        cb.ax.yaxis.set_label_coords(1.05, 0.2)
                        cb.ax.tick_params(labelsize=14)
                        cb_range = cb.ax.get_xlim()
                    plt.xlim(-400, 400)
                    plt.ylim(-100, 100)
                    plt.gca().set_xticklabels([])
                    plt.gca().set_yticklabels([])
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.tick_params(axis='both', top=True, right=True, direction='in', labelsize=14)

                    plt.subplot(len(ion_list), 4, 4*i + 3)
                    plt.pcolormesh(xlist, ylist, ion_thermal_temp_list[i].reshape((400, 400)), norm=LogNorm(), rasterized=True)
                    plt.clim(cb_range)
                    plt.title('thermal broadening')
                    #plt.ylabel(ion_list[i], rotation=0, fontsize=14, position=(1.4, 0.5))
                    plt.gca().yaxis.set_label_coords(1.035, 0.4)
                    if np.count_nonzero(ion_thermal_temp_list[i]) > 2:
                        cb = plt.colorbar(orientation="horizontal")
                        cb.solids.set_rasterized(True)
                        cb.ax.set_ylabel(r'T/$\mathrm{K}$', rotation=0, fontsize=14)
                        cb.ax.yaxis.set_label_coords(1.05, 0.2)
                        cb.ax.tick_params(labelsize=14)
                    plt.xlim(-400, 400)
                    plt.ylim(-100, 100)
                    plt.gca().set_xticklabels([])
                    plt.gca().set_yticklabels([])
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.tick_params(axis='both', top=True, right=True, direction='in', labelsize=14)

                    plt.subplot(len(ion_list), 4, 4*i + 4)
                    plt.pcolormesh(xlist, ylist, ion_kinematic_temp_list[i].reshape((400, 400)), norm=LogNorm(), rasterized=True)
                    plt.clim(cb_range)
                    plt.title('kinematic broadening')
                    #plt.ylabel(ion_list[i], rotation=0, fontsize=14, position=(1.4, 0.5))
                    plt.gca().yaxis.set_label_coords(1.035, 0.4)
                    if np.count_nonzero(ion_kinematic_temp_list[i]) > 2:
                        cb = plt.colorbar(orientation="horizontal")
                        cb.solids.set_rasterized(True)
                        cb.ax.set_ylabel(r'T/$\mathrm{K}$', rotation=0, fontsize=14)
                        cb.ax.yaxis.set_label_coords(1.05, 0.2)
                        cb.ax.tick_params(labelsize=14)
                    plt.xlim(-400, 400)
                    plt.ylim(-100, 100)
                    plt.gca().set_xticklabels([])
                    plt.gca().set_yticklabels([])
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.tick_params(axis='both', top=True, right=True, direction='in', labelsize=14)

                #plt.tight_layout()
                plt.savefig(projection_path % (run_name, background_value, timemark) + 'effective_temp_map_%d.png' % (10 * direction), dpi=400, bbox_inches='tight')
                plt.savefig(projection_path % (run_name, background_value, timemark) + 'effective_temp_map_%d.eps' % (10 * direction), bbox_inches='tight')
                #plt.savefig('/home/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/column_density_map_%d.eps' % (background, 10 * direction), bbox_inches='tight')
                #plt.show()
                plt.close()
                
                
                plt.figure(figsize=(5.5, 18))
                for i in range(len(ion_list)):
                    plt.subplot(len(ion_list), 2, i + 1)
                    plt.pcolormesh(xlist, ylist, ion_colden_list[i].reshape((400, 400)), norm=LogNorm(), rasterized=True)
                    plt.title(ion_list[i], fontsize=16)
                    #plt.ylabel(ion_list[i], rotation=0, fontsize=16, position=(1.4, 0.5))
                    plt.gca().yaxis.set_label_coords(1.035, 0.4)
                    if np.count_nonzero(ion_temp_list[i]) > 1:
                        cb = plt.colorbar(orientation="horizontal")
                        cb.ax.set_ylabel(r'N/$\mathrm{cm^{-2}}$', rotation=0, fontsize=16)
                        cb.ax.yaxis.set_label_coords(1.09, 0.2)
                        cb.ax.tick_params(labelsize=16)
                    plt.xlim(-400, 400)
                    plt.ylim(-100, 100)
                    plt.gca().set_xticklabels([])
                    plt.gca().set_yticklabels([])
                    plt.gca().set_aspect('equal', adjustable='box')
                    plt.tick_params(axis='both', top=True, right=True, direction='in', labelsize=16)

                #plt.tight_layout()
                plt.savefig(projection_path % (run_name, background_value, timemark) + 'colden_map_%d.png' % (10 * direction), dpi=400, bbox_inches='tight')
                plt.savefig(projection_path % (run_name, background_value, timemark) + 'colden_map_%d.eps' % (10 * direction), bbox_inches='tight')
                #plt.savefig('/home/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/column_density_map_%d.eps' % (background, 10 * direction), bbox_inches='tight')
                #plt.show()
                plt.close()
                '''
                plt.figure(figsize=(18, 5))
                plt.subplot(131)
                for index in ionization_order:
                    plt.scatter(ion_colden_list[index], ion_temp_list[index], s=0.8, alpha=0.5, label=ion_list[index], rasterized=True)
                plt.title('total', fontsize=18)
                plt.xlim(2e9, 2e16)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlabel(r'$N/\mathrm{cm^{-2}}$', fontsize=18)
                plt.ylabel(r'$T_{\mathrm{eff}}/\mathrm{K}$', fontsize=18)
                plt.tick_params(labelsize=18)
                if direction == direction_list[0]:
                    xlim = plt.gca().get_xlim()
                    ylim = plt.gca().get_ylim()

                plt.subplot(132)
                for index in ionization_order:
                    plt.scatter(ion_colden_list[index], ion_thermal_temp_list[index], s=0.8, alpha=0.5, label=ion_list[index], rasterized=True)
                plt.title('thermal', fontsize=18)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlim(xlim)
                plt.ylim(ylim)
                #leg = plt.legend(fontsize=10)
                #leg.get_frame().set_facecolor('none')
                plt.xlabel(r'$N/\mathrm{cm^{-2}}$', fontsize=18)
                plt.ylabel(r'$T_{\mathrm{thermal}}/\mathrm{K}$', fontsize=18)
                plt.tick_params(labelsize=18)

                plt.subplot(133)
                for index in ionization_order:
                    plt.scatter(ion_colden_list[index], ion_kinematic_temp_list[index], s=0.8, alpha=0.5, label=ion_list[index], rasterized=True)
                plt.title('kinematic', fontsize=18)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlim(xlim)
                plt.ylim(ylim)
                #leg = plt.legend(fontsize=10)
                #leg.get_frame().set_facecolor('none')
                leg = plt.legend(fontsize=18, frameon=False, loc=(1.01, 0), markerscale=4)
                plt.xlabel(r'$N/\mathrm{cm^{-2}}$', fontsize=18)
                plt.ylabel(r'$T_{\mathrm{doppler}}/\mathrm{K}$', fontsize=18)
                plt.tick_params(labelsize=18)

                plt.savefig(projection_path % (run_name, background_value, timemark) + '%s_pd_%d.png' % (run_name, 10 * direction), dpi=500, bbox_inches='tight')
                plt.savefig(projection_path % (run_name, background_value, timemark) + '%s_pd_%d.eps' % (run_name, 10 * direction), bbox_inches='tight')
                plt.close()

                plt.figure(figsize=(18, 5))
                plt.subplot(131)
                for index in ionization_order:
                    plt.scatter(ion_colden_list[index], ion_width_list[index], s=0.8, alpha=0.5, label=ion_list[index], rasterized=True)
                plt.title('total', fontsize=18)
                plt.xlim(2e9, 2e16)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlabel(r'$N/\mathrm{cm^{-2}}$', fontsize=18)
                plt.ylabel(r'$b/\mathrm{(cm/s)}$', fontsize=18)
                plt.tick_params(labelsize=18)
                if direction == direction_list[0]:
                    xlim_2 = plt.gca().get_xlim()
                    ylim_2 = plt.gca().get_ylim()

                plt.subplot(132)
                for index in ionization_order:
                    plt.scatter(ion_colden_list[index], ion_thermal_width_list[index], s=0.8, alpha=0.5, label=ion_list[index], rasterized=True)
                plt.title('thermal', fontsize=18)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlim(xlim_2)
                plt.ylim(ylim_2)
                #leg = plt.legend(fontsize=10)
                #leg.get_frame().set_facecolor('none')
                plt.xlabel(r'$N/\mathrm{cm^{-2}}$', fontsize=18)
                plt.ylabel(r'$b/\mathrm{(cm/s)}$', fontsize=18)
                plt.tick_params(labelsize=18)

                plt.subplot(133)
                for index in ionization_order:
                    plt.scatter(ion_colden_list[index], ion_kinematic_width_list[index], s=0.8, alpha=0.5, label=ion_list[index], rasterized=True)
                plt.title('kinematic', fontsize=18)
                plt.xscale('log')
                plt.yscale('log')
                plt.xlim(xlim_2)
                plt.ylim(ylim_2)
                #leg = plt.legend(fontsize=10)
                #leg.get_frame().set_facecolor('none')
                leg = plt.legend(fontsize=18, frameon=False, loc=(1.01, 0), markerscale=4)
                plt.xlabel(r'$N/\mathrm{cm^{-2}}$', fontsize=18)
                plt.ylabel(r'$b/\mathrm{(cm/s)}$', fontsize=18)
                plt.tick_params(labelsize=18)

                plt.savefig(projection_path % (run_name, background_value, timemark) + '%s_pd2_%d.png' % (run_name, 10 * direction), dpi=500, bbox_inches='tight')
                plt.savefig(projection_path % (run_name, background_value, timemark) + '%s_pd2_%d.eps' % (run_name, 10 * direction), bbox_inches='tight')
                plt.close()