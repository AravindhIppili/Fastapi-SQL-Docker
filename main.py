from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from init_config import startup_handler, shutdown_handler
from Routes.router import router as pizza_router

app = FastAPI(title="Pizzeria", version="V1")

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# Add event handlers for startup and shutdown procedures
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

@app.get("/")
async def healthcheck():
    return JSONResponse({"status": "Healthy!"}, status_code=200)

# Include the pizza_router with a prefix for API versioning
app.include_router(pizza_router, prefix="/api/v1")
