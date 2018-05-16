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


class PROP_GmdcSettings(PropertyGroup):

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


class OP_AddMorph(bpy.types.Operator):
    bl_label = "Add Morph"
    bl_idname = "gmdc.morphs_add_morph"

    def execute(self, context):
        gmdc_props = context.scene.gmdc_props
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
        type = None
        if gmdc_props.morph_type == 'FAT':
            type = "fat"
            if gmdc_props.mesh_type == 'TOP':
                morphname = "topmorphs, fattop"
            if gmdc_props.mesh_type == 'BOT':
                morphname = "topmorphs, pregtop"

        if gmdc_props.morph_type == 'PREG':
            type = "preg"
            if gmdc_props.morph_type == 'FAT':
                morphname = "botmorphs, fatbot"
            if gmdc_props.morph_type == 'PREG':
                morphname = "botmorphs, pregbot"


        # Return on duplicate names
        for key in obj.data.shape_keys.key_blocks:
            if type in key.name:
                print("Morph already present")
                return {'CANCELLED'}


        shpkey = obj.shape_key_add(from_mix=False)
        shpkey.name = morphname

        return {'FINISHED'}


class OP_UpdateMorphNames(bpy.types.Operator):
    bl_label = "Update Morph names"
    bl_idname = "gmdc.morphs_update_names"

    def execute(self, context):
        gmdc_props = context.scene.gmdc_props
        obj = bpy.context.scene.objects.active

        if not obj.data.shape_keys:
            print('No morphs present.')
            return {'CANCELLED'}

        for key in obj.data.shape_keys.key_blocks[1:]:
            if gmdc_props.mesh_type == 'TOP':
                key.name = key.name.replace("bot", "top")
            elif gmdc_props.mesh_type == 'BOT':
                key.name = key.name.replace("top", "bot")

        return {'FINISHED'}


class OP_UpdateNeckFix(bpy.types.Operator):
    bl_label = "Update Applied Neckseam fix"
    bl_idname = "gmdc.fixes_neckseam"

    def execute(self, context):
        gmdc_props = context.scene.gmdc_props
        obj = bpy.context.scene.objects.active

        global NECKFIX
        obj["neck_fix"] = NECKFIX[gmdc_props.neckfix_type]

        return {'FINISHED'}


class OP_HideShadows(bpy.types.Operator):
    bl_label = "Hide all shadow meshes"
    bl_idname = "gmdc.shadow_hide"

    def execute(self, context):
        obj = bpy.context.scene.objects.active
        if obj.parent:
            obj = obj.parent

        for ob in bpy.context.scene.objects:
            if ob.get("is_shadow") == True and ob.parent == obj:
                ob.hide = True

        return {'FINISHED'}


class OP_UnhideShadows(bpy.types.Operator):
    bl_label = "Unhide all shadow meshes"
    bl_idname = "gmdc.shadow_unhide"

    def execute(self, context):
        obj = bpy.context.scene.objects.active
        if obj.parent:
            obj = obj.parent

        for ob in bpy.context.scene.objects:
            if ob.get("is_shadow") == True and ob.parent == obj:
                ob.hide = False

        return {'FINISHED'}


class OP_UnHideArmature(bpy.types.Operator):
    bl_label = "Unhide Armature"
    bl_idname = "gmdc.armature_unhide"

    def execute(self, context):
        obj = bpy.context.scene.objects.active
        if obj.parent:
            obj = obj.parent

        for ob in bpy.context.scene.objects:
            if ob.type == 'ARMATURE' and ob.parent == obj:
                ob.hide = False

        return {'FINISHED'}


class OP_HideArmature(bpy.types.Operator):
    bl_label = "Hide Armature"
    bl_idname = "gmdc.armature_hide"

    def execute(self, context):
        obj = bpy.context.scene.objects.active
        if obj.parent:
            obj = obj.parent

        for ob in bpy.context.scene.objects:
            if ob.type == 'ARMATURE' and ob.parent == obj:
                ob.hide = True

        return {'FINISHED'}


class GmdcPanel(bpy.types.Panel):
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
        elif obj and obj.select and obj.parent and not obj.type == 'MESH':
            if obj.parent.get("filename", None):
                self.draw_container(obj.parent, scene)


    def draw_container(self, obj, scene):
        layout = self.layout
        layout.separator()

        layout.label(text="Container Properties:")
        box = layout.box()
        col = box.column()
        col.label(text=obj.name, icon='GROUP')

        col = box.column()
        col.prop(obj, '["filename"]')
        row = col.row(align=True)
        row.label(text="Shadows:", icon='LAMP_SPOT')
        row.operator("gmdc.shadow_hide", text="Hide", icon='RESTRICT_VIEW_ON')
        row.operator("gmdc.shadow_unhide", text="Unhide", icon='RESTRICT_VIEW_OFF')
        row = col.row(align=True)
        row.label(text="Armature:", icon='ARMATURE_DATA')
        row.operator("gmdc.armature_hide", text="Hide", icon='RESTRICT_VIEW_ON')
        row.operator("gmdc.armature_unhide", text="Unhide", icon='RESTRICT_VIEW_OFF')



    def draw_object(self, obj, scene):
        layout = self.layout
        gmdc_props = scene.gmdc_props

        if obj.parent:
            self.draw_container(obj.parent, scene)

        # Group properties
        layout.separator()
        layout.label("Group Properties:")

        box = layout.box()
        col = box.column()
        col.label(text=obj.name, icon='MESH_CUBE')

        box.prop(obj, "name")

        if obj.get("opacity") != None:
            row = box.row()
            row.label("Opacity:")
            row.prop(obj, '["opacity"]', text="")

        if obj.get("is_shadow") != None:
            row = box.row()
            row.label("Shadowmesh:")
            row.prop(obj, '["is_shadow"]', text="")

        if obj.get("calc_tangents") != None and not obj.get("is_shadow"):
            row = box.row()
            row.label("Calculate Tangents:")
            row.prop(obj, '["calc_tangents"]', text="")


        # MORPHS
        box2 = layout.box()
        box2.label(text="Morphs:", icon='SHAPEKEY_DATA')

        col = box2.column(align=True)
        row = col.row(align=True)
        row.prop(gmdc_props, "mesh_type", expand=True)
        col.operator("gmdc.morphs_update_names", text="Update morph names")

        if obj.data.shape_keys:

            for i, key in enumerate(obj.data.shape_keys.key_blocks[1:]):
                box = box2.box()
                row = box.row(align=True)
                row.label(text="Morph " + str(i) + ":")
                row.label(text=key.name)

        col = box2.column(align=True)
        row = col.row(align=True)
        row.prop(gmdc_props, "morph_type", expand=True)
        col.operator("gmdc.morphs_add_morph", text="Add Morph")


        # FIXES
        fixes = layout.box()
        fixes.label(text="Fixes:", icon='MODIFIER')

        col = fixes.column(align=True)
        row = col.row(align=True)
        row.operator("gmdc.fixes_neckseam", text="Apply neck fix")
        row.prop(gmdc_props, "neckfix_type", expand=False, text="")
