from db import SessionLocal
from models.player_model import PlayerModel
from models.user_model import UserModel
from models.spell_model import SpellModel
from models.player_equipment import PlayerEquipmentModel


class PlayerService:

    @staticmethod
    def get_player_by_telegram_id(user_id: int):
        session = SessionLocal()

        user = session.query(UserModel).filter_by(
            telegram_id = user_id
        ).first()

        player = session.query(PlayerModel).filter_by(
            user_id = user.id
        ).first()

        session.close()
        return player

    @staticmethod
    def get_player(user_id: int):
        session = SessionLocal()

        user = session.query(PlayerModel).filter_by(
            user_id = user_id
        ).first()

        session.close()
        return user

    @staticmethod
    def get_stat(user_id: int, stat_name: str):
        session = SessionLocal()

        user = session.query(PlayerModel).filter_by(
            user_id = user_id
        ).first()

        session.close()

        if stat_name == "здоровье":
            return user.maxHp
        elif stat_name == "ману":
            return user.maxMp
        elif stat_name == "атаку":
            return user.attack
        elif stat_name == "защиту":
            return user.defens
        elif stat_name == "увороты":
            return user.dodje
        elif stat_name == "магическую силу":
            return user.mgkpwr
        else:
            return None
        
    @staticmethod
    def set_stat(user_telegram_id: int, stat_name: str, stat_value: int):
        session = SessionLocal()

        user = session.query(PlayerModel).filter_by(
            user_id = user_telegram_id
        ).first()

        

        if stat_name == "здоровье":
            user.maxHp = stat_value
        elif stat_name == "ману":
            user.maxMp = stat_value
        elif stat_name == "атаку":
            user.attack = stat_value
        elif stat_name == "защиту":
            user.defens = stat_value
        elif stat_name == "увороты":
            user.dodje = stat_value
        elif stat_name == "магическую силу":
            user.mgkpwr = stat_value

        session.commit()

        session.close()

    @staticmethod
    def get_player_spell_list(user_id: int):
        session = SessionLocal()

        player = session.query(PlayerModel).filter_by(
            id = user_id
        ).first()

        spells = player.spells

        session.close()

        return spells

    @staticmethod
    def add_spell_to_player(user_id: int, spell: SpellModel):
        session = SessionLocal()

        player = session.query(PlayerModel).filter_by(
            id = user_id
        ).first()

        spells = player.spells.append(spell)

        session.commit()

        session.close()

        return spells
    
    @staticmethod
    def level_up(user_id: int):
        session = SessionLocal()

        player = session.query(PlayerModel).filter_by(
            id = user_id
        ).first()

        player.level += 1

        session.commit()

        session.close()
        
