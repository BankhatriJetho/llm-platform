from app.logger import logger
from fastapi import FastAPI
from app.routes import routes, datasets, fine_tune, inference

# Initialize FastAPI app
app = FastAPI(title="LLM Platform", version="0.1.0")

# Include routes
app.include_router(routes.router)

# Include inference
app.include_router(inference.router)

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM Platform!"}

@app.get("/health", tags=["Health"], operation_id="health_status")
async def health_check():
    return {"status": "healthy"}

# Register routes
app.include_router(datasets.router, prefix="/api")
app.include_router(fine_tune.router, prefix="/api")
app.include_router(inference.router, prefix="/api")

# Add startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: Initializing resources.")
    # Add code here for initializing global resources, e.g., database connections
    # Example: await db.connect()

# Add shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown: Cleaning up resources.")
    # Add code here for cleanup, e.g., closing database connections
    # Example: await db.disconnect()
