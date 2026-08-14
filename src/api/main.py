from fastapi import FastAPI
from src.api.routes import pipeline, health

app = FastAPI(title="AI Intelligence Pipeline API")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# include routes
app.include_router(health.router)
app.include_router(pipeline.router)