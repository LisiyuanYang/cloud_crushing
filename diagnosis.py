from turtle import back
import numpy as np

projection_base = '/work/lyang_umass_edu/nonSorted_ColDen/Projection_Database/Projections/T0.3_v1000_chi300_cond/HM_1e%d/TF%.1f/blob0.825/T0.3_v1000_chi300_cond_colden_%d.csv'
direction_list = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
TF_list = [1.0, 2.0, 3.0]

f = open('diagnosis.txt', 'w')

for background_value in range(8):
    for temperature_floor in TF_list:
        for direction in direction_list:
            data = np.loadtxt(projection_base % (background_value, temperature_floor, direction), skiprows=1, delimiter=',')
            maxline = data[np.argmax(data[:, 6]), 6]
            print(background_value, temperature_floor, direction, np.argmax(data[:, 6]), maxline, file=f)
f.close()
