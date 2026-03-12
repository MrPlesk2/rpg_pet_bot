from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from db import Base
from models.player_spells import player_spells

class EquipmentModel(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    slot = Column(String)

    rarity = Column(Integer, default=0)

    maxHp = Column(Integer, default=0)
    maxMp = Column(Integer, default=0)
    attack = Column(Integer, default=0)
    defens = Column(Integer, default=0)
    dodje = Column(Integer, default=0)
    mgkpwr = Column(Integer, default=0)

    player_items = relationship("PlayerEquipmentModel", back_populates="equipment")
