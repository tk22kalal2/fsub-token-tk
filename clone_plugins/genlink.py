# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
import asyncio
from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import ADMINS, LOG_CHANNEL, BOT_USERNAME, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, LOGGER
from plugins.database import unpack_new_file_id
from plugins.users_api import get_user, get_short_link
from helper_func import encode

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def generate_share_link(bot_username, base64_string):
    return f"https://t.me/{bot_username}?start={base64_string}"

async def copy_message_and_generate_link(client, message):
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        LOGGER(__name__).warning(e)
        return None, "Something went wrong..!"

    converted_id = post_message.id * abs(client.db_channel.id)
    base64_string = await encode(f"get-{converted_id}")
    return post_message, base64_string

@Client.on_message(filters.command(['link']))
async def gen_link_s(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply('Reply to a message to get a shareable link.')
    
    if replied.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT]:
        return await message.reply("Reply to a supported media.")
    
    if message.has_protected_content:
        return await message.reply("Protected content is not supported.")
    
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    post_message, base64_string = await copy_message_and_generate_link(client, replied)
    
    if post_message is None:
        await reply_text.edit_text(base64_string)
        return
    
    user_id = message.from_user.id
    user = await get_user(user_id)
    bot_username = (await client.get_me()).username
    link = generate_share_link(bot_username, base64_string)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share Link", url=f"https://telegram.me/share/url?url={link}")]
    ])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass

@Client.on_message(filters.private & filters.user(ADMINS) & ~filters.command([
    "start", "users", "broadcast", "ping", "uptime", "batch", "logs", "genlink", 
    "delvar", "getvar", "setvar", "speedtest", "update", "stats", "vars", "id"
]))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    post_message, base64_string = await copy_message_and_generate_link(client, message)
    
    if post_message is None:
        await reply_text.edit_text(base64_string)
        return
    
    link = generate_share_link(client.username, base64_string)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share Link", url=f"https://telegram.me/share/url?url={link}")]
    ])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except Exception:
            pass

@Client.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    base64_string = await encode(f"get-{converted_id}")
    link = generate_share_link(client.username, base64_string)

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share Link", url=f"https://telegram.me/share/url?url={link}")]
    ])
    
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception:
        pass

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
