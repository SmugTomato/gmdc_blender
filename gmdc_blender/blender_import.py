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
        b_model = self.parse_data(context, self.filepath)

        if b_model != False:
            self.do_import(b_model)

        return {'FINISHED'}


    def parse_data(self, context, filepath):
        gmdc_data = GMDC.from_file_data(context, filepath)

        if gmdc_data.load_header() == False:
            print ('Unsupported GMDC version', hex(gmdc_data.header.file_type))
            return False

        gmdc_data.load_data()
        b_model = blender_model.BlenderModel.from_gmdc(gmdc_data)
        return b_model


    def do_import(self, b_model):
        # Create object and mesh
        mesh = bpy.data.meshes.new(b_model.name)
        object = bpy.data.objects.new(b_model.name, mesh)
        bpy.context.scene.objects.link(object)

        # Load vertices and faces
        mesh.from_pydata(b_model.vertices, [], b_model.faces)

        # Load normals
        for i in range(0,len(mesh.vertices)):
            mesh.vertices[i].normal = b_model.normals[i]

        # Create UV layer and load UV coordinates
        mesh.uv_textures.new('UVMap')
        for i, polygon in enumerate(mesh.polygons):
            for j, loopindex in enumerate(polygon.loop_indices):
                meshuvloop = mesh.uv_layers.active.data[loopindex]

                vertex_index = b_model.faces[i][j]
                meshuvloop.uv = b_model.uvs[vertex_index]

        # Create vertex groups for bone assignments
