# ORDER MATTERS! Bones further down the chain should come after their parents.
arms_fk_to_ik = {
    "ARM_FK": "MCH_IK_INT_ARM",
    "FOREARM_FK": "MCH_IK_INT_FOREARM",
    "HAND_FK": "MCH_IK_INT_HAND",
}

arms_ik_to_fk = {
    "HAND_IK": "HAND_FK",
    "ARM_IK_POLE": "MCH_ARM_FK_POLE_SNAP",
}

legs_fk_to_ik = {
    "LEG_FK": "MCH_IK_INT_LEG",
    "SHIN_FK": "MCH_IK_INT_SHIN",
    "FOOT_FK": "MCH_IK_INT_FOOT",
}

legs_ik_to_fk = {
    "FOOT_IK": "FOOT_FK",
    "LEG_IK_POLE": "MCH_LEG_FK_POLE_SNAP",
}

tools_ik_to_fk = {
	"TOOL_IK": "TOOL_OFFSET_FK",
}

tools_fk_to_ik = {
	"TOOL_OFFSET_FK": "TOOL_IK",
}