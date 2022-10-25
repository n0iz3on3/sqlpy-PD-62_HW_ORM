import sqlalchemy as sqa
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sqa.Column(sqa.Integer, primary_key=True)
    name = sqa.Column(sqa.String(length=45), nullable=False)

    def __str__(self):
        return f'Publisher id: {self.id} \nName: {self.name}\n'


class Book(Base):
    __tablename__ = "book"

    id = sqa.Column(sqa.Integer, primary_key=True)
    title = sqa.Column(sqa.String(length=45), nullable=False)
    id_publisher = sqa.Column(sqa.Integer, sqa.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

    def __str__(self):
        return f'{self.title}\n'


class Shop(Base):
    __tablename__ = "shop"

    id = sqa.Column(sqa.Integer, primary_key=True)
    name = sqa.Column(sqa.String(length=45), nullable=False)


class Stock(Base):
    __tablename__ = "stock"

    id = sqa.Column(sqa.Integer, primary_key=True)
    id_book = sqa.Column(sqa.Integer, sqa.ForeignKey("book.id"), nullable=False)
    id_shop = sqa.Column(sqa.Integer, sqa.ForeignKey("shop.id"), nullable=False)
    count = sqa.Column(sqa.Integer, nullable=False)

    book = relationship(Book, backref="stock1")
    shop = relationship(Shop, backref="stock2")


class Sale(Base):
    __tablename__ = "sale"

    id = sqa.Column(sqa.Integer, primary_key=True)
    price = sqa.Column(sqa.Numeric, nullable=False)
    date_sale = sqa.Column(sqa.Date, nullable=False)
    id_stock = sqa.Column(sqa.Integer, sqa.ForeignKey("stock.id"), nullable=False)
    count = sqa.Column(sqa.Integer, nullable=False)

    stock = relationship(Stock, backref="sale")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)