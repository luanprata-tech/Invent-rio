from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True) # Tipo de Equipamento
    brand = Column(String) # Fabricante / Marca
    model = Column(String) # Modelo do Ativo
    serial_number = Column(String, unique=True, index=True) # S/N
    patrimony_number = Column(String, unique=True, nullable=True, index=True) # PAT
    acquisition_date = Column(String, nullable=True) # Data de Aquisição (String para simplificar formatação dd/mm/aaaa)
    funding_source = Column(String, nullable=True) # Fonte de Recursos / Dotação
    department = Column(String, index=True) # Setor / Departamento de Lotação
    responsible_user = Column(String, nullable=True) # Responsável / Usuário
    created_at = Column(DateTime, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)

    ips = relationship("IP", back_populates="asset")
