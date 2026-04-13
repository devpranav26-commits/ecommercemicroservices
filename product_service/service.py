from sqlalchemy.orm import Session
import models
import repository

# CREATE
def create_product_service(db: Session, name: str, price: float, stock: int):

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


# GET ALL
def get_all_products_service(db: Session):
    return repository.get_all_products(db)


# GET BY ID
def get_product_by_id_service(db: Session, product_id: int):
    product = repository.get_product_by_id(db, product_id)

    if not product:
        raise Exception("Product not found")

    return product


# UPDATE
def update_product_service(db: Session, product_id: int, name: str, price: float, stock: int):

    if stock < 0:
        raise Exception("Stock cannot be negative")

    product = repository.update_product(db, product_id, name, price, stock)

    if not product:
        raise Exception("Product not found")

    return product


# DELETE
def delete_product_service(db: Session, product_id: int):
    product = repository.delete_product(db, product_id)

    if not product:
        raise Exception("Product not found")

    return {"message": "Product deleted successfully"}


# PAGINATION + STREAMS
def get_products_paginated_service(db: Session, page: int, size: int, sort_by: str):

    products = repository.get_products_paginated(db, page, size, sort_by)

    # 🔥 Streams equivalent (filter + map)

    # Filter
    filtered = [p for p in products if p.stock > 0]

    # Transform
    result = [
        {
            "id": p.id,
            "name": p.name.upper(),
            "price": p.price,
            "stock": p.stock
        }
        for p in filtered
    ]

    return result