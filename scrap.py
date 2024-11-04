from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from sqlmodel import Field, Session, SQLModel, create_engine, select
import time
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger
from pydantic import BaseModel
from pandas_to_pydantic import dataframe_to_pydantic
import re
from unidecode import unidecode
import os
import sys
import pathlib
import json

import functions.data_etl as etl
from models.estruturas import tb_registro, tb_falta_agua

#---------------------------------------------------------
# logger

logger.info('Script iniciado')

#----------------------------------------------------------
# database 

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///data/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)
SQLModel.metadata.create_all(engine)

# params definition --------------------------------------

date_reg = datetime.now()

chrome_pathexe = r'C:/Users/alencar/Documents/DataScience/chrome_driver/chromedriver-win64/chromedriver.exe'
url = "https://www.caesb.df.gov.br/portal-servicos/app/publico/consultarfaltadagua?execution=e1s1"
elem_xpath = '/html/body/div[4]/div/div/div/main/article/div/section[2]/div[2]/div[3]/div/div[1]/form'

#--------------------------------------------------------

service = Service(executable_path=chrome_pathexe)

options = webdriver.ChromeOptions()
options.add_argument('--hedless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome(service=service, options=options)
wd.get(url)
wd.find_element(By.XPATH, elem_xpath)
time.sleep(1)

html = wd.page_source
time.sleep(1)

table = pd.read_html(html)

#------------------------------------------------------
# Tratando a inexistência de dados na tabela

firstlinetable = table[0].iloc[0][1]
date = datetime.now()

if firstlinetable == "Faltas de Água não encontradas":
  logger.warning('{}', firstlinetable)
  with open("log.txt", "w") as text_file: 
    print(f"{date} | {firstlinetable}", file=text_file)
    text_file.close()

  tdd = pd.DataFrame({'situacao': [firstlinetable], 'date': [date]})

  try:
    with Session(engine) as session:
      for _, row in tdd.iterrows():
        tda = tb_registro(
          situacao=row['situacao'],
          data_registro=row['date']
        )
        session.add(tda)
      session.commit()

  except Exception as e:
    print(f"An error occurred: {e}")
  
else:
  information = 'Infos de falta de agua coletados e salvos emn arquivo csv'
  logger.debug(information)
  table[0].to_csv('src/data/data.csv', mode='a', header=False, encoding="utf-8") 

  tb = etl.etl_process(df = table[0], tabela_ra_path='src/data/table_ra.csv')  # backup
  
  # colocar o loop da outra tabela caso tenho dados

  with Session(engine) as session:
    for _, row in tb.iterrows():
      td = tb_falta_agua(
        ide = row['ide'],
        ra =  row['ra'],
        end =  row['end'],
        inicio =  row['inicio'],
        fim =  row['fim'],
        tipo = row['tipo'],
        motivo =  row['motivo'],
        tempo = row['tempo'],
        hora_inicio = row['hora_inicio'],
        hora_fim = row['hora_fim'],
        mes = row['mes'],
        ano = row['ano'],
        ra_num = row['ra_num'],
        CD_SUBDIST = int | None,
        data_regristro = date.strftime('%d/%m/%Y')
      )
      session.add(td)
    session.commit()

# final logger
logger.info('Script finalizado')
logger.add('log.log')

# end
wd.quit()