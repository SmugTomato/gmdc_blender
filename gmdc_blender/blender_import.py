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
        b_models = self.parse_data(context, self.filepath)

        if b_models != False:
            for model in b_models:
                self.do_import(model)

        return {'FINISHED'}


    def parse_data(self, context, filepath):
        gmdc_data = GMDC.from_file_data(context, filepath)

        if gmdc_data.load_header() == False:
            print ('Unsupported GMDC version', hex(gmdc_data.header.file_type))
            return False

        gmdc_data.load_data()
        b_models = blender_model.BlenderModel.groups_from_gmdc(gmdc_data)
        return b_models


    def do_import(self, b_model):
        print('Importing group:', b_model.name)

        # Create object and mesh
        mesh = bpy.data.meshes.new(b_model.name)
        object = bpy.data.objects.new(b_model.name, mesh)
        bpy.context.scene.objects.link(object)

        # Load vertices and faces
        mesh.from_pydata(b_model.vertices, [], b_model.faces)

        # Load normals
        for i, vert in enumerate(mesh.vertices):
            vert.normal = b_model.normals[i]
            pass
        # print(len(mesh.vertices), len(b_model.vertices))

        # Create UV layer and load UV coordinates
        mesh.uv_textures.new('UVMap')
        for i, polygon in enumerate(mesh.polygons):
            for j, loopindex in enumerate(polygon.loop_indices):
                meshuvloop = mesh.uv_layers.active.data[loopindex]

                vertex_index = b_model.faces[i][j]
                meshuvloop.uv = b_model.uvs[vertex_index]

        # Create vertex groups for bone assignments
