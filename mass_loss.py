import numpy as np
from matplotlib import pyplot as plt
from cloud_util import runs


runlist = []
##add only the 3 different conduction levels

#runlist.append(runs['run4'])    #T0.3_v1000_chi300
#runlist.append(runs['runx2'])   #T0.3_v1000_chi300_ld2
#runlist.append(runs['run1'])   #T0.3_v1000_chi300_cond
#runlist.append(runs['runx14'])   #T0.3_v1000_chi300_cond_0.1_ld2
#runlist.append(runs['runx8'])   #T0.3_v1000_chi300_cond_ld2

#runlist.append(runs['run16'])  #T0.3_v1700_chi300
#runlist.append(runs['runx4'])   #T0.3_v1700_chi300_ld2
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
#runlist.append(runs['runa1'])   #T0.3_v1700_chi300_apk
#runlist.append(runs['runp1'])
#runlist.append(runs['runp1'])
#runlist.append(runs['runp2'])
#runlist.append(runs['runp3'])
#runlist.append(runs['runp4'])
#runlist.append(runs['runp5'])
#runlist.append(runs['runp6'])
#runlist.append(runs['runp7'])
#runlist.append(runs['runp8'])
#runlist.append(runs['runp9'])
#runlist.append(runs['runp10'])
#runlist.append(runs['runp11'])
#runlist.append(runs['runp12'])
#runlist.append(runs['runp13'])
#runlist.append(runs['runp14'])
#runlist.append(runs['runp15'])
runlist.append(runs['runp9'])
runlist.append(runs['runp9b'])
runlist.append(runs['runp14'])
runlist.append(runs['runp16'])
runlist.append(runs['runp17'])
runlist.append(runs['runp18'])


colors = ['blue', 'cyan', 'green', 'lime', 'red', 'orange', 'magenta', 'brown']
#colors = ['blue', 'green', 'red', 'cyan', 'orange']
linestyles = ['-', '--', ':']
#colors = ['red', 'orange']

if __name__ == '__main__':
    full_mcloud_blobcut_list_1 = []
    full_mcloud_blobcut_list_2 = []
    full_mcloud_densitycut_list = []
    full_time_list = []

    mcloud_blobcut_list_1 = []
    mcloud_blobcut_list_2 = []
    mcloud_densitycut_list = []
    distance_list = []
    velocity_list = []
    time_list = []


    for j in range(len(runlist)):
        run = runlist[j]
        run_name = run['Name']
        directory = run['Dir']

        aux_file = directory + run_name + '/%s.dat' % run_name
        aux_data = np.loadtxt(aux_file, usecols=(1, 2, 3, 4, 8, 10))
        full_timenum_list = np.loadtxt(aux_file, usecols=0, dtype=int)

        timenum_list = np.array(run['f_list'], dtype=int)
        index_list = np.searchsorted(full_timenum_list, timenum_list)

        full_mcloud_blobcut_list_1.append(aux_data[:, 2])
        full_mcloud_blobcut_list_2.append(aux_data[:, 1])
        full_mcloud_densitycut_list.append(aux_data[:, 3])
        full_time_list.append(aux_data[:, 0])

        distance_list.append(aux_data[:, 5])
        velocity_list.append(run['velocity'] - aux_data[:, 4])

        #mcloud_blobcut_list_1.append(aux_data[index_list, 2])
        #mcloud_blobcut_list_2.append(aux_data[index_list, 1])
        #mcloud_densitycut_list.append(aux_data[index_list, 3])
        #time_list.append(aux_data[index_list, 0])

    '''
    run = run16
    run_name = run['Name']
    directory = run['Dir']

    aux_file = directory + run_name + '/%s.dat' % run_name
    aux_data = np.loadtxt(aux_file, usecols=(1, 2, 3))

    old_time_list = aux_data[:, 0]
    old_blobcut_list = aux_data[:, 2]

    run = run11
    run_name = run['Name']
    directory = run['Dir']

    aux_file = directory + run_name + '/%s.dat' % run_name
    aux_data = np.loadtxt(aux_file, usecols=(1, 2, 3))

    old_cond_time_list = aux_data[:, 0]
    old_cond_blobcut_list = aux_data[:, 2]
    '''
    
    plt.figure()
    for j in range(len(runlist)):
        plt.plot(full_time_list[j], full_mcloud_blobcut_list_1[j], c=colors[j], ls='-', label=runlist[j]['Name'])
        plt.plot(full_time_list[j], full_mcloud_blobcut_list_2[j], c=colors[j], ls='--')
        #plt.plot(full_time_list[j], full_mcloud_densitycut_list[j], c=colors[j], ls=':')
        #if 'ld2' in runlist[j]['Name']:
        #    plt.scatter(time_list[j], mcloud_blobcut_list[j], c=colors[j], s=64)
        #plt.scatter(time_list[j], mcloud_densitycut_list[j], c=colors[j], s=12)

    plt.xlim(0, 50)
    plt.legend(fontsize=12)
    plt.gca().add_artist(plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1)))
    h1 = plt.plot([],[], color="blue", ls='-', label=r"$C_{\mathrm{cloud}} > 0.5$")[0]
    h2 = plt.plot([],[], color="blue", ls='--', label=r"$C_{\mathrm{cloud}} > 0.82$")[0]
    #h3 = plt.plot([],[], color="blue", ls=':', label=r'$\rho > \rho_{\mathrm{init}}/3$')[0]
    #plt.legend(handles=[h1, h2, h3], fontsize=12)
    plt.legend(handles=[h1, h2], fontsize=12)
    #h1 = plt.plot([],[], color="black", ls=linestyles[0], label='None')[0]
    #h2 = plt.plot([],[], color="black", ls=linestyles[1], label='Weak')[0]
    #h3 = plt.plot([],[], color="black", ls=linestyles[2], label='Full')[0]
    plt.xlabel(r'$t/t_\mathrm{cc}$', fontsize=12)
    #plt.xlabel('snapnum', fontsize=13)
    plt.ylabel(r'$M/M_\mathrm{init}$', fontsize=12)
    plt.tick_params(which='both', direction='in', right=True, top=True, labelsize=12)
    plt.savefig('figures/mass_loss_%s.pdf' % runlist[-1]['Name'], bbox_inches='tight')
    plt.close()
    
    plt.figure()
    for j in range(len(runlist)):
        plt.plot(full_time_list[j], distance_list[j], c=colors[j], ls='-', label=runlist[j]['Name'])
        #plt.plot(full_time_list[j], full_mcloud_densitycut_list[j], c=colors[j], ls=':')
        #if 'ld2' in runlist[j]['Name']:
        #    plt.scatter(time_list[j], mcloud_blobcut_list[j], c=colors[j], s=64)
        #plt.scatter(time_list[j], mcloud_densitycut_list[j], c=colors[j], s=12)

    plt.xlim(0, 50)
    plt.legend(fontsize=12)
    plt.gca().add_artist(plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1)))
    #h1 = plt.plot([],[], color="black", ls=linestyles[0], label='None')[0]
    #h2 = plt.plot([],[], color="black", ls=linestyles[1], label='Weak')[0]
    #h3 = plt.plot([],[], color="black", ls=linestyles[2], label='Full')[0]
    plt.xlabel(r'$t/t_\mathrm{cc}$', fontsize=12)
    #plt.xlabel('snapnum', fontsize=13)
    plt.ylabel(r'$d/\mathrm{kpc}$', fontsize=12)
    plt.tick_params(which='both', direction='in', right=True, top=True, labelsize=12)
    plt.savefig('figures/distance_%s.pdf' % runlist[-1]['Name'], bbox_inches='tight')
    plt.close()

    plt.figure()
    for j in range(len(runlist)):
        plt.plot(full_time_list[j], velocity_list[j], c=colors[j], ls='-', label=runlist[j]['Name'])
        #plt.plot(full_time_list[j], full_mcloud_densitycut_list[j], c=colors[j], ls=':')
        #if 'ld2' in runlist[j]['Name']:
        #    plt.scatter(time_list[j], mcloud_blobcut_list[j], c=colors[j], s=64)
        #plt.scatter(time_list[j], mcloud_densitycut_list[j], c=colors[j], s=12)

    plt.xlim(0, 50)
    plt.legend(fontsize=12)
    plt.gca().add_artist(plt.legend(fontsize=12, loc='upper left', bbox_to_anchor=(1, 1)))
    #h1 = plt.plot([],[], color="black", ls=linestyles[0], label='None')[0]
    #h2 = plt.plot([],[], color="black", ls=linestyles[1], label='Weak')[0]
    #h3 = plt.plot([],[], color="black", ls=linestyles[2], label='Full')[0]
    plt.xlabel(r'$t/t_\mathrm{cc}$', fontsize=12)
    #plt.xlabel('snapnum', fontsize=13)
    plt.ylabel(r'$v/\mathrm{km/s}$', fontsize=12)
    plt.tick_params(which='both', direction='in', right=True, top=True, labelsize=12)
    plt.savefig('figures/velocity_%s.pdf' % runlist[-1]['Name'], bbox_inches='tight')
    plt.close()
    '''
    plt.figure(figsize=(8, 5))
    for j in range(5):
        if j < 2:
            ax = plt.subplot(3, 3, j + 1)
        else:
            ax = plt.subplot(3, 3, j + 2)

        ax.plot(full_time_list[3 * j], full_mcloud_blobcut_list_2[3 * j], c=colors[0])
        ax.plot(full_time_list[3 * j + 1], full_mcloud_blobcut_list_2[3 * j + 1], c=colors[1])
        ax.plot(full_time_list[3 * j + 2], full_mcloud_blobcut_list_2[3 * j + 2], c=colors[2])
        ax.set_xlim(0, 25)
        ax.set_ylim(0, 1)
        if j >= 3:
            ax.set_xlabel(r'$t/t_{\mathrm{cc}}$', fontsize=12)
        else:
            ax.set_xticklabels([])
        if j == 0 or j == 2:
            ax.set_ylabel(r'$M/M_{\mathrm{init}}$', fontsize=12)
        else:
            ax.set_yticklabels([])
        ax.set_title(runlist[3 * j]['Formal_name'] + ' ', fontsize=11, y=0.8, loc='right')
        if j == 4:
            h1 = ax.plot([],[], c=colors[0], label='None')[0]
            h2 = ax.plot([],[], c=colors[1], label='Weak')[0]
            h3 = ax.plot([],[], c=colors[2], label='Full')[0]
            ax.legend(handles=[h1, h2, h3], title='Conduction:', loc='lower right', fontsize=10)
        
        ax.set_yticks([0.25, 0.5, 0.75])
        ax.tick_params(which='both', direction='in', right=True, top=True, labelsize=10)
    
    ax = plt.subplot(3, 3, 3)
    ax.plot(old_time_list, old_blobcut_list, c=colors[0])
    ax.plot(old_cond_time_list, old_cond_blobcut_list, c=colors[2])
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 1)
    ax.set_title(run16['Formal_name'] + ' ', fontsize=11, y=0.8, loc='right')
    #ax.set_xlabel(r'$t/t_{\mathrm{cc}}$', fontsize=10)
    #ax.set_ylabel(r'$M/M_{\mathrm{init}}$', fontsize=10)
    ax.set_yticks([0.25, 0.5, 0.75])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.tick_params(which='both', direction='in', right=True, top=True, labelsize=10)

    for j in range(1):
        ax = plt.subplot(3, 3, j + 7)

        ax.plot(full_time_list[2 * j + 15], full_mcloud_blobcut_list_2[2 * j + 15], c=colors[0])
        ax.plot(full_time_list[2 * j + 16], full_mcloud_blobcut_list_2[2 * j + 16], c=colors[1])
        ax.set_xlim(0, 25)
        ax.set_ylim(0, 1)
        ax.set_xlabel(r'$t/t_{\mathrm{cc}}$', fontsize=12)
        if j == 0 or j == 2:
            ax.set_ylabel(r'$M/M_{\mathrm{init}}$', fontsize=12)
        else:
            ax.set_yticklabels([])
        ax.set_title(runlist[2 * j + 15]['Formal_name'] + ' ', fontsize=11, y=0.8, loc='right')        
        ax.set_yticks([0.25, 0.5, 0.75])
        ax.tick_params(which='both', direction='in', right=True, top=True, labelsize=10)

    plt.subplots_adjust(wspace=0.05, hspace=0.05)
    #plt.tight_layout()
    plt.savefig('figures/mass_loss_%s.pdf' % runlist[-1]['Name'], bbox_inches='tight')
    plt.close()
    '''
    
