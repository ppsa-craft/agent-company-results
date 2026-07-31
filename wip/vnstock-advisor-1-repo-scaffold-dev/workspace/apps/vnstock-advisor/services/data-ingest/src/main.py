from fastapi import FastAPI
from vnstock_shared.config import get_settings

settings = get_settings()

app = FastAPI(
    title="vnstock Data Ingest",
    description="Market data ingestion service",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "data-ingest",
        "version": "0.1.0",
    }


@app.get("/")
async def root():
    return {"message": "vnstock Data Ingest Service"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.data_ingest_port)