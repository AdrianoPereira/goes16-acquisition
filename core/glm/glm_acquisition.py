from core.model import Model
from netCDF4 import Dataset
from shapely.geometry import Point
import os
import pandas as pd


class GLM(Model):
    def __init__(self):
        super().__init__()

    def is_glm_file(self, file):
        file = file.split('/')[-1]
        return file.startswith('OR_GLM')

    def create_dataframe_glm(self, dir_download=None, filename=None, output_csv=None, remove_download=True):
        files = self.get_files(dir_download)
        print(files)
        files = list(filter(lambda file: self.is_glm_file(file), files))
        if len(files) == 0:
            print('GLM netCDF files not found')
            return
        data = {}
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
        filename = os.path.join(output_csv, filename)
        df.to_csv('%s' %filename, index=False)

        if remove_download:
            self.remove_files(dir_download)

        return filename


