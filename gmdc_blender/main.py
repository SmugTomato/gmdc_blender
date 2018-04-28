# from .gmdc_data import *
# from .element_id import ElementID
# from .blender_model import BlenderModel

from gmdc_data import gmdc
import element_id


test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/TestMesh.5gd')
# test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ToddlerTestMesh.5gd')
test_gmdc.load_header()
test_gmdc.load_data()

for l in test_gmdc.linkages:
    for ref in l.indices:
        element = test_gmdc.elements[ref]
        print(hex(element.element_identity), '\tSet:', hex(element.set_format), '\tBlock:', hex(element.block_format), '\tLength:', len(element.element_values), '\t', element_id.element_ids[element.element_identity])

print()
for m in test_gmdc.model.name_pairs:
    print(m)
