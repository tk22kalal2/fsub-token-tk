import os
from bot import Bot
import logging
from logging.handlers import RotatingFileHandler
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

LOG_FILE_NAME = "logs.txt"
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(LOG_FILE_NAME, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
# Set up logging
logging.basicConfig(level=logging.ERROR)  # You can set the desired log level

# Create a logger instance
LOGGER = logging.getLogger(__name__)

@Bot.on_message(filters.private & filters.incoming)
async def forward_to_admin(client: Bot, m: Message):
    try:
        for admin_chat_id in ADMINS:
            try:
                await m.forward(chat_id=admin_chat_id)
            except PeerIdInvalid as e:
                LOGGER.error(f"Error forwarding to admin_chat_id {admin_chat_id}: {e}")
            except Exception as e:
                LOGGER.error(f"An unexpected error occurred while forwarding to admin_chat_id {admin_chat_id}: {e}")
    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")


