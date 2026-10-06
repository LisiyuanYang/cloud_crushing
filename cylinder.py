import numpy as np

def cylinder_pathlen(radius, length, impact_parameter, theta, x): #x: uniform random number between 0 and 1
    if theta > np.pi / 2 or theta < 0:
        exit(1)
    
    if x < 0 or x > 1:
        exit(1)

    width = 2 * np.sqrt(radius ** 2 - impact_parameter ** 2)

    if theta >= np.arctan(width / length):
        tol_len = length + width / np.tan(theta)
        if x * tol_len <= width / np.tan(theta):
            return x * tol_len / np.cos(theta)
        elif x * tol_len <= length:
            return width / np.cos(theta)
        else:
            return (1 - x) * tol_len / np.cos(theta)
    
    else:
        phi = np.pi / 2 - theta
        tol_len = width + length / np.tan(phi)
        if x * tol_len <= length / np.tan(phi):
            return x * tol_len / np.cos(phi)
        elif x * tol_len <= width:
            return length / np.cos(phi)
        else:
            return (1 - x) * tol_len / np.cos(phi)

