from fastapi import FastAPI
from src.api.routes import pipeline, health

app = FastAPI(title="AI Intelligence Pipeline API")

# include routes
app.include_router(health.router)
app.include_router(pipeline.router)