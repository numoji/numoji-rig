import bpy


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

    if not hasattr(bpy.types.Armature, "roblox_rig_tool_groups"):
        bpy.types.Armature.roblox_rig_tool_groups = bpy.props.CollectionProperty(
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
    del bpy.types.Armature.roblox_rig_tool_groups
    del bpy.types.Armature.ui_vertical_spacing
    del bpy.types.Armature.ui_horizontal_spacing
    del bpy.types.Armature.is_roblox_rig
