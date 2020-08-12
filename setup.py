from core.acquisition import Acquisition

# sensor = 'ABI-L2-CMIPF'
sensor = 'GLM-L2-LCFA'
DOWN_OUT = '/home/adriano/earth-observation'
CSV_OUT = '/home/adriano/earth-observation/data'
glm = Acquisition(sensor=sensor, csvfile_out=CSV_OUT, download_out=DOWN_OUT)
# glm.download_out = 'db'
glm.download()
glm.create_dataframe('flash', remove_download_files=False)

