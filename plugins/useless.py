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
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid


@Bot.on_message(filters.private & filters.incoming)
async def forward_to_admin(client: Bot, m: Message):
    try:
        for admin_chat_id in ADMINS:
            await client.send_message(chat_id=admin_chat_id, text=message.text)
    except PeerIdInvalid as e:
        LOGGER.error(f"PeerIdInvalid error: {e}")
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")

