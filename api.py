from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DOIRecordDB(Base):
    __tablename__ = "dois"
    id = Column(Integer, primary_key=True, index=True)
    doi = Column(String(255), unique=True, index=True)
    title = Column(String(512))
    authors = Column(String(1024))
    journal = Column(String(512))
    year = Column(Integer)
    url = Column(String(1024))
    read = Column(Boolean)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class DOIRecord(BaseModel):
    doi: str
    title: str
    authors: str
    journal: str
    year: int
    url: str
    read: bool

@app.post("/guardar_doi")
def guardar_doi(record: DOIRecord, db: Session = Depends(get_db)):
    db_record = db.query(DOIRecordDB).filter(DOIRecordDB.doi == record.doi).first()
    if db_record:
        raise HTTPException(status_code=400, detail="El DOI ya está registrado")
    new_record = DOIRecordDB(**record.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "DOI almacenado exitosamente"}

@app.get("/dois", response_model=List[DOIRecord])
def obtener_dois(db: Session = Depends(get_db)):
    return db.query(DOIRecordDB).all()
