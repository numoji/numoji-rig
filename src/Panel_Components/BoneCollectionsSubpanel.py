import bpy
from .CollapsibleHeaderSubpanel import CollapsibleHeaderSubpanel
from src.groupData import bone_groups

description = """- LMB: Toggle select
- Shift + LMB: Add / Remove to selection
- Ctrl + LMB: Toggle visibility or toggle solo if in solo mode
- Ctrl + Shift + LMB: Toggle solo"""


class BoneCollectionAction(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.bone_collection_action"
    bl_label = "Bone Collection Action"
    bl_description = description

    collection_name: bpy.props.StringProperty()  # type: ignore

    selected_collections = set()
    selected_bone_names = set()

    @classmethod
    def poll(self, context):
        try:
            armature = context.view_layer.objects.active
            return 'is_roblox_rig' in armature.data
        except (AttributeError, KeyError, TypeError):
            return False

    def invoke(self, context, event):

        self.ctrl_pressed = event.ctrl
        self.shift_pressed = event.shift

        return self.execute(context)

    def get_action(self):
        if self.ctrl_pressed and self.shift_pressed:
            return "TOGGLE_SOLO"
        elif self.ctrl_pressed:
            return "TOGGLE_VISIBLE"
        elif self.shift_pressed:
            return "APPEND_SELECT"
        else:
            return "TOGGLE_SELECT"

    def execute(self, context):
        action = self.get_action()

        armature = context.active_object
        self.selected_collections = set()

        self.selected_bone_names = set([bone.name for bone in bpy.context.selected_pose_bones])
        for collection in armature.data.collections:
            if not collection.is_visible:
                continue
            for collection_bone in collection.bones:
                if collection_bone.name in self.selected_bone_names:
                    self.selected_collections.add(collection.name)

        if action == "TOGGLE_SOLO":
            self.toggle_solo(armature)
        elif action == "TOGGLE_VISIBLE":
            self.toggle_visible(armature)
        elif action == "APPEND_SELECT":
            self.append_select(armature)
        elif action == "TOGGLE_SELECT":
            self.toggle_select(armature)
        else:
            pass

        return {"FINISHED"}

    def set_active(self, armature):
        collection = armature.data.collections[self.collection_name]
        if not collection.is_visible:
            collection.is_visible = True
        if armature.data.collections.is_solo_active and not collection.is_solo:
            collection.is_solo = True
        armature.data.collections.active = collection

        return collection

    def toggle_solo(self, armature):
        collection = armature.data.collections[self.collection_name]
        collection.is_solo = not collection.is_solo

    def toggle_visible(self, armature):
        collection = armature.data.collections[self.collection_name]
        if armature.data.collections.is_solo_active:
            collection.is_solo = not collection.is_solo
            return
        collection.is_visible = not collection.is_visible

    def append_select(self, armature):
        collection = self.set_active(armature)
        if collection.name in self.selected_collections:
            bpy.ops.armature.collection_deselect()
        else:
            bpy.ops.armature.collection_select()

    def toggle_select(self, armature):
        collection = self.set_active(armature)

        if len(self.selected_collections) == 0:
            bpy.ops.armature.collection_select()
        elif len(self.selected_collections) == 1 and collection.name in self.selected_collections:
            bpy.ops.armature.collection_deselect()
        else:
            bpy.ops.pose.select_all(action="DESELECT")
            if not self.selected_bone_names.issubset(set([bone.name for bone in collection.bones])):
                bpy.ops.armature.collection_select()


class BoneCollectionToggleProp(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.bone_collection_toggle"
    bl_label = "Bone Collection Toggle"
    collection_name: bpy.props.StringProperty()  # type: ignore
    prop_name: bpy.props.StringProperty()  # type: ignore

    def execute(self, context):
        armature = context.active_object
        collection = armature.data.collections[self.collection_name]
        setattr(collection, self.prop_name, not getattr(collection, self.prop_name))

        return {"FINISHED"}


class BoneCollectionsSubpanel(CollapsibleHeaderSubpanel):
    bl_parent_id = "UiMainPanel"
    bl_label = "Collections Visibility"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Item"

    selected_collections = set()

    def draw_collection_toggle(self, armature, layout, row_entry):
        collection_name = row_entry[0]
        icon_name = row_entry[1]
        display_name = row_entry[2] if len(row_entry) > 2 else ""
        scale = row_entry[3] if len(row_entry) > 3 else 1
        collection = armature.data.collections[collection_name]

        is_solo_active = armature.data.collections.is_solo_active
        is_solo = collection.is_solo
        is_visible = collection.is_visible
        is_selected = collection_name in self.selected_collections
        is_active = is_solo if is_solo_active else is_visible if not is_solo_active else False

        if display_name != "" or is_solo:
            visiblity_op_container = layout.row(align=True)
            visiblity_op_container.active = is_active

            visiblity_icon = "SOLO_ON" if is_solo else "HIDE_OFF" if is_visible else "HIDE_ON"
            visiblity_op = visiblity_op_container.operator("roblox_rig_ui.bone_collection_toggle", text="", icon=visiblity_icon, emboss=True)
            visiblity_op.collection_name = collection_name
            visiblity_op.prop_name = "is_solo" if collection.is_solo else "is_visible"

            horizontal_spacing = armature.data.ui_horizontal_spacing
            layout.separator(factor=horizontal_spacing)

        action_op_container = layout.row(align=True)
        action_op_container.active = is_active
        action_op_container.scale_x = scale

        highlight = is_selected if not is_solo_active or is_solo else False
        action_op = action_op_container.operator("roblox_rig_ui.bone_collection_action", text=display_name, icon=icon_name, emboss=True, depress=highlight)
        action_op.collection_name = collection_name
        # button_row.prop(collection, "is_visible", text=display_name, icon=icon_name, toggle=True)

    def draw(self, context):
        layout = self.layout
        armature = context.view_layer.objects.active

        horizontal_spacing = armature.data.ui_horizontal_spacing * 3
        vertical_spacing = armature.data.ui_vertical_spacing * 1.5

        collection_groups_layout = layout.column(align=True)
        self.selected_collections = set()

        selected_bone_names = set([bone.name for bone in bpy.context.selected_pose_bones])
        for collection in armature.data.collections:
            if not collection.is_visible:
                continue
            for collection_bone in collection.bones:
                if collection_bone.name in selected_bone_names:
                    self.selected_collections.add(collection.name)

        for idx, group in enumerate(bone_groups):
            group_obj = armature.data.roblox_rig_bone_groups[idx+1]
            self.draw_collapse_header(collection_groups_layout, group_obj)
            if group_obj.visible:
                # group_layout = collection_groups_layout.column()
                for idx, row in enumerate(group["rows"]):
                    if idx > 0:
                        collection_groups_layout.separator(factor=vertical_spacing)
                    row_layout = collection_groups_layout.row(align=True)
                    for idx, row_entry in enumerate(row):
                        if idx > 0:
                            row_layout.separator(factor=horizontal_spacing)
                        self.draw_collection_toggle(armature, row_layout, row_entry)
