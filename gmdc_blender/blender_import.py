import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from .gmdc_data.gmdc import GMDC
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
    gmdc_data = GMDC.from_file_data(context, filepath)

    # a = gmdc_data.load_header()

    if gmdc_data.load_header() == False:
        print ('Unsupported GMDC version', hex(gmdc_data.header.file_type))
        return {'ERROR'}

    print('Version:', gmdc_data.header.version)

    gmdc_data.load_data()

    print('Byte Offset:', gmdc_data.data_read.byte_offset, '/', len(gmdc_data.data_read.file_data))

    #  Execute actual import code
    b_model = blender_model.BlenderModel.from_gmdc(gmdc_data)

    my_mesh = bpy.data.meshes.new(b_model.name)
    my_object = bpy.data.objects.new(b_model.name, my_mesh)

    my_object.location = bpy.context.scene.cursor_location
    bpy.context.scene.objects.link(my_object)

    # my_mesh.from_pydata(b_model.vertices, [], b_model.faces)
    my_mesh.from_pydata(b_model.vertices, [], b_model.faces)

    # Load normals
    # my_mesh.flip_normals()
    for i in range(0,len(my_mesh.vertices)):
        my_mesh.vertices[i].normal = b_model.normals[i]

    # Load UV
    my_mesh.uv_textures.new('UVMap')

    for i, polygon in enumerate(my_mesh.polygons):
        for j, loopindex in enumerate(polygon.loop_indices):
            meshloop = my_mesh.loops[j]
            meshuvloop = my_mesh.uv_layers.active.data[loopindex]
            meshvertex = my_mesh.vertices[meshloop.vertex_index]

            vertex_index = b_model.faces[i][j]
            meshuvloop.uv = b_model.uvs[vertex_index]

            # new_vertex_index =

            # b_model.vertices[vertex_index]
            # print(meshvertex.x)



    # my_mesh.update(calc_edges=True)
