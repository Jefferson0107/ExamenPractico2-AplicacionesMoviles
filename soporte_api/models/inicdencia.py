from datetime import datetime
from enum import Enum
from typing import Optional
import sqlalchemy as sa
from sqlmodel import SQLModel, Field
 
 
class Prioridad(str, Enum):
    baja = "Baja"
    media = "Media"
    alta = "Alta"
 
 
class Estado(str, Enum):
    pendiente = "Pendiente"
    en_proceso = "En proceso"
    resuelta = "Resuelta"
 
 
class IncidenciaBase(SQLModel):
    nombre_usuario: str = Field(max_length=100)
    correo: str = Field(max_length=150)
    numero_equipo: int
    descripcion: str = Field(max_length=500)
    prioridad: Prioridad
    estado: Estado
 
 
class Incidencia(IncidenciaBase, table=True):
    __tablename__ = "incidencias"
 
    id: Optional[int] = Field(default=None, primary_key=True)
 
    prioridad: Prioridad = Field(
        sa_column=sa.Column(
            sa.Enum(Prioridad, values_callable=lambda enum_cls: [e.value for e in enum_cls], name="prioridad"),
            nullable=False,
        )
    )
    estado: Estado = Field(
        sa_column=sa.Column(
            sa.Enum(Estado, values_callable=lambda enum_cls: [e.value for e in enum_cls], name="estado"),
            nullable=False,
        )
    )
 
    fecha_registro: Optional[datetime] = Field(
        default=None,
        sa_column=sa.Column(sa.DateTime, server_default=sa.func.now(), nullable=False),
    )
 
 
class IncidenciaCreate(IncidenciaBase):
    pass
 
 
class IncidenciaUpdate(SQLModel):
    nombre_usuario: Optional[str] = None
    correo: Optional[str] = None
    numero_equipo: Optional[int] = None
    descripcion: Optional[str] = None
    prioridad: Optional[Prioridad] = None
    estado: Optional[Estado] = None
 
 
class IncidenciaRead(IncidenciaBase):
    id: int
    fecha_registro: datetime
 