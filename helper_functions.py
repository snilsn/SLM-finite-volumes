import numpy as np
from fipy import numerix

def create_dz(n, m, L):
    
    faces = numerix.array([L*(i/n)**m for i in range(n+1)], dtype=object)
    dz = numerix.diff(faces)
    if numerix.absolute(dz.sum() - L) < 1e-3:
        return dz
    else:
        print('error, wrong sum')
        return None
    
def create_dy(n, m, L):
    
    if n % 2 == 1:
        print('please use an even number of cells in the y dimension')
        return None
    
    faces1 = numerix.array([L/2*(i/round(n/2))**m for i in range(round(n/2)+1)], dtype=object)
    faces2 = L - faces1
    faces2.sort()
    faces2 = faces2[1:]

    faces = numerix.concatenate((faces1, faces2))
    dy = numerix.diff(faces)
    
    print(dy.sum())
    print(L)
    if numerix.absolute(dy.sum() - L) < 1e-3:
        return dy
    else:
        print('error, wrong sum')
        return None        
