import sqlalchemy
import json
from sqlalchemy.orm import sessionmaker
from models import *

with open("connect.json", encoding="utf-8") as file:
    data = json.load(file)
    name = data["name"]
    password = data["password"]
    host = data["host"]
    port = data["port"]
    db_name = data["db_name"]

DSN = f'postgresql://{name}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

# Создание таблиц и связей
create_tables(engine)

# Добавление данных
with open("test_data.json", 'r', encoding="utf-8") as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

publ_name = input('Ведите имя писателя или id для вывода: ')
if publ_name.isnumeric():
    for c in session.query(Publisher).filter(
            Publisher.id == int(publ_name)).all():
        print(c)
else:
    for c in session.query(Publisher).filter(
            Publisher.name.like(f'%{publ_name}%')).all():
        print(c)

session.close()
