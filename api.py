from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

database = []  # Lista temporal para almacenar los datos

class DOIRecord(BaseModel):
    doi: str
    title: str
    authors: str
    journal: str
    year: int
    url: str
    read: bool

@app.post("/guardar_doi")
def guardar_doi(record: DOIRecord):
    if any(item.doi == record.doi for item in database):
        raise HTTPException(status_code=400, detail="El DOI ya está registrado")
    database.append(record)
    return {"message": "DOI almacenado exitosamente"}

@app.get("/dois", response_model=List[DOIRecord])
def obtener_dois():
    return database
