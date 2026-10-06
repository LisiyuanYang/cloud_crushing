import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import yt

ion_list = ['H I 1215', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV']
included = [0, 1, 10, 3, 4, 6, 7, 8, 9] #indices of the ions included
density_cut_list = [1, 3.33, 10] #*1e-25 g/cm^3
temperature_cut_list = [2, 3, 5] #*1e4 K

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

runlist = [run4]

data_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e4/TF1.0/%s_colden_%d.csv'
cloud_data_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e4/TF1.0/T%.1f_rho%.1f/%s_colden_%d.csv'

if __name__ == '__main__':
    for run in runlist:
        run_name = run['Name']
        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' + run['f_list'][3])
        allDataRegion = data.all_data()
        cloudRegion_jn = allDataRegion.cut_region(['obj["density"] >= 3.33e-25'])
        mass_fractions = {'all': cloudRegion_jn.quantities.total_mass()[0] / (1.23e38 * yt.units.g)}

        direction = 0.0
        coldens = {'all': np.loadtxt(data_file % (run_name, run_name, 10 * direction), delimiter=',', skiprows=1)}
        for density_cut in density_cut_list:
            for temperature_cut in temperature_cut_list:
                cloudRegion = allDataRegion.cut_region(['obj["density"] >= %.2fe-25' % density_cut]).cut_region(['obj["temperature"] <= %.2fe4' % temperature_cut])
                mass_fractions['T%.1f_rho%.1f' % (temperature_cut, density_cut)] = cloudRegion.quantities.total_mass()[0] / (1.23e38 * yt.units.g)

                coldens['T%.1f_rho%.1f' % (temperature_cut, density_cut)] = \
                    np.loadtxt(cloud_data_file % (run_name, temperature_cut, density_cut, run_name, 10 * direction), delimiter=',', skiprows=1)

        fig, axs = plt.subplots(3, 3, figsize=(15, 5))
        axs = axs.flatten()
        for iteration, i in enumerate(included):
            colden_ion = coldens['all'][:, i+1]
            ax = axs[iteration]
            mass_fraction = mass_fractions['all'].value
            bins = ax.hist(np.log10(colden_ion), range=[12, np.log10(max(colden_ion))], histtype='step', bins=80, label='all, cloud %.1f%%' % (100 * mass_fraction))[1]
            for density_cut in density_cut_list:
                for temperature_cut in temperature_cut_list:
                    colden_cloud_ion = coldens['T%.1f_rho%.1f' % (temperature_cut, density_cut)][:, i+1]
                    mass_fraction = mass_fractions['T%.1f_rho%.1f' % (temperature_cut, density_cut)].value
                    ax.hist(np.log10(colden_cloud_ion), histtype='step', bins=bins, label='T%.1f_rho%.1f, %.1f%%' % (temperature_cut, density_cut, 100 * mass_fraction))
            ax.set_xlabel(r'$\log(N)/\mathrm{cm^{-2}}$')
            ax.set_yscale('log')
            #ax.legend()
            ax.set_title(ion_list[i])
            handles, labels = ax.get_legend_handles_labels()

        fig.legend(handles, labels, loc="upper left")    
        fig.tight_layout()
        fig.savefig('figures/cloud_separation_%s_%d.jpg' % (run_name, 10 * direction), dpi=400)
        fig.savefig('figures/cloud_separation_%s_%d.eps' % (run_name, 10 * direction), bbox_inches='tight')
        #fig.show()
        fig.clf()