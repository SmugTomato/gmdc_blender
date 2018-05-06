'''
Copyright (C) 2018 SmugTomato

Created by SmugTomato

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import bpy
import bmesh
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from mathutils import Vector

from .rcol.gmdc import GMDC
from .blender_model import BlenderModel
from .morphmap import MorphMap
from .bone_data import BoneData


class ExportGMDC(Operator, ExportHelper):
    """Sims 2 GMDC Exporter"""
    bl_idname = "export.gmdc_export"
    bl_label = "Sims 2 GMDC Export"
    bl_options = {'REGISTER', 'UNDO'}

    # ExportHelper mixin class uses this
    filename_ext = ".5gd"

    filter_glob = StringProperty(
            default="*.5gd",
            options={'HIDDEN'},
            maxlen=255,  # Max internal buffer length, longer would be clamped.
            )

    export_type = EnumProperty(
            name="Export",
            description="Choose an export method",
            items=(('SELECTED', "Selected", "Only export selected objects. (Recommended)"),
                   ('SCENE', "Scene", "Export all supported objects in the scene.")),
            default='SELECTED',
            )

    do_fix_weights = BoolProperty(
            name="Fix weights",
            description="Limit to 4 skin weights and normalize them.",
            default=True,
            )


    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select objects to export depending on user choice
        obs_to_export = []
        if self.export_type == 'SELECTED':
            scene_obs = bpy.context.selected_objects
            print('Selected only')
        else:
            scene_obs = bpy.context.scene.objects
            print('Scene')

        # Check for existance of necessary custom properties
        for ob in scene_obs:
            if ob.type == 'MESH':
                opacity = ob.data.get( 'opacity', None )
                # Internal GMDC filename, NOT the actual name of the file you save
                filename = ob.data.get( 'filename', None )
                if opacity and filename:
                    obs_to_export.append(ob)

        # Further sanity checks, check array length and existance of Armature modifier
        if len(obs_to_export) == 0:
            print('ERROR: No valid objects were found')
            return{'CANCELLED'}
        armature = obs_to_export[0].modifiers.get( 'Armature', None )
        if armature == None:
            print('ERROR: No armature modifier')
            return{'CANCELLED'}


        # Restructure bone data
        bones = BoneData.from_armature(armature.object)

        print(obs_to_export)

        # Continue export process
        b_models = []
        for ob in obs_to_export:
            b_models.append( ExportGMDC.build_group(ob, filename) )

        # Build gmdc
        gmdc_data = GMDC.build_data(b_models, bones)

        # Write data
        gmdc_data.write(self.filepath)


        return {'FINISHED'}


    @staticmethod
    def avg_vector(normals):
        i = 0
        total = Vector( (0,0,0) )
        for n in normals:
            total += n
            i += 1
        return total / i


    @staticmethod
    def build_group(object, filename):
        # Bmesh section
        mesh = object.data
        bm = bmesh.new()
        bm.from_mesh(mesh)


        # Triangulate faces
        bmesh.ops.triangulate(bm, faces=bm.faces)


        # Split UV seam edges
        edges_to_split = []
        old_normals = []
        for e in bm.edges:
            if e.seam:
                edges_to_split.append(e)

        bmesh.ops.split_edges(bm, edges=edges_to_split)

        # Rebuild normals
        normals = {}
        for i, v in enumerate(bm.verts):
            if tuple(v.co) not in normals:
                normals[ tuple(v.co) ] = [v.normal]
            else:
                normals[ tuple(v.co) ].append(v.normal)
        for i, key in enumerate(normals):
            normals[key] = ExportGMDC.avg_vector( normals[key] )
        for v in bm.verts:
            v.normal = normals[ tuple(v.co) ]


        bm.to_mesh(mesh)
        bm.free()

        vertices    = []
        normals     = []
        uvs         = []
        faces       = []
        bone_assign = []
        bone_weight = []
        name        = object.name
        filename    = mesh['filename']
        opacity     = mesh['opacity']

        # Vertices, normals and pre-populating uvs
        for vert in mesh.vertices:
            vertices.append( (-vert.co[0], -vert.co[1], vert.co[2]) )
            normals.append( (-vert.normal[0], -vert.normal[1], vert.normal[2]) )
            uvs.append( None )


        # Faces
        for f in mesh.polygons:
            faces.append( (f.vertices[0], f.vertices[1], f.vertices[2]) )


        # UVs
        uv_layer = mesh.uv_layers[0]
        for i, polygon in enumerate(mesh.polygons):
            for j, loopindex in enumerate(polygon.loop_indices):
                meshuvloop = mesh.uv_layers.active.data[loopindex]
                uv = ( meshuvloop.uv[0], -meshuvloop.uv[1] + 1 )
                vertidx = faces[i][j]
                uvs[vertidx] = uv


        # Vertex groups (Bone assignments and weights)
        for vert in mesh.vertices:
            assign = [255] * 4
            weight = [0] * 3
            for i, assignment in enumerate(vert.groups):
                if i < 3:
                    weight[i] = assignment.weight
                assign[i] = assignment.group
            bone_assign.append(assign)
            bone_weight.append(weight)


        # Morphs
        morphs = MorphMap.from_blender(mesh)
        morph_bytemap = MorphMap.make_bytemap(morphs, len(vertices))



        # bpy.ops.ed.undo()   # Undo triangulation
        return BlenderModel(vertices, normals, faces, uvs, name, bone_assign,
                            bone_weight, opacity, morphs, filename, morph_bytemap)


    def __do_export(objects, filename):
        pass
