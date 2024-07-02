# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import re
from pyrogram import filters, Client, enums
from plugins.database import unpack_new_file_id
from clone_plugins.users_api import get_user, get_short_link
import base64

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMINS, CUSTOM_CAPTION, CD_CHANNEL
from clone_plugins.helper_func import encode
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
import asyncio


@Client.on_message(filters.private & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="Please forward or send the link of the first message for the batch.",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return

        if first_message.forward_from_message_id:
            f_msg_id = first_message.forward_from_message_id
        else:
            try:
                f_msg_id = int(re.search(r'/(\d+)', first_message.text).group(1))
            except:
                await first_message.reply("❌ Invalid input. Please forward a valid message or send a valid message link.", quote=True)
                continue
        break

    while True:
        try:
            second_message = await client.ask(
                text="Please forward or send the link of the last message for the batch.",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return

        if second_message.forward_from_message_id:
            s_msg_id = second_message.forward_from_message_id
        else:
            try:
                s_msg_id = int(re.search(r'/(\d+)', second_message.text).group(1))
            except:
                await second_message.reply("❌ Invalid input. Please forward a valid message or send a valid message link.", quote=True)
                continue
        break

    message_links = []
    for msg_id in range(min(f_msg_id, s_msg_id), max(f_msg_id, s_msg_id) + 1):
        try:
            base64_string = await encode(f"get-{msg_id * abs(-1002249946503)}")
            user_id = message.from_user.id
            user = await get_user(user_id)
            # Get the bot's username
            bot_username = (await client.get_me()).username
            link = f"https://t.me/{bot_username}?start={base64_string}"
            message_links.append(link)
        except Exception as e:
            await message.reply(f"Error generating link for message {msg_id}: {e}")

    for link in message_links:
        try:
            clean_caption = ""  # Default to empty if no custom caption
            await client.send_message(chat_id=message.from_user.id, text=f"{clean_caption}\n{link}")
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await client.send_message(chat_id=message.from_user.id, text=f"{clean_caption}\n{link}")
        except Exception as e:
            await message.reply(f"Error processing message {msg_id}: {e}")

    await message.reply("Batch processing completed.")


# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
