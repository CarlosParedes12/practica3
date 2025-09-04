from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Base, engine, SessionLocal
from models import Usuario

# Inicializar tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Practica 3 - Web Service con FastAPI y Render")

# Dependencia para manejar sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- SCHEMAS (Pydantic) -----------

class UsuarioIn(BaseModel):
    nombre: str
    correo: EmailStr
    password: str

class UsuarioOut(BaseModel):
    id_usuario: int
    nombre: str
    correo: EmailStr
    password: str
    class Config:
        orm_mode = True

class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    correo: EmailStr | None = None
    password: str | None = None

# ----------- ENDPOINTS -----------

@app.get("/")
def root():
    return {"mensaje": "Bienvenido al Web Service de Practica 3 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()

@app.get("/api/usuarios/{id_usuario}", response_model=UsuarioOut)
def obtener_usuario(id_usuario: int, db: Session = Depends(get_db)):
    u = db.get(Usuario, id_usuario)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u

@app.post("/api/usuarios", response_model=UsuarioOut)
def crear_usuario(usuario: UsuarioIn, db: Session = Depends(get_db)):
    nuevo = Usuario(**usuario.dict())
    db.add(nuevo)
    try:
        db.commit()
        db.refresh(nuevo)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El correo ya existe")
    return nuevo

@app.put("/api/usuarios/{id_usuario}", response_model=UsuarioOut)
def actualizar_usuario(id_usuario: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    u = db.get(Usuario, id_usuario)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if data.nombre is not None:
        u.nombre = data.nombre
    if data.correo is not None:
        u.correo = data.correo
    if data.password is not None:
        u.password = data.password
    try:
        db.commit()
        db.refresh(u)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El correo ya existe")
    return u

@app.delete("/api/usuarios/{id_usuario}", status_code=204)
def eliminar_usuario(id_usuario: int, db: Session = Depends(get_db)):
    u = db.get(Usuario, id_usuario)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(u)
    db.commit()
    return None

