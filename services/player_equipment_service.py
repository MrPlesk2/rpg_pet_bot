from db import SessionLocal

from sqlalchemy.orm import joinedload

from models.player_model import PlayerModel
from models.user_model import UserModel
from models.spell_model import SpellModel
from models.equipment_model import EquipmentModel
from models.player_equipment import PlayerEquipmentModel


class PlayerEquipmentService:

    @staticmethod
    def get_all_equipment(player_id: int):
        session = SessionLocal()

        equipment = session.query(PlayerEquipmentModel) \
            .options(joinedload(PlayerEquipmentModel.equipment)) \
            .filter_by(player_id=player_id) \
            .all()

        session.close()
        return equipment
    
    @staticmethod
    def get_all_equipment_equipped(player_id: int):
        session = SessionLocal()

        equipment = session.query(PlayerEquipmentModel) \
            .options(joinedload(PlayerEquipmentModel.equipment)) \
            .filter_by(player_id=player_id, is_equipped=True) \
            .all()

        session.close()
        return equipment
    
    @staticmethod
    def get_all_equipment_equipped_items(player_id: int):
        session = SessionLocal()

        equipment = session.query(PlayerEquipmentModel) \
            .options(joinedload(PlayerEquipmentModel.equipment)) \
            .filter_by(player_id=player_id, is_equipped=True) \
            .all()

        equipment_items = [item.equipment for item in equipment]
        session.close()

        return equipment_items

    @staticmethod
    def get_equipment(player_id: int, equipment_id: int):
        session = SessionLocal()

        equipment = session.query(PlayerEquipmentModel).filter_by(
            player_id=player_id,
            equipment_id=equipment_id
        ).first()

        session.close()
        return equipment
    
    @staticmethod
    def add_equipment(player_id: int, equipment_id: int):
        session = SessionLocal()

        player_equipment = PlayerEquipmentModel(
            player_id=player_id,
            equipment_id=equipment_id,
            is_equipped=False
        )

        session.add(player_equipment)
        session.commit()

        session.close()

    @staticmethod
    def equip(player_id: int, equipment_id: int):
        session = SessionLocal()

        player_item = (
            session.query(PlayerEquipmentModel)
            .options(joinedload(PlayerEquipmentModel.equipment))
            .filter_by(
                player_id=player_id,
                equipment_id=equipment_id
            )
            .first()
        )

        if not player_item:
            session.close()
            return False

        slot = player_item.equipment.slot

        already_equipped = (
            session.query(PlayerEquipmentModel)
            .join(EquipmentModel)
            .filter(
                PlayerEquipmentModel.player_id == player_id,
                PlayerEquipmentModel.is_equipped == True,
                EquipmentModel.slot == slot
            )
            .first()
        )

        if already_equipped:
            session.close()
            return False

        player_item.is_equipped = True

        session.commit()
        session.close()

        return True

    @staticmethod
    def unequip(player_id: int, equipment_id: int):
        session = SessionLocal()

        equipment = session.query(PlayerEquipmentModel).filter_by(
            player_id=player_id,
            equipment_id=equipment_id
        ).first()

        equipment.is_equipped = False

        session.commit()

        session.close()
