import random
from services.equipment_service import EquipmentService

def generate_equipment(level: int):
    nothing_chance = max(0, 15 - level)
    common_chance = nothing_chance + level
    uncommon_chance = common_chance + max(0, (level - 5) * 2)
    rare_chance = uncommon_chance + max(0, (level - 10) * 4)
    epic_chance = rare_chance + max(0, (level - 15) * 6)
    legendary_chance = epic_chance + max(0, (level - 20) * 8)

    value = random.randint(0, legendary_chance - 1)

    if value < nothing_chance:
        return None
    elif value < common_chance:
        common_equipment = EquipmentService.get_equipment_list_by_rarity("common")
        equipment = common_equipment[random.randint(0, common_equipment.count() - 1)]
    elif value < uncommon_chance:
        uncommon_equipment = EquipmentService.get_equipment_list_by_rarity("uncommon")
        equipment = uncommon_equipment[random.randint(0, uncommon_equipment.count() - 1)]
    elif value < rare_chance:
        rare_equipment = EquipmentService.get_equipment_list_by_rarity("rare")
        equipment = rare_equipment[random.randint(0, rare_equipment.count() - 1)]
    elif value < epic_chance:
        epic_equipment = EquipmentService.get_equipment_list_by_rarity("epic")
        equipment = epic_equipment[random.randint(0, epic_equipment.count() - 1)]
    else:
        legendary_equipment = EquipmentService.get_equipment_list_by_rarity("legendary")
        equipment = legendary_equipment[random.randint(0, legendary_equipment.count() - 1)]

    return equipment