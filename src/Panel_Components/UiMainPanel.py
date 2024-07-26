import bpy


class UiSpacingConfigure(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.spacing_configure"
    bl_label = ""
    bl_description = "Panel Display Options"

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        armature = context.active_object.data
        layout = self.layout
        if armature:
            box_title = layout.box()
            box_title.label(text=f"Configure {context.active_object.name}")

            layout.separator()
            column = layout.column()
            column.label(text="UI Settings")
            column.prop(armature, "ui_horizontal_spacing", text="Horizontal Spacing", slider=True)
            column.prop(armature, "ui_vertical_spacing", text="Vertical Spacing", slider=True)
        else:
            self.layout.label(text="Select a roblox character rig to configure panel spacing", icon="INFO")


class UiMainPanel(bpy.types.Panel):
    bl_label = ""
    bl_idname = "UiMainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rig Controls"

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="Rig Controls")
        options = layout.row(align=True)
        options.active = False
        options.operator("roblox_rig_ui.spacing_configure", text="", icon="PREFERENCES", emboss=False)

    def draw(self, context):
        layout = self.layout
        armature = context.view_layer.objects.active

        if 'is_roblox_rig' not in armature.data:
            layout.label(text='Select a roblox character armature')
