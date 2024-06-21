
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
            [InlineKeyboardButton("BIOCHEMESTRY", callback_data="biochemestry")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiology")],
            [InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacology")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathology")],
            [InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiology")],
            [InlineKeyboardButton("PSM", callback_data="psm")],
            [InlineKeyboardButton("OPTHALMOLOGY", callback_data="opthalmology")],
            [InlineKeyboardButton("ENT", callback_data="ent")],
            [InlineKeyboardButton("FMT", callback_data="fmt")],
            [InlineKeyboardButton("SURGERY", callback_data="surgery")],
            [InlineKeyboardButton("MEDICINE", callback_data="medicine")],
            [InlineKeyboardButton("DERMATOLOHY", callback_data="dermatology")],
            [InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatry")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesia")],
            [InlineKeyboardButton("RADIOLOGY", callback_data="radiology")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedics")],
            [InlineKeyboardButton("PEDIATRICS", callback_data="pediatrics")],
            [InlineKeyboardButton("OBGY", callback_data="obgy")],
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("biochemestry"):
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
    
    elif query.data.startswith("opthalmology"):
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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
        opthalmology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opthalmology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opthalmology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opthalmology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
