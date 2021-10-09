import numpy as np
from matplotlib.pyplot import *
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import netCDF4
import sys, os, glob
##### import self-defined lib #####
from data_load import load_data
from functions import check_folder
# =================================
def draw_var(var, var_name, log, tidx):
    # check dir ====================
    fig_dir = home_dir + 'figure_VVM/{CN}/thermodynamic/{VN}/'.\
              format(CN=case_name,
                     VN=var_name)

    check_folder(fig_dir=fig_dir)

    # load variable ====================
    variable = np.array(var)[:len(zc), iycmin:iycmax+1, ixcmin:ixcmax+1]

    # drawing setting ====================
    lvs = np.linspace(log['vmin'], log['vmax'], log['Ncolor'])
    cbar = log['cbar']

    # select which section and draw ====================
    if 'x' not in log['axis']:
        variable = variable[:, :, log['section']]
        cf = contourf(yc, zc, variable, levels=lvs, cmap=cbar)
    elif 'y' not in log['axis']:
        variable = variable[:, log['section'], :]
        cf = contourf(xc, zc, variable, levels=lvs, cmap=cbar)
    elif 'z' not in log['axis']:
        variable = variable[log['section'], :, :]
        cf = contourf(xc, yc, variable, levels=lvs, cmap=cbar)
    colorbar(cf)

    title('Time: {:06d}'.format(tidx))

    # saving figure ====================
    savefig(fig_dir + '{VN}-{IDX:06d}.jpg'\
            .format(CN = case_name, 
                    VN = var_name, 
		            IDX= tidx), dpi=100)
    clf()
    print('Drawing {VN} @ {IDX:06d}'.format(VN=var_name, IDX=tidx))

def gen_thturb(tidx):
    # load origin 3D th ====================
    data = load_data(case_name, "Thermodynamic", idx=tidx)
    th = np.array(data['th'])[0]

    # calculation ====================
    thbar = np.mean(th, axis=(1, 2)) # shape: (z, )
    thturb = th - np.tile(thbar[:, np.newaxis, np.newaxis], 
                          reps=(1, th.shape[1], th.shape[2]))

    return thturb, thbar

if __name__ == "__main__":
    case_name = str(input())
    home_dir = "/home/atmenu10246/"

    diag = load_data(case_name, "Thermodynamic", idx=0)
    # gloabl variable ====================
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
    'vmin' : -7, 
    'vmax' : +7, 
    'Ncolor' : 20,
    'section' : 63, 
    'axis' : 'xz',
    'cbar' : 'coolwarm',
    }

    for i in range(30):
        # primary variables ====================
        #var = load_data(case_name="bubble", category="Thermodynamic", idx=i)
        #var_name = "th"
        #var = np.array(var[var_name])[0]
        #draw_var(var=var, var_name=var_name, log=draw_log, tidx=i)

        # secondary variables ====================
        thturb, thbar = gen_thturb(tidx=i)
        draw_var(var=thturb, var_name='thturb', log=draw_log, tidx=i)


