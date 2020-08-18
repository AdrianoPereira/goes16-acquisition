import sys; sys.path.insert(0, "/home/adriano/goes16-acquisition")
"""
This is a file to download the data from the GOES Satellite (ABI and GLM) during
the tornado that reach the Brazilian state of Santa Catarina.
https://g1.globo.com/sc/santa-catarina/noticia/2020/08/15/tornado-deixa-casas-destruidas-no-norte-de-sc-eu-nao-me-contava-vivo-mais-diz-produtor-rural.ghtml
"""
from goes16downloader.abi import ABIDownloader
from goes16downloader.glm import GLMDownloader
import numpy as np
from datetime import datetime as dt


def get_list_datetimes():
    year = 2020
    month = 8
    days = [14, 15]
    hours =  np.arange(0, 24)
    minutes = np.arange(0, 60, 10)

    list_datetimes = list()

    for day in days:
        for hour in hours:
            for minute in minutes:
                datetime = dict(year=year, month=month, day=day, hour=hour,
                                minute=minute)
                list_datetimes.append(datetime)

    return list_datetimes


def download_abi_files(list_datetimes):
    for datetime in list_datetimes:
        ABIDownloader(**datetime, channels=[8, 13])


def download_glm_files(list_datetimes):
    for datetime in list_datetimes:
        GLMDownloader(**datetime)


if __name__ == "__main__":
    list_datetimes = get_list_datetimes()
    # download_glm_files(list_datetimes)
    download_abi_files(list_datetimes)
