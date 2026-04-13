from sqlalchemy.orm import Session
from models import Product

# CREATE
def create_product(db: Session, product: Product):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

# READ ALL
def get_all_products(db: Session):
    return db.query(Product).all()

# READ BY ID
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