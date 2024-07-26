from .CollapsibleHeaderSubpanel import CollapsibleHeaderSubpanel
from src.groupData import property_groups, properties_bone_name


class BonePropertiesSubpanel(CollapsibleHeaderSubpanel):
    bl_parent_id = "UiMainPanel"
    bl_label = "Rig Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    def draw_property_control(self, armature, layout_row, row_entry):
        prop_name = row_entry[0]
        display_name = row_entry[1]
        property_bone = armature.pose.bones[properties_bone_name]

        prop_value = property_bone[prop_name]
        prop_type = type(prop_value)
        prop_custom_name_display = display_name if display_name is not None else prop_name

        if prop_type == bool:
            layout_row.prop(property_bone, f'["{prop_name}"]', text=prop_custom_name_display, toggle=True)
        elif prop_type in (int, float):
            slider = prop_type == float
            layout_row.prop(property_bone, f'["{prop_name}"]', text=prop_custom_name_display, slider=slider)

    def draw(self, context):
        layout = self.layout
        armature = context.view_layer.objects.active

        horizontal_spacing = armature.data.ui_horizontal_spacing * 3
        vertical_spacing = armature.data.ui_vertical_spacing * 1.5

        property_groups_layout = layout.column(align=True)

        for idx, group in enumerate(property_groups):
            group_obj = armature.data.roblox_rig_property_groups[idx]
            self.draw_collapse_header(property_groups_layout, group_obj)
            if group_obj.visible:
                # group_layout = collection_groups_layout.column()
                for idx, row in enumerate(group["rows"]):
                    if idx > 0:
                        property_groups_layout.separator(factor=vertical_spacing)
                    row_layout = property_groups_layout.row(align=True)
                    for idx, row_entry in enumerate(row):
                        if idx > 0:
                            row_layout.separator(factor=horizontal_spacing)
                        self.draw_property_control(armature, row_layout, row_entry)
