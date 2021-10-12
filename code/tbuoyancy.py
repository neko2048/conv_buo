import numpy as np
from numpy import ma
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys
##### import self-defined lib #####
from nclcmaps import nclcmap
sys.path.append('../code/')
from data_load import load_data

def cut_edge(data, edge_arg):
    argxmin = edge_arg["argxmin"]
    argxmax = edge_arg["argxmax"]
    argymin = edge_arg["argymin"]
    argymax = edge_arg["argymax"]
    argzmin = edge_arg["argzmin"]
    argzmax = edge_arg["argzmax"]

    return np.array(data)[0, argzmin:argzmax+1, argymin:argymax+1, argxmin:argxmax+1]


def gen_buoyancy(data, edge_arg):
    # need theta, qv, qc

    theta = cut_edge(data['th'], set_axisarg)
    theta0 = np.mean(theta, axis=(1, 2))
    theta0 = np.tile(theta0[:, np.newaxis, np.newaxis], 
                     reps=(1, theta.shape[1], theta.shape[2]))
    theta_turb = theta - theta0

    qv = cut_edge(data['qv'], set_axisarg)
    qc = cut_edge(data['qc'], set_axisarg)

    return 9.81 * (theta_turb/theta0 + 0.61 * qv - qc)

def gen_tv_buoyancy(data, edge_arg):
    # theta, qv
    tv = cut_edge(data['th'], set_axisarg)
    tv0 = np.mean(tv, axis=(1, 2))
    tv0 = np.tile(tv0[:, np.newaxis, np.newaxis], 
                     reps=(1, tv.shape[1], tv.shape[2]))
    buoyancy = (tv - tv0) / tv0
    return buoyancy


def draw_cloud(profile):
    xarg = np.argmin(np.abs(xc  - profile))
    # rain
    cmap = nclcmap('BrownBlue12')
    colors = cm.Blues(np.linspace(0.3, 1))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    qr = cut_edge(thmo["qr"], set_axisarg)[1:, 1:, xarg]
    qr = ma.masked_array(qr, qr<=1e-6)#5e-6)
    pcolormesh(yc, zc, qr, cmap=cmap, vmin=0, vmax=0.005)
    colorbar()
    # cloud
    colors = cm.Greys(np.hstack([np.linspace(0.5, 0.75, 95)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    qc = cut_edge(thmo["qc"], set_axisarg)[1:, 1:, xarg]
    qc = ma.masked_array(qc, qc<=0)
    pcolormesh(yc, zc, qc, cmap=cmap, vmin=0, vmax=0.005)
    colorbar()

    # wind information
    w = (cut_edge(dyna["w"], set_axisarg)[1:] + \
        cut_edge(dyna["w"], set_axisarg)[:-1]) / 2
    yy, zz = np.meshgrid(yc, czc)
    pw = w[:, :, xarg] > 0
    quiver(yy[pw], zz[pw], 0, w[:, :, xarg][pw], color='red', alpha=0.2)
    nw = w[:, :, xarg] < 0 
    quiver(yy[nw], zz[nw], 0, w[:, :, xarg][nw], color='blue', alpha=0.2)


    title("TIME: {T:06d}".format(T=i*2))
    savefig("cloud_{T:06d}.jpg".format(T=i), dpi=200)
    clf()

def draw_buoyancy(profile, type):
    xarg = np.argmin(np.abs(xc  - profile))
    # buoyancy
    if type == "tv":
        buoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg)[1:]
        contourf(yc, czc, buoyancy[:, :, xarg], cmap='coolwarm', levels=np.arange(-0.015, 0.015, 0.001))
    else:
        buoyancy = gen_buoyancy(data=thmo, edge_arg=set_axisarg)[1:]
        contourf(yc, czc, buoyancy[:, :, xarg], cmap='coolwarm', levels=np.arange(-0.15, 0.15, 0.01))
    colorbar()

    # vertical velocity
    w = (cut_edge(dyna["w"], set_axisarg)[1:] + \
        cut_edge(dyna["w"], set_axisarg)[:-1]) / 2

    yy, zz = np.meshgrid(yc, czc)
    pw = w[:, :, xarg] > 0
    quiver(yy[pw], zz[pw], 0, w[:, :, xarg][pw], color='red', alpha=0.2)
    nw = w[:, :, xarg] < 0 
    quiver(yy[nw], zz[nw], 0, w[:, :, xarg][nw], color='blue', alpha=0.2)

    title("X: {X} | TIME: {T:06d}".format(X=profile, T=i*2))
    savefig("buoyancy_tv{T:06d}.jpg".format(T=i), dpi=200)
    clf()

def draw_srf_rain():
    # surface rain 
    qr = (cut_edge(thmo["qr"], set_axisarg)[1, :, :] + \
          cut_edge(thmo["qr"], set_axisarg)[0, :, :]) / 2
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
    cqv = cut_edge(thmo["qv"], set_axisarg)[1:, 1:, 1:]
    gradx = np.tile((xc[1:] - xc[:-1])[np.newaxis, np.newaxis, :], reps=(len(czc), len(yc)-1, 1))
    grady = np.tile((yc[1:] - yc[:-1])[np.newaxis, :, np.newaxis], reps=(len(czc), 1, len(xc)-1))
    gradz = np.tile((zc[1:] - zc[:-1])[:, np.newaxis, np.newaxis], reps=(1, len(yc)-1, len(xc)-1))
    # gradient z start from surface to heights
    # gradient shape: (k-1, j-1, i-1)
    grid_density = np.tile(cdensity[:, np.newaxis, np.newaxis], reps=(1, len(yc)-1, len(xc)-1))
    weight = gradz * grid_density # shape: (k-1, j-1, i-1)

    cwv = np.sum(weight * cqv, axis=(0)) # column water vapor, shape: (k-1, j-1, i-1)
    pcolormesh(xc, yc, cwv, vmin=50, vmax=70)
    colorbar()

    # cloud existence
    Eqc = np.mean(cut_edge(thmo["qr"], set_axisarg), axis=0) > 5e-7
    Eqc = np.array(Eqc, dtype=int)
    contour(xc, yc, Eqc, levels=[1], colors='black')
    title("Column Water Vapor [" +  r"$kg/m^2$" + "] | T: {T:06d}".format(T=i*2))
    savefig('cwv_{T:06d}.jpg'.format(T=i), dpi=200)
    clf()

def draw_xycoreshell():
    tvbuoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg)[1:, 1:, 1:] # shape: (k-1, j-1, i-1)
    w = cut_edge(dyna["w"], set_axisarg)[:, 1:, 1:] # choose for xy now
    cw = (w[1:] + w[:-1]) / 2 # z center at one with theta
    qc = cut_edge(thmo["qc"], set_axisarg)[1:, 1:, 1:]

    # core: a saturated volume that is positively buoyant and moving upward
    colors = cm.Reds(np.hstack([np.linspace(0.5, 1)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    topmask_core = np.logical_and(tvbuoyancy > 0, cw > 0)
    topmask_core = np.logical_and(topmask_core, qc > 0)
    xytopmask_core = np.sum(topmask_core, axis=(0))
    xytopmask_core = np.ma.masked_array(xytopmask_core, xytopmask_core<=0)
    pcolormesh(xc, yc, xytopmask_core, vmin=1, vmax=20, cmap=cmap)
    colorbar()

    # shell: saturated part but not core
    colors = cm.Blues(np.hstack([np.linspace(0.5, 1)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    topmask_shell = np.array(qc > 0, dtype=int) - np.array(topmask_core, dtype=int)
    xytopmask_shell = np.sum(topmask_shell, axis=(0))
    xytopmask_shell = np.ma.masked_array(xytopmask_shell, xytopmask_shell<=0)
    pcolormesh(xc, yc, xytopmask_shell, vmin=1, cmap=cmap, alpha=.5)


    title("Core & Shell Top View | T: {T:06d}".format(T=i*2))
    savefig('coreshell_xy{T:06d}.jpg'.format(T=i), dpi=200)
    clf()

def draw_yzcoreshell(profile):
    xarg = np.argmin(np.abs(xc - profile))
    tvbuoyancy = gen_tv_buoyancy(data=thmo, edge_arg=set_axisarg)[1:, 1:, xarg] # shape: (k-1, j-1, i-1)
    w = cut_edge(dyna["w"], set_axisarg)[:, 1:, xarg] # choose for xy now
    cw = (w[1:] + w[:-1]) / 2 # z center at one with theta
    qc = cut_edge(thmo["qc"], set_axisarg)[1:, 1:, xarg]

    # core: a saturated volume that is positively buoyant and moving upward
    colors = cm.Reds(np.hstack([np.linspace(0.5, 0.75)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    mask_core = np.logical_and(tvbuoyancy > 0, cw > 0)
    mask_core = np.logical_and(mask_core, qc > 0)
    mask_core = np.ma.masked_array(mask_core, mask_core<=0)
    pcolormesh(yc, zc, mask_core, cmap=cmap, vmin=0, vmax=1)

    # shell: saturated part but not core
    colors = cm.Blues(np.hstack([np.linspace(0.5, 0.75)]))
    cmap = LinearSegmentedColormap.from_list('name', colors)
    mask_shell = np.array(qc > 0, dtype=int) - np.array(mask_core, dtype=int)
    mask_shell = np.ma.masked_array(mask_shell, mask_shell<=0)
    pcolormesh(yc, zc, mask_shell, cmap=cmap, vmin=0, vmax=1)

    title("Core & Shell | X: {P} | T: {T:06d}".format(P=profile, T=i*2))
    savefig('coreshell_yz{T:06d}.jpg'.format(T=i), dpi=200)
    clf()


if __name__ == "__main__":
    response = str(input())
    case_name = response.split()[0]
    tidx = int(response.split()[1])
    length = int(response.split()[2])


    home_dir = "/home/atmenu10246/"
#    tidx = 0
    thmo = load_data(case_name, "Thermodynamic", idx=tidx)
    dyna = load_data(case_name, "Dynamic", idx=tidx)
    # gloabl variable #
    xc, yc = np.array(thmo['xc']), np.array(thmo['yc']), 
    zc = np.array(thmo['zc'])
    density = np.loadtxt("../constants/diurnal_prescribed_density.txt")

    set_axis = {
    "xmin": 35000, 
    "xmax": 50000, 
    "ymin": 30000, 
    "ymax": 45000, 
    "zmin": 0, 
    "zmax": 13000, 
    }

    set_axisarg = {
    "argxmin": np.argmin(np.abs(xc - set_axis['xmin'])), 
    "argxmax": np.argmin(np.abs(xc - set_axis['xmax'])), 
    "argymin": np.argmin(np.abs(yc - set_axis['ymin'])), 
    "argymax": np.argmin(np.abs(yc - set_axis['ymax'])), 
    "argzmin": np.argmin(np.abs(zc - set_axis['zmin'])), 
    "argzmax": np.argmin(np.abs(zc - set_axis['zmax'])), 
    }

    # cutting needed grids
    xc = xc[set_axisarg["argxmin"]:set_axisarg["argxmax"]+1]
    yc = yc[set_axisarg["argymin"]:set_axisarg["argymax"]+1]
    zc = zc[set_axisarg["argzmin"]:set_axisarg["argzmax"]+1]
    density = density[set_axisarg["argzmin"]:set_axisarg["argzmax"]+1]
    czc = (zc[1:] + zc[:-1]) / 2
    cdensity = (density[1:] + density[:-1]) / 2

    #print("Dimension: {X} (X grids) x {Y} (Y grids) x {Z} (Z grids)" \
    #      .format(X=len(xc), Y=len(yc), Z=len(zc)))

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
        draw_xycoreshell()
        #draw_yzcoreshell(profile=42000)
        output_string = "task {START} -> {NOW} -> {END} ({P} %)"\
                        .format(START=tidx, NOW=i, END=tidx+length-1, P=((i - tidx + 1)/(length)*100))
        print(output_string)

