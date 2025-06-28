from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

db_path = os.path.join(os.getcwd(), "store.sqlite3")
print("Creating DB at:", db_path)

engine = create_engine(f'sqlite:///{db_path}', echo=True)

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'product'
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Float)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    category = relationship("Category", back_populates="products")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

if not session.query(Category).first():
    electronics = Category(category_name='Electronics')
    fashion = Category(category_name='Fashion')
    groceries = Category(category_name='Groceries')
    session.add_all([electronics, fashion, groceries])
    session.commit()

    products = [
        Product(product_name='Laptop', price=75000.0, category_id=electronics.category_id),
        Product(product_name='T-Shirt', price=999.0, category_id=fashion.category_id),
        Product(product_name='Rice Bag', price=1200.0, category_id=groceries.category_id),
        Product(product_name='Headphones', price=1500.0, category_id=electronics.category_id)
    ]
    session.add_all(products)
    session.commit()

print("\n=== Product List ===")
for p in session.query(Product).all():
    print(f"{p.product_name} - ₹{p.price} ({p.category.category_name})")
