from fastapi import APIRouter
from utils.drop_dictionary import set_drop_dictionary

router = APIRouter()

@router.post("/items")
async def handle():
    ourDict = {
        ("Bones", "Gnome child"): [],
        ("Crystal shard", ""): []
    }

    set_drop_dictionary(ourDict)