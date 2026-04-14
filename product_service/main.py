from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import threading

from database import engine, SessionLocal, Base
import models
import service
import consumer

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

# CREATE PRODUCT
@app.post("/products")
def create_product(name: str, price: int, stock: int, db: Session = Depends(get_db)):
    return service.create_product_service(db, name, price, stock)

# GET PRODUCT BY ID
@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = service.get_product_service(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# GET ALL PRODUCTS
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return service.get_all_products_service(db)


# 🔥 START KAFKA CONSUMER IN BACKGROUND
def start_kafka():
    consumer.start_consumer()

thread = threading.Thread(target=start_kafka)
thread.daemon = True
thread.start()