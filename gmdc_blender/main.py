from gmdc_data import *

gmdc.read_file_data()
gmdc.load_data()

for e in gmdc.elements:
    print(hex(e.element_identity), gmdc.element_ids[e.element_identity])
