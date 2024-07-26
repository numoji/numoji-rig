import bpy
from .CollapsibleHeaderSubpanel import CollapsibleHeaderSubpanel
from src.ikSnapMap import arms_fk_to_ik, arms_ik_to_fk, legs_fk_to_ik, legs_ik_to_fk
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


class IkSwitchAction(bpy.types.Operator):
    bl_idname = "roblox_rig_ui.ik_snap_action"
    bl_label = "Bone Collection Action"
    bl_description = "Snap bones"

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

    def execute(self, context):
        prop_name = f"{self.snap_type}_FK_IK.{self.snap_side}"
        armature = context.view_layer.objects.active
        property_bone = armature.pose.bones[properties_bone_name]
        property_bone[prop_name] = 1 if self.switch_to == "IK" else 0

        switch_from = "FK" if self.switch_to == "IK" else "IK"
        switch_from_collection_name = f"{self.snap_type}_{switch_from}.{self.snap_side}"
        switch_from_collection = armature.data.collections[switch_from_collection_name]

        switch_to_collection_name = f"{self.snap_type}_{self.switch_to}.{self.snap_side}"
        switch_to_collection = armature.data.collections[switch_to_collection_name]

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

        for bone_name, matrix in matrices_to_write.items():
            bone = armature.pose.bones[bone_name]
            bone.matrix = matrix
            bpy.context.view_layer.update()

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

    def draw(self, context):
        layout = self.layout
        armature = context.view_layer.objects.active
        self.armature = armature

        horizontal_spacing = armature.data.ui_horizontal_spacing * 3
        # vertical_spacing = armature.data.ui_vertical_spacing * 1.5

        tool_groups_layout = layout.column(align=True)

        tool_groups_layout.label(text="Arms FK ⇔ IK Snap")
        arm_row = tool_groups_layout.row(align=True)
        self.draw_snap_operator(arm_row, "Arm switch to", "L", "ARM")
        arm_row.separator(factor=horizontal_spacing)
        self.draw_snap_operator(arm_row, "Arm switch to", "R", "ARM")

        tool_groups_layout.label(text="Legs FK ⇔ IK Snap")
        leg_row = tool_groups_layout.row(align=True)
        self.draw_snap_operator(leg_row, "Leg switch to", "L", "LEG")
        leg_row.separator(factor=horizontal_spacing)
        self.draw_snap_operator(leg_row, "Leg switch to", "R", "LEG")
