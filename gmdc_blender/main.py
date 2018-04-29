# from .gmdc_data import *
# from .element_id import ElementID
# from .blender_model import BlenderModel

from rcol_data import gmdc, cres
import element_id


test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ChildTestMesh.5gd')
# test_gmdc = gmdc.GMDC.from_test_func('../sims2_files/ToddlerTestMesh.5gd')
test_gmdc.load_header()
test_gmdc.load_data()

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

# def main():
#     # CRES Load test
#     test_cres = cres.CRES.from_test_func('../sims2_files/AdultTestMesh.5cr')
#     test_cres.load_header()
#     test_cres.load_data()

# main()
