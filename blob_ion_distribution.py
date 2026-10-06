import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import yt

ion_list = ['H I', 'He II', 'C II', 'C III', 'C IV', 'O IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII', 'Mg II', 'Si II', 'Si III', 'Si IV']
#ion_list = ['H I 1215', 'He II', 'Mg II', 'C III', 'C IV', 'O VI', 'O VII', 'O VIII', 'Ne VIII']
included = [0, 1, 10, 3, 4, 6, 7, 8, 9] #indices of the ions included
blob_cut_list = [0.8, 0.825, 0.85, 0.875, 0.9]

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


data_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e2/TF1.0/%s_colden_%d.csv'
cloud_data_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e2/TF1.0/T5.0_rho3.3/%s_colden_%d.csv'
blob_data_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/HM_1e2/TF1.0/blob%s/%s_colden_%d.csv'

if __name__ == '__main__':
    for run in runlist:
        run_name = run['Name']
        direction = 0.0
        coldens = {'all': np.loadtxt(data_file % (run_name, run_name, 10 * direction), delimiter=',', skiprows=1)}
        mass_fractions = {}

        data = yt.load(run['Dir'] + run['Name'] + '/KH_hdf5_chk_' + run['f_list'][3])
        allDataRegion = data.all_data()
        blobs = allDataRegion["blob"].value

        #read the column density and mass fraction of T5.0_rho3.3
        cloudRegion = allDataRegion.cut_region(['obj["density"] >= 3.33e-25']).cut_region(['obj["temperature"] <= 5e4'])
        mass_fractions['T5.0_rho3.3'] = cloudRegion.quantities.total_mass()[0] / (1.23e38 * yt.units.g)

        blobs_cloud = cloudRegion["blob"].value

        coldens['T5.0_rho3.3'] = \
            np.loadtxt(cloud_data_file % (run_name, run_name, 10 * direction), delimiter=',', skiprows=1) / 100

        for blob_cut in blob_cut_list:
            cloudRegion = allDataRegion.cut_region(['obj["blob"] >= %s' % str(blob_cut)])
            mass_fractions['blob%s' % str(blob_cut)] = cloudRegion.quantities.total_mass()[0] / (1.23e38 * yt.units.g)

            coldens['blob%s' % str(blob_cut)] = \
                np.loadtxt(blob_data_file % (run_name, str(blob_cut), run_name, 10 * direction), delimiter=',', skiprows=1) / 100
        
        plt.figure()
        bins = plt.hist(blobs, histtype='step', bins=25, label='all')[1]
        plt.hist(blobs_cloud, histtype='step', bins=bins, label='T5.0_rho3.3')
        plt.yscale('log')
        plt.xlabel(r'$C_{\mathrm{cloud}}$')
        plt.legend()
        plt.savefig('figures/blob_dist_%s.jpg' % run_name, dpi=400)
        plt.savefig('figures/blob_dist_%s.eps' % run_name, bbox_inches='tight')
        plt.close()

        fig, axs = plt.subplots(3, 3, figsize=(15, 5))
        axs = axs.flatten()
        for iteration, i in enumerate(included):
            colden_ion = coldens['all'][:, i+1]
            ax = axs[iteration]
            #bins = np.histogram(np.log10(colden_ion), range=[12, np.log10(max(colden_ion))],bins=80)[1]
            bins = ax.hist(np.log10(colden_ion), range=[12, np.log10(max(colden_ion))], histtype='step', bins=80, label='all')[1]
            
            colden_cloud_ion = coldens['T5.0_rho3.3'][:, i+1]
            mass_fraction = mass_fractions['T5.0_rho3.3'].value
            ax.hist(np.log10(colden_cloud_ion), histtype='step', bins=bins, label='T5.0_rho3.3, %.1f%%' % (100 * mass_fraction))
            for blob_cut in blob_cut_list:
                colden_cloud_ion = coldens['blob%s' % str(blob_cut)][:, i+1]
                mass_fraction = mass_fractions['blob%s' % str(blob_cut)].value
                ax.hist(np.log10(colden_cloud_ion), histtype='step', bins=bins, label=r'$C_{\mathrm{cloud}}>$%s, %.1f%%' % (str(blob_cut), 100 * mass_fraction))
                #ax.hist(np.log10(colden_cloud_ion), histtype='step', bins=bins, color='black')
            ax.set_xlabel(r'$\log(N/\mathrm{cm^{-2}})$', fontsize=14)
            ax.tick_params(axis='both', which='major',direction='in', labelsize=14)
            ax.set_yscale('log')
            #ax.legend()
            ax.set_title(ion_list[i], fontsize = 14)
            handles, labels = ax.get_legend_handles_labels()

        fig.legend(handles, labels, loc="upper left")
        fig.tight_layout()
        fig.savefig('figures/blob_separation_%s_%d.jpg' % (run_name, 10 * direction), dpi=400)
        fig.savefig('figures/blob_separation_%s_%d.pdf' % (run_name, 10 * direction), bbox_inches='tight')
        #fig.show()
        fig.clf()