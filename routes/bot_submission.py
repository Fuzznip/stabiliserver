from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional, Union
import logging
from utils.request_handlers.pet_handler import submit_pet
from utils.request_handlers.kill_count_handler import submit_kill_count
from utils.request_handlers.parse_response import DiscordEmbedData
import json
import requests
from datetime import datetime
import os

router = APIRouter()

class DropSubmission(BaseModel):
    submission_type: str
    timestamp: str
    user: str
    discord_id: str
    item_name: str
    source: str
    quantity: int
    attachment_url: Optional[str] = None

class KillCountSubmission(BaseModel):
    submission_type: str
    timestamp: str
    user: str
    discord_id: str
    boss_name: str
    kill_count: int
    attachment_url: Optional[str] = None

class BotSubmissionResponse(BaseModel):
    message: str

async def process_drop_submission(submission: DropSubmission) -> None:
    """
    Process a drop submission from the Discord bot.
    
    Args:
        submission: The drop submission data
    """
    logging.info(f"Processing drop submission for {submission.user} ({submission.discord_id}): {submission.item_name} from {submission.source}")
    
    # Use the submit function from utils.submit to send this to the API
    # We're using "MANUAL" as the type since this is from manual submission through the bot
    from utils.submit import write
    
    notifications = write(
        player=submission.user,
        discordId=submission.discord_id,
        trigger=submission.item_name,
        source=submission.source,
        quantity=submission.quantity,
        totalValue=0,  # No value for manual submissions
        type="MANUAL"
    )
    
    # If we have notifications to send and an attachment URL, send webhook messages
    if notifications and submission.attachment_url:
        await send_webhook_notifications(notifications, submission.user, submission.item_name, submission.attachment_url)

async def process_kc_submission(submission: KillCountSubmission) -> None:
    """
    Process a kill count submission from the Discord bot.
    
    Args:
        submission: The kill count submission data
    """
    logging.info(f"Processing kill count submission for {submission.user} ({submission.discord_id}): {submission.boss_name} with KC {submission.kill_count}")
    
    # Use the dedicated kill count submission function
    notifications = submit_kill_count(
        rsn=submission.user,
        discordId=submission.discord_id,
        boss=submission.boss_name,
        count=submission.kill_count
    )
    
    # If we have notifications to send and an attachment URL, send webhook messages
    if notifications and submission.attachment_url:
        await send_webhook_notifications(notifications, submission.user, f"{submission.boss_name} Kill Count: {submission.kill_count}", submission.attachment_url)

async def send_webhook_notifications(notifications: list[tuple[str, DiscordEmbedData]], username: str, description_text: str, attachment_url: str) -> None:
    """
    Send webhook notifications with the given data.
    
    Args:
        notifications: List of (thread_id, embed_data) tuples
        username: The username to display in the embed
        description_text: The text to display in the description
        attachment_url: URL to the attachment image
    """
    for thread_id, notification in notifications:
        webhook_url = os.getenv("WEBHOOK_URL")
        if not webhook_url:
            logging.error("WEBHOOK_URL environment variable is not set.")
            return
        
        # Append thread ID as a query parameter
        url_with_thread = f"{webhook_url}?thread_id={thread_id}"
        
        # Construct the embed payload
        embed = {
            "title": "Manual Submission",
            "color": 0x992D22,  # Dark red
            "description": description_text,
            "author": {
                "name": username
            },
            "image": {
                "url": attachment_url
            }
        }
        
        payload = {
            "embeds": [embed]
        }
        
        # Send the POST request
        try:
            response = requests.post(
                url_with_thread,
                json=payload
            )
            
            if response.status_code not in [200, 204]:
                logging.error(f"Failed to send webhook to thread {thread_id}: {response.status_code} {response.text}")
        except Exception as e:
            logging.error(f"Error sending webhook: {e}")

@router.post("/bot", response_model=BotSubmissionResponse)
async def handle_bot_submission(background_tasks: BackgroundTasks, submission: Union[DropSubmission, KillCountSubmission]):
    """
    Handle submissions from the Discord bot, either drops or kill counts.
    
    Args:
        submission: Either a drop or kill count submission
        
    Returns:
        A success message
    """
    try:
        if submission.submission_type == "drop":
            drop_submission = DropSubmission(**submission.model_dump())
            background_tasks.add_task(process_drop_submission, drop_submission)
            return BotSubmissionResponse(message="Drop submission received and processed")
        
        elif submission.submission_type == "kc":
            kc_submission = KillCountSubmission(**submission.model_dump())
            background_tasks.add_task(process_kc_submission, kc_submission)
            return BotSubmissionResponse(message="Kill count submission received and processed")
        
        else:
            raise HTTPException(status_code=400, detail=f"Unknown submission_type: {submission.submission_type}")
    
    except Exception as e:
        logging.error(f"Error processing bot submission: {e}")
        raise HTTPException(status_code=500, detail=str(e))