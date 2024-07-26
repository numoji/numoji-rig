import bpy


class CollapsibleHeaderSubpanel(bpy.types.Panel):
    @classmethod
    def poll(self, context):
        try:
            armature = context.view_layer.objects.active
            return 'is_roblox_rig' in armature.data
        except (AttributeError, KeyError, TypeError):
            return False

    def draw_collapse_header(self, group_layout, group_obj):
        header_container = group_layout.column()
        icon = "DOWNARROW_HLT" if group_obj.visible else "RIGHTARROW"
        row = header_container.row(align=False)
        row.prop(group_obj, "visible", text="", icon=icon, emboss=False)
        row.label(text=group_obj.name)
