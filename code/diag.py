import numpy as np
from matplotlib.pyplot import *
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import netCDF4
import sys, os, glob
##### import self-defined lib #####
from data_load import load_data
# =================================

def draw_var(var_name, log, tidx):
    data = load_data(case_name, "Diag", idx=tidx)
    variable = np.array(data[var_name])[0, :len(zc), iycmin:iycmax+1, ixcmin:ixcmax+1]
    lvs = np.linspace(log['vmin'], log['vmax'], log['Ncolor'])
    # select which section
    if 'x' not in log['axis']:
        variable = variable[:, :, log['section']]
        cf = contourf(yc, zc, variable, levels=lvs)
    elif 'y' not in log['axis']:
        variable = variable[:, log['section'], :]
        cf = contourf(xc, zc, variable, levels=lvs)
    elif 'z' not in log['axis']:
        variable = variable[log['section'], :, :]
        cf = contourf(xc, yc, variable, levels=lvs)
    colorbar(cf)

    title('Time: {:06d}'.format(tidx))

    # check dir
    fig_dir = home_dir + 'figure_VVM/{CN}/diag/{VN}/'.\
              format(CN=case_name,
                     VN=var_name)

    if not os.path.isdir(fig_dir):
        print('No {VN} Folder, Creating...'.format(VN=var_name))
        os.mkdir(fig_dir)


    # saving figure
    savefig(fig_dir + '{VN}-{IDX:06d}.jpg'\
            .format(CN = case_name, 
                    VN = var_name, 
		            IDX= tidx), dpi=100)
    clf()
    print('Drawing {VN} @ {IDX:06d}'.format(VN=var_name, IDX=tidx))

if __name__ == "__main__":
    case_name = str(input())
    home_dir = "/home/atmenu10246/"

    diag = load_data(case_name, "Diag", idx=0)
    # gloabl variable #
    xc, yc = np.array(diag['xc']), np.array(diag['yc']), 
    zc = np.array(diag['zc'])
    xc = xc - np.max(xc) / 2 # center @ 0
    xcmin, xcmax = -5000, 5000
    ycmin, ycmax = np.min(yc), np.max(yc)
    zclim = 12000
    ixcmin, ixcmax = np.where(xc>=xcmin)[0][0], np.where(xc<=xcmax)[0][-1]
    iycmin, iycmax = np.where(yc>=ycmin)[0][0], np.where(yc<=ycmax)[0][-1]
    zc = zc[zc <= zclim]
    xc = xc[(xc >= xcmin) & (xc <= xcmax)]

    draw_log = {
    'vmin' : 0, 
    'vmax' : 0.005, 
    'Ncolor' : 20,
    'section' : 63, 
    'axis' : 'xz'
    }
    draw_var(var_name='dm01', log=draw_log, tidx=0)
