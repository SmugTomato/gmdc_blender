# '''
# Copyright (C) 2018 SmugTomato
#
# Created by SmugTomato
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# '''
#
#
# bl_info = {
#     "name": "Sims 2 GMDC Tools",
#     "category": "Import-Export",
# 	"version": (0, 0, 1),
# 	"blender": (2, 79, 0),
# 	"location": "File > Import/Export",
# 	"description": "Importer and exporter for Sims 2 GMDC(.5gd) files"
# }
# import bpy
# from bpy_extras.io_utils import ImportHelper
# from bpy.props import StringProperty, BoolProperty, EnumProperty
# from bpy.types import Operator
#
# from .blender_import import ImportGMDC
# from .blender_export import ExportGMDC
#
#
# def menu_func_im(self, context):
#     self.layout.operator(ImportGMDC.bl_idname)
#
# def menu_func_ex(self, context):
#     self.layout.operator(ExportGMDC.bl_idname)
#
# def register():
#     bpy.utils.register_class(ImportGMDC)
#     bpy.utils.register_class(ExportGMDC)
#     bpy.types.INFO_MT_file_import.append(menu_func_im)
#     bpy.types.INFO_MT_file_export.append(menu_func_ex)
#
#
# def unregister():
#     bpy.utils.unregister_class(ImportGMDC)
#     bpy.utils.unregister_class(ExportGMDC)
#     bpy.types.INFO_MT_file_import.remove(menu_func_im)
#     bpy.types.INFO_MT_file_export.remove(menu_func_ex)
#
#
# if __name__ == "__main__":
#     register()
