bone_groups = [
    {
        "name": "Root",
        "rows": [
            [("ROOT", "NONE", "Root"), ("ROOT_OFFSET", "NONE", "Offset")],
            [
                ("CENTER_MASS_PIVOT", "NONE", "CM Pivot"),
                ("CENTER_MASS_CALC", "NONE", "CM Dynamic"),
            ],
        ],
    },
    {
        "name": "Body",
        "rows": [
            [("HEAD", "NONE", "Head"), ("HEAD_TARGET", "NONE", "Look Target")],
            [
                ("CHEST", "NONE", "Chest"),
                ("HIPS", "NONE", "Hips"),
                ("SHOULDERS", "NONE", "Shoulders"),
                ("TORSO", "WORLD", ""),
            ],
        ],
    },
    {
        "name": "Arms",
        "rows": [
            [("ARM_FK.L", "NONE", "L Arm FK"), ("ARM_FK.R", "NONE", "R Arm FK")],
            [("ARM_IK.L", "NONE", "L Arm IK"), ("ARM_IK.R", "NONE", "R Arm IK", 0.9)],
        ],
    },
    {
        "name": "Legs",
        "rows": [
            [("LEG_FK.L", "NONE", "L Leg FK"), ("LEG_FK.R", "NONE", "R Leg FK")],
            [("LEG_IK.L", "NONE", "L Leg IK"), ("LEG_IK.R", "NONE", "R Leg IK", 0.9)],
        ],
    },
    {
        "name": "Tools",
        "rows": [
            [("TOOL_FK.L", "NONE", "L Tool FK"), ("TOOL_FK.R", "NONE", "R Tool FK")],
            [
                ("TOOL_IK.L", "NONE", "L Tool IK"),
                ("TOOL_IK.R", "NONE", "R Tool IK", 0.9),
            ],
        ],
    },
]

properties_bone_name = "PROPERTIES"
property_groups = [
    {
        "name": "Head",
        "rows": [
            [("HEAD_TRACK", "Track"), ("HEAD_FOLLOW", "Follow Torso")],
        ],
    },
    {
        "name": "Body",
        "rows": [
            [("SHOULDER_INFLUENCE", "Shoulder Twist Influence")],
            [("CENTER_MASS_PIVOT", "Pivot around Center Mass")],
        ],
    },
    {
        "name": "Arms",
        "rows": [
            [
                ("ARM_FOLLOW.L", "L Follow Shoulder"),
                ("ARM_FOLLOW.R", "R Follow Shoulder"),
            ],
            [("ARM_FK_IK.L", "L Arm FK ⇔ IK"), ("ARM_FK_IK.R", "R Arm FK ⇔ IK")],
            [
                ("ARM_IK_STRETCH.L", "L Arm Stretch Bias"),
                ("ARM_IK_STRETCH.R", "R Arm Stretch Bias"),
            ],
        ],
    },
    {
        "name": "Legs",
        "rows": [
            [("LEG_FK_IK.L", "L Leg FK ⇔ IK"), ("LEG_FK_IK.R", "R Leg FK ⇔ IK")],
            [
                ("LEG_IK_STRETCH.L", "L Leg Stretch Bias"),
                ("LEG_IK_STRETCH.R", "R Leg Stretch Bias"),
            ],
        ],
    },
    {
        "name": "Tools",
        "rows": [
            [("TOOL_FK_IK.L", "L Tool FK ⇔ IK"), ("TOOL_FK_IK.R", "R Tool FK ⇔ IK")],
        ],
    },
    {
        "name": "Parent",
        "rows": [
            [("HAND_PARENT.L", "L Hand Parent"), ("HAND_PARENT.R", "R Hand Parent")],
        ],
    },
]

tool_groups = [{"name": "IK/FK Snap"}, {"name": "Reparenting"}]
