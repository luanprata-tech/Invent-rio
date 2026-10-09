import os
import sys
import csv

# Append backend directory to path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.asset import Asset
from app.models.ip import IP

def main():
    db = SessionLocal()
    
    # Query all assets that are computers and not deleted
    assets = db.query(Asset).filter(Asset.is_deleted == False).all()
    
    # Sort by device_name
    assets.sort(key=lambda x: x.device_name if x.device_name else "")
    
    csv_file_path = "../Inventario_Completar.csv"
    
    with open(csv_file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        
        # Write header
        writer.writerow([
            "ID do Sistema", 
            "Nome do Dispositivo", 
            "Endereço IP", 
            "Tipo de Equipamento", 
            "Fabricante/Marca", 
            "Modelo", 
            "Número de Série", 
            "Número de Patrimônio", 
            "Data de Aquisição", 
            "Fonte de Recursos", 
            "Setor/Departamento", 
            "Usuário Responsável"
        ])
        
        for a in assets:
            # Get IP if allocated
            ip_addr = ""
            if a.ips:
                ip_addr = a.ips[0].ip_address
                
            writer.writerow([
                a.id,
                a.device_name or "",
                ip_addr,
                a.category or "",
                a.brand or "",
                a.model or "",
                a.serial_number or "",
                a.patrimony_number or "",
                a.acquisition_date or "",
                a.funding_source or "",
                a.department or "",
                a.responsible_user or ""
            ])
            
    print(f"Planilha exportada com sucesso para: {os.path.abspath(csv_file_path)}")

if __name__ == "__main__":
    main()
