import sys; sys.path.insert(0, '/home/adriano/goes16-acquisition')
from goes16downloader import Downloader
import datetime as dt
from goes16downloader.constants import *


class GLMData(Downloader):
    def __init__(self, **kwargs):
        super(GLMData, self).__init__(**kwargs)
        self.ARGS = dict(year=self.year, month=self.month, day=self.day,
                         julian_day=self.julian_day, hour=self.hour,
                         minute=self.minute)
        self.time = kwargs.get('time', None)
        self.queries = list()
        self.initializer()

    def download(self):
        pass

    def initializer(self) -> None:
        self.julian_day = self.get_julian_day()
        self.time = self.format_time()

        times = [dict(year=self.year, julian_day=self.time['julian_day'],
                      hour=self.time['hour'], minute=minute)
                 for minute in self.time['minute'] ]

        self.queries = [GLM_QUERY.substitute(time) for time in times]
        print(self.queries[0])

    def get_julian_day(self):
        return str(dt.datetime.strptime('%s-%s-%s' % (self.year, self.month,
                                                      self.day), '%Y-%m-%d').\
                   timetuple().tm_yday).zfill(3)



if __name__ == "__main__":
    info = dict(year=2020, month=8, day=11, hour=0, minute=0)
    glm = GLMData(**info)









