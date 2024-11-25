from app.logger import logger  # Import the logger
from fastapi import FastAPI
from app.routes import datasets, fine_tune, inference

# Initialize FastAPI app
app = FastAPI(title="LLM Platform", version="0.1.0")

# Include routes
app.include_router(datasets.router, prefix="/api")
app.include_router(fine_tune.router, prefix="/api")
app.include_router(inference.router, prefix="/api")

# Root endpoint for testing
@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the LLM Platform!"}

@app.get("/health", tags=["Health"], operation_id="health_status")
async def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event triggered.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown event triggered.")
