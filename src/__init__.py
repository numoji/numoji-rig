from . import registerTypes
from . import registerClasses

bl_info = {
    "name": "Roblox Rig UI",
    "category": "Rigging",
    "description": "UI Panel for managing Numoji's roblox character rig.",
    "author": "CrossStarCross @ Numoji",
    "blender": (4, 0, 0),
    "version": (1, 0, 0),
    "doc_url": "https://github.com/numoji/numoji-rig",
    "support": "COMMUNITY",
    "location": "View3D > Sidebar",
}


def register():
    registerClasses.register_classes()
    registerTypes.register_attributes()


def unregister():
    registerClasses.unregister_classes()
    registerTypes.unregister_attributes()


if __name__ == "__main__":
    register()
