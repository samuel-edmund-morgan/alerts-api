from fastapi import FastAPI
from app.routers import data

app = FastAPI()
app.include_router(data.router)

@app.get("/")
async def root():
    return {"message": "FastAPI with alerts.in.ua integration is running!"}