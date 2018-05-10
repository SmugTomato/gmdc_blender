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
    bl_label = "Sims 2 GMDC (.5gd)"
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
        # if armature == None:
        #     print('ERROR: No armature modifier')
        #     return{'CANCELLED'}


        # Restructure bone data
        has_armature = obs_to_export[0].modifiers.get( 'Armature', None ) != None
        bones = None
        if has_armature:
            bones = BoneData.from_armature(armature.object)

        print(obs_to_export)

        # Continue export process
        b_models = []
        for ob in obs_to_export:
            print(ob)
            b_models.append( ExportGMDC.build_group(ob, filename, has_armature) )

        # Build gmdc
        gmdc_data = GMDC.build_data(b_models, bones)

        # Write data
        gmdc_data.write(self.filepath)


        return {'FINISHED'}


    @staticmethod
    def recalc_normals(bm_mesh):
        # Run through all edges again, check if normals of their verts should be smoothed
        verts_to_smooth = {}
        for e in bm_mesh.edges:
            if not e.seam or not e.smooth:
                continue
            for v in e.verts:
                if tuple( v.co ) not in verts_to_smooth:
                    verts_to_smooth[ tuple( v.co ) ] = [ v ]
                    continue
                if v not in verts_to_smooth[ tuple( v.co ) ]:
                    verts_to_smooth[ tuple( v.co ) ].append( v )

        # Finally run all vertices given by above loop through the normal smooth function
        for vert in verts_to_smooth:
            total = Vector( (0,0,0) )
            for v in verts_to_smooth[vert]:
                total += v.normal
            avg = total / len(verts_to_smooth[vert])
            for v in verts_to_smooth[vert]:
                v.normal = avg


    @staticmethod
    def build_group(object, filename, has_armature):

        # Make a copy of the mesh to keep the original intact
        mesh = object.to_mesh(bpy.context.scene, False, 'RENDER', False, False)
        temp_obj = bpy.data.objects.new('temp_obj', mesh)
        bm = bmesh.new()
        bm.from_mesh(mesh)


        # Triangulate faces
        bmesh.ops.triangulate(bm, faces=bm.faces)

        ## RECALCULATING NORMALS
        # Get all edges to split (UV seams and Sharp edges)
        uvsplit = []
        for e in bm.edges:
            if e.seam or not e.smooth:
                uvsplit.append(e)

        # Split edges given by above loop
        bmesh.ops.split_edges(bm, edges=uvsplit)

        ExportGMDC.recalc_normals(bm)

        bm.to_mesh(mesh)
        bm.free()

        vertices    = []
        normals     = []
        tangents    = []
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
            vert.normal.normalize()
            normals.append( (-vert.normal[0], -vert.normal[1], vert.normal[2]) )


            c1 = vert.normal.cross(Vector( (0,1,0) )).normalized()
            c2 = vert.normal.cross(Vector( (0,0,1) )).normalized()

            if c1.length > c2.length:
                tangents.append(c1)
            else:
                tangents.append(c2)

            # tan = vert.normal.orthogonal().normalized()
            # tangents.append( (tan[0], tan[1], tan[2]) )
            # print(tan)
            uvs.append( None )


        # Faces
        for f in mesh.polygons:
            faces.append( (f.vertices[0], f.vertices[1], f.vertices[2]) )


        # Tangents
        mesh.calc_tangents()

        # tangents = [0] * len(vertices)
        # for i, polygon in enumerate(mesh.polygons):
        #     for j, vert in enumerate([mesh.loops[z] for z in polygon.loop_indices]):
        #         tan = ( vert.tangent[0], vert.tangent[1], vert.tangent[2] )
        #         tangents[polygon.vertices[j]] = tan
        #         print(tan, vert.tangent)


        # UVs
        uv_layer = mesh.uv_layers[0]
        print(uv_layer, name)
        for i, polygon in enumerate(mesh.polygons):
            for j, loopindex in enumerate(polygon.loop_indices):
                meshuvloop = mesh.uv_layers.active.data[loopindex]
                uv = ( meshuvloop.uv[0], -meshuvloop.uv[1] + 1 )
                vertidx = faces[i][j]
                uvs[vertidx] = uv
        print(uvs)
        print()


        # Vertex groups (Bone assignments and weights)
        if has_armature:
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
        morphs = []
        morph_bytemap = None
        if mesh.shape_keys:

            temp_obj.show_only_shape_key = True

            # Recalculate normals for each morph and then create it
            for key in temp_obj.data.shape_keys.key_blocks[1:]:
                # Set active shape key
                idx = temp_obj.data.shape_keys.key_blocks.find(key.name)
                temp_obj.active_shape_key_index = idx

                # Create a copy from active shape key
                morphmesh = temp_obj.to_mesh(bpy.context.scene, True, 'RENDER', False, False)

                # Initialize bmesh
                morph_bm = bmesh.new()
                morph_bm.from_mesh(morphmesh)

                # Recalculate normals and create morph
                ExportGMDC.recalc_normals(morph_bm)

                # Remove copied mesh
                morph_bm.to_mesh(morphmesh)
                morph_bm.free()

                # Create morph and remove copied mesh
                morphs.append( MorphMap.from_blender(mesh, morphmesh, key.name) )
                bpy.data.meshes.remove(morphmesh)


            temp_obj.active_shape_key_index = 0
            temp_obj.show_only_shape_key = False



            morph_bytemap = MorphMap.make_bytemap(morphs, len(vertices))


        # Remove copied mesh once done
        bpy.data.meshes.remove(mesh)

        # bpy.ops.ed.undo()   # Undo triangulation
        return BlenderModel(vertices, normals, tangents, faces, uvs, name, bone_assign,
                            bone_weight, opacity, morphs, filename, morph_bytemap)


    def __do_export(objects, filename):
        pass
