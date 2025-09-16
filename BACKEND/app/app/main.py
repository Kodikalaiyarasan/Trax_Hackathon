from fastapi import FastAPI
from .database import engine
from . import models
from .routes import schedule_routes, realtime_routes, ai_routes # type: ignore
from fastapi.middleware.cors import CORSMiddleware
import os

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Railway AI Optimization Engine (Prototype)")

# CORS (allow any for hackathon/demo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(schedule_routes.router)
app.include_router(realtime_routes.router)
app.include_router(ai_routes.router)

@app.get("/health")
def health():
    return {"status": "ok", "db": os.getenv("POSTGRES_HOST", "db")}
