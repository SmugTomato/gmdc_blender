# from .gmdc_data import *
# from .element_id import ElementID
# from .blender_model import BlenderModel

from gmdc_data import gmdc
import element_id


test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ChildTestMesh.5gd')
# test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ToddlerTestMesh.5gd')
test_gmdc.load_header()
test_gmdc.load_data()

# for j, l in enumerate(test_gmdc.linkages):
#     print('Linkage index:', j)
#     for i, ref in enumerate(l.indices):
#         element = test_gmdc.elements[ref]
#         print(i, hex(element.element_identity), '\tSet:', hex(element.set_format), '\tBlock:', hex(element.block_format), '\tLength:', len(element.element_values), '\t', element_id.element_ids[element.element_identity])
#     print()
#
# print()
# for m in test_gmdc.model.name_pairs:
#     print(m)
# print()


# Model load test
# Load every group in the mesh, then load needed data from them
groups = []
for g in test_gmdc.groups:
    # Load single group from a linkage

    # Get all linked elements
    elements = []
    for e in test_gmdc.linkages[g.link_index].indices:
        elements.append(e)
    groups.append(elements)
    # print(g.link_index, groups[g.link_index], g.name)

for i, g in enumerate(groups):
    print(test_gmdc.groups[i].name)
    for e in g:
        element = test_gmdc.elements[e]
        print('Element:', e, '\t', hex(element.element_identity), '\tLength:', len(element.element_values), '\t', element_id.element_ids[element.element_identity])
    print()
