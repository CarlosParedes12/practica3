from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre:     Mapped[str] = mapped_column(String(100), nullable=False)
    correo:     Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password:   Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_reg:  Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
