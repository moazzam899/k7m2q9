
from fastapi import FastAPI

app = FastAPI(
    title="Wind Power Analytics API",
    description="Backend API for UK wind power forecast analysis",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Wind Power Analytics API is running!"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "success",
        "message": "Backend is healthy"
    }
