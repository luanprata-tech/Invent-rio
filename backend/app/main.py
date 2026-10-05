from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.db.database import engine, Base
from app.models.user import User
from app.models.asset import Asset
from app.models.ip import IP
from app.models.attributes import Category, Brand, ModelAttr, Department, FundingSource

from app.api.routes import auth, attributes, assets

# Create tables
Base.metadata.create_all(bind=engine)

from app.db.database import SessionLocal
from app.core.security import get_password_hash

def init_db():
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            hashed_pw = get_password_hash("admin")
            admin_user = User(username="admin", hashed_password=hashed_pw, is_active=True)
            db.add(admin_user)
            db.commit()
    finally:
        db.close()

init_db()

app = FastAPI(title=settings.PROJECT_NAME)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(attributes.router, prefix="/api/attributes", tags=["attributes"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/inventario", response_class=HTMLResponse)
def read_inventario(request: Request, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.is_deleted == False).all()
    
    total = len(assets)
    stats = {
        "Computador": {"count": 0, "pct": 0.0},
        "Notebook": {"count": 0, "pct": 0.0},
        "Smartphone": {"count": 0, "pct": 0.0},
        "Impressora": {"count": 0, "pct": 0.0},
        "Servidor": {"count": 0, "pct": 0.0},
        "Telefone": {"count": 0, "pct": 0.0},
        "Outros": {"count": 0, "pct": 0.0},
        "todos": {"count": total, "pct": 100.0}
    }
    
    for a in assets:
        if a.category in stats and a.category != "todos":
            stats[a.category]["count"] += 1
        else:
            stats["Outros"]["count"] += 1
            
    if total > 0:
        for k in stats:
            if k != "todos":
                stats[k]["pct"] = round((stats[k]["count"] / total) * 100, 1)

    categories = db.query(Category).all()
    brands = db.query(Brand).all()
    models = db.query(ModelAttr).all()
    departments = db.query(Department).all()
    funding_sources = db.query(FundingSource).all()

    return templates.TemplateResponse(
        request=request, 
        name="inventario.html", 
        context={
            "assets": assets, 
            "stats": stats,
            "categories": categories,
            "brands": brands,
            "models": models,
            "departments": departments,
            "funding_sources": funding_sources
        }
    )

@app.get("/ips", response_class=HTMLResponse)
def read_ips(request: Request, db: Session = Depends(get_db)):
    ips = db.query(IP).all()
    return templates.TemplateResponse(
        request=request,
        name="ips.html",
        context={"ips": ips}
    )

