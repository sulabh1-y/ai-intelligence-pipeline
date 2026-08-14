from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.routes import pipeline, health

app = FastAPI(title="AI Intelligence Pipeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes (these are matched BEFORE the static mount)
app.include_router(health.router)
app.include_router(pipeline.router)

# Serve frontend static files at root — must be LAST
# html=True makes "/" serve index.html automatically
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")