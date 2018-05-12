import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Operator,
                       PropertyGroup,
                       )


NECKFIX = {
    'NONE':   -1,
    'AF':     0,
    'AM':     1,
    'TF':     2,
    'TM':     3,
    'CU':     4,
    'PU':     5
}


class MySettings(PropertyGroup):

    is_shadow = BoolProperty(
        name="Shadow mesh",
        description="Is this group a shadow mesh?",
        )

    mesh_type = EnumProperty(
        name="Bodymesh Type",
        description="Type of this bodymesh (Top/Bottom/Body)",
        items=[ ('TOP', "Top mesh", ""),
                ('BOT', "Bottom/Body mesh", ""),
               ],
        default='BOT'
        )

    morph_type = EnumProperty(
        name="Morph Type",
        description="Type of morph to add",
        items=[ ('FAT', "Fat", ""),
                ('PREG', "Pregnant", ""),
               ],
        default='FAT'
        )

    neckfix_type = EnumProperty(
        name="Neck fix",
        description="Neck normals fix to apply",
        items=[ ('AF', "Adult Female", ""),
                ('AM', "Adult Male", ""),
                ('TF', "Teen Female", ""),
                ('TM', "Teen Male", ""),
                ('CU', "Child", ""),
                ('PU', "Toddler", ""),
                ('NONE', "None", ""),
               ],
        default='NONE'
        )


class MyOperator(bpy.types.Operator):
    bl_label = "Add Morph"
    bl_idname = "gmdc.morphs_add_morph"

    def execute(self, context):
        mytool = context.scene.my_tool
        obj = bpy.context.scene.objects.active


        if not obj.data.shape_keys:
            # Blender always needs a base shape key
            shpkey = obj.shape_key_add(from_mix=False)
            shpkey.name = "Basis"


        # Check morph count
        if len(obj.data.shape_keys.key_blocks) > 4:
            print("Too many morphs")
            return {'CANCELLED'}


        # Select proper morph name
        morphname = None
        if mytool.mesh_type == 'TOP':
            if mytool.morph_type == 'FAT':
                morphname = "topmorphs, fattop"
            if mytool.morph_type == 'PREG':
                morphname = "topmorphs, pregtop"
        if mytool.mesh_type == 'BOT':
            if mytool.morph_type == 'FAT':
                morphname = "botmorphs, fatbot"
            if mytool.morph_type == 'PREG':
                morphname = "botmorphs, pregbot"


        # Return on duplicate names
        for key in obj.data.shape_keys.key_blocks:
            if key.name == morphname:
                print("Morph already present")
                return {'CANCELLED'}


        shpkey = obj.shape_key_add(from_mix=False)
        shpkey.name = morphname

        return {'FINISHED'}


class UpdateMorphNames(bpy.types.Operator):
    bl_label = "Update Morph names"
    bl_idname = "gmdc.morphs_update_names"

    def execute(self, context):
        mytool = context.scene.my_tool
        obj = bpy.context.scene.objects.active

        if not obj.data.shape_keys:
            print('No morphs present.')
            return {'CANCELLED'}

        for key in obj.data.shape_keys.key_blocks[1:]:
            if mytool.mesh_type == 'TOP':
                key.name = key.name.replace("bot", "top")
            elif mytool.mesh_type == 'BOT':
                key.name = key.name.replace("top", "bot")

        return {'FINISHED'}


class UpdateNeckFix(bpy.types.Operator):
    bl_label = "Update Applied Neckseam fix"
    bl_idname = "gmdc.fixes_neckseam"

    def execute(self, context):
        mytool = context.scene.my_tool
        obj = bpy.context.scene.objects.active

        global NECKFIX
        obj.data["neck_fix"] = NECKFIX[mytool.neckfix_type]

        return {'FINISHED'}


class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Sims 2 GMDC Tools Panel"
    bl_idname = "SCENE_PT_gmdctools"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"


    def draw(self, context):
        layout = self.layout

        scene = context.scene
        obj = scene.objects.active

        # Import/Export buttons
        row = layout.row()
        row.operator("import.gmdc_import", text="Import...", icon='IMPORT')
        row.operator("export.gmdc_export", text="Export...", icon='EXPORT')

        #print(scene.objects.active)

        if obj and obj.select and obj.type == 'MESH':
            self.draw_object(obj, scene)

        if obj and obj.select and obj.type == 'EMPTY':
            self.draw_container(obj, scene)


    def draw_container(self, obj, scene):
        layout = self.layout
        layout.separator()

        layout.label(text="Container Properties:")
        box = layout.box()
        col = box.column()
        col.label(text=obj.name, icon='GROUP')

        box.prop(obj, "name")



    def draw_object(self, obj, scene):
        layout = self.layout
        mytool = scene.my_tool

        if obj.parent:
            self.draw_container(obj.parent, scene)

        # Group properties
        layout.separator()
        layout.label("Group Properties:")

        box = layout.box()
        col = box.column()
        col.label(text=obj.name, icon='MESH_CUBE')

        box.prop(obj, "name")

        if obj.data.get("opacity") != None:
            row = box.row()
            row.label("Opacity:")
            row.prop(obj.data, '["opacity"]', text="")

        if obj.data.get("is_shadow") != None:
            row = box.row()
            row.label("Shadowmesh:")
            row.prop(obj.data, '["is_shadow"]', text="")

        if obj.data.get("calc_tangents") != None and not obj.data.get("is_shadow"):
            row = box.row()
            row.label("Calculate Tangents:")
            row.prop(obj.data, '["calc_tangents"]', text="")


        # MORPHS
        box2 = layout.box()
        box2.label(text="Morphs:", icon='SHAPEKEY_DATA')

        col = box2.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "mesh_type", expand=True)
        col.operator("gmdc.morphs_update_names", text="Update morph names")

        if obj.data.shape_keys:

            for i, key in enumerate(obj.data.shape_keys.key_blocks[1:]):
                box = box2.box()
                row = box.row(align=True)
                row.label(text="Morph " + str(i) + ":")
                row.label(text=key.name)

        col = box2.column(align=True)
        row = col.row(align=True)
        row.prop(mytool, "morph_type", expand=True)
        col.operator("gmdc.morphs_add_morph", text="Add Morph")


        # FIXES
        fixes = layout.box()
        fixes.label(text="Fixes:", icon='MODIFIER')

        col = fixes.column(align=True)
        row = col.row(align=True)
        row.operator("gmdc.fixes_neckseam", text="Apply neck fix")
        row.prop(mytool, "neckfix_type", expand=False, text="")






def register():
    bpy.utils.register_class(HelloWorldPanel)

    bpy.utils.register_class(MyOperator)
    bpy.utils.register_class(UpdateMorphNames)
    bpy.utils.register_class(UpdateNeckFix)

    bpy.utils.register_class(MySettings)
    bpy.types.Scene.my_tool = PointerProperty(type=MySettings)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)

    bpy.utils.unregister_class(MyOperator)
    bpy.utils.unregister_class(UpdateMorphNames)
    bpy.utils.unregister_class(UpdateNeckFix)

    bpy.utils.unregister_class(MySettings)
    del bpy.types.Scene.my_tool


if __name__ == "__main__":
    register()
