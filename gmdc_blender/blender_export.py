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
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

from .rcol.gmdc import GMDC
from .blender_model import BlenderModel


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
            name="Objects",
            description="Choose an export method",
            items=(('SELECTED', "Selected only", "Only export selected objects. (Recommended)"),
                   ('SCENE', "Scene", "Export all supported objects in the scene.")),
            default='SELECTED',
            )


    def execute(self, context):
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
            return{'ERROR'}
        armature = obs_to_export[0].modifiers.get( 'Armature', None )
        if armature == None:
            print('ERROR: No armature modifier')
            return{'ERROR'}


        # Continue export process
        # b_models = BlenderModel.from_blender(obs_to_export, filename)
        ExportGMDC.build_group(obs_to_export[0])



        return {'FINISHED'}


    @staticmethod
    def build_group(object, filename):
        # Triangulate before exporting
        bpy.context.scene.objects.active = object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED', ngon_method='BEAUTY')
        bpy.ops.object.mode_set(mode='OBJECT')

        mesh = object.data

        vertices    = []
        normals     = []
        uvs         = []
        faces       = []
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
        uv_layer = mesh.uv_layers['UVMap']
        for i, polygon in enumerate(mesh.polygons):
            for j, loopindex in enumerate(polygon.loop_indices):
                meshuvloop = mesh.uv_layers.active.data[loopindex]
                uv = ( meshuvloop.uv[0], -meshuvloop.uv[1] - 1 )
                vertidx = faces[i][j]
                uvs[vertidx] = uv


        return BlenderModel(vertices, normals, faces, uvs, name, None,
                            None, opacity, None, filename)


    def __do_export(objects, filename):
        pass
