
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import logging
import random
import asyncio
from Script import script
from validators import domain
from clone_plugins.dbusers import db
from clone_plugins.users_api import get_user, update_user_info
from pyrogram import Client, filters, enums
from plugins.database import get_file_details
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import BOT_USERNAME, ADMINS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery, InputMediaPhoto
from config import PICS, CUSTOM_FILE_CAPTION, AUTO_DELETE_TIME, AUTO_DELETE, PROTECT_CONTENT
import re
import json
import base64
from config import DB_URI as MONGO_URL
from pymongo import MongoClient

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]

logger = logging.getLogger(__name__)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
SECONDS = int(os.getenv("SECONDS", "30"))

async def schedule_deletion(msgs, delay):
    await asyncio.sleep(delay)
    for msg in msgs:
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

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

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('MARROW', callback_data='marrow')
        ]]
        me2 = (await client.get_me()).mention
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.CLONE_START_TXT.format(message.from_user.mention, me2),
            reply_markup=reply_markup
        )
        return

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
    
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""   

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                )
            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = '@VJ_Botz  ' + ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@'), file.file_name.split()))
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            k = await msg.reply(f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nThis Movie File/Video will be deleted in <b><u>{AUTO_DELETE} mins</u> 🫥 <i></b>(Due to Copyright Issues)</i>.\n\n<b><i>Please forward this File/Video to your Saved Messages and Start Download there</i></b>",quote=True)
            await asyncio.sleep(AUTO_DELETE_TIME)
            await msg.delete()
            await k.edit_text("<b>Your File/Video is successfully deleted!!!</b>")
            return
        except:
            pass
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

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
        await m.reply("Shortener API updated successfully to " + api)
    else:
        await m.reply("You are not authorized to use this command.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command("base_site") & filters.private)
async def base_site_handler(client, m: Message):
    user_id = m.from_user.id
    user = await get_user(user_id)
    cmd = m.command
    text = f"/base_site (base_site)\n\nCurrent base site: None\n\n EX: /base_site shortnerdomain.com"
    
    if len(cmd) == 1:
        return await m.reply(text=text, disable_web_page_preview=True)
    elif len(cmd) == 2:
        base_site = cmd[1].strip()
        if not domain(base_site):
            return await m.reply(text=text, disable_web_page_preview=True)
        await update_user_info(user_id, {"base_site": base_site})
        await m.reply("Base Site updated successfully")
    else:
        await m.reply("You are not authorized to use this command.")

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('MARROW', callback_data='marrow')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            chat_id=query.message.chat.id, 
            message_id=query.message.id, 
            media=InputMediaPhoto(random.choice(PICS))
        )
        me2 = (await client.get_me()).mention
        await query.message.edit_text(
            text=script.CLONE_START_TXT.format(query.from_user.mention, me2),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "marrow":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomy")],
            [InlineKeyboardButton("OPTHALMOLOGY", callback_data="opthalmology")],
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
        bot_username = "testingclonepavo_bot"
        histology_message = (
            f"⏯: 03. NEET PG 2021 atf.mp4\n"
            f"https://t.me/{bot_username}?start=Z2V0LTg5NjUxMTE5MDM1MzE4Njk\n\n"
            f"⏯: 04. NEET PG 2020 atf.mp4\n"
            f"https://t.me/{bot_username}?start=Z2V0LTg5NjYxMTM5Mjc4ODY3OTY\n\n"
            f"⏯: 01. INI CET May 2022 atf.mp4\n"
            f"https://t.me/{bot_username}?start=Z2V0LTg5NjcxMTU5NTIyNDE3MjM"
        )
        msg = await query.message.reply_text(histology_message, protect_content=PROTECT_CONTENT)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data == "upper_limb":
        # Handle upper limb button press if needed
        pass
    
    elif query.data == "amino_acids":
        # Handle amino acids button press if needed
        pass
    
    elif query.data == "proteins":
        # Handle proteins button press if needed
        pass

    
    elif query.data == "opthalmology":
        X = "testingclonepavo_bot"
        histology_message_template = (            
            f"1. How to Approach Orthopaedics Ed6 yw .mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMjY0Mzc4MjQ2NzUxMTY\n\n"
            
            f"2. Basics Histology and Physiology of Bones yw .mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMjc0Mzk4NDkwMzAwNDM\n\n"
            
            f"3. Basics Fracture and Healing yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMjg0NDE4NzMzODQ5NzA\n\n"
            
            f"4. Open Fracture Amputations and Polytrauma yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMjk0NDM4OTc3Mzk4OTc\n\n"
            
            f"5. Metabolic Bone Disease Part 1 yw .mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzA0NDU5MjIwOTQ4MjQ\n\n"
            
            f"6. Metabolic Bone Disease Part 2 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzE0NDc5NDY0NDk3NTE\n\n"
            
            f"7. Upper Limb Trauma Clavicle and Shoulder yw .mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzI0NDk5NzA4MDQ2Nzg\n\n"
            
            f"8. Upper Limb Trauma Arm and Elbow yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzM0NTE5OTUxNTk2MDU\n\n"
            
            f"9. Upper Limb Trauma Forearm Wrist Hand yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzQ0NTQwMTk1MTQ1MzI\n\n"
            
            f"10. Lower Limb Trauma Part 1 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzU0NTYwNDM4Njk0NTk\n\n"
            
            f"11. Lower Limb Trauma Part 2 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzY0NTgwNjgyMjQzODY\n\n"
            
            f"12. Sports Injuries yw .mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzc0NjAwOTI1NzkzMTM\n\n"
            
            f"13. Regional conditions (Cumulative Trauma disorders) yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzg0NjIxMTY5MzQyNDA\n\n"
            
            f"14. Nerve Injuries Fundamentals yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxMzk0NjQxNDEyODkxNjc\n\n"
            
            f"15. Nerve Injuries Part 1 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDA0NjYxNjU2NDQwOTQ\n\n"
            
            f"16. Nerve Injuries Part 2 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDE0NjgxODk5OTkwMjE\n\n"
            
            f"17. Bone tumors Part 1 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDI0NzAyMTQzNTM5NDg\n\n"
            
            f"18. Bone Tumors Part 2 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDM0NzIyMzg3MDg4NzU\n\n"
            
            f"19. Orthopaedics Infection Pyogenic yw. mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDQ0NzQyNjMwNjM4MDI\n\n"
            
            f"20. Orthopaedics Infection Tuberculosis yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDU0NzYyODc0MTg3Mjk\n\n"
            
            f"21. Paediatrics Orthopaedics Part 1yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDY0NzgzMTE3NzM2NTY\n\n"
            
            f"22. Paediatrics Orthopaedics Part 2 yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDc0ODAzMzYxMjg1ODM\n\n"
            
            f"23. Paediatrics Orthopaedics Part 3 yw .mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDg0ODIzNjA0ODM1MTA\n\n"
            
            f"24. Paediatrics Orthopaedics MCQs yw.mp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNDk0ODQzODQ4Mzg0Mzc\n\n"
            
            f"25. AVN and Osteochondritis. Ywmp4\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNTA0ODY0MDkxOTMzNjQ\n\n"
            
            f"26. Spine Part 1 yw\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNTE0ODg0MzM1NDgyOTE\n\n"
            
            f"27. Spine Part 2 yw\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNTI0OTA0NTc5MDMyMTg\n\n"
            
            f"28. Joint Disorders Part 1yw\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNTM0OTI0ODIyNTgxNDU\n\n"
            
            f"29. Joint Disorders Part yw\n"
            f"https://t.me/{{\"X\"}}?start=Z2V0LTkxNTQ0OTQ1MDY2MTMwNzI\n\n"
        )
        histology_message = histology_message_template.replace("{\"X\"}", X)
        msg = await query.message.reply_text(histology_message, protect_content=PROTECT_CONTENT)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    






# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01
