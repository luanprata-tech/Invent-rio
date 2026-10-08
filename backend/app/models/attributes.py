from sqlalchemy import Column, Integer, String
from app.db.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)

class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)

class ModelAttr(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    brand_name = Column(String(255), nullable=True, index=True)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)

class FundingSource(Base):
    __tablename__ = "funding_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
