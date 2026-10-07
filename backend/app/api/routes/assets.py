from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.api.deps import get_db
from app.models.asset import Asset
from app.models.ip import IP

router = APIRouter()

class AssetCreate(BaseModel):
    category: str
    brand: str
    model: str
    serial_number: str
    patrimony_number: Optional[str] = None
    acquisition_date: Optional[str] = None
    funding_source: Optional[str] = None
    department: str
    responsible_user: Optional[str] = None
    ip_address: Optional[str] = None

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_asset(item: AssetCreate, db: Session = Depends(get_db)):
    # Check if serial number already exists
    if db.query(Asset).filter(Asset.serial_number == item.serial_number).first():
        raise HTTPException(status_code=400, detail="Número de série já cadastrado")
        
    # Check if PAT already exists (only if not SEM-PAT/None)
    if item.patrimony_number and item.patrimony_number != 'SEM-PAT':
        if db.query(Asset).filter(Asset.patrimony_number == item.patrimony_number).first():
            raise HTTPException(status_code=400, detail="Número de patrimônio já cadastrado")

    # Save asset
    db_asset = Asset(
        category=item.category,
        brand=item.brand,
        model=item.model,
        serial_number=item.serial_number,
        patrimony_number=None if item.patrimony_number in ("SEM-PAT", "", None) else item.patrimony_number,
        acquisition_date=item.acquisition_date,
        funding_source=item.funding_source,
        department=item.department,
        responsible_user=item.responsible_user
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    
    # Save IP relationship if provided
    if item.ip_address:
        # Check if IP exists or create it
        db_ip = db.query(IP).filter(IP.ip_address == item.ip_address).first()
        if not db_ip:
            db_ip = IP(ip_address=item.ip_address, status="Alocado")
            db.add(db_ip)
            db.commit()
            db.refresh(db_ip)
            
        # Ensure it's not alocated to someone else, or just overwrite?
        # Overwrite logic for now
        db_ip.asset_id = db_asset.id
        db_ip.status = "Alocado"
        db.commit()

    return db_asset

@router.get("/unallocated")
def get_unallocated_assets(department: str, include_asset_id: Optional[int] = None, db: Session = Depends(get_db)):
    # Find assets in department that are not deleted
    assets = db.query(Asset).filter(
        Asset.department == department,
        Asset.is_deleted == False
    ).all()
    
    unallocated = []
    for a in assets:
        if not a.ips or (include_asset_id and a.id == include_asset_id):
            unallocated.append({
                "id": a.id,
                "category": a.category,
                "brand": a.brand,
                "model": a.model,
                "patrimony_number": a.patrimony_number,
                "responsible_user": a.responsible_user
            })
    return unallocated

@router.get("/{asset_id}")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    # Fetch associated IPs
    ip_list = [ip.ip_address for ip in asset.ips]
    return {
        "id": asset.id,
        "category": asset.category,
        "brand": asset.brand,
        "model": asset.model,
        "serial_number": asset.serial_number,
        "patrimony_number": asset.patrimony_number or "SEM-PAT",
        "acquisition_date": asset.acquisition_date,
        "funding_source": asset.funding_source,
        "department": asset.department,
        "responsible_user": asset.responsible_user,
        "ips": ip_list
    }

@router.put("/{asset_id}")
def update_asset(asset_id: int, asset_in: AssetCreate, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Check for uniqueness if S/N or PAT changed
    if db_asset.serial_number != asset_in.serial_number:
        if db.query(Asset).filter(Asset.serial_number == asset_in.serial_number).first():
            raise HTTPException(status_code=400, detail="Serial Number already exists")
    if asset_in.patrimony_number != "SEM-PAT" and db_asset.patrimony_number != asset_in.patrimony_number:
        if db.query(Asset).filter(Asset.patrimony_number == asset_in.patrimony_number).first():
            raise HTTPException(status_code=400, detail="Patrimony Number already exists")
            
    db_asset.category = asset_in.category
    db_asset.brand = asset_in.brand
    db_asset.model = asset_in.model
    db_asset.serial_number = asset_in.serial_number
    db_asset.patrimony_number = None if asset_in.patrimony_number in ("SEM-PAT", "", None) else asset_in.patrimony_number
    db_asset.acquisition_date = asset_in.acquisition_date
    db_asset.funding_source = asset_in.funding_source
    db_asset.department = asset_in.department
    db_asset.responsible_user = asset_in.responsible_user
    
    # Handle IP update
    if asset_in.ip_address:
        # Check if already exists for this asset
        existing_ip = next((ip for ip in db_asset.ips if ip.ip_address == asset_in.ip_address), None)
        if not existing_ip:
            # Check if used by someone else
            other_ip = db.query(IP).filter(IP.ip_address == asset_in.ip_address, IP.asset_id != asset_id).first()
            if other_ip:
                raise HTTPException(status_code=400, detail="IP address already allocated to another asset")
            new_ip = IP(ip_address=asset_in.ip_address, asset_id=asset_id, is_allocated=True)
            db.add(new_ip)
    
    db.commit()
    db.refresh(db_asset)
    return {"detail": "Asset updated"}


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.id == asset_id, Asset.is_deleted == False).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    # Free associated IPs
    for ip in db_asset.ips:
        db.delete(ip)
        
    # Soft delete
    db_asset.is_deleted = True
    db.commit()
    return {"detail": "Asset soft-deleted"}

class AssetTransfer(BaseModel):
    department: str
    reason: Optional[str] = None

@router.patch("/{asset_id}/transfer")
def transfer_asset(asset_id: int, transfer_data: AssetTransfer, db: Session = Depends(get_db)):
    db_asset = db.query(Asset).filter(Asset.id == asset_id, Asset.is_deleted == False).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_asset.department = transfer_data.department
    # Log logic or save reason could be added here if there was a TransferLog model
    db.commit()
    return {"detail": "Asset transferred"}
