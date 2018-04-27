from gmdc_data import *

gmdc.read_file_data()
gmdc.load_data()

print('\nByte Offset:', gmdc.byte_offset, '/', len(gmdc.file_data))
