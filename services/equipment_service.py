from db import SessionLocal
from models.player_model import PlayerModel
from models.user_model import UserModel
from models.spell_model import SpellModel
from models.equipment_model import EquipmentModel


class EquipmentService:

    @staticmethod
    def get_equipment(equipment_id: int):
        session = SessionLocal()

        equipment = session.query(EquipmentModel).filter_by(
            id=equipment_id
        ).first()

        session.close()
        return equipment
    
    @staticmethod
    def get_equipment_list_by_rarity(rarity: str):
        session = SessionLocal()

        if rarity == "common":
            equipment = session.query(EquipmentModel).filter_by(
                rarity = 0
            )
        elif rarity == "uncommon":
            equipment = session.query(EquipmentModel).filter_by(
                rarity = 1
            )
        elif rarity == "rare":
            equipment = session.query(EquipmentModel).filter_by(
                rarity = 2
            )
        elif rarity == "epic":
            equipment = session.query(EquipmentModel).filter_by(
                rarity = 3
            )
        elif rarity == "legendary":
            equipment = session.query(EquipmentModel).filter_by(
                rarity = 4
            )

        session.close()
        return equipment
    
    @staticmethod
    def add_equipment(name: str, slot: str, rarity: int, maxHp: int, maxMp: int, attack: int, defens: int, dodje: int, mgkpwr: int):
        session = SessionLocal()

        equipment = EquipmentModel()
        equipment.name = name
        equipment.slot = slot
        equipment.rarity = rarity

        equipment.maxHp = maxHp
        equipment.maxMp = maxMp
        equipment.attack = attack
        equipment.defens = defens
        equipment.dodje = dodje
        equipment.mgkpwr = mgkpwr

        session.add(equipment)

        session.commit()

        session.close()

