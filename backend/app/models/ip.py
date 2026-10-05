from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class IP(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    subnet = Column(String, index=True)
    status = Column(String, default="Disponível") # Disponível, Alocado, Reservado
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)

    asset = relationship("Asset", back_populates="ips")
