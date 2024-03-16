from random import randint

# constants are obtained from OSRS DPS Calc
# https://docs.google.com/spreadsheets/d/1wBXIlvAmqoQpu5u9XBfD4B0PW7D8owyO_CnRDiTHBKQ

# https://oldschool.runescape.wiki/w/Damage_per_second/Melee#Step_six:_Calculate_the_hit_chance
# Max defence roll = (level * prayer + 9) * (bonus + 64)
# Max attack roll = attack level * prayer + 8 * (64 + gear bonus)


class TombsMonster:  # Raid level applies modifier to defence max roll, not stats which determine it
    def __init__(self, raid_level, path_level, defence_level, magic_level, stab_defence, magic_defence, range_defence, max_hp):
        self.raid_level = raid_level
        self.path_level = path_level
        self.defence_level = defence_level
        self.magic_level = magic_level
        self.stab_def = stab_defence
        self.magic_def = magic_defence
        self.range_def = range_defence
        self.max_hp = int(round(max_hp * (1 + raid_level/5*2/100), -1))

        if self.path_level == 1:
            self.max_hp = int(round(max_hp * (1 + raid_level / 5 * 2 / 100) + (self.max_hp * 0.08), -1))
        elif self.path_level > 1:
            self.max_hp = int(round(max_hp * (1 + raid_level / 5 * 2 / 100) + (self.max_hp * 0.08) + (self.path_level - 1) * 0.05 * self.max_hp, -1))

        self.current_hp = self.max_hp

    @property
    def max_roll_vs_magic(self):
        return int((self.magic_level + 9) * int(self.magic_def + 64) * (1 + self.raid_level/5*2/100))

    @property
    def max_roll_vs_range(self):
        return int((self.defence_level + 9) * int(self.range_def + 64) * (1 + self.raid_level/5*2/100))

    @property
    def max_roll_vs_stab(self):
        return int((self.defence_level + 9) * int(self.stab_def + 64) * (1 + self.raid_level/5*2/100))

