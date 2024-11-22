from fastapi import FastAPI
from app.routes import routes
from app.routes import datasets, fine_tune, inference

# Initialize FastAPI app
app = FastAPI(title="LLM Platform", version="0.1.0")

# Include routes
app.include_router(routes.router)

# Root endpoint for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the LLM Platform!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Register routes
app.include_router(datasets.router, prefix="/api")
app.include_router(fine_tune.router, prefix="/api")
app.include_router(inference.router, prefix="/api")