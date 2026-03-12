from db import SessionLocal
from models.player_model import PlayerModel
from models.user_model import UserModel
from models.spell_model import SpellModel


class UserService:

    @staticmethod
    def get_user(user_id: int):
        session = SessionLocal()

        user = session.query(UserModel).filter_by(
            telegram_id=user_id
        ).first()

        session.close()
        return user

    @staticmethod
    def get_or_create_user(user_data: dict):
        session = SessionLocal()

        user = session.query(UserModel).filter_by(
            telegram_id=user_data["telegram_id"]
        ).first()

        if not user:
            user = UserModel(**user_data)

            # сразу создаём Player
            player = PlayerModel()
            
            magic_missile = session.query(SpellModel).filter_by(tag="magic_missle").first()
            fireball = session.query(SpellModel).filter_by(tag="fireball").first()
            magic_shield = session.query(SpellModel).filter_by(tag="magic_shield").first()

            if magic_missile:
                player.spells.append(magic_missile)
            if fireball:
                player.spells.append(fireball)
            if magic_shield:
                player.spells.append(magic_shield)

            user.player = player

            session.add(user)
            session.commit()
            session.refresh(user)

        session.close()
        return user
