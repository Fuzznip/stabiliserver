from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.dink_submission import router as stability_router
from routes.dink import router as dink_router
from routes.reload_drop_dictionary import router as item_router
from routes.bot_submission import router as bot_router
import os
import traceback
import logging
from routes.reload_drop_dictionary import populate_drop_dictionary
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

async def lifespan(app: FastAPI):
    logging.info("Starting application lifespan...")
    await populate_drop_dictionary(os.environ.get("API"))
    yield  # This is where the application runs
    logging.info("Shutting down application lifespan...")

app = FastAPI(lifespan=lifespan)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full exception with stack trace
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    
    # Return a structured error response
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)},
    )

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stability_router)
app.include_router(dink_router)
app.include_router(item_router)
app.include_router(bot_router)
