from fastapi import FastAPI
from app.api.routes import health, data

app = FastAPI(title="League Standings Service")

app.include_router(health.router)
app.include_router(data.router)
