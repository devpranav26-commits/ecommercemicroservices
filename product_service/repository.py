from sqlalchemy.orm import Session
from sqlalchemy import text
from models import Product

# CREATE
def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# GET ALL
def get_all_products(db: Session):
    return db.query(Product).all()

# GET BY ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# UPDATE
def update_product(db: Session, product_id: int, name: str, price: float, stock: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.name = name
        product.price = price
        product.stock = stock
        db.commit()
        db.refresh(product)
    return product

# DELETE
def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    return product

# PAGINATION + SORTING
def get_products_paginated(db: Session, page: int, size: int, sort_by: str):

    query = db.query(Product)

    if sort_by == "price":
        query = query.order_by(Product.price)
    elif sort_by == "name":
        query = query.order_by(Product.name)
    elif sort_by == "stock":
        query = query.order_by(Product.stock)
    else:
        query = query.order_by(Product.id)

    offset = (page - 1) * size

    return query.offset(offset).limit(size).all()

# 🔥 NATIVE QUERY
def get_products_above_price(db: Session, price: float):
    query = text("SELECT * FROM products WHERE price > :price")
    result = db.execute(query, {"price": price})
    return result.fetchall()