# from .gmdc_data import *
# from .element_id import ElementID
# from .blender_model import BlenderModel

from rcol.gmdc import GMDC
from rcol.rcol_data import Rcol
from rcol.data_helper import DataHelper


# test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ChildTestMesh.5gd')
# # test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ToddlerTestMesh.5gd')
# test_gmdc.load_header()
# test_gmdc.load_data()

# # Model load test
# # Load every group in the mesh, then load needed data from them
# groups = []
# for g in test_gmdc.groups:
#     # Load single group from a linkage

#     # Get all linked elements
#     elements = []
#     for e in test_gmdc.linkages[g.link_index].indices:
#         elements.append(e)
#     groups.append(elements)
#     # print(g.link_index, groups[g.link_index], g.name)

# for i, g in enumerate(groups):
#     print(test_gmdc.groups[i].name)
#     for e in g:
#         element = test_gmdc.elements[e]
#         print('Element:', e, '\t', hex(element.element_identity), '\tLength:', len(element.element_values), '\t', element_id.element_ids[element.element_identity])
#     print()

def main():
    test_rcol = Rcol.from_test_func('../sims2_files/AdultTestMesh.5cr')
    test_rcol.print()

    count = 0
    for ob in test_rcol.data_blocks:
        if ob.identity.identity == DataHelper.TRANSFORM_NODE:
            count += 1
    print(count)

main()