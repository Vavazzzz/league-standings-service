from fastapi import FastAPI
from app.api.routes import health, data

app = FastAPI(title="League Standings Service")

app.include_router(health.router)
app.include_router(data.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)