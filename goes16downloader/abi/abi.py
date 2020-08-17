import sys; sys.path.insert(0, '/home/adriano/goes16-acquisition')
from goes16downloader import Downloader
import datetime as dt
from goes16downloader.constants import *


class ABIDownloader(Downloader):
    def __init__(self, **kwargs):
        super(ABIDownloader, self).__init__(**kwargs)
        self.time = kwargs.get('time', None)
        self.instrument = 'ABI-L2-MCMIPF'
        self.ARGS = dict(year=self.year, month=str(self.month).zfill(2),
                         day=str(self.day).zfill(2),
                         julian_day=str(self.julian_day).zfill(3),
                         hour=str(self.hour).zfill(2),
                         minute=str(self.minute).zfill(2),
                         instrument=self.instrument,
                         remote_url=self.remote_url, directory=self.directory)
        self.query_base = list()
        self.initializer()
        self.files_to_download = []
        self.directory = None

    def initializer(self) -> None:
        self.julian_day = self.get_julian_day()
        self.time = self.format_time()

        times = [dict(year=self.year, julian_day=self.time['julian_day'],
                      hour=self.time['hour'], minute=minute)
                 for minute in self.time['minute']]
        self.directory = INSTRUMENT_LOCAL_PATH.substitute(**self.ARGS)
        self.make_directory()
        self.query_base = QUERY_LIST_FILES.substitute(
            **self.time, instrument=self.instrument
        )
        self.remote_url = self.query_base.split(' ')[-1]
        self.files_to_download = self.get_and_select_files()
        self.download_files()

    def get_julian_day(self):
        return str(dt.datetime.strptime('%s-%s-%s' % (self.year, self.month,
                                                      self.day), '%Y-%m-%d').\
                   timetuple().tm_yday).zfill(3)


if __name__ == "__main__":
    info = dict(year=2020, month=8, day=14, hour=20, minute=0)
    glm = ABIDownloader(**info)









