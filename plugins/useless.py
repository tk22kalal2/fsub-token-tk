import os
from bot import Bot
import logging
from logging.handlers import RotatingFileHandler
from config import (
    ADMINS,
    OWNER_ID,
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


from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid

@Bot.on_message(filters.private & filters.incoming)
async def forward_to_admin_and_reply(client: Bot, m: Message):
    try:
        # Forward the incoming message to admins
        for admin_chat_id in ADMINS:
            try:
                forwarded_message = await m.forward(chat_id=admin_chat_id)
                
                # Wait for the admin's reply
                reply_message = await client.listen(filters.chat(forwarded_message.chat.id) & filters.reply)

                # Forward the admin's reply back to the user
                try:
                    await reply_message.forward(chat_id=m.chat.id)
                except PeerIdInvalid as e:
                    LOGGER.error(f"Error forwarding admin's reply to user: {e}")
                except Exception as e:
                    LOGGER.error(f"An unexpected error occurred while forwarding admin's reply to user: {e}")

            except PeerIdInvalid as e:
                LOGGER.error(f"Error forwarding to admin_chat_id {admin_chat_id}: {e}")
            except Exception as e:
                LOGGER.error(f"An unexpected error occurred while forwarding to admin_chat_id {admin_chat_id}: {e}")

    except Exception as e:
        LOGGER.error(f"An unexpected error occurred: {e}")

