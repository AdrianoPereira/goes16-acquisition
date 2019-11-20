import os
import subprocess as sp
from datetime import datetime as dt


class Model(object):
    def __init__(self):
        pass

    def download(self, sensor):
        now = dt.utcnow()
        year = now.year
        day = julian_day(now.year, now.month, now.day)
        hour = now.hour
        minute = now.minute
        time = get_time(day, hour, minute)
        time['y'] = str(year)
        day, hour = time['d'], time['h']

        # downloading data
        filename = '%s_s%s%s%s%s' % (sensor, time['y'], time['d'], time['h'], time['m'][0])
        filename += '_e%s%s%s%s.csv' % (time['y'], time['d'], time['h'], time['m'][-1])
        query = make_query(year, day, hour, sensor)
        files = filter_files(query, time)
        path = query.split()[-1]
        download_files(path, files)

        res = dict(dir_download=path, filename_csv=filename)

        return res

    def get_files(self, dir_download):
        try:
            if dir_download is None:
                raise TypeError('You need to enter a path!')
            files = os.listdir(dir_download)
        except FileNotFoundError:
            raise Exception('You need to enter a valid path!')

        files = sorted([os.path.join(dir_download, file) for file in files])
        files = list(filter(lambda file: file.endswith('.nc'), files))

        return files

    def remove_files(dir_download):
        print('remove ', dir_download)
        os.system("rm -rf %s" % (dir_download))


def download_files(path, filenames):
    if not os.path.exists(path):
        os.makedirs(path)
        for filename in filenames:
            print('Downloading %s...'%filename)
            query = 'aws s3 cp s3://%s%s %s'%(path, filename, path)
            out = sp.Popen([query], shell=True, stdout=sp.PIPE)
            _ = out.communicate()[0].decode('utf-8')


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