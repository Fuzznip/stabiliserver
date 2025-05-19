from fastapi import APIRouter, BackgroundTasks, Form, File, UploadFile
from utils.parse_dink_submission import parse_dink_request
import httpx

router = APIRouter()

@router.post("/stability")
async def handle_request(
    background_tasks: BackgroundTasks,
    payload_json: str = Form(None),
    file: UploadFile = File(None)
):
    file_content = await file.read() if file else None  # Read file content if provided
    background_tasks.add_task(parse_dink_request, payload_json, file_content)

    # Forward the payload and file to: https://discord.com/api/webhooks/1373903130588221562/5mvU_mdhlr-eW8RcRVjfaNaUlY0Gf-KbenDaEbbsFPor5MqoHwoSxX6PHADrqXb5LPVx
    webhook_url = "https://discord.com/api/webhooks/1373903130588221562/5mvU_mdhlr-eW8RcRVjfaNaUlY0Gf-KbenDaEbbsFPor5MqoHwoSxX6PHADrqXb5LPVx"
    data = {"payload_json": payload_json}
    files = {"file": (file.filename, file_content)} if file and file_content else None

    async with httpx.AsyncClient() as client:
        await client.post(webhook_url, data=data, files=files)

    return {}
