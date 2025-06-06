from fastapi import FastAPI

from app.routes import router
from app.database import create_db

app = FastAPI()


@app.on_event("startup")
def initialize():
    create_db()


app.include_router(router)

@app.get("/")
async def root():
    return {"message": "url-shortener"}
