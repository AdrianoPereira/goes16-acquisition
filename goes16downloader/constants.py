from string import Template
import os


INSTRUMENT_LOCAL_PATH = Template(
    os.path.join(
        os.path.join(os.environ['HOME'], '.goes16downloader'),
        'datasets/$instrument/$year/$month/$day/'
    )
)

GLM_QUERY_LIST_FILES = Template(
    "aws s3 ls noaa-goes16/GLM-L2-LCFA/$year/$julian_day/$hour/"
)

