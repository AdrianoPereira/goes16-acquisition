from core import os
import subprocess as sp
from datetime import datetime as dt
from core.glm import *
from core.model import Model
from netCDF4 import Dataset
from shapely.geometry import Point
import os
import pandas as pd
from core.glm import glm_functions


class Acquisition(object):
    def __init__(self, sensor=None, download_out=None, csvfile_out=None):
        self.sensor = sensor
        self.download_out = download_out
        self.csvfile_out = csvfile_out
        self.csv_filename = ''

    def download(self):
        if self.sensor is None:
            raise Exception('You need to enter a sensor! <sensor>')
        if self.csvfile_out is None:
            raise Exception('You need to enter a folder to save CSV file! <csvfile_out>')
        if self.download_out is None:
            raise Exception('You need to enter a folder to save netCDF files! <download_out>')

        now = dt.utcnow()
        year = now.year
        day = julian_day(now.year, now.month, now.day)
        hour = now.hour
        minute = now.minute
        time = get_time(day, hour, minute)
        time['y'] = str(year)
        day, hour = time['d'], time['h']

        self.csv_filename = '%s_s%s%s%s%s' % (self.sensor, time['y'], time['d'], time['h'], time['m'][0])
        self.csv_filename += '_e%s%s%s%s.csv' % (time['y'], time['d'], time['h'], time['m'][-1])
        query = make_query(year, day, hour, self.sensor)
        filenames = filter_files(query, time)
        self.download_out = os.path.join(self.download_out, query.split()[-1])
        download_path = query.split()[-1]
        download_files(self.download_out, download_path, filenames)

    def create_dataframe(self):
        def get_files(dir_download):
            try:
                if dir_download is None:
                    raise TypeError('You need to enter a path!')
                files = os.listdir(dir_download)
            except FileNotFoundError:
                raise Exception('You need to enter a valid path!')

            files = sorted([os.path.join(dir_download, file) for file in files])
            files = list(filter(lambda file: file.endswith('.nc'), files))

            return files

        if 'GLM' in self.sensor:
            glm_functions.create_flash_dataframe(self.csv_filename)


    def remove_files(dir_download):
        print('remove ', dir_download)
        os.system("rm -rf %s" % (dir_download))


def download_files(download_out, download_path, filenames):
    if not os.path.exists(download_out):
        os.makedirs(download_out)
        for filename in filenames:
            print('Downloading %s%s...'%(download_out, filename))
            query = 'aws s3 cp s3://%s%s %s'%(download_path, filename, download_out)
            out = sp.Popen([query], shell=True, stdout=sp.PIPE)
            _ = out.communicate()[0].decode('utf-8')
    print('All files sensor downloaded!')


def make_query(year, day, hour, sensor='GLM-L2-LCFA'):
    query = "aws s3 ls noaa-goes16/%s/%s/%s/%s/"%(sensor, year, day, hour)

    return query


def filter_files(query, time):
    def contains(filename, filters):
        if not filename.endswith('.nc'):
            return False

        for f in filters:
            if f in filename:
                return True

        return False

    filters = ['_s%s%s%s%s' % (time['y'], time['d'], time['h'], m) for m in time['m']]

    out = sp.Popen([query], shell=True, stdout=sp.PIPE)
    out = out.communicate()[0].decode('utf-8')
    files = out.split()
    filenames = sorted(list(filter(lambda file: contains(file, filters), files)))

    return filenames


def julian_day(year, month, day):
    return str(dt.strptime('%s-%s-%s'%(year, month, day), '%Y-%m-%d')
               .timetuple().tm_yday).zfill(3)


def get_time(day, hour, minute):
    day, hour, minute = int(day), int(hour  ), int(minute)
    if minute%10 == 0:
        minute = list(range(minute-10, minute+1))
        return dict(d='%s'%str(day).zfill(3), h='%s'%str(hour).zfill(2), m=[str(x).zfill(2) for x in minute])

    if minute < 10:
        minute = list(map(lambda x: str(x).zfill(2), range(50, 60)))
        hour -= 1
    elif minute < 20:
        minute = list(map(lambda x: str(x).zfill(2), range(0, 11)))
    elif minute < 30:
        minute = list(map(lambda x: str(x).zfill(2), range(10, 21)))
    elif minute < 40:
        minute = list(map(lambda x: str(x).zfill(2), range(20, 31)))
    elif minute < 50:
        minute = list(map(lambda x: str(x).zfill(2), range(30, 41)))
    elif minute < 60:
        minute = list(map(lambda x: str(x).zfill(2), range(40, 51)))

    if hour < 0:
        day -= 1
        hour = 23

    return dict(d='%s'%str(day).zfill(3), h='%s'%str(hour).zfill(2), m=minute)