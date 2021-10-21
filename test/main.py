import numpy as np
from numpy import ma
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys
##### import self-defined lib #####
from nclcmaps import nclcmap
sys.path.append('../code/')
from process_data import *
from initiate import *

def draw_pure(var_name, type, log, tidx):
    try:
        data = load_data(case_name, type, idx=tidx)
    except FileNotFoundError:
        return None
    variable = cut_edge(data[var_name], set_axisarg)
    # select which section
    if 'x' not in log['axis']:
        arg = np.argmin(np.min(xc - profile))
        variable = variable[:, :, arg]
        cf = contourf(yc, zc, variable)
    elif 'y' not in log['axis']:
        arg = np.argmin(np.min(yc - profile))
        variable = variable[:, arg, :]
        cf = contourf(xc, zc, variable)
    elif 'z' not in log['axis']:
        arg = np.argmin(np.min(zc - profile))
        variable = variable[arg, :, :]
        cf = contourf(xc, yc, variable)
    colorbar(cf)

    title('Time: {:06d}'.format(tidx))
    # saving figure
    savefig("{VN}_{T:06d}.jpg".format(VN=var_name, T=i), dpi=200)
    clf()


def draw_cloud(profile):
    xarg = np.argmin(np.abs(xc  - profile))
    # rain
    cmap = nclcmap('BrownBlue12')
    colors = cm.Blues(np.linspace(0.3, 1))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    qr = cut_edge(thmo["qr"], set_axisarg)[:, :, xarg]
    qr = ma.masked_array(qr, qr<=1e-6)#5e-6)
    pcolormesh(yb, zb, qr, cmap=cmap, vmin=0, vmax=0.005)
    #colorbar()
    # cloud
    colors = cm.Greys(np.hstack([np.linspace(0.5, 0.75, 95)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    qc = cut_edge(thmo["qc"], set_axisarg)[:, :, xarg]
    qc = ma.masked_array(qc, qc<=0)
    pcolormesh(yb, zb, qc, cmap=cmap, vmin=0, vmax=0.005)
    #colorbar()

    # wind information
    y, z = np.meshgrid(yc, zz)
    w = cut_edge(dyna["w"], set_axisarg)[:, :, xarg]
    pw = w > 0
    quiver(y[pw], z[pw], 0, w[pw], color='red', alpha=0.2)
    nw = w < 0 
    quiver(y[nw], z[nw], 0, w[nw], color='blue', alpha=0.2)

    title("TIME: {T:06d}".format(T=i*2))
    savefig("cloud_{T:06d}.jpg".format(T=i), dpi=200)
    clf()

def draw_buoyancy(profile, type):
    xarg = np.argmin(np.abs(xc  - profile))
    # buoyancy
    if type == "tv":
        buoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg)[:]
        contourf(yc, zc, buoyancy[:, :, xarg], cmap='coolwarm', levels=np.arange(-0.015, 0.015, 0.001))
    else:
        buoyancy = gen_buoyancy(data=thmo, edge_arg=set_axisarg)[:]
        contourf(yc, zc, buoyancy[:, :, xarg], cmap='coolwarm', levels=np.arange(-0.15, 0.15, 0.01))
    colorbar()

    # vertical velocity
    y, z = np.meshgrid(yc, zz)
    w = cut_edge(dyna["w"], set_axisarg)[:, :, xarg]
    pw = w > 0
    quiver(y[pw], z[pw], 0, w[pw], color='red', alpha=0.2)
    nw = w < 0 
    quiver(y[nw], z[nw], 0, w[nw], color='blue', alpha=0.2)

    title("X: {X} | TIME: {T:06d}".format(X=profile, T=i*2))
    savefig("buoyancy_tv{T:06d}.jpg".format(T=i), dpi=200)
    clf()

def draw_srf_rain():
    # surface rain 
    qr = cut_edge(thmo['qr'], set_axisarg)[0, :, :]
    qr = ma.masked_array(qr, qr<0)
    cmap = nclcmap('BrownBlue12')
    #colors = cm.Blues(np.linspace(0.5, 1, 90))
    cmap = LinearSegmentedColormap.from_list('name', [(0, "#bc763c"), (0.1, "#ffffff"), (0.2, "#b5cbe6"), (1.0, "#007bbb")])
    contourf(xc, yc, qr, levels=np.arange(0, 0.002, 0.0001), cmap=cmap)
    colorbar()

    # cloud existence
    Eqc = np.mean(cut_edge(thmo["qr"], set_axisarg), axis=0) > 1e-6
    Eqc = np.array(Eqc, dtype=int)
    contour(xc, yc, Eqc, levels=[1], colors='black')

    title("TIME: {T:06d}".format(T=i*2))
    savefig("srfrain_{T:06d}.jpg".format(T=i), dpi=200)
    clf()


def draw_cwv():
    cqv = cut_edge(thmo["qv"], set_axisarg)
    gradz = np.tile((zb[1:] - zb[:-1])[:, np.newaxis, np.newaxis], reps=(1, len(yc), len(xc)))
    # gradient z start from surface to heights
    grid_density = np.tile(denc[:, np.newaxis, np.newaxis], reps=(1, len(yc), len(xc)))
    weight = gradz * grid_density # shape: (k-1, j-1, i-1)

    cwv = np.sum(weight * cqv, axis=(0)) # column water vapor, shape: (k, j, i)
    pcolormesh(xb, yb, cwv, vmin=50, vmax=70)
    colorbar()

    # cloud existence
    Eqc = np.mean(cut_edge(thmo["qr"], set_axisarg), axis=0) > 5e-7
    Eqc = np.array(Eqc, dtype=int)
    contour(xc, yc, Eqc, levels=[1], colors='black')
    title("Column Water Vapor [" +  r"$kg/m^2$" + "] | T: {T:06d}".format(T=i*2))
    savefig('cwv_{T:06d}.jpg'.format(T=i), dpi=200)
    clf()

def draw_xycoreshell():
    tvbuoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg) # shape: (k, j, i)
    w = cut_edge(dyna["w"], set_axisarg) # choose for xy now
    wc = np.array([w[0]] + [xw for xw in (w[1:]+w[:-1])/2]) # z level same as the one with theta
    qc = cut_edge(thmo["qc"], set_axisarg)

    # core: a saturated volume that is positively buoyant and moving upward
    colors = cm.Reds(np.hstack([np.linspace(0.5, 1)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    topmask_core = np.logical_and(tvbuoyancy > 0, wc > 0)
    topmask_core = np.logical_and(topmask_core, qc > 0)
    xytopmask_core = np.sum(topmask_core, axis=(0))
    xytopmask_core = np.ma.masked_array(xytopmask_core, xytopmask_core<=0)
    pcolormesh(xb, yb, xytopmask_core, vmin=1, vmax=20, cmap=cmap)
    colorbar()

    # shell: saturated part but not core
    colors = cm.Blues(np.hstack([np.linspace(0.5, 1)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    topmask_shell = np.array(qc > 0, dtype=int) - np.array(topmask_core, dtype=int)
    xytopmask_shell = np.sum(topmask_shell, axis=(0))
    xytopmask_shell = np.ma.masked_array(xytopmask_shell, xytopmask_shell<=0)
    pcolormesh(xb, yb, xytopmask_shell, vmin=1, cmap=cmap, alpha=.5)


    title("Core & Shell Top View | T: {T:06d}".format(T=i*2))
    savefig('coreshell_xy{T:06d}.jpg'.format(T=i), dpi=200)
    clf()

def draw_yzcoreshell(profile):
    xarg = np.argmin(np.abs(xc - profile))
    tvbuoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg)[:, :, xarg] # shape: (k-1, j-1, i-1)
    w = cut_edge(dyna["w"], set_axisarg)[:, :, xarg] # choose for xy now
    wc = np.array([w[0]] + [xw for xw in (w[1:]+w[:-1])/2]) # z center at one with theta
    qc = cut_edge(thmo["qc"], set_axisarg)[:, :, xarg]

    # core: a saturated volume that is positively buoyant and moving upward
    colors = cm.Reds(np.hstack([np.linspace(0.5, 0.75)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    mask_core = np.logical_and(tvbuoyancy > 0, wc > 0)
    mask_core = np.logical_and(mask_core, qc > 0)
    mask_core = np.ma.masked_array(mask_core, mask_core<=0)
    pcolormesh(yb, zb, mask_core, cmap=cmap, vmin=0, vmax=1)

    # shell: saturated part but not core
    colors = cm.Blues(np.hstack([np.linspace(0.5, 0.75)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    mask_shell = np.array(qc > 0, dtype=int) - np.array(mask_core, dtype=int)
    mask_shell = np.ma.masked_array(mask_shell, mask_shell<=0)
    pcolormesh(yb, zb, mask_shell, cmap=cmap, vmin=0, vmax=1)

    title("Core & Shell | X: {P} | T: {T:06d}".format(P=profile, T=i*2))
    savefig('coreshell_yz{T:06d}.jpg'.format(T=i), dpi=200)
    clf()


if __name__ == "__main__":
    # >>> for the pure drawing data e.g. diag, thermodynamic variables >>>
    draw_log = {
    'vmin' : -0.4, 
    'vmax' : 0.4, 
    'Ncolor' : 20,
    'profile' : 40000, 
    'axis' : 'xz',
    'cbar' : 'coolwarm',
    }
    # <<< for the pure drawing data e.g. diag, thermodynamic variables <<<
    for i in range(tidx, tidx+length):
        thmo = load_data(case_name, "Thermodynamic", idx=i)
        dyna = load_data(case_name, "Dynamic", idx=i)
        # =====testing region=====
        
        # =====testing region=====
        
        # ========== drawing options ========== #
        #draw_cloud(profile=42000)
        #draw_buoyancy(profile=42000, type="tv")
        #draw_buoyancy(profile=42000, type="None")
        #draw_srf_rain()
        #draw_cwv()
        #draw_xycoreshell()
        #draw_yzcoreshell(profile=42000)
        #draw_pure(var_name="qr", type="Thermodynamic", log=draw_log, tidx=i)
        output_string = "task {START} -> {NOW} -> {END} ({P} %)"\
                        .format(START=tidx, NOW=i, END=tidx+length-1, P=((i - tidx + 1)/(length)*100))
        print(output_string)

