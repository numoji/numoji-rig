bone_groups = [
    {
        "name": "Root",
        "rows": [
            [("ROOT", "NONE", "Root"), ("ROOT_OFFSET", "NONE", "Offset")],
            [("CENTER_MASS_PIVOT", "NONE", "CM Pivot"), ("CENTER_MASS_CALC", "NONE", "CM Dynamic")]
        ]
    },
    {
        "name": "Body",
        "rows": [
            [("HEAD", "NONE", "Head"), ("HEAD_TARGET", "NONE", "Look Target")],
            [("CHEST", "NONE", "Chest"), ("HIPS", "NONE", "Hips"), ("SHOULDERS", "NONE", "Shoulders"), ("TORSO", "WORLD", "")]
        ]
    },
    {
        "name": "Arms",
        "rows": [
            [("ARM_FK.L", "NONE", "L Arm FK"), ("ARM_FK.R", "NONE", "R Arm FK")],
            [("ARM_IK.L", "NONE", "L Arm IK"), ("ARM_IK.R", "NONE", "R Arm IK", 0.9), ("HANDS_IK", "WORLD", "")]
        ]
    },
    {
        "name": "Legs",
        "rows": [
            [("LEG_FK.L", "NONE", "L Leg FK"), ("LEG_FK.R", "NONE", "R Leg FK")],
            [("LEG_IK.L", "NONE", "L Leg IK"), ("LEG_IK.R", "NONE", "R Leg IK", 0.9), ("FEET_IK", "WORLD", "")]
        ]
    }
]

properties_bone_name = "PROPERTIES"
property_groups = [
    {
        "name": "Head Properties",
        "rows": [
            [("HEAD_TRACK", "Track"), ("HEAD_FOLLOW", "Follow Torso")],
        ]
    },
    {
        "name": "Body Properties",
        "rows": [
            [("SHOULDER_INFLUENCE", "Shoulder Twist Influence")],
            [("CENTER_MASS_PIVOT", "Pivot around Center Mass")],
        ]
    },
    {
        "name": "Arms Properties",
        "rows": [
            [("ARM_FOLLOW.L", "L Follow Shoulder"), ("ARM_FOLLOW.R", "R Follow Shoulder")],
            [("ARM_FK_IK.L", "L FK ⇔ IK"), ("ARM_FK_IK.R", "R FK ⇔ IK")],
            [("ARM_IK_STRETCH.L", "L IK Stretch"), ("ARM_IK_STRETCH.R", "R IK Stretch")],
        ]
    },
    {
        "name": "Legs Properties",
        "rows": [
            [("LEG_FK_IK.L", "L FK ⇔ IK"), ("LEG_FK_IK.R", "R FK ⇔ IK")],
            [("LEG_IK_STRETCH.L", "L IK Stretch"), ("LEG_IK_STRETCH.R", "R IK Stretch")],
        ]
    }
]
