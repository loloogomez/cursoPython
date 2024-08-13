from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError

algoritmo = "HS256"
duracion = 1
seed = "58bb898b82b6b5ae35fe7ba4abbae58a7420e6f45ab94715cf746668ac5ee4df"

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

#Entidad user
class User(BaseModel):
    id: int
    nombre: str
    edad: int

class User_db(User):
    password: str


users_db =  {
                "Lorenzo":{"id":1, "nombre":"Lorenzo", "edad":21, "password":"$2a$12$W5zmVXKBAN2oQ8F1Ea.M2ewKQCyYxYNb5huQntQOX0z9PvSdHb08u"},
                "Lazaro":{"id":2, "nombre":"Lazaro", "edad":19, "password":"$2a$12$vBW6FRaYP0SkIvqGxZ5ALuHB211xehQA54Rkn2FXp9pq6NR50SCYW"}
            }

def buscar_usuario_db(username: str):
    if username in users_db:
        return User_db(**users_db[username])
    
def buscar_usuario(username:str):
    if username in users_db:
        return User(**users_db[username])
    
def usuario_autenticado(access_token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="acceso no autorizado",
            headers={"WWW-Authenticate":"Bearer"})
    
    try:
        username = jwt.decode(access_token, seed, algorithms=[algoritmo]).get("sub")
        if username is None:
            raise exception
    
    except InvalidTokenError:
        raise exception
    
    return buscar_usuario(username)


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Nombre de usuario incorrecto")
    
    user = buscar_usuario_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password incorrecta")

    token_expiration = timedelta(hours=duracion)

    access_token = {"sub":user.nombre,
                    "exp":datetime.now(timezone.utc) + token_expiration,
                    }
 
    return {"access_token": jwt.encode(access_token, seed, algorithm=algoritmo) ,"token_type":"bearer" }


@app.get("/users/me", response_model=User, status_code=200)
async def me(user: User = Depends(usuario_autenticado)):
    return user
