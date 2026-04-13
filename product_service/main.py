from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models

# CREATE TABLES
Base.metadata.create_all(bind=engine)

app = FastAPI()

# DB Dependency (like @Autowired in Spring)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TEST API
@app.get("/")
def read_root():
    return {"message": "Product Service Running"}