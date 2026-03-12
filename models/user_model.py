from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship
from db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    name = Column(String)
    username = Column(String)
    phone = Column(String)

    player = relationship("PlayerModel", back_populates="user", uselist=False)