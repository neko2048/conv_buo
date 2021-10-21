import netCDF4 
import numpy as np 
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