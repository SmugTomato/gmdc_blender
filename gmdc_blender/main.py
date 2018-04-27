from .gmdc_data import *
from .element_id import ElementID
from .blender_model import BlenderModel

def import_gmdc(context, filepath):
    gmdc.read_file_data(context, filepath)
    gmdc.load_data()

    print('Byte Offset:', gmdc.byte_offset, '/', len(gmdc.file_data))

    b_model = BlenderModel.from_gmdc()
