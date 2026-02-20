from fastapi import APIRouter, BackgroundTasks, Form, File, UploadFile, Request
from utils.parse_dink_submission import parse_dink_request
import httpx

router = APIRouter()
import logging

logger = logging.getLogger(__name__)

@router.post("/stability")
async def handle_request(
    request: Request,
    background_tasks: BackgroundTasks,
    payload_json: str = Form(None),
    file: UploadFile = File(None)
):
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown")
    user_agent = request.headers.get("user-agent", "unknown")
    logger.info(f"POST /stability from ip={client_ip!r} user-agent={user_agent!r}")

    file_content = None
    filename = None

    if file:
        try:
            file_content = await file.read()
            filename = file.filename
        except Exception as e:
            logger.error(f"Error reading file content: {str(e)}")

    # Add processing tasks to background
    background_tasks.add_task(parse_dink_request, payload_json, file_content)

    return {}
