from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, time, timedelta
from pydantic import BaseModel
#---------------------------------------------------------------------

#sqlite_file_name = "database.db"
#sqlite_url = f"sqlite:///data/{sqlite_file_name}"
#connect_args = {"check_same_thread": False}
#engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

#---------------------------------------------------------------------

# database principal table

class tb_falta_agua(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True, nullable=False)
  ide: str | None
  ra: str | None
  end: str | None
  inicio: datetime | None
  fim: datetime | None
  tipo: str | None
  motivo: str | None
  tempo: str | None 
  hora_inicio: time | None # time
  hora_fim: time | None # time
  mes: str |  None
  ano: str | None 
  ra_num: int | None 
  CD_SUBDIST: int | None
  data_regristro: str | None #datetime | None #datetime | None
  class Config:
        table_args = {"extend_existing": True}

# modelo table de registro de situacao

class tb_registro(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True, nullable=False)
  situacao: str | None
  data_registro: datetime | None
  class Config:
    table_args = {"extend_existing": True}

#SQLModel.metadata.create_all(engine)
