from fastapi import FastAPI

from app.database import create_db
from app.routes import router

app = FastAPI()


@app.on_event("startup")
def initialize():
    create_db()


app.include_router(router)


@app.get("/")
async def root():
    return {"message": "url-shortener"}
