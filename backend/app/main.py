import asyncio
import platform
import platform
from pydantic import BaseModel
from fastapi import FastAPI, Request, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from fastapi.responses import HTMLResponse, FileResponse
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

@app.get("/manifest.json", include_in_schema=False)
def get_manifest():
    return FileResponse("app/static/manifest.json")

@app.get("/sw.js", include_in_schema=False)
def get_sw():
    return FileResponse("app/static/sw.js", media_type="application/javascript")
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.get("/inventario", response_class=HTMLResponse)
def read_inventario(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
            "funding_sources": funding_sources,
            "total_assets": total
        }
    )

@app.get("/ips", response_class=HTMLResponse)
def read_ips(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), subnet: str = "172.23.6.0/24"):
    prefix = subnet.split('.0/24')[0] + '.'
    ips_list = db.query(IP).filter(IP.ip_address.like(f"{prefix}%")).all()
    ips_list.sort(key=lambda ip: int(ip.ip_address.split('.')[-1]))
    
    ip_dict = {ip.ip_address: ip for ip in ips_list}
    
    allocated_count = sum(1 for ip in ips_list if ip.status in ['Alocado', 'Reservado'])
    falso_livre_count = sum(1 for ip in ips_list if ip.status == 'Livre' and ip.last_ping_result == True)
    total_utilizable = 254
    livres_count = total_utilizable - allocated_count - falso_livre_count
    allocated_pct = round((allocated_count / total_utilizable) * 100, 1)
    
    total_assets = db.query(Asset).filter(Asset.is_deleted == False).count()
    departments = db.query(Department).all()
    
    return templates.TemplateResponse(
        request=request,
        name="ips.html",
        context={
            "ips": ips_list, 
            "ip_dict": ip_dict,
            "total_assets": total_assets,
            "current_subnet": subnet,
            "prefix": prefix,
            "allocated_count": allocated_count,
            "allocated_pct": allocated_pct,
            "livres_count": livres_count,
            "falso_livre_count": falso_livre_count,
            "departments": departments
        }
    )

class PingRequest(BaseModel):
    subnet: str

async def ping_ip(ip_address: str):
    import platform
    is_windows = platform.system().lower() == "windows"
    cmd = ['ping', '-n', '1', '-w', '1000', ip_address] if is_windows else ['ping', '-c', '1', '-W', '1', ip_address]
    
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, _ = await proc.communicate()
    out_str = stdout.decode('utf-8', errors='ignore').lower()
    
    if 'unreachable' in out_str or 'inacess' in out_str:
        return ip_address, 'unreachable'
    elif proc.returncode == 0 and 'esgotado' not in out_str and 'time out' not in out_str and '100% packet loss' not in out_str:
        return ip_address, 'up'
    else:
        return ip_address, 'timeout' 

@app.post("/api/ips/ping")
async def ping_subnet(req: PingRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prefix = req.subnet.split('.0/24')[0] + '.'
    ips_to_ping = [f"{prefix}{i}" for i in range(1, 255)]
    results = await asyncio.gather(*(ping_ip(ip) for ip in ips_to_ping))
    ping_status = {ip: is_up for ip, is_up in results}
    
    db_ips = db.query(IP).filter(IP.ip_address.like(f"{prefix}%")).all()
    db_ips_dict = {ip.ip_address: ip for ip in db_ips}
    
    for ip_str, status_str in ping_status.items():
        if ip_str in db_ips_dict:
            db_ips_dict[ip_str].last_ping_result = status_str
        else:
            if status_str != 'timeout':
                new_ip = IP(ip_address=ip_str, subnet=req.subnet, status='Livre', last_ping_result=status_str)
                db.add(new_ip)
    
    db.commit()
    return {"message": "Ping concluído", "success": True}

class AllocateIPRequest(BaseModel):
    ip_address: str
    asset_id: int
    subnet: str

@app.post("/api/ips/allocate")
def allocate_ip(req: AllocateIPRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Create or update IP
    db_ip = db.query(IP).filter(IP.ip_address == req.ip_address).first()
    if not db_ip:
        db_ip = IP(ip_address=req.ip_address, subnet=req.subnet, status='Alocado', asset_id=req.asset_id)
        db.add(db_ip)
    else:
        db_ip.status = 'Alocado'
        db_ip.asset_id = req.asset_id
    db.commit()
    return {"success": True}

class ReleaseIPRequest(BaseModel):
    ip_address: str

@app.post("/api/ips/release")
def release_ip(req: ReleaseIPRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_ip = db.query(IP).filter(IP.ip_address == req.ip_address).first()
    if db_ip:
        db_ip.status = 'Livre'
        db_ip.asset_id = None
        db.commit()
    return {"success": True}

class ReserveIPRequest(BaseModel):
    ip_address: str
    subnet: str

@app.post("/api/ips/reserve")
def reserve_ip(req: ReserveIPRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_ip = db.query(IP).filter(IP.ip_address == req.ip_address).first()
    if not db_ip:
        db_ip = IP(ip_address=req.ip_address, subnet=req.subnet, status='Reservado', asset_id=None)
        db.add(db_ip)
    else:
        db_ip.status = 'Reservado'
        db_ip.asset_id = None
    db.commit()
    return {"success": True}
