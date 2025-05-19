from fastapi import APIRouter, BackgroundTasks, Form, File, UploadFile
from utils.parse_dink_submission import parse_dink_request
import httpx

router = APIRouter()
import logging

logger = logging.getLogger(__name__)

async def forward_to_webhook(payload_json: str, file_content: bytes, filename: str = None):
    webhook_url = "https://discord.com/api/webhooks/1373903130588221562/5mvU_mdhlr-eW8RcRVjfaNaUlY0Gf-KbenDaEbbsFPor5MqoHwoSxX6PHADrqXb5LPVx"
    data = {"payload_json": payload_json}
    files = {"file": (filename, file_content)} if file_content and filename else None

    try:
        async with httpx.AsyncClient() as client:
            await client.post(webhook_url, data=data, files=files, timeout=60.0)
            logger.info("Successfully forwarded payload to Discord webhook")
    except Exception as e:
        logger.error(f"Error sending to webhook: {str(e)}")

@router.post("/stability")
async def handle_request(
    background_tasks: BackgroundTasks,
    payload_json: str = Form(None),
    file: UploadFile = File(None)
):
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
    background_tasks.add_task(forward_to_webhook, payload_json, file_content, filename)

    return {}
