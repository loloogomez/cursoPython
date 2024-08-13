from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"message":"No encontrado"}})


@router.get("/", response_model=list[User], status_code=201)
async def users():
    return users_schema(db_client.users.find())

#por path
@router.get("/{id}", response_model=User, status_code=200)
async def user(id:str):
    aux = search_user("_id", ObjectId(id))
    if (type(aux) == User):
        return aux
    else:
        raise HTTPException(status_code=404, detail="El usuario no fue encontrado")

@router.post("/", response_model=User, status_code=201) #201 http code for created
async def user(user: User):

    user_dict = dict(user)

    tipo = type(search_user("nombre", user.nombre))
    
    if not (tipo == User):           
        del user_dict["id"]

        id = db_client.users.insert_one(user_dict).inserted_id

        new_user = user_schema(db_client.users.find_one({"_id":id}))

        return User(**new_user)

    else:
        raise HTTPException(status_code=400, detail="El usuario ya esta cargado")

@router.put("/", response_model=User, status_code=200)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=204)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
    if not found:
        return {"error":"El usuario no se ha eliminado"}
    

def search_user(field: str, key: str):
    try:
        user = user_schema(db_client.users.find_one({field:key}))
        return User(**user)
    except:
        return{"error":"Usuario no encontrado"}