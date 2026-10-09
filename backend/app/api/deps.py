from typing import Generator, Optional
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.models.user import User
from app.db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db = Depends(get_db), token: Optional[str] = Depends(oauth2_scheme)):
    if not token:
        token = request.cookies.get("access_token")
        
    if not token:
        if request.url.path.startswith("/api/"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
        else:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
            
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
    except JWTError:
        if request.url.path.startswith("/api/"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
        else:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        if request.url.path.startswith("/api/"):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não autenticado")
        else:
            raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, headers={"Location": "/"})
    return user
