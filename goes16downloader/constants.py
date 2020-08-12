from string import Template
import os


INSTRUMENT_LOCAL_PATH = Template(
    os.path.join(
        '/'.join(os.path.abspath(os.path.dirname(__file__)).split(os.sep)[:-1]),
        'datasets/$instrument/$year/$month/$day'
    )
)

GLM_QUERY = Template(
    "aws s3 ls noaa-goes16/GLM-L2-LCFA/$year/$julian_day/$hour"
)
