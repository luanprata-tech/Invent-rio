from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.api.deps import get_db
from app.models.attributes import Category, Brand, ModelAttr, Department, FundingSource

router = APIRouter()

class AttributeCreate(BaseModel):
    name: str

class AttributeResponse(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ModelCreate(BaseModel):
    name: str
    brand_id: int

class ModelResponse(BaseModel):
    id: int
    name: str
    brand_id: int | None = None
    class Config:
        orm_mode = True

# --- BRANDS ---
@router.get("/brands", response_model=List[AttributeResponse])
def get_brands(db: Session = Depends(get_db)):
    return db.query(Brand).all()

@router.post("/brands", response_model=AttributeResponse)
def create_brand(item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = Brand(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- MODELS ---
@router.get("/models", response_model=List[ModelResponse])
def get_models(db: Session = Depends(get_db)):
    return db.query(ModelAttr).all()

@router.post("/models", response_model=ModelResponse)
def create_model(item: ModelCreate, db: Session = Depends(get_db)):
    db_item = ModelAttr(name=item.name, brand_id=item.brand_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- DEPARTMENTS ---
@router.get("/departments", response_model=List[AttributeResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()

@router.post("/departments", response_model=AttributeResponse)
def create_department(item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = Department(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- FUNDING SOURCES ---
@router.get("/funding-sources", response_model=List[AttributeResponse])
def get_funding_sources(db: Session = Depends(get_db)):
    return db.query(FundingSource).all()

@router.post("/funding-sources", response_model=AttributeResponse)
def create_funding_source(item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = FundingSource(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- CATEGORIES ---
@router.get("/categories", response_model=List[AttributeResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

@router.post("/categories", response_model=AttributeResponse)
def create_category(item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = Category(name=item.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/brands/{item_id}", response_model=AttributeResponse)
def update_brand(item_id: int, item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = db.query(Brand).filter(Brand.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/brands/{item_id}")
def delete_brand(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Brand).filter(Brand.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

@router.put("/models/{item_id}", response_model=ModelResponse)
def update_modelattr(item_id: int, item: ModelCreate, db: Session = Depends(get_db)):
    db_item = db.query(ModelAttr).filter(ModelAttr.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.brand_id = item.brand_id
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/models/{item_id}")
def delete_modelattr(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ModelAttr).filter(ModelAttr.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

@router.put("/departments/{item_id}", response_model=AttributeResponse)
def update_department(item_id: int, item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = db.query(Department).filter(Department.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/departments/{item_id}")
def delete_department(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Department).filter(Department.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

@router.put("/funding-sources/{item_id}", response_model=AttributeResponse)
def update_fundingsource(item_id: int, item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = db.query(FundingSource).filter(FundingSource.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/funding-sources/{item_id}")
def delete_fundingsource(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(FundingSource).filter(FundingSource.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}

@router.put("/categories/{item_id}", response_model=AttributeResponse)
def update_category(item_id: int, item: AttributeCreate, db: Session = Depends(get_db)):
    db_item = db.query(Category).filter(Category.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/categories/{item_id}")
def delete_category(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Category).filter(Category.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Item deleted"}
