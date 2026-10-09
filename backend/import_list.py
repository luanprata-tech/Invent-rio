import os
import sys

# Append backend directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.asset import Asset
from app.models.ip import IP
from app.models.attributes import Brand, Category, Department

def main():
    list_path = "lista0904.txt"
    if not os.path.exists(list_path):
        list_path = "../lista0904.txt"
    if not os.path.exists(list_path):
        print(f"File not found.")
        return

    db = SessionLocal()

    # Ensure required attributes exist
    cat = db.query(Category).filter(Category.name.ilike("Computador")).first()
    if not cat:
        db.add(Category(name="Computador"))
        
    brand = db.query(Brand).filter(Brand.name.ilike("Padrão")).first()
    if not brand:
        db.add(Brand(name="Padrão"))
        
    dept = db.query(Department).filter(Department.name.ilike("GEINFORM")).first()
    if not dept:
        db.add(Department(name="GEINFORM"))
        
    db.commit()

    with open(list_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()

    added = 0
    skipped = 0

    for line in lines:
        parts = line.strip().split()
        if len(parts) < 3:
            continue
            
        # Try to parse Host (A) records
        # Ex: CMCTS-102       Host (A)        172.23.6.102    ?01/?03/?2024 10:00:00
        # The columns are tab or space separated. 'Host' and '(A)' might be parts[1] and parts[2].
        # Let's search for the IP pattern in the line
        
        name = parts[0]
        
        if "Host" in line and "(A)" in line:
            # Extract IP address
            import re
            match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', line)
            if not match:
                continue
            ip_addr = match.group(0)
            
            # Check if it's in 172.23.6.0/24
            if not ip_addr.startswith("172.23.6."):
                continue
                
            # Check if IP already allocated
            db_ip = db.query(IP).filter(IP.ip_address == ip_addr).first()
            if db_ip and (db_ip.status == "Alocado" or db_ip.asset_id is not None):
                print(f"Skipping {ip_addr}: already allocated (status={db_ip.status}, asset_id={db_ip.asset_id})")
                skipped += 1
                continue
                
            # Check if asset with same device_name exists to prevent duplicates
            db_asset = db.query(Asset).filter(Asset.device_name == name, Asset.is_deleted == False).first()
            if db_asset:
                print(f"Skipping {name}: asset already exists")
                skipped += 1
                continue
                
            print(f"Adding PC: {name} with IP: {ip_addr}")
            
            new_asset = Asset(
                category="Computador",
                brand="Padrão",
                department="GEINFORM",
                device_name=name,
                patrimony_number="SEM-PAT"
            )
            db.add(new_asset)
            db.commit()
            db.refresh(new_asset)
            
            if not db_ip:
                db_ip = IP(ip_address=ip_addr, subnet="172.23.6.0/24", status="Alocado", asset_id=new_asset.id)
                db.add(db_ip)
            else:
                db_ip.status = "Alocado"
                db_ip.asset_id = new_asset.id
                db_ip.subnet = "172.23.6.0/24"
                
            db.commit()
            added += 1

    print(f"Process finished! Added: {added}, Skipped: {skipped}")

if __name__ == "__main__":
    main()
