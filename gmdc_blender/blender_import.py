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
from .skeleton_builder import SkeletonBuilder

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

        cres_path = self.filepath.replace('.5gd', '.5cr')
        cres = Rcol.from_file_data(cres_path)

        self.import_skeleton(cres)

        self.vert_groups = []
        for block in cres.data_blocks:
            if block.identity.identity == DataHelper.TRANSFORM_NODE:
                if block.assigned_subset != 0x7fffffff:
                    self.vert_groups.append( block.objectgraph.filename )
        # print(self.vert_groups)

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
        bones_info = SkeletonBuilder.build(data.data_blocks)

        # Create armature and object
        name = 'Skel'
        bpy.ops.object.add(
            type='ARMATURE',
            enter_editmode=True,
            location=(0,0,0))
        ob = bpy.context.object
        ob.show_x_ray = True
        ob.name = name
        amt = ob.data
        amt.name = name+'Amt'
        amt.show_axes = True

        boneTable = [
            ('Base', None, (1,0,0)),
            ('Mid', 'Base', (1,0,0)),
            ('Tip', 'Mid', (0,0,1))
        ]

        # Create bones
        bpy.ops.object.mode_set(mode='EDIT')
        # for (bname, pname, vector) in boneTable:
        for b in bones_info:
            bone = amt.edit_bones.new(b.name)
            rot = Quaternion(b.rotation)
            trans = Vector(b.position)
            if b.parent != -1:
                b_parent = bones_info[b.parent]
                parent = amt.edit_bones[b_parent.name]
                bone.parent = parent
                bone.head = parent.tail
                bone.use_connect = False
                # (trans_p, rot_p, scale_p) = parent.matrix.decompose()
                # rot = rot * rot_p
                # trans = trans - trans_p
            else:
                bone.head = Vector(trans)
            bone.tail = rot * Vector(trans) + bone.head
            print(rot.magnitude)
        bpy.ops.object.mode_set(mode='OBJECT')



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
        for grp in self.vert_groups:
            object.vertex_groups.new(grp)
