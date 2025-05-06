from fastapi import APIRouter, BackgroundTasks, Form, File, UploadFile
from utils.parse_dink_submission import parse_dink_request

router = APIRouter()

@router.post("/stability")
async def handle_request(
    background_tasks: BackgroundTasks,
    payload_json: str = Form(None),
    file: UploadFile = File(None)
):
    file_content = await file.read() if file else None  # Read file content if provided
    background_tasks.add_task(parse_dink_request, payload_json, file_content)

    return {}
