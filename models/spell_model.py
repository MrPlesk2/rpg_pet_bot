from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db import Base
from models.player_spells import player_spells

class SpellModel(Base):
    __tablename__ = "spells"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tag = Column(String)

    attack_num = Column(Integer, default=1)
    base_dmg = Column(Integer, default=5)
    mgk_pwr_coef = Column(Integer, default=3)
    manacost = Column(Integer, default=20)

    players = relationship(
        "PlayerModel",
        secondary=player_spells,
        back_populates="spells"
    )
