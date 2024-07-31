import bpy
from .Panel_Components.BoneCollectionsSubpanel import BoneCollectionsSubpanel, BoneCollectionAction, BoneCollectionToggleProp
from .Panel_Components.BonePropertiesSubpanel import BonePropertiesSubpanel
from .registerTypes import RobloxRigCollapsibleGroup
from .Panel_Components.UiMainPanel import UiMainPanel, UiSpacingConfigure
from .Panel_Components.ToolsSubpanel import IkSwitchAction, ReparentBone, ToolsSubpanel
from src.groupData import bone_groups, property_groups, tool_groups


def is_group_on_armature(armature_data, group_collection, group_name):
    for group in getattr(armature_data, group_collection):
        if group.name == group_name:
            return True
    return False


class InitializeArmatures(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.initialize_armatures"
    bl_label = "Initialize Armatures"
    bl_description = "Initialize armatures with Roblox Rig data"

    def execute(self, context):
        for armature_data in bpy.data.armatures:
            if armature_data and hasattr(armature_data, "is_roblox_rig"):
                # Setup bone groups
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
                    new_group.visible = True

                # Setup property groups
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
                    new_group.visible = True

                # Setup tool groups
                if not hasattr(armature_data, "roblox_rig_tool_groups"):
                    armature_data.roblox_rig_tool_groups = bpy.props.CollectionProperty(
                        type=RobloxRigCollapsibleGroup,
                        options={"HIDDEN"}
                    )

                for group in tool_groups:
                    if is_group_on_armature(armature_data, "roblox_rig_property_groups", group["name"]):
                        continue
                    new_group = armature_data.roblox_rig_tool_groups.add()
                    new_group.name = group["name"]
                    new_group.visible = True

                # Setup spacing
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
        return {"FINISHED"}


def register_classes():

    bpy.utils.register_class(UiSpacingConfigure)
    bpy.utils.register_class(UiMainPanel)

    bpy.utils.register_class(BoneCollectionToggleProp)
    bpy.utils.register_class(BoneCollectionAction)
    bpy.utils.register_class(BoneCollectionsSubpanel)

    bpy.utils.register_class(BonePropertiesSubpanel)
    bpy.utils.register_class(RobloxRigCollapsibleGroup)

    bpy.utils.register_class(IkSwitchAction)
    bpy.utils.register_class(ReparentBone)
    bpy.utils.register_class(ToolsSubpanel)

    bpy.utils.register_class(InitializeArmatures)


def unregister_classes():
    bpy.utils.unregister_class(BoneCollectionToggleProp)
    bpy.utils.unregister_class(BoneCollectionAction)
    bpy.utils.unregister_class(UiSpacingConfigure)
    bpy.utils.unregister_class(UiMainPanel)
    bpy.utils.unregister_class(BoneCollectionsSubpanel)
    bpy.utils.unregister_class(BonePropertiesSubpanel)
    bpy.utils.unregister_class(RobloxRigCollapsibleGroup)
    bpy.utils.unregister_class(IkSwitchAction)
    bpy.utils.unregister_class(ReparentBone)
    bpy.utils.unregister_class(ToolsSubpanel)
    bpy.utils.unregister_class(InitializeArmatures)
