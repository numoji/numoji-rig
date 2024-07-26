from . import registerTypes
from . import registerClasses

bl_info = {
    "name": "Roblox Rig UI",
    "category": "Rigging",
    "description": "UI Panel for managing Numoji's roblox character rig.",
    "author": "CrossStarCross @ Numoji",
    "blender": (4, 0, 0),
    "version": (1, 1, 420),
    "doc_url": "https://www.notion.so/notthatnda/Rig-UI-Documentation-ce181010f51e4d4c8ff1308ad884ed7e",
    "tracker_url": "https://www.notion.so/notthatnda/Features-Roadmap-and-Development-db480723be7a47da82d9f8371e2c5f92",
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
