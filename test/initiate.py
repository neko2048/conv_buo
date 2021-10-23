import numpy as np
import sys
import netCDF4
##### import self-defined lib #####
sys.path.append('../code/')

response = str(input())
case_name = response.split()[0]
tidx = int(response.split()[1])
length = int(response.split()[2])

# >>>>> data processing >>>>>
def load_data(case_name, category, idx):
    try: 
        nc_location = "/home/atmenu10246/VVM/DATA/{CN}/archive/{CN}.L.{CG}-{IDX:06d}.nc"\
                       .format(CN=case_name, CG=category, IDX=idx)
        data = netCDF4.Dataset(nc_location)
    except FileNotFoundError:
        nc_location = "/home/atmenu10246/VVM/DATA/{CN}/archive/exp.L.{CG}-{IDX:06d}.nc"\
                       .format(CN=case_name, CG=category, IDX=idx)
        data = netCDF4.Dataset(nc_location)
    return data

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
# <<<<< data processing <<<<<


home_dir = "/home/atmenu10246/"
thmo = load_data(case_name, "Thermodynamic", idx=tidx)
dyna = load_data(case_name, "Dynamic", idx=tidx)
# gloabl variable #
# ========== theta grid ==========
xc, yc = np.array(thmo['xc']), np.array(thmo['yc']), # theta level (i, ), (j, )
zc = np.array(thmo['zc']) # theta level (k, )
denc = np.loadtxt("../constants/{CN}_density.txt".format(CN=case_name)) # theta level (k, )
zz = np.loadtxt("../constants/{CN}_z.txt".format(CN=case_name), skiprows=2)[:-1, 1] # W level (k, )

set_axis = {
"xmin": 0, #35000, 
"xmax": 1000000, #50000, 
"ymin": 0, #30000, 
"ymax": 1000000, #45000, 
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
zz = zz[set_axisarg["argzmin"]:set_axisarg["argzmax"]+1]
denc = denc[set_axisarg["argzmin"]:set_axisarg["argzmax"]+1]
dx, dy, dz = np.gradient(xc), np.gradient(yc), np.gradient(zc) # (i, ), (j, ), (k, )
# boundary of theta (i+1, j+1, k+1)
xb = (np.array([xc[0] - dx[0]] + [x for x in xc]) + np.array([x for x in xc] + [xc[-1] + dx[-1]])) / 2 
yb = (np.array([yc[0] - dy[0]] + [y for y in yc]) + np.array([y for y in yc] + [yc[-1] + dy[-1]])) / 2 
zb = np.array([zc[0], (zc[0] + zc[1]) / 2] + [z for z in zz[1:]])
