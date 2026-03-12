from sqlalchemy import Table, Column, Integer, ForeignKey
from db import Base

player_spells = Table(
    "player_spells",
    Base.metadata,
    Column("player_id", Integer, ForeignKey("players.id")),
    Column("spell_id", Integer, ForeignKey("spells.id")),
)