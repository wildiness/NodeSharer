bl_info = {
    "name": "Node Sharer",
    "author": "NodeSharer Devs",
    "version": (0, 1, 0),
    "blender": (2, 90, 0),
    "location": "Node Editor Toolbar",
    "description": "Share node setups as text strings.",
    "warning": "Did I name this beta? It's actually alpha AF",
    "category": "Node",
}


def register():
    from . import nodesharer
    nodesharer.register()


def unregister():
    from . import nodesharer
    nodesharer.unregister()
