import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank   = comm.Get_rank()

if __name__ == '__main__':
    if rank == 0:
        data = (1, 2, 'ab', np.array([1, 2, 3]))
    else:
        data = None
    data = comm.bcast(data, root=0)
    print('received:', data)
    print('modified:', data[-1] * 2)
