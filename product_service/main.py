from fastapi import FastAPI
from database import engine, Base
import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Product Service Running"}