import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = 'postgresql://postgres:...m@localhost:5432/bookmart_db'
engine = sqlalchemy.create_engine(DSN)

# Создание всех таблиц из modules.py
create_tables(engine)

# Создание сессии для управления данными в БД
Session = sessionmaker(bind=engine)
session = Session()

# Получить данные для заполенния БД из .json
def get_data_json():
    with open("tests_data.json", "r") as f:
        data = json.load(f)
        return data
    
data_to_upload = get_data_json()

# Загрузить данные в таблицы по инструкции
def upload_to_db(data):
    for record in data:
        model = {
            "publisher": Publisher,
            "book": Book,
            "shop": Shop,
            "stock": Stock,
            "sale": Sale
            }[record.get("model")]
        session.add(model(id=record.get("pk"), **record.get("fields")))
    session.commit()

upload_to_db(data_to_upload)

# Вывод всех книг издателя по айди или имени
ask = input("Введите имя издателя или его айди: \n")
try:
    ask = int(ask)
    subq = session.query(Publisher).filter(Publisher.id == ask).subquery()
    print("\nВсе книги издателя:")
    for element in session.query(Book).join(subq, Book.id_publisher == subq.c.id).all():
        print(element)
    print("\nМагазины, где продается издатель: ")
    for element in session.query(Shop).join(Stock).join(Book).join(Publisher).join(subq).all():
        print(element.name)
except ValueError:
    subq = session.query(Publisher).filter(Publisher.name == ask).subquery()
    print("\nВсе книги издателя:")
    for element in session.query(Book).join(subq, Book.id_publisher == subq.c.id).all():
        print(element)
    print("\nМагазины, где продается издатель: ")
    for element in session.query(Shop).join(Stock).join(Book).join(Publisher).join(subq).all():
        print(element.name)

session.close()
