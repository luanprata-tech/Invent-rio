from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base

class IP(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(255), unique=True, index=True)
    subnet = Column(String(255), index=True)
    status = Column(String(255), default="Disponível") # Disponível, Alocado, Reservado
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    last_ping_result = Column(Boolean, nullable=True)

    asset = relationship("Asset", back_populates="ips")
