import os
import pandas as pd
import geopandas as gpd
import numpy as np
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from core.abi import remap


# bbox = [-85, -56, -35, 15] #minx, maxx, miny, maxy
# bbox = [-82, -32, -58, 13] #minx, maxx, miny, maxy
bbox = [-53.08059692, -25.25489044, -44.20065689, -19.78015137]
path = 'data/noaa-goes16/ABI-L2-CMIPF/2019/329/16'
files = [os.path.join(path, file) for file in os.listdir(path)]
files = list(filter(lambda file: file.endswith('.nc'), files))
files = {file[60:63]: file for file in sorted(files)}

for channel in list(files.keys())[10:14]:
    print('Channel ', channel)
    df = dict(channel=[], value=[], lon=[], lat=[], ind_x=[], ind_y=[])
    data = remap(path=files[channel], extent=bbox, resolution=2, driver='netCDF4')
    grid = data.ReadAsArray()

    lons = np.linspace(bbox[0], bbox[1], grid.shape[1])
    lats = np.linspace(bbox[2], bbox[3], grid.shape[0])

    for row, lat in enumerate(lats):
        for col, lon in enumerate(lons):
            print('X=%s, Y=%s'%(col, row))
            df['channel'].append(channel)
            df['value'].append(grid[row][col])
            df['lon'].append(lon)
            df['lat'].append(lat)
            df['ind_x'].append(row)
            df['ind_y'].append(col)

    df = pd.DataFrame(df)
    df.to_csv('ABI-INFO-%s.csv'%channel, index=False)
