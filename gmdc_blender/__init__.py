bl_info = {
    "name": "Sims 2 GMDC Tools",
    "category": "Import-Export",
	"version": (0, 0, 1),
	"blender": (2, 79, 0),
	"location": "File > Import/Export",
	"description": "Importer and exporter for Sims 2 GMDC(.5gd) files"
}
import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from .blender_import import ImportGMDC


def menu_func_im(self, context):
    self.layout.operator(ImportGMDC.bl_idname)

def register():
    bpy.utils.register_class(ImportGMDC)
    bpy.types.INFO_MT_file_import.append(menu_func_im)


def unregister():
    bpy.utils.unregister_class(ImportGMDC)
    bpy.types.INFO_MT_file_import.remove(menu_func_im)


if __name__ == "__main__":
    register()
