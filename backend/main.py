from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Notas Stats v5")

class Nota(BaseModel):
    estudiante_id:int
    asignatura_id:int
    valor:str|None=None
    estado:str|None=None

@app.get("/")
def home():
    return {"app":"Notas Stats v5","status":"running"}

@app.post("/notas")
def crear_nota(nota:Nota):
    return nota