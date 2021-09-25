import netCDF4 

def load_data(case_name, category, idx):
    nc_location = "/home/atmenu10246/VVM/DATA/{CN}/archive/{CN}.L.{CG}-{IDX:06d}.nc"\
	    .format(CN=case_name, CG=category, IDX=idx)
    data = netCDF4.Dataset(nc_location)
    return data
