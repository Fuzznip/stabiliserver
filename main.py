from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.dink_submission import router as stability_router
from routes.dink import router as dink_router
from routes.reload_drop_dictionary import router as drop_router

load_dotenv()

app = FastAPI()

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
app.include_router(drop_router)
