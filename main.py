# from .gmdc_data import *
# from .element_id import ElementID
# from .blender_model import BlenderModel

from io_sims2gmdc.rcol.gmdc import GMDC
# from io_sims2gmdc.rcol.data_helper import DataHelper
from io_sims2gmdc.bone_data import BoneData
from io_sims2gmdc.element_id import element_ids
from io_sims2gmdc.element_id import ElementID

# from io_sims2gmdc.rcol.rcol_data import Rcol
from io_sims2gmdc.blender_model import BlenderModel
import struct


def main():
    testgmdc = GMDC.from_file_data('sims2_files/Table/Tbale_Mesh.5gd')
    testgmdc.load_header()
    testgmdc.load_data()

    testmod = BlenderModel.from_gmdc(testgmdc, testgmdc, 0)

    for grp in testgmdc.groups:
        print( 'Link index:\t', grp.link_index )
        print( 'Name:\t\t', grp.name )
        print( 'Faces:\t\t', len(grp.faces) )
    print(len(testgmdc.elements))
    print()



main()
