import sys; sys.path.insert(0, '/home/adriano/goes16-acquisition')
from goes16downloader._exceptions import *
import os
import subprocess as sp


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

    def initializer(self) -> None:
        pass

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
            return dict(julian_day='%s' % str(_julian_day).zfill(3),
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

        return dict(julian_day='%s' % str(_julian_day).zfill(3),
                    hour='%s' % str(_hour).zfill(2),
                    minute=_minute)

    def select_files(self, query, time):
        def contains(filename, filters):
            if not filename.endswith('.nc'):
                return False

            for f in filters:
                if f in filename:
                    return True

            return False

        filters = ['_s%s%s%s%s' % (time['y'], time['d'], time['h'], m) for m in
                   time['m']]

        out = sp.Popen([query], shell=True, stdout=sp.PIPE)
        out = out.communicate()[0].decode('utf-8')
        files = out.split()
        filenames = sorted(
            list(filter(lambda file: contains(file, filters), files)))

        return filenames

    # def set_directory(self, instrument: str) -> None:
    #     try:
    #         if not self.has_date():
    #             raise DateRequiredError
    #         self.directory = INSTRUMENT_LOCAL_PATH.substitute(
    #             instrument=instrument,
    #             year=self.year,
    #             month=self.month,
    #             day=self.day)
    #     except DateRequiredError as err:
    #         print(err)
    #
    # def make_directory(self) -> None:
    #     try:
    #         if not self.has_directory():
    #             raise DirectoryRequiredError
    #         if not os.path.exists(self.directory):
    #             os.makedirs(self.directory)
    #     except DirectoryRequiredError as err:
    #         print(err)
