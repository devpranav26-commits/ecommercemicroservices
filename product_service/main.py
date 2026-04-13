from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
import service

Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Product Service Running"}

# CREATE
@app.post("/products")
def create_product(name: str, price: float, stock: int, db: Session = Depends(get_db)):
    try:
        return service.create_product_service(db, name, price, stock)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# GET ALL
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return service.get_all_products_service(db)

# GET BY ID
@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return service.get_product_by_id_service(db, product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# UPDATE
@app.put("/products/{product_id}")
def update_product(product_id: int, name: str, price: float, stock: int, db: Session = Depends(get_db)):
    try:
        return service.update_product_service(db, product_id, name, price, stock)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# DELETE
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return service.delete_product_service(db, product_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# PAGINATION
@app.get("/products/paginated")
def get_products_paginated(page: int = 1, size: int = 5, sort_by: str = "id", db: Session = Depends(get_db)):
    return service.get_products_paginated_service(db, page, size, sort_by)

# 🔥 NATIVE QUERY API
@app.get("/products/price-filter")
def get_products_above_price(price: float, db: Session = Depends(get_db)):
    return service.get_products_above_price_service(db, price)