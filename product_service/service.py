from sqlalchemy.orm import Session
import models
import repository

# CREATE PRODUCT (Business Logic)
def create_product_service(db: Session, name: str, price: float, stock: int):
    
    # Validation (Business Rule)
    if stock < 0:
        raise Exception("Stock cannot be negative")

    if price <= 0:
        raise Exception("Price must be greater than 0")

    product = models.Product(
        name=name,
        price=price,
        stock=stock
    )

    return repository.create_product(db, product)


# GET ALL PRODUCTS
def get_all_products_service(db: Session):
    return repository.get_all_products(db)


# GET PRODUCT BY ID
def get_product_by_id_service(db: Session, product_id: int):
    product = repository.get_product_by_id(db, product_id)

    if not product:
        raise Exception("Product not found")

    return product


# UPDATE PRODUCT
def update_product_service(db: Session, product_id: int, name: str, price: float, stock: int):
    
    if stock < 0:
        raise Exception("Stock cannot be negative")

    product = repository.update_product(db, product_id, name, price, stock)

    if not product:
        raise Exception("Product not found")

    return product


# DELETE PRODUCT
def delete_product_service(db: Session, product_id: int):
    product = repository.delete_product(db, product_id)

    if not product:
        raise Exception("Product not found")

    return {"message": "Product deleted successfully"}