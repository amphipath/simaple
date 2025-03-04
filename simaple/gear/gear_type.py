from __future__ import annotations

from enum import IntEnum


class GearType(IntEnum):
    weapon = -1
    sub_weapon = -2
    cap = 100
    face_accessory = 101
    eye_accessory = 102
    earrings = 103
    coat = 104
    longcoat = 105
    pants = 106
    shoes = 107
    glove = 108
    cape = 110
    ring = 111
    pendant = 112
    belt = 113
    medal = 114
    shoulder_pad = 115
    pocket = 116
    badge = 118
    android = 166
    machine_heart = 167
    shield = 109
    emblem = 119
    power_source = 119020
    shining_rod = 1212
    tuner = 1213
    breath_shooter = 1214
    soul_shooter = 122
    desperado = 123
    energy_sword = 124
    esp_limiter = 126
    chain2 = 127
    magic_gauntlet = 128
    hand_fan = 129
    oh_sword = 130
    oh_axe = 131
    oh_blunt = 132
    dagger = 133
    katara = 134
    cane = 136
    wand = 137
    staff = 138
    th_sword = 140
    th_axe = 141
    th_blunt = 142
    spear = 143
    polearm = 144
    bow = 145
    crossbow = 146
    throwing_glove = 147
    knuckle = 148
    gun = 149
    shovel = 150
    pickaxe = 151
    dual_bow = 152
    hand_cannon = 153
    sword_zb = 156
    sword_zl = 157
    gauntlet_buster = 158
    ancient_bow = 159
    soul_shield = 1098
    demon_shield = 1099
    magic_arrow = 135200
    card = 135210
    hero_medal = 135220
    rosario = 135221
    chain = 135222
    book1 = 135223
    book2 = 135224
    book3 = 135225
    bow_master_feather = 135226
    crossbow_thimble = 135227
    shadower_sheath = 135228
    night_lord_poutch = 135229
    orb = 135240
    nova_marrow = 135250
    soul_bangle = 135260
    mailin = 135270
    viper_wristband = 135290
    captain_sight = 135291
    cannon_gun_powder = 135292
    aran_pendulum = 135293
    evan_paper = 135294
    battlemage_ball = 135295
    wild_hunter_arrow_head = 135296
    cygnus_gem = 135297
    cannon_gun_powder2 = 135298
    controller = 135300
    fox_pearl = 135310
    chess = 135320
    transmitter = 135330
    explosive_pill = 135340
    magic_wing = 135350
    path_of_abyss = 135360
    relic = 135370
    fan_tassel = 135380
    bracelet = 135400
    weapon_belt = 135401
    machine_engine = 161
    machine_arms = 162
    machine_legs = 163
    machine_body = 164
    machine_transistors = 165
    _dummy = 169
    dragon_mask = 194
    dragon_pendant = 195
    dragon_wings = 196
    dragon_tail = 197
    pet_equip = 180
    title = 200

    def is_weaponry(self) -> bool:
        return self.is_weapon() or self.is_sub_weapon() or self == GearType.emblem

    def is_improved_as_weapon(self) -> bool:
        return self.is_weapon() or self == GearType.katara

    def is_weapon(self) -> bool:
        return self.is_left_weapon() or self.is_double_hand_weapon()

    def is_left_weapon(self) -> bool:
        return (
            121 <= self.value <= 139
            and self != GearType.katara
            or self.value // 10 == 121
        )

    def is_sub_weapon(self) -> bool:
        if self in (GearType.shield, GearType.demon_shield, GearType.soul_shield):
            return True
        if self.value // 1000 == 135:
            return True
        return False

    def is_double_hand_weapon(self) -> bool:
        return 140 <= self.value <= 149 or 152 <= self.value <= 159

    def is_armor(self) -> bool:
        return self.value == 100 or 104 <= self.value <= 110

    def is_accessory(self) -> bool:
        return 101 <= self.value <= 103 or 111 <= self.value <= 113 or self.value == 115

    def is_mechanic_gear(self) -> bool:
        return 161 <= self.value <= 165

    def is_dragon_gear(self) -> bool:
        return 194 <= self.value <= 197
