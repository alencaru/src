#from pydantic import BaseModel
import pandas as pd
from unidecode import unidecode

def etl_process(df, tabela_ra_path):
    
    #df = pd.DataFrame(columns = range(6))
    # fazer função para renomear colunas sem depender da posição e da quantidade de colunas
    df = df.set_axis(["ra", "end", "inicio", "fim", "tipo", "motivo"], axis='columns')

    #df = pd.DataFrame([d.dict()])
    df["inicio"] = df["inicio"].str.replace(' às ', ' ').str.replace('h', ':')
    df["inicio"] = pd.to_datetime(df["inicio"], format='%d/%m/%Y %H:%M:%S')

    df["fim"] = df["fim"].str.replace(' às ', ' ').str.replace('h', ':')
    df["fim"] = pd.to_datetime(df["fim"], format='%d/%m/%Y %H:%M:%S')

    df["tempo"] = (df["fim"] - df["inicio"])

    #-------------------------------------------------------------------------------
    # criando a coluna de hora inicial e final

    df["hora_inicio"] = df['inicio'].dt.time
    df["hora_fim"] = df['fim'].dt.time

    #-------------------------------------------------------------------------------
    # criando o id_ra

    df["ide"] = df["ra"].str.casefold().str.replace(" ", "_")
    df["ide"] = df["ide"].str.casefold().str.replace("/", "_")
    df["ide"] = df["ide"].apply(unidecode)

    # criando da coluna mes e ano
    df["ano"] = pd.to_datetime(df['inicio']).dt.strftime('%Y')
    df["mes"] = pd.to_datetime(df['inicio']).dt.strftime('%m')
    df["mes_nome"] = df['inicio'].apply(lambda x: x.strftime('%B')) 

    #-------------------------------------------------------------------------------
    # analisando o campo nome para definir a regra de divisão dos enderecos

    tabela_ra = pd.read_csv(tabela_ra_path)
    tabela_ra = tabela_ra.drop('Unnamed: 0', axis='columns')

    dfa = df.join(tabela_ra.set_index('ide'), on='ide')

    return(dfa)

#---------------
# testing

#table = etl_process(df=df, tabela_ra_path='./data/table_ra.csv')

#-------------------------------------------------------------------------------------