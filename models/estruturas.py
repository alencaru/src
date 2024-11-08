from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, time, timedelta
from pydantic import BaseModel
#---------------------------------------------------------------------

sqlite_file_name = "database3.db"
sqlite_url = f"sqlite:///data/{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args, extend_existing=True)

#---------------------------------------------------------------------

# database principal table

class tb_falta_agua(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True, nullable=False)
  ide: str | None
  ra: str | None
  end: str | None
  inicio: str | None
  fim: str | None
  tipo: str | None
  motivo: str | None
  tempo: str | None # timedelta
  hora_inicio: str | None # time
  hora_fim: str | None # time
  mes: str |  None
  ano: str | None 
  ra_num: int | None 
  CD_SUBDIST: int | None
  data_regristro: str | None #datetime | None

# modelo table de registro de situacao

class tb_registro(SQLModel, table=True):
  id: int | None = Field(default=None, primary_key=True, nullable=False)
  situacao: str | None
  data_registro: datetime | None

SQLModel.metadata.create_all(engine)
