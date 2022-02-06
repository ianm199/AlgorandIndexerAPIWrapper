import psycopg2
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import sessionmaker
Base = declarative_base()
engine = create_engine('postgresql://postgres:Billyboy7!@database-1.cr1i9jzgfqhq.us-east-2.rds.amazonaws.com')
Session = sessionmaker(bind=engine)


class Product(Base):
    __tablename__ = "products"
    id=Column(Integer, primary_key=True)
    title=Column('title', String(32))
    in_stock=Column('in_stock', Boolean)
    quantity=Column('quantity', Integer)
    price=Column('price', Numeric)

if __name__ == '__main__':
    print("teest!")