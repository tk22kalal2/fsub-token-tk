# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, LOGGER
from helper_func import encode

X_CHANNEL = "-1002249946503"

@Client.on_message(
    filters.private
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
            chat_id=X_CHANNEL, disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(
            chat_id=X_CHANNEL, disable_notification=True
        )
    except Exception as e:
        LOGGER(__name__).warning(e)
        await reply_text.edit_text("Something went Wrong..!")
        return
    converted_id = post_message.id * abs(X_CHANNEL)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    user_id = message.from_user.id
    user = await get_user(user_id)
            # Get the bot's username
    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Video Link", url=f"{link}"
                )
            ]
        ]
    )

    await reply_text.edit(
        f"<b>Here is your link</b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass


@Client.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(X_CHANNEL)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    user_id = message.from_user.id
    user = await get_user(user_id)
            # Get the bot's username
    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Video Link", url=f"{link}"                    
                )
            ]
        ]
    )
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass
