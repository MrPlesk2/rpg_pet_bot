from db import SessionLocal
from models.player_model import PlayerModel
from models.user_model import UserModel
from models.spell_model import SpellModel


class SpellService:

    @staticmethod
    def create_spell(name: str, tag: str, attack_num: int, base_dmg: int, mgk_pwr_coef: int, manacost: int):
        session = SessionLocal()

        spell = SpellModel(
            name=name,
            tag=tag,
            attack_num=attack_num,
            base_dmg=base_dmg,
            mgk_pwr_coef=mgk_pwr_coef,
            manacost=manacost
        )

        session.add(spell)
        session.commit()
        session.close()

        return 1

    @staticmethod
    def get_spell_by_name(name: str):
        session = SessionLocal()

        spell = session.query(SpellModel).filter_by(
            name=name
        ).first()

        session.close()

        return spell
    
    @staticmethod
    def get_spell_by_tag(tag: str):
        session = SessionLocal()

        spell = session.query(SpellModel).filter_by(
            tag=tag
        ).first()

        session.close()

        return spell
    