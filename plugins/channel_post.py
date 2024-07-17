# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from TechVJ.bot import StreamBot

from config import ADMINS, CHANNEL_ID, LOGGER
from helper_func import encode


@StreamBot.on_message(
    filters.private
    & filters.user(ADMINS)
    & ~filters.command(
        [
            "start",
            "users",
            "broadcast",
            "ping",
            "uptime",
            "batch",
            "logs",
            "genlink",
            "delvar",
            "getvar",
            "setvar",
            "speedtest",
            "update",
            "stats",
            "vars",
            "id",
        ]
    )
)
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(
            chat_id=client.db_channel.id, disable_notification=True
        )
    except Exception as e:
        LOGGER(__name__).warning(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(client.db_channel)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    await reply_text.edit(
        f"<b>Here is your link</b>\n\n{link}",
        disable_web_page_preview=True,
    )

    


@StreamBot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    
