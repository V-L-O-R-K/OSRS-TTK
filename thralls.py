from random import randint


class Thrall:  # ignores cast time and duration ... may actually be ever so slightly less dps
    def __init__(self):
        self.attack_speed = 4
        self.max_hit = 3
        self.average_hit = 3 / 2
        self.dps = self.average_hit / (4 * 0.6)

    @staticmethod
    def roll_damage():
        return randint(0, 3)
