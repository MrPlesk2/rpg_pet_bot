from services.player_equipment_service import PlayerEquipmentService

def generate_page(page: int, player_id: int):
    player_equipment = PlayerEquipmentService.get_all_equipment(player_id=player_id)
    answer = ""

    for i in range(page * 5, min((page + 1) * 5, len(player_equipment))):
        answer += f"{player_equipment[i].equipment.name} {"(Экпировано)" if player_equipment[i].is_equipped else ""}\n" + \
                  f"{f"/unequip_{player_equipment[i].equipment.id}" if player_equipment[i].is_equipped else f"/equip_{player_equipment[i].equipment.id}"}\n" + \
                  f"/equipment_stat_{player_equipment[i].equipment.id}\n\n"

    return answer