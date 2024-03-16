from random import randint, uniform


# Need a separate thing for fang
class StandardWeapon:
    def __init__(self, attack_speed, max_hit, max_hit_roll):
        self.attack_speed = attack_speed
        self.max_hit = max_hit
        self.hit_max_roll = max_hit_roll

    def hit_chance(self, enemy_def_roll):

        if self.hit_max_roll > enemy_def_roll:
            return 1 - ((enemy_def_roll + 2) / (2 * (self.hit_max_roll + 1)))
        else:
            return self.hit_max_roll / (2 * (enemy_def_roll + 1))

    def roll_damage(self):
        return randint(0, self.max_hit)

    def average_hit(self, enemy_def_roll):
        return self.hit_chance(enemy_def_roll) * self.max_hit / 2

    def dps(self, enemy_def_roll):
        return (self.hit_chance(enemy_def_roll) * self.max_hit / 2) / (self.attack_speed * 0.6)
