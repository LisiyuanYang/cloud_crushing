import numpy as np
from matplotlib import pyplot as plt

ions = ['H I 1215', 'C IV', 'O IV', 'Mg II']
ion_weights = [1, 12, 16, 24]

unit_M = 1.23271e+49
unit_L = 1.10214e+26
MHYDR = 1.6726e-24

unit_col = unit_M / unit_L ** 2
colors = ['blue', 'red', 'green', 'orange', 'cyan', 'orange', 'pink']

def read_cloud(cloudszfile):
    raw = np.loadtxt(cloudszfile, usecols=(1, 2, 3, 7))
    raw_HI = raw[::4]
    raw_CIV = raw[1::4]
    raw_OIV = raw[2::4]
    raw_MgII = raw[3::4]
    return raw_HI, raw_CIV, raw_OIV, raw_MgII

if __name__ == '__main__':
    model = 'l25n288-phew-m5'
    angles = np.arange(10, 81)
    cloudszfile_base = '/work/lyang_umass_edu/los/%s/z2.1/cloudszfile.%s.%d.210_0'
    raw_HI = []
    raw_CIV = []
    raw_OIV = []
    raw_MgII = []

    for angle in angles:
        print('\r%d' % angle, end='\r')
        raws = read_cloud(cloudszfile_base % (model, model, angle))
        raw_HI.append(raws[0])
        raw_CIV.append(raws[1])
        raw_OIV.append(raws[2])
        raw_MgII.append(raws[3])
    
    raw_HI = np.concatenate(raw_HI, axis=0)
    raw_CIV = np.concatenate(raw_CIV, axis=0)
    raw_OIV = np.concatenate(raw_OIV, axis=0)
    raw_MgII = np.concatenate(raw_MgII, axis=0)

    log_scaling_factors_HI = np.log10(raw_HI[:, 3])
    log_scaling_factors_CIV = np.log10(raw_CIV[:, 3] * raw_CIV[:, 2])
    log_scaling_factors_OIV = np.log10(raw_OIV[:, 3] * raw_OIV[:, 2])
    log_scaling_factors_MgII = np.log10(raw_MgII[:, 3] * raw_MgII[:, 2])

    raw_HI[:, 1] += np.log10(unit_col / (ion_weights[0] * MHYDR))
    raw_CIV[:, 1] += np.log10(unit_col / (ion_weights[1] * MHYDR) * raw_CIV[:, 2])
    raw_OIV[:, 1] += np.log10(unit_col / (ion_weights[2] * MHYDR) * raw_OIV[:, 2])
    raw_MgII[:, 1] += np.log10(unit_col / (ion_weights[3] * MHYDR) * raw_MgII[:, 2])
    
    

    valid_absorbers = np.where((raw_CIV[:, 1] > 12) | (raw_OIV[:, 1] > 12) | (raw_MgII[:, 1] > 12))[0]

    plt.figure(figsize=(16, 3), dpi=300)
    ax = plt.subplot(1, 4, 1)
    ax.hist(log_scaling_factors_HI[valid_absorbers], histtype='step', bins=75, range=(-5.5, 0), density=True, color=colors[0], label='H I')
    ax.hist(log_scaling_factors_CIV[valid_absorbers], histtype='step', bins=75, range=(-5.5, 0), density=True, color=colors[1], label='C IV')
    ax.hist(log_scaling_factors_OIV[valid_absorbers], histtype='step', bins=75, range=(-5.5, 0), density=True, color=colors[2], label='O IV')
    ax.hist(log_scaling_factors_MgII[valid_absorbers], histtype='step', bins=75, range=(-5.5, 0), density=True, color=colors[3], label='Mg II')
    ax.set_xlabel('log(scale_factor)')
    ax.legend()

    ax = plt.subplot(1, 4, 2)
    ax.hist(np.log10(raw_CIV[valid_absorbers, 2]), histtype='step', bins=75, range=(-3, 1), density=True, color=colors[1], label='C IV')
    ax.hist(np.log10(raw_OIV[valid_absorbers, 2]), histtype='step', bins=75, range=(-3, 1), density=True, color=colors[2], label='O IV')
    ax.hist(np.log10(raw_MgII[valid_absorbers, 2]), histtype='step', bins=75, range=(-3, 1), density=True, color=colors[3], label='Mg II')
    ax.set_xlabel(r'$\log(Z/Z_{\odot})$')
    #ax.legend()

    ax = plt.subplot(1, 4, 3)
    ax.scatter(raw_CIV[valid_absorbers, 1], np.log10(raw_CIV[valid_absorbers, 2]), alpha=0.7, s=1.2, c=colors[1], label='C IV', rasterized=True)
    ax.scatter(raw_OIV[valid_absorbers, 1], np.log10(raw_OIV[valid_absorbers, 2]), alpha=0.7, s=1.2, c=colors[2], label='O IV', rasterized=True)
    ax.scatter(raw_MgII[valid_absorbers, 1], np.log10(raw_MgII[valid_absorbers, 2]), alpha=0.7, s=1.2, c=colors[3], label='Mg II', rasterized=True)
    ax.set_xlim(12, 15)
    ax.set_ylim(-3, 1)
    ax.set_xlabel(r'$\log(N/cm^{-2})$')
    ax.set_ylabel(r'$\log(Z/Z_{\odot})$')
    #ax.legend()

    ax = plt.subplot(1, 4, 4)
    ax.scatter(raw_CIV[valid_absorbers, 1], log_scaling_factors_CIV[valid_absorbers], alpha=0.7, s=1.2, c=colors[1], label='C IV', rasterized=True)
    ax.scatter(raw_OIV[valid_absorbers, 1], log_scaling_factors_OIV[valid_absorbers], alpha=0.7, s=1.2, c=colors[2], label='O IV', rasterized=True)
    ax.scatter(raw_MgII[valid_absorbers, 1], log_scaling_factors_MgII[valid_absorbers], alpha=0.7, s=1.2, c=colors[3], label='Mg II', rasterized=True)
    ax.set_xlim(12, 15)
    ax.set_ylim(-5.5, 0)
    ax.set_xlabel(r'$\log(N/cm^{-2})$')
    ax.set_ylabel('log(scale_factor)')
    #ax.legend()

    plt.tight_layout()
    plt.savefig('figures/scaling_factors_%s.pdf' % model, bbox_inches='tight')
    plt.clf()
    plt.close()