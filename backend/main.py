# backend/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# Import routers (they will be created next)
try:
    from backend.routes.slots import router as slots_router
    from backend.routes.booking import router as booking_router
    from backend.routes.info import router as info_router
except Exception:
    # If route files are empty or not yet implemented, avoid import-time crash.
    slots_router = None
    booking_router = None
    info_router = None

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting Zenfru backend...")
    yield
    # Shutdown
    print("Shutting down Zenfru backend...")

app = FastAPI(
    title="Zenfru Voice Clinic Assistant - Backend",
    description="FastAPI backend for slot discovery & booking for the Zenfru voice assistant.",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow local testing origins (adjust for deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to specific origins in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": "Zenfru Voice Clinic Assistant Backend"}

# Include routers if available
if slots_router:
    app.include_router(slots_router, prefix="/slots", tags=["slots"])
if booking_router:
    app.include_router(booking_router, prefix="/booking", tags=["booking"])
if info_router:
    app.include_router(info_router, prefix="/info", tags=["info"])