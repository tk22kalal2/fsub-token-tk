import os
from bot import Bot
from config import (
    ADMINS,
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    # DB_URI, sql database
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
async def forward_to_admin(client: Bot, m: Message):
    # Forward the message to ADMINS chat ID
    for admin_chat_id in ADMINS:
        await client.send_message(chat_id=admin_chat_id, text=m.text)

