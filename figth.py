from enemy import Enemy
from player import Player

class Fight:
    def __init__(self, enemy: Enemy, player: Player):
        self.enemy = enemy
        self.player = player

    def main_fight_message(self):
        return f"Вы сражаетесь с {self.enemy.enemy_type}\n" + \
               f"Враг собирается {"атаковать" if self.enemy.action == "attack" else "защищаться"}\n" + \
               f"У него осталось {self.enemy.hp} здоровья\n\n" + \
               f"У вас осталось {self.player.hp} здоровья\n" + \
               f"У вас осталось {self.player.mp} маны"
    
    def main_fight_message_not_changed(self):
        return f"Вы сражаетесь с {self.enemy.enemy_type}\n" + \
               f"Враг собирается {"атаковать" if self.enemy.action == "attack" else "защищаться"}\n" + \
               f"У него осталось {self.enemy.hp} здоровья\n\n" + \
               f"У вас осталось {self.player.hp} здоровья\n" + \
               f"У вас осталось {self.player.mp} маны\n\n" + \
               f"Действие выполнено)"
