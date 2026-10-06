import sys
from mpi4py import MPI
import yt
import numpy as np
import trident as tri
import matplotlib.pyplot as plt
from matplotlib import cm
#import subprocess
from yt.data_objects.particle_filters import add_particle_filter
import h5py
from yt.units import centimeter, gram, second, Kelvin, erg, parsec
import os
import sqlite3
import math
import io
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory's path
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from cloud_util import runs, ions

comm = MPI.COMM_WORLD
nprocs = comm.Get_size()
rank   = comm.Get_rank()

#yt.enable_parallelism()

#### Parameters ####
blob_cut = 0.
#blob_cut = 0.5
back_base = 'HM_1e%d'
ionTable_base = '/work/pi_nsk_umass_edu/lyang/newTridentTables/Cloudy23/hm-1e%d-z%g/HM_1e%d.h5'
dbname_base = '/scratch/workspace/lyang_umass_edu-cloud_crushing/data_bases/coldens_new_varz.db'
makeTable = True
singleFile = False

#density_cut_list = [1, 3.33, 10] #*1e-25 g/cm^3
#temperature_cut_list = [2, 3, 5] #*1e4 K

#density_cut = 3.33
#temperature_cut = 5

#blob_list = [0.825]
#blob_cut = 0.825

#constans
kpc = 3.086e+21*centimeter
c_speed = 3.0e10  #cm/s
mp = 1.6726e-24*gram #grams
kb = 1.3806e-16*erg/Kelvin   #egs/K
tempfloor = float(sys.argv[1])
todo_list_file = sys.argv[2]
if len(sys.argv) > 3:
    startline = int(sys.argv[3])
else:
    startline = 0

#extended_radius = 4 * parsec

#add metallicity to dataset, constant Z = 1 Zsun
def _metallicity(field, data):
    factor = 1.0 # 1.0 solar metallicity
    return (
        data.ds.arr(np.ones_like(data["gas", "density"]), 'Zsun') * factor
    )

def _metallicity_variable(field, data):
    return (
        data.ds.arr(np.array(data["flash", "metl"]), 'Zsun')
    )

def _altTemp(field, data):
    temp = data['temperature']
    lowtemps = np.where(temp < tempfloor * 1e4)
    temp[lowtemps] = tempfloor * 1e4   #sets all temps below tempfloor * 1e4 to tempfloor * 1e4
    return temp

def iscloud(field, data, cloudRegion, extended_radius):
    xlist = data['gas', 'x']
    ylist = data['gas', 'y']
    zlist = data['gas', 'z']
    #temp = data['temperature']

    xlist_cloud = cloudRegion['gas', 'x']
    ylist_cloud = cloudRegion['gas', 'y']
    zlist_cloud = cloudRegion['gas', 'z']

    result = np.zeros_like(xlist)
    for i in range(len(xlist_cloud)):
        inr = np.where((xlist_cloud[i] - xlist) ** 2 + (ylist_cloud[i] - ylist) ** 2 + (zlist_cloud[i] - zlist) ** 2 <= extended_radius ** 2)
        result[inr] = 1
    return result * yt.units.dimensionless

def adapt_array(arr):
    #http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

#function to determine the velocity of the cloud for a particular run
#will return an array of velocities (km/s) for the appropriate velocity bins to use
#in the observational data.
def findCloudVel(directory, runName, f_list, density_cut, temperature_cut):
    velList = []
    velFrames = []
    for i in f_list:
        data = yt.load(directory+runName+'/KH_hdf5_chk_'+i)
        allDataRegion = data.all_data()
        cloudRegion = allDataRegion.cut_region(['obj["density"] >= %.2fe-25' % density_cut]).cut_region(['obj["temperature"] <= %.2fe4' % temperature_cut])
        avg_vy_cloud = cloudRegion.quantities.weighted_average_quantity('vely', 'ones') #vely is the velocity in the radial direction (towards/away obs)

        #need to add the frame velocity!
        #get the frame velocity
        f = h5py.File(directory+runName+'/KH_hdf5_chk_'+i, 'r')
        velframe = f['real scalars'][7][1] #cm/s
        velFrames.append(velframe/1.0e5) #append frame vel in km/s
        f.close()

        vy_cloud = (avg_vy_cloud.value+velframe)/1.0e5  #convert to km/s
        velList.append(vy_cloud)

    #print('Frame vels:')
    #print(velFrames)
    #print('Cloud vels:')
    #print(velList)
    return velList, velFrames

def fatten(data, region, radius): #expand a region outwards by a specific distance (radius)
    xlist = region['gas', 'x']
    ylist = region['gas', 'y']
    zlist = region['gas', 'z']

    expanded_region_list = []

    for i in range(len(xlist)):
        center = (xlist[i], ylist[i], zlist[i])
        expanded_region_list.append(data.sphere(center, radius))

    print('combined %d regions' % len(xlist))
    return data.union(expanded_region_list)

#given one data file sphere size, and an ion, return average absorption  (given velocity in km/s)
def calcRankCol(run, velocityBin, HM_index, blob_cut, redshift, r, ion):
    directory = run['Dir']
    runName = run['Name']
    runNumber = run['f_list'][velocityBin]
    back = back_base % HM_index
    ionTable = ionTable_base % (HM_index, redshift, HM_index)
    
    #load and add ions to the dataset
    #frameVel = frameVel*1.0e5*(centimeter/second)  #convert to cm/s

    data = yt.load(directory+runName+'/KH_hdf5_chk_'+runNumber)
    allDataRegion = data.all_data()
    #cloudRegion = allDataRegion.cut_region(['obj["density"] >= %.2fe-25' % density_cut]).cut_region(['obj["temperature"] <= %.2fe4' % temperature_cut])
    cloudRegion = allDataRegion.cut_region(['obj["blob"] >= %g' % blob_cut])

    #_iscloud = lambda field, data : iscloud(field, data, cloudRegion, extended_radius)
    #data.add_field(('gas', 'iscloud'), function=_iscloud, sampling_type='cell', force_override=True)
    #cloud_extended = allDataRegion.cut_region(['obj["gas", "iscloud"] > 0'])
    #print(len(cloudRegion['gas', 'x']))
    #print(len(cloud_extended['gas', 'x']))

    #print("starting...")
    #data.add_field(('gas', 'metallicity'), function=_metallicity, sampling_type='cell', display_name='Metallicity', units='Zsun')
    data.add_field(('gas', 'metallicity'), function=_metallicity_variable, sampling_type='cell', display_name='Metallicity', units='Zsun')
    data.add_field(('gas', 'temperature_alt'), function=_altTemp, sampling_type='cell', units='K', display_name = 'Temperature Alt')
    #connect to database
    #cursor = conn.cursor()

    #make temperature maps
    #select entire region
    #reg = data.all_data()

    #find center
    #c = allDataRegion.quantities.center_of_mass() #Can avoid cutting off the tail
    c = data.domain_center #Can avoid cutting off the tail

    vx_c = cloudRegion.quantities.weighted_average_quantity('velocity_x', weight='cell_mass')
    vy_c = cloudRegion.quantities.weighted_average_quantity('velocity_y', weight='cell_mass')

    #widths [right-left, top-bot, front-back] in code units
    #W = [2.468e21, 2.468e21, 2.468e21] #800 pc
    #W = [1.234e22, 1.234e22, 1.234e22] #4 kpc
    W=[12 * run['radius'] * yt.units.pc] * 3
    #set pixels along one edge
    pix = 600
    tri.add_ion_fields(data, ions=[ion['ion']], ionization_table=ionTable)

    #add ion fields to the dataset
    #loop through angles;
    #for y proj: r = 0
    #for x proj: r = 1

    #print('started:', runName, HM_index, ion['ion'], r, v, redshift)
    a = math.acos(r)
    #a = d*math.pi/180.
    N = [math.sin(a), math.cos(a), 0]#It happens that y is the direction of the ambient velocity.
    los_vel_c = (vx_c * N[0] + vy_c * N[1]).to('cm/s').value

    _los_velocity = lambda field, data : (data['velocity_x'] * N[0] + data['velocity_y'] * N[1]) * data[ion['fieldname']]
    _los_velocity_2 = lambda field, data : (data['velocity_x'] * N[0] + data['velocity_y'] * N[1]) ** 2 * data[ion['fieldname']]
    #These are not really los_velocity or los_velocity**2. The extra factor of ion_density is added because the weight function does not work properly with them.
    data.add_field(("gas", "los_velocity"), function=_los_velocity, sampling_type='cell', units='cm**-2/s', force_override=True)
    data.add_field(("gas", "los_velocity_2"), function=_los_velocity_2, sampling_type='cell', units='cm**-1/s**2', force_override=True)
    

    temp = yt.off_axis_projection(cloudRegion, c, N, W, pix, 'temperature', weight=ion['fieldname'], no_ghost=False, north_vector=[0, 0, 1])
    temp = np.array(np.rot90(temp, k=3))

    frb = yt.off_axis_projection(cloudRegion, c, N, W, pix, ion['fieldname'], no_ghost=False, north_vector=[0, 0, 1])
    frb = np.array(np.rot90(frb, k=3))

    los_vel = yt.off_axis_projection(cloudRegion, c, N, W, pix, ("gas", "los_velocity"), no_ghost=False, north_vector=[0, 0, 1])
    los_vel = np.array(np.rot90(los_vel, k=3)) / frb

    #print(los_vel)

    los_vel_2 = yt.off_axis_projection(cloudRegion, c, N, W, pix, ("gas", "los_velocity_2"), no_ghost=False, north_vector=[0, 0, 1])
    los_vel_2 = np.array(np.rot90(los_vel_2, k=3)) / frb
    #print(los_vel_2)
    #print(np.sqrt(np.average(los_vel_2, weights=frb) - np.average(los_vel, weights=frb)**2))
    
    bt2 = 1.6509e8 * temp / ion['massNum']
    bd2 = los_vel_2 - los_vel**2
    #print(bd2)
    b = np.sqrt(bt2 + 2 * bd2)
    bt = np.sqrt(bt2)
    bd = np.sqrt(bd2) #Note that bd is 1/sqrt(2) times the actual kinematic broadening. It is corrected in extract_projections.py

    los_vel -= los_vel_c

    #code to plot frb if you'd like to look at it for troubleshooting purposes
    #fig, ax = plt.subplots()
    #cax = ax.matshow(np.log10(frb), interpolation='nearest', cmap=cm.get_cmap('viridis'))
    #cbar = fig.colorbar(cax)
    #fig.savefig('proj'+ion['ion']+str(r)+'.png')


    #flatten the frb to a 1d array
    flattened_num = frb.flatten()
    projectedNum = flattened_num
    projectedWidth = b.flatten()
    projectedThermalWidth = bt.flatten()
    projectedDopplerWidth = bd.flatten()
    los_vel = los_vel.flatten()

    data_package = (projectedNum, projectedWidth, projectedThermalWidth, projectedDopplerWidth, los_vel, ion['ion'], runName, str(r), str(blob_cut), str(tempfloor), back, velocityBin, str(redshift))
    #print('finished computing:', runName, HM_index, ion['ion'], r, v, redshift)
    #conn.commit()
    #conn.close()
    return data_package

#make tables for the database;
## !! Deletes existing tables if already defined!! ##
#fills the run table
def makeTables(conn, run_list):
    cursor = conn.cursor()
    #cursor.execute("""DROP TABLE IF EXISTS proj;""")
    create_proj = """CREATE TABLE IF NOT EXISTS proj (
    ion TEXT,
    coldens array,
    width array,
    width_thermal array,
    width_doppler array,
    los_vel array,
    background TEXT,
    direction TEXT,
    blob_cut TEXT,
    temp_floor TEXT,
    run_name TEXT NOT NULL,
    redshift TEXT,
    timeNum FLOAT,
    PRIMARY KEY (run_name, ion, background, direction, blob_cut, temp_floor, redshift, timeNum)
    );"""
    cursor.execute(create_proj)

    #if int((rank % (4 * len(HM_list))) / len(HM_list)) == 0:
    create_run = """ CREATE TABLE IF NOT EXISTS run (
    run_name TEXT,
    mach FLOAT,
    velocity FLOAT,
    tcc FLOAT,
    PRIMARY KEY (run_name)
    );"""
    cursor.execute(create_run)

    for run in run_list:#only need to insert once for each run
        exe_str = "INSERT OR REPLACE INTO run (run_name, mach, velocity, tcc) VALUES(?, ?, ?, ?)"
        exe_param = (run['Name'], run['Mach'], run['velocity'], run['tcc'])
        cursor.execute(exe_str, exe_param)
    
    conn.commit()


def write_projection(conn, data_cluster):
    cursor = conn.cursor()
    for data_package in data_cluster:
        if data_package != None:
            cursor.execute('INSERT OR REPLACE INTO proj (coldens, width, width_thermal, width_doppler, los_vel, ion, run_name, direction, blob_cut, temp_floor, background, timeNum, redshift) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ',\
                            data_package)
    conn.commit()

run_list = [run for run in runs.values()]
ion_list = [ion for ion in ions.values()]

if __name__ == '__main__':

    #other potential runs to use:
    '''
    run6 = { 'Name':'T1_v1700_chi1000_lref4',
                'Dir':'../../Blob_paper1/Files/',
                'Mach':3.5,
                'f_list':['0020', '0030', '0040', '0050']}
    run7 = { 'Name':'T1_v1700_chi1000_lref6',
                'Dir':'../../Blob_paper1/Files/',
                'Mach':3.5,
                'f_list':['0021', '0029', '0038']}
    '''


### dictionaries of ion info

#The real stuff starts here
    if rank == 0:
        sqlite3.register_adapter(np.ndarray, adapt_array)
        # Converts TEXT to np.array when selecting
        sqlite3.register_converter("array", convert_array)

        #conn = sqlite3.connect(dbname_base % tempfloor, detect_types=sqlite3.PARSE_DECLTYPES)
        conn = sqlite3.connect(dbname_base, detect_types=sqlite3.PARSE_DECLTYPES)
        makeTables(conn, run_list)

        with open(todo_list_file) as f:
            todo_list = [line.strip() for line in f]
        
        if startline > 0:
            todo_list = todo_list[startline : ]

    else:
        todo_list = []
    
    todo_list = comm.bcast(todo_list, root=0) #Send todo lists to all processes
    
    Nlines_local = int(np.ceil(len(todo_list) / (nprocs - 1)))

    if rank > 0:
        todo_list_local = todo_list[(rank - 1) : : (nprocs - 1)]
        if len(todo_list_local) < Nlines_local:
            todo_list_local.extend([None] * (Nlines_local - len(todo_list_local)))

    for i in range(Nlines_local):
        if rank > 0:
            command_line = todo_list_local[i]
            if command_line != None:
                elems = command_line.split()
                run_name = elems[0]
                HM_index = int(elems[1])
                ion_name = '%s %s' % (elems[2], elems[3])
                
                #if ion_name == 'H I':
                #    ion_name = 'H I 1215' 
                    #r = float(elems[5])
                    #v = int(elems[6])
                    #redshift = float(elems[7])
                #else:
                r = float(elems[4])
                v = int(elems[5])
                redshift = float(elems[6])

                run = [myrun for myrun in run_list if myrun['Name'] == run_name][0]
                ion = [myion for myion in ion_list if myion['ion'] == ion_name][0]

                tri.ion_balance.table_store = {} #Force trident to reload ionization tables

                #dataframe for a single file
                #unRank = pd.DataFrame()

                #find appropriate velocity bins
                #velBins, velFrames = findCloudVel(run['Dir'], run['Name'], run['f_list'], density_cut, temperature_cut)

                #velocities are in km/s
                #calculate the ranked columns for each ion/velocity bin
                data_package = calcRankCol(run, v, HM_index, blob_cut, redshift, r, ion)
            else:
                data_package = None

        else: #if rank == 0
            data_package = None
        
        data_cluster = comm.gather(data_package, root=0) #After each round, gather all projection data to process 0 and write them to the database. Otherwise, the database might get locked.
        if rank == 0:
            write_projection(conn, data_cluster)
            print('Finished writing: data cluster %d/%d, # of computing processes: %d' % (i + 1, Nlines_local, nprocs - 1), flush=True)
    if rank == 0:
        conn.close()
