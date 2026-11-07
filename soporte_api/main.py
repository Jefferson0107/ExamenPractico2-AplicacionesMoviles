from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, select
from config.db import engine, get_session
from models.inicdencia import Incidencia, IncidenciaCreate, IncidenciaRead, IncidenciaUpdate

app = FastAPI(title="SoporteApp API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.post("/incidencias", response_model=IncidenciaRead, status_code=status.HTTP_201_CREATED)
def crear_incidencia(data: IncidenciaCreate, session: Session = Depends(get_session)):
    incidencia = Incidencia.model_validate(data)
    session.add(incidencia)
    session.commit()
    session.refresh(incidencia)
    return incidencia


@app.get("/incidencias", response_model=List[IncidenciaRead])
def listar_incidencias(session: Session = Depends(get_session)):
    return session.exec(select(Incidencia).order_by(Incidencia.id.desc())).all()


@app.get("/incidencias/{incidencia_id}", response_model=IncidenciaRead)
def obtener_incidencia(incidencia_id: int, session: Session = Depends(get_session)):
    incidencia = session.get(Incidencia, incidencia_id)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    return incidencia


@app.put("/incidencias/{incidencia_id}", response_model=IncidenciaRead)
def actualizar_incidencia(
    incidencia_id: int, data: IncidenciaUpdate, session: Session = Depends(get_session)
):
    incidencia = session.get(Incidencia, incidencia_id)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(incidencia, key, value)

    session.add(incidencia)
    session.commit()
    session.refresh(incidencia)
    return incidencia


@app.delete("/incidencias/{incidencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_incidencia(incidencia_id: int, session: Session = Depends(get_session)):
    incidencia = session.get(Incidencia, incidencia_id)
    if not incidencia:
        raise HTTPException(status_code=404, detail="Incidencia no encontrada")
    session.delete(incidencia)
    session.commit()
