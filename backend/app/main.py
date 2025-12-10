"""main.py
FastAPI application entry point.
Roast My Profile - AI-powered profile picture roasting service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.config import settings
from app.routes.roast import router as roast_router
from app.workers.worker import worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    Startup: Start the worker
    Shutdown: Stop the worker
    """
    # Startup
    print("🚀 Starting Roast My Profile API")
    
    # Validate configuration
    try:
        settings.validate()
        print(f"✅ Configuration validated (Provider: {settings.AI_PROVIDER})")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        raise
    
    # Start worker
    worker.start()
    
    yield
    
    # Shutdown
    print("👋 Shutting down Roast My Profile API")
    worker.stop()


# Create FastAPI app
app = FastAPI(
    title="Roast My Profile API",
    description="AI-powered profile picture roasting service",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check."""
    return JSONResponse(content={
        "service": "Roast My Profile API",
        "status": "running",
        "version": "1.0.0",
        "provider": settings.AI_PROVIDER
    })


@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse(content={
        "status": "healthy",
        "worker": "running"
    })


# Include routers
app.include_router(roast_router)


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
