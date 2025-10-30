from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import importlib

app = FastAPI(
    title="Zenfru Voice Clinic Assistant - Backend",
    description="FastAPI backend for slot discovery & booking for the Zenfru voice assistant.",
    version="0.1.0",
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "service": "Zenfru Voice Clinic Assistant Backend"}


# --- Try imports dynamically ---
def try_import(module_name):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


# Try both local and deployed import paths
slots_router = (
    getattr(try_import("backend.routes.slots"), "router", None)
    or getattr(try_import("routes.slots"), "router", None)
)
booking_router = (
    getattr(try_import("backend.routes.booking"), "router", None)
    or getattr(try_import("routes.booking"), "router", None)
)
info_router = (
    getattr(try_import("backend.routes.info"), "router", None)
    or getattr(try_import("routes.info"), "router", None)
)


# Include routers
if slots_router:
    app.include_router(slots_router, prefix="/slots", tags=["slots"])
if booking_router:
    app.include_router(booking_router, prefix="/booking", tags=["booking"])
if info_router:
    app.include_router(info_router, prefix="/info", tags=["info"])


@app.on_event("startup")
async def startup_event():
    print("Starting Zenfru backend...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down Zenfru backend...")
