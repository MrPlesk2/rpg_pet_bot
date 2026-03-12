import random
import equipment_generator

class Enemy:
    def __init__(self, level:int):
        level_rand = random.randint(-2,2)
        level = max(3, level + level_rand)
        self.level = level

        hp_level = random.randint(1, int(level/2))
        level -= hp_level
        attack_level = random.randint(0, int(level*2/3))
        defens_level = level - attack_level

        self.hp = 100 + hp_level * 10
        self.maxHp = self.hp
        self.attack_stat = attack_level
        self.defens_stat = defens_level

        self.enemy_type = "rat"

        self.action = "attack"

    def attack(self):
        if random.random() > max(0.4, min(0.8, self.hp / self.maxHp)):
            self.action = "defens"
        else:
            self.action = "attack"
        return max(0, self.attack_stat + random.randint(-2,2))

    def defens(self):
        if random.random() > max(0.7, min(0.8, self.hp / self.maxHp)):
            self.action = "defens"
        else:
            self.action = "attack"
        return max(0, self.defens_stat + random.randint(-2,2))

    def generate_equipment(self):
        return equipment_generator.generate_equipment(self.level)
    