import bpy
from .CollapsibleHeaderSubpanel import CollapsibleHeaderSubpanel
from src.snapMap import arms_fk_to_ik, arms_ik_to_fk, legs_fk_to_ik, legs_ik_to_fk
from src.groupData import properties_bone_name


def get_snapped_matrix(bone_to_snap_to, bone_to_snap):
    # rest post matrices
    switch_to_rest_matrix = bone_to_snap_to.bone.matrix_local
    bone_rest_matrix = bone_to_snap.bone.matrix_local

    # rest pose offset matrix

    rest_offset = switch_to_rest_matrix.inverted() @ bone_rest_matrix
    world_space_offset_matrix = bone_to_snap_to.matrix @ rest_offset

    return world_space_offset_matrix


snap = {
    "FK": {
        "ARM": arms_fk_to_ik,
        "LEG": legs_fk_to_ik
    },
    "IK": {
        "ARM": arms_ik_to_fk,
        "LEG": legs_ik_to_fk
    }
}


def insert_keyframe(armature, pose_bone, bone_name, prop_name=None):
    if prop_name is not None:
        armature.keyframe_insert(data_path=f'pose.bones["{bone_name}"]["{prop_name}"]', group=bone_name, keytype="GENERATED")
    else:
        armature.keyframe_insert(data_path=f'pose.bones["{bone_name}"].location', group=bone_name, keytype="GENERATED")

        if pose_bone.rotation_mode == "QUATERNION":
            armature.keyframe_insert(data_path=f'pose.bones["{bone_name}"].rotation_quaternion', group=bone_name, keytype="GENERATED")
        elif pose_bone.rotation_mode == "AXIS_ANGLE":
            armature.keyframe_insert(data_path=f'pose.bones["{bone_name}"].rotation_axis_angle', group=bone_name, keytype="GENERATED")
        else:
            armature.keyframe_insert(data_path=f'pose.bones["{bone_name}"].rotation_euler', group=bone_name, keytype="GENERATED")


def add_keyframe(pose_bone, prop_name=None, set_prev_constant=False, prev_value=None, set_constant=False):
    armature = pose_bone.id_data
    bone_name = pose_bone.name
    current_frame = bpy.context.scene.frame_current
    frame_start = bpy.context.scene.frame_start
    action = armature.animation_data.action

    if bone_name not in action.groups.keys():
        group = action.groups.new(bone_name)
        group.use_pin = True

    insert_keyframe(armature, pose_bone, bone_name, prop_name)

    if not set_constant or not set_prev_constant:
        return

    for fcurve in action.fcurves.values():
        if (prop_name is not None and fcurve.data_path == f'pose.bones["{bone_name}"]["{prop_name}"]'
                or fcurve.data_path == f'pose.bones["{bone_name}"].location'
                or fcurve.data_path == f'pose.bones["{bone_name}"].rotation_quaternion'
                or fcurve.data_path == f'pose.bones["{bone_name}"].rotation_axis_angle'
                or fcurve.data_path == f'pose.bones["{bone_name}"].rotation_euler'):

            if set_constant:
                for idx, keyframe in fcurve.keyframe_points.items():
                    if fcurve.keyframe_points[idx].co[0] == current_frame:
                        keyframe.interpolation = "CONSTANT"

            if set_prev_constant:
                has_previous_keyframe = False

                for idx, keyframe in fcurve.keyframe_points.items():
                    if idx+1 <= len(fcurve.keyframe_points)-1 and fcurve.keyframe_points[idx+1].co[0] == current_frame:
                        has_previous_keyframe = True
                        keyframe.interpolation = "CONSTANT"

                prev_value = prev_value if prev_value is not None else fcurve.evaluate(current_frame-1)

                if not has_previous_keyframe and frame_start < current_frame:
                    bpy.context.scene.frame_current = current_frame-1
                    bpy.context.view_layer.update()
                    insert_keyframe(armature, pose_bone, bone_name, prop_name)
                    bpy.context.scene.frame_current = current_frame
                    bpy.context.view_layer.update()

            fcurve.keyframe_points.handles_recalc()


class IkSwitchAction(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.ik_snap_action"
    bl_label = "Bone Collection Action"
    bl_description = """LMB - Switch FK/IK
+ Shift - Switch FK/IK Collection Visibility
+ Ctrl - Insert keyframe for switch"""

    switch_to: bpy.props.StringProperty()  # type: ignore
    snap_type: bpy.props.StringProperty()  # type: ignore
    snap_side: bpy.props.StringProperty()  # type: ignore

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

    def execute(self, context):
        prop_name = f"{self.snap_type}_FK_IK.{self.snap_side}"
        armature = context.view_layer.objects.active
        property_bone = armature.pose.bones[properties_bone_name]

        current_prop_value = property_bone[prop_name]
        property_bone[prop_name] = 1 if self.switch_to == "IK" else 0
        if self.ctrl_pressed:
            add_keyframe(property_bone, prop_name, True, current_prop_value)

        switch_from = "FK" if self.switch_to == "IK" else "IK"
        switch_from_collection_name = f"{self.snap_type}_{switch_from}.{self.snap_side}"
        switch_from_collection = armature.data.collections[switch_from_collection_name]

        switch_to_collection_name = f"{self.snap_type}_{self.switch_to}.{self.snap_side}"
        switch_to_collection = armature.data.collections[switch_to_collection_name]

        if self.shift_pressed:
            switch_from_collection.is_visible = False
            switch_to_collection.is_visible = True

        snap_map = snap[self.switch_to][self.snap_type]
        matrices_to_write = {}
        for bone_name, switch_to_bone_name in snap_map.items():
            bone_name = bone_name + "." + self.snap_side
            switch_to_bone_name = switch_to_bone_name + "." + self.snap_side

            bone = armature.pose.bones[bone_name]
            switch_to_bone = armature.pose.bones[switch_to_bone_name]

            if bone and switch_to_bone:
                offset_matrix = get_snapped_matrix(switch_to_bone, bone)
                matrices_to_write[bone_name] = offset_matrix

        if self.ctrl_pressed:
            switch_from_map = snap_map = snap[switch_from][self.snap_type]
            for switch_bone_name in switch_from_map.keys():
                switch_from_bone = bone = armature.pose.bones[switch_bone_name + "." + self.snap_side]
                add_keyframe(switch_from_bone, set_constant=True)

        for bone_name, matrix in matrices_to_write.items():
            bone = armature.pose.bones[bone_name]
            bone.matrix = matrix
            if self.ctrl_pressed:
                add_keyframe(bone)
            bpy.context.view_layer.update()

        return {"FINISHED"}


parents = {
    "BOARD_PARENT": ["ROOT_OFFSET", "ORG_HAND.L", "ORG_HAND.R"],
    "HAND_IK_PARENT.L": ["ROOT_OFFSET", "RTG_BOARD_IK_HAND_OFFSET.L", "BOARD", "HIPS", "CHEST", "HEAD"],
    "HAND_IK_PARENT.R": ["ROOT_OFFSET", "RTG_BOARD_IK_HAND_OFFSET.R", "BOARD", "HIPS", "CHEST", "HEAD"],
    "FOOT_IK_PARENT.L": ["RTG_BOARD_IK_FOOT_OFFSET.L",  "ROOT_OFFSET"],
    "FOOT_IK_PARENT.R": ["RTG_BOARD_IK_FOOT_OFFSET.R",  "ROOT_OFFSET"],
}

compensator_for_parent = {
    "ORG_HAND.L": "PARENT_DISCREPANCY_COMPENSATOR.L",
    "ORG_HAND.R": "PARENT_DISCREPANCY_COMPENSATOR.R",
}


class ReparentBone(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.reparent_bone"
    bl_label = "Reparent Bone Action"
    bl_description = """LMB - Switch Parent & insert keyframe
LMB + Ctrl - Switch parent without keyframe
"""
    bone_name: bpy.props.StringProperty()  # type: ignore
    prop_name: bpy.props.StringProperty()  # type: ignore
    parent_idx: bpy.props.IntProperty()  # type: ignore

    def invoke(self, context, event):
        self.ctrl_pressed = event.ctrl
        return self.execute(context)

    def execute(self, context):
        armature = context.view_layer.objects.active
        property_bone = armature.pose.bones[properties_bone_name]
        bone_name = self.bone_name
        prop_name = self.prop_name
        parent_idx = self.parent_idx

        compensator_bone = None
        if bone_name in parents.keys():
            parent_bone_name = parents[bone_name][parent_idx]
            compensator_bone_name = compensator_for_parent.get(parent_bone_name)
            if compensator_bone_name:
                compensator_bone = armature.pose.bones[compensator_bone_name]

        pose_bone = armature.pose.bones[bone_name]
        original_matrix = pose_bone.matrix.copy()

        current_parent_idx = property_bone[prop_name]
        property_bone[prop_name] = parent_idx

        if self.ctrl_pressed:
            return {"FINISHED"}

        add_keyframe(property_bone, prop_name, set_prev_constant=True, prev_value=current_parent_idx, set_constant=True)

        for fcurve in armature.animation_data.drivers.values():
            fcurve.driver.expression += ''  # force update
        bpy.context.view_layer.update()

        moved_matrix = pose_bone.matrix.copy()
        pose_bone.matrix_basis = pose_bone.matrix.inverted() @ original_matrix
        bpy.context.view_layer.update()

        if compensator_bone is not None:
            compensator_bone.matrix = moved_matrix
            add_keyframe(compensator_bone, set_prev_constant=True, set_constant=True)
        add_keyframe(pose_bone, set_prev_constant=True, set_constant=True)

        return {"FINISHED"}


class ToolsSubpanel(CollapsibleHeaderSubpanel):
    bl_parent_id = "UiMainPanel"
    bl_label = "Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw_snap_operator(self, row_layout, text, side, snap_type):
        property_bone = self.armature.pose.bones[properties_bone_name]
        ik_amount = property_bone[f"{snap_type}_FK_IK.{side}"]

        if ik_amount > 0:
            switch_to = "FK"
            text = f"{side} {text} FK"
        else:
            switch_to = "IK"
            text = f"{side} {text} IK"

        switch_op = row_layout.operator("roblox_rig_ui.ik_snap_action", text=text, icon="NONE")
        switch_op.switch_to = switch_to
        switch_op.snap_type = snap_type
        switch_op.snap_side = side

    def draw_reparent_operator(self, row_layout, bone_name, prop_name, parent_idx, text):
        reparent_op = row_layout.operator("roblox_rig_ui.reparent_bone", text=text, icon="NONE")
        reparent_op.bone_name = bone_name
        reparent_op.prop_name = prop_name
        reparent_op.parent_idx = parent_idx

    def draw(self, context):
        layout = self.layout
        armature = context.view_layer.objects.active
        self.armature = armature

        horizontal_spacing = armature.data.ui_horizontal_spacing * 3
        vertical_spacing = armature.data.ui_vertical_spacing * 1.5

        ikfk_layout = layout.column(align=True)
        ikfk_group_obj = armature.data.roblox_rig_tool_groups[0]
        self.draw_collapse_header(ikfk_layout, ikfk_group_obj)

        if ikfk_group_obj.visible:
            ikfk_layout.label(text="Arms FK ⇔ IK Snap")
            arm_row = ikfk_layout.row(align=True)
            self.draw_snap_operator(arm_row, "Arm switch to", "L", "ARM")
            arm_row.separator(factor=horizontal_spacing)
            self.draw_snap_operator(arm_row, "Arm switch to", "R", "ARM")

            ikfk_layout.label(text="Legs FK ⇔ IK Snap")
            leg_row = ikfk_layout.row(align=True)
            self.draw_snap_operator(leg_row, "Leg switch to", "L", "LEG")
            leg_row.separator(factor=horizontal_spacing)
            self.draw_snap_operator(leg_row, "Leg switch to", "R", "LEG")

        reparent_layout = layout.column(align=True)
        reparent_group_obj = armature.data.roblox_rig_tool_groups[1]
        self.draw_collapse_header(reparent_layout, reparent_group_obj)
        if reparent_group_obj.visible:
            board_row = reparent_layout.row(align=True)
            board_row.label(text="Board")
            self.draw_reparent_operator(board_row, "BOARD_PARENT", "BOARD_PARENT", 0, "None")
            board_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(board_row, "BOARD_PARENT", "BOARD_PARENT", 1, "L Hand")
            board_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(board_row, "BOARD_PARENT", "BOARD_PARENT", 2, "R Hand")

            reparent_layout.separator(factor=vertical_spacing)
            l_hand_row = reparent_layout.row(align=True)
            l_hand_row.label(text="L Hand")
            self.draw_reparent_operator(l_hand_row, "HAND_IK_PARENT.L", "HAND_PARENT.L", 0, "None")
            l_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(l_hand_row, "HAND_IK_PARENT.L", "HAND_PARENT.L", 1, "Board")
            l_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(l_hand_row, "HAND_IK_PARENT.L", "HAND_PARENT.L", 2, "Hips")
            l_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(l_hand_row, "HAND_IK_PARENT.L", "HAND_PARENT.L", 3, "Chest")
            l_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(l_hand_row, "HAND_IK_PARENT.L", "HAND_PARENT.L", 4, "Head")

            reparent_layout.separator(factor=vertical_spacing)
            r_hand_row = reparent_layout.row(align=True)
            r_hand_row.label(text="R Hand")
            self.draw_reparent_operator(r_hand_row, "HAND_IK_PARENT.R", "HAND_PARENT.R", 0, "None")
            r_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(r_hand_row, "HAND_IK_PARENT.R", "HAND_PARENT.R", 1, "Board")
            r_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(r_hand_row, "HAND_IK_PARENT.R", "HAND_PARENT.R", 2, "Hips")
            r_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(r_hand_row, "HAND_IK_PARENT.R", "HAND_PARENT.R", 3, "Chest")
            r_hand_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(r_hand_row, "HAND_IK_PARENT.R", "HAND_PARENT.R", 4, "Head")

            reparent_layout.separator(factor=vertical_spacing)
            l_foot_row = reparent_layout.row(align=True)
            l_foot_row.label(text="L Foot")
            self.draw_reparent_operator(l_foot_row, "FOOT_IK_PARENT.L", "FOOT_PARENT.L", 0, "Board")
            l_foot_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(l_foot_row, "FOOT_IK_PARENT.L", "FOOT_PARENT.L", 1, "None")

            reparent_layout.separator(factor=vertical_spacing)
            r_foot_row = reparent_layout.row(align=True)
            r_foot_row.label(text="R Foot")
            self.draw_reparent_operator(r_foot_row, "FOOT_IK_PARENT.R", "FOOT_PARENT.R", 0, "Board")
            r_foot_row.separator(factor=horizontal_spacing)
            self.draw_reparent_operator(r_foot_row, "FOOT_IK_PARENT.R", "FOOT_PARENT.R", 1, "None")

