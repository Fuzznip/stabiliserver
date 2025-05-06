from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.dink_submission import router as stability_router
from routes.dink import router as dink_router
from routes.reload_drop_dictionary import router as item_router
import os
import logging
from routes.reload_drop_dictionary import populate_drop_dictionary
logging.basicConfig(level=logging.INFO)

load_dotenv()

async def lifespan(app: FastAPI):
    logging.info("Starting application lifespan...")
    await populate_drop_dictionary(os.environ.get("API"))
    yield  # This is where the application runs
    logging.info("Shutting down application lifespan...")

app = FastAPI(lifespan=lifespan)

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
