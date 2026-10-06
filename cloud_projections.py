import numpy as np
from matplotlib import pyplot as plt

cloud_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/T0.3_v1000_chi300/HM_1e4/TF1.0/T5.0_rho3.3/T0.3_v1000_chi300_colden_%d.csv'
blob_file = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/T0.3_v1000_chi300/HM_1e4/TF1.0/blob%s/T0.3_v1000_chi300_colden_%d.csv'

pix = 400

if __name__ == '__main__':
    blob_cut = 0.825
    direction = 1.0

    pixels = np.zeros(pix ** 2, dtype=int)
    cloud_region = np.loadtxt(cloud_file % (10 * direction), dtype=int, delimiter=',', usecols=0, skiprows=1)
    blob_region = np.loadtxt(blob_file % (str(blob_cut), 10 * direction), dtype=int, delimiter=',', usecols=0, skiprows=1)
    overlap_region = np.intersect1d(cloud_region, blob_region)

    unique_cloud_region = np.setdiff1d(cloud_region, overlap_region, assume_unique=True)
    unique_blob_region = np.setdiff1d(blob_region, overlap_region, assume_unique=True)

    pixels[unique_blob_region] = 1
    pixels[unique_cloud_region] = 2
    pixels[overlap_region] = 3

    pixels.shape = (pix, pix)

    plt.figure()
    plt.pcolormesh(2 * np.arange(pix + 1), 2 * np.arange(pix + 1), pixels, rasterized=True)
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=14)
    plt.xlabel('x/pc', fontsize=14)
    plt.ylabel('y/pc', fontsize=14)
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.title(r'1: $C_{\mathrm{cloud}}$ > %s, 2: T5.0_rho3.3, 3: overlapped' % str(blob_cut), fontsize=14)
    plt.savefig('figures/cloud_projections_blob%s_%d.png' % (str(blob_cut), 10 * direction), dpi=400)
    plt.savefig('figures/cloud_projections_blob%s_%d.eps' % (str(blob_cut), 10 * direction), bbox_inches='tight')
    plt.clf()
    plt.close()