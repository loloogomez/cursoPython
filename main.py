from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import users, products
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()

#routers
app.include_router(users.router)
app.include_router(products.router)

#static files
app.mount("/static", StaticFiles(directory="static"), name="statico")


@app.post("/items/")
async def create_item(item: Item):
    return item