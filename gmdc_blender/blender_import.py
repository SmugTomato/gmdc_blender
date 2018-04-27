import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from .gmdc_data import gmdc
from . import blender_model

class ImportGMDC(Operator, ImportHelper):
    """Sims 2 GMDC Importer"""
    bl_idname = "import.gmdc_import"
    bl_label = "Sims 2 GMDC (.5gd)"
    bl_options = {'REGISTER', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".5gd"

    filter_glob = StringProperty(
            default="*.5gd",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    def execute(self, context):
        do_import(context, self.filepath)

        return {'FINISHED'}

def do_import(context, filepath):
    gmdc.read_file_data(context, filepath)
    gmdc.load_data()

    print('Byte Offset:', gmdc.byte_offset, '/', len(gmdc.file_data))

    #  Execute actual import code
    b_model = blender_model.BlenderModel.from_gmdc()

    my_mesh = bpy.data.meshes.new(b_model.name)
    my_object = bpy.data.objects.new(b_model.name, my_mesh)

    my_object.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(my_object)

    my_mesh.from_pydata(b_model.vertices, [], b_model.faces)
