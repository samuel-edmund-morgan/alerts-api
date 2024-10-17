from fastapi import FastAPI
from app.routers import token, data

app = FastAPI()
app.include_router(token.router)
app.include_router(data.router)

@app.get("/")
async def root():
    return {"message": "FastAPI is running"}
