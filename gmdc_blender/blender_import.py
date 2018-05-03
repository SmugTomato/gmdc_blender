import bpy, math
import bmesh
from mathutils import Vector, Matrix, Quaternion
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from .rcol.gmdc import GMDC
from .rcol.rcol_data import Rcol
from .rcol.data_helper import DataHelper
from . import blender_model
from .bone_data import BoneData

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
        gmdc_data = GMDC.from_file_data(self.filepath)
        if gmdc_data.load_header() == False:
            print ('Unsupported GMDC version', hex(gmdc_data.header.file_type))
            return False

        gmdc_data.load_data()
        b_models = blender_model.BlenderModel.groups_from_gmdc(gmdc_data)

        armature = self.import_skeleton(gmdc_data)

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



    def import_skeleton(self, data):
        skeldata = BoneData.build_bones(data)

        # Create armature and object
        name = 'Armature'
        bpy.ops.object.add(
            type='ARMATURE',
            enter_editmode=True,
            location=(0,0,0))
        # Armature object
        ob = bpy.context.object
        ob.show_x_ray = True
        ob.name = name
        # Armature
        amt = ob.data
        amt.draw_type = 'STICK'

        # Create bones from skeldata
        for bonedata in skeldata:
            bone = amt.edit_bones.new(bonedata.name)
            trans = Vector(bonedata.position)
            rot = Quaternion(bonedata.rotation)
            bone.tail = rot * trans
            if bonedata.parent != None:
                parent = amt.edit_bones[bonedata.parent]
                bone.parent = parent
                bone.head = parent.tail
            if bone.tail == bone.head:
                # Blender does not support 0 length bones
                bone.tail += Vector((0,0.00001,0))

            # Enter custom properties for exporting later
            # # Translate Vector
            bone['tX'] = bonedata.position[0]
            bone['tY'] = bonedata.position[1]
            bone['tZ'] = bonedata.position[2]
            # # Rotation Quaternion
            bone['rW'] = bonedata.rotation[0]
            bone['rX'] = bonedata.rotation[1]
            bone['rY'] = bonedata.rotation[2]
            bone['rZ'] = bonedata.rotation[3]


        # Go back to Object mode, scale the armature -1 along Z and apply the transform
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.transform.resize(value=(1, 1, -1))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        # Return the Armature object
        return ob


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
        # for grp in self.vert_groups:
        #     object.vertex_groups.new(grp)
