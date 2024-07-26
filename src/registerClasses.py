import bpy
from .Panel_Components.BoneCollectionsSubpanel import BoneCollectionsSubpanel, BoneCollectionAction, BoneCollectionToggleProp
from .Panel_Components.BonePropertiesSubpanel import BonePropertiesSubpanel
from .registerTypes import RobloxRigCollapsibleGroup
from .Panel_Components.UiMainPanel import UiMainPanel, UiSpacingConfigure


def register_classes():

    bpy.utils.register_class(UiSpacingConfigure)
    bpy.utils.register_class(UiMainPanel)

    bpy.utils.register_class(BoneCollectionToggleProp)
    bpy.utils.register_class(BoneCollectionAction)
    bpy.utils.register_class(BoneCollectionsSubpanel)

    bpy.utils.register_class(BonePropertiesSubpanel)
    bpy.utils.register_class(RobloxRigCollapsibleGroup)


def unregister_classes():
    bpy.utils.unregister_class(BoneCollectionToggleProp)
    bpy.utils.unregister_class(BoneCollectionAction)
    bpy.utils.unregister_class(UiSpacingConfigure)
    bpy.utils.unregister_class(UiMainPanel)
    bpy.utils.unregister_class(BoneCollectionsSubpanel)
    bpy.utils.unregister_class(BonePropertiesSubpanel)
    bpy.utils.unregister_class(RobloxRigCollapsibleGroup)
