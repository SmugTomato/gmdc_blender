from gmdc_data import *

gmdc.read_file_data()
gmdc.load_data()

print(gmdc.header.file_name)
