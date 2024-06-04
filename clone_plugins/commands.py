
# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import logging
import random
import asyncio
from validators import domain
from Script import script
from plugins.dbusers import db
from pyrogram import Client, filters, enums
from plugins.users_api import get_user, update_user_info
from plugins.database import get_file_details
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, InputMediaPhoto
from config import Var, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION, AUTO_DELETE_TIME, AUTO_DELETE, ADMINS
import re
import json
import base64
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

BATCH_FILES = {}

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
import re
import asyncio
from datetime import datetime
from time import time
from pymongo import MongoClient
from pyrogram import Client, filters
from bot import Bot
from config import DB_URI as MONGO_URL
from config import (
    ADMINS,
    CUSTOM_CAPTION,
    DISABLE_CHANNEL_BUTTON,
    FORCE_MSG,
    PROTECT_CONTENT,
    DB_NAME,
    START_MSG,
    API_ID,
    API_HASH,
)
#from database.sql import add_user, delete_user, full_userbase, query_msg
from database.mongo import collection, adds_user, del_user, fulls_userbase, present_user
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from helper_func import decode, get_messages, subsall, subsch, subsgc
from helper import b64_to_str, str_to_b64, get_current_time, shorten_url

from plugins.button import fsub_button, start_button

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def delete_after_delay(message: Message, delay):
    await asyncio.sleep(AUTO_DELETE_TIME)
    await message.delete()

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ0


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ')
            ],[
            InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/vj_botz')
            ],[
            InlineKeyboardButton('🤖 ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʟᴏɴᴇ ʙᴏᴛ', callback_data='clone')
            ],[
            InlineKeyboardButton('MARROW', callback_data='marrow')
            ],[
            InlineKeyboardButton('💁‍♀️ ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('😊 ᴀʙᴏᴜᴛ', callback_data='about')
            
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        me2 = (await client.get_me()).mention
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, me2),
            reply_markup=reply_markup
        )
        return

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except BaseException:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except BaseException:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except BaseException:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except BaseException:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()
        
        cloned_bot = mongo_collection.find_one({"user_id": message.from_user.id})
        cloned_bot_client = None
        if cloned_bot:
            cloned_bot_client = Client(
                f"{cloned_bot['bot_id']}_session",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=cloned_bot['token'],
            )
            await cloned_bot_client.start()

        for msg_list in messages:
            for msg in msg_list:
                if bool(CUSTOM_CAPTION) & bool(msg.document):
                    caption = CUSTOM_CAPTION.format(
                        previouscaption=msg.caption.html if msg.caption else "",
                        filename=msg.document.file_name,
                    )
                else:
                    caption = msg.caption.html if msg.caption else ""

                reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None

                try:
                    # Send message to the main bot user
                    X = await msg.copy(
                        chat_id=message.from_user.id,
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        protect_content=PROTECT_CONTENT,
                        reply_markup=reply_markup,
                    )
                    await X.forward(chat_id=cloned_bot['bot_id'])
                    await asyncio.sleep(0.5)
                    
                    # Send message to the cloned bot user if exists
                    if cloned_bot_client:
                        try:
                            await cloned_bot_client.copy_message(
                                chat_id=message.from_user.id,
                                from_chat_id=client.db_channel.id,
                                message_id=msg.id,
                                caption=caption,
                                parse_mode=ParseMode.HTML,
                                protect_content=PROTECT_CONTENT,
                                reply_markup=reply_markup,
                            )
                            await asyncio.sleep(0.5)
                        except ChannelInvalid:
                            await message.reply_text("Cloned bot does not have access to the specified channel.")

                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    try:
                        # Send message to the main bot user
                        X = await msg.copy(
                            chat_id=message.from_user.id,
                            caption=caption,
                            parse_mode=ParseMode.HTML,
                            protect_content=PROTECT_CONTENT,
                            reply_markup=reply_markup,
                        )
                        await X.forward(chat_id=cloned_bot['bot_id'])
                        await asyncio.sleep(0.5)
                        
                        # Send message to the cloned bot user if exists
                        if cloned_bot_client:
                            try:
                                await cloned_bot_client.copy_message(
                                    chat_id=message.from_user.id,
                                    from_chat_id=client.db_channel.id,
                                    message_id=msg.id,
                                    caption=caption,
                                    parse_mode=ParseMode.HTML,
                                    protect_content=PROTECT_CONTENT,
                                    reply_markup=reply_markup,
                                )
                                await asyncio.sleep(0.5)
                            except ChannelInvalid:
                                await message.reply_text("Cloned bot does not have access to the specified channel.")

                    except BaseException:
                        pass

        if cloned_bot_client:
            await cloned_bot_client.stop()
    else:
        out = start_button(client)
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f"@{message.from_user.username}" if message.from_user.username else None,
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=InlineKeyboardMarkup(out),
            disable_web_page_preview=True,
            quote=True,
        )
        
        return
                                           

@Client.on_message(filters.command('api') & filters.private)
async def shortener_api_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command

    if len(cmd) == 1:
        s = script.SHORTENER_API_MESSAGE.format(base_site=user["base_site"], shortener_api=user["shortener_api"])
        return await m.reply(s)

    elif len(cmd) == 2:    
        api = cmd[1].strip()
        await update_user_info(user_id, {"shortener_api": api})
        await m.reply("<b>Shortener API updated successfully to</b> " + api)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command("base_site") & filters.private)
async def base_site_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command
    text = f"`/base_site (base_site)`\n\n<b>Current base site: None\n\n EX:</b> `/base_site shortnerdomain.com`"
    if len(cmd) == 1:
        return await m.reply(text=text, disable_web_page_preview=True)
    elif len(cmd) == 2:
        base_site = cmd[1].strip()
        if not domain(base_site):
            return await m.reply(text=text, disable_web_page_preview=True)
        await update_user_info(user_id, {"base_site": base_site})
        await m.reply("<b>Base Site updated successfully</b>")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔒 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        me2 = (await client.get_me()).mention
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(me2),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ᴍʏ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ')
            ],[
            InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/vj_botz')
            ],[
            InlineKeyboardButton('🤖 ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ᴄʟᴏɴᴇ ʙᴏᴛ', callback_data='clone')
            ],[
            InlineKeyboardButton('💁‍♀️ ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('😊 ᴀʙᴏᴜᴛ', callback_data='about')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        me2 = (await client.get_me()).mention
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, me2),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    elif query.data == "clone":
        buttons = [[
            InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('🔒 Cʟᴏsᴇ', callback_data='close_data')
        ]]
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CLONE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "marrow":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomy")],
            [InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistry")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)
    elif query.data == "anatomy":
        anatomy_buttons = [
            [InlineKeyboardButton("HISTOLOGY", callback_data="histology")],
            [InlineKeyboardButton("UPPER LIMB", callback_data="upper_limb")],
            [InlineKeyboardButton("BACK TO MARROW MENU", callback_data="marrow")]
        ]
        reply_markup = InlineKeyboardMarkup(anatomy_buttons)
        await query.message.edit_reply_markup(reply_markup)
    elif query.data == "biochemistry":
        biochemistry_buttons = [
            [InlineKeyboardButton("AMINO ACIDS", callback_data="amino_acids")],
            [InlineKeyboardButton("PROTEINS", callback_data="proteins")],
            [InlineKeyboardButton("BACK TO MARROW MENU", callback_data="marrow")]
        ]
        reply_markup = InlineKeyboardMarkup(biochemistry_buttons)
        await query.message.edit_reply_markup(reply_markup)
    elif query.data == "histology":
        Bot_username = "testingclonepavo_bot"
        histology_message = (
            f"⏯: 27 skin and SYSTEM.mp4\n"
            f"https://t.me/{Bot_username}?start=Z2V0LTg4MzI4NDQ2ODg2ODE1MDU\n\n"
            f"⏯: 28 short topic on derma.mp4\n"
            f"https://t.me/{Bot_username}?start=Z2V0LTg4MzM4NDY3MTMwMzY0MzI"
        )
        await query.message.reply_text(histology_message)
    elif query.data == "upper_limb":
        # Handle upper limb button press if needed
        pass
    elif query.data == "amino_acids":
        # Handle amino acids button press if needed
        pass
    elif query.data == "proteins":
        # Handle proteins button press if needed
        pass

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    elif query.data == "help":
        buttons = [
            [
                InlineKeyboardButton('Hᴏᴍᴇ', callback_data='start'),
                InlineKeyboardButton('🔒 Cʟᴏsᴇ', callback_data='close_data')
            ]
        ]
        try:
            await client.edit_message_media(
                query.message.chat.id,
                query.message.id,
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=script.HELP_TXT,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"☣something went wrong\n\n{e}", show_alert=True)
            return

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

    

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
