from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


#Entidad user
class User(BaseModel):
    id: int
    nombre: str
    edad: int

class User_db(User):
    password: str


app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

users_db =  {
                "Lorenzo":{"id":1, "nombre":"Lorenzo", "edad":21, "password":"123456"},
                "Lazaro":{"id":2, "nombre":"Lazaro", "edad":19, "password":"654321"}
            }

def buscar_usuario_db(username: str):
    if username in users_db:
        return User_db(**users_db[username])
    
def buscar_usuario(username: str):
    if username in users_db:
        return User(**users_db[username])

    
async def current_user(token: str = Depends(oauth2)):
    user = buscar_usuario(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="acceso no autorizado",
            headers={"WWW-Authenticate":"Bearer"})
    
    return user


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Nombre de usuario incorrecto")
    
    user = buscar_usuario_db(form.username)

    if not user.password == form.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password incorrecta")

    return {"access_token":user.nombre ,"token_type":"bearer" }


@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
