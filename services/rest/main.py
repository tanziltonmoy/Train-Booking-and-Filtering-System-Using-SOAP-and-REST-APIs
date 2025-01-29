from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from services.rest.routes import router
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Train Booking REST API",
    description="API for searching trains and managing reservations.",
    version="1.0.0"
)

# Register routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Train Booking REST API"}

# Global Exception Handler
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Train Booking REST API...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
