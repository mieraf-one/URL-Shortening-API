from fastapi import FastAPI
from app.routers import auth as auth_router
from app.routers import urls as urls_router


app = FastAPI()


app.include_router(auth_router.router)
app.include_router(urls_router.router)