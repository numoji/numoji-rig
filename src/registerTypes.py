import bpy
from src.groupData import bone_groups, property_groups


class RobloxRigCollapsibleGroup(bpy.types.PropertyGroup):
    visible: bpy.props.BoolProperty(name="Toggle", default=True, override={"LIBRARY_OVERRIDABLE"})  # type: ignore
    name: bpy.props.StringProperty(name="Name", default="Group", override={"LIBRARY_OVERRIDABLE"})  # type: ignore


def register_attributes():
    if not hasattr(bpy.types.Armature, "roblox_rig_bone_groups"):
        bpy.types.Armature.roblox_rig_bone_groups = bpy.props.CollectionProperty(
            type=RobloxRigCollapsibleGroup,
            options={"HIDDEN"}
        )

    if not hasattr(bpy.types.Armature, "roblox_rig_property_groups"):
        bpy.types.Armature.roblox_rig_property_groups = bpy.props.CollectionProperty(
            type=RobloxRigCollapsibleGroup,
            options={"HIDDEN"}
        )

    if not hasattr(bpy.types.Armature, "ui_vertical_spacing"):
        bpy.types.Armature.ui_vertical_spacing = bpy.props.FloatProperty(
            default=0.2,
            min=0.0,
            max=1.0,
            description="Vertical spacing between buttons",
            options={"HIDDEN"}
        )

    if not hasattr(bpy.types.Armature, "ui_horizontal_spacing"):
        bpy.types.Armature.ui_horizontal_spacing = bpy.props.FloatProperty(
            default=0.2,
            min=0.0,
            max=1.0,
            description="Horizontal spacing between buttons",
            options={"HIDDEN"}
        )

    if not hasattr(bpy.types.Armature, "is_roblox_rig"):
        bpy.types.Armature.is_roblox_rig = bpy.props.BoolProperty(
            default=False,
            options={"HIDDEN"}
        )


def unregister_attributes():
    del bpy.types.Armature.roblox_rig_bone_groups
    del bpy.types.Armature.roblox_rig_property_groups
    del bpy.types.Armature.ui_vertical_spacing
    del bpy.types.Armature.ui_horizontal_spacing
    del bpy.types.Armature.is_roblox_rig


def is_group_on_armature(armature_data, group_collection, group_name):
    for group in getattr(armature_data, group_collection):
        if group.name == group_name:
            return True
    return False


def initialize_group_data_on_roblox_armatures():
    for armature_data in bpy.data.armatures:
        if armature_data and hasattr(armature_data, "is_roblox_rig"):
            if not hasattr(armature_data, "roblox_rig_bone_groups"):
                armature_data.roblox_rig_bone_groups = bpy.props.CollectionProperty(
                    type=RobloxRigCollapsibleGroup,
                    options={"HIDDEN"}
                )

            for group in bone_groups:
                if is_group_on_armature(armature_data, "roblox_rig_bone_groups", group["name"]):
                    continue
                new_group = armature_data.roblox_rig_bone_groups.add()
                new_group.name = group["name"]

            if not hasattr(armature_data, "roblox_rig_property_groups"):
                armature_data.roblox_rig_property_groups = bpy.props.CollectionProperty(
                    type=RobloxRigCollapsibleGroup,
                    options={"HIDDEN"}
                )

            for group in property_groups:
                if is_group_on_armature(armature_data, "roblox_rig_property_groups", group["name"]):
                    continue
                new_group = armature_data.roblox_rig_property_groups.add()
                new_group.name = group["name"]

            if not hasattr(armature_data, "ui_vertical_spacing"):
                armature_data.ui_vertical_spacing = bpy.props.FloatProperty(
                    default=0.2,
                    min=0.0,
                    max=1.0,
                    description="Vertical spacing between buttons",
                    options={"HIDDEN"}
                )

            if not hasattr(armature_data, "ui_horizontal_spacing"):
                armature_data.ui_horizontal_spacing = bpy.props.FloatProperty(
                    default=0.2,
                    min=0.0,
                    max=1.0,
                    description="Horizontal spacing between buttons",
                    options={"HIDDEN"}
                )
