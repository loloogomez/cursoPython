from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])

class Product(BaseModel):
    id: int
    nombre: str
    cantidad: int
    precio: float

productos_db = [Product(id=1, nombre="pan", cantidad=10, precio=10),
                Product(id=2, nombre="budin", cantidad=20, precio=20),
                Product(id=3, nombre="facturas", cantidad=30, precio=30)]

@router.get("/")
async def products():
    return productos_db


