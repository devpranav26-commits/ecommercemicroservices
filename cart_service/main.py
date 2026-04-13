from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
import service

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Cart Service Running"}

# 🔥 ADD TO CART API
@app.post("/cart/add")
def add_to_cart(user_id: int, product_id: int, quantity: int, db: Session = Depends(get_db)):
    try:
        return service.add_to_cart_service(db, user_id, product_id, quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))