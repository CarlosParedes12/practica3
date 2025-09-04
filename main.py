from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Base, engine, get_db
from models import Usuario

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Practica3 Web Service", version="1.0.0")

class UsuarioIn(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    correo: EmailStr | None = None
    password: str | None = None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/usuarios", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.post("/api/usuarios", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(data: UsuarioIn, db: Session = Depends(get_db)):
    u = Usuario(nombre=data.nombre, correo=data.correo, password=data.password)
    db.add(u)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El correo ya existe")
    db.refresh(u)
    return u
