from fastapi import FastAPI
from app import routes

app = FastAPI()

app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "url-shortener"}
