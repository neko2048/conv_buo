import numpy as np
from matplotlib.pyplot import *
import sys
##### import self-defined lib #####
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

    theta = cut_edge(data['th'], edge_arg)
    theta0 = np.mean(theta, axis=(1, 2))
    theta0 = np.tile(theta0[:, np.newaxis, np.newaxis], 
                     reps=(1, theta.shape[1], theta.shape[2]))
    theta_turb = theta - theta0

    qv = cut_edge(data['qv'], edge_arg)
    qc = cut_edge(data['qc'], edge_arg)

    return 9.81 * (theta_turb/theta0 + 0.61 * qv - qc)



if __name__ == "__main__":
    case_name = str(input())
    home_dir = "/home/atmenu10246/"
    tidx = 0
    thmo = load_data(case_name, "Thermodynamic", idx=tidx)
    dyna = load_data(case_name, "Dynamic", idx=tidx)
    # gloabl variable #
    xc, yc = np.array(thmo['xc']), np.array(thmo['yc']), 
    zc = np.array(thmo['zc'])


    set_axis = {
    "xmin": 40800, 
    "xmax": 41200, 
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
    zc = (zc[1:] + zc[:-1]) / 2

    print("Dimension: {X} (X grids) x {Y} (Y grids) x {Z} (Z grids)" \
          .format(X=len(xc), Y=len(yc), Z=len(zc)))



    for i in range(325, 360):
        print(i)
        thmo = load_data(case_name, "Thermodynamic", idx=i)
        dyna = load_data(case_name, "Dynamic", idx=i)

        buoyancy = gen_buoyancy(data=thmo, edge_arg=set_axisarg)[1:]
        w = (cut_edge(dyna["w"], edge_arg=set_axisarg)[1:] + \
            cut_edge(dyna["w"], edge_arg=set_axisarg)[:-1]) / 2

        contourf(yc, zc, buoyancy[:, :, 2])

        colorbar()
        title("TIME: {T:06d}".format(T=i*2))
        savefig("buoyancy_{T:06d}.jpg".format(T=i*2), dpi=200)
        clf()

