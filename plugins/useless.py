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

@Bot.on_message(filters.private & filters.incoming)
async def show_clone_button(client, message):
    await message.reply("Choose an option:", reply_markup=buttonz)

@Bot.on_message(filters.private & filters.text & filters.regex('CLONE'))
async def clone(client, message):
    await message.reply("/clone")

# Starting the bot
Bot.run()
