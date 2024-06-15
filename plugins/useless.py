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
from pyrogram.types import Message, ReplyKeyboardMarkup

buttonz = ReplyKeyboardMarkup(
    [
        ["CLONE"],
    ],
    resize_keyboard=True
)

@Bot.on_message(filters.command("clone") & filters.private & filters.incoming & filters.regex('CLONE'))
async def clone(client, message):
    await message.reply_text(script.CLONE_TXT, reply_markup=buttonz)


