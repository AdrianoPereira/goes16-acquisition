from core import Dataset
from core import Point
from core import os
from core import pandas as pd


def create_flash_dataframe(output_csv, csv_filename):
    def is_glm_file(self, file):
        file = file.split('/')[-1]
        return file.startswith('OR_GLM')

    files = [os.path.join(output_csv, file) for file in os.listdir(output_csv)]
    files = list(filter(lambda file: is_glm_file(file), files))

    if len(files) == 0:
        print('GLM netCDF files not found')
        return

    data = dict()
    data['start_scan'] = []
    data['end_scan'] = []
    data['year'] = []
    data['julian_day'] = []
    data['hour'] = []
    data['minute'] = []
    data['flash_lon'] = []
    data['flash_lat'] = []
    data['geometry'] = []

    for file in files:
        nc = Dataset(file, 'r')
        file = file.split('/')[-1]

        start_scan = file[20:34]
        end_scan = file[36:50]
        y = start_scan[:4]
        jd = start_scan[4:7]
        h = start_scan[7:9]
        m = start_scan[9:11]

        lons, lats = nc.variables['flash_lon'], nc.variables['flash_lat']

        for lon, lat in zip(lons, lats):
            point = Point(lon, lat)
            data['start_scan'].append(start_scan)
            data['end_scan'].append(end_scan)
            data['year'].append(y)
            data['julian_day'].append(jd)
            data['hour'].append(h)
            data['minute'].append(m)
            data['flash_lon'].append(lon)
            data['flash_lat'].append(lat)
            data['geometry'].append(point)

    if not os.path.exists(output_csv):
        os.makedirs(output_csv)
    df = pd.DataFrame(data)
    filename = os.path.join(output_csv, csv_filename)
    df.to_csv('%s' % filename, index=False)

    print('CSV file created: ', filename)
