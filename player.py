from models.player_model import PlayerModel
from services.player_service import PlayerService
from services.user_service import UserService
from services.player_equipment_service import PlayerEquipmentService
import random

class Player:
    def __init__(self, model: PlayerModel):
        self.model = model

        equipment_items = PlayerEquipmentService.get_all_equipment_equipped_items(model.id)

        self.hp = model.maxHp + 10 * sum(item.maxHp for item in equipment_items)
        self.mp = model.maxMp + 10 * sum(item.maxMp for item in equipment_items)
        self._attack = model.attack + sum(item.attack for item in equipment_items)
        self._defens = model.defens + sum(item.defens for item in equipment_items)
        self.dodje = model.dodje + sum(item.dodje for item in equipment_items)
        self.mgkpwr = model.mgkpwr + sum(item.mgkpwr for item in equipment_items)
    
    def raise_stat(self, stat_name: str):
        if stat_name == "здоровье":
            self.model.maxHp += 10
            PlayerService.set_stat(self.model.user_id, stat_name, self.model.maxHp)
        elif stat_name == "ману":
            self.model.maxMp += 10
            PlayerService.set_stat(self.model.user_id, stat_name, self.model.maxMp)
        elif stat_name == "атаку":
            self.model.attack += 1
            PlayerService.set_stat(self.model.user_id, stat_name, self.model.attack)
        elif stat_name == "защиту":
            self.model.defens += 1
            PlayerService.set_stat(self.model.user_id, stat_name, self.model.defens)
        elif stat_name == "увороты":
            self.model.dodje += 1
            PlayerService.set_stat(self.model.user_id, stat_name, self.model.dodje)
        elif stat_name == "магическую силу":
            self.model.mgkpwr += 1
            PlayerService.set_stat(self.model.user_id, stat_name, self.model.mgkpwr)

    def level_up(self):
        self.model.level += 1
        PlayerService.level_up(self.model.user_id)

    def attack(self):
        crit = random.randint(0, 20)
        if crit >= 19:
            return max(0, 2 * (self._attack + random.randint(-2,2)))
        return max(0, self._attack + random.randint(-2,2))
    
    def defens(self):
        return max(0, self._defens + random.randint(-2,2))
