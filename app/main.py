from fastapi import FastAPI
from app.api.routes import standings, health

app = FastAPI(title="League Standings Service")

app.include_router(health.router)
app.include_router(standings.router)
