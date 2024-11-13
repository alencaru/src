from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime, time, timedelta
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional
from pandas_to_pydantic import dataframe_to_pydantic

sqlite_file_name = "database2.db"
sqlite_url = f"sqlite:///data/{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

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
  mes: int |  None
  ano: int | None 
  ra_num: int | None 
  CD_SUBDIST: int | None
  data_regristro: datetime | None #datetime | None
  class Config:
      table_args = {"extend_existing": True}

tb = pd.read_csv('teste_table.csv')
tb.set_index('ra_num', inplace=True, drop=False)
tb['data_registro'] = datetime.now()
tb['CD_SUBDIST'] = int(tb['CD_SUBDIST'])

#pd.to_datetime(tb.data_registro, format="%Y-%m-%d %H:%M:%S.%f") #infer_datetime_format=True) 

class pydantic_table(BaseModel):
   #id: Optional[int] = None
   ide: str | None
   ra: str | None
   end: str | None
   inicio: datetime | None
   fim: datetime | None
   tipo: str | None
   motivo: str | None
   tempo: str | None 
   hora_inicio: time | None
   hora_fim: time | None
   mes: int |  None
   ano: int | None 
   ra_num: int | None 
   CD_SUBDIST: int | None
   data_registro: datetime | None 

tb_model = dataframe_to_pydantic(tb, pydantic_table)

def df_to_sqlmodel(df: pd.DataFrame) -> List[SQLModel]:
    """Convert a pandas DataFrame into a a list of SQLModel objects."""    
    objs = [tb_falta_agua(**row) for row in df.to_dict('records')]
    with Session(engine) as session:
        session.add(*objs)
        session.commit()
    session.close()
    #return objs

sql_model_objs = df_to_sqlmodel(tb)

with Session(engine) as session:
  session.add(tb_model)
  session.commit()
  session.refresh(tb_model)
  session.close()


#for i in sql_model_objs:
#    print(i)


