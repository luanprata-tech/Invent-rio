from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(255), index=True) # Tipo de Equipamento
    brand = Column(String(255)) # Fabricante / Marca
    model = Column(String(255)) # Modelo do Ativo
    device_name = Column(String(255), nullable=True) # Nome do Dispositivo
    serial_number = Column(String(255), unique=True, index=True) # S/N
    patrimony_number = Column(String(255), unique=True, nullable=True, index=True) # PAT
    acquisition_date = Column(String(255), nullable=True) # Data de Aquisição (String para simplificar formatação dd/mm/aaaa)
    funding_source = Column(String(255), nullable=True) # Fonte de Recursos / Dotação
    department = Column(String(255), index=True) # Setor / Departamento de Lotação
    responsible_user = Column(String(255), nullable=True) # Responsável / Usuário
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    ips = relationship("IP", back_populates="asset")
