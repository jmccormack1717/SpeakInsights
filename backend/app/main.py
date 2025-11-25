"""FastAPI application entry point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import query, datasets, schema

app = FastAPI(
    title="SpeakInsights API",
    description="Prompt-driven data analytics platform",
    version="1.0.0",
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(datasets.router, prefix="/api/v1", tags=["datasets"])
app.include_router(schema.router, prefix="/api/v1", tags=["schema"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "SpeakInsights API is running"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

