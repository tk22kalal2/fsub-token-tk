
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

def paginate_links(links, page, per_page=20):
    start = page * per_page
    end = start + per_page
    return links[start:end], len(links) > end
    
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
            InlineKeyboardButton('MARROW', callback_data='marrow'),
            InlineKeyboardButton('PREPLADDER 5', callback_data='prepladder'),
            InlineKeyboardButton('DOCTUTORAL', callback_data='doctut')
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
            [InlineKeyboardButton("ANATOMY", callback_data="anatomy"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistry")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiology"), InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacology")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathology"), InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiology")],
            [InlineKeyboardButton("PSM", callback_data="psm"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="ophthalmology")],
            [InlineKeyboardButton("ENT", callback_data="ent"), InlineKeyboardButton("FMT", callback_data="fmt")],
            [InlineKeyboardButton("SURGERY", callback_data="surgery"), InlineKeyboardButton("MEDICINE", callback_data="medicine")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="dermatology"), InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatry")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesia"), InlineKeyboardButton("RADIOLOGY", callback_data="radiology")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedics"), InlineKeyboardButton("PEDIATRICS", callback_data="pediatrics")],
            [InlineKeyboardButton("OBGY", callback_data="obgy"), InlineKeyboardButton("RECENT UPDATES", callback_data="recentupdates")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)

    
    elif query.data.startswith("orthopedics"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. How to Approach Orthopaedics Ed6 yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjE1MDg2NzcwOTc1NjE)",
            "[<b>2. Basics Histology and Physiology of Bones yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjI1MTA3MDE0NTI0ODg)",
            "[<b>3. Basics Fracture and Healing yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjM1MTI3MjU4MDc0MTU)",
            "[<b>4. Open Fracture Amputations and Polytrauma yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjQ1MTQ3NTAxNjIzNDI)",
            "[<b>5. Metabolic Bone Disease Part 1 yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjU1MTY3NzQ1MTcyNjk)",
            "[<b>6. Metabolic Bone Disease Part 2 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjY1MTg3OTg4NzIxOTY)",
            "[<b>7. Upper Limb Trauma Clavicle and Shoulder yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjc1MjA4MjMyMjcxMjM)",
            "[<b>8. Upper Limb Trauma Arm and Elbow yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjg1MjI4NDc1ODIwNTA)",
            "[<b>9. Upper Limb Trauma Forearm Wrist Hand yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNjk1MjQ4NzE5MzY5Nzc)",
            "[<b>10. Lower Limb Trauma Part 1 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzA1MjY4OTYyOTE5MDQ)",
            "[<b>11. Lower Limb Trauma Part 2 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzE1Mjg5MjA2NDY4MzE)",
            "[<b>12. Sports Injuries yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzI1MzA5NDUwMDE3NTg)",
            "[<b>13. Regional conditions (Cumulative Trauma disorders) yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzM1MzI5NjkzNTY2ODU)",
            "[<b>14. Nerve Injuries Fundamentals yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzQ1MzQ5OTM3MTE2MTI)",
            "[<b>15. Nerve Injuries Part 1 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzU1MzcwMTgwNjY1Mzk)",
            "[<b>16. Nerve Injuries Part 2 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzY1MzkwNDI0MjE0NjY)",
            "[<b>17. Bone tumors Part 1 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzc1NDEwNjY3NzYzOTM)",
            "[<b>18. Bone Tumors Part 2 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzg1NDMwOTExMzEzMjA)",
            "[<b>19. Orthopaedics Infection Pyogenic yw. mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxNzk1NDUxMTU0ODYyNDc)",
            "[<b>20. Orthopaedics Infection Tuberculosis yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODA1NDcxMzk4NDExNzQ)",
            "[<b>21. Paediatrics Orthopaedics Part 1yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODE1NDkxNjQxOTYxMDE)",
            "[<b>22. Paediatrics Orthopaedics Part 2 yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODI1NTExODg1NTEwMjg)",
            "[<b>23. Paediatrics Orthopaedics Part 3 yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODM1NTMyMTI5MDU5NTU)",
            "[<b>24. Paediatrics Orthopaedics MCQs yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODQ1NTUyMzcyNjA4ODI)",
            "[<b>25. AVN and Osteochondritis. Ywmp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODU1NTcyNjE2MTU4MDk)",
            "[<b>26. Spine Part 1 yw</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODY1NTkyODU5NzA3MzY)",
            "[<b>27. Spine Part 2 yw</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODc1NjEzMTAzMjU2NjM)",
            "[<b>28. Joint Disorders Part 1yw</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODg1NjMzMzQ2ODA1OTA)",
            "[<b>29. Joint Disorders Part yw</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxODk1NjUzNTkwMzU1MTc)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        orthopedics_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"orthopedics_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"orthopedics_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(orthopedics_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("biochemistry"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01: How to approach Biochemistry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDc2ODI3NzE2MjEyODM)",
            "[<b>02: Biochemistry of Fed State</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDg2ODQ3OTU5NzYyMTA)",
            "[<b>03: Biochemistry of Fasting State</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDk2ODY4MjAzMzExMzc)",
            "[<b>04: Concept of Enzyme Regulation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTA2ODg4NDQ2ODYwNjQ)",
            "[<b>05: Introduction to Enzymes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTE2OTA4NjkwNDA5OTE)",
            "[<b>06: Classifications of Enzymes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTI2OTI4OTMzOTU5MTg)",
            "[<b>07: Mechanism of Action of Enzymes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTM2OTQ5MTc3NTA4NDU)",
            "[<b>08: Enzyme Kinetics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTQ2OTY5NDIxMDU3NzI)",
            "[<b>09: Enzyme Inhibition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTU2OTg5NjY0NjA2OTk)",
            "[<b>10: Enzyme Regulation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTY3MDA5OTA4MTU2MjY)",
            "[<b>11: Clinical Enzymology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTc3MDMwMTUxNzA1NTM)",
            "[<b>12: Chemistry of Carbohydrates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTg3MDUwMzk1MjU0ODA)",
            "[<b>13: Glycosaminoglycans & Mucopolysaccharides</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNTk3MDcwNjM4ODA0MDc)",
            "[<b>14: Glucose Transporters</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjA3MDkwODgyMzUzMzQ)",
            "[<b>15: Glycolysis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjE3MTExMTI1OTAyNjE)",
            "[<b>16: Applied aspects of Glycolysis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjI3MTMxMzY5NDUxODg)",
            "[<b>17: Pyruvate Dehydrogenase</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjM3MTUxNjEzMDAxMTU)",
            "[<b>18: Glycogen Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjQ3MTcxODU2NTUwNDI)",
            "[<b>19: Glycogen Storage Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjU3MTkyMTAwMDk5Njk)",
            "[<b>20: Gluconeogenesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjY3MjEyMzQzNjQ4OTY)",
            "[<b>21: Minor Metabolic Pathways</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjc3MjMyNTg3MTk4MjM)",
            "[<b>22: Chemistry of Lipids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjg3MjUyODMwNzQ3NTA)",
            "[<b>23: Sphingolipidoses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNjk3MjczMDc0Mjk2Nzc)",
            "[<b>24: Oxidation of Fatty Acid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzA3MjkzMzE3ODQ2MDQ)",
            "[<b>25: Ketone Bodies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzE3MzEzNTYxMzk1MzE)",
            "[<b>26: Fatty Acid Synthesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzI3MzMzODA0OTQ0NTg)",
            "[<b>27: Cholesterol & Bile Acid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzM3MzU0MDQ4NDkzODU)",
            "[<b>28: Lipoproteins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzQ3Mzc0MjkyMDQzMTI)",
            "[<b>29: Dyslipidemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzU3Mzk0NTM1NTkyMzk)",
            "[<b>30: Lipases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzY3NDE0Nzc5MTQxNjY)",
            "[<b>31: Chemistry of Amino Acids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzc3NDM1MDIyNjkwOTM)",
            "[<b>32: Fibrous Proteins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzg3NDU1MjY2MjQwMjA)",
            "[<b>33: General Amino Acid Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNzk3NDc1NTA5Nzg5NDc)",
            "[<b>34: Urea Cycle & its disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODA3NDk1NzUzMzM4NzQ)",
            "[<b>35: Aromatic Amino Acids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODE3NTE1OTk2ODg4MDE)",
            "[<b>36: Glycine & Serine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODI3NTM2MjQwNDM3Mjg)",
            "[<b>37: Sulphur containing Amino Acids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODM3NTU2NDgzOTg2NTU)",
            "[<b>38: Tryptophan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODQ3NTc2NzI3NTM1ODI)",
            "[<b>39: Branched-chain Amino Acids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODU3NTk2OTcxMDg1MDk)",
            "[<b>40: Acidic & Basic Amino Acids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODY3NjE3MjE0NjM0MzY)",
            "[<b>41: Miscellaneous Amino Acids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODc3NjM3NDU4MTgzNjM)",
            "[<b>42: Krebs Cycle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODg3NjU3NzAxNzMyOTA)",
            "[<b>43: Electron Transport Chain</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyODk3Njc3OTQ1MjgyMTc)",
            "[<b>44: Chemistry of Nucleotides</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTA3Njk4MTg4ODMxNDQ)",
            "[<b>45: Metabolism of Nucleotides</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTE3NzE4NDMyMzgwNzE)",
            "[<b>46: Structure & Organization of DNA</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTI3NzM4Njc1OTI5OTg)",
            "[<b>47: DNA Replication</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTM3NzU4OTE5NDc5MjU)",
            "[<b>48: Transcription</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTQ3Nzc5MTYzMDI4NTI)",
            "[<b>49: Translation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTU3Nzk5NDA2NTc3Nzk)",
            "[<b>50: Gene Expression</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTY3ODE5NjUwMTI3MDY)",
            "[<b>51: Hybridization Techniques</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTc3ODM5ODkzNjc2MzM)",
            "[<b>52: Recombinant DNA Technology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTg3ODYwMTM3MjI1NjA)",
            "[<b>53: Polymerase Chain Reaction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyOTk3ODgwMzgwNzc0ODc)",
            "[<b>54: DNA Sequencing</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDA3OTAwNjI0MzI0MTQ)",
            "[<b>55: Mutation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDE3OTIwODY3ODczNDE)",
            "[<b>56: Vitamin A</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDI3OTQxMTExNDIyNjg)",
            "[<b>57: Vitamin D, E & K</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDM3OTYxMzU0OTcxOTU)",
            "[<b>58: Hematopoietic Vitamins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDQ3OTgxNTk4NTIxMjI)",
            "[<b>59: Energy Releasing Vitamins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDU4MDAxODQyMDcwNDk)",
            "[<b>60: Vitamin B6 & Vitamin C</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDY4MDIyMDg1NjE5NzY)",
            "[<b>61: Heme Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDc4MDQyMzI5MTY5MDM)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        biochemistry_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"biochemistry_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"biochemistry_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(biochemistry_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data.startswith("anesthesia"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01.How to approach Anaesthesia Edition 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDg4MDYyNTcyNzE4MzA)",
            "[<b>02.Introduction and History</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMDk4MDgyODE2MjY3NTc)",
            "[<b>03.Pre-Anaesthetic Checkup: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTA4MTAzMDU5ODE2ODQ)",
            "[<b>04.Pre-Anaesthetic Checkup: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTE4MTIzMzAzMzY2MTE)",
            "[<b>05.Pre-op preparation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTI4MTQzNTQ2OTE1Mzg)",
            "[<b>06.Monitoring under Anaesthesia: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTM4MTYzNzkwNDY0NjU)",
            "[<b>07.Monitoring under Anaesthesia: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTQ4MTg0MDM0MDEzOTI)",
            "[<b>08.Boyle's Machine: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTU4MjA0Mjc3NTYzMTk)",
            "[<b>09.Boyle's Machine: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTY4MjI0NTIxMTEyNDY)",
            "[<b>10.Breathing systems</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTc4MjQ0NzY0NjYxNzM)",
            "[<b>11.Regional Anaesthesia: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTg4MjY1MDA4MjExMDA)",
            "[<b>12.Regional Anaesthesia: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMTk4Mjg1MjUxNzYwMjc)",
            "[<b>13.Epidural Anaesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjA4MzA1NDk1MzA5NTQ)",
            "[<b>14.Peripheral Nerve Blocks</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjE4MzI1NzM4ODU4ODE)",
            "[<b>15.Intravenous Anaesthetics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjI4MzQ1OTgyNDA4MDg)",
            "[<b>16.Inhalation Anaesthetics: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjM4MzY2MjI1OTU3MzU)",
            "[<b>17.Inhalation Anaesthetics: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjQ4Mzg2NDY5NTA2NjI)",
            "[<b>18.Local Anaesthetics: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjU4NDA2NzEzMDU1ODk)",
            "[<b>19.Local Anaesthetics: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjY4NDI2OTU2NjA1MTY)",
            "[<b>20.Muscle Relaxants: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjc4NDQ3MjAwMTU0NDM)",
            "[<b>21.Muscle Relaxants: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjg4NDY3NDQzNzAzNzA)",
            "[<b>22.Anaesthesia for Coexisting diseases Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMjk4NDg3Njg3MjUyOTc)",
            "[<b>23.Anaesthesia for Coexisting Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzA4NTA3OTMwODAyMjQ)",
            "[<b>24.Malignant Hyperthermia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzE4NTI4MTc0MzUxNTE)",
            "[<b>25.Day care Anaesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzI4NTQ4NDE3OTAwNzg)",
            "[<b>26.Airway Management</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzM4NTY4NjYxNDUwMDU)",
            "[<b>27.Anaesthesia Equipment</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzQ4NTg4OTA0OTk5MzI)",
            "[<b>28.How to approach a patient in ICU</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzU4NjA5MTQ4NTQ4NTk)",
            "[<b>29.Oxygen therapy in ICU</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzY4NjI5MzkyMDk3ODY)",
            "[<b>30.Mechanical Ventilation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzc4NjQ5NjM1NjQ3MTM)",
            "[<b>31.CPR</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzg4NjY5ODc5MTk2NDA)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anesthesia_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anesthesia_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anesthesia_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anesthesia_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
    
    elif query.data.startswith("ophthalmology"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.How to approach Ophthalmology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzMzk4NjkwMTIyNzQ1Njc)",	
            "[<b>2. Anatomy of eye , layers, str. of eyeball and anatomy of cornea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDA4NzEwMzY2Mjk0OTQ)",	
            "[<b>3. Anatomy of eye - sclera and it's pathologies, Limbus and Ocular routes of drug administration</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDE4NzMwNjA5ODQ0MjE)",	
            "[<b>4. Anatomy of eye - Middle layer of eyeball , Horner Syndrome and Accommodation with it's anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDI4NzUwODUzMzkzNDg)",	
            "[<b>5. Anatomy of eye - Innermost layer , Blood Supply of Eye and Embryology of Eye</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDM4NzcxMDk2OTQyNzU)",	
            "[<b>6. Neuro-Ophtha - Visual pathway and Visual field defects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDQ4NzkxMzQwNDkyMDI)",	
            "[<b>7. Neuro-Ophtha - Pupillary Reflexes , Light reflex pathway and it's lesions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDU4ODExNTg0MDQxMjk)",	
            "[<b>8. Neuro-Ophtha - Optic atrophy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDY4ODMxODI3NTkwNTY)",	
            "[<b>9. Neuro-Ophtha - Colour blindness and Congenital anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDc4ODUyMDcxMTM5ODM)",	
            "[<b>10. Squint</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDg4ODcyMzE0Njg5MTA)",	
            "[<b>11. Squint Investigation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNDk4ODkyNTU4MjM4Mzc)",	
            "[<b>12. Paralytic Squint</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTA4OTEyODAxNzg3NjQ)",	
            "[<b>13. Squint Types</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTE4OTMzMDQ1MzM2OTE)",	
            "[<b>14. Lens Anatomy and Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTI4OTUzMjg4ODg2MTg)",	
            "[<b>15. Lens - Acquired cataract</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTM4OTczNTMyNDM1NDU)",	
            "[<b>16. Lens - Cataract surgery and it's complications</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTQ4OTkzNzc1OTg0NzI)",	
            "[<b>17. Lens - Congenital cataract , Ectopia lentis and</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTU5MDE0MDE5NTMzOTk)",	
            "[<b>18. Glaucoma Investigations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTY5MDM0MjYzMDgzMjY)",	
            "[<b>19. Glaucoma Investigations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTc5MDU0NTA2NjMyNTM)",	
            "[<b>20. Glaucoma - Open Angle and Angle closure</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTg5MDc0NzUwMTgxODA)",	
            "[<b>21. Glaucoma - Secondary glaucoma and Congenital glaucoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNTk5MDk0OTkzNzMxMDc)",	
            "[<b>22. Optics - Test for Vision and Normal optics of the eye</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjA5MTE1MjM3MjgwMzQ)",	
            "[<b>23. Optics - Myopia and Hypermetropia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjE5MTM1NDgwODI5NjE)",	
            "[<b>24. Optics - Astigmatism, Tests for refraction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjI5MTU1NzI0Mzc4ODg)",	
            "[<b>25. Retina - Anatomy and Investigation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjM5MTc1OTY3OTI4MTU)",	
            "[<b>26. RETINA - Retinoblastoma and Macular edema</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjQ5MTk2MjExNDc3NDI)",	
            "[<b>27. Retina - Dystrophies and fundus ( Retinitis Pigmentosa etc )</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjU5MjE2NDU1MDI2Njk)",	
            "[<b>28. RETINA - Vascular disorders - Part 1 - Diabetic retinopathy and Vitreous hmg</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjY5MjM2Njk4NTc1OTY)",	
            "[<b>29. RETINA - Vascular Disease Part 2 - HTN Retinopathy, CRAO , CRVO and ROP</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjc5MjU2OTQyMTI1MjM)",	
            "[<b>30. RETINAL DETACHMENT</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjg5Mjc3MTg1Njc0NTA)",	
            "[<b>31. CORNEA - Special Investigation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNjk5Mjk3NDI5MjIzNzc)",	
            "[<b>32 Corneal Ulcers</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzA5MzE3NjcyNzczMDQ)",	
            "[<b>33. Corneal dystrophies, Keratoconus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzE5MzM3OTE2MzIyMzE)",	
            "[<b>34 Uvea - Anterior Uveitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzI5MzU4MTU5ODcxNTg)",	
            "[<b>35 - Uvea Intermediate, Pan uveitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzM5Mzc4NDAzNDIwODU)",	
            "[<b>36. Conjuctiva - Anatomy and It's type</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzQ5Mzk4NjQ2OTcwMTI)",	
            "[<b>37. Eyelid - Anatomy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzU5NDE4ODkwNTE5Mzk)",	
            "[<b>38. ORBIT</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzY5NDM5MTM0MDY4NjY)",	
            "[<b>39. Ocular Trauma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzc5NDU5Mzc3NjE3OTM)",	
            "[<b>40. Lacrimal apparatus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzg5NDc5NjIxMTY3MjA)",	
            "[<b>41. Community Ophthalmology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzNzk5NDk5ODY0NzE2NDc)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        ophthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ophthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ophthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ophthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("fmt"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01: How to approach Forensic Medicine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODA5NTIwMTA4MjY1NzQ)",
            "[<b>02: Indian Legal System - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODE5NTQwMzUxODE1MDE)",
            "[<b>03: Indian Legal System - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODI5NTYwNTk1MzY0Mjg)",
            "[<b>04: Medical Law & Ethics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODM5NTgwODM4OTEzNTU)",
            "[<b>05: Medical Negligence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODQ5NjAxMDgyNDYyODI)",
            "[<b>06: Consent in Medical Practice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODU5NjIxMzI2MDEyMDk)",
            "[<b>07: Mechanical Injuries - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODY5NjQxNTY5NTYxMzY)",
            "[<b>08: Mechanical Injuries - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODc5NjYxODEzMTEwNjM)",
            "[<b>09: Regional Injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODg5NjgyMDU2NjU5OTA)",
            "[<b>10: Thermal Injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzODk5NzAyMzAwMjA5MTc)",
            "[<b>11: Proximal Ballistics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTA5NzIyNTQzNzU4NDQ)",
            "[<b>12: Intermediate & Terminal Ballistics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTE5NzQyNzg3MzA3NzE)",
            "[<b>13: Electrical Injuries, Explosion Injuries & Torture methods</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTI5NzYzMDMwODU2OTg)",
            "[<b>14: Transportation Injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTM5NzgzMjc0NDA2MjU)",
            "[<b>15: Autopsy Procedures</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTQ5ODAzNTE3OTU1NTI)",
            "[<b>16: Early Postmortem changes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTU5ODIzNzYxNTA0Nzk)",
            "[<b>17: Late Postmortem changes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTY5ODQ0MDA1MDU0MDY)",
            "[<b>18: Asphyxial Deaths - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTc5ODY0MjQ4NjAzMzM)",
            "[<b>19: Asphyxial Deaths - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTg5ODg0NDkyMTUyNjA)",
            "[<b>20: Human Identification - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkzOTk5OTA0NzM1NzAxODc)",
            "[<b>21: Human Identification - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDA5OTI0OTc5MjUxMTQ)",
            "[<b>22: Human Identification - Part 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDE5OTQ1MjIyODAwNDE)",
            "[<b>23: Impotence, Virginity, Delivery & Abortion</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDI5OTY1NDY2MzQ5Njg)",
            "[<b>24: Infant Deaths & Child Abuse</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDM5OTg1NzA5ODk4OTU)",
            "[<b>25: Sexual Offences</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDUwMDA1OTUzNDQ4MjI)",
            "[<b>26: General Toxicology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDYwMDI2MTk2OTk3NDk)",
            "[<b>27: Duties of a Doctor in a Case of Poisoning</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDcwMDQ2NDQwNTQ2NzY)",
            "[<b>28: Corrosive Poisons</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDgwMDY2Njg0MDk2MDM)",
            "[<b>29: Metallic & Non-Metallic Irritants</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MDkwMDg2OTI3NjQ1MzA)",
            "[<b>30: Animal & Plant Irritants</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTAwMTA3MTcxMTk0NTc)",
            "[<b>31: Neurotoxic Poisons [Deliriants]</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTEwMTI3NDE0NzQzODQ)",
            "[<b>32: Neurotoxic Poisons [Inebriants]</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTIwMTQ3NjU4MjkzMTE)",
            "[<b>33: Neurotoxic Poisons [Somniferous & Spinal Poisons]</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTMwMTY3OTAxODQyMzg)",
            "[<b>34: Asphyxiants & Cardiac Poisons</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTQwMTg4MTQ1MzkxNjU)",
            "[<b>35: Agricultural Poisons</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTUwMjA4Mzg4OTQwOTI)",
            "[<b>36: Forensic Psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTYwMjI4NjMyNDkwMTk)",
            "[<b>37: Trace Evidence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTcwMjQ4ODc2MDM5NDY)",
            "[<b>38: Acts & Legal sections of Importance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTgwMjY5MTE5NTg4NzM)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        fmt_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"fmt_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"fmt_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(fmt_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("dermatology"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1 intro to derma.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MTkwMjg5MzYzMTM4MDA)",
            "[<b>2 basi dermat part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjAwMzA5NjA2Njg3Mjc)",
            "[<b>3 basic of dermat.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjEwMzI5ODUwMjM2NTQ)",
            "[<b>4 papulo squ dsz part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjIwMzUwMDkzNzg1ODE)",
            "[<b>5 pappulo squamous dsz.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjMwMzcwMzM3MzM1MDg)",
            "[<b>6 appengdage disored part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjQwMzkwNTgwODg0MzU)",
            "[<b>7 appendage diso 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjUwNDEwODI0NDMzNjI)",
            "[<b>8 appendage and disorder part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjYwNDMxMDY3OTgyODk)",
            "[<b>9 bullous dsz part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjcwNDUxMzExNTMyMTY)",
            "[<b>10 bullous dsz.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjgwNDcxNTU1MDgxNDM)",
            "[<b>11 bacterial infection skin.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MjkwNDkxNzk4NjMwNzA)",
            "[<b>12 mycobacterial infection.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzAwNTEyMDQyMTc5OTc)",
            "[<b>13 viral infection.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzEwNTMyMjg1NzI5MjQ)",
            "[<b>15 parasitic inf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzIwNTUyNTI5Mjc4NTE)",
            "[<b>16 hansen dsz.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzMwNTcyNzcyODI3Nzg)",
            "[<b>17 HANSEN DSZ.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzQwNTkzMDE2Mzc3MDU)",
            "[<b>18 STD 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzUwNjEzMjU5OTI2MzI)",
            "[<b>19 STD 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzYwNjMzNTAzNDc1NTk)",
            "[<b>20 std 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzcwNjUzNzQ3MDI0ODY)",
            "[<b>21 GENODERMATOME.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzgwNjczOTkwNTc0MTM)",
            "[<b>22 ECZEMA.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0MzkwNjk0MjM0MTIzNDA)",
            "[<b>23 HISTAMINE RELATED DSZ.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDAwNzE0NDc3NjcyNjc)",
            "[<b>24 PIGMENTARY DSZ.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDEwNzM0NzIxMjIxOTQ)",
            "[<b>25 CUTANEOUS DRUG RXN.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDIwNzU0OTY0NzcxMjE)",
            "[<b>26 skin in rheumat.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDMwNzc1MjA4MzIwNDg)",
            "[<b>27 skin aND SYSTEM.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDQwNzk1NDUxODY5NzU)",
            "[<b>28 short topic on derna.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDUwODE1Njk1NDE5MDI)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        dermatology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"dermatology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"dermatology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(dermatology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psychiatry"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. How to approach psychiatry edition 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDYwODM1OTM4OTY4Mjk)",
            "[<b>2. Introduction to psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDcwODU2MTgyNTE3NTY)",
            "[<b>3. Psychopathology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDgwODc2NDI2MDY2ODM)",
            "[<b>4. Psychotic disorders part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NDkwODk2NjY5NjE2MTA)",
            "[<b>5. Psychotic disorders part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTAwOTE2OTEzMTY1Mzc)",
            "[<b>6. Depressive disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTEwOTM3MTU2NzE0NjQ)",
            "[<b>7. Bipolar disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTIwOTU3NDAwMjYzOTE)",
            "[<b>8. Stress , Trauma and related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTMwOTc3NjQzODEzMTg)",
            "[<b>9. Anxiety disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTQwOTk3ODg3MzYyNDU)",
            "[<b>10. Obsessive compulsive and related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTUxMDE4MTMwOTExNzI)",
            "[<b>11. Somatization , Dissociation related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTYxMDM4Mzc0NDYwOTk)",
            "[<b>12. Neurocognitive disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTcxMDU4NjE4MDEwMjY)",
            "[<b>13. Eating Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTgxMDc4ODYxNTU5NTM)",
            "[<b>14. Sex , Gender and related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NTkxMDk5MTA1MTA4ODA)",
            "[<b>15. Sleep and related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjAxMTE5MzQ4NjU4MDc)",
            "[<b>16. Personality and related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjExMTM5NTkyMjA3MzQ)",
            "[<b>17. Substance use and other addictive disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjIxMTU5ODM1NzU2NjE)",
            "[<b>18. Child , adolescent and related disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjMxMTgwMDc5MzA1ODg)",
            "[<b>19. Emergency psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjQxMjAwMzIyODU1MTU)",
            "[<b>20. Psychopharmacology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjUxMjIwNTY2NDA0NDI)",
            "[<b>21. Somatic treatments in psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjYxMjQwODA5OTUzNjk)",
            "[<b>22. Psychology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjcxMjYxMDUzNTAyOTY)",
            "[<b>23. Psychological therapies and assessments</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjgxMjgxMjk3MDUyMjM)",
            "[<b>24. Public health and Legal aspects related to Mental Health</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NjkxMzAxNTQwNjAxNTA)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psychiatry_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psychiatry_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psychiatry_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psychiatry_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("ent"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. How to prepare ENT using Ed6.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzAxMzIxNzg0MTUwNzc)",
            "[<b>2. Basics of Ear yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzExMzQyMDI3NzAwMDQ)",
            "[<b>3. Clinical Embryology of Inner Ear yw .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzIxMzYyMjcxMjQ5MzE)",
            "[<b>4. Clinical Embryology of External and Middle Ear yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzMxMzgyNTE0Nzk4NTg)",
            "[<b>5. Clinical Anatomy of External Ear yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzQxNDAyNzU4MzQ3ODU)",
            "[<b>6. Clinical Anatomy of Middle Ear 1 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzUxNDIzMDAxODk3MTI)",
            "[<b>7. Clinical anatomy of Middle Ear 2 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzYxNDQzMjQ1NDQ2Mzk)",
            "[<b>8. Clinical Anatomy of Inner Ear Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzcxNDYzNDg4OTk1NjY)",
            "[<b>9. Nerve Supply of Ear Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzgxNDgzNzMyNTQ0OTM)",
            "[<b>10. Audiology and Evaluation Tuning Fork Tests Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0NzkxNTAzOTc2MDk0MjA)",
            "[<b>11. Audiology and Evaluation Audiogram (PTA) Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODAxNTI0MjE5NjQzNDc)",
            "[<b>12. Audiology Part 3  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODExNTQ0NDYzMTkyNzQ)",
            "[<b>13. Audiology Part 4 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODIxNTY0NzA2NzQyMDE)",
            "[<b>14. Vestibular Physiology  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODMxNTg0OTUwMjkxMjg)",
            "[<b>15. Approach to vertigo and Vestibular function test  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODQxNjA1MTkzODQwNTU)",
            "[<b>16. Diseases of Pinna Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODUxNjI1NDM3Mzg5ODI)",
            "[<b>17. Diseases of External Auditory Canal  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODYxNjQ1NjgwOTM5MDk)",
            "[<b>18. Conditions of Tympanic Membrane  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODcxNjY1OTI0NDg4MzY)",
            "[<b>19. Acute otitis Media Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODgxNjg2MTY4MDM3NjM)",
            "[<b>20. Serous otitis Media  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0ODkxNzA2NDExNTg2OTA)",
            "[<b>21. cmom Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTAxNzI2NjU1MTM2MTc)",
            "[<b>22. Chronic squamous otitis Media  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTExNzQ2ODk4Njg1NDQ)",
            "[<b>23. Complications of otitis Media  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTIxNzY3MTQyMjM0NzE)",
            "[<b>24. Otosclerosis Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTMxNzg3Mzg1NzgzOTg)",
            "[<b>25. Menier's Disease Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTQxODA3NjI5MzMzMjU)",
            "[<b>26. Superior Semicircular Canal Dehiscence  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTUxODI3ODcyODgyNTI)",
            "[<b>27. BPPV Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTYxODQ4MTE2NDMxNzk)",
            "[<b>28. Vestibular Neuritis .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTcxODY4MzU5OTgxMDY)",
            "[<b>29. Sudden SNHL.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTgxODg4NjAzNTMwMzM)",
            "[<b>30. Tumors of External and Middle Ear .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk0OTkxOTA4ODQ3MDc5NjA)",
            "[<b>31. Acoustic Neuroma.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDAxOTI5MDkwNjI4ODc)",
            "[<b>32. Facial Nerve 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDExOTQ5MzM0MTc4MTQ)",
            "[<b>33. Facial Nerve 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDIxOTY5NTc3NzI3NDE)",
            "[<b>34. Hearing Rehabilitation.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDMxOTg5ODIxMjc2Njg)",
            "[<b>35. Clinical Anatomy of External Nose and Choanal atresia.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDQyMDEwMDY0ODI1OTU)",
            "[<b>36. Clinical anatomy of Lateral wall of Nose.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDUyMDMwMzA4Mzc1MjI)",
            "[<b>37. Clinical Anatomy and diseases of septum.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDYyMDUwNTUxOTI0NDk)",
            "[<b>38.Nerve Supply of Nose and its diseases 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDcyMDcwNzk1NDczNzY)",
            "[<b>39. Nerve Supply of Nose and its diseases 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDgyMDkxMDM5MDIzMDM)",
            "[<b>40. Arterial supply of Nose and Epistaxis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MDkyMTExMjgyNTcyMzA)",
            "[<b>41. Clinical Anatomy of PNS and Rhinosinusitis Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTAyMTMxNTI2MTIxNTc)",
            "[<b>42. Complications of Sinusitis Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTEyMTUxNzY5NjcwODQ)",
            "[<b>43. Nasal Polyps Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTIyMTcyMDEzMjIwMTE)",
            "[<b>44. Fungal Sinusitis Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTMyMTkyMjU2NzY5Mzg)",
            "[<b>45. Atrophic Rhinitis and Granulomatous Conditions of Nose Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTQyMjEyNTAwMzE4NjU)",
            "[<b>46. Fracture of Face and CSF Rhinorrhea Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTUyMjMyNzQzODY3OTI)",
            "[<b>47. Tumors of Nose and PNS  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTYyMjUyOTg3NDE3MTk)",
            "[<b>48. Clinical Anatomy of Pharynx 1 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTcyMjczMjMwOTY2NDY)",
            "[<b>49. Clinical Anatomy of Pharynx 2 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTgyMjkzNDc0NTE1NzM)",
            "[<b>50. Clinical Anatomy of Pharynx 3 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MTkyMzEzNzE4MDY1MDA)",
            "[<b>51. Clinical Anatomy of Pharynx 4 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjAyMzMzOTYxNjE0Mjc)",
            "[<b>52. Adenoid Hypertrophy Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjEyMzU0MjA1MTYzNTQ)",
            "[<b>53. Angiofibroma Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjIyMzc0NDQ4NzEyODE)",
            "[<b>54. Tracheostomy and Foreign body in airway  Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjMyMzk0NjkyMjYyMDg)",
            "[<b>54. NASOPHARYNGEAL CARCINOMA Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjQyNDE0OTM1ODExMzU)",
            "[<b>55. CONDITION OF TONSIL AND TONSILLECTOMY Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjUyNDM1MTc5MzYwNjI)",
            "[<b>56. CONDITION OF TONSIL PART 2 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjYyNDU1NDIyOTA5ODk)",
            "[<b>57. CLINICAL ANATOMY LARYGNX PART 1 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjcyNDc1NjY2NDU5MTY)",
            "[<b>58. CLINICAL ANATOMY LARNY PART 2 Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjgyNDk1OTEwMDA4NDM)",
            "[<b>59. LARYNX INFECTION Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MjkyNTE2MTUzNTU3NzA)",
            "[<b>60 Yw. congenital larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MzAyNTM2Mzk3MTA2OTc)",
            "[<b>61. VOICE DISORDER Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MzEyNTU2NjQwNjU2MjQ)",
            "[<b>62. NERVE SUPPLY VOCAL CPRD AND PALSY Yw.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MzIyNTc2ODg0MjA1NTE)",
            "[<b>63 Yw. carcinoma larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk1MzMyNTk3MTI3NzU0Nzg)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        ent_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ent_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ent_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ent_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("radiology"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01.Introduction to Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MTY0Mjc3MzQyMzQ0MTk)",
            "[<b>02.X-ray Fundamentals</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MTc0Mjk3NTg1ODkzNDY)",
            "[<b>03.X-ray Production and Interactions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MTg0MzE3ODI5NDQyNzM)",
            "[<b>04.CT basics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MTk0MzM4MDcyOTkyMDA)",
            "[<b>05.USG basics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjA0MzU4MzE2NTQxMjc)",
            "[<b>06.MRI basics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjE0Mzc4NTYwMDkwNTQ)",
            "[<b>07.Contrast Media</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjI0Mzk4ODAzNjM5ODE)",
            "[<b>08.USG interpretation module</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjM0NDE5MDQ3MTg5MDg)",
            "[<b>09.CT interpretation module</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjQ0NDM5MjkwNzM4MzU)",
            "[<b>10.CXR basics: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjU0NDU5NTM0Mjg3NjI)",
            "[<b>11.CXR basics: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MjY0NDc5Nzc3ODM2ODk)",
            "[<b>12.Pleural abnormalities and Lobar collapse</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Mjc0NTAwMDIxMzg2MTY)",
            "[<b>13.Silhouette sign and Lung infections:Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Mjg0NTIwMjY0OTM1NDM)",
            "[<b>14.Silhouette sign and Lung infections: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Mjk0NTQwNTA4NDg0NzA)",
            "[<b>15.Mediastinum: Lung tumors and Miscellaneous</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzA0NTYwNzUyMDMzOTc)",
            "[<b>16.Congenital heart disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzE0NTgwOTk1NTgzMjQ)",
            "[<b>17.Acquired heart disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzI0NjAxMjM5MTMyNTE)",
            "[<b>18.CNS: Stroke imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzM0NjIxNDgyNjgxNzg)",
            "[<b>19.CNS: Trauma imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzQ0NjQxNzI2MjMxMDU)",
            "[<b>20.CNS: Tumor imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzU0NjYxOTY5NzgwMzI)",
            "[<b>21.CNS: Infections and Miscellaneous</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2MzY0NjgyMjEzMzI5NTk)",
            "[<b>22.MRI: Blood appearance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Mzc0NzAyNDU2ODc4ODY)",
            "[<b>23.GUT: Conventional procedures</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Mzg0NzIyNzAwNDI4MTM)",
            "[<b>24.GUT imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Mzk0NzQyOTQzOTc3NDA)",
            "[<b>25.Renal papillary necrosis: Animation module</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDA0NzYzMTg3NTI2Njc)",
            "[<b>26.GIT: Conventional procedures</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDE0NzgzNDMxMDc1OTQ)",
            "[<b>27.GIT imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDI0ODAzNjc0NjI1MjE)",
            "[<b>28.Hydatid cyst: Animation module</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDM0ODIzOTE4MTc0NDg)",
            "[<b>29 . Hepatobiliary and Pancreatic imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDQ0ODQ0MTYxNzIzNzU)",
            "[<b>30.Radionuclide imaging basics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDU0ODY0NDA1MjczMDI)",
            "[<b>31. PET scan: Animation module</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDY0ODg0NjQ4ODIyMjk)",
            "[<b>32.Systemic Radionuclide imaging: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDc0OTA0ODkyMzcxNTY)",
            "[<b>33.Systemic Radionuclide imaging: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDg0OTI1MTM1OTIwODM)",
            "[<b>34.Radiotherapy. Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NDk0OTQ1Mzc5NDcwMTA)",
            "[<b>35.Radiotherapy. Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTA0OTY1NjIzMDE5Mzc)",
            "[<b>36.Obstetrics and Gynaecology imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTE0OTg1ODY2NTY4NjQ)",
            "[<b>37.Breast imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTI1MDA2MTEwMTE3OTE)",
            "[<b>38.MSK: Arthritis and infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTM1MDI2MzUzNjY3MTg)",
            "[<b>39.MSK: Systemic bone disorders and Miscellaneous imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTQ1MDQ2NTk3MjE2NDU)",
            "[<b>40.MSK: Bone tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTU1MDY2ODQwNzY1NzI)",
            "[<b>41.MSK: Trauma rapid review</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTY1MDg3MDg0MzE0OTk)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        radiology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"radiology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"radiology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(radiology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pathology"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01: How to approach Pathology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTc1MTA3MzI3ODY0MjY)",
            "[<b>02: Cell Adaptations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTg1MTI3NTcxNDEzNTM)",
            "[<b>03: Cell Injury</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NTk1MTQ3ODE0OTYyODA)",
            "[<b>04: Cell Death</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjA1MTY4MDU4NTEyMDc)",
            "[<b>05: Intracellular Accumulations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjE1MTg4MzAyMDYxMzQ)",
            "[<b>07: Chronic Inflammation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjI1MjA4NTQ1NjEwNjE)",
            "[<b>08: Mediators of Inflammation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjM1MjI4Nzg5MTU5ODg)",
            "[<b>09: Wound Healing & Tissue Repair</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjQ1MjQ5MDMyNzA5MTU)",
            "[<b>11: Neoplasia Basics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjU1MjY5Mjc2MjU4NDI)",
            "[<b>12: Types of Carcinogenesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NjY1Mjg5NTE5ODA3Njk)",
            "[<b>13: Hallmarks of Neoplasia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Njc1MzA5NzYzMzU2OTY)",
            "[<b>14: Lab Diagnosis of Cancer</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Njg1MzMwMDA2OTA2MjM)",
            "[<b>15: Tricks to Diagnose Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Njk1MzUwMjUwNDU1NTA)",
            "[<b>16: Genetics - Basic Concepts & Diagnosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzA1MzcwNDk0MDA0Nzc)",
            "[<b>17: Genetics - Mendelian Modes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzE1MzkwNzM3NTU0MDQ)",
            "[<b>18: Genetics - Non Mendelian Modes & Pedigree</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzI1NDEwOTgxMTAzMzE)",
            "[<b>19: Genetics - Chromosomal Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzM1NDMxMjI0NjUyNTg)",
            "[<b>20: Immunity - Types of Immune Cells</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzQ1NDUxNDY4MjAxODU)",
            "[<b>21: Hypersensitivity Reactions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzU1NDcxNzExNzUxMTI)",
            "[<b>22: HLA & Graft Rejection</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2NzY1NDkxOTU1MzAwMzk)",
            "[<b>23: Immunodeficiency Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Nzc1NTEyMTk4ODQ5NjY)",
            "[<b>24. Amyloidosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Nzg1NTMyNDQyMzk4OTM)",
            "[<b>25: General Pathology Images</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2Nzk1NTUyNjg1OTQ4MjA)",
            "[<b>26: RBC - Introduction & Hypoproliferative Anemias</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODA1NTcyOTI5NDk3NDc)",
            "[<b>27: Peripheral Smear Examination</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODE1NTkzMTczMDQ2NzQ)",
            "[<b>28: Microcytic Hypochromic Anemias</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODI1NjEzNDE2NTk2MDE)",
            "[<b>29: Megaloblastic Anemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODM1NjMzNjYwMTQ1Mjg)",
            "[<b>30: Hemolytic Anemia - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODQ1NjUzOTAzNjk0NTU)",
            "[<b>31: Hemolytic Anemia - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODU1Njc0MTQ3MjQzODI)",
            "[<b>32: WBC Introduction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODY1Njk0MzkwNzkzMDk)",
            "[<b>33: Acute Lymphoblastic Leukemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODc1NzE0NjM0MzQyMzY)",
            "[<b>34: Acute Myeloid Leukemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODg1NzM0ODc3ODkxNjM)",
            "[<b>35: Myeloid Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2ODk1NzU1MTIxNDQwOTA)",
            "[<b>36: Hodgkin’s Lymphoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTA1Nzc1MzY0OTkwMTc)",
            "[<b>37: Non Hodgkin’s Lymphoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTE1Nzk1NjA4NTM5NDQ)",
            "[<b>38: Plasma Cell Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTI1ODE1ODUyMDg4NzE)",
            "[<b>39: Haemostatis - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTM1ODM2MDk1NjM3OTg)",
            "[<b>40: Haemostatis - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTQ1ODU2MzM5MTg3MjU)",
            "[<b>41: Blood Banking & Transfusion Medicine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTU1ODc2NTgyNzM2NTI)",
            "[<b>42: Practical Hematology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTY1ODk2ODI2Mjg1Nzk)",
            "[<b>43: Hematology Clinical Case Discussions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTc1OTE3MDY5ODM1MDY)",
            "[<b>44: Hematology Images</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTg1OTM3MzEzMzg0MzM)",
            "[<b>45: Blood Vessels - Sclerosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk2OTk1OTU3NTU2OTMzNjA)",
            "[<b>46: Blood Vessels - Vasculitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDA1OTc3ODAwNDgyODc)",
            "[<b>47: Vascular Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDE1OTk4MDQ0MDMyMTQ)",
            "[<b>48: Cardiovascular System - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDI2MDE4Mjg3NTgxNDE)",
            "[<b>49: Cardiovascular System - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDM2MDM4NTMxMTMwNjg)",
            "[<b>50: Obstructive Lung Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDQ2MDU4Nzc0Njc5OTU)",
            "[<b>51: Restrictive Lung Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDU2MDc5MDE4MjI5MjI)",
            "[<b>52: Granulomas & Infections of the Lung</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDY2MDk5MjYxNzc4NDk)",
            "[<b>53: Lung Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDc2MTE5NTA1MzI3NzY)",
            "[<b>54: Esophagus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDg2MTM5NzQ4ODc3MDM)",
            "[<b>55: Stomach</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MDk2MTU5OTkyNDI2MzA)",
            "[<b>56: Intestinal Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTA2MTgwMjM1OTc1NTc)",
            "[<b>57: Inflammatory Bowel Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTE2MjAwNDc5NTI0ODQ)",
            "[<b>58: Polyps & Colon Cancer</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTI2MjIwNzIzMDc0MTE)",
            "[<b>59: Liver Pathology - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTM2MjQwOTY2NjIzMzg)",
            "[<b>60: Liver Pathology - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTQ2MjYxMjEwMTcyNjU)",
            "[<b>61: Kidney - Basics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTU2MjgxNDUzNzIxOTI)",
            "[<b>62: Nephritic Syndromes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTY2MzAxNjk3MjcxMTk)",
            "[<b>63: Nephrotic Syndromes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTc2MzIxOTQwODIwNDY)",
            "[<b>64: Renal Involvement in Systemic Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTg2MzQyMTg0MzY5NzM)",
            "[<b>65: Kidney Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MTk2MzYyNDI3OTE5MDA)",
            "[<b>66: Male Genital - Penis & Prostate</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjA2MzgyNjcxNDY4Mjc)",
            "[<b>67: Testis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjE2NDAyOTE1MDE3NTQ)",
            "[<b>68: Female Genital Tract - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjI2NDIzMTU4NTY2ODE)",
            "[<b>69: Uterus & Endometrium</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjM2NDQzNDAyMTE2MDg)",
            "[<b>70: Ovarian Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjQ2NDYzNjQ1NjY1MzU)",
            "[<b>71: Breast Pathology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjU2NDgzODg5MjE0NjI)",
            "[<b>72: Non Neoplastic Lesions - Thyroid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MjY2NTA0MTMyNzYzODk)",
            "[<b>73: Thyroid Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Mjc2NTI0Mzc2MzEzMTY)",
            "[<b>74: Adrenal Medulla</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Mjg2NTQ0NjE5ODYyNDM)",
            "[<b>75: Pituitary & Parathyroid Gland</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Mjk2NTY0ODYzNDExNzA)",
            "[<b>76: Dermatopathology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzA2NTg1MTA2OTYwOTc)",
            "[<b>77: Bone & Soft Tissue Lesions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzE2NjA1MzUwNTEwMjQ)",
            "[<b>78: CNS- Non Neoplastic Lesions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzI2NjI1NTk0MDU5NTE)",
            "[<b>79: CNS Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzM2NjQ1ODM3NjA4Nzg)",
            "[<b>80: Systemic Pathology Images - Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzQ2NjY2MDgxMTU4MDU)",
            "[<b>81: Systemic Pathology Images - Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzU2Njg2MzI0NzA3MzI)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pathology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pathology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pathology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pathology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("obgy"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. How to study Obg</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3MzY2NzA2NTY4MjU2NTk)",
            "[<b>2 Gametogenesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Mzc2NzI2ODExODA1ODY)",
            "[<b>3 Fertilisation and Implantation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Mzg2NzQ3MDU1MzU1MTM)",
            "[<b>4. Teratogenic exposure of conceptus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Mzk2NzY3Mjk4OTA0NDA)",
            "[<b>5 fetus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDA2Nzg3NTQyNDUzNjc)",
            "[<b>6. Placenta</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDE2ODA3Nzg2MDAyOTQ)",
            "[<b>7. Placental Functions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDI2ODI4MDI5NTUyMjE)",
            "[<b>8. Placental anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDM2ODQ4MjczMTAxNDg)",
            "[<b>9 Cord and Anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDQ2ODY4NTE2NjUwNzU)",
            "[<b>10 amnitic fluid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDU2ODg4NzYwMjAwMDI)",
            "[<b>11 amniotic fluid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDY2OTA5MDAzNzQ5Mjk)",
            "[<b>12 Antenatal patients - History</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDc2OTI5MjQ3Mjk4NTY)",
            "[<b>13 Antenatal patients - Signs, Symptoms and Minor ailments</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDg2OTQ5NDkwODQ3ODM)",
            "[<b>14 Antenatal patient - Investigations and Advice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NDk2OTY5NzM0Mzk3MTA)",
            "[<b>15 aneuploid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTA2OTg5OTc3OTQ2Mzc)",
            "[<b>16 fetal monitoring</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTE3MDEwMjIxNDk1NjQ)",
            "[<b>17. Maternal adaptation in pregnancy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTI3MDMwNDY1MDQ0OTE)",
            "[<b>18 Obstetrics Pharmacology Integration</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTM3MDUwNzA4NTk0MTg)",
            "[<b>19. Obstetrics Radiology Integration Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTQ3MDcwOTUyMTQzNDU)",
            "[<b>20. Obstetrics Radiology Integration part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTU3MDkxMTk1NjkyNzI)",
            "[<b>21. Obstetrics Medicine Integration</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTY3MTExNDM5MjQxOTk)",
            "[<b>22 anemia 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTc3MTMxNjgyNzkxMjY)",
            "[<b>23 Anemia in pregnancy: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTg3MTUxOTI2MzQwNTM)",
            "[<b>24 Diabetes in pregnancy. Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NTk3MTcyMTY5ODg5ODA)",
            "[<b>25 Diabetes in pregnancy. Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjA3MTkyNDEzNDM5MDc)",
            "[<b>26 Hypertension in pregnancy. Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjE3MjEyNjU2OTg4MzQ)",
            "[<b>27 Hypertension in pregnancy: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjI3MjMyOTAwNTM3NjE)",
            "[<b>28. IUGR</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjM3MjUzMTQ0MDg2ODg)",
            "[<b>29 HIV in pregnancy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjQ3MjczMzg3NjM2MTU)",
            "[<b>30 RH negative Pregnancy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjU3MjkzNjMxMTg1NDI)",
            "[<b>31 Twin Pregnancy part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NjY3MzEzODc0NzM0Njk)",
            "[<b>32 Twin Pregnancy Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Njc3MzM0MTE4MjgzOTY)",
            "[<b>33 Preterm Labor part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Njg3MzU0MzYxODMzMjM)",
            "[<b>34 Preterm labor part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Njk3Mzc0NjA1MzgyNTA)",
            "[<b>35. PROM</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzA3Mzk0ODQ4OTMxNzc)",
            "[<b>36 Abortion: Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzE3NDE1MDkyNDgxMDQ)",
            "[<b>37 Abortion: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzI3NDM1MzM2MDMwMzE)",
            "[<b>38 Ectopic pregnancy. Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzM3NDU1NTc5NTc5NTg)",
            "[<b>39 Ectopic pregnancy. Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzQ3NDc1ODIzMTI4ODU)",
            "[<b>40 Gestational trophoblastic disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzU3NDk2MDY2Njc4MTI)",
            "[<b>41 Antepartum haemorrhage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3NzY3NTE2MzEwMjI3Mzk)",
            "[<b>42 Placenta accreta spectrum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Nzc3NTM2NTUzNzc2NjY)",
            "[<b>43 Maternal pelvis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Nzg3NTU2Nzk3MzI1OTM)",
            "[<b>44 Fetal skull</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3Nzk3NTc3MDQwODc1MjA)",
            "[<b>45 Terminology related to labor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODA3NTk3Mjg0NDI0NDc)",
            "[<b>46. Leopold Maneuver and antenatal examination</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODE3NjE3NTI3OTczNzQ)",
            "[<b>47. Mechanism of labor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODI3NjM3NzcxNTIzMDE)",
            "[<b>48 Normal labor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODM3NjU4MDE1MDcyMjg)",
            "[<b>49. Induction of labor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODQ3Njc4MjU4NjIxNTU)",
            "[<b>50. Stages of labor, Abnormal labor, Partogram part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODU3Njk4NTAyMTcwODI)",
            "[<b>51 Stages of labor, Abnormal labor and Partogram: Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODY3NzE4NzQ1NzIwMDk)",
            "[<b>52 Complications of third stage of labor - PPH</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODc3NzM4OTg5MjY5MzY)",
            "[<b>53. Other complications of third stage of labor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODg3NzU5MjMyODE4NjM)",
            "[<b>54. Malpresentation part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3ODk3Nzc5NDc2MzY3OTA)",
            "[<b>55. Malpresentation part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTA3Nzk5NzE5OTE3MTc)",
            "[<b>56. Instrumental delivery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTE3ODE5OTYzNDY2NDQ)",
            "[<b>57 Cesarean section</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTI3ODQwMjA3MDE1NzE)",
            "[<b>59. Menstrual Cycle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTM3ODYwNDUwNTY0OTg)",
            "[<b>60. Atypical Uterine bleeding part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTQ3ODgwNjk0MTE0MjU)",
            "[<b>61. Atypical Uterine bleeding Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTU3OTAwOTM3NjYzNTI)",
            "[<b>62. Dysmenorrhea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTY3OTIxMTgxMjEyNzk)",
            "[<b>63. Gynecology Anatomy Integration part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTc3OTQxNDI0NzYyMDY)",
            "[<b>64. Gynecology Anatomy Integration Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTg3OTYxNjY4MzExMzM)",
            "[<b>65. Gynecology Anatomy Integration Part 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk3OTk3OTgxOTExODYwNjA)",
            "[<b>66. Gynecology Anatomy Integration Part 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDA4MDAyMTU1NDA5ODc)",
            "[<b>67. Gynecology Physiology Integration Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDE4MDIyMzk4OTU5MTQ)",
            "[<b>68. Gynecology Physiology Integration Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDI4MDQyNjQyNTA4NDE)",
            "[<b>69. Gynecology Pharmacology Integration part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDM4MDYyODg2MDU3Njg)",
            "[<b>70. Gynecology Pharmacology Integration part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDQ4MDgzMTI5NjA2OTU)",
            "[<b>71. Gynecology Pharmacology Integration part 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDU4MTAzMzczMTU2MjI)",
            "[<b>72. Gynecology Pathology integration part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDY4MTIzNjE2NzA1NDk)",
            "[<b>73. Gynecology Pathology Integration part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDc4MTQzODYwMjU0NzY)",
            "[<b>74. Menopause</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDg4MTY0MTAzODA0MDM)",
            "[<b>75. Pcos part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MDk4MTg0MzQ3MzUzMzA)",
            "[<b>76. PCOS PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTA4MjA0NTkwOTAyNTc)",
            "[<b>77. Endometrosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTE4MjI0ODM0NDUxODQ)",
            "[<b>78. Fibroid Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTI4MjQ1MDc4MDAxMTE)",
            "[<b>79. Fibroid part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTM4MjY1MzIxNTUwMzg)",
            "[<b>80. Polyp and adenomyosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTQ4Mjg1NTY1MDk5NjU)",
            "[<b>81. Congenital Malformations of uterus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTU4MzA1ODA4NjQ4OTI)",
            "[<b>82. Prolapse</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTY4MzI2MDUyMTk4MTk)",
            "[<b>83. Stress urinary incontinence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTc4MzQ2Mjk1NzQ3NDY)",
            "[<b>84. Urinary Fistulas</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTg4MzY2NTM5Mjk2NzM)",
            "[<b>85. Normal sexual development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MTk4Mzg2NzgyODQ2MDA)",
            "[<b>86. Puberty</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjA4NDA3MDI2Mzk1Mjc)",
            "[<b>87. Disorders of sexual development part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjE4NDI3MjY5OTQ0NTQ)",
            "[<b>88. Disorders of sexual development part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjI4NDQ3NTEzNDkzODE)",
            "[<b>89. Primary Amenorrhea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjM4NDY3NzU3MDQzMDg)",
            "[<b>90. secondary amenorrhea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjQ4NDg4MDAwNTkyMzU)",
            "[<b>91. Vaginitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjU4NTA4MjQ0MTQxNjI)",
            "[<b>92. PID</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MjY4NTI4NDg3NjkwODk)",
            "[<b>93. Genital TB</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4Mjc4NTQ4NzMxMjQwMTY)",
            "[<b>94. Female Infertility</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4Mjg4NTY4OTc0Nzg5NDM)",
            "[<b>95. Male infertility</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4Mjk4NTg5MjE4MzM4NzA)",
            "[<b>96. Natural Methods of Contraception</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzA4NjA5NDYxODg3OTc)",
            "[<b>97. Barrier Methods of contraception</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzE4NjI5NzA1NDM3MjQ)",
            "[<b>98 Estrogen and Progesterone contraceptives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzI4NjQ5OTQ4OTg2NTE)",
            "[<b>99 Only Progesterone contraceptives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzM4NjcwMTkyNTM1Nzg)",
            "[<b>100 IUCDS</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzQ4NjkwNDM2MDg1MDU)",
            "[<b>101 Permanent methods of contraception</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzU4NzEwNjc5NjM0MzI)",
            "[<b>102 Miscellaneous contraception</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4MzY4NzMwOTIzMTgzNTk)",
            "[<b>103. Endometrial Hyperplasia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4Mzc4NzUxMTY2NzMyODY)",
            "[<b>104. Endometrial Cancer</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4Mzg4NzcxNDEwMjgyMTM)",
            "[<b>105. CIN Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4Mzk4NzkxNjUzODMxNDA)",
            "[<b>106. CIN PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4NDA4ODExODk3MzgwNjc)",
            "[<b>107. Cancer cervix</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4NDE4ODMyMTQwOTI5OTQ)",
            "[<b>108 Ovarian cancer. Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4NDI4ODUyMzg0NDc5MjE)",
            "[<b>109 Ovarian cancer. Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4NDM4ODcyNjI4MDI4NDg)",
            "[<b>110 Vulval cancer</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk4NDQ4ODkyODcxNTc3NzU)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        obgy_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"obgy_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"obgy_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(obgy_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("recentupdates"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Surgery recent updates - Bailey Chapters 1 to 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NDgwOTc3OTU3MTUyNTY)",
            "[<b>Surgery Recent updates - Nutriton</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NDkwOTk4MjAwNzAxODM)",
            "[<b>Surgery Recent updates -Trauma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTAxMDE4NDQ0MjUxMTA)",
            "[<b>Surgery Recent updates - Endocrine Surgery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTExMDM4Njg3ODAwMzc)",
            "[<b>Surgery Recent updates - Head and Neck section</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTIxMDU4OTMxMzQ5NjQ)",
            "[<b>Surgery Recent updates - GIT Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTMxMDc5MTc0ODk4OTE)",
            "[<b>Surgery Recent updates - GIT Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTQxMDk5NDE4NDQ4MTg)",
            "[<b>Surgery Recent updates - GIT Part 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTUxMTE5NjYxOTk3NDU)",
            "[<b>Surgery Recent updates - Urology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTYxMTM5OTA1NTQ2NzI)",
            "[<b>Surgery Recent updates - Transplant surgery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTcxMTYwMTQ5MDk1OTk)",
            "[<b>Surgery Recent updates - Vascular surgery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTgxMTgwMzkyNjQ1MjY)",
            "[<b>Surgery Recent updates - Pediatrics surgery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NTkxMjAwNjM2MTk0NTM)",
            "[<b>Medicine Recent updates - 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjAxMjIwODc5NzQzODA)",
            "[<b>Medicine Recent updates - 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjExMjQxMTIzMjkzMDc)",
            "[<b>OBGY Recent updates - 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjIxMjYxMzY2ODQyMzQ)",
            "[<b>OBGY Recent updates - 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjMxMjgxNjEwMzkxNjE)",
            "[<b>Paediatrics Recent updates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjQxMzAxODUzOTQwODg)",
            "[<b>Dermatology Recent updates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjUxMzIyMDk3NDkwMTU)",
            "[<b>Community Medicine Recent updates -1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjYxMzQyMzQxMDM5NDI)",
            "[<b>Community Medicine Recent updates -2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjcxMzYyNTg0NTg4Njk)",
            "[<b>Pharmacology Recent updates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTk5NjgxMzgyODI4MTM3OTY)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        recentupdates_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"recentupdates_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"recentupdates_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(recentupdates_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("surgery"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data.startswith("pediatrics"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>0.How to approach pediatrics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTA1NjczODMzOTA0NDQ)",
            "[<b>1.Normal Newborn</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTE1Njk0MDc3NDUzNzE)",
            "[<b>2.Routine Newborn Care</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTI1NzE0MzIxMDAyOTg)",
            "[<b>3.Management of LBW Babies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTM1NzM0NTY0NTUyMjU)",
            "[<b>4.Neonatal Resuscitation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTQ1NzU0ODA4MTAxNTI)",
            "[<b>5.Infections in neonates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTU1Nzc1MDUxNjUwNzk)",
            "[<b>6.Birth asphyxia and neonatal seizures</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTY1Nzk1Mjk1MjAwMDY)",
            "[<b>7. NEC</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTc1ODE1NTM4NzQ5MzM)",
            "[<b>8.Respiratory distress in newborn</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTg1ODM1NzgyMjk4NjA)",
            "[<b>9.Neonatal hypoglycemia and infant of diabetic mother</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkxOTk1ODU2MDI1ODQ3ODc)",
            "[<b>10.Neonatal jaundice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDA1ODc2MjY5Mzk3MTQ)",
            "[<b>11. Normal Growth</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDE1ODk2NTEyOTQ2NDE)",
            "[<b>12. Abnormalities in head and size</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDI1OTE2NzU2NDk1Njg)",
            "[<b>13. Short stature</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDM1OTM3MDAwMDQ0OTU)",
            "[<b>14. Normal development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDQ1OTU3MjQzNTk0MjI)",
            "[<b>15.  Disorders of development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDU1OTc3NDg3MTQzNDk)",
            "[<b>16. Behavioural disorders in children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDY1OTk3NzMwNjkyNzY)",
            "[<b>17. Breastfeeding</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDc2MDE3OTc0MjQyMDM)",
            "[<b>18. Malnutrition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDg2MDM4MjE3NzkxMzA)",
            "[<b>19. Rickets and scurvy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMDk2MDU4NDYxMzQwNTc)",
            "[<b>20. Genetic disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTA2MDc4NzA0ODg5ODQ)",
            "[<b>21. Common childhood infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTE2MDk4OTQ4NDM5MTE)",
            "[<b>22. TORCH Infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTI2MTE5MTkxOTg4Mzg)",
            "[<b>23. COVID-19 in children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTM2MTM5NDM1NTM3NjU)",
            "[<b>24. Gastrointestinal anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTQ2MTU5Njc5MDg2OTI)",
            "[<b>25. Diarrhoea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTU2MTc5OTIyNjM2MTk)",
            "[<b>26. Miscellaneous topics in GIT</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTY2MjAwMTY2MTg1NDY)",
            "[<b>27. Neonatal Cholestasis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTc2MjIwNDA5NzM0NzM)",
            "[<b>28. Metabolic Liver Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTg2MjQwNjUzMjg0MDA)",
            "[<b>29. Upper airway disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMTk2MjYwODk2ODMzMjc)",
            "[<b>30. Foreign body, congenital lung anomalies and asthma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjA2MjgxMTQwMzgyNTQ)",
            "[<b>31. Lower respiratory tract infection</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjE2MzAxMzgzOTMxODE)",
            "[<b>32 . Cystic fibrosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjI2MzIxNjI3NDgxMDg)",
            "[<b>33. Fetal circulation and introduction to congenital heart disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjM2MzQxODcxMDMwMzU)",
            "[<b>34. Acynotic congenital heart defects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjQ2MzYyMTE0NTc5NjI)",
            "[<b>35. Cyanotic congenital heart defects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjU2MzgyMzU4MTI4ODk)",
            "[<b>36. Acute rheumatic fever</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjY2NDAyNjAxNjc4MTY)",
            "[<b>37. Congenital anomalies of kidney and urinary tract</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjc2NDIyODQ1MjI3NDM)",
            "[<b>38. Glomerulonephritis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjg2NDQzMDg4Nzc2NzA)",
            "[<b>39. Nephrotic syndrome</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMjk2NDYzMzMyMzI1OTc)",
            "[<b>40. Inherited tubular disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzA2NDgzNTc1ODc1MjQ)",
            "[<b>41. Acute kidney injury and chronic kidney disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzE2NTAzODE5NDI0NTE)",
            "[<b>42. Congenital anomalies and hydrocephalus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzI2NTI0MDYyOTczNzg)",
            "[<b>43. Seizure disorders and epilepsy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzM2NTQ0MzA2NTIzMDU)",
            "[<b>44. Cerebral palsy and CNS infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzQ2NTY0NTUwMDcyMzI)",
            "[<b>45. Neuromuscular disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzU2NTg0NzkzNjIxNTk)",
            "[<b>46. Growth hormone deficiency and hypothyroidism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzY2NjA1MDM3MTcwODY)",
            "[<b>47. Adrenal disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzc2NjI1MjgwNzIwMTM)",
            "[<b>48. Pubertal disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzg2NjQ1NTI0MjY5NDA)",
            "[<b>49. Haematological malignancies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyMzk2NjY1NzY3ODE4Njc)",
            "[<b>50. Solid tumors in children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDA2Njg2MDExMzY3OTQ)",
            "[<b>51. Rheumatic disease of childhood</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDE2NzA2MjU0OTE3MjE)",
            "[<b>52. Approach to anemia in children and nutritional anemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDI2NzI2NDk4NDY2NDg)",
            "[<b>53. Congenital Hemolytic Anemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDM2NzQ2NzQyMDE1NzU)",
            "[<b>54. Bleeding disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDQ2NzY2OTg1NTY1MDI)",
            "[<b>55. Shock</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDU2Nzg3MjI5MTE0Mjk)",
            "[<b>56. PALS Guidelines</b>](https://t.me/{{\"X\"}}?start=Z2V0LTkyNDY2ODA3NDcyNjYzNTY)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pediatrics_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pediatrics_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pediatrics_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pediatrics_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data == "prepladder":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomyp"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistryp")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiologyp"), InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacologyp")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathologyp"), InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiologyp")],
            [InlineKeyboardButton("PSM", callback_data="psmp"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="ophthalmologyp")],
            [InlineKeyboardButton("ENT", callback_data="entp"), InlineKeyboardButton("FMT", callback_data="fmtp")],
            [InlineKeyboardButton("SURGERY", callback_data="surgeryp"), InlineKeyboardButton("MEDICINE", callback_data="medicinep")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="dermatologyp"), InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatryp")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesiap"), InlineKeyboardButton("RADIOLOGY", callback_data="radiologyp")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedicsp"), InlineKeyboardButton("PEDIATRICS", callback_data="pediatricsp")],
            [InlineKeyboardButton("OBGY", callback_data="obgyp"), InlineKeyboardButton("RECENT UPDATES", callback_data="recentupdatesp")]
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start") InlineKeyboardButton("CLOSE", callback_data="close_data")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("anatomyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Introduction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDA2MjE1MjA4MzAxMDIy)",
            "[<b>1. developmental-timeline</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDA3MjE3MjMyNjU1OTQ5)",
            "[<b>2. Gametogenesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDA4MjE5MjU3MDEwODc2)",
            "[<b>3. developmental period week 1 & 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDA5MjIxMjgxMzY1ODAz)",
            "[<b>4. developmental-period-week-3-4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDEwMjIzMzA1NzIwNzMw)",
            "[<b>5. ectoderm-neural-crest-cells-derivatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDExMjI1MzMwMDc1NjU3)",
            "[<b>6. mesoderm-derivatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDEyMjI3MzU0NDMwNTg0)",
            "[<b>7. endoderm-derivatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDEzMjI5Mzc4Nzg1NTEx)",
            "[<b>8. placenta-formation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDE0MjMxNDAzMTQwNDM4)",
            "[<b>9. Germ-layer-derivatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDE1MjMzNDI3NDk1MzY1)",
            "[<b>1 body-tubes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDE2MjM1NDUxODUwMjky)",
            "[<b>2 epithelial-tissue</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDE3MjM3NDc2MjA1MjE5)",
            "[<b>3 glands</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDE4MjM5NTAwNTYwMTQ2)",
            "[<b>4 connective-tissue</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDE5MjQxNTI0OTE1MDcz)",
            "[<b>5 lymphoid-tissue</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDIwMjQzNTQ5MjcwMDAw)",
            "[<b>6 Cartilage-tissue</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDIxMjQ1NTczNjI0OTI3)",
            "[<b>7 Integumentary-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDIyMjQ3NTk3OTc5ODU0)",
            "[<b>8 Cell-junctions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDIzMjQ5NjIyMzM0Nzgx)",
            "[<b>9 Cell-junctions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDI0MjUxNjQ2Njg5NzA4)",
            "[<b>10 Respiratory-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDI1MjUzNjcxMDQ0NjM1)",
            "[<b>11 Digestive-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDI2MjU1Njk1Mzk5NTYy)",
            "[<b>12 Urinary-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDI3MjU3NzE5NzU0NDg5)",
            "[<b>13 Genital-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDI4MjU5NzQ0MTA5NDE2)",
            "[<b>1 Osteology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDI5MjYxNzY4NDY0MzQz)",
            "[<b>2 Arthrology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDMwMjYzNzkyODE5Mjcw)",
            "[<b>1 Organization-Of-Nervous-System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDMxMjY1ODE3MTc0MTk3)",
            "[<b>2 Development-Of-Nervous-System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDMyMjY3ODQxNTI5MTI0)",
            "[<b>3 Third-Ventricle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDMzMjY5ODY1ODg0MDUx)",
            "[<b>4 Fourth-Ventricle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDM0MjcxODkwMjM4OTc4)",
            "[<b>5 White-Matter-Types-Of-Fibres</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDM1MjczOTE0NTkzOTA1)",
            "[<b>6 Neural-Columns</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDM2Mjc1OTM4OTQ4ODMy)",
            "[<b>7 cerebrum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDM3Mjc3OTYzMzAzNzU5)",
            "[<b>8 Basal-Ganglia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDM4Mjc5OTg3NjU4Njg2)",
            "[<b>9 Internal-Capsule</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDM5MjgyMDEyMDEzNjEz)",
            "[<b>10 Thalamus-And-Hypthalamus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQwMjg0MDM2MzY4NTQw)",
            "[<b>11 Brainstem-and-Cranial-Nerve-Nuclei</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQxMjg2MDYwNzIzNDY3)",
            "[<b>12 Neural-Column-and-Brainstem-Nuclei</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQyMjg4MDg1MDc4Mzk0)",
            "[<b>13 Cerebellum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQzMjkwMTA5NDMzMzIx)",
            "[<b>14 Spinal-Cord</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQ0MjkyMTMzNzg4MjQ4)",
            "[<b>15 Autonomic-nervous-system.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQ1Mjk0MTU4MTQzMTc1)",
            "[<b>16 Arterial-Supply-of-Brain</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQ2Mjk2MTgyNDk4MTAy)",
            "[<b>17 Brainstem-Lesions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQ3Mjk4MjA2ODUzMDI5)",
            "[<b>18 Venous-Drainage-of-Cranial-Cavity</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQ4MzAwMjMxMjA3OTU2)",
            "[<b>1 Pharyngeal-Arches</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDQ5MzAyMjU1NTYyODgz)",
            "[<b>2 Pharyngeal-Pouches-Clefts</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDUwMzA0Mjc5OTE3ODEw)",
            "[<b>3 Tongue-Development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDUxMzA2MzA0MjcyNzM3)",
            "[<b>4 Pharyngeal-Arch-Arteries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDUyMzA4MzI4NjI3NjY0)",
            "[<b>5 Development-of-Skull</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDUzMzEwMzUyOTgyNTkx)",
            "[<b>6 Cranial-Cavity-Introduction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDU0MzEyMzc3MzM3NTE4)",
            "[<b>7 Cranial-Cavity-II-Cranial-fossae-and-related-foramina</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDU1MzE0NDAxNjkyNDQ1)",
            "[<b>8 _Cranial-Cavity-III-Middle-Cranial-Fossa</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDU2MzE2NDI2MDQ3Mzcy)",
            "[<b>9 Cranial-Cavity-IV-Posterior-Cranial-Fossa</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDU3MzE4NDUwNDAyMjk5)",
            "[<b>10 Trigeminal-Nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDU4MzIwNDc0NzU3MjI2)",
            "[<b>11 Cavernous-sinus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDU5MzIyNDk5MTEyMTUz)",
            "[<b>12 Facial-Nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDYwMzI0NTIzNDY3MDgw)",
            "[<b>13 Glossopharyngeal-Nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDYxMzI2NTQ3ODIyMDA3)",
            "[<b>14 vagus-nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDYyMzI4NTcyMTc2OTM0)",
            "[<b>15 hypoglossal-nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDYzMzMwNTk2NTMxODYx)",
            "[<b>16 cervical-plexus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDY0MzMyNjIwODg2Nzg4)",
            "[<b>17 scalenus-anterior-muscle-relations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDY1MzM0NjQ1MjQxNzE1)",
            "[<b>18 Head-and-Neck-Arterial-Supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDY2MzM2NjY5NTk2NjQy)",
            "[<b>19 Head-and-Neck-Venous-Drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDY3MzM4NjkzOTUxNTY5)",
            "[<b>20 Head-and-Neck-Lymphatic-Drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDY4MzQwNzE4MzA2NDk2)",
            "[<b>21 Scalp</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDY5MzQyNzQyNjYxNDIz)",
            "[<b>22 Neck-Triangles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDcwMzQ0NzY3MDE2MzUw)",
            "[<b>23 Neck-Fascia-and-Spaces</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDcxMzQ2NzkxMzcxMjc3)",
            "[<b>24 Neck-Fascia-and-Spaces-Revision</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDcyMzQ4ODE1NzI2MjA0)",
            "[<b>25 Parotid-Gland</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDczMzUwODQwMDgxMTMx)",
            "[<b>26 Pharynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDc0MzUyODY0NDM2MDU4)",
            "[<b>27 Oesophagus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDc1MzU0ODg4NzkwOTg1)",
            "[<b>29 Larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDc2MzU2OTEzMTQ1OTEy)",
            "[<b>30 Vertebral-LandMarks</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDc3MzU4OTM3NTAwODM5)",
            "[<b>31 Ear</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDc4MzYwOTYxODU1NzY2)",
            "[<b>32 Nose</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDc5MzYyOTg2MjEwNjkz)",
            "[<b>33 EyeBall</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDgwMzY1MDEwNTY1NjIw)",
            "[<b>34 Cranial-Nerves-3-4-and-6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDgxMzY3MDM0OTIwNTQ3)",
            "[<b>1 Spinal-cord-termination</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDgyMzY5MDU5Mjc1NDc0)",
            "[<b>2 Spinal-cord-Enlargements-and-Spaces</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDgzMzcxMDgzNjMwNDAx)",
            "[<b>3 Vertebrae</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDg0MzczMTA3OTg1MzI4)",
            "[<b>4 Lumbar-puncture</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDg1Mzc1MTMyMzQwMjU1)",
            "[<b>5 Vertebral-curvatures-and-slip-disc</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDg2Mzc3MTU2Njk1MTgy)",
            "[<b>6 Cranio-Vertebral-joints</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDg3Mzc5MTgxMDUwMTA5)",
            "[<b>7 -Vertebral-landmarks-and-triangles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDg4MzgxMjA1NDA1MDM2)",
            "[<b>1 evelopment-Cardiovascular-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDg5MzgzMjI5NzU5OTYz)",
            "[<b>2 Development Embryonicveins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDkwMzg1MjU0MTE0ODkw)",
            "[<b>3 Development-Heart-tube</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDkxMzg3Mjc4NDY5ODE3)",
            "[<b>4 Development-Heart-Tube-Transverse-pericardial-sinus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDkyMzg5MzAyODI0NzQ0)",
            "[<b>5 Development Interatrial-septum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDkzMzkxMzI3MTc5Njcx)",
            "[<b>6 Development AP-septum-formation-anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDk0MzkzMzUxNTM0NTk4)",
            "[<b>7 Fetoplacental-circulation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDk1Mzk1Mzc1ODg5NTI1)",
            "[<b>8 Surfaces and Grooves</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDk2Mzk3NDAwMjQ0NDUy)",
            "[<b>9 Venous drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDk3Mzk5NDI0NTk5Mzc5)",
            "[<b>10 Interior</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDk4NDAxNDQ4OTU0MzA2)",
            "[<b>11 Arterial-supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMDk5NDAzNDczMzA5MjMz)",
            "[<b>12 Sternal-angle-and-Mediastinum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTAwNDA1NDk3NjY0MTYw)",
            "[<b>13 Lungs Hilum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTAxNDA3NTIyMDE5MDg3)",
            "[<b>14 Broncho-pulmonary-segments</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTAyNDA5NTQ2Mzc0MDE0)",
            "[<b>15 Pleura-Surface-markings</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTAzNDExNTcwNzI4OTQx)",
            "[<b>16 Joints</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTA0NDEzNTk1MDgzODY4)",
            "[<b>17 Respiratory-movements</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTA1NDE1NjE5NDM4Nzk1)",
            "[<b>18 Intercostal-drainage-and-block</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTA2NDE3NjQzNzkzNzIy)",
            "[<b>19 Phrenic-nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTA3NDE5NjY4MTQ4NjQ5)",
            "[<b>20 Venous-drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTA4NDIxNjkyNTAzNTc2)",
            "[<b>21 Lymphatic-drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTA5NDIzNzE2ODU4NTAz)",
            "[<b>1 Embryology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTEwNDI1NzQxMjEzNDMw)",
            "[<b>2 Nerve-supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTExNDI3NzY1NTY4MzU3)",
            "[<b>3 Dermatomes-and-Myotomes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTEyNDI5Nzg5OTIzMjg0)",
            "[<b>4 Brachial-Plexus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTEzNDMxODE0Mjc4MjEx)",
            "[<b>5 Brachial-Plexus-II</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTE0NDMzODM4NjMzMTM4)",
            "[<b>6 Bones-and-Muscles-Proximal-Region-Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTE1NDM1ODYyOTg4MDY1)",
            "[<b>7 Bones-and-Muscles-Proximal-Region-Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTE2NDM3ODg3MzQyOTky)",
            "[<b>8 Bones-and-Muscles-Proximal-Region-Part-3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTE3NDM5OTExNjk3OTE5)",
            "[<b>9 Axilla</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTE4NDQxOTM2MDUyODQ2)",
            "[<b>10 Scapular-movements</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTE5NDQzOTYwNDA3Nzcz)",
            "[<b>11 Clavipectoral-fascia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTIwNDQ1OTg0NzYyNzAw)",
            "[<b>12 Muscles-of-anterior-arm-region</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTIxNDQ4MDA5MTE3NjI3)",
            "[<b>13 Muscles-of-anterior-forearm-region</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTIyNDUwMDMzNDcyNTU0)",
            "[<b>14 Cubital-fossa</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTIzNDUyMDU3ODI3NDgx)",
            "[<b>15 Carpal-and-Metacarpal-bones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTI0NDU0MDgyMTgyNDA4)",
            "[<b>16 Muscles-of-Hand</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTI1NDU2MTA2NTM3MzM1)",
            "[<b>17 Posterior-forearm-muscles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTI2NDU4MTMwODkyMjYy)",
            "[<b>18. radial-nerve-lessions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTI3NDYwMTU1MjQ3MTg5)",
            "[<b>19. ulnar-nerve-lesions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTI4NDYyMTc5NjAyMTE2)",
            "[<b>20. dr-rajesh-kaushal-1080-live-upper-limb-venous-drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTI5NDY0MjAzOTU3MDQz)",
            "[<b>21. dr-rajesh-kaushal-1080-live-upper-limb-lymphatic-drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTMwNDY2MjI4MzExOTcw)",
            "[<b>22. muscles-of-anterior-arm-region</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTMxNDY4MjUyNjY2ODk3)",
            "[<b>1. Umbilical-cord-contents-and-Anomalies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTMyNDcwMjc3MDIxODI0)",
            "[<b>2. Diaphragm-Development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTMzNDcyMzAxMzc2NzUx)",
            "[<b>3. Development-of-Mesentery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTM0NDc0MzI1NzMxNjc4)",
            "[<b>4. Gut-Rotation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTM1NDc2MzUwMDg2NjA1)",
            "[<b>5. Abdominal-planes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTM2NDc4Mzc0NDQxNTMy)",
            "[<b>6. Neurovascular-bundles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTM3NDgwMzk4Nzk2NDU5)",
            "[<b>7. Liver</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTM4NDgyNDIzMTUxMzg2)",
            "[<b>8. Inguinal-region-and-Femoral-region</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTM5NDg0NDQ3NTA2MzEz)",
            "[<b>9. Abdominal-wall-layers</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQwNDg2NDcxODYxMjQw)",
            "[<b>10. Inguinal-canal-and-Spermatic-cord</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQxNDg4NDk2MjE2MTY3)",
            "[<b>11. Inguinal-and-Femoral-region-associated-hernias</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQyNDkwNTIwNTcxMDk0)",
            "[<b>12. Peritoneal-cavity-Sacs-and-spaces</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQzNDkyNTQ0OTI2MDIx)",
            "[<b>13.Stomach</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQ0NDk0NTY5MjgwOTQ4)",
            "[<b>14. Arterial-supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQ1NDk2NTkzNjM1ODc1)",
            "[<b>15. Small-Intestine-Duodenum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQ2NDk4NjE3OTkwODAy)",
            "[<b>16.Small-Intestine-Jejunum-and-Ileum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQ3NTAwNjQyMzQ1NzI5)",
            "[<b>17. Small-Intestine-Biliary-Apparatus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQ4NTAyNjY2NzAwNjU2)",
            "[<b>18. Large-Intestine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTQ5NTA0NjkxMDU1NTgz)",
            "[<b>19. Pancreas</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTUwNTA2NzE1NDEwNTEw)",
            "[<b>20. Kidney</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTUxNTA4NzM5NzY1NDM3)",
            "[<b>21. Ureter</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTUyNTEwNzY0MTIwMzY0)",
            "[<b>22. Venous-drainage-of-abdomen-and-thorax</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTUzNTEyNzg4NDc1Mjkx)",
            "[<b>1. Development-of-Genito-Urinary-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTU0NTE0ODEyODMwMjE4)",
            "[<b>2. Pelvis-and-Perineum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTU1NTE2ODM3MTg1MTQ1)",
            "[<b>3. Perineal-pouches-and-ischiorectal-fossa</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTU2NTE4ODYxNTQwMDcy)",
            "[<b>4. Perineal-pouches-II</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTU3NTIwODg1ODk0OTk5)",
            "[<b>5. Prostate-gland-and-Parts-of-male-urethra</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTU4NTIyOTEwMjQ5OTI2)",
            "[<b>6. Pelvic-diaphragm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTU5NTI0OTM0NjA0ODUz)",
            "[<b>7. Extravasation-of-Urine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTYwNTI2OTU4OTU5Nzgw)",
            "[<b>8. Pudendal-nerve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTYxNTI4OTgzMzE0NzA3)",
            "[<b>9. Pelvis-Perineum-Arterial-supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTYyNTMxMDA3NjY5NjM0)",
            "[<b>10. Pelvis-Perineum-Nerve-supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTYzNTMzMDMyMDI0NTYx)",
            "[<b>11. Female-reproductive-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTY0NTM1MDU2Mzc5NDg4)",
            "[<b>12. Rectum-and-Anal-canal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTY1NTM3MDgwNzM0NDE1)",
            "[<b>1. Nerve-Supply-Overview-Lower-limb</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTY2NTM5MTA1MDg5MzQy)",
            "[<b>3. Nerve-Supply-Thigh-Muscles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTY3NTQxMTI5NDQ0MjY5)",
            "[<b>4. Movements-Associated-Muscles-Hip-Knee-Joints</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTY4NTQzMTUzNzk5MTk2)",
            "[<b>5. Muscles-of-Gluteal-Region</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTY5NTQ1MTc4MTU0MTIz)",
            "[<b>6. Hybrid-Muscles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTcwNTQ3MjAyNTA5MDUw)",
            "[<b>7.  Popliteus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTcxNTQ5MjI2ODYzOTc3)",
            "[<b>8. Knee-Joint</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTcyNTUxMjUxMjE4OTA0)",
            "[<b>9. Adductor-Canal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTczNTUzMjc1NTczODMx)",
            "[<b>10. Popliteal-Fossa</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTc0NTU1Mjk5OTI4NzU4)",
            "[<b>11. Leg-Muscles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTc1NTU3MzI0MjgzNjg1)",
            "[<b>12-Legand Footregion Nervesupply Replace</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTc2NTU5MzQ4NjM4NjEy)",
            "[<b>13. plantar-arches-eng-replace</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTc3NTYxMzcyOTkzNTM5)",
            "[<b>14. flexor-retinaculum-eng-replace</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTc4NTYzMzk3MzQ4NDY2)",
            "[<b>15. sole-muscles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTc5NTY1NDIxNzAzMzkz)",
            "[<b>16. lower-limb-arterial-supply</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTgwNTY3NDQ2MDU4MzIw)",
            "[<b>17. lower-limb-venous-drainage</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTgxNTY5NDcwNDEzMjQ3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anatomyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anatomyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anatomyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anatomyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("physiologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Homeostasis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTgyNTcxNDk0NzY4MTc0)",
            "[<b>2. Body Fluids; Distribution and Management</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTgzNTczNTE5MTIzMTAx)",
            "[<b>3. Cell Physiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTg0NTc1NTQzNDc4MDI4)",
            "[<b>4. Transport Across Cell Membrane</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTg1NTc3NTY3ODMyOTU1)",
            "[<b>1. Nerve And Neuron</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTg2NTc5NTkyMTg3ODgy)",
            "[<b>2. Resting Membrane Potential</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTg3NTgxNjE2NTQyODA5)",
            "[<b>3. Action Potential in Neuron</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTg4NTgzNjQwODk3NzM2)",
            "[<b>4. Nerve Fiber Classification-</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTg5NTg1NjY1MjUyNjYz)",
            "[<b>5. Structural Functional Anatomy of Skeletal Muscle Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTkwNTg3Njg5NjA3NTkw)",
            "[<b>6. Structural Functional Anatomy of Skeletal Muscle Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTkxNTg5NzEzOTYyNTE3)",
            "[<b>7. Motor Unit</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTkyNTkxNzM4MzE3NDQ0)",
            "[<b>8. Smooth Muscle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTkzNTkzNzYyNjcyMzcx)",
            "[<b>1. Live Conducting System of Heart</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTk0NTk1Nzg3MDI3Mjk4)",
            "[<b>2. Action Potential on Heart</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTk1NTk3ODExMzgyMjI1)",
            "[<b>3. Live ECG Basic Concepts</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTk2NTk5ODM1NzM3MTUy)",
            "[<b>4. Live Cardiac Cycle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTk3NjAxODYwMDkyMDc5)",
            "[<b>5. Live Cardiac Output</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTk4NjAzODg0NDQ3MDA2)",
            "[<b>6. Live Hemodynamics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMTk5NjA1OTA4ODAxOTMz)",
            "[<b>7. Live Blood Pressure It's Regulation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjAwNjA3OTMzMTU2ODYw)",
            "[<b>8. Regional Circulation Coronary and Cerebral New</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjAxNjA5OTU3NTExNzg3)",
            "[<b>1. Hematopoiesis and Blood Cells</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjAyNjExOTgxODY2NzE0)",
            "[<b>2. Hemostasis-New</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjAzNjE0MDA2MjIxNjQx)",
            "[<b>1. Functional Anatomy of Renal Physiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjA0NjE2MDMwNTc2NTY4)",
            "[<b>2. Gfr It's Regulation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjA1NjE4MDU0OTMxNDk1)",
            "[<b>3. JG Appratus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjA2NjIwMDc5Mjg2NDIy)",
            "[<b>4. Clearance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjA3NjIyMTAzNjQxMzQ5)",
            "[<b>5. Tubular Transport Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjA4NjI0MTI3OTk2Mjc2)",
            "[<b>6. Tubular Transport Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjA5NjI2MTUyMzUxMjAz)",
            "[<b>7. Acid Secretion in Kidney</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjEwNjI4MTc2NzA2MTMw)",
            "[<b>8. Counter Current System in Kidney</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjExNjMwMjAxMDYxMDU3)",
            "[<b>1. Functional Anatomy of The Respiratory System new</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjEyNjMyMjI1NDE1OTg0)",
            "[<b>2. Mechanics of Respiration new</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjEzNjM0MjQ5NzcwOTEx)",
            "[<b>3. Ventilation Perfusion of Lungs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjE0NjM2Mjc0MTI1ODM4)",
            "[<b>4.Compliance of Lung New</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjE1NjM4Mjk4NDgwNzY1)",
            "[<b>5. Lung Volume Capacities New</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjE2NjQwMzIyODM1Njky)",
            "[<b>6. Principles of Gas Diffusion</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjE3NjQyMzQ3MTkwNjE5)",
            "[<b>7. Oxygen Transport</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjE4NjQ0MzcxNTQ1NTQ2)",
            "[<b>8. Carbon Dioxide Transport</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjE5NjQ2Mzk1OTAwNDcz)",
            "[<b>9. Regulation of Respiration</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjIwNjQ4NDIwMjU1NDAw)",
            "[<b>10. Hypoxia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjIxNjUwNDQ0NjEwMzI3)",
            "[<b>11. High Altitude Physiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjIyNjUyNDY4OTY1MjU0)",
            "[<b>12. Deep Sea Diving</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjIzNjU0NDkzMzIwMTgx)",
            "[<b>1. Motility of Git</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjI0NjU2NTE3Njc1MTA4)",
            "[<b>2. Gi Hormones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjI1NjU4NTQyMDMwMDM1)",
            "[<b>3. Secretion and Absorption</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjI2NjYwNTY2Mzg0OTYy)",
            "[<b>1. Synapse Pre Synaptic Events</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjI3NjYyNTkwNzM5ODg5)",
            "[<b>2. Synapse Post Synaptic Events</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjI4NjY0NjE1MDk0ODE2)",
            "[<b>3. Synaptic Inhibition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjI5NjY2NjM5NDQ5NzQz)",
            "[<b>4. Somato Sensory Receptor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjMwNjY4NjYzODA0Njcw)",
            "[<b>5. Nociceptor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjMxNjcwNjg4MTU5NTk3)",
            "[<b>6. Proprioceptors and Reflexes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjMyNjcyNzEyNTE0NTI0)",
            "[<b>7. Ascending Tracts of Spinal Cord</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjMzNjc0NzM2ODY5NDUx)",
            "[<b>8.Descending Tracts of Spinal Cord</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjM0Njc2NzYxMjI0Mzc4)",
            "[<b>9. Basal Ganglia Cerebellum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjM1Njc4Nzg1NTc5MzA1)",
            "[<b>10. Special Senses Visual and Auditory Receptors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjM2NjgwODA5OTM0MjMy)",
            "[<b>11. Special Senses Smell and Taste Receptors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjM3NjgyODM0Mjg5MTU5)",
            "[<b>12. Hypothalamus and Limbic System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjM4Njg0ODU4NjQ0MDg2)",
            "[<b>13. EEG and Sleep</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjM5Njg2ODgyOTk5MDEz)",
            "[<b>14. Learning and Memory</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQwNjg4OTA3MzUzOTQw)",
            "[<b>1. Mechanisms of Hormone Actions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQxNjkwOTMxNzA4ODY3)",
            "[<b>2. Pituitary Hormones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQyNjkyOTU2MDYzNzk0)",
            "[<b>3. Thyroid Hormones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQzNjk0OTgwNDE4NzIx)",
            "[<b>4. Endocrine Pancrease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQ0Njk3MDA0NzczNjQ4)",
            "[<b>5. Hormonal Regulation of Calcium Balance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQ1Njk5MDI5MTI4NTc1)",
            "[<b>6. Adrenal Physiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQ2NzAxMDUzNDgzNTAy)",
            "[<b>7. Male Reproductive Physiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQ3NzAzMDc3ODM4NDI5)",
            "[<b>8. Female Reproductive Physiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQ4NzA1MTAyMTkzMzU2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        physiologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"physiologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"physiologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(physiologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("biochemistryp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1 .Cell and integration of Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjQ5NzA3MTI2NTQ4Mjgz)",
            "[<b>1. Classification of Carbohydrates Simple Carbohydrates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjUwNzA5MTUwOTAzMjEw)",
            "[<b>2. Mucopolysaccharidosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjUxNzExMTc1MjU4MTM3)",
            "[<b>3. Complex Carbohydrates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjUyNzEzMTk5NjEzMDY0)",
            "[<b>4. Isomerism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjUzNzE1MjIzOTY3OTkx)",
            "[<b>5. Urine Investigations Clinical Diagnosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjU0NzE3MjQ4MzIyOTE4)",
            "[<b>1. Glut Transporters</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjU1NzE5MjcyNjc3ODQ1)",
            "[<b>2. Glycolysis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjU2NzIxMjk3MDMyNzcy)",
            "[<b>3. Citric Acid Cycle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjU3NzIzMzIxMzg3Njk5)",
            "[<b>4. Glycogen Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjU4NzI1MzQ1NzQyNjI2)",
            "[<b>5. gluconeogenesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjU5NzI3MzcwMDk3NTUz)",
            "[<b>6. glycogen-storage-disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjYwNzI5Mzk0NDUyNDgw)",
            "[<b>7.fructose-and-galactose-metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjYxNzMxNDE4ODA3NDA3)",
            "[<b>8. hmp-shunt</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjYyNzMzNDQzMTYyMzM0)",
            "[<b>9. fates-of-pyruvate-pdh-complex</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjYzNzM1NDY3NTE3MjYx)",
            "[<b>1. Electron Transport Chain</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjY0NzM3NDkxODcyMTg4)",
            "[<b>1. Lipid Chemistry and Complex Lipids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjY1NzM5NTE2MjI3MTE1)",
            "[<b>2. Fatty Acid Cholesterol and Glycolipids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjY2NzQxNTQwNTgyMDQy)",
            "[<b>1. Fatty Acid Synthesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjY3NzQzNTY0OTM2OTY5)",
            "[<b>2. Fatty Acid Oxidation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjY4NzQ1NTg5MjkxODk2)",
            "[<b>3. Cholesterol and Bile Acid Synthesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjY5NzQ3NjEzNjQ2ODIz)",
            "[<b>4. lipoprotein-metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjcwNzQ5NjM4MDAxNzUw)",
            "[<b>5. Hyperlipoproteinemia & Fatty Liver</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjcxNzUxNjYyMzU2Njc3)",
            "[<b>1.Amino Acid Protein Chemistry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjcyNzUzNjg2NzExNjA0)",
            "[<b>2. Hemoglobin and Myoglobin</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjczNzU1NzExMDY2NTMx)",
            "[<b>3. EPP Chromatography</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjc0NzU3NzM1NDIxNDU4)",
            "[<b>1. Amino-Acid Catabolism Urea-Cycle and Hyperammonemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjc1NzU5NzU5Nzc2Mzg1)",
            "[<b>2. Glycine and one Carbon Pool</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjc2NzYxNzg0MTMxMzEy)",
            "[<b>3. Phenylalanine and Tyrosine Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjc3NzYzODA4NDg2MjM5)",
            "[<b>4. Amino Acid Metabolism Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjc4NzY1ODMyODQxMTY2)",
            "[<b>1.nucleotides-dna-chromosomes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjc5NzY3ODU3MTk2MDkz)",
            "[<b>2.mitochondrial-dna-and-replication</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjgwNzY5ODgxNTUxMDIw)",
            "[<b>3.DNA Repair Mechanism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjgxNzcxOTA1OTA1OTQ3)",
            "[<b>4.rna-transcription-post-transcriptional-modifications</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjgyNzczOTMwMjYwODc0)",
            "[<b>5.properties-of-genetic-code-mutation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjgzNzc1OTU0NjE1ODAx)",
            "[<b>6.inhibitors-of-translation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjg0Nzc3OTc4OTcwNzI4)",
            "[<b>7.PCR</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjg1NzgwMDAzMzI1NjU1)",
            "[<b>8.recombinant-dna-technology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjg2NzgyMDI3NjgwNTgy)",
            "[<b>9. microarray-crispr-lac-operon</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjg3Nzg0MDUyMDM1NTA5)",
            "[<b>10.chromosomes-cell-cycle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjg4Nzg2MDc2MzkwNDM2)",
            "[<b>1.enzymes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjg5Nzg4MTAwNzQ1MzYz)",
            "[<b>1. heme-synthesis-and-porphyrias</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjkwNzkwMTI1MTAwMjkw)",
            "[<b>1. fat-soluble-vitamins part1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjkxNzkyMTQ5NDU1MjE3)",
            "[<b>2.  fat-soluble-vitamins Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjkyNzk0MTczODEwMTQ0)",
            "[<b>3. water-soluble-vitamins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjkzNzk2MTk4MTY1MDcx)",
            "[<b>4. alcohol-metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjk0Nzk4MjIyNTE5OTk4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        biochemistryp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"biochemistryp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"biochemistryp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(biochemistryp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pharmacologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. How To Study</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjk1ODAwMjQ2ODc0OTI1)",
            "[<b>2. Introduction to Pharmacology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjk2ODAyMjcxMjI5ODUy)",
            "[<b>1.Pharmacokinetics Absorption</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjk3ODA0Mjk1NTg0Nzc5)",
            "[<b>2.  Pharmacokinetics Drug Distribution</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjk4ODA2MzE5OTM5NzA2)",
            "[<b>3. Pharmacokinetics Drug Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMjk5ODA4MzQ0Mjk0NjMz)",
            "[<b>4. Pharmacokinetics  Drug Excretion</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzAwODEwMzY4NjQ5NTYw)",
            "[<b>5. Half - Life, Kinetics of Elimination and Steady State Plasma Concentration</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzAxODEyMzkzMDA0NDg3)",
            "[<b>6. pH and pKa</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzAyODE0NDE3MzU5NDE0)",
            "[<b>7. Bioavailablity</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzAzODE2NDQxNzE0MzQx)",
            "[<b>8.  Pharmacodynamics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzA0ODE4NDY2MDY5MjY4)",
            "[<b>9. Dose Response Curve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzA1ODIwNDkwNDI0MTk1)",
            "[<b>10. Combined Effect ff Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzA2ODIyNTE0Nzc5MTIy)",
            "[<b>11. Adverse Drug Effects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzA3ODI0NTM5MTM0MDQ5)",
            "[<b>12. New Drugs Development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzA4ODI2NTYzNDg4OTc2)",
            "[<b>13. Drug Label and Fdc</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzA5ODI4NTg3ODQzOTAz)",
            "[<b>14. Theraputic Drug Monitoring</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzEwODMwNjEyMTk4ODMw)",
            "[<b>15. Rational Drug Prescribing,Essential Medicine & EBM</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzExODMyNjM2NTUzNzU3)",
            "[<b>16. Pharmacogenetics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzEyODM0NjYwOTA4Njg0)",
            "[<b>17. Pharmacokinetics Problems</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzEzODM2Njg1MjYzNjEx)",
            "[<b>1. Introduction to ANS and Cholinergic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzE0ODM4NzA5NjE4NTM4)",
            "[<b>2. Management of OP and Carbamate Poisoning</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzE1ODQwNzMzOTczNDY1)",
            "[<b>3. Drugs Used in Myasthenia Gravis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzE2ODQyNzU4MzI4Mzky)",
            "[<b>4. Anti Cholinergic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzE3ODQ0NzgyNjgzMzE5)",
            "[<b>5. Drugs Acting in Eye</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzE4ODQ2ODA3MDM4MjQ2)",
            "[<b>6. drugs-acting-on-bladder-and-bowel</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzE5ODQ4ODMxMzkzMTcz)",
            "[<b>7.introduction-of-adrenergic-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzIwODUwODU1NzQ4MTAw)",
            "[<b>8. adrenergic-drugs-catecholamines</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzIxODUyODgwMTAzMDI3)",
            "[<b>9. adrenergic-drugs-non-catecholamines</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzIyODU0OTA0NDU3OTU0)",
            "[<b>10. alpha-blockers</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzIzODU2OTI4ODEyODgx)",
            "[<b>11. beta-blockers</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzI0ODU4OTUzMTY3ODA4)",
            "[<b>12. Pharmacotherapy  of Glaucoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzI1ODYwOTc3NTIyNzM1)",
            "[<b>13. drugs-acting-on-ganglia.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzI2ODYzMDAxODc3NjYy)",
            "[<b>1. Histamine & Anti Histamine Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzI3ODY1MDI2MjMyNTg5)",
            "[<b>2. Serotonin Pharmacology and Drug for Migraine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzI4ODY3MDUwNTg3NTE2)",
            "[<b>3. prostaglandins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzI5ODY5MDc0OTQyNDQz)",
            "[<b>4. NSAIDs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzMwODcxMDk5Mjk3Mzcw)",
            "[<b>5. Gout</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzMxODczMTIzNjUyMjk3)",
            "[<b>6. Rheumatoid-arthritis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzMyODc1MTQ4MDA3MjI0)",
            "[<b>1. Diuretic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzMzODc3MTcyMzYyMTUx)",
            "[<b>2. Anti Diuretics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzM0ODc5MTk2NzE3MDc4)",
            "[<b>1. Drugs affecting RAAS pathway</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzM1ODgxMjIxMDcyMDA1)",
            "[<b>2. Anti Anginal Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzM2ODgzMjQ1NDI2OTMy)",
            "[<b>3. pharamacotherapy-of-chf</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzM3ODg1MjY5NzgxODU5)",
            "[<b>4. hypertension</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzM4ODg3Mjk0MTM2Nzg2)",
            "[<b>5. drugs-for-pulmonary-hypertension</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzM5ODg5MzE4NDkxNzEz)",
            "[<b>6. anti-arrhythmic-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQwODkxMzQyODQ2NjQw)",
            "[<b>1. sedative-hypnotics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQxODkzMzY3MjAxNTY3)",
            "[<b>2. ethanol</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQyODk1MzkxNTU2NDk0)",
            "[<b>3. anti-epileptic-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQzODk3NDE1OTExNDIx)",
            "[<b>4. anti-parkinsonian-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQ0ODk5NDQwMjY2MzQ4)",
            "[<b>5. mania-and-bipolar-disorde</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQ1OTAxNDY0NjIxMjc1)",
            "[<b>6. Anti Psychotic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQ2OTAzNDg4OTc2MjAy)",
            "[<b>7. anti-depressant-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQ3OTA1NTEzMzMxMTI5)",
            "[<b>8. opioids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQ4OTA3NTM3Njg2MDU2)",
            "[<b>9. drugs-for-anxiety</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzQ5OTA5NTYyMDQwOTgz)",
            "[<b>1. Hypothalamus & Pituitary Hormones Pharmacology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzUwOTExNTg2Mzk1OTEw)",
            "[<b>2. pharmacotherapy-of-diabetes-mellitus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzUxOTEzNjEwNzUwODM3)",
            "[<b>3. pharmacotherapy-of-osteoporosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzUyOTE1NjM1MTA1NzY0)",
            "[<b>4. corticosteroids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzUzOTE3NjU5NDYwNjkx)",
            "[<b>5. testosterone</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzU0OTE5NjgzODE1NjE4)",
            "[<b>6. benign-prostatic-hyperplasia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzU1OTIxNzA4MTcwNTQ1)",
            "[<b>7. estrogen-and-progesterone-preparations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzU2OTIzNzMyNTI1NDcy)",
            "[<b>8. hormonal-contraceptives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzU3OTI1NzU2ODgwMzk5)",
            "[<b>9. thyroid-hormones-anti-thyroid-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzU4OTI3NzgxMjM1MzI2)",
            "[<b>1. anti-microbials-penicillin</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzU5OTI5ODA1NTkwMjUz)",
            "[<b>2. cephalosporins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzYwOTMxODI5OTQ1MTgw)",
            "[<b>3.glycopeptides</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzYxOTMzODU0MzAwMTA3)",
            "[<b>4. tetracycline</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzYyOTM1ODc4NjU1MDM0)",
            "[<b>5. macrolides</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzYzOTM3OTAzMDA5OTYx)",
            "[<b>6. aminoglycosides-and-oxazolidinons</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzY0OTM5OTI3MzY0ODg4)",
            "[<b>7. sulfonamides</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzY1OTQxOTUxNzE5ODE1)",
            "[<b>8. flouroquinolones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzY2OTQzOTc2MDc0NzQy)",
            "[<b>9. antimicrobial-resistance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzY3OTQ2MDAwNDI5NjY5)",
            "[<b>10. important-points-in-antibacterial-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzY4OTQ4MDI0Nzg0NTk2)",
            "[<b>11. important-infections-and-drug-of-choice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzY5OTUwMDQ5MTM5NTIz)",
            "[<b>12. -drugs-for-uti-and-stis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzcwOTUyMDczNDk0NDUw)",
            "[<b>1. anti-tb-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzcxOTU0MDk3ODQ5Mzc3)",
            "[<b>2. tb-treatment-guidlines</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzcyOTU2MTIyMjA0MzA0)",
            "[<b>3. treatment-of-leprosy-and-mac</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzczOTU4MTQ2NTU5MjMx)",
            "[<b>4.anti-viral-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzc0OTYwMTcwOTE0MTU4)",
            "[<b>5. anti-hiv-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzc1OTYyMTk1MjY5MDg1)",
            "[<b>6. antiprotozoal-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzc2OTY0MjE5NjI0MDEy)",
            "[<b>7. anti-malarial-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzc3OTY2MjQzOTc4OTM5)",
            "[<b>8. Anti Fungal Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzc4OTY4MjY4MzMzODY2)",
            "[<b>9. anti-helminthic-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzc5OTcwMjkyNjg4Nzkz)",
            "[<b>1. Asthama</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzgwOTcyMzE3MDQzNzIw)",
            "[<b>2. Cough</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzgxOTc0MzQxMzk4NjQ3)",
            "[<b>1. Peptic Ulcer Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzgyOTc2MzY1NzUzNTc0)",
            "[<b>2. anti-emetic-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzgzOTc4MzkwMTA4NTAx)",
            "[<b>3. constipation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzg0OTgwNDE0NDYzNDI4)",
            "[<b>4. anti-diarrheal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzg1OTgyNDM4ODE4MzU1)",
            "[<b>1. anti-platelet-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzg2OTg0NDYzMTczMjgy)",
            "[<b>2. anti-coagulants</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzg3OTg2NDg3NTI4MjA5)",
            "[<b>3. thrombolytics-fibrinolytics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzg4OTg4NTExODgzMTM2)",
            "[<b>4. drugs-for-dyslipidemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzg5OTkwNTM2MjM4MDYz)",
            "[<b>5. colony-stimulating-factors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzkwOTkyNTYwNTkyOTkw)",
            "[<b>6. hemantinics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzkxOTk0NTg0OTQ3OTE3)",
            "[<b>7. chelating-agents</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzkyOTk2NjA5MzAyODQ0)",
            "[<b>1. platinum-compounds</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzkzOTk4NjMzNjU3Nzcx)",
            "[<b>2. cell-cycle-specific-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzk1MDAwNjU4MDEyNjk4)",
            "[<b>3. anti-cancer-drug</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzk2MDAyNjgyMzY3NjI1)",
            "[<b>4. hormonal-agents</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzk3MDA0NzA2NzIyNTUy)",
            "[<b>5. targeted-therapy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzk4MDA2NzMxMDc3NDc5)",
            "[<b>6. adverse-effects-of-anti-cancer-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwMzk5MDA4NzU1NDMyNDA2)",
            "[<b>1. Immunomodulators</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDAwMDEwNzc5Nzg3MzMz)",
            "[<b>1. general-anaesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDAxMDEyODA0MTQyMjYw)",
            "[<b>2. local-anaesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDAyMDE0ODI4NDk3MTg3)",
            "[<b>3. skeletal-muscle-relaxant-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDAzMDE2ODUyODUyMTE0)",
            "[<b>1. prescribing-drugs-during-pregnancy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDA0MDE4ODc3MjA3MDQx)",
            "[<b>2. confusing-drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDA1MDIwOTAxNTYxOTY4)",
            "[<b>3. antidotes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDA2MDIyOTI1OTE2ODk1)",
            "[<b>4. drug-interactions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDA3MDI0OTUwMjcxODIy)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pharmacologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pharmacologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pharmacologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pharmacologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("fmtp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. postmortem-techniques</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDA4MDI2OTc0NjI2NzQ5)",	
            "[<b>1. IPC Sections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDA5MDI4OTk4OTgxNjc2)",	
            "[<b>1. Torture</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDEwMDMxMDIzMzM2NjAz)",	
            "[<b>1. Court of Law</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDExMDMzMDQ3NjkxNTMw)",	
            "[<b>1. traces-of-evidence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDEyMDM1MDcyMDQ2NDU3)",	
            "[<b>1. sexual-offence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDEzMDM3MDk2NDAxMzg0)",	
            "[<b>2. impotence-sterility</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDE0MDM5MTIwNzU2MzEx)",	
            "[<b>3. version-impotence-abortion-and-mtp</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDE1MDQxMTQ1MTExMjM4)",	
            "[<b>1. medical-jurisprudence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDE2MDQzMTY5NDY2MTY1)",	
            "[<b>1. Infanticide</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDE3MDQ1MTkzODIxMDky)",	
            "[<b>1. asphyxial-death</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDE4MDQ3MjE4MTc2MDE5)",	
            "[<b>1. road-traffic-accident</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDE5MDQ5MjQyNTMwOTQ2)",	
            "[<b>2. thermal-injury</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDIwMDUxMjY2ODg1ODcz)",	
            "[<b>3. regional-injury</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDIxMDUzMjkxMjQwODAw)",	
            "[<b>4.mechanical-injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDIyMDU1MzE1NTk1NzI3)",	
            "[<b>1. Forensic Ballistics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDIzMDU3MzM5OTUwNjU0)",	
            "[<b>2. discharge-from-gun-effects</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDI0MDU5MzY0MzA1NTgx)",	
            "[<b>1.indentification-part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDI1MDYxMzg4NjYwNTA4)",	
            "[<b>2.indentification-part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDI2MDYzNDEzMDE1NDM1)",	
            "[<b>1. general-toxicology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDI3MDY1NDM3MzcwMzYy)",	
            "[<b>2. general-toxicology-2-insecticide-metallic-and-non-metallic-poison</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDI4MDY3NDYxNzI1Mjg5)",	
            "[<b>3. general-toxicology-3-starvation-death-asphyxiant-poison-miscellaneous-laws</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDI5MDY5NDg2MDgwMjE2)",	
            "[<b>4. animal-irritant-poison</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDMwMDcxNTEwNDM1MTQz)",	
            "[<b>5. corrosives-poisoning</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDMxMDczNTM0NzkwMDcw)",	
            "[<b>6. spinal-cardiac-poison</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDMyMDc1NTU5MTQ0OTk3)",	
            "[<b>7. somniferous-poison</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDMzMDc3NTgzNDk5OTI0)",	
            "[<b>8. organic-plant-irritant-poisions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDM0MDc5NjA3ODU0ODUx)",	
            "[<b>9. metal-poisons-miscellaneous-poisons-cns-depressant</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDM1MDgxNjMyMjA5Nzc4)",	
            "[<b>1.thanatology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDM2MDgzNjU2NTY0NzA1)",	
            "[<b>1. Forensic Psychiatry Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDM3MDg1NjgwOTE5NjMy)",	
            "[<b>2. Forensic Psychiatry Part-2.mkv</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDM4MDg3NzA1Mjc0NTU5)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        fmtp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"fmtp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"fmtp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(fmtp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("psmp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Definition , Components and Tools of Epidemiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDM5MDg5NzI5NjI5NDg2)",
            "[<b>2. need-classification-unit-approach-to-study-designs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQwMDkxNzUzOTg0NDEz)",
            "[<b>3. descriptive-study-disease-distribution</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQxMDkzNzc4MzM5MzQw)",
            "[<b>4. cohort-study</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQyMDk1ODAyNjk0MjY3)",
            "[<b>5. case-control-study</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQzMDk3ODI3MDQ5MTk0)",
            "[<b>6. nested-case-control</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQ0MDk5ODUxNDA0MTIx)",
            "[<b>7. cross-sectional-ecological-study-design-and-longitudinal-study-design</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQ1MTAxODc1NzU5MDQ4)",
            "[<b>8. bias</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQ2MTAzOTAwMTEzOTc1)",
            "[<b>9. confounders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQ3MTA1OTI0NDY4OTAy)",
            "[<b>10. experimental-studies-randomized-and-non-randomized-control-trials</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQ4MTA3OTQ4ODIzODI5)",
            "[<b>11. clinical-trials</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDQ5MTA5OTczMTc4NzU2)",
            "[<b>12. systematic-review-and-meta-analysis-evidence-based</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDUwMTExOTk3NTMzNjgz)",
            "[<b>13. hills-criteria</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDUxMTE0MDIxODg4NjEw)",
            "[<b>1. concept-of-disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDUyMTE2MDQ2MjQzNTM3)",
            "[<b>2. concept-of-well-being</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDUzMTE4MDcwNTk4NDY0)",
            "[<b>3. disease-control-elimination-and-eradication-of-disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDU0MTIwMDk0OTUzMzkx)",
            "[<b>4. levels-of-prevention</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDU1MTIyMTE5MzA4MzE4)",
            "[<b>5. health-indicators</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDU2MTI0MTQzNjYzMjQ1)",
            "[<b>v6. monitoring-evaluation-surveillance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDU3MTI2MTY4MDE4MTcy)",
            "[<b>1. vaccines</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDU4MTI4MTkyMzczMDk5)",
            "[<b>2. national-immunization-schedule-delayed-immunization</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDU5MTMwMjE2NzI4MDI2)",
            "[<b>3. open-vial-policy-misson-indradhanush</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDYwMTMyMjQxMDgyOTUz)",
            "[<b>4. cold-chain</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDYxMTM0MjY1NDM3ODgw)",
            "[<b>5. vaccines-cold-chain</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDYyMTM2Mjg5NzkyODA3)",
            "[<b>1. screening-test</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDYzMTM4MzE0MTQ3NzM0)",
            "[<b>2. properties-of-screening-test</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDY0MTQwMzM4NTAyNjYx)",
            "[<b>3. tests-in-combination</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDY1MTQyMzYyODU3NTg4)",
            "[<b>1. demography</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDY2MTQ0Mzg3MjEyNTE1)",
            "[<b>2. indicators-of-demography</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDY3MTQ2NDExNTY3NDQy)",
            "[<b>3. fertility-indicators</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDY4MTQ4NDM1OTIyMzY5)",
            "[<b>4. sources-of-health-information</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDY5MTUwNDYwMjc3Mjk2)",
            "[<b>1. family-planning-definition-concept</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDcwMTUyNDg0NjMyMjIz)",
            "[<b>2. Classification of Contraceptives and Barrier Methods of Contraceptive</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDcxMTU0NTA4OTg3MTUw)",
            "[<b>3. intra uterine devices</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDcyMTU2NTMzMzQyMDc3)",
            "[<b>4. hormonal-contraceptives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDczMTU4NTU3Njk3MDA0)",
            "[<b>5. physiological-methods-sterilization</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDc0MTYwNTgyMDUxOTMx)",
            "[<b>6. National Family Planning Welfare Program</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDc1MTYyNjA2NDA2ODU4)",
            "[<b>1. Preventive Obstetrics , Maternal Health</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDc2MTY0NjMwNzYxNzg1)",
            "[<b>2. preventive-paediatrics-child-health-indicators</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDc3MTY2NjU1MTE2NzEy)",
            "[<b>3. Growth and Devlopment . School Health Services</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDc4MTY4Njc5NDcxNjM5)",
            "[<b>1. nutrition-macronutrient-micronutrient</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDc5MTcwNzAzODI2NTY2)",
            "[<b>2. micronutrition-vitamins</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDgwMTcyNzI4MTgxNDkz)",
            "[<b>3. Food Adulteration and Food Fortification</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDgxMTc0NzUyNTM2NDIw)",
            "[<b>4.Nutrition Health Programmers and Food Logos</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDgyMTc2Nzc2ODkxMzQ3)",
            "[<b>5. Recommended Dietary Allowance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDgzMTc4ODAxMjQ2Mjc0)",
            "[<b>1. sociology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDg0MTgwODI1NjAxMjAx)",
            "[<b>2. Family and Socioeconomic Scales</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDg1MTgyODQ5OTU2MTI4)",
            "[<b>3. health-economics-doctor-patient-relationship-right-of-an-individuals-social-security</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDg2MTg0ODc0MzExMDU1)",
            "[<b>1. Water - Introduction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDg3MTg2ODk4NjY1OTgy)",
            "[<b>2. Purification of Water</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDg4MTg4OTIzMDIwOTA5)",
            "[<b>3. Air Pollution</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDg5MTkwOTQ3Mzc1ODM2)",
            "[<b>4. waste-disposal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDkwMTkyOTcxNzMwNzYz)",
            "[<b>5. noise-light-housing-radiation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDkxMTk0OTk2MDg1Njkw)",
            "[<b>6. entomology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDkyMTk3MDIwNDQwNjE3)",
            "[<b>1. infectious-disease-epidemiology part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDkzMTk5MDQ0Nzk1NTQ0)",
            "[<b>2. Infectious Disease Epidemiology Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDk0MjAxMDY5MTUwNDcx)",
            "[<b>3. measels-and-rubella</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDk1MjAzMDkzNTA1Mzk4)",
            "[<b>4. chicken-pox-and-small-pox</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDk2MjA1MTE3ODYwMzI1)",
            "[<b>5. mumps-and-pertussis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDk3MjA3MTQyMjE1MjUy)",
            "[<b>6. diptheria</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDk4MjA5MTY2NTcwMTc5)",
            "[<b>7. acute-respiratory-infection</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNDk5MjExMTkwOTI1MTA2)",
            "[<b>8. tuberculosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTAwMjEzMjE1MjgwMDMz)",
            "[<b>9. polio</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTAxMjE1MjM5NjM0OTYw)",
            "[<b>10. hepatitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTAyMjE3MjYzOTg5ODg3)",
            "[<b>11. diarrhea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTAzMjE5Mjg4MzQ0ODE0)",
            "[<b>12. cholera</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTA0MjIxMzEyNjk5NzQx)",
            "[<b>13. typhoid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTA1MjIzMzM3MDU0NjY4)",
            "[<b>14. soil-transmitted-helminthic-infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTA2MjI1MzYxNDA5NTk1)",
            "[<b>15. dengue</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTA3MjI3Mzg1NzY0NTIy)",
            "[<b>16. malaria</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTA4MjI5NDEwMTE5NDQ5)",
            "[<b>17. lymphatic-filariasis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTA5MjMxNDM0NDc0Mzc2)",
            "[<b>18. kala-azar-leishmaniasis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTEwMjMzNDU4ODI5MzAz)",
            "[<b>19. japanese-encephalitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTExMjM1NDgzMTg0MjMw)",
            "[<b>20. yellow-fever-kfd</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTEyMjM3NTA3NTM5MTU3)",
            "[<b>21. Rabies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTEzMjM5NTMxODk0MDg0)",
            "[<b>22. leptospirosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTE0MjQxNTU2MjQ5MDEx)",
            "[<b>23. plague</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTE1MjQzNTgwNjAzOTM4)",
            "[<b>24. tetanus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTE2MjQ1NjA0OTU4ODY1)",
            "[<b>25. hiv-aids</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTE3MjQ3NjI5MzEzNzky)",
            "[<b>26. rickettsial-diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTE4MjQ5NjUzNjY4NzE5)",
            "[<b>27 ebola-nipah-zika-virus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTE5MjUxNjc4MDIzNjQ2)",
            "[<b>1. national-health-mission-rmnch-a-maternal-initiatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTIwMjUzNzAyMzc4NTcz)",
            "[<b>2. child-adolescent-health-initiatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTIxMjU1NzI2NzMzNTAw)",
            "[<b>3. nacp-global-initiatives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTIyMjU3NzUxMDg4NDI3)",
            "[<b>4. national-tuberculosis-elimination-programme</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTIzMjU5Nzc1NDQzMzU0)",
            "[<b>5. nvbdcp-part1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTI0MjYxNzk5Nzk4Mjgx)",
            "[<b>6. nvbdcp-part2(diagnosis-treatment-prophylaxis)</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTI1MjYzODI0MTUzMjA4)",
            "[<b>7. polio-end-game-eradication-strategy-national-polio-surveillance-program</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTI2MjY1ODQ4NTA4MTM1)",
            "[<b>8. leprosy-and-national-leprosy-eradication-program</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTI3MjY3ODcyODYzMDYy)",
            "[<b>9. ncds-npcdcs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTI4MjY5ODk3MjE3OTg5)",
            "[<b>10. national-program-for-control-of-blindness-visual-impairment</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTI5MjcxOTIxNTcyOTE2)",
            "[<b>11. health-initiatives-idsp-ayushman-bharat-miscellaneous</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTMwMjczOTQ1OTI3ODQz)",
            "[<b>1. health-education</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTMxMjc1OTcwMjgyNzcw)",
            "[<b>2. health-communication-interviews</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTMyMjc3OTk0NjM3Njk3)",
            "[<b>1. health-planing-and-planing-cycle</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTMzMjgwMDE4OTkyNjI0)",
            "[<b>2. health-planning-committees-niti-aayog</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTM0MjgyMDQzMzQ3NTUx)",
            "[<b>3. health-management-techniques-inventory-management</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTM1Mjg0MDY3NzAyNDc4)",
            "[<b>1. healh-care-of-the-community</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTM2Mjg2MDkyMDU3NDA1)",
            "[<b>2. health-care-delivery-system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTM3Mjg4MTE2NDEyMzMy)",
            "[<b>1. international-health</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTM4MjkwMTQwNzY3MjU5)",
            "[<b>2. sustainable-development-goals-miscellaneous</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTM5MjkyMTY1MTIyMTg2)",
            "[<b>1. occupational-health</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQwMjk0MTg5NDc3MTEz)",
            "[<b>2. ESI Act , Factory Acd and Nrega ACt</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQxMjk2MjEzODMyMDQw)",
            "[<b>3. disaster-management</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQyMjk4MjM4MTg2OTY3)",
            "[<b>4. biomedical-waste Managemenr</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQzMzAwMjYyNTQxODk0)",
            "[<b>5. genetics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQ0MzAyMjg2ODk2ODIx)",
            "[<b>1. biostatics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQ1MzA0MzExMjUxNzQ4)",
            "[<b>2. measures-of-central-tendency</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQ2MzA2MzM1NjA2Njc1)",
            "[<b>3. measures-of-dispersion</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQ3MzA4MzU5OTYxNjAy)",
            "[<b>4. types-of-distribution</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQ4MzEwMzg0MzE2NTI5)",
            "[<b>5. types-of-errors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTQ5MzEyNDA4NjcxNDU2)",
            "[<b>6. test-of-statistical-significance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTUwMzE0NDMzMDI2Mzgz)",
            "[<b>7. graphical-representation-of-data</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTUxMzE2NDU3MzgxMzEw)",
            "[<b>8. sampling-probability</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTUyMzE4NDgxNzM2MjM3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psmp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psmp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psmp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psmp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("entp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Anatomy of External Ear Middle Ear</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTUzMzIwNTA2MDkxMTY0)",
            "[<b>2. Anatomy of Inner Ear</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTU0MzIyNTMwNDQ2MDkx)",
            "[<b>3. Physiology of Hearing</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTU1MzI0NTU0ODAxMDE4)",
            "[<b>4. Assesment of Hearing</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTU2MzI2NTc5MTU1OTQ1)",
            "[<b>5. Physiology of Vestibular System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTU3MzI4NjAzNTEwODcy)",
            "[<b>6. Assessment of Vestibular System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTU4MzMwNjI3ODY1Nzk5)",
            "[<b>7.Disease of Vestibular system</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTU5MzMyNjUyMjIwNzI2)",
            "[<b>8. Disease of External Ear</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTYwMzM0Njc2NTc1NjUz)",
            "[<b>9. Eustachian Tube</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTYxMzM2NzAwOTMwNTgw)",
            "[<b>10. Middel Ear Diseases Asom Som</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTYyMzM4NzI1Mjg1NTA3)",
            "[<b>11. Middle Ear Diseases Cholesteatoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTYzMzQwNzQ5NjQwNDM0)",
            "[<b>12. Middel Ear Diseases CSOM</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTY0MzQyNzczOTk1MzYx)",
            "[<b>13. Complication of ASOM and CSOM</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTY1MzQ0Nzk4MzUwMjg4)",
            "[<b>14. Otosclerosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTY2MzQ2ODIyNzA1MjE1)",
            "[<b>15. Facial nerve and Acoustic Neuroma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTY3MzQ4ODQ3MDYwMTQy)",
            "[<b>16. Meniere's Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTY4MzUwODcxNDE1MDY5)",
            "[<b>17. Glomus Tumor</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTY5MzUyODk1NzY5OTk2)",
            "[<b>18. Hearing Rehabilitation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTcwMzU0OTIwMTI0OTIz)",
            "[<b>19. Otalgia and Tinnitus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTcxMzU2OTQ0NDc5ODUw)",
            "[<b>1. Anatomy of Nose and Paranasal Sinuses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTcyMzU4OTY4ODM0Nzc3)",
            "[<b>2. Diseases of External Nose</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTczMzYwOTkzMTg5NzA0)",
            "[<b>3. Acute Chronic Rhinitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTc0MzYzMDE3NTQ0NjMx)",
            "[<b>4. CSF Rhinorrhea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTc1MzY1MDQxODk5NTU4)",
            "[<b>5. Granulomatous Lesions of Nose</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTc2MzY3MDY2MjU0NDg1)",
            "[<b>6. Congenital Anomalies of Nose</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTc3MzY5MDkwNjA5NDEy)",
            "[<b>7. Nasal Polyps</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTc4MzcxMTE0OTY0MzM5)",
            "[<b>8. Epistaxis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTc5MzczMTM5MzE5MjY2)",
            "[<b>9. Facial Trauma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTgwMzc1MTYzNjc0MTkz)",
            "[<b>10. Sinusitis and its Complication</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTgxMzc3MTg4MDI5MTIw)",
            "[<b>11. Tumors of The Nose Sinuses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTgyMzc5MjEyMzg0MDQ3)",
            "[<b>12. Malignancies of Paranasal Sinuses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTgzMzgxMjM2NzM4OTc0)",
            "[<b>13. Septal Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTg0MzgzMjYxMDkzOTAx)",
            "[<b>1. Anatomy of Pharynx Pharyngeal Spaces</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTg1Mzg1Mjg1NDQ4ODI4)",
            "[<b>2. Adenoids and Tonsils</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTg2Mzg3MzA5ODAzNzU1)",
            "[<b>3. Juvenile Nasopharyngeal Angiofibroma Nasopharyngeal Carcinoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTg3Mzg5MzM0MTU4Njgy)",
            "[<b>4. Ludwigs Angina and Pharyngeal Pouch</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTg4MzkxMzU4NTEzNjA5)",
            "[<b>5. Abscesses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTg5MzkzMzgyODY4NTM2)",
            "[<b>1. Anatomy of Larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTkwMzk1NDA3MjIzNDYz)",
            "[<b>2. Inflammator Conditions of Larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTkxMzk3NDMxNTc4Mzkw)",
            "[<b>3.  Benignc Inflammatory Lesions of Larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTkyMzk5NDU1OTMzMzE3)",
            "[<b>4. Voice Pathalogies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTkzNDAxNDgwMjg4MjQ0)",
            "[<b>5  Congenital Lesions of Larynx</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTk0NDAzNTA0NjQzMTcx)",
            "[<b>6. Laryngeal Paralysis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTk1NDA1NTI4OTk4MDk4)",
            "[<b>7. Laryngeal Carcinoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTk2NDA3NTUzMzUzMDI1)",
            "[<b>1. Radiology In ENT</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTk3NDA5NTc3NzA3OTUy)",
            "[<b>2. Instruments</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTk4NDExNjAyMDYyODc5)",
            "[<b>3. ENT Surgeries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNTk5NDEzNjI2NDE3ODA2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        entp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"entp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"entp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(entp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("pediatricsp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Assessment of Growth and Growth Charts</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjAwNDE1NjUwNzcyNzMz)",
            "[<b>2. Normal Anthropometric Parameters</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjAxNDE3Njc1MTI3NjYw)",
            "[<b>3. Short Stature tall Stature</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjAyNDE5Njk5NDgyNTg3)",
            "[<b>4. Abnormalities of Head Size Shape</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjAzNDIxNzIzODM3NTE0)",
            "[<b>5. Normal Abnormal Dentition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjA0NDIzNzQ4MTkyNDQx)",
            "[<b>6. Image Based Questions Growth</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjA1NDI1NzcyNTQ3MzY4)",
            "[<b>1. Important Motor Milestones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjA2NDI3Nzk2OTAyMjk1)",
            "[<b>2. Social Language Milestones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjA3NDI5ODIxMjU3MjIy)",
            "[<b>3. Developmental Implications of Important Milestones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjA4NDMxODQ1NjEyMTQ5)",
            "[<b>4. Image Based Questions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjA5NDMzODY5OTY3MDc2)",
            "[<b>1. Abnormalities of Development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjEwNDM1ODk0MzIyMDAz)",
            "[<b>2. Behavioural Disordes in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjExNDM3OTE4Njc2OTMw)",
            "[<b>1. Puberty and Adolescence</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjEyNDM5OTQzMDMxODU3)",
            "[<b>1. Important Terminologies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjEzNDQxOTY3Mzg2Nzg0)",
            "[<b>2. Primitive Neonatalc Reflex Conditions Seen in Neonates Not Requiring Treatment</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjE0NDQzOTkxNzQxNzEx)",
            "[<b>3. Neonatal Resuscitation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjE1NDQ2MDE2MDk2NjM4)",
            "[<b>4. IUGR</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjE2NDQ4MDQwNDUxNTY1)",
            "[<b>5. Feeding of Preterm Neonate</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjE3NDUwMDY0ODA2NDky)",
            "[<b>6. Neonatal Sepsis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjE4NDUyMDg5MTYxNDE5)",
            "[<b>7. Neonatal Hypothermia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjE5NDU0MTEzNTE2MzQ2)",
            "[<b>8.Neonatal Hypoglycemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjIwNDU2MTM3ODcxMjcz)",
            "[<b>9. Perinatal Asphyxia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjIxNDU4MTYyMjI2MjAw)",
            "[<b>10. Important Scores in Neonates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjIyNDYwMTg2NTgxMTI3)",
            "[<b>11. Respiratory Disorders in Neonates</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjIzNDYyMjEwOTM2MDU0)",
            "[<b>12. Necrotising Entercolitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjI0NDY0MjM1MjkwOTgx)",
            "[<b>13. Neonatal Jaundice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjI1NDY2MjU5NjQ1OTA4)",
            "[<b>14. Erythroblastosis Fetalis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjI2NDY4Mjg0MDAwODM1)",
            "[<b>15. Latest Updates In Neonatology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjI3NDcwMzA4MzU1NzYy)",
            "[<b>16. Neonatology Images</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjI4NDcyMzMyNzEwNjg5)",
            "[<b>1. Breast Milk Breast Feeding</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjI5NDc0MzU3MDY1NjE2)",
            "[<b>2. Micronutrients in Health Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjMwNDc2MzgxNDIwNTQz)",
            "[<b>3. Malnutrition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjMxNDc4NDA1Nzc1NDcw)",
            "[<b>4. Images from Nutrition Malnutrition</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjMyNDgwNDMwMTMwMzk3)",
            "[<b>1. Body Composition Acid Base Balance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjMzNDgyNDU0NDg1MzI0)",
            "[<b>2. Disorders of Sodium Potassium</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjM0NDg0NDc4ODQwMjUx)",
            "[<b>3. IV Fluids in Health Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjM1NDg2NTAzMTk1MTc4)",
            "[<b>4. Images Fluids and Electrolytes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjM2NDg4NTI3NTUwMTA1)",
            "[<b>1. Types of Genetic Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjM3NDkwNTUxOTA1MDMy)",
            "[<b>2. Important Genetic Syndromes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjM4NDkyNTc2MjU5OTU5)",
            "[<b>3. Images in Genetics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjM5NDk0NjAwNjE0ODg2)",
            "[<b>1. Disorders of  Carbohydrate Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQwNDk2NjI0OTY5ODEz)",
            "[<b>2. Disorders of Amino Acid Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQxNDk4NjQ5MzI0NzQw)",
            "[<b>3. Lysosomal Storage Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQ0NTA0NzIyMzg5NTIx)",
            "[<b>4. Images Inborn Errors of Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQ1NTA2NzQ2NzQ0NDQ4)",
            "[<b>1. Primary Immuno Deficiency</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQ2NTA4NzcxMDk5Mzc1)",
            "[<b>2. Vasculitic Disorders of Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQ3NTEwNzk1NDU0MzAy)",
            "[<b>3. Images of Disorders Of Immune System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQ4NTEyODE5ODA5MjI5)",
            "[<b>1. Important Viral Diseases in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjQ5NTE0ODQ0MTY0MTU2)",
            "[<b>2. COVID 19 in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjUwNTE2ODY4NTE5MDgz)",
            "[<b>3. Important Bacterial Diseases in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjUxNTE4ODkyODc0MDEw)",
            "[<b>4. Congenital Inferctions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjUyNTIwOTE3MjI4OTM3)",
            "[<b>5. Images of Important Infectious Diseases in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjUzNTIyOTQxNTgzODY0)",
            "[<b>1. Immunization - General Concepts & Special Situtation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjU0NTI0OTY1OTM4Nzkx)",
            "[<b>2. Individual Vaccine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjU1NTI2OTkwMjkzNzE4)",
            "[<b>3. Immunization Related Images</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjU2NTI5MDE0NjQ4NjQ1)",
            "[<b>1. Fetal Circulation Classification of Congenital Heart Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjU3NTMxMDM5MDAzNTcy)",
            "[<b>2. Important Acyanotic Congenital Heart Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjU4NTMzMDYzMzU4NDk5)",
            "[<b>3. Tetralogy of Fallot</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjU5NTM1MDg3NzEzNDI2)",
            "[<b>4. Rheumatic Heart Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjYwNTM3MTEyMDY4MzUz)",
            "[<b>5. Other Congenital Heart Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjYxNTM5MTM2NDIzMjgw)",
            "[<b>6. Image Based Question Pediatric Cardiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjYyNTQxMTYwNzc4MjA3)",
            "[<b>1. Important Hemotological Disorders in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjYzNTQzMTg1MTMzMTM0)",
            "[<b>2. Important Bleeding & Coagulation Disorders in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjY0NTQ1MjA5NDg4MDYx)",
            "[<b>3. Hematological Malignancies in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjY1NTQ3MjMzODQyOTg4)",
            "[<b>4. Tumors of Infancy Childhood</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjY2NTQ5MjU4MTk3OTE1)",
            "[<b>5. Images From Pediatric Hemato Oncology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjY3NTUxMjgyNTUyODQy)",
            "[<b>1. Disorders of Gastrointestinal System Including Diarrhea</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjY4NTUzMzA2OTA3NzY5)",
            "[<b>2. Liver Disorders in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjY5NTU1MzMxMjYyNjk2)",
            "[<b>1. Respiratory Disorders in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjcwNTU3MzU1NjE3NjIz)",
            "[<b>2. Bronchial Asthma In Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjcxNTU5Mzc5OTcyNTUw)",
            "[<b>3. Infections Of Airways Lungs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjcyNTYxNDA0MzI3NDc3)",
            "[<b>4. Images Of Respiratory Disorders in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjczNTYzNDI4NjgyNDA0)",
            "[<b>5. Cystic Fibrosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjc0NTY1NDUzMDM3MzMx)",
            "[<b>1. Normal Structure Fuction of Kidney in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjc1NTY3NDc3MzkyMjU4)",
            "[<b>2. Acute Chronic Kidney Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjc2NTY5NTAxNzQ3MTg1)",
            "[<b>3. Congenital Abnormalites of Genitourinary Tract</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjc3NTcxNTI2MTAyMTEy)",
            "[<b>4. Nephritic Nephrotic Syndrome</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjc4NTczNTUwNDU3MDM5)",
            "[<b>5. Obstructive Infective Disorders of Urinary Tract Infection in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjc5NTc1NTc0ODExOTY2)",
            "[<b>6. Renal Tubular Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjgwNTc3NTk5MTY2ODkz)",
            "[<b>1. Congential CNS  Malformation Hydrocephalus in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjgxNTc5NjIzNTIxODIw)",
            "[<b>2. Seizures in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjgyNTgxNjQ3ODc2NzQ3)",
            "[<b>3.Disorders with CNS Involvement Brain Death</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjgzNTgzNjcyMjMxNjc0)",
            "[<b>4. Images from Pediatricc Neurology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjg0NTg1Njk2NTg2NjAx)",
            "[<b>1. Disorders of Muscles in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjg1NTg3NzIwOTQxNTI4)",
            "[<b>2. Rickets</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjg2NTg5NzQ1Mjk2NDU1)",
            "[<b>3. Disorders Involving Bones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjg3NTkxNzY5NjUxMzgy)",
            "[<b>2. Disorders of Thryroid in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjg4NTkzNzk0MDA2MzA5)",
            "[<b>3. Adrenal Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjg5NTk1ODE4MzYxMjM2)",
            "[<b>4. Disorders of Puberty</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjkwNTk3ODQyNzE2MTYz)",
            "[<b>5. Disorders of Sexual Development</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjkxNTk5ODY3MDcxMDkw)",
            "[<b>6. Type 1 Diabetes Mellitus Obesity in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjkyNjAxODkxNDI2MDE3)",
            "[<b>1. Common Childhood Poisonings</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjkzNjAzOTE1NzgwOTQ0)",
            "[<b>1. Orogastric Feeding Tube Insertionina Neonate</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjk0NjA1OTQwMTM1ODcx)",
            "[<b>2. How to use Radiant Warmer for a Neonate</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjk1NjA3OTY0NDkwNzk4)",
            "[<b>3. Self Inflating Bag and Mask for Neonatal Resuscitation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjk2NjA5OTg4ODQ1NzI1)",
            "[<b>4. Identification of Preterms VS Term Neonate</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjk3NjEyMDEzMjAwNjUy)",
            "[<b>5. Steps of Hand Washing before Entering a Neonatal Intensive Care Unit (NICU)</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjk4NjE0MDM3NTU1NTc5)",
            "[<b>6. Different Types of Seizures seen in Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNjk5NjE2MDYxOTEwNTA2)",
            "[<b>7. Gower Sign</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzAwNjE4MDg2MjY1NDMz)",
            "[<b>8. Setting Sun Sign</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzAxNjIwMTEwNjIwMzYw)",
            "[<b>9. Sturge Weber Syndrome</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzAyNjIyMTM0OTc1Mjg3)",
            "[<b>10. Intravenous Cannula and its Insertion in Neonates Children</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzAzNjI0MTU5MzMwMjE0)",
            "[<b>11. Phototheraphy for Neonatal Jaundice</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzA0NjI2MTgzNjg1MTQx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pediatricsp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pediatricsp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pediatricsp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pediatricsp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("surgeryp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. About the faculty</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzA1NjI4MjA4MDQwMDY4)",	
            "[<b>2. How to use theapp</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzA2NjMwMjMyMzk0OTk1)",	
            "[<b>3. Which books to study</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzA3NjMyMjU2NzQ5OTIy)",	
            "[<b>1. High Yield Topics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzA4NjM0MjgxMTA0ODQ5)",	
            "[<b>1. Breast Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzA5NjM2MzA1NDU5Nzc2)",	
            "[<b>2.  Breast Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzEwNjM4MzI5ODE0NzAz)",	
            "[<b>3. Thyroid Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzExNjQwMzU0MTY5NjMw)",	
            "[<b>4. Thyroid Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzEyNjQyMzc4NTI0NTU3)",	
            "[<b>5. Parathyroid Adrenal Gland</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzEzNjQ0NDAyODc5NDg0)",	
            "[<b>1. Liver Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzE0NjQ2NDI3MjM0NDEx)",	
            "[<b>2. Liver Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzE1NjQ4NDUxNTg5MzM4)",	
            "[<b>3. Portal Hypertention</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzE2NjUwNDc1OTQ0MjY1)",	
            "[<b>4. Gallbladder</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzE3NjUyNTAwMjk5MTky)",	
            "[<b>5. Bile Dusct Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzE4NjU0NTI0NjU0MTE5)",	
            "[<b>6. Bile Dusct Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzE5NjU2NTQ5MDA5MDQ2)",	
            "[<b>7. Pancreas</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzIwNjU4NTczMzYzOTcz)",	
            "[<b>1. Esophagus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzIxNjYwNTk3NzE4OTAw)",	
            "[<b>2. Stomach and Duodenum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzIyNjYyNjIyMDczODI3)",	
            "[<b>3. Peritoneum</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzIzNjY0NjQ2NDI4NzU0)",	
            "[<b>4. Intestinal Obtruction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzI0NjY2NjcwNzgzNjgx)",	
            "[<b>5. Small Intestine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzI1NjY4Njk1MTM4NjA4)",	
            "[<b>6. Large Intestine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzI2NjcwNzE5NDkzNTM1)",	
            "[<b>7. Ileostomy and Colostomy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzI3NjcyNzQzODQ4NDYy)",	
            "[<b>8. Inflammatory Blow Disease Part1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzI4Njc0NzY4MjAzMzg5)",	
            "[<b>9. Inflammatory Blow Disease Part2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzI5Njc2NzkyNTU4MzE2)",	
            "[<b>10. Vermiform Appendix1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzMwNjc4ODE2OTEzMjQz)",	
            "[<b>11 .Rectum And Anal Canal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzMxNjgwODQxMjY4MTcw)",	
            "[<b>12. Hernia and Abdominal Wall 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzMyNjgyODY1NjIzMDk3)",	
            "[<b>12. Hernia and Abdominal Wall 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzMzNjg0ODg5OTc4MDI0)",	
            "[<b>13. Spleen</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzM0Njg2OTE0MzMyOTUx)",	
            "[<b>1. Kidney and Ureter Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzM1Njg4OTM4Njg3ODc4)",	
            "[<b>2. Kidney and Ureter Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzM2NjkwOTYzMDQyODA1)",	
            "[<b>3. Kidney Ureter Part-3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzM3NjkyOTg3Mzk3NzMy)",	
            "[<b>4. Urinary Bladder</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzM4Njk1MDExNzUyNjU5)",	
            "[<b>5. Prostate and Seminal Vesicles</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzM5Njk3MDM2MTA3NTg2)",	
            "[<b>6. Urethra and Penis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQwNjk5MDYwNDYyNTEz)",	
            "[<b>7. Testis Secrotum Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQxNzAxMDg0ODE3NDQw)",	
            "[<b>8. Testis Secrotum Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQyNzAzMTA5MTcyMzY3)",	
            "[<b>1. Arterial Discorders Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQzNzA1MTMzNTI3Mjk0)",	
            "[<b>2. Arteria Disorders Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQ0NzA3MTU3ODgyMjIx)",	
            "[<b>3. Venous Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQ1NzA5MTgyMjM3MTQ4)",	
            "[<b>4. Lymphatic System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQ2NzExMjA2NTkyMDc1)",	
            "[<b>5. Thorax and Mediastinum Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQ3NzEzMjMwOTQ3MDAy)",	
            "[<b>6. Thorax and Mediastinum Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQ4NzE1MjU1MzAxOTI5)",	
            "[<b>1. Burns</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzQ5NzE3Mjc5NjU2ODU2)",	
            "[<b>2. Plastic Surgery and Skin Lesions</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzUwNzE5MzA0MDExNzgz)",	
            "[<b>3. Wound Healding Tissue Reapair and Scar</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzUxNzIxMzI4MzY2NzEw)",	
            "[<b>1. Cerebrovasular Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzUyNzIzMzUyNzIxNjM3)",	
            "[<b>2. CNS Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzUzNzI1Mzc3MDc2NTY0)",	
            "[<b>1. Oral Cavity</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzU0NzI3NDAxNDMxNDkx)",	
            "[<b>2. Salivary Glands</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzU1NzI5NDI1Nzg2NDE4)",	
            "[<b>3. Neck</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzU2NzMxNDUwMTQxMzQ1)",	
            "[<b>4. Facial Injuries and Abnormalities</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzU3NzMzNDc0NDk2Mjcy)",	
            "[<b>1. Oncology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzU4NzM1NDk4ODUxMTk5)",	
            "[<b>1. Trauma ATLS Protocol</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzU5NzM3NTIzMjA2MTI2)",	
            "[<b>2. Pediatric Surgery Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzYwNzM5NTQ3NTYxMDUz)",	
            "[<b>3. Nutritionn</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzYxNzQxNTcxOTE1OTgw)",	
            "[<b>4. Peadiatric Surgery Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzYyNzQzNTk2MjcwOTA3)",	
            "[<b>5. Head Injury</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzYzNzQ1NjIwNjI1ODM0)",	
            "[<b>6. Neck and Thoracic Injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzY0NzQ3NjQ0OTgwNzYx)",	
            "[<b>7. Abdominal Trauma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzY1NzQ5NjY5MzM1Njg4)",	
            "[<b>8. Trasplantation Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzY2NzUxNjkzNjkwNjE1)",	
            "[<b>10. Robotics, Laparoscopy and Bariatic Surgery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzY3NzUzNzE4MDQ1NTQy)",	
            "[<b>11. Sutures and Anastomoses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzY4NzU1NzQyNDAwNDY5)",	
            "[<b>12. Shock</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzY5NzU3NzY2NzU1Mzk2)",	
            "[<b>13. General Surgery</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzcwNzU5NzkxMTEwMzIz)",	
            "[<b>14. Tubes, Catheters and Drains</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzcxNzYxODE1NDY1MjUw)",	
            "[<b>15. Instruments Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzcyNzYzODM5ODIwMTc3)",	
            "[<b>16. Instruments Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzczNzY1ODY0MTc1MTA0)",	
            "[<b>9. Trasplantation Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzc0NzY3ODg4NTMwMDMx)",	
            "[<b>1. Clinical Examination of Fistulan in Ano</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzc1NzY5OTEyODg0OTU4)",	
            "[<b>2. Modifield Radical Mastectomy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzc2NzcxOTM3MjM5ODg1)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        surgeryp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"surgeryp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"surgeryp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(surgeryp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("radiologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Basics of Radiology Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzc3NzczOTYxNTk0ODEy)",	
            "[<b>2. Basics of Radiology Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzc4Nzc1OTg1OTQ5NzM5)",	
            "[<b>3. Basics of MRi</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzc5Nzc4MDEwMzA0NjY2)",	
            "[<b>4. Intervetional Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzgwNzgwMDM0NjU5NTkz)",	
            "[<b>5. Radiation Units, Protectionn, Dose Limits and Hazards</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzgxNzgyMDU5MDE0NTIw)",	
            "[<b>6. Contrast Media</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzgyNzg0MDgzMzY5NDQ3)",	
            "[<b>1. Respiratory Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzgzNzg2MTA3NzI0Mzc0)",	
            "[<b>2. CVS Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzg0Nzg4MTMyMDc5MzAx)",	
            "[<b>1. Neuroradiology Part-1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzg1NzkwMTU2NDM0MjI4)",	
            "[<b>2. Neuroradiology Part-2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzg2NzkyMTgwNzg5MTU1)",	
            "[<b>3. Head and Neck Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzg3Nzk0MjA1MTQ0MDgy)",	
            "[<b>1. GIT</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzg4Nzk2MjI5NDk5MDA5)",	
            "[<b>1. Hepatobiliary and Pancreatic Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzg5Nzk4MjUzODUzOTM2)",	
            "[<b>1. Genitourinary Radiology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzkwODAwMjc4MjA4ODYz)",	
            "[<b>1. OBGy Imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzkxODAyMzAyNTYzNzkw)",	
            "[<b>2. Breast Imaging</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzkyODA0MzI2OTE4NzE3)",	
            "[<b>1. MSK</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzkzODA2MzUxMjczNjQ0)",	
            "[<b>1. nuclear Medicine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzk0ODA4Mzc1NjI4NTcx)",	
            "[<b>1. Radiotherapy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzk1ODEwMzk5OTgzNDk4)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        radiologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"radiologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"radiologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(radiologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("anesthesiap"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Introduction to Anesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzk2ODEyNDI0MzM4NDI1)",	
            "[<b>2. History and Stages of Anesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzk3ODE0NDQ4NjkzMzUy)",	
            "[<b>1. Preanesthetic Evalution</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzk4ODE2NDczMDQ4Mjc5)",	
            "[<b>1. Oxygen Therapy and Airway</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwNzk5ODE4NDk3NDAzMjA2)",	
            "[<b>2. Airway Devices</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODAwODIwNTIxNzU4MTMz)",	
            "[<b>1. Anesthesia Machine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODAxODIyNTQ2MTEzMDYw)",	
            "[<b>1. Anesthesia Circuit</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODAyODI0NTcwNDY3OTg3)",	
            "[<b>1. Monitoring in Anaesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODAzODI2NTk0ODIyOTE0)",	
            "[<b>1. Modes of Ventilation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODA0ODI4NjE5MTc3ODQx)",	
            "[<b>1. Inhalational Anesthetic Agents</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODA1ODMwNjQzNTMyNzY4)",	
            "[<b>1. Intravenous Anesthetic Agents</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODA2ODMyNjY3ODg3Njk1)",	
            "[<b>1. Neuromuscular Blocker</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODA3ODM0NjkyMjQyNjIy)",	
            "[<b>1. Regional Anesthesia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODA4ODM2NzE2NTk3NTQ5)",	
            "[<b>1. Fluid Therapy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODA5ODM4NzQwOTUyNDc2)",	
            "[<b>1. Discharge Scoring System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODEwODQwNzY1MzA3NDAz)",	
            "[<b>1. BLS and ACLS Protocol</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODExODQyNzg5NjYyMzMw)",	
            "[<b>1. Brain Death</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODEyODQ0ODE0MDE3MjU3)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anesthesiap_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anesthesiap_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anesthesiap_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anesthesiap_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psychiatryp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Basics of Psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODEzODQ2ODM4MzcyMTg0)",
            "[<b>1. Schizophrenia other Psychotic Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODE0ODQ4ODYyNzI3MTEx)",
            "[<b>1. Mood DIsorder</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODE1ODUwODg3MDgyMDM4)",
            "[<b>1. Neurotic Stress Related Somatoform Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODE2ODUyOTExNDM2OTY1)",
            "[<b>2. Trauma and Stressor Related Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODE3ODU0OTM1NzkxODky)",
            "[<b>3. Dissocaitive Disorders Conversion Disorder Somatic Symptoms and Related Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODE4ODU2OTYwMTQ2ODE5)",
            "[<b>1. Substance Use Addictive Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODE5ODU4OTg0NTAxNzQ2)",
            "[<b>1. Child Psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODIwODYxMDA4ODU2Njcz)",
            "[<b>1. Organic Mental Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODIxODYzMDMzMjExNjAw)",
            "[<b>1. Sleep Disorder</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODIyODY1MDU3NTY2NTI3)",
            "[<b>1. Sexual Disorder</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODIzODY3MDgxOTIxNDU0)",
            "[<b>1. Eating Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODI0ODY5MTA2Mjc2Mzgx)",
            "[<b>1. Personality Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODI1ODcxMTMwNjMxMzA4)",
            "[<b>1. Forensic Psychiatry</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODI2ODczMTU0OTg2MjM1)",
            "[<b>13. Psychology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODI3ODc1MTc5MzQxMTYy)",
            "[<b>1. Electro Convulsive Therapy(Miscellaneous Topics)</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODI4ODc3MjAzNjk2MDg5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psychiatryp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psychiatryp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psychiatryp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psychiatryp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("orthopedicsp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Introduction to Orthopedics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODI5ODc5MjI4MDUxMDE2)",
            "[<b>2. Xray Diagnosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODMwODgxMjUyNDA1OTQz)",
            "[<b>1. Osteomyelitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODMxODgzMjc2NzYwODcw)",
            "[<b>2. Chronic Ostheomyelitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODMyODg1MzAxMTE1Nzk3)",
            "[<b>3. Special Type of Ostheomyelitis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODMzODg3MzI1NDcwNzI0)",
            "[<b>4. Osteochondritis and Ostheonecrosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODM0ODg5MzQ5ODI1NjUx)",
            "[<b>1. Tuberculosis of Bone</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODM1ODkxMzc0MTgwNTc4)",
            "[<b>1. Bone Tumours Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODM2ODkzMzk4NTM1NTA1)",
            "[<b>2. Bone Tumours Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODM3ODk1NDIyODkwNDMy)",
            "[<b>1. Peripheral Nerve Injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODM4ODk3NDQ3MjQ1MzU5)",
            "[<b>1. Upper Limb Trauma Part 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODM5ODk5NDcxNjAwMjg2)",
            "[<b>2.  Upper Limb Trauma Part 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQwOTAxNDk1OTU1MjEz)",
            "[<b>1. Fracture Neck of Femur</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQxOTAzNTIwMzEwMTQw)",
            "[<b>2. Hip Dislocation</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQyOTA1NTQ0NjY1MDY3)",
            "[<b>1. Open Fractures and it's Complications</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQzOTA3NTY5MDE5OTk0)",
            "[<b>2. Volkmann's Ischemia</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQ0OTA5NTkzMzc0OTIx)",
            "[<b>1. Metabolic Bone Disorder</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQ1OTExNjE3NzI5ODQ4)",
            "[<b>1. Rheumatoid Arthritis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQ2OTEzNjQyMDg0Nzc1)",
            "[<b>2. Osteoarthritis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQ3OTE1NjY2NDM5NzAy)",
            "[<b>1. Sports Injuries</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQ4OTE3NjkwNzk0NjI5)",
            "[<b>1. CTEV and CDH</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODQ5OTE5NzE1MTQ5NTU2)",
            "[<b>1. Miscellaneous Topics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODUwOTIxNzM5NTA0NDgz)",
            "[<b>2. Slipped Capital Femoral Epiphysis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODUxOTIzNzYzODU5NDEw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        orthopedicsp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"orthopedicsp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"orthopedicsp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(orthopedicsp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("dermatologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Basics of Dermatology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODUyOTI1Nzg4MjE0MzM3)",	
            "[<b>2. Skin Lesions in Dermatology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODUzOTI3ODEyNTY5MjY0)",	
            "[<b>1. Bacterial Infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODU0OTI5ODM2OTI0MTkx)",	
            "[<b>2. Fungal Infections</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODU1OTMxODYxMjc5MTE4)",	
            "[<b>3. Viral Infections of Skin</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODU2OTMzODg1NjM0MDQ1)",	
            "[<b>4. Parasitic Infestations</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODU3OTM1OTA5OTg4OTcy)",	
            "[<b>1. Cutaneous Tuberculosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODU4OTM3OTM0MzQzODk5)",	
            "[<b>2. Leprosy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODU5OTM5OTU4Njk4ODI2)",	
            "[<b>1. Immunobullous Disorders and Skin Structure</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODYwOTQxOTgzMDUzNzUz)",	
            "[<b>1.  Papulosqaumous Disorders Psoriasis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODYxOTQ0MDA3NDA4Njgw)",	
            "[<b>2. Lichen Planus</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODYyOTQ2MDMxNzYzNjA3)",	
            "[<b>1. Hair Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODYzOTQ4MDU2MTE4NTM0)",	
            "[<b>2. Nail Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODY0OTUwMDgwNDczNDYx)",	
            "[<b>3. Disorders of Glands</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODY1OTUyMTA0ODI4Mzg4)",	
            "[<b>1. Genital Ulcer Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODY2OTU0MTI5MTgzMzE1)",	
            "[<b>2. STD Discharge</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODY3OTU2MTUzNTM4MjQy)",	
            "[<b>1. Eczema</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODY4OTU4MTc3ODkzMTY5)",	
            "[<b>1. Pigmentary Disorders</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODY5OTYwMjAyMjQ4MDk2)",	
            "[<b>1. Connective Tissue Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODcwOTYyMjI2NjAzMDIz)",	
            "[<b>1. Skin Tumors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODcxOTY0MjUwOTU3OTUw)",	
            "[<b>1. Systemic Diseases Skin</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODcyOTY2Mjc1MzEyODc3)",	
            "[<b>1. Adverse Cutaneous Drug Reaction</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODczOTY4Mjk5NjY3ODA0)",	
            "[<b>2. Pediatric Dermatoses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODc0OTcwMzI0MDIyNzMx)",	
            "[<b>3. Urticaria and Angioedema</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODc1OTcyMzQ4Mzc3NjU4)",	
            "[<b>4. Genodermatoses</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODc2OTc0MzcyNzMyNTg1)",	
            "[<b>5. Vector Borne Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODc3OTc2Mzk3MDg3NTEy)",	
            "[<b>6. Bedside Tests in Dermatology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEwODc4OTc4NDIxNDQyNDM5)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        dermatologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"dermatologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"dermatologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(dermatologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("rapidrevisionp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Embryology Histology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTI0NDc0Mzg4Mzk5NTU0)",	
            "[<b>2.  Neuroanatomy Head Neck part -1 .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTI1NDc2NDEyNzU0NDgx)",	
            "[<b>3.Neuroanatomy_Head_Neck part -2 .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTI2NDc4NDM3MTA5NDA4)",	
            "[<b>4.  Back Thorax.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTI3NDgwNDYxNDY0MzM1)",	
            "[<b>5. Upper Limb Lower Limb.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTI4NDgyNDg1ODE5MjYy)",	
            "[<b>6.  Abdomen Pelvis Perineum.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTI5NDg0NTEwMTc0MTg5)",	
            "[<b>7. Anatomy Image discussion Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTMwNDg2NTM0NTI5MTE2)",	
            "[<b>8. Anatomy Image discussion Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTMxNDg4NTU4ODg0MDQz)",	
            "[<b>9. Image Based Discussion Part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTMyNDkwNTgzMjM4OTcw)",	
            "[<b>10. Image Based Discussion Part 4.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTMzNDkyNjA3NTkzODk3)",	
            "[<b>1. Neurophysiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTM0NDk0NjMxOTQ4ODI0)",	
            "[<b>2. General Physiology and Git.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTM1NDk2NjU2MzAzNzUx)",	
            "[<b>3. Cardiovascular System.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTM2NDk4NjgwNjU4Njc4)",	
            "[<b>4. Renal Physiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTM3NTAwNzA1MDEzNjA1)",	
            "[<b>5. Endocrine Reproductive.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTM4NTAyNzI5MzY4NTMy)",	
            "[<b>6. Respiratory Physiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTM5NTA0NzUzNzIzNDU5)",	
            "[<b>7. Physiology Image Vased Discussion Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQwNTA2Nzc4MDc4Mzg2)",	
            "[<b>8. Physiology Image Based Discussion Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQxNTA4ODAyNDMzMzEz)",	
            "[<b>1. Integration of Metabolism.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQyNTEwODI2Nzg4MjQw)",	
            "[<b>2. Carbohydrate Chemistry Metabolism.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQzNTEyODUxMTQzMTY3)",	
            "[<b>3. Lipid Chemistry & Metabolism Or Heme Synthesis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQ0NTE0ODc1NDk4MDk0)",	
            "[<b>4. ABG Interpretation.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQ1NTE2ODk5ODUzMDIx)",	
            "[<b>5. Aminoacid and Proteins.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQ2NTE4OTI0MjA3OTQ4)",	
            "[<b>6. Genetics.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQ3NTIwOTQ4NTYyODc1)",	
            "[<b>1. Cell Injury and Inflammation.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQ4NTIyOTcyOTE3ODAy)",	
            "[<b>2. Genetics, Neoplasia & Immunity.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTQ5NTI0OTk3MjcyNzI5)",	
            "[<b>3. Systemic Pathology Part - 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTUwNTI3MDIxNjI3NjU2)",	
            "[<b>4. Systemic Pathology Part - 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTUxNTI5MDQ1OTgyNTgz)",	
            "[<b>5. Hemathology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTUyNTMxMDcwMzM3NTEw)",	
            "[<b>6. Renal Pathology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTUzNTMzMDk0NjkyNDM3)",	
            "[<b>7. Endocrine Patholog.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTU0NTM1MTE5MDQ3MzY0)",	
            "[<b>8. Pathology Image Discussion Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTU1NTM3MTQzNDAyMjkx)",	
            "[<b>9. Pathology Image Discussion Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTU2NTM5MTY3NzU3MjE4)",	
            "[<b>1. General & ANS Pharmacology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTU3NTQxMTkyMTEyMTQ1)",	
            "[<b>2. Renal CVS & CNS Pharmacolony.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTU4NTQzMjE2NDY3MDcy)",	
            "[<b>3. Anti-Microbials, Endocrine & GIT.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTU5NTQ1MjQwODIxOTk5)",	
            "[<b>4. Autacoids, Blood, Anti-Cancer, Immunosuppressant.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTYwNTQ3MjY1MTc2OTI2)",	
            "[<b>5. Pharmacology Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTYxNTQ5Mjg5NTMxODUz)",	
            "[<b>1. General Microbiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTYyNTUxMzEzODg2Nzgw)",	
            "[<b>2. Mycology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTYzNTUzMzM4MjQxNzA3)",	
            "[<b>3. Bacteriology Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTY0NTU1MzYyNTk2NjM0)",	
            "[<b>4. Bacteriology Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTY1NTU3Mzg2OTUxNTYx)",	
            "[<b>5. Virology Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTY2NTU5NDExMzA2NDg4)",	
            "[<b>6. Virology Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTY3NTYxNDM1NjYxNDE1)",	
            "[<b>7. Parasitology Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTY4NTYzNDYwMDE2MzQy)",	
            "[<b>8. Parasitology Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTY5NTY1NDg0MzcxMjY5)",	
            "[<b>9. Immunology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTcwNTY3NTA4NzI2MTk2)",	
            "[<b>1. Forensic MEdicine Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTcxNTY5NTMzMDgxMTIz)",	
            "[<b>2. Forensic Medicine Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTcyNTcxNTU3NDM2MDUw)",	
            "[<b>3. Forensic Medicine Part-3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTczNTczNTgxNzkwOTc3)",	
            "[<b>4. Forensic Medicine Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTc0NTc1NjA2MTQ1OTA0)",	
            "[<b>1. Epidemiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTc1NTc3NjMwNTAwODMx)",	
            "[<b>2. Nutrition & Health  social and Health.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTc2NTc5NjU0ODU1NzU4)",	
            "[<b>3. Health care system in india.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTc3NTgxNjc5MjEwNjg1)",	
            "[<b>4. Environment & Health.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTc4NTgzNzAzNTY1NjEy)",	
            "[<b>5. Demography & Health.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTc5NTg1NzI3OTIwNTM5)",	
            "[<b>6. Communicable Disease.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTgwNTg3NzUyMjc1NDY2)",	
            "[<b>7. Biostatistics.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTgxNTg5Nzc2NjMwMzkz)",	
            "[<b>8. National Health Programs.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTgyNTkxODAwOTg1MzIw)",	
            "[<b>9. Allied Health Disciplines.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTgzNTkzODI1MzQwMjQ3)",	
            "[<b>10. PSm Image Discussion Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTg0NTk1ODQ5Njk1MTc0)",	
            "[<b>1. Ear Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTg1NTk3ODc0MDUwMTAx)",	
            "[<b>2. Ear Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTg2NTk5ODk4NDA1MDI4)",	
            "[<b>3. Nose.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTg3NjAxOTIyNzU5OTU1)",	
            "[<b>4. Pharynx.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTg4NjAzOTQ3MTE0ODgy)",	
            "[<b>5. Lartnx.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTg5NjA1OTcxNDY5ODA5)",	
            "[<b>6. ENT Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTkwNjA3OTk1ODI0NzM2)",	
            "[<b>1. Opththalmology Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTkxNjEwMDIwMTc5NjYz)",	
            "[<b>2. Opththalmology Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTkyNjEyMDQ0NTM0NTkw)",	
            "[<b>3. Ophthamology Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTkzNjE0MDY4ODg5NTE3)",	
            "[<b>1. Obstetrics Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTk0NjE2MDkzMjQ0NDQ0)",	
            "[<b>2. Obstetrics Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTk1NjE4MTE3NTk5Mzcx)",	
            "[<b>3. Obstetrics Part-3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTk2NjIwMTQxOTU0Mjk4)",	
            "[<b>4. Obstetrics Part-4.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTk3NjIyMTY2MzA5MjI1)",	
            "[<b>5. Gynaecology Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTk4NjI0MTkwNjY0MTUy)",	
            "[<b>6. Gynaecology Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMTk5NjI2MjE1MDE5MDc5)",	
            "[<b>7. Obstetrics and Gynaecology Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjAwNjI4MjM5Mzc0MDA2)",	
            "[<b>1. General Pediatrics.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjAxNjMwMjYzNzI4OTMz)",	
            "[<b>2. Neonatology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjAyNjMyMjg4MDgzODYw)",	
            "[<b>3.Systemic Pediatrics.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjAzNjM0MzEyNDM4Nzg3)",	
            "[<b>4. Pediatrics Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjA0NjM2MzM2NzkzNzE0)",	
            "[<b>4. Dermatology Image Discussion .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjA1NjM4MzYxMTQ4NjQx)",	
            "[<b>1. General Surgery PArt1A.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjA2NjQwMzg1NTAzNTY4)",	
            "[<b>2. General Surgery Part1B.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjA3NjQyNDA5ODU4NDk1)",	
            "[<b>3.General Surgery Part2-A.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjA4NjQ0NDM0MjEzNDIy)",	
            "[<b>4.General Surgery Part2-B.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjA5NjQ2NDU4NTY4MzQ5)",	
            "[<b>5. Hepatobiliary Pancreatic Surgery.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjEwNjQ4NDgyOTIzMjc2)",	
            "[<b>6. GIT Part-1 (Esophagus,Stomach,Peritoneum).mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjExNjUwNTA3Mjc4MjAz)",	
            "[<b>7. GIT Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjEyNjUyNTMxNjMzMTMw)",	
            "[<b>8. Git Part-3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjEzNjU0NTU1OTg4MDU3)",	
            "[<b>9. Surgery image Discussion Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjE0NjU2NTgwMzQyOTg0)",	
            "[<b>10. Surgery image Discussion Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjE1NjU4NjA0Njk3OTEx)",	
            "[<b>11. Surgery image Discussion Part-3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjE2NjYwNjI5MDUyODM4)",	
            "[<b>1. Cardiology Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjE3NjYyNjUzNDA3NzY1)",	
            "[<b>2. Cardiology Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjE4NjY0Njc3NzYyNjky)",	
            "[<b>3. Cardiology Part-3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjE5NjY2NzAyMTE3NjE5)",	
            "[<b>4. Rheumatology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjIwNjY4NzI2NDcyNTQ2)",	
            "[<b>5. Neurology Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjIxNjcwNzUwODI3NDcz)",	
            "[<b>6. Neurology Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjIyNjcyNzc1MTgyNDAw)",	
            "[<b>7. Neurology Part 3 Endocrinology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjIzNjc0Nzk5NTM3MzI3)",	
            "[<b>8. Kidney.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjI0Njc2ODIzODkyMjU0)",	
            "[<b>9. Respiratory System.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjI1Njc4ODQ4MjQ3MTgx)",	
            "[<b>10. Liver, Git & Hematology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjI2NjgwODcyNjAyMTA4)",	
            "[<b>11. Medical Image Discussion Part-1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjI3NjgyODk2OTU3MDM1)",	
            "[<b>12. Medical Image Discussion Part-2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjI4Njg0OTIxMzExOTYy)",	
            "[<b>1. Radiology Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjI5Njg2OTQ1NjY2ODg5)",	
            "[<b>2. Radiology Part 2 .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjMwNjg4OTcwMDIxODE2)",	
            "[<b>3. Radiology Part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjMxNjkwOTk0Mzc2NzQz)",	
            "[<b>4. Radiology Image Discussion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjMyNjkzMDE4NzMxNjcw)",	
            "[<b>1. Anesthesia Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjMzNjk1MDQzMDg2NTk3)",	
            "[<b>2.  Anesthesia Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjM0Njk3MDY3NDQxNTI0)",	
            "[<b>3. Anesthesia Part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjM1Njk5MDkxNzk2NDUx)",	
            "[<b>1. Orthopedics Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjM2NzAxMTE2MTUxMzc4)",	
            "[<b>2. Orthopedics Part 2 .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjM3NzAzMTQwNTA2MzA1)",	
            "[<b>3. Orthopedics Part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjM4NzA1MTY0ODYxMjMy)",	
            "[<b>1. Psychiatry Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjM5NzA3MTg5MjE2MTU5)",	
            "[<b>2. Psychiatry Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQwNzA5MjEzNTcxMDg2)",	
            "[<b>3. Image Based Discussion Psychiatry.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQxNzExMjM3OTI2MDEz)",	
            "[<b>1. Dermatology Part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQyNzEzMjYyMjgwOTQw)",	
            "[<b>2. Dermatology Part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQzNzE1Mjg2NjM1ODY3)",	
            "[<b>3. Dermatology Part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQ0NzE3MzEwOTkwNzk0)",	
            "[<b>4. Dermatology Image Discussion .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQ1NzE5MzM1MzQ1NzIx)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        rapidrevisionp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"rapidrevisionp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"rapidrevisionp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(rapidrevisionp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("microbiologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. General Microbiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQ2NzIxMzU5NzAwNjQ4)",
            "[<b>2. General Microbiology Microscopes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQ3NzIzMzg0MDU1NTc1)",
            "[<b>3. General Microbiology Bacterial Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQ4NzI1NDA4NDEwNTAy)",
            "[<b>4. General Microbiology Bacterial Shapes and Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjQ5NzI3NDMyNzY1NDI5)",
            "[<b>5. General Microbiology Bacterial Genetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjUwNzI5NDU3MTIwMzU2)",
            "[<b>6. General Microbiology Culture Media atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjUxNzMxNDgxNDc1Mjgz)",
            "[<b>7. General Microbiology Sterilization and Disinfection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjUyNzMzNTA1ODMwMjEw)",
            "[<b>8. Staphylococcaceae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjUzNzM1NTMwMTg1MTM3)",
            "[<b>9. Streptococcaceae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjU0NzM3NTU0NTQwMDY0)",
            "[<b>10. Neisseria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjU1NzM5NTc4ODk0OTkx)",
            "[<b>11. Gram Positive Bacilli Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjU2NzQxNjAzMjQ5OTE4)",
            "[<b>12. Gram Positive Bacilli Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjU3NzQzNjI3NjA0ODQ1)",
            "[<b>13. Gram Positive Bacteria Part 3 Mycobacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjU4NzQ1NjUxOTU5Nzcy)",
            "[<b>14. Gram Negative Bacteria Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjU5NzQ3Njc2MzE0Njk5)",
            "[<b>15. Gram Negative Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjYwNzQ5NzAwNjY5NjI2)",
            "[<b>16. Bacteriology Vibrio and Non Fermenters atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjYxNzUxNzI1MDI0NTUz)",
            "[<b>17. Bacteriology Hbb 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjYyNzUzNzQ5Mzc5NDgw)",
            "[<b>18. Bacteriology Spirochetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjYzNzU1NzczNzM0NDA3)",
            "[<b>19. Bacteriology Rickettsiae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjY0NzU3Nzk4MDg5MzM0)",
            "[<b>20. Bacteriology Chlamydia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjY1NzU5ODIyNDQ0MjYx)",
            "[<b>21. Miscellaneous Bacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjY2NzYxODQ2Nzk5MTg4)",
            "[<b>22. Virology General Properties atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjY3NzYzODcxMTU0MTE1)",
            "[<b>23. Dna Virology Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjY4NzY1ODk1NTA5MDQy)",
            "[<b>24. Dna Virology Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjY5NzY3OTE5ODYzOTY5)",
            "[<b>25. Dna Virology Hepatitis Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjcwNzY5OTQ0MjE4ODk2)",
            "[<b>26. Virology Rna Myxovirus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjcxNzcxOTY4NTczODIz)",
            "[<b>27. Virology Rna Picornaviridae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjcyNzczOTkyOTI4NzUw)",
            "[<b>28. Virology Rna Rhabdovirus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjczNzc2MDE3MjgzNjc3)",
            "[<b>29. Rna Virology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjc0Nzc4MDQxNjM4NjA0)",
            "[<b>30. Retrovirus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjc1NzgwMDY1OTkzNTMx)",
            "[<b>31. Virology Other Rna Viruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjc2NzgyMDkwMzQ4NDU4)",
            "[<b>32. Covid 19 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjc3Nzg0MTE0NzAzMzg1)",
            "[<b>33. Mycology Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjc4Nzg2MTM5MDU4MzEy)",
            "[<b>34. Mycology Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjc5Nzg4MTYzNDEzMjM5)",
            "[<b>35. Parasitology Classification Amoeba atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjgwNzkwMTg3NzY4MTY2)",
            "[<b>36. Parasitology Flagellates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjgxNzkyMjEyMTIzMDkz)",
            "[<b>37. Parasitology Hemoflagellates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjgyNzk0MjM2NDc4MDIw)",
            "[<b>38. Parasitology Coccidian Parasites atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjgzNzk2MjYwODMyOTQ3)",
            "[<b>39. Plasmodium and Babesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjg0Nzk4Mjg1MTg3ODc0)",
            "[<b>40. Cestodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjg1ODAwMzA5NTQyODAx)",
            "[<b>41. Trematodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjg2ODAyMzMzODk3NzI4)",
            "[<b>42. Nematodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjg3ODA0MzU4MjUyNjU1)",
            "[<b>43. Immunity Introduction Activation of Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjg4ODA2MzgyNjA3NTgy)",
            "[<b>44. Types of Hypersensitivity Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjg5ODA4NDA2OTYyNTA5)",
            "[<b>45. Immunity Tolerance Autoimmune Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjkwODEwNDMxMzE3NDM2)",
            "[<b>46. Immunodeficiency Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjkxODEyNDU1NjcyMzYz)",
            "[<b>47. Transplant Immunology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjkyODE0NDgwMDI3Mjkw)",
            "[<b>48. Immunity Antigen and Antibody atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjkzODE2NTA0MzgyMjE3)",
            "[<b>49. Immunity Antigen Antibody Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjk0ODE4NTI4NzM3MTQ0)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        microbiologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"microbiologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"microbiologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(microbiologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pathologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Cell Injury Introduction Necrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjk1ODIwNTUzMDkyMDcx)",
            "[<b>2. Cell Injury Newer Cell Deaths atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjk2ODIyNTc3NDQ2OTk4)",
            "[<b>3. Intracellular Accumulations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjk3ODI0NjAxODAxOTI1)",
            "[<b>4. Autophagy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjk4ODI2NjI2MTU2ODUy)",
            "[<b>5. Inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMjk5ODI4NjUwNTExNzc5)",
            "[<b>6. Inflammation Mediators atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzAwODMwNjc0ODY2NzA2)",
            "[<b>7. Chronic Inflammation Granuloma and Wound Healing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzAxODMyNjk5MjIxNjMz)",
            "[<b>8. Genetics Indroduction and Mendelian Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzAyODM0NzIzNTc2NTYw)",
            "[<b>9. Genetics Non Mendelian and Chromosomal Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzAzODM2NzQ3OTMxNDg3)",
            "[<b>10. Genetics Diagnosis of Genetic Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzA0ODM4NzcyMjg2NDE0)",
            "[<b>11. Genetics Miscellaneous Concepts in Genetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzA1ODQwNzk2NjQxMzQx)",
            "[<b>12. Classification of Neoplasms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzA2ODQyODIwOTk2MjY4)",
            "[<b>13. Features of Neoplasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzA3ODQ0ODQ1MzUxMTk1)",
            "[<b>14. Fundamental of Neoplasia Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzA4ODQ2ODY5NzA2MTIy)",
            "[<b>15. Fundamental of Neoplasia Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzA5ODQ4ODk0MDYxMDQ5)",
            "[<b>16. Etiology of Neoplasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzEwODUwOTE4NDE1OTc2)",
            "[<b>17. Diagnosis of Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzExODUyOTQyNzcwOTAz)",
            "[<b>18. Immunity Introduction Activation of Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzEyODU0OTY3MTI1ODMw)",
            "[<b>19. Types of Hypersensitivity Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzEzODU2OTkxNDgwNzU3)",
            "[<b>20. Immunity Tolerance Autoimmune Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzE0ODU5MDE1ODM1Njg0)",
            "[<b>21. Immunodeficiency Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzE1ODYxMDQwMTkwNjEx)",
            "[<b>22. Transplant Immunology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzE2ODYzMDY0NTQ1NTM4)",
            "[<b>23. Amyloidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzE3ODY1MDg4OTAwNDY1)",
            "[<b>24. Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzE4ODY3MTEzMjU1Mzky)",
            "[<b>25. Cardiac Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzE5ODY5MTM3NjEwMzE5)",
            "[<b>26. Carditis and Cardiac Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzIwODcxMTYxOTY1MjQ2)",
            "[<b>27. Lung Pathology Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzIxODczMTg2MzIwMTcz)",
            "[<b>28. Lung Pathology Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzIyODc1MjEwNjc1MTAw)",
            "[<b>29. Salivary Gland atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzIzODc3MjM1MDMwMDI3)",
            "[<b>30. Git Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzI0ODc5MjU5Mzg0OTU0)",
            "[<b>31. Git Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzI1ODgxMjgzNzM5ODgx)",
            "[<b>32. Hepatobiliaryology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzI2ODgzMzA4MDk0ODA4)",
            "[<b>33. Cirrhosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzI3ODg1MzMyNDQ5NzM1)",
            "[<b>34. Renal Pathology Introduction and Spotters atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzI4ODg3MzU2ODA0NjYy)",
            "[<b>35. Renal Pathology Nephritic and Nephrotic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzI5ODg5MzgxMTU5NTg5)",
            "[<b>36. Renal Pathology Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzMwODkxNDA1NTE0NTE2)",
            "[<b>37. Pathology of Female Genital atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzMxODkzNDI5ODY5NDQz)",
            "[<b>38. Pathology of Male Genital atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzMyODk1NDU0MjI0Mzcw)",
            "[<b>39. Breast Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzMzODk3NDc4NTc5Mjk3)",
            "[<b>40. Breast Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzM0ODk5NTAyOTM0MjI0)",
            "[<b>41. Central Nervous System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzM1OTAxNTI3Mjg5MTUx)",
            "[<b>42. Brain Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzM2OTAzNTUxNjQ0MDc4)",
            "[<b>43. Thyroid Gland Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzM3OTA1NTc1OTk5MDA1)",
            "[<b>44. Endocrineology Parathyroid Gland atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzM4OTA3NjAwMzUzOTMy)",
            "[<b>45. Bone and Soft Tissue Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzM5OTA5NjI0NzA4ODU5)",
            "[<b>46. Dermatology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQwOTExNjQ5MDYzNzg2)",
            "[<b>47. Hematology Inroduction Erythropoiesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQxOTEzNjczNDE4NzEz)",
            "[<b>48. Microcytic Hypochromic Anaemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQyOTE1Njk3NzczNjQw)",
            "[<b>49. Macrocytic Anaemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQzOTE3NzIyMTI4NTY3)",
            "[<b>50. Hemolytic Anemias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQ0OTE5NzQ2NDgzNDk0)",
            "[<b>51. Sickle Cell Anaemia Thalasemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQ1OTIxNzcwODM4NDIx)",
            "[<b>52. Auto Immune Hemolytic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQ2OTIzNzk1MTkzMzQ4)",
            "[<b>53. Rbc Shapes Inclusions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQ3OTI1ODE5NTQ4Mjc1)",
            "[<b>54. Basics of Wbc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQ4OTI3ODQzOTAzMjAy)",
            "[<b>55. Leukemia and Lymphoma Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzQ5OTI5ODY4MjU4MTI5)",
            "[<b>56. Leukemia and Lymphoma Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzUwOTMxODkyNjEzMDU2)",
            "[<b>57. Leukemia and Lymphoma Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzUxOTMzOTE2OTY3OTgz)",
            "[<b>58. Chronic Myeloproliferative Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzUyOTM1OTQxMzIyOTEw)",
            "[<b>59. Plasma Cell Dyscrasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzUzOTM3OTY1Njc3ODM3)",
            "[<b>60. Flow Cytometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzU0OTM5OTkwMDMyNzY0)",
            "[<b>61. Platelet Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzU1OTQyMDE0Mzg3Njkx)",
            "[<b>62. Platelet Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzU2OTQ0MDM4NzQyNjE4)",
            "[<b>63. Blood Banking and Transfusion Medicine Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzU3OTQ2MDYzMDk3NTQ1)",
            "[<b>64. Blood Banking and Transfusion Medicine Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzU4OTQ4MDg3NDUyNDcy)",
            "[<b>65. Tissue Processing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzU5OTUwMTExODA3Mzk5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pathologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pathologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pathologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pathologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("ophthalmologyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Address to Students atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzYwOTUyMTM2MTYyMzI2)",
            "[<b>2. Introuction to Opthalmology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzYxOTU0MTYwNTE3MjUz)",
            "[<b>3. Lens Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzYyOTU2MTg0ODcyMTgw)",
            "[<b>4. Complication of Cataract Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzYzOTU4MjA5MjI3MTA3)",
            "[<b>5. Lasers in Eye atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzY0OTYwMjMzNTgyMDM0)",
            "[<b>6. Glaucoma Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzY1OTYyMjU3OTM2OTYx)",
            "[<b>7. Glaucoma Part 2  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzY2OTY0MjgyMjkxODg4)",
            "[<b>8. Glaucoma Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzY3OTY2MzA2NjQ2ODE1)",
            "[<b>9. Glaucoma Part 4 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzY4OTY4MzMxMDAxNzQy)",
            "[<b>10. Laser Treatment in Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzY5OTcwMzU1MzU2NjY5)",
            "[<b>11. Cornea Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzcwOTcyMzc5NzExNTk2)",
            "[<b>12. Cornea Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzcxOTc0NDA0MDY2NTIz)",
            "[<b>13. Sclera atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzcyOTc2NDI4NDIxNDUw)",
            "[<b>14. Uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzczOTc4NDUyNzc2Mzc3)",
            "[<b>15. Neuro Ophthalmology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzc0OTgwNDc3MTMxMzA0)",
            "[<b>16. Conjunctiva atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzc1OTgyNTAxNDg2MjMx)",
            "[<b>17. Allergic Conjunctiva atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzc2OTg0NTI1ODQxMTU4)",
            "[<b>18. Lacrimal Drainage System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzc3OTg2NTUwMTk2MDg1)",
            "[<b>19. Orbit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzc4OTg4NTc0NTUxMDEy)",
            "[<b>20. Occluar Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzc5OTkwNTk4OTA1OTM5)",
            "[<b>21. Lids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzgwOTkyNjIzMjYwODY2)",
            "[<b>22. Optics Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzgxOTk0NjQ3NjE1Nzkz)",
            "[<b>23. Optics Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzgyOTk2NjcxOTcwNzIw)",
            "[<b>24. Squint Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzgzOTk4Njk2MzI1NjQ3)",
            "[<b>25. Squint Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzg1MDAwNzIwNjgwNTc0)",
            "[<b>26. Squint Workup atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzg2MDAyNzQ1MDM1NTAx)",
            "[<b>27. Retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzg3MDA0NzY5MzkwNDI4)",
            "[<b>28. Vitreous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzg4MDA2NzkzNzQ1MzU1)",
            "[<b>29. Embryology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzg5MDA4ODE4MTAwMjgy)",
            "[<b>30. Community Ophthalmology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzkwMDEwODQyNDU1MjA5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        ophthalmologyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ophthalmologyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ophthalmologyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ophthalmologyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("obgyp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Menstruation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzkxMDEyODY2ODEwMTM2)",
            "[<b>2. Menstruation Problems Young Small Girls atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzkyMDE0ODkxMTY1MDYz)",
            "[<b>3. Ovarian Hyperstimulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzkzMDE2OTE1NTE5OTkw)",
            "[<b>4. Tests of Ovulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzk0MDE4OTM5ODc0OTE3)",
            "[<b>5. Endometriosis Adenomyosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzk1MDIwOTY0MjI5ODQ0)",
            "[<b>6. Hormone Replacement Therapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzk2MDIyOTg4NTg0Nzcx)",
            "[<b>7. Ovarian Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzk3MDI1MDEyOTM5Njk4)",
            "[<b>8. Polycystic Ovarian Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzk4MDI3MDM3Mjk0NjI1)",
            "[<b>9. Cervical Carcinoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExMzk5MDI5MDYxNjQ5NTUy)",
            "[<b>10. Post Menopausal Bleeding atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDAwMDMxMDg2MDA0NDc5)",
            "[<b>11. Vulvar Carcinoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDAxMDMzMTEwMzU5NDA2)",
            "[<b>12. Fibroids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDAyMDM1MTM0NzE0MzMz)",
            "[<b>13. Hysterectomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDAzMDM3MTU5MDY5MjYw)",
            "[<b>14. Gametogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDA0MDM5MTgzNDI0MTg3)",
            "[<b>15. Mullerian Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDA1MDQxMjA3Nzc5MTE0)",
            "[<b>16. Abnormal Uterine Bleeding Its a Downpour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDA2MDQzMjMyMTM0MDQx)",
            "[<b>17. Intersex She Is Your Brother atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDA3MDQ1MjU2NDg4OTY4)",
            "[<b>18. Pubertal Changes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDA4MDQ3MjgwODQzODk1)",
            "[<b>19. Infertility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDA5MDQ5MzA1MTk4ODIy)",
            "[<b>20. Genital Organ Prolapse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDEwMDUxMzI5NTUzNzQ5)",
            "[<b>21. Urinary Fistula in Obstetrics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDExMDUzMzUzOTA4Njc2)",
            "[<b>22. Emergency Contraceptives atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDEyMDU1Mzc4MjYzNjAz)",
            "[<b>23. Contraception atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDEzMDU3NDAyNjE4NTMw)",
            "[<b>24. Genital Tract Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDE0MDU5NDI2OTczNDU3)",
            "[<b>25. Amenorrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDE1MDYxNDUxMzI4Mzg0)",
            "[<b>26. Clinical Anatomy Female Reproductive Tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDE2MDYzNDc1NjgzMzEx)",
            "[<b>27. Endometrial Carcinoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDE3MDY1NTAwMDM4MjM4)",
            "[<b>28. Covid 19 in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDE4MDY3NTI0MzkzMTY1)",
            "[<b>29. Post Partum Haemorrhage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDE5MDY5NTQ4NzQ4MDky)",
            "[<b>30. Placenta Separation Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDIwMDcxNTczMTAzMDE5)",
            "[<b>31. Placenta Cord Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDIxMDczNTk3NDU3OTQ2)",
            "[<b>32. Rh Isoimmunization atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDIyMDc1NjIxODEyODcz)",
            "[<b>33. Twin Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDIzMDc3NjQ2MTY3ODAw)",
            "[<b>34. Molar Pregnancy Gestational Trophoblastic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDI0MDc5NjcwNTIyNzI3)",
            "[<b>35. Antepartum Hemorrhage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDI1MDgxNjk0ODc3NjU0)",
            "[<b>36. Pregnancy Induced Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDI2MDgzNzE5MjMyNTgx)",
            "[<b>37. Diabetes in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDI3MDg1NzQzNTg3NTA4)",
            "[<b>38. Intrauterine Growth Retardation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDI4MDg3NzY3OTQyNDM1)",
            "[<b>39. Basic Definitions Cardinal Movements Ecv atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDI5MDg5NzkyMjk3MzYy)",
            "[<b>40. Medical Illness Complicating Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDMwMDkxODE2NjUyMjg5)",
            "[<b>41. Parturition Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDMxMDkzODQxMDA3MjE2)",
            "[<b>42. Fetal Skull Maternal Pelvis Important Dimensions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDMyMDk1ODY1MzYyMTQz)",
            "[<b>43. Malpositions Malpresentations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDMzMDk3ODg5NzE3MDcw)",
            "[<b>44. Basics of Instrumental Delivery Methods of Labour Induction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDM0MDk5OTE0MDcxOTk3)",
            "[<b>45. Episiotomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDM1MTAxOTM4NDI2OTI0)",
            "[<b>46. Puerperium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDM2MTAzOTYyNzgxODUx)",
            "[<b>47. Caeserian Section atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDM3MTA1OTg3MTM2Nzc4)",
            "[<b>48. Infection in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDM4MTA4MDExNDkxNzA1)",
            "[<b>49. Ectopic Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDM5MTEwMDM1ODQ2NjMy)",
            "[<b>50. Drugs in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQwMTEyMDYwMjAxNTU5)",
            "[<b>51. Anaemia in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQxMTE0MDg0NTU2NDg2)",
            "[<b>52. Vomiting in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQyMTE2MTA4OTExNDEz)",
            "[<b>53. Abortions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQzMTE4MTMzMjY2MzQw)",
            "[<b>54. Induced Abortions Mtp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQ0MTIwMTU3NjIxMjY3)",
            "[<b>55. Physiological Changes of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQ1MTIyMTgxOTc2MTk0)",
            "[<b>56. Diagnosis of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQ2MTI0MjA2MzMxMTIx)",
            "[<b>57. Prenatal Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQ3MTI2MjMwNjg2MDQ4)",
            "[<b>58. Preterm Labor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQ4MTI4MjU1MDQwOTc1)",
            "[<b>59. Pndt Act atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDQ5MTMwMjc5Mzk1OTAy)",
            "[<b>60. Fetal Circulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDUwMTMyMzAzNzUwODI5)",
            "[<b>61. Amniotic Fluid Dynamics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDUxMTM0MzI4MTA1NzU2)",
            "[<b>62. Sterlization Surgeries Tubectomy and Vasectomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDUyMTM2MzUyNDYwNjgz)",
            "[<b>63. Special Cases in Obstetrics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDUzMTM4Mzc2ODE1NjEw)",
            "[<b>64. Liver Disease in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDU0MTQwNDAxMTcwNTM3)",
            "[<b>65. Tuberculosis and Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDU1MTQyNDI1NTI1NDY0)",
            "[<b>66. Antenatal Care in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDU2MTQ0NDQ5ODgwMzkx)",
            "[<b>67. Drugs Used in Obstetrics and Gynaecology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDU3MTQ2NDc0MjM1MzE4)",
            "[<b>68. Instruments in Gynecology and Obstetrics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDU4MTQ4NDk4NTkwMjQ1)",
            "[<b>69. Controversial Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDU5MTUwNTIyOTQ1MTcy)",
            "[<b>70. Common Controversies in Obstetrics Gynaecology Mcqs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDYwMTUyNTQ3MzAwMDk5)",
            "[<b>71. Image Based Questions Obs and Gyne atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDYxMTU0NTcxNjU1MDI2)",
            "[<b>72. Azoospermic Man Gets His Own Biological Child atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDYyMTU2NTk2MDA5OTUz)",
            "[<b>73. From Being a Gamate to Becoming a Human atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDYzMTU4NjIwMzY0ODgw)",
            "[<b>74. Lapro Hysteroscopy for Workup of an Infertile Women atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDY0MTYwNjQ0NzE5ODA3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        obgyp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"obgyp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"obgyp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(obgyp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("clinicalp"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Acute Respiratory Infection Dr. Neha Taneja atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDY1MTYyNjY5MDc0NzM0)",
            "[<b>Antenatal care Dr. Neha Taneja atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDY2MTY0NjkzNDI5NjYx)",
            "[<b>Diarrhoea Dr. Neha Taneja atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDY3MTY2NzE3Nzg0NTg4)",
            "[<b>Hypertension Dr.Neha Taneja atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDY4MTY4NzQyMTM5NTE1)",
            "[<b>Natal Care Dr.Neha Taneja atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDY5MTcwNzY2NDk0NDQy)",
            "[<b>Severe Acute Malnutrition Dr. Neha Taneja atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDcwMTcyNzkwODQ5MzY5)",
            "[<b>CNS examination Dr. Rajat Chauhan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDcxMTc0ODE1MjA0Mjk2)",
            "[<b>General Physical Examination Dr. Rajat Chauhan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDcyMTc2ODM5NTU5MjIz)",
            "[<b>Normal CVS examination Dr. Rajat-Chauhan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDczMTc4ODYzOTE0MTUw)",
            "[<b>Normal GIT Examination Dr. Rajat Chauhan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDc0MTgwODg4MjY5MDc3)",
            "[<b>Respiratory examination Dr. Rajat Chauhan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDc1MTgyOTEyNjI0MDA0)",
            "[<b>Basal Cell Carcinoma Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDc2MTg0OTM2OTc4OTMx)",
            "[<b>Clinical Case Discussion Atopic Dermatitis Re Render  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDc3MTg2OTYxMzMzODU4)",
            "[<b>Clinical Case Discussion Vitiligo Dr. Chesta Aggarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDc4MTg4OTg1Njg4Nzg1)",
            "[<b>Fixed Drug Eruption Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDc5MTkxMDEwMDQzNzEy)",
            "[<b>Herpes Zoster Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDgwMTkzMDM0Mzk4NjM5)",
            "[<b>Kaposi Sarcoma Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDgxMTk1MDU4NzUzNTY2)",
            "[<b>Leprosy Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDgyMTk3MDgzMTA4NDkz)",
            "[<b>Lichen Planus Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDgzMTk5MTA3NDYzNDIw)",
            "[<b>Malignent Melanoma Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDg0MjAxMTMxODE4MzQ3)",
            "[<b>Pemphigus Vulgaris Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDg1MjAzMTU2MTczMjc0)",
            "[<b>Psoriasis Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDg2MjA1MTgwNTI4MjAx)",
            "[<b>Scabies Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDg3MjA3MjA0ODgzMTI4)",
            "[<b>Sjs Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDg4MjA5MjI5MjM4MDU1)",
            "[<b>ASOM Dr. Vyshnavi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDg5MjExMjUzNTkyOTgy)",
            "[<b>Facial Nerve Palsy Dr.Vyshnavi  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDkwMjEzMjc3OTQ3OTA5)",
            "[<b>Tonsillitis Dr.Vyshnavi  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDkxMjE1MzAyMzAyODM2)",
            "[<b>Cataract Dr. Sudha Replace atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDkyMjE3MzI2NjU3NzYz)",
            "[<b>Chronic Dacryocystitis Dr. Sudha  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDkzMjE5MzUxMDEyNjkw)",
            "[<b>Diabetic Retinopathy Dr. Sudha  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDk0MjIxMzc1MzY3NjE3)",
            "[<b>Leucomatous Corneal Opacity Dr. Sudha Replace atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDk1MjIzMzk5NzIyNTQ0)",
            "[<b>Pseudophakia Dr. Sudha  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDk2MjI1NDI0MDc3NDcx)",
            "[<b>Pterygium Dr. Sudha Replace atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDk3MjI3NDQ4NDMyMzk4)",
            "[<b>Third Nerve Palsy Dr. Sudha Replace atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDk4MjI5NDcyNzg3MzI1)",
            "[<b>Vernal Kerato Conjunctivitis Dr. Sudha  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNDk5MjMxNDk3MTQyMjUy)",
            "[<b>Abruptio Placenta Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTAwMjMzNTIxNDk3MTc5)",
            "[<b>Amenorrhea Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTAxMjM1NTQ1ODUyMTA2)",
            "[<b>Anemia in Pregnancy Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTAyMjM3NTcwMjA3MDMz)",
            "[<b>Bad Obg History Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTAzMjM5NTk0NTYxOTYw)",
            "[<b>Breech Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTA0MjQxNjE4OTE2ODg3)",
            "[<b>Case Discusion Rh Incompatibility Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTA1MjQzNjQzMjcxODE0)",
            "[<b>Case Discussio Uterine Prolapase Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTA2MjQ1NjY3NjI2NzQx)",
            "[<b>Contraception Dr. Puni Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTA3MjQ3NjkxOTgxNjY4)",
            "[<b>Diabetes Mellitus in Pregnancy Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTA4MjQ5NzE2MzM2NTk1)",
            "[<b>Drugs in Pregancy Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTA5MjUxNzQwNjkxNTIy)",
            "[<b>Ectopic Pregnency Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTEwMjUzNzY1MDQ2NDQ5)",
            "[<b>Endometriosis Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTExMjU1Nzg5NDAxMzc2)",
            "[<b>Fibroid Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTEyMjU3ODEzNzU2MzAz)",
            "[<b>Heart Diseases in Pregnancy Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTEzMjU5ODM4MTExMjMw)",
            "[<b>IUGR Dr. Punit Bhojani atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTE0MjYxODYyNDY2MTU3)",
            "[<b>Infection Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTE1MjYzODg2ODIxMDg0)",
            "[<b>Infertility Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTE2MjY1OTExMTc2MDEx)",
            "[<b>Menorhagia Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTE3MjY3OTM1NTMwOTM4)",
            "[<b>Molar Pregnancy Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTE4MjY5OTU5ODg1ODY1)",
            "[<b>Neet Pg 1080 Live C a Cervix Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTE5MjcxOTg0MjQwNzky)",
            "[<b>Oligohydramnios Polyhydramnios Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTIwMjc0MDA4NTk1NzE5)",
            "[<b>Ovarian Cancer Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTIxMjc2MDMyOTUwNjQ2)",
            "[<b>PCOS Dr. Punit Bhojani atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTIyMjc4MDU3MzA1NTcz)",
            "[<b>PPH Dr. Punit Bhojani atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTIzMjgwMDgxNjYwNTAw)",
            "[<b>Placenta Previa Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTI0MjgyMTA2MDE1NDI3)",
            "[<b>Post Date Pregnancy Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTI1Mjg0MTMwMzcwMzU0)",
            "[<b>Pre Eclampsia Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTI2Mjg2MTU0NzI1Mjgx)",
            "[<b>Pregnancy With Previous LSCS Dr. Punit Bhojani atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTI3Mjg4MTc5MDgwMjA4)",
            "[<b>Preterm Labor Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTI4MjkwMjAzNDM1MTM1)",
            "[<b>Tuberculosis Dr. Neha Taneja  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTI5MjkyMjI3NzkwMDYy)",
            "[<b>Twin Pregnany Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTMwMjk0MjUyMTQ0OTg5)",
            "[<b>Acute Epiglotitis Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTMxMjk2Mjc2NDk5OTE2)",
            "[<b>Acyanotic Congentinal Heart Disease Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTMyMjk4MzAwODU0ODQz)",
            "[<b>Bronchiolitis Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTMzMzAwMzI1MjA5Nzcw)",
            "[<b>Congenital Diaphragmatic Hernia Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTM0MzAyMzQ5NTY0Njk3)",
            "[<b>Cse Discussion Systic Fibrosis Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTM1MzA0MzczOTE5NjI0)",
            "[<b>Down Syndrome Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTM2MzA2Mzk4Mjc0NTUx)",
            "[<b>Infantile Hypertrophic Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTM3MzA4NDIyNjI5NDc4)",
            "[<b>Kawasaki Disease Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTM4MzEwNDQ2OTg0NDA1)",
            "[<b>Nephrotic Syndrome Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTM5MzEyNDcxMzM5MzMy)",
            "[<b>Neuroblastoma Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQwMzE0NDk1Njk0MjU5)",
            "[<b>New Born Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQxMzE2NTIwMDQ5MTg2)",
            "[<b>Pneumonia Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQyMzE4NTQ0NDA0MTEz)",
            "[<b>Post Infectious Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQzMzIwNTY4NzU5MDQw)",
            "[<b>Respiratory Distress Syndrome Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQ0MzIyNTkzMTEzOTY3)",
            "[<b>Rickets Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQ1MzI0NjE3NDY4ODk0)",
            "[<b>Tettralogy of Fallot Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQ2MzI2NjQxODIzODIx)",
            "[<b>Thalassemia Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQ3MzI4NjY2MTc4NzQ4)",
            "[<b>Wilm's Tumor Dr. Sanjay Khatri atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQ4MzMwNjkwNTMzNjc1)",
            "[<b>Abdominal Mass Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTQ5MzMyNzE0ODg4NjAy)",
            "[<b>Acute Cholecystitis Dr.Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTUwMzM0NzM5MjQzNTI5)",
            "[<b>Appendicitis Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTUxMzM2NzYzNTk4NDU2)",
            "[<b>Benign Prostatic Hyperplasia Dr.Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTUyMzM4Nzg3OTUzMzgz)",
            "[<b>Bleeding per Rectum Dr Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTUzMzQwODEyMzA4MzEw)",
            "[<b>Breast Lump Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTU0MzQyODM2NjYzMjM3)",
            "[<b>Carcinoma Esophagus Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTU1MzQ0ODYxMDE4MTY0)",
            "[<b>Carcinoma Prostate Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTU2MzQ2ODg1MzczMDkx)",
            "[<b>Carcinoma Tongue Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTU3MzQ4OTA5NzI4MDE4)",
            "[<b>Carcinoma of Bladder Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTU4MzUwOTM0MDgyOTQ1)",
            "[<b>Cervical Lymphadenopathy Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTU5MzUyOTU4NDM3ODcy)",
            "[<b>Hepatocellular Carcinoma Dr. Deepak 3 June 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTYwMzU0OTgyNzkyNzk5)",
            "[<b>Inguinal Hernia Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTYxMzU3MDA3MTQ3NzI2)",
            "[<b>Intestinal Obstructon Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTYyMzU5MDMxNTAyNjUz)",
            "[<b>Neet Pg 1080 Live C a Penis Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTYzMzYxMDU1ODU3NTgw)",
            "[<b>Obstructive Jaudice Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTY0MzYzMDgwMjEyNTA3)",
            "[<b>Paraumbilical Hernia Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTY1MzY1MTA0NTY3NDM0)",
            "[<b>Parotid Swelling Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTY2MzY3MTI4OTIyMzYx)",
            "[<b>Peripheral Vascular Disease Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTY3MzY5MTUzMjc3Mjg4)",
            "[<b>Rif Lump Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTY4MzcxMTc3NjMyMjE1)",
            "[<b>Scrotal Swelling Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTY5MzczMjAxOTg3MTQy)",
            "[<b>Soft Tissue Sarcoma Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTcwMzc1MjI2MzQyMDY5)",
            "[<b>Thyroid Swelling Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTcxMzc3MjUwNjk2OTk2)",
            "[<b>Varicose Vein Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTcyMzc5Mjc1MDUxOTIz)",
            "[<b>Acute Ischemic Contracture Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTczMzgxMjk5NDA2ODUw)",
            "[<b>Bony Swelling Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTc0MzgzMzIzNzYxNzc3)",
            "[<b>Carpal Tunnel Syndrome Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTc1Mzg1MzQ4MTE2NzA0)",
            "[<b>Dequervain S Tenosynovitis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTc2Mzg3MzcyNDcxNjMx)",
            "[<b>Knee Synovitis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTc3Mzg5Mzk2ODI2NTU4)",
            "[<b>Malunion Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTc4MzkxNDIxMTgxNDg1)",
            "[<b>Non Union Diaphyseal Fracture Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTc5MzkzNDQ1NTM2NDEy)",
            "[<b>Osteoarthritis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTgwMzk1NDY5ODkxMzM5)",
            "[<b>Osteoporosis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTgxMzk3NDk0MjQ2MjY2)",
            "[<b>Pivd Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTgyMzk5NTE4NjAxMTkz)",
            "[<b>Rheumatoid Arthritis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTgzNDAxNTQyOTU2MTIw)",
            "[<b>Septic Arthritis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTg0NDAzNTY3MzExMDQ3)",
            "[<b>T.B Spine Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTg1NDA1NTkxNjY1OTc0)",
            "[<b>Ulnar Nerve Palsy Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTg2NDA3NjE2MDIwOTAx)",
            "[<b>Anorexia Nervosa Dr. Sandeep Goil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTg3NDA5NjQwMzc1ODI4)",
            "[<b>Autism Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTg4NDExNjY0NzMwNzU1)",
            "[<b>Bulima Nervosa Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTg5NDEzNjg5MDg1Njgy)",
            "[<b>Case Discusion Ptsd Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTkwNDE1NzEzNDQwNjA5)",
            "[<b>Cocaine Intoxication Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTkxNDE3NzM3Nzk1NTM2)",
            "[<b>Dementia Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTkyNDE5NzYyMTUwNDYz)",
            "[<b>Depression Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTkzNDIxNzg2NTA1Mzkw)",
            "[<b>Hyperacyivity Disorder Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTk0NDIzODEwODYwMzE3)",
            "[<b>Panic Attack Dr. Sandeep Govil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTk1NDI1ODM1MjE1MjQ0)",
            "[<b>Acute Bacterial Meningitis Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTk2NDI3ODU5NTcwMTcx)",
            "[<b>Atrial Fibrillation Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTk3NDI5ODgzOTI1MDk4)",
            "[<b>Bartter Syndrome Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTk4NDMxOTA4MjgwMDI1)",
            "[<b>Bronchial Asthma Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNTk5NDMzOTMyNjM0OTUy)",
            "[<b>COPD Dr. Santosh Patil atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjAwNDM1OTU2OTg5ODc5)",
            "[<b>Cerebrovascular Accident Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjAxNDM3OTgxMzQ0ODA2)",
            "[<b>Chronic Kidney Disease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjAyNDQwMDA1Njk5NzMz)",
            "[<b>Chronic Stable Angina Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjAzNDQyMDMwMDU0NjYw)",
            "[<b>Coarctation of Arota Dr. Sanjay Khatri  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjA0NDQ0MDU0NDA5NTg3)",
            "[<b>Community Acquired Pneumona Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjA1NDQ2MDc4NzY0NTE0)",
            "[<b>Congestive Heart Failure Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjA2NDQ4MTAzMTE5NDQx)",
            "[<b>Cor Pulmonale Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjA3NDUwMTI3NDc0MzY4)",
            "[<b>Covid 19 Pneumonia Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjA4NDUyMTUxODI5Mjk1)",
            "[<b>Crohn's Disease Dr. Santosh Patil atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjA5NDU0MTc2MTg0MjIy)",
            "[<b>Cushing Syndrome Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjEwNDU2MjAwNTM5MTQ5)",
            "[<b>Dengue Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjExNDU4MjI0ODk0MDc2)",
            "[<b>Diabetes Insipidus Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjEyNDYwMjQ5MjQ5MDAz)",
            "[<b>Diabetic Ketoacidosis Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjEzNDYyMjczNjAzOTMw)",
            "[<b>Dilated Cardiomyopathy Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjE0NDY0Mjk3OTU4ODU3)",
            "[<b>Dyslipidemia Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjE1NDY2MzIyMzEzNzg0)",
            "[<b>Gastritis Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjE2NDY4MzQ2NjY4NzEx)",
            "[<b>Gbs Dr.Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjE3NDcwMzcxMDIzNjM4)",
            "[<b>Graves Disease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjE4NDcyMzk1Mzc4NTY1)",
            "[<b>Hemiplegia Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjE5NDc0NDE5NzMzNDky)",
            "[<b>Hip Arthritis Dr. Mukul Mohindra  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjIwNDc2NDQ0MDg4NDE5)",
            "[<b>Hyperprolactinemia Dr. Santosh Patil 3 June 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjIxNDc4NDY4NDQzMzQ2)",
            "[<b>Hypertension Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjIyNDgwNDkyNzk4Mjcz)",
            "[<b>Hyperthyroidism Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjIzNDgyNTE3MTUzMjAw)",
            "[<b>Hypertrophic Cardiomyopathy Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjI0NDg0NTQxNTA4MTI3)",
            "[<b>Idiopathic Thrombocytopenic Purpura Dr. Punit Bhojani  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjI1NDg2NTY1ODYzMDU0)",
            "[<b>Inflammatory Bowel Disease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjI2NDg4NTkwMjE3OTgx)",
            "[<b>Interstitial Lung Diseases Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjI3NDkwNjE0NTcyOTA4)",
            "[<b>Lung Cancer Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjI4NDkyNjM4OTI3ODM1)",
            "[<b>Matablic Syndrome Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjI5NDk0NjYzMjgyNzYy)",
            "[<b>Migraine Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjMwNDk2Njg3NjM3Njg5)",
            "[<b>Mitral Regurgitation Dr. Santosh Patil 3 June 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjMxNDk4NzExOTkyNjE2)",
            "[<b>Mitral Stenosis Final Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjMyNTAwNzM2MzQ3NTQz)",
            "[<b>Motor Neuron Disease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjMzNTAyNzYwNzAyNDcw)",
            "[<b>Multiply Melganoma Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjM0NTA0Nzg1MDU3Mzk3)",
            "[<b>Muscular Dystrophy Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjM1NTA2ODA5NDEyMzI0)",
            "[<b>Myxedema Coma Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjM2NTA4ODMzNzY3MjUx)",
            "[<b>Nephritic Syndrome Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjM3NTEwODU4MTIyMTc4)",
            "[<b>Obstructive Sleep Apnea Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjM4NTEyODgyNDc3MTA1)",
            "[<b>Paraplegia Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjM5NTE0OTA2ODMyMDMy)",
            "[<b>Parkinsons Dr.Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQwNTE2OTMxMTg2OTU5)",
            "[<b>Peptic Ulcer Disease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQxNTE4OTU1NTQxODg2)",
            "[<b>Pericarditis Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQyNTIwOTc5ODk2ODEz)",
            "[<b>Pheochromocytoma Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQzNTIzMDA0MjUxNzQw)",
            "[<b>Pleural Effusion Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQ0NTI1MDI4NjA2NjY3)",
            "[<b>Pneumoconosis Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQ1NTI3MDUyOTYxNTk0)",
            "[<b>Pneumocystis Pneumonia Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQ2NTI5MDc3MzE2NTIx)",
            "[<b>Polycystic Kidney Diesease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQ3NTMxMTAxNjcxNDQ4)",
            "[<b>Pulmonary Tuberculosis Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQ4NTMzMTI2MDI2Mzc1)",
            "[<b>Renal Lump Dr. Deepak  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjQ5NTM1MTUwMzgxMzAy)",
            "[<b>Secondary to Insulinoma Dr. Santosh Patil 3 June 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjUwNTM3MTc0NzM2MjI5)",
            "[<b>Sick Sinus Syndrome Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjUxNTM5MTk5MDkxMTU2)",
            "[<b>Subarachnoid Haemorrhage Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjUyNTQxMjIzNDQ2MDgz)",
            "[<b>Subdural Hemorrhagea Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjUzNTQzMjQ3ODAxMDEw)",
            "[<b>Syphilis Dr. Santosh Patil 3 June 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjU0NTQ1MjcyMTU1OTM3)",
            "[<b>Typhoid Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjU1NTQ3Mjk2NTEwODY0)",
            "[<b>Ulcerative Colitis Dr. Santosh Patil 3 June 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjU2NTQ5MzIwODY1Nzkx)",
            "[<b>Urticiria Dr. Chesta Agarwal  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjU3NTUxMzQ1MjIwNzE4)",
            "[<b>Viral Hepatitis Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjU4NTUzMzY5NTc1NjQ1)",
            "[<b>Wilson S Disease Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjU5NTU1MzkzOTMwNTcy)",
            "[<b>Zollinger Ellison Syndrome Dr. Santosh Patil  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjYwNTU3NDE4Mjg1NDk5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        clinicalp_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"clinicalp_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"clinicalp_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(clinicalp_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
