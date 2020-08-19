import sys; sys.path.insert(0, '/home/adriano/goes16-acquisition')
import os
import subprocess as sp
from string import Template


class Downloader:
    def __init__(self, **kwargs):
        self.year = kwargs.get('year', None)
        self.month = kwargs.get('month', None)
        self.day = kwargs.get('day', None)
        self.julian_day = kwargs.get('day', None)
        self.hour = kwargs.get('hour', None)
        self.minute = kwargs.get('minute', None)
        self.directory = kwargs.get('directory', None)
        self.remote_url = kwargs.get('remote_url', None)
        self.filename = kwargs.get('filename', None)
        self.token = None
        self.instrument = None

    def initializer(self) -> None:
        pass

    def download_files(self):
        for file in self.files_to_download:
            print('Downloading %s...', file)
            args = dict(remote_url=self.remote_url, file=file,
                        directory=self.directory)
            local_url = Template(
                "$directory$file"
            ).substitute(**args)

            if not os.path.exists(local_url):
                query_download = Template(
                    "aws s3 cp s3://$remote_url$file $directory"
                ).substitute(**args)
                out = sp.Popen([query_download], shell=True, stdout=sp.PIPE)
                _ = out.communicate()[0].decode('utf-8')
            else:
                print('File %s alread exists'%file)

    def set_remote_url(self) -> None:
        pass

    def set_filename(self) -> None:
        pass

    def has_date(self) -> bool:
        return self.year is not None and self.month is not None and \
               self.day is not None

    def has_time(self):
        return self.hour is not None and self.minute is not None

    def format_time(self):
        container = [self.year, self.month, self.julian_day, self.hour,
                     self.minute]
        _year, _month, _julian_day, _hour, _minute = list(map(int, container))

        if _minute % 10 == 0 and _minute > 0:
            _minute = list(range(_minute - 10, _minute + 1))
            return dict(year=_year, julian_day='%s' % str(_julian_day).zfill(3),
                        hour='%s' % str(_hour).zfill(2),
                        minute=[str(x).zfill(2) for x in _minute])
        if _minute < 10:
            _minute = list(map(lambda x: str(x).zfill(2), range(50, 60)))
            _hour -= 1
        elif _minute < 20:
            _minute = list(map(lambda x: str(x).zfill(2), range(0, 11)))
        elif _minute < 30:
            _minute = list(map(lambda x: str(x).zfill(2), range(10, 21)))
        elif _minute < 40:
            _minute = list(map(lambda x: str(x).zfill(2), range(20, 31)))
        elif _minute < 50:
            _minute = list(map(lambda x: str(x).zfill(2), range(30, 41)))
        elif _minute < 60:
            _minute = list(map(lambda x: str(x).zfill(2), range(40, 51)))

        if _hour < 0:
            _julian_day -= 1
            _hour = 23

        return dict(year=_year, julian_day='%s' % str(_julian_day).zfill(3),
                    hour='%s' % str(_hour).zfill(2),
                    minute=_minute)

    def get_and_select_files(self):
        def contains(filename, filters):
            if self.instrument == 'GLM-L2-LCFA':
                if not filename.endswith('.nc'):
                    return False
            else:
                if not filename.endswith('.nc') or \
                        filename[:22] not in self.channels:
                    return False

            for f in filters:
                if f in filename:
                    return True

            return False

        filters = ['_s%s%s%s%s' % (self.time['year'], self.time['julian_day'],
                                   self.time['hour'], m) for m in
                   self.time['minute']]

        out = sp.Popen([self.query_base], shell=True, stdout=sp.PIPE)
        out = out.communicate()[0].decode('utf-8')
        files = out.split()
        filenames = sorted(
            list(filter(lambda file: contains(file, filters), files)))

        return filenames

    def make_directory(self) -> None:
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
