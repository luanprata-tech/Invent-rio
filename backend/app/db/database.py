from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

connect_args = {}
engine_kwargs = {}

if settings.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    connect_args["check_same_thread"] = False
else:
    # Boas práticas para MySQL: Evitar erros de conexão ociosa derrubada pelo servidor
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_recycle"] = 3600

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args=connect_args,
    **engine_kwargs
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
