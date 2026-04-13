from fastapi import FastAPI
from database import engine, Base
import models  # IMPORTANT (for tables)

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Sample Service Running"}