from sqlalchemy import Column, Integer, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from db import Base
from models.player_spells import player_spells

class PlayerEquipmentModel(Base):
    __tablename__ = "player_equipment"

    id = Column(Integer, primary_key=True)
    
    player_id = Column(Integer, ForeignKey("players.id"))

    equipment_id = Column(Integer, ForeignKey("equipment.id"))

    is_equipped = Column(Boolean, default=False)

    player = relationship("PlayerModel", back_populates="equipment")
    equipment = relationship("EquipmentModel", back_populates="player_items")