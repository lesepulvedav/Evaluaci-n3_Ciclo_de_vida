from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Tienda de Lácteos API")

class Lacteo(BaseModel):
    id: int
    nombre: str
    tipo: str
    precio: float
    stock: int

# Base de datos inicial
inventario = [
    Lacteo(id=1, nombre="Leche Entera 1L", tipo="Leche", precio=1.50, stock=100),
]

@app.get("/productos", response_model=List[Lacteo])
def obtener_productos():
    return inventario

@app.post("/productos", response_model=Lacteo)
def crear_producto(producto: Lacteo):
    for p in inventario:
        if p.id == producto.id:
            raise HTTPException(status_code=400, detail="El ID del producto ya existe")
    inventario.append(producto)
    return producto