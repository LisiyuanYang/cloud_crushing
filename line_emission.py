import numpy as np
from cloud_util import Upsi_g_temp_list

def get_Upsi_g(ion, temp):
    ref_Upsi_g = ion['Upsi_g']
    return np.interp(np.log10(temp), Upsi_g_temp_list, ref_Upsi_g)

def get_sigma_v(ion, temp, wavelength):#temp should be in K, wavelength should be in angstroms and the result is in cm^3/s
    Upsi_g = get_Upsi_g(ion, temp)
    return 8.538e-6 * Upsi_g / (temp ** 0.5) * np.exp(-1.43878e8 / (wavelength * temp))

def get_emission_individual(ion, temp, wavelength, n_ion, mH, electron_abundance, Bfactor=1):#divide this by A_pixel (in kpc^2) to get the intensity (in cm^-2 s^-1 arcsec^-2)
    sigma_v = get_sigma_v(ion, temp, wavelength)
    return 233.5 * Bfactor * sigma_v * n_ion * mH * electron_abundance

def get_emission_intensity(ion, temp, wavelength, n_ion, mH, electron_abundance, area=1, Bfactor=1): #mH should be in solarmass and area should be in kpc^2
    sigma_v = get_sigma_v(ion, temp, wavelength)
    return 233.5 * Bfactor * np.sum(sigma_v * n_ion * mH * electron_abundance) / area

