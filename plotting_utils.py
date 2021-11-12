from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

def plot_3d_vectorfield(mesh, v_x, v_y, v_z):
    #%matplotlib notebook
    
    mesh_points = numerix.array(mesh.cellCenters).reshape(list(mesh.shape).append(3))
    ax = plt.figure(figsize = (7, 7)).add_subplot(projection='3d')
    plot = ax.quiver(mesh_points[0], mesh_points[1], mesh_points[2], v_x, v_y, v_z, length=0.000001)
    plt.show()
    
    return None

def plot_2d_xy(variable, N):
    
    if N >= variable.mesh.nz:
        print('Value of N too high')
        return None
    
    xy_points = variable.mesh.nx*variable.mesh.ny
    
    mesh_2d = Grid2D(nx = variable.mesh.nx, ny = variable.mesh.ny, dx = variable.mesh.dx, dy = variable.mesh.dy)
    
    view_xy = CellVariable(mesh = mesh_2d, value=numerix.array(variable)[N*xy_points:(N+1)*xy_points])
    viewer = Viewer(vars = [view_xy])
    viewer.fig.set_figheight(10)
    viewer.fig.set_figwidth(10)
    
    return None

def plot_2d_xz(variable, N):
    
    if N >= variable.mesh.ny:
        print('Value of N too high')
        return None
    
    xz_points = variable.mesh.nx*variable.mesh.nz
    mesh_2d = Grid2D(nx = variable.mesh.nx, ny = variable.mesh.nz, dx = variable.mesh.dx, dy = variable.mesh.dz)
    
    variable = np.array(variable).reshape((variable.mesh.nx, variable.mesh.ny, variable.mesh.nz))[:, 0, :]
    
    view_xz = CellVariable(mesh = mesh_2d, value = variable.flatten())
    
    viewer = Viewer(vars = [view_xz])
    viewer.fig.set_figheight(10)
    viewer.fig.set_figwidth(10)
    
    return None