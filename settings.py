# game setup
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT_PATH = "graphics/font/futura.ttf"
UI_FONT_SIZE = 18

"""
UI colors. strings are used for more general colors. Values are used for more
specialized colors.
"""
ENERGY_COLOR = "blue"
HEALTH_COLOR = "red"
TEXT_COLOR = (238, 238, 238)
UI_BG_COLOR = (34, 34, 34)
UI_BORDER_COLOR = (17, 17, 17)
UI_BORDER_COLOR_ACTIVE = "gold"
WATER_COLOR = (113, 221, 238)

# weapons
weapon_data = {
    "axe":
    {"cooldown": 300, "damage": 20, "graphic": "graphics/weapons/axe/full.png"},
    "lance":
    {"cooldown": 400, "damage": 30, "graphic": "graphics/weapons/lance/full.png"},
    "rapier":
    {"cooldown": 50, "damage": 8, "graphic": "graphics/weapons/rapier/full.png"},
    "sai":
    {"cooldown": 80, "damage": 10, "graphic": "graphics/weapons/sai/full.png"},
    "sword":
    {"cooldown": 100, "damage": 15, "graphic": "graphics/weapons/sword/full.png"}
}

magic_data = {
    "flame": {
        "strength": 5, "cost": 20, "graphic": "graphics/particles/flame/fire.png"
    },
    "heal": {
        "strength": 20, "cost": 10, "graphic": "graphics/particles/heal/heal.png"
    }
}

# enemy
monster_data = {
    "bamboo": {
        "attack_radius": 50, "attack_sound": "audio/attack/slash.wav",
        "attack_type": "leaf_attack", "damage": 6, "exp": 120, "health": 70,
        "notice_radius": 300, "resistance": 3, "speed": 3
    },
    "raccoon": {
        "attack_radius": 120, "attack_sound": "audio/attack/claw.wav",
        "attack_type": "claw", "damage": 40, "exp": 250, "health": 300,
        "notice_radius": 400, "resistance": 3, "speed": 2
    },
    "spirit": {
        "attack_radius": 60, "attack_sound": "audio/attack/fireball.wav",
        "attack_type": "thunder", "damage": 8, "exp": 110, "health": 100,
        "notice_radius": 350, "resistance": 3, "speed": 4
    },
    "squid": {
        "attack_radius": 80, "attack_sound": "audio/attack/slash.wav",
        "attack_type": "slash", "damage": 20, "exp": 100, "health": 100,
        "notice_radius": 360, "resistance": 3, "speed": 3
    }
}
