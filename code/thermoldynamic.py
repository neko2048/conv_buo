import numpy as np
from matplotlib.pyplot import *
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import netCDF4
import sys, os, glob
##### import self-defined lib #####
from data_load import load_data
# =================================

def draw_var(var_name, axis, section, tidx):
    print('Drawing TIDX: {IDX}'.format(IDX=tidx))
    data = load_data(case_name, "Thermodynamic", idx=tidx)
    variable = np.array(data[var_name])[0, :len(zc), iycmin:iycmax+1, ixcmin:ixcmax+1]
    vmin, vmax = 0, 0.005
    lvs = np.linspace(vmin, vmax, 20)
    # select which section
    if 'x' not in axis:
        variable = variable[:, :, section]
        cf = contourf(yc, zc, variable, levels=lvs)
    elif 'y' not in axis:
        variable = variable[:, section, :]
        cf = contourf(xc, zc, variable, levels=lvs)
    elif 'z' not in axis:
        variable = variable[section, :, :]
        cf = contourf(xc, yc, variable, levels=lvs)
    colorbar(cf)

    title('Time: {:06d}'.format(tidx))
    
    fig_dir = home_dir + 'figure_VVM/{CN}/thermodynamic/{VN}/'.\
              format(CN=case_name,
                     VN=var_name)
    if not os.path.isdir(fig_dir):
        os.mkdir(fig_dir)

    savefig(fig_dir + '{VN}-{IDX:06d}.jpg'\
            .format(CN = case_name, 
                    VN = var_name, 
		            IDX= tidx), dpi=100)
    clf()

if __name__ == "__main__":
    case_name = str(input())
    home_dir = "/home/atmenu10246/"

    thermody = load_data(case_name, "Thermodynamic", idx=0)
    # gloabl variable #
    xc, yc, zc = np.array(thermody['xc']), np.array(thermody['yc']), np.array(thermody['zc'])
    xc = xc - np.max(xc) / 2 # center @ 0
    xcmin, xcmax = -5000, 5000
    ycmin, ycmax = np.min(yc), np.max(yc)
    zclim = 12000
    ixcmin, ixcmax = np.where(xc>=xcmin)[0][0], np.where(xc<=xcmax)[0][-1]
    iycmin, iycmax = np.where(yc>=ycmin)[0][0], np.where(yc<=ycmax)[0][-1]
    zc = zc[zc <= zclim]
    xc = xc[(xc >= xcmin) & (xc <= xcmax)]

    for i in range(30):
        draw_var(var_name='qc', axis='xz', section=63, tidx=i)
