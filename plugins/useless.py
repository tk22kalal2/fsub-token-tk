import os

from bot import Bot
from config import (
    ADMINS,
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    #DB_URI, sql database
    MONGO_URI,
    FORCE_MSG,
    FORCE_SUB_CHANNEL,
    FORCE_SUB_GROUP,
    LOGGER,
    PROTECT_CONTENT,
    START_MSG,
    TG_BOT_TOKEN,
)
from pyrogram import filters
from pyrogram.types import Message



@Bot.on_message(filters.private & filters.incoming)
async def forward_to_admin(event):
    # Check if the message is from a private chat
    if event.is_private:
        # Forward the user's message to the admin
        await client.send_message(ADMIN_ID, f"User ID: {event.sender_id}\nMessage: {event.raw_text}")

