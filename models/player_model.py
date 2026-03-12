from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.player_spells import player_spells

class PlayerModel(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    maxHp = Column(Integer, default=100)
    maxMp = Column(Integer, default=100)
    attack = Column(Integer, default=0)
    defens = Column(Integer, default=0)
    dodje = Column(Integer, default=0)
    mgkpwr = Column(Integer, default=0)
    level = Column(Integer, default=1)

    user = relationship("UserModel", back_populates="player")

    spells = relationship(
        "SpellModel",
        secondary=player_spells,
        back_populates="players"
    )

    equipment = relationship(
        "PlayerEquipmentModel",
        back_populates="player",
    )