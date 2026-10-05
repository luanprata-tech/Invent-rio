from app.db.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = db.query(User).filter(User.username == "admin").first()
    if not user:
        admin_user = User(
            username="admin",
            hashed_password=get_password_hash("admin")
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print("Usuário admin/admin criado com sucesso!")
    else:
        print("Usuário admin já existe.")
    db.close()

if __name__ == "__main__":
    print("Inicializando banco de dados...")
    init_db()
