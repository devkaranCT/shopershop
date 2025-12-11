from fastapi import FastAPI
import models
from database import engine
from routers import auth, products, cart

app = FastAPI()

# used to set up your database schema based on your Python models
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
