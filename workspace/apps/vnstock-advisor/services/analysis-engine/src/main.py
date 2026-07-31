from fastapi import FastAPI
from vnstock_shared.config import get_settings

settings = get_settings()

app = FastAPI(
    title="vnstock Analysis Engine",
    description="Technical analysis and signal generation service",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "analysis-engine",
        "version": "0.1.0",
    }


@app.get("/")
async def root():
    return {"message": "vnstock Analysis Engine Service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.analysis_engine_port)