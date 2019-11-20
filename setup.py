from core.acquisition import Acquisition

sensor = 'ABI-L2-CMIPF'
sensor = 'GLM-L2-LCFA'
glm = Acquisition(sensor=sensor, csvfile_out='here', download_out='data')
glm.download()
