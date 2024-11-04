import pandas as pd
from sqlmodel import SQLModel, Field, create_engine, Session

# Dados do primeiro DataFrame (Person)
data1 = {
    "id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
}
df1 = pd.DataFrame(data1)

# Dados do segundo DataFrame (Product)
data2 = {
    "id": [1, 2, 3],
    "product": ["Laptop", "Phone", "Tablet"],
    "price": [1000, 500, 300],
}
df2 = pd.DataFrame(data2)

# Definir a classe SQLModel para a tabela Person
class Person(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    age: int

# Definir a classe SQLModel para a tabela Product
class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    product: str
    price: float

# Conectar ao banco SQLite
engine = create_engine("sqlite:///database.db")

# Criar as tabelas no banco de dados
SQLModel.metadata.create_all(engine)

# Inserir os dados do DataFrame df1 na tabela Person
with Session(engine) as session:
    for _, row in df1.iterrows():
        person = Person(id=row['id'], name=row['name'], age=row['age'])
        session.add(person)
    session.commit()

# Inserir os dados do DataFrame df2 na tabela Product
with Session(engine) as session:
    for _, row in df2.iterrows():
        product = Product(id=row['id'], product=row['product'], price=row['price'])
        session.add(product)
    session.commit()

print("Dados salvos no banco de dados SQLite com sucesso!")