import numpy as np
from mpi4py import MPI
import yt
from extract_projections import mkdir

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank   = comm.Get_rank()

run1 = {'Name':'T0.3_v1000_chi300',
    'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
    'Mach':3.8,
    'tcc':1.7,
    'velocity':1000,
    'f_list':['0025', '0033', '0042', '0058']}

run2 = { 'Name':'T0.3_v1000_chi300_cond',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':3.8,
        'tcc':1.7,
        'velocity':1000,
        'f_list':['0013', '0038', '0080', '0132']}

run3 = { 'Name':'T0.3_v1700_chi300_cond',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper2/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0003', '0020', '0046', '0078']}

run4 = { 'Name':'T0.3_v1700_chi300',
        'Dir':'/nas/astro-th/lyang/GiantDrive1/Blob_paper1/Files/',
        'Mach':6.5,
        'tcc':1.0,
        'velocity':1700,
        'f_list':['0022', '0032', '0053', '0085']}


runlist = []
runlist.append(run1)
runlist.append(run2)
runlist.append(run3)
runlist.append(run4)

rlist = np.linspace(0, 1, num=11)
theta_list = np.arccos(rlist)

def get_column_density(snapshot, theta, boxsize_pc, Npix):
    projected_box = [boxsize_pc * yt.units.pc, boxsize_pc * yt.units.pc, boxsize_pc * yt.units.pc]
    data = yt.load(snapshot)
    allDataRegion = data.all_data()
    data_center = allDataRegion.quantities.center_of_mass()

    cloudRegion = allDataRegion.cut_region(['obj["blob"] >= %.2f' % 0.825])
    los = [np.sin(theta), np.cos(theta), 0] #The relative velocity of the cloud turns out to the in the y direction
    colden = yt.off_axis_projection(cloudRegion, data_center, los, projected_box, Npix, 'density', no_ghost=False, north_vector=[0, 0, 1]).to('g/cm**2')
    colden = np.array(np.rot90(colden, k=3))
    return colden

if __name__ == '__main__':
    Ncomp = len(runlist) * len(theta_list)
    if rank >= Ncomp:
        exit(0)
    else:
        for run in runlist[int(rank / len(theta_list))::int(nprocs / len(theta_list))]:
            theta = theta_list[rank % len(theta_list)]
            r = rlist[rank % len(theta_list)]
            directory = run['Dir']
            run_name = run['Name']
            for i in range(len(run['f_list'])):
                snapnum = run['f_list'][i]
                save_path = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/%s/mass_distribution/t%d/' % (run_name, i)
                mkdir(save_path)

                colden = get_column_density(directory + run_name + '/KH_hdf5_chk_' +  snapnum, theta, 800, 400)
                np.savetxt(save_path + run_name + '_%d.csv' % (10 * r), colden.flatten(), fmt='%.5e')
