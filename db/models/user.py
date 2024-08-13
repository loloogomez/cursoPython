from pydantic import BaseModel

#Entidad user
class User(BaseModel):
    id: str | None = None
    nombre: str
    edad: int