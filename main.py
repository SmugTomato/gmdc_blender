# from .gmdc_data import *
# from .element_id import ElementID
# from .blender_model import BlenderModel

from gmdc_blender.rcol.gmdc import GMDC
from gmdc_blender.rcol.data_helper import DataHelper
from gmdc_blender.bone_data import BoneData
from gmdc_blender.element_id import element_ids
from gmdc_blender.element_id import ElementID

from gmdc_blender.rcol.rcol_data import Rcol
from gmdc_blender.blender_model import BlenderModel
import struct


def main():
    test_gmdc = GMDC.from_test_func('sims2_files/AdultTestMesh.5gd')
    test_gmdc.load_header()
    test_gmdc.load_data()
    test_gmdc.write('sims2_files/AdultTestMeshOUT.5gd')

    # test_rcol = Rcol.from_file_data('sims2_files/AdultTestMesh.5cr')
    # # test_rcol.print()
    #
    # arr = []
    # for block in test_rcol.data_blocks:
    #     if block.identity.identity == DataHelper.TRANSFORM_NODE and block.assigned_subset < 100:
    #         tup = (block.assigned_subset, block.objectgraph.filename)
    #         arr.append(tup)
    #
    # arr2 = sorted(arr, key=lambda x: x[0])
    # for tup in arr2:
    #     print (tup)

    #
    # bones = SkeletonBuilder.build(test_rcol.data_blocks)

    # for i, name in enumerate(SkeletonBuilder.bone_parent_table):
    #     print(i, '\t', name, sep="")
    #
    # test_gmdc = GMDC.from_test_func('sims2_files/UnderwearTest.5gd')
    # test_gmdc.load_header()
    # test_gmdc.load_data()
    #
    #
    # bmod = BlenderModel.groups_from_gmdc(test_gmdc)
    # print(bmod[0].morphs)


    # for pair in test_gmdc.model.name_pairs:
    #     print(pair)
    # print()
    #
    # for grp in test_gmdc.groups:
    #     print(grp.link_index)
    # print()
    #
    # for link in test_gmdc.linkages:
    #     for ind in link.indices:
    #         if test_gmdc.elements[ind].element_identity == ElementID.MORPH_VERTEX_MAP:
    #             print(
    #                 test_gmdc.elements[ind].identity_repitition,
    #                 element_ids[test_gmdc.elements[ind].element_identity]
    #             )
    #             for i, v in enumerate(test_gmdc.elements[ind].element_values):
    #                 print(i, v)

main()
