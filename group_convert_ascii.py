import glob
import os

for folder in glob.glob('/work/pi_nsk_umass_edu/lyang/newTridentTables/HM_shu/hm-1e-100-z0.1006/'):
    runfile_name = glob.glob('*.run', root_dir=folder)[0]
    os.system('cp ./cloudy_ascii_hdf5.py %s' % folder)
    os.system('cp ./convert.py %s' % folder)
    os.system('cd %s\npython convert.py %s %s H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn' % (folder, runfile_name, runfile_name[:-4] + '.h5'))
