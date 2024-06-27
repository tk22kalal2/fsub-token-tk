
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import logging
import random
import markdown
import telegraph
import asyncio
from Script import script
from validators import domain
from clone_plugins.dbusers import db
from clone_plugins.users_api import get_user, update_user_info
from pyrogram import Client, filters, enums
from plugins.database import get_file_details
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import BOT_USERNAME, ADMINS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Message, CallbackQuery, InputMediaPhoto
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
SECONDS = int(os.getenv("SECONDS", "120"))

# Initialize Telegraph
telegraph_client = telegraph.Telegraph()
telegraph_client.create_account(short_name='short_name')

def paginate_links(links, page, per_page=20):
    if len(links) <= per_page:
        return links, False  # No pagination needed, show all links

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
        buttons = [
            [InlineKeyboardButton('MARROW', callback_data='marrow')],
            [InlineKeyboardButton('PREPLADDER 5', callback_data='prepladder')],
            [InlineKeyboardButton('CEREBELLUM', callback_data='cerebellum')],
            [InlineKeyboardButton('DOCTUTORAL', callback_data='doctut')],
            [InlineKeyboardButton('DAMS', callback_data='dams'), InlineKeyboardButton('MIST', callback_data='mist')],            
            [InlineKeyboardButton('OTHERS', callback_data='others')]
        ]
        me2 = (await client.get_me()).mention
        reply_markup = InlineKeyboardMarkup(buttons)
    
        # Define the ReplyKeyboardMarkup
        reply_keyboard = ReplyKeyboardMarkup(
            [[KeyboardButton('/menu')]], resize_keyboard=True, one_time_keyboard=True
        )
    
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.CLONE_START_TXT.format(message.from_user.mention, me2),
            reply_markup=reply_keyboard
        )
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.CLONE_START_TXT.format(message.from_user.mention, me2),
            reply_markup=reply_markup
        )
        return

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command("menu") & filters.incoming)
async def menu(client, message):
    buttons = [
        [InlineKeyboardButton('MARROW', callback_data='marrow')],
        [InlineKeyboardButton('PREPLADDER 5', callback_data='prepladder')],
        [InlineKeyboardButton('DOCTUTORAL', callback_data='doctut')],
        [InlineKeyboardButton('CEREBELLUM', callback_data='cerebellum')],
        [InlineKeyboardButton('DAMS', callback_data='dams'), InlineKeyboardButton('MIST', callback_data='mist')],
        [InlineKeyboardButton('OTHERS', callback_data='others')]
    ]
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
        buttons = [
            [InlineKeyboardButton('MARROW', callback_data='marrow')],
            [InlineKeyboardButton('PREPLADDER 5', callback_data='prepladder')],
            [InlineKeyboardButton('CEREBELLUM', callback_data='cerebellum')],
            [InlineKeyboardButton('DOCTUTORAL', callback_data='doctut')],
            [InlineKeyboardButton('DAMS', callback_data='dams'), InlineKeyboardButton('MIST', callback_data='mist')],
            [InlineKeyboardButton('OTHERS', callback_data='others')]
        ]
        
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

    elif query.data == "dams":
        dams_buttons = [
            [InlineKeyboardButton("DAMS ENGLISH", callback_data="damse"), InlineKeyboardButton("DAMS HINGLISH", callback_data="damsh")],
            [InlineKeyboardButton("DAMS DVT", callback_data="damsdvt"), InlineKeyboardButton("DAMS PYQ", callback_data="damspyq")],
            [InlineKeyboardButton("DAMS CLINICALS", callback_data="damsclinicals"), InlineKeyboardButton("DAMS TND", callback_data="damstnd")],
            [InlineKeyboardButton("DAMS SPECIAL TND", callback_data="damsspecialtnd")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(dams_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data == "others":
        others_buttons = [
            [InlineKeyboardButton("ZAINAB VOHRA RADIOLOGY", callback_data="zvradiology")],
            [InlineKeyboardButton("ASHISH SIR PHYSIOLOGY", callback_data="ashishphysiok")],
            [InlineKeyboardButton("RAJIV DHAWAN ENT", callback_data="rdent")],
            [InlineKeyboardButton("SRIKANT ANATOMY", callback_data="srikantanatomy")],
            [InlineKeyboardButton("PRIYANSH JAIN MEDICINE", callback_data="pjmedicine")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(others_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data == "marrow":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="oanatomyr"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="obiochemistryr")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="ophysiologyr"), InlineKeyboardButton("PHARMACOLOGY", callback_data="opharmacologyr")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="opathologyr"), InlineKeyboardButton("MICROBIOLOGY", callback_data="omicrobiologyr")],
            [InlineKeyboardButton("PSM", callback_data="opsmr"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="oophthalmologyr")],
            [InlineKeyboardButton("ENT", callback_data="oentr"), InlineKeyboardButton("FMT", callback_data="ofmtr")],
            [InlineKeyboardButton("SURGERY", callback_data="osurgeryr"), InlineKeyboardButton("MEDICINE", callback_data="omediciner")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="odermatologyr"), InlineKeyboardButton("PSYCHIATRY", callback_data="opsychiatryr")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="oanesthesiar"), InlineKeyboardButton("RADIOLOGY", callback_data="oradiologyr")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="oorthopedicsr"), InlineKeyboardButton("PEDIATRICS", callback_data="opediatricsr")],
            [InlineKeyboardButton("OBGY", callback_data="oobgyr"), InlineKeyboardButton("RECENT UPDATES", callback_data="recentupdates")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("oorthopedicsr"):
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
        oorthopedicsr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"oorthopedicsr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"oorthopedicsr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(oorthopedicsr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
        
    elif query.data.startswith("obiochemistryr"):
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
        obiochemistryr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"obiochemistryr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"obiochemistryr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(obiochemistryr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data.startswith("oanesthesiar"):
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
        oanesthesiar_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"oanesthesiar_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"oanesthesiar_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(oanesthesiar_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
    
    elif query.data.startswith("oophthalmologyr"):
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
        oophthalmologyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"oophthalmologyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"oophthalmologyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(oophthalmologyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("ofmtr"):
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
        ofmtr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ofmtr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ofmtr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ofmtr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("odermatologyr"):
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
        odermatologyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"odermatologyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"odermatologyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(odermatologyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("opsychiatryr"):
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
        opsychiatryr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opsychiatryr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opsychiatryr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opsychiatryr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("oentr"):
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
        oentr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"oentr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"oentr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(oentr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("oradiologyr"):
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
        oradiologyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"oradiologyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"oradiologyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(oradiologyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("opathologyr"):
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
        opathologyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"opathologyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"opathologyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(opathologyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("oobgyr"):
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
        oobgyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"oobgyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"oobgyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(oobgyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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

    elif query.data.startswith("msurgeryr"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mopthalmolog_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mopthalmolog_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mopthalmolog_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mopthalmolog_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mpsmr"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mopthalmolo_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mopthalmolo_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mopthalmolo_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mopthalmolog_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data.startswith("mpediatricsr"):
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
        mpediatricsr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mpediatricsr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mpediatricsr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mpediatricsr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data == "prepladder":
        prepladder_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomyp"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistryp")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiologyp"), InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacologyp")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathologyp"), InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiologyp")],
            [InlineKeyboardButton("PSM", callback_data="psmp"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="ophthalmologyp")],
            [InlineKeyboardButton("ENT", callback_data="pent"), InlineKeyboardButton("FMT", callback_data="fmtp")],
            [InlineKeyboardButton("SURGERY", callback_data="surgeryp"), InlineKeyboardButton("MEDICINE", callback_data="medicinep")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="dermatologyp"), InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatryp")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesiap"), InlineKeyboardButton("RADIOLOGY", callback_data="radiologyp")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedicsp"), InlineKeyboardButton("PEDIATRICS", callback_data="pediatricsp")],
            [InlineKeyboardButton("OBGY", callback_data="obgyp"), InlineKeyboardButton("RAPID REVISION", callback_data="rapidrevisionp")],
            [InlineKeyboardButton("CLINICALS", callback_data="clinicalp"), InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(prepladder_buttons)
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


    elif query.data.startswith("pent"):
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
        pent_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pent_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pent_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pent_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
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

    
    elif query.data == "doctut":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomyd"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistryd")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiologyd"), InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacologyd")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathologyd"), InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiologyd")],
            [InlineKeyboardButton("PSM", callback_data="psmd"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="ophthalmologyd")],
            [InlineKeyboardButton("ENT", callback_data="entd"), InlineKeyboardButton("FMT", callback_data="fmtd")],
            [InlineKeyboardButton("SURGERY", callback_data="surgeryd"), InlineKeyboardButton("MEDICINE", callback_data="medicined")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="dermatologyd"), InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatryd")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesiad"), InlineKeyboardButton("RADIOLOGY", callback_data="radiologyd")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedicsd"), InlineKeyboardButton("PEDIATRICS", callback_data="pediatricsd")],
            [InlineKeyboardButton("OBGY", callback_data="obgyd"), InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("anatomyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Abdomen Abdominal Aorta  Celia Trunk atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjYxNTU5NDQyNjQwNDI2)",	
            "[<b>Abdomen Anterior Abdominal Wall and Inguinal Canal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjYyNTYxNDY2OTk1MzUz)",	
            "[<b>Abdomen Ivc Portal Vein Ivc  Portocaval Anastomosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjYzNTYzNDkxMzUwMjgw)",	
            "[<b>Abdomen Liver Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjY0NTY1NTE1NzA1MjA3)",	
            "[<b>Abdomen Peritoneum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjY1NTY3NTQwMDYwMTM0)",	
            "[<b>Abdomen Rectus Sheath Posterior Abdominal Wall and Thoracolumbar Fascia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjY2NTY5NTY0NDE1MDYx)",	
            "[<b>Abdomen Sma Ima atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjY3NTcxNTg4NzY5OTg4)",	
            "[<b>Abdomen Stomach  Diaphragm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjY4NTczNjEzMTI0OTE1)",	
            "[<b>Embryology 1. General Embryology 3 2Nd Week atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjY5NTc1NjM3NDc5ODQy)",	
            "[<b>Embryology 1. General Embryology 3 3Rd Week atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjcwNTc3NjYxODM0NzY5)",	
            "[<b>Embryology 1. General Embryology 3 Gametogenesis 1St Week atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjcxNTc5Njg2MTg5Njk2)",	
            "[<b>Embryology 2. Systemic Embryology 12 Cns Embryology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjcyNTgxNzEwNTQ0NjIz)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Arterial System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjczNTgzNzM0ODk5NTUw)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Diaphragm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjc0NTg1NzU5MjU0NDc3)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Face Palate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjc1NTg3NzgzNjA5NDA0)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Heart atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjc2NTg5ODA3OTY0MzMx)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Interatrial Septum  Interventricular Septum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjc3NTkxODMyMzE5MjU4)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Tongue  Thyroid Gland atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjc4NTkzODU2Njc0MTg1)",	
            "[<b>Embryology 2. Systemic Embryology 12 Development of Venous System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjc5NTk1ODgxMDI5MTEy)",	
            "[<b>Embryology 2. Systemic Embryology 12 Gut Embrology Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjgwNTk3OTA1Mzg0MDM5)",	
            "[<b>Head and Neck Dural Venous Sinuses and Cavernous Sinus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjgxNTk5OTI5NzM4OTY2)",	
            "[<b>Head and Neck Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjgyNjAxOTU0MDkzODkz)",	
            "[<b>Head and Neck Pharynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjgzNjAzOTc4NDQ4ODIw)",	
            "[<b>Head and Neck Posterior Triangle of Neck atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjg0NjA2MDAyODAzNzQ3)",	
            "[<b>Head and Neck Subclavian Artery Scalenus Anterior Muscle Veins of Face atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjg1NjA4MDI3MTU4Njc0)",	
            "[<b>Head and Neck Temporomandibular Joint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjg2NjEwMDUxNTEzNjAx)",	
            "[<b>Head and Neck Tongue atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjg3NjEyMDc1ODY4NTI4)",	
            "[<b>Head and Neck Transverse Section of Neck atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjg4NjE0MTAwMjIzNDU1)",	
            "[<b>Histology Epithelium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjg5NjE2MTI0NTc4Mzgy)",	
            "[<b>Lower Limb Adductor Canal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjkwNjE4MTQ4OTMzMzA5)",	
            "[<b>Lower Limb Arches of Foot atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjkxNjIwMTczMjg4MjM2)",	
            "[<b>Lower Limb Common Peroneal Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjkyNjIyMTk3NjQzMTYz)",	
            "[<b>Lower Limb Femoral Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjkzNjI0MjIxOTk4MDkw)",	
            "[<b>Lower Limb Femoral Triangle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjk0NjI2MjQ2MzUzMDE3)",	
            "[<b>Lower Limb Gluteal Region Greater  Lesser Sciatic Foramen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjk1NjI4MjcwNzA3OTQ0)",	
            "[<b>Lower Limb Iliotibial Tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjk2NjMwMjk1MDYyODcx)",	
            "[<b>Lower Limb Lumbosacral Plexus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjk3NjMyMzE5NDE3Nzk4)",	
            "[<b>Lower Limb Obturator Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjk4NjM0MzQzNzcyNzI1)",	
            "[<b>Lower Limb Tibial Nerve  Sole of Foot atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNjk5NjM2MzY4MTI3NjUy)",	
            "[<b>Lower Limb V S of Lower Limb  Popliteal Fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzAwNjM4MzkyNDgyNTc5)",	
            "[<b>NeuroBasal Ganglia and Internal Capsule atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzAxNjQwNDE2ODM3NTA2)",	
            "[<b>NeuroBlood Supply of Brain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzAyNjQyNDQxMTkyNDMz)",	
            "[<b>NeuroBrodmann Area atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzAzNjQ0NDY1NTQ3MzYw)",	
            "[<b>NeuroCerebellumb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzA0NjQ2NDg5OTAyMjg3)",	
            "[<b>NeuroCervical Fossa and Cranial Foramen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzA1NjQ4NTE0MjU3MjE0)",	
            "[<b>NeuroCranial Nerve Nuclei atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzA2NjUwNTM4NjEyMTQx)",	
            "[<b>NeuroIntroduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzA3NjUyNTYyOTY3MDY4)",	
            "[<b>NeuroLateral Ventricles  3Rd Ventricle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzA4NjU0NTg3MzIxOTk1)",	
            "[<b>NeuroSpinal Cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzA5NjU2NjExNjc2OTIy)",	
            "[<b>NeuroT S of Midbrain Pons and Medulla atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzEwNjU4NjM2MDMxODQ5)",	
            "[<b>NeuroVentral Aspect of Brainstem Dorsal Ventral Aspect of Brainstem atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzExNjYwNjYwMzg2Nzc2)",	
            "[<b>NeuroWhite Matter  Projection Fibers Ascending Tracts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzEyNjYyNjg0NzQxNzAz)",	
            "[<b>NeuroWhite Matter  Projection Fibers Descending Tracts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzEzNjY0NzA5MDk2NjMw)",	
            "[<b>NeuroWhite Matter Association  Commissural Fibers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzE0NjY2NzMzNDUxNTU3)",	
            "[<b>Pelvis and Perinium Internal Iliac Artery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzE1NjY4NzU3ODA2NDg0)",	
            "[<b>Pelvis and Perinium Ischiorectal Fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzE2NjcwNzgyMTYxNDEx)",	
            "[<b>Pelvis and Perinium Pelvis  Perineum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzE3NjcyODA2NTE2MzM4)",	
            "[<b>Pelvis and Perinium Urinary Bladder  Urethra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzE4Njc0ODMwODcxMjY1)",	
            "[<b>Qrp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzE5Njc2ODU1MjI2MTky)",	
            "[<b>Qrp by Dr Mohammed Azam atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzIwNjc4ODc5NTgxMTE5)",	
            "[<b>Upper Limb Anatomical Snuff Box and Extensor Retinaculum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzIxNjgwOTAzOTM2MDQ2)",	
            "[<b>Upper Limb Axillary Artery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzIyNjgyOTI4MjkwOTcz)",	
            "[<b>Upper Limb Brachial Artery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzIzNjg0OTUyNjQ1OTAw)",	
            "[<b>Upper Limb Brachial Plexus and Clinical Correlation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzI0Njg2OTc3MDAwODI3)",	
            "[<b>Upper Limb Carpal Tunnel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzI1Njg5MDAxMzU1NzU0)",	
            "[<b>Upper Limb Cubital Fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzI2NjkxMDI1NzEwNjgx)",	
            "[<b>Upper Limb Major Nerves  Musculocutaneous Nerve  Axillary Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzI3NjkzMDUwMDY1NjA4)",	
            "[<b>Upper Limb Muscles of Arm and Forearm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzI4Njk1MDc0NDIwNTM1)",	
            "[<b>Upper Limb Median Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzI5Njk3MDk4Nzc1NDYy)",	
            "[<b>Upper Limb Muscles of Hand atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzMwNjk5MTIzMTMwMzg5)",	
            "[<b>Upper Limb Palmar Arches atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzMxNzAxMTQ3NDg1MzE2)",	
            "[<b>Upper Limb Pectoral Region Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzMyNzAzMTcxODQwMjQz)",	
            "[<b>Upper Limb Pectoral Region Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzMzNzA1MTk2MTk1MTcw)",	
            "[<b>Upper Limb Radial Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzM0NzA3MjIwNTUwMDk3)",	
            "[<b>Upper Limb Scapular Anastomosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzM1NzA5MjQ0OTA1MDI0)",	
            "[<b>Upper Limb Ulnar Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzM2NzExMjY5MjU5OTUx)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anatomyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anatomyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anatomyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anatomyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("physiologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Cell Cell Connections  Intracellular Organelles Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzM3NzEzMjkzNjE0ODc4)",
            "[<b>Cell Cell Connections  Intracellular Organelles Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzM4NzE1MzE3OTY5ODA1)",
            "[<b>Cell Cell Membrane atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzM5NzE3MzQyMzI0NzMy)",
            "[<b>Cell Demonstration of Electrical Activities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQwNzE5MzY2Njc5NjU5)",
            "[<b>Cell Electrical Properties of Cell atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQxNzIxMzkxMDM0NTg2)",
            "[<b>Cell Transport Across Membrane atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQyNzIzNDE1Mzg5NTEz)",
            "[<b>Cns Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQzNzI1NDM5NzQ0NDQw)",
            "[<b>Cns Brown Sequard Syndrome  Other Spinal Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQ0NzI3NDY0MDk5MzY3)",
            "[<b>Cns Cerebellum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQ1NzI5NDg4NDU0Mjk0)",
            "[<b>Cns Cortex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQ2NzMxNTEyODA5MjIx)",
            "[<b>Cns Eeg Normal  Abnormalities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQ3NzMzNTM3MTY0MTQ4)",
            "[<b>Cns Epilepsy and Status Epilepticus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQ4NzM1NTYxNTE5MDc1)",
            "[<b>Cns Hemispherical Specialization atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzQ5NzM3NTg1ODc0MDAy)",
            "[<b>Cns Initiation Propagation of Action Potentials atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzUwNzM5NjEwMjI4OTI5)",
            "[<b>Cns Language  Aphasias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzUxNzQxNjM0NTgzODU2)",
            "[<b>Cns Learning  Memory atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzUyNzQzNjU4OTM4Nzgz)",
            "[<b>Cns Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzUzNzQ1NjgzMjkzNzEw)",
            "[<b>Cns Muscle Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzU0NzQ3NzA3NjQ4NjM3)",
            "[<b>Cns Muscle Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzU1NzQ5NzMyMDAzNTY0)",
            "[<b>Cns Muscle Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzU2NzUxNzU2MzU4NDkx)",
            "[<b>Cns Nerve Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzU3NzUzNzgwNzEzNDE4)",
            "[<b>Cns Nerve Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzU4NzU1ODA1MDY4MzQ1)",
            "[<b>Cns Neuromuscular Junction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzU5NzU3ODI5NDIzMjcy)",
            "[<b>Cns Papez Circuit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzYwNzU5ODUzNzc4MTk5)",
            "[<b>Cns Physiological Correlates  Peripheral Nerve Disorders Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzYxNzYxODc4MTMzMTI2)",
            "[<b>Cns Physiological Correlates  Peripheral Nerve Disorders Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzYyNzYzOTAyNDg4MDUz)",
            "[<b>Cns Spinal Cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzYzNzY1OTI2ODQyOTgw)",
            "[<b>Cns Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzY0NzY3OTUxMTk3OTA3)",
            "[<b>Cns Thalamus  Hypothalamus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzY1NzY5OTc1NTUyODM0)",
            "[<b>Cvs Abnormalities of Ecg Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzY2NzcxOTk5OTA3NzYx)",
            "[<b>Cvs Abnormalities of Ecg Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzY3Nzc0MDI0MjYyNjg4)",
            "[<b>Cvs Basics of Ecg Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzY4Nzc2MDQ4NjE3NjE1)",
            "[<b>Cvs Basics of Ecg Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzY5Nzc4MDcyOTcyNTQy)",
            "[<b>Cvs Blood Pressure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzcwNzgwMDk3MzI3NDY5)",
            "[<b>Cvs Cardiac Action Potential atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzcxNzgyMTIxNjgyMzk2)",
            "[<b>Cvs Cardiac Contraction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzcyNzg0MTQ2MDM3MzIz)",
            "[<b>Cvs Cardiac Cycle and Output atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzczNzg2MTcwMzkyMjUw)",
            "[<b>Cvs Cardiac Output Calculation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzc0Nzg4MTk0NzQ3MTc3)",
            "[<b>Cvs Conduction System  Basics of Ecg atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzc1NzkwMjE5MTAyMTA0)",
            "[<b>Cvs Flow Resistance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzc2NzkyMjQzNDU3MDMx)",
            "[<b>Cvs Heart Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzc3Nzk0MjY3ODExOTU4)",
            "[<b>Cvs Heart Sounds atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzc4Nzk2MjkyMTY2ODg1)",
            "[<b>Cvs Jvp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzc5Nzk4MzE2NTIxODEy)",
            "[<b>Cvs Myocardial Ischemia Infarction Electrical Correlates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzgwODAwMzQwODc2NzM5)",
            "[<b>Cvs Pressure Volume Loop atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzgxODAyMzY1MjMxNjY2)",
            "[<b>Cvs Reflexes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzgyODA0Mzg5NTg2NTkz)",
            "[<b>Cvs Regulation of Cardiac Output atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzgzODA2NDEzOTQxNTIw)",
            "[<b>Endocrine Adrenal Cortex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzg0ODA4NDM4Mjk2NDQ3)",
            "[<b>Endocrine Anterior Pituitary Growth Hormone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzg1ODEwNDYyNjUxMzc0)",
            "[<b>Endocrine Anterior Pituitary Prolactin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzg2ODEyNDg3MDA2MzAx)",
            "[<b>Endocrine Classification of Hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzg3ODE0NTExMzYxMjI4)",
            "[<b>Endocrine Female Reproductive System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzg4ODE2NTM1NzE2MTU1)",
            "[<b>Endocrine Hormones Questions in Calcium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzg5ODE4NTYwMDcxMDgy)",
            "[<b>Endocrine Implantation and Placenta atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzkwODIwNTg0NDI2MDA5)",
            "[<b>Endocrine Male Reproductive System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzkxODIyNjA4NzgwOTM2)",
            "[<b>Endocrine Oogenesis Fertilization atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzkyODI0NjMzMTM1ODYz)",
            "[<b>Endocrine Pancreas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzkzODI2NjU3NDkwNzkw)",
            "[<b>Endocrine Physiological Changes in Pregnancy Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzk0ODI4NjgxODQ1NzE3)",
            "[<b>Endocrine Physiological Changes in Pregnancy Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzk1ODMwNzA2MjAwNjQ0)",
            "[<b>Endocrine Posterior Pituitary Vasopressin and Siadh and Diabetes Insipidus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzk2ODMyNzMwNTU1NTcx)",
            "[<b>Endocrine Receptors and Second Messengers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzk3ODM0NzU0OTEwNDk4)",
            "[<b>Endocrine Spermatogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzk4ODM2Nzc5MjY1NDI1)",
            "[<b>Endocrine Thyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExNzk5ODM4ODAzNjIwMzUy)",
            "[<b>Fundamental Biophysics 1 Fundamental Biophysics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODAwODQwODI3OTc1Mjc5)",
            "[<b>Git Esophagus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODAxODQyODUyMzMwMjA2)",
            "[<b>Git Intestinal Absorption atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODAyODQ0ODc2Njg1MTMz)",
            "[<b>Git Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODAzODQ2OTAxMDQwMDYw)",
            "[<b>Git Pancreas and Bile atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODA0ODQ4OTI1Mzk0OTg3)",
            "[<b>Git Questions on Esophagus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODA1ODUwOTQ5NzQ5OTE0)",
            "[<b>Git Saliva atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODA2ODUyOTc0MTA0ODQx)",
            "[<b>Git Stomach atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODA3ODU0OTk4NDU5NzY4)",
            "[<b>Miscellaneous Deep Sea Diving  High Actinide atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODA4ODU3MDIyODE0Njk1)",
            "[<b>Miscellaneous Exercise  Sports atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODA5ODU5MDQ3MTY5NjIy)",
            "[<b>Miscellaneous Space  Gravity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODEwODYxMDcxNTI0NTQ5)",
            "[<b>Miscellaneous Temperature Regulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODExODYzMDk1ODc5NDc2)",
            "[<b>Qrp Ini Cet Qrp Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODEyODY1MTIwMjM0NDAz)",
            "[<b>Qrp by Dr Prem 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODEzODY3MTQ0NTg5MzMw)",
            "[<b>Qrp by Dr Prem 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODE0ODY5MTY4OTQ0MjU3)",
            "[<b>Renal Physiology - Acid Base Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODE1ODcxMTkzMjk5MTg0)",
            "[<b>Renal Physiology - Basics of Nephron atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODE2ODczMjE3NjU0MTEx)",
            "[<b>Renal Physiology - Body Fluids Movments atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODE3ODc1MjQyMDA5MDM4)",
            "[<b>Renal Physiology - Body Fluids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODE4ODc3MjY2MzYzOTY1)",
            "[<b>Renal Physiology - Distal Convoluted Tubule and Collecting Duct atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODE5ODc5MjkwNzE4ODky)",
            "[<b>Renal Physiology - Electrolyte Mineral H2o Homeostasis Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODIwODgxMzE1MDczODE5)",
            "[<b>Respiration - O2 Therapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODIxODgzMzM5NDI4NzQ2)",
            "[<b>Respiration - Ventilization Perfusion Relationship atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODIyODg1MzYzNzgzNjcz)",
            "[<b>Special Senses Vision atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODIzODg3Mzg4MTM4NjAw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        physiologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"physiologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"physiologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(physiologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("biochemistryd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Aiims Recall Qs Aiims Recall Session May 2019 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODI0ODg5NDEyNDkzNTI3)",
            "[<b>Aiims Recall Qs Aiims Recall Session Nov 2019 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODI1ODkxNDM2ODQ4NDU0)",
            "[<b>Amino Acid and Proteins 21St  22Nd Amino Acids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODI2ODkzNDYxMjAzMzgx)",
            "[<b>Amino Acid and Proteins Amino Acid Catabolism Carbon Skelton atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODI3ODk1NDg1NTU4MzA4)",
            "[<b>Amino Acid and Proteins Amino Acid Catabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODI4ODk3NTA5OTEzMjM1)",
            "[<b>Amino Acid and Proteins Amino Acids  Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODI5ODk5NTM0MjY4MTYy)",
            "[<b>Amino Acid and Proteins Amino Acids  Properties atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODMwOTAxNTU4NjIzMDg5)",
            "[<b>Amino Acid and Proteins Biosynthesis of Amino Acids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODMxOTAzNTgyOTc4MDE2)",
            "[<b>Amino Acid and Proteins Collagend atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODMyOTA1NjA3MzMyOTQz)",
            "[<b>Amino Acid and Proteins Disorders of Urea Cycle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODMzOTA3NjMxNjg3ODcw)",
            "[<b>Amino Acid and Proteins Phenylalanine Tyrosine Complex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODM0OTA5NjU2MDQyNzk3)",
            "[<b>Amino Acid and Proteins Phenylalanine Tyrosine Complex Tyrosinemia  Others atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODM1OTExNjgwMzk3NzI0)",
            "[<b>Amino Acid and Proteins Post Translational Modification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODM2OTEzNzA0NzUyNjUx)",
            "[<b>Amino Acid and Proteins Protein Structure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODM3OTE1NzI5MTA3NTc4)",
            "[<b>Amino Acid and Proteins Separation of Proteins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODM4OTE3NzUzNDYyNTA1)",
            "[<b>Amino Acid and Proteins Special Products of Amino Acids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODM5OTE5Nzc3ODE3NDMy)",
            "[<b>Bioenergetics Eelectron Transport Chain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQwOTIxODAyMTcyMzU5)",
            "[<b>Bioenergetics Krebs Cycle Tca Cycle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQxOTIzODI2NTI3Mjg2)",
            "[<b>Bioenergetics Link Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQyOTI1ODUwODgyMjEz)",
            "[<b>Bioenergetics Shuttle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQzOTI3ODc1MjM3MTQw)",
            "[<b>Carbohydrates Classification 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQ0OTI5ODk5NTkyMDY3)",
            "[<b>Carbohydrates Classification 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQ1OTMxOTIzOTQ2OTk0)",
            "[<b>Carbohydrates Fructose Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQ2OTMzOTQ4MzAxOTIx)",
            "[<b>Carbohydrates Galactose Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQ3OTM1OTcyNjU2ODQ4)",
            "[<b>Carbohydrates Gluconeogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQ4OTM3OTk3MDExNzc1)",
            "[<b>Carbohydrates Glucose Transport atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODQ5OTQwMDIxMzY2NzAy)",
            "[<b>Carbohydrates Glycogen Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODUwOTQyMDQ1NzIxNjI5)",
            "[<b>Carbohydrates Glycogen Storage Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODUxOTQ0MDcwMDc2NTU2)",
            "[<b>Carbohydrates Glycolysis Highlights atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODUyOTQ2MDk0NDMxNDgz)",
            "[<b>Carbohydrates Glycolysis Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODUzOTQ4MTE4Nzg2NDEw)",
            "[<b>Carbohydrates Hmp Shunt atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODU0OTUwMTQzMTQxMzM3)",
            "[<b>Carbohydrates Identification of Carbohydrates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODU1OTUyMTY3NDk2MjY0)",
            "[<b>Carbohydrates Isomerism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODU2OTU0MTkxODUxMTkx)",
            "[<b>Enzymes Applications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODU3OTU2MjE2MjA2MTE4)",
            "[<b>Enzymes Enzyme Inhibition atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODU4OTU4MjQwNTYxMDQ1)",
            "[<b>Enzymes Enzyme Regulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODU5OTYwMjY0OTE1OTcy)",
            "[<b>Enzymes Introduction and Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODYwOTYyMjg5MjcwODk5)",
            "[<b>Enzymes Isoenzymes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODYxOTY0MzEzNjI1ODI2)",
            "[<b>Enzymes Kinetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODYyOTY2MzM3OTgwNzUz)",
            "[<b>Enzymes Mechanism of Catalysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODYzOTY4MzYyMzM1Njgw)",
            "[<b>Enzymes Properties atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODY0OTcwMzg2NjkwNjA3)",
            "[<b>General Acid Base Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODY1OTcyNDExMDQ1NTM0)",
            "[<b>General Acid Base Homeostasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODY2OTc0NDM1NDAwNDYx)",
            "[<b>General Actions of Insulin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODY3OTc2NDU5NzU1Mzg4)",
            "[<b>General Introduction to atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODY4OTc4NDg0MTEwMzE1)",
            "[<b>Heme Metabolism Heme Degradation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODY5OTgwNTA4NDY1MjQy)",
            "[<b>Heme Metabolism Heme Synthesis and Porphyriase atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODcwOTgyNTMyODIwMTY5)",
            "[<b>Heme Metabolism Hyperbilirubinemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODcxOTg0NTU3MTc1MDk2)",
            "[<b>Lipid Metabolism Bile Acid Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODcyOTg2NTgxNTMwMDIz)",
            "[<b>Lipid Metabolism Cholesterol Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODczOTg4NjA1ODg0OTUw)",
            "[<b>Lipid Metabolism Fatty Acid Oxidation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODc0OTkwNjMwMjM5ODc3)",
            "[<b>Lipid Metabolism Fatty Acid Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODc1OTkyNjU0NTk0ODA0)",
            "[<b>Lipid Metabolism Fatty Acids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODc2OTk0Njc4OTQ5NzMx)",
            "[<b>Lipid Metabolism Ketogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODc3OTk2NzAzMzA0NjU4)",
            "[<b>Lipid Metabolism Lipids Introduction and Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODc4OTk4NzI3NjU5NTg1)",
            "[<b>Lipid Metabolism Lipoprotein Transport atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODgwMDAwNzUyMDE0NTEy)",
            "[<b>Lipid Metabolism Lipoprotein atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODgxMDAyNzc2MzY5NDM5)",
            "[<b>Lipid Metabolism Sphingolipids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODgyMDA0ODAwNzI0MzY2)",
            "[<b>Molecular Biology Dna 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODgzMDA2ODI1MDc5Mjkz)",
            "[<b>Molecular Biology Dna 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODg0MDA4ODQ5NDM0MjIw)",
            "[<b>Molecular Biology Dna Damage Repair atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODg1MDEwODczNzg5MTQ3)",
            "[<b>Molecular Biology Dna Polymerase atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODg2MDEyODk4MTQ0MDc0)",
            "[<b>Molecular Biology Dna Rna Sequence Relationship atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODg3MDE0OTIyNDk5MDAx)",
            "[<b>Molecular Biology Dna Synthesis Replication atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODg4MDE2OTQ2ODUzOTI4)",
            "[<b>Molecular Biology Genetic Code atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODg5MDE4OTcxMjA4ODU1)",
            "[<b>Molecular Biology Introduction Nucleotide atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODkwMDIwOTk1NTYzNzgy)",
            "[<b>Molecular Biology Lac Operon atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODkxMDIzMDE5OTE4NzA5)",
            "[<b>Molecular Biology Lesch Nyhan Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODkyMDI1MDQ0MjczNjM2)",
            "[<b>Molecular Biology Mitochondrial Dna  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODkzMDI3MDY4NjI4NTYz)",
            "[<b>Molecular Biology Mutation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODk0MDI5MDkyOTgzNDkw)",
            "[<b>Molecular Biology Nucleotide Properties atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODk1MDMxMTE3MzM4NDE3)",
            "[<b>Molecular Biology Pcr atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODk2MDMzMTQxNjkzMzQ0)",
            "[<b>Molecular Biology Protein Synthesis Translation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODk3MDM1MTY2MDQ4Mjcx)",
            "[<b>Molecular Biology Purine Degradation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODk4MDM3MTkwNDAzMTk4)",
            "[<b>Molecular Biology Purine Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExODk5MDM5MjE0NzU4MTI1)",
            "[<b>Molecular Biology Pyrimidine Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTAwMDQxMjM5MTEzMDUy)",
            "[<b>Molecular Biology Rna 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTAxMDQzMjYzNDY3OTc5)",
            "[<b>Molecular Biology Rna 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTAyMDQ1Mjg3ODIyOTA2)",
            "[<b>Molecular Biology Rna Synthesis Transcription atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTAzMDQ3MzEyMTc3ODMz)",
            "[<b>Qrp Ini Cet Qrp Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTA0MDQ5MzM2NTMyNzYw)",
            "[<b>Qrp by Dr Nilesh Chandra 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTA1MDUxMzYwODg3Njg3)",
            "[<b>Qrp by Dr Nilesh Chandra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTA2MDUzMzg1MjQyNjE0)",
            "[<b>Vitamins Lipid Soluble Vitamins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTA3MDU1NDA5NTk3NTQx)",
            "[<b>Vitamins Vitamins Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTA4MDU3NDMzOTUyNDY4)",
            "[<b>Vitamins Water Soluble Vitamins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTA5MDU5NDU4MzA3Mzk1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        biochemistryd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"biochemistryd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"biochemistryd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(biochemistryd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pathologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Patho Fee Videos - Approach to Anemia and Understanding atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTEwMDYxNDgyNjYyMzIy)",
            "[<b>1. Patho Fee Videos - Diagnosis Part 2 Fnac atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTExMDYzNTA3MDE3MjQ5)",
            "[<b>1. Patho Fee Videos - How to Revise Pathology for Upcoming Exams atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTEyMDY1NTMxMzcyMTc2)",
            "[<b>1. Patho Fee Videos - How to Use Doctutorials App atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTEzMDY3NTU1NzI3MTAz)",
            "[<b>1. Patho Fee Videos - Membranoproliferative Glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTE0MDY5NTgwMDgyMDMw)",
            "[<b>1. Patho Fee Videos - Natural Killer Cells Nk Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTE1MDcxNjA0NDM2OTU3)",
            "[<b>1. Patho Fee Videos - Pathophysiology and Approach to Diagnosis of G6pd Deficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTE2MDczNjI4NzkxODg0)",
            "[<b>1. Patho Fee Videos - Wilms Tumor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTE3MDc1NjUzMTQ2ODEx)",
            "[<b>2. General 1. Cell - Anchoring Junction With Concepts of Bullous Lesions of Skin and Immunofluorescence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTE4MDc3Njc3NTAxNzM4)",
            "[<b>2. General 1. Cell - Cell Chromatin and Epigenetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTE5MDc5NzAxODU2NjY1)",
            "[<b>2. General 1. Cell - Cell to Cell Interactions Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTIwMDgxNzI2MjExNTky)",
            "[<b>2. General 1. Cell - Collagen and Some of Its Defects and Differentiation of Epidermolysis Bullosa From Bullous Pemphigoid Aiims Special Topic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTIxMDgzNzUwNTY2NTE5)",
            "[<b>2. General 1. Cell - Cytoplasmic Protiens and Focus on Immunohistochemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTIyMDg1Nzc0OTIxNDQ2)",
            "[<b>2. General 1. Cell - Extracellular Matrix Fibrillinopathies Marfan Syndrome and Stain for Elastic Fibres atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTIzMDg3Nzk5Mjc2Mzcz)",
            "[<b>2. General 1. Cell - Microtubules Ciliopathies and Cilocythopthoria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTI0MDg5ODIzNjMxMzAw)",
            "[<b>2. General 2. Cell Adaptation, Injury - Aging atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTI1MDkxODQ3OTg2MjI3)",
            "[<b>2. General 2. Cell Adaptation, Injury - Autophagy and R10 Updates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTI2MDkzODcyMzQxMTU0)",
            "[<b>2. General 2. Cell Adaptation, Injury - Causes of Cell Injury and Reversible Cell Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTI3MDk1ODk2Njk2MDgx)",
            "[<b>2. General 2. Cell Adaptation, Injury - Cell Death and Differences Between Apoptosis and Necrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTI4MDk3OTIxMDUxMDA4)",
            "[<b>2. General 2. Cell Adaptation, Injury - Cellular Accumulations Calcium and Malakoplakia and Stains atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTI5MDk5OTQ1NDA1OTM1)",
            "[<b>2. General 2. Cell Adaptation, Injury - Cellular Accumulations Fats atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTMwMTAxOTY5NzYwODYy)",
            "[<b>2. General 2. Cell Adaptation, Injury - Cellular Accumulations Pigments atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTMxMTAzOTk0MTE1Nzg5)",
            "[<b>2. General 2. Cell Adaptation, Injury - Cellular Accumulations Proteins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTMyMTA2MDE4NDcwNzE2)",
            "[<b>2. General 2. Cell Adaptation, Injury - Cellular Adaptations Part 1  Hypertrophy and Atrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTMzMTA4MDQyODI1NjQz)",
            "[<b>2. General 2. Cell Adaptation, Injury - Irreversible Cell Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTM0MTEwMDY3MTgwNTcw)",
            "[<b>2. General 2. Cell Adaptation, Injury - Necrosis Its Mechanisms and Subtypes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTM1MTEyMDkxNTM1NDk3)",
            "[<b>2. General 2. Cell Adaptation, Injury - Robbins 10Th Updates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTM2MTE0MTE1ODkwNDI0)",
            "[<b>2. General 3. Neoplasia - Cell Cycle Its Regulators Rb Gene atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTM3MTE2MTQwMjQ1MzUx)",
            "[<b>2. General 3. Neoplasia - Chemical Carcinogenesis and Ames Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTM4MTE4MTY0NjAwMjc4)",
            "[<b>2. General 3. Neoplasia - Diagnosis Part 2 Fnac atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTM5MTIwMTg4OTU1MjA1)",
            "[<b>2. General 3. Neoplasia - Diagnosis Part 3 Biopsy Special Stains and Immunohistochemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQwMTIyMjEzMzEwMTMy)",
            "[<b>2. General 3. Neoplasia - Diagnosis of Cancer Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQxMTI0MjM3NjY1MDU5)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Angiogenesis Genes Apoptotic Genes and Dna Repair Genes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQyMTI2MjYyMDE5OTg2)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Angiogenesis Genes Vhl Energy and Oncometabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQzMTI4Mjg2Mzc0OTEz)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQ0MTMwMzEwNzI5ODQw)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Metastasis and Escaping Immunity and Death and Recap atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQ1MTMyMzM1MDg0NzY3)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Proto Oncogenes Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQ2MTM0MzU5NDM5Njk0)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Proto Oncogenes Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQ3MTM2MzgzNzk0NjIx)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Proto Oncogenes Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQ4MTM4NDA4MTQ5NTQ4)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Tumor Suppressor Genes Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTQ5MTQwNDMyNTA0NDc1)",
            "[<b>2. General 3. Neoplasia - Genetic Basis of Cancer Tumor Suppressor Genes Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTUwMTQyNDU2ODU5NDAy)",
            "[<b>2. General 3. Neoplasia - Introduction to Neoplasia Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTUxMTQ0NDgxMjE0MzI5)",
            "[<b>2. General 3. Neoplasia - Microbial Carcinogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTUyMTQ2NTA1NTY5MjU2)",
            "[<b>2. General 3. Neoplasia - Radiation Carcinogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTUzMTQ4NTI5OTI0MTgz)",
            "[<b>2. General 3. Neoplasia - Recent Advances in Neoplasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTU0MTUwNTU0Mjc5MTEw)",
            "[<b>2. General 4. Genetic Disorders - Cgh and Gwasc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTU1MTUyNTc4NjM0MDM3)",
            "[<b>2. General 4. Genetic Disorders - Chromosomal Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTU2MTU0NjAyOTg4OTY0)",
            "[<b>2. General 4. Genetic Disorders - Fluorescent in Situ Hybridization Fish atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTU3MTU2NjI3MzQzODkx)",
            "[<b>2. General 4. Genetic Disorders - Gene Editing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTU4MTU4NjUxNjk4ODE4)",
            "[<b>2. General 4. Genetic Disorders - Introduction to Genetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTU5MTYwNjc2MDUzNzQ1)",
            "[<b>2. General 4. Genetic Disorders - Mendelian Disorders Autosomal Dominant Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTYwMTYyNzAwNDA4Njcy)",
            "[<b>2. General 4. Genetic Disorders - Mendelian Disorders Autosomal Recessive atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTYxMTY0NzI0NzYzNTk5)",
            "[<b>2. General 4. Genetic Disorders - Mendelian Disorders Holandric Disorders Co Dominant Pleiotrophy Genetic Heterogenetity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTYyMTY2NzQ5MTE4NTI2)",
            "[<b>2. General 4. Genetic Disorders - Mendelian Disorders X Linked Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTYzMTY4NzczNDczNDUz)",
            "[<b>2. General 4. Genetic Disorders - Microarray atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTY0MTcwNzk3ODI4Mzgw)",
            "[<b>2. General 4. Genetic Disorders - Mlpa Jist of All Techniques atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTY1MTcyODIyMTgzMzA3)",
            "[<b>2. General 4. Genetic Disorders - Molecular Techniques in Genetics Basics and Karyotyping atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTY2MTc0ODQ2NTM4MjM0)",
            "[<b>2. General 4. Genetic Disorders - Multifactorial Inheritance Polymorphisms and Linkage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTY3MTc2ODcwODkzMTYx)",
            "[<b>2. General 4. Genetic Disorders - Non Mendelian Disorders Genomic Imprinting atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTY4MTc4ODk1MjQ4MDg4)",
            "[<b>2. General 4. Genetic Disorders - Non Mendelian Disorders Gonadal Mosacism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTY5MTgwOTE5NjAzMDE1)",
            "[<b>2. General 4. Genetic Disorders - Non Mendelian Disorders Mitochondrial Inheritance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTcwMTgyOTQzOTU3OTQy)",
            "[<b>2. General 4. Genetic Disorders - Non Mendelian Disorders Trinucleotide Repeat Inheritence and Fragile X Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTcxMTg0OTY4MzEyODY5)",
            "[<b>2. General 4. Genetic Disorders - Pcr and Other Molecular Techniques atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTcyMTg2OTkyNjY3Nzk2)",
            "[<b>2. General 4. Genetic Disorders - Understanding Pedigree Analysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTczMTg5MDE3MDIyNzIz)",
            "[<b>2. General 5. Inflammation - Cellular Mediators Ibq Mast Cell atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTc0MTkxMDQxMzc3NjUw)",
            "[<b>2. General 5. Inflammation - Chronic Inflammation Types of Macrophages and Giant Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTc1MTkzMDY1NzMyNTc3)",
            "[<b>2. General 5. Inflammation - Classification of Inflammation and Mechanism of Inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTc2MTk1MDkwMDg3NTA0)",
            "[<b>2. General 5. Inflammation - Diagnosis of Inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTc3MTk3MTE0NDQyNDMx)",
            "[<b>2. General 5. Inflammation - Disease of Inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTc4MTk5MTM4Nzk3MzU4)",
            "[<b>2. General 5. Inflammation - Mechanism of Inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTc5MjAxMTYzMTUyMjg1)",
            "[<b>2. General 5. Inflammation - Morphological Features of Inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTgwMjAzMTg3NTA3MjEy)",
            "[<b>2. General 5. Inflammation - Plasma Mediators With Complement Opathies Aiims Highlight Topic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTgxMjA1MjExODYyMTM5)",
            "[<b>2. General 5. Inflammation - Repair and Regeneration and Their Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTgyMjA3MjM2MjE3MDY2)",
            "[<b>2. General 5. Inflammation - Rosai Dorfman Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTgzMjA5MjYwNTcxOTkz)",
            "[<b>2. General 5. Inflammation - Types of Granulomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTg0MjExMjg0OTI2OTIw)",
            "[<b>2. General 6. Immunity - Adaptive Immunity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTg1MjEzMzA5MjgxODQ3)",
            "[<b>2. General 6. Immunity - Amyloidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTg2MjE1MzMzNjM2Nzc0)",
            "[<b>2. General 6. Immunity - Basic Function of Immunity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTg3MjE3MzU3OTkxNzAx)",
            "[<b>2. General 6. Immunity - Bruton Agammaglobulinemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTg4MjE5MzgyMzQ2NjI4)",
            "[<b>2. General 6. Immunity - Digeorge Syndrome and Recap of Lymphocyte Maturation Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTg5MjIxNDA2NzAxNTU1)",
            "[<b>2. General 6. Immunity - Graft Rejection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTkwMjIzNDMxMDU2NDgy)",
            "[<b>2. General 6. Immunity - Hyper Igm Syndrome Isolated Iga Defect X Linked Lymphoproliferative Disorder and Recap of All Immunodeficiency Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTkxMjI1NDU1NDExNDA5)",
            "[<b>2. General 6. Immunity - Hypersensitivity Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTkyMjI3NDc5NzY2MzM2)",
            "[<b>2. General 6. Immunity - Immunodeficiency Diseases Classification Detailed Overview of Scid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTkzMjI5NTA0MTIxMjYz)",
            "[<b>2. General 6. Immunity - Immunodeficiency Diseases Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTk0MjMxNTI4NDc2MTkw)",
            "[<b>2. General 6. Immunity - Innate Immunity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTk1MjMzNTUyODMxMTE3)",
            "[<b>2. General 6. Immunity - Interaction of B Cell T Cell Hyper Igm Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTk2MjM1NTc3MTg2MDQ0)",
            "[<b>2. General 6. Immunity - Lymphocyte Activation Defects Classification and Common Variable Immunodeficiency Cvid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTk3MjM3NjAxNTQwOTcx)",
            "[<b>2. General 6. Immunity - Mhc and Its Matching atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTk4MjM5NjI1ODk1ODk4)",
            "[<b>2. General 6. Immunity - Must Know Hiv in Hiv atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTExOTk5MjQxNjUwMjUwODI1)",
            "[<b>2. General 6. Immunity - Natural Killer Cells Nk Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDAwMjQzNjc0NjA1NzUy)",
            "[<b>2. General 6. Immunity - Preventing Graft Rejection and Gvhd Gvl atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDAxMjQ1Njk4OTYwNjc5)",
            "[<b>2. General 6. Immunity - Tolerance and Its Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDAyMjQ3NzIzMzE1NjA2)",
            "[<b>2. General 6. Immunity - Wiskott Aldrich Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDAzMjQ5NzQ3NjcwNTMz)",
            "[<b>2. General 7. Hemodynamics - Difference Between Hyperemia and Congestion With Emphasis on All Types of Cvc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDA0MjUxNzcyMDI1NDYw)",
            "[<b>2. General 7. Hemodynamics - Embolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDA1MjUzNzk2MzgwMzg3)",
            "[<b>2. General 7. Hemodynamics - Infarcts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDA2MjU1ODIwNzM1MzE0)",
            "[<b>2. General 7. Hemodynamics - Shock atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDA3MjU3ODQ1MDkwMjQx)",
            "[<b>2. General 7. Hemodynamics - Virchow Triad atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDA4MjU5ODY5NDQ1MTY4)",
            "[<b>3. Cardiovascular System - Hypertrophic Obstructive Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDA5MjYxODkzODAwMDk1)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Alzheimer Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDEwMjYzOTE4MTU1MDIy)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Approach to Cns Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDExMjY1OTQyNTA5OTQ5)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Basic Introduction With Focus on Glial Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDEyMjY3OTY2ODY0ODc2)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Cns Hemorrhage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDEzMjY5OTkxMjE5ODAz)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Craniopharyngioma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDE0MjcyMDE1NTc0NzMw)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Csf Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDE1Mjc0MDM5OTI5NjU3)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Focus on Neuronal Cells Its Inclusions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDE2Mjc2MDY0Mjg0NTg0)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Metastasis Meningioma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDE3Mjc4MDg4NjM5NTEx)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Nerve Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDE4MjgwMTEyOTk0NDM4)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Oligodendroglioma and Updates on Gloma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDE5MjgyMTM3MzQ5MzY1)",
            "[<b>4. Systemic 1. Central Nervous System and Its Disorders - Prion Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDIwMjg0MTYxNzA0Mjky)",
            "[<b>4. Systemic 2. Git - Basic Understanding of Git atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDIxMjg2MTg2MDU5MjE5)",
            "[<b>4. Systemic 2. Git - Carcinoma of Colon and Anal Canal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDIyMjg4MjEwNDE0MTQ2)",
            "[<b>4. Systemic 2. Git - Esophagus Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDIzMjkwMjM0NzY5MDcz)",
            "[<b>4. Systemic 2. Git - Esophagus Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDI0MjkyMjU5MTI0MDAw)",
            "[<b>4. Systemic 2. Git - Esophagus Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDI1Mjk0MjgzNDc4OTI3)",
            "[<b>4. Systemic 2. Git - Gastric Polyps and Stomach Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDI2Mjk2MzA3ODMzODU0)",
            "[<b>4. Systemic 2. Git - Gastritis Gastric Ulcer and H Pylori atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDI3Mjk4MzMyMTg4Nzgx)",
            "[<b>4. Systemic 2. Git - Hirschsprung Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDI4MzAwMzU2NTQzNzA4)",
            "[<b>4. Systemic 2. Git - Inflammatory Bowel Disease and Detailed Discussion of Chrons Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDI5MzAyMzgwODk4NjM1)",
            "[<b>4. Systemic 2. Git - Intestinal Polyps and Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDMwMzA0NDA1MjUzNTYy)",
            "[<b>4. Systemic 2. Git - Malabsorbtion Syndromes With Focus on Celiac Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDMxMzA2NDI5NjA4NDg5)",
            "[<b>4. Systemic 2. Git - Malabsorption Syndromes With Focus on Whipple Disease and Tropical Sprue atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDMyMzA4NDUzOTYzNDE2)",
            "[<b>4. Systemic 2. Git - Overview of Ibd and Detailed Discussion of Ulcerative Colitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDMzMzEwNDc4MzE4MzQz)",
            "[<b>4. Systemic 2. Git - Ulcers of Intestine With Importance on Pseudomemenranous Colitis Jipmer Focus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDM0MzEyNTAyNjczMjcw)",
            "[<b>4. Systemic 2. Git - Unusual Causes of Malabsorption Aiims Highlight Topic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDM1MzE0NTI3MDI4MTk3)",
            "[<b>4. Systemic 3. Breast - Basics of Breast Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDM2MzE2NTUxMzgzMTI0)",
            "[<b>4. Systemic 3. Breast - Basics of Breast atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDM3MzE4NTc1NzM4MDUx)",
            "[<b>4. Systemic 3. Breast - Breast Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDM4MzIwNjAwMDkyOTc4)",
            "[<b>4. Systemic 3. Breast - Classification of Breast Lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDM5MzIyNjI0NDQ3OTA1)",
            "[<b>4. Systemic 3. Breast - Fibrocystic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQwMzI0NjQ4ODAyODMy)",
            "[<b>4. Systemic 3. Breast - Fibroepithelial Lesions With Emphasis on Fibroadenoma and Phyllodes Tumor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQxMzI2NjczMTU3NzU5)",
            "[<b>4. Systemic 3. Breast - In Situ Lesions Dcis Lcis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQyMzI4Njk3NTEyNjg2)",
            "[<b>4. Systemic 3. Breast - Inflammatory Lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQzMzMwNzIxODY3NjEz)",
            "[<b>4. Systemic 3. Breast - Proliferative Breast Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQ0MzMyNzQ2MjIyNTQw)",
            "[<b>4. Systemic 4. Male Genital System - Classification of Testicular Tumors Continued and Seminoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQ1MzM0NzcwNTc3NDY3)",
            "[<b>4. Systemic 4. Male Genital System - Gonadoblastoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQ2MzM2Nzk0OTMyMzk0)",
            "[<b>4. Systemic 4. Male Genital System - Penile Lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQ3MzM4ODE5Mjg3MzIx)",
            "[<b>4. Systemic 4. Male Genital System - Prostate Cancer and Gleason Score atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQ4MzQwODQzNjQyMjQ4)",
            "[<b>4. Systemic 4. Male Genital System - Sex Cord Tumors Testicular Lymphoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDQ5MzQyODY3OTk3MTc1)",
            "[<b>4. Systemic 4. Male Genital System - Spermatocytic Tumor and Nsgct 1 Non Seminomatous Gct atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDUwMzQ0ODkyMzUyMTAy)",
            "[<b>4. Systemic 4. Male Genital System - Understanding Basic Testis Structure Gcnis and Classification of Testicular Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDUxMzQ2OTE2NzA3MDI5)",
            "[<b>4. Systemic 5. Female Genital System - Classification of Ovarian Cancers in Detail atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDUyMzQ4OTQxMDYxOTU2)",
            "[<b>4. Systemic 5. Female Genital System - Endometrium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDUzMzUwOTY1NDE2ODgz)",
            "[<b>4. Systemic 5. Female Genital System - Gestational Trophoblastic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDU0MzUyOTg5NzcxODEw)",
            "[<b>4. Systemic 5. Female Genital System - Myometrium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDU1MzU1MDE0MTI2NzM3)",
            "[<b>4. Systemic 5. Female Genital System - Pap Smear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDU2MzU3MDM4NDgxNjY0)",
            "[<b>4. Systemic 5. Female Genital System - Vaginal Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDU3MzU5MDYyODM2NTkx)",
            "[<b>4. Systemic 5. Female Genital System - Vulva atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDU4MzYxMDg3MTkxNTE4)",
            "[<b>4. Systemic 5. Female Genital System - Who Classification of Ovarian Malignancies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDU5MzYzMTExNTQ2NDQ1)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Arrythmogenic Right Ventricular atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDYwMzY1MTM1OTAxMzcy)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Cardiac Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDYxMzY3MTYwMjU2Mjk5)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Dilated Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDYyMzY5MTg0NjExMjI2)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDYzMzcxMjA4OTY2MTUz)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Myocardial Infarction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDY0MzczMjMzMzIxMDgw)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Restrictive Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDY1Mzc1MjU3Njc2MDA3)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Rheumatic Heart Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDY2Mzc3MjgyMDMwOTM0)",
            "[<b>4. Systemic 6. Cardiovascular System and Its Disorders - Understanding Cardiomyopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDY3Mzc5MzA2Mzg1ODYx)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Alcoholic Liver Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDY4MzgxMzMwNzQwNzg4)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Approach to Jaundice atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDY5MzgzMzU1MDk1NzE1)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Autoimmune Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDcwMzg1Mzc5NDUwNjQy)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Cirrhosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDcxMzg3NDAzODA1NTY5)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Hepatic Adenoma Aiims atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDcyMzg5NDI4MTYwNDk2)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Introduction to Liver atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDczMzkxNDUyNTE1NDIz)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Liver Function Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDc0MzkzNDc2ODcwMzUw)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Nafld Non Alcoholic Fatty Liver Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDc1Mzk1NTAxMjI1Mjc3)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Neonatal Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDc2Mzk3NTI1NTgwMjA0)",
            "[<b>4. Systemic 7. Liver Gallbladder Pancreas and Its Disorders - Nodules of Liver atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDc3Mzk5NTQ5OTM1MTMx)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Amyloid Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDc4NDAxNTc0MjkwMDU4)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Crystals in Urine Casts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDc5NDAzNTk4NjQ0OTg1)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Diabetic Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDgwNDA1NjIyOTk5OTEy)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Electron Microscopy of Kidney Understanding With Images atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDgxNDA3NjQ3MzU0ODM5)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Focal Segmental Glomerulosclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDgyNDA5NjcxNzA5NzY2)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Iga Nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDgzNDExNjk2MDY0Njkz)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Immunofluorescence in Kidney Aiims Highlight Topics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDg0NDEzNzIwNDE5NjIw)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Membranoproliferative Glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDg1NDE1NzQ0Nzc0NTQ3)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Membranous Nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDg2NDE3NzY5MTI5NDc0)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Minimal Change Disease Nephrotic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDg3NDE5NzkzNDg0NDAx)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Nephritic Syndrome Clinical Features Urine Findings atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDg4NDIxODE3ODM5MzI4)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Nephrotic Syndrome Clinical Features Genes Urine Findings atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDg5NDIzODQyMTk0MjU1)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Pathophysiology of Glomerular Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDkwNDI1ODY2NTQ5MTgy)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Polyomavirus Tb Kidney Malakoplakia Aiims Highlight Topics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDkxNDI3ODkwOTA0MTA5)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Post Streptococcal Glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDkyNDI5OTE1MjU5MDM2)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Rapidly Progressive Glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDkzNDMxOTM5NjEzOTYz)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Renal Tumors in Adults atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDk0NDMzOTYzOTY4ODkw)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Sle Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDk1NDM1OTg4MzIzODE3)",
            "[<b>4. Systemic 8. Renal System and Its Disorders - Wilms Tumor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDk2NDM4MDEyNjc4NzQ0)",
            "[<b>4. Systemic 10. Respiratory System - Ards Acute Respiratory Distress Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDk3NDQwMDM3MDMzNjcx)",
            "[<b>4. Systemic 10. Respiratory System - Basics of Respiratory System Alveoli Bronchi With Images atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDk4NDQyMDYxMzg4NTk4)",
            "[<b>4. Systemic 10. Respiratory System - Benign Lung Tumours Unsual Tumours of Lung atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMDk5NDQ0MDg1NzQzNTI1)",
            "[<b>4. Systemic 10. Respiratory System - Copd Chronic Bronchitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTAwNDQ2MTEwMDk4NDUy)",
            "[<b>4. Systemic 10. Respiratory System - Lung Tumour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTAxNDQ4MTM0NDUzMzc5)",
            "[<b>4. Systemic 10. Respiratory System - Obstructive Lung Disease With Focus on Emphysema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTAyNDUwMTU4ODA4MzA2)",
            "[<b>4. Systemic 10. Respiratory System - Obstructive Lung Diseases Bronchiectasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTAzNDUyMTgzMTYzMjMz)",
            "[<b>4. Systemic 10. Respiratory System - Obstructive Lung Diseases Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTA0NDU0MjA3NTE4MTYw)",
            "[<b>4. Systemic 10. Respiratory System - Pneumonia With Special Types of Fungal Pneumonias and Pneumocystis Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTA1NDU2MjMxODczMDg3)",
            "[<b>4. Systemic 10. Respiratory System - Restrictive Lung Disease Classification Except Pneumoconiosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTA2NDU4MjU2MjI4MDE0)",
            "[<b>4. Systemic 10. Respiratory System - Restrictive Lung Disease With Focus on Pneumoconiosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTA3NDYwMjgwNTgyOTQx)",
            "[<b>4. Systemic 10. Respiratory System - Restrictive Lung Disease Fibrosing Rld and Honeycomb Lung atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTA4NDYyMzA0OTM3ODY4)",
            "[<b>4. Systemic 10. Respiratory System - Pneumonia With Special Types of Pneumonias Aspiration Pneumonia Golden Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTA5NDY0MzI5MjkyNzk1)",
            "[<b>4. Systemic 10. Respiratory System - Restrictive Lung Disease Part 3 Sarcoidosis and Its Differentials atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTEwNDY2MzUzNjQ3NzIy)",
            "[<b>4. Systemic 11. Blood Vessels - Basics of Blood Vessels atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTExNDY4Mzc4MDAyNjQ5)",
            "[<b>4. Systemic 11. Blood Vessels - Benign Vascular Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTEyNDcwNDAyMzU3NTc2)",
            "[<b>4. Systemic 11. Blood Vessels - Blood Vessels Anomalies and Abnormalities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTEzNDcyNDI2NzEyNTAz)",
            "[<b>4. Systemic 11. Blood Vessels - Dissection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTE0NDc0NDUxMDY3NDMw)",
            "[<b>4. Systemic 11. Blood Vessels - Kaposi Sarcoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTE1NDc2NDc1NDIyMzU3)",
            "[<b>4. Systemic 11. Blood Vessels - Large Vessel Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTE2NDc4NDk5Nzc3Mjg0)",
            "[<b>4. Systemic 11. Blood Vessels - Aneurysm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTE3NDgwNTI0MTMyMjEx)",
            "[<b>4. Systemic 11. Blood Vessels - Blood Vessel Tumors Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTE4NDgyNTQ4NDg3MTM4)",
            "[<b>4. Systemic 11. Blood Vessels - Malignant Vascular Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTE5NDg0NTcyODQyMDY1)",
            "[<b>4. Systemic 11. Blood Vessels - Medium Vessel Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTIwNDg2NTk3MTk2OTky)",
            "[<b>4. Systemic 11. Blood Vessels - Small Vessel Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTIxNDg4NjIxNTUxOTE5)",
            "[<b>4. Systemic 11. Blood Vessels - Sclerosis With Highlight on Atherosclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTIyNDkwNjQ1OTA2ODQ2)",
            "[<b>4. Systemic 11. Blood Vessels - Vasculitis Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTIzNDkyNjcwMjYxNzcz)",
            "[<b>4. Systemic 11. Blood Vessels - Vasculitis Special Types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTI0NDk0Njk0NjE2NzAw)",
            "[<b>4. Systemic 12. Skin - Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTI1NDk2NzE4OTcxNjI3)",
            "[<b>4. Systemic 12. Skin - Bullous Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTI2NDk4NzQzMzI2NTU0)",
            "[<b>4. Systemic 12. Skin - Infections of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTI3NTAwNzY3NjgxNDgx)",
            "[<b>4. Systemic 12. Skin - Inflammatory Dermatos Including Psoriasis and Lichen Planus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTI4NTAyNzkyMDM2NDA4)",
            "[<b>4. Systemic 12. Skin - Pigmentary Disorders of Skin Including Nevus and Melanoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTI5NTA0ODE2MzkxMzM1)",
            "[<b>4. Systemic 12. Skin - Tumors of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTMwNTA2ODQwNzQ2MjYy)",
            "[<b>4. Systemic 13. Head and Neck - Head Neck atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTMxNTA4ODY1MTAxMTg5)",
            "[<b>4. Systemic 13. Head and Neck - Malignant Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTMyNTEwODg5NDU2MTE2)",
            "[<b>4. Systemic 13. Head and Neck - Salivary Gland Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTMzNTEyOTEzODExMDQz)",
            "[<b>4. Systemic 13. Head and Neck - Salivary Gland Quiz atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTM0NTE0OTM4MTY1OTcw)",
            "[<b>4. Systemic 13. Head and Neck - Salivary Gland Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTM1NTE2OTYyNTIwODk3)",
            "[<b>4. Systemic 14. Bone Tumors in Jist - Bone Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTM2NTE4OTg2ODc1ODI0)",
            "[<b>4. Systemic 15. Pancreas - Classification of Cystic Lesions of Pancreas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTM3NTIxMDExMjMwNzUx)",
            "[<b>5. Endocrine 1. Endocrine System and Its Disorders - Pituitary atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTM4NTIzMDM1NTg1Njc4)",
            "[<b>Basics of Thyroid With Emphasis on Graves Disease and Thyroiditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTM5NTI1MDU5OTQwNjA1)",
            "[<b>Malignancy of Thyroid With Emphasis on Molecular Classification of Follicular Neoplasms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQwNTI3MDg0Mjk1NTMy)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Alpha Thalassemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQxNTI5MTA4NjUwNDU5)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Approach to Anemia With Emphasis on Approach to Hemolytic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQyNTMxMTMzMDA1Mzg2)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Approach to Anemia and Understanding Mch Mchc Rdw Red Cell Parameters Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQzNTMzMTU3MzYwMzEz)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Approach to Microcytic Hypochromic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQ0NTM1MTgxNzE1MjQw)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Autoimmune Hemolytic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQ1NTM3MjA2MDcwMTY3)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Diagnosis of Thalassemia in Jist and Alkali Denaturation Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQ2NTM5MjMwNDI1MDk0)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Genetics of B Thalassemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQ3NTQxMjU0NzgwMDIx)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Hypoproliferative Anemias Aplastic Anemia and Pure Red Cell Aplasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQ4NTQzMjc5MTM0OTQ4)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Macrocytic Anemia With Focus on Megaloblastic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTQ5NTQ1MzAzNDg5ODc1)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Pathophysiological Features and Diagnosis of Sickle Cell Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTUwNTQ3MzI3ODQ0ODAy)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Pathophysiology and Approach to Diagnosis of G6pd Deficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTUxNTQ5MzUyMTk5NzI5)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Pathophysiology and Approach to Diagnosis of Pnh atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTUyNTUxMzc2NTU0NjU2)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Pathophysiology and Approach to Diagnosis of Spherocytosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTUzNTUzNDAwOTA5NTgz)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Red Cell Inclusions Aiims atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTU0NTU1NDI1MjY0NTEw)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Red Cell Membrane Abnormalities Jipmer and Aiims atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTU1NTU3NDQ5NjE5NDM3)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Sideroblastic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTU2NTU5NDczOTc0MzY0)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Thalassemia Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTU3NTYxNDk4MzI5Mjkx)",
            "[<b>6. Hematology - 1. Red Blood Cells and Its Disorders - Understanding Sickle Cell Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTU4NTYzNTIyNjg0MjE4)",
            "[<b>APLA_and_Factor_8_Inhibitors_Concept_of_Mixing_Studies_and_Reptilase atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTU5NTY1NTQ3MDM5MTQ1)",
            "[<b>Approach-To-Secondary-Hemostatic-Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTYwNTY3NTcxMzk0MDcy)",
            "[<b>Approach-to-Fibrinolytic-System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTYxNTY5NTk1NzQ4OTk5)",
            "[<b>Approach_to_Anticoagulant_Molecules_with_Special_Emphasis_on_Factor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTYyNTcxNjIwMTAzOTI2)",
            "[<b>Approach_to_Primary_Hemostatic_Disorders_and_Platelet_Aggregometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTYzNTczNjQ0NDU4ODUz)",
            "[<b>Idiopathic-Thrombocytopenic-Purpura atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTY0NTc1NjY4ODEzNzgw)",
            "[<b>Platelets-and-Coagulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTY1NTc3NjkzMTY4NzA3)",
            "[<b>Thrombotic_Microangiopathies_Microangiopathic_Hemolytic_Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTY2NTc5NzE3NTIzNjM0)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Acute Myeloid Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTY3NTgxNzQxODc4NTYx)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Approach to B Cell Lymphoma Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTY4NTgzNzY2MjMzNDg4)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Basic Understanding of Leukemia Lymphoma and Pathogenesis of Acute Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTY5NTg1NzkwNTg4NDE1)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Basis of Chronic Leukemia and Lymphomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTcwNTg3ODE0OTQzMzQy)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Chronic Lymphocytic Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTcxNTg5ODM5Mjk4MjY5)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Chronic Myeloproliferative Neoplasms Chronic Myeloid Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTcyNTkxODYzNjUzMTk2)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Classification and Clinical Features of Acute Lymphoblastic Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTczNTkzODg4MDA4MTIz)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Flow Cytometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTc0NTk1OTEyMzYzMDUw)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Heavy Chain Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTc1NTk3OTM2NzE3OTc3)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Hodgkin Lymphoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTc2NTk5OTYxMDcyOTA0)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Images of Mature White Blood Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTc3NjAxOTg1NDI3ODMx)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Introduction to Wbc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTc4NjA0MDA5NzgyNzU4)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Langerhans Cell Histiocytosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTc5NjA2MDM0MTM3Njg1)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Mds atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTgwNjA4MDU4NDkyNjEy)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - Monoclonal Gammopathy Myeloma and Waldenstrom Macroglobulinemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTgxNjEwMDgyODQ3NTM5)",
            "[<b>6. Hematology - 3. White Blood Cells and Its Disorders - T Cell Lympoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTgyNjEyMTA3MjAyNDY2)",
            "[<b>6. Hematology - 4. Techniques in Haematology - Anticoagulants and Vacutainers in Haematology and Blood Banking Aiims atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTgzNjE0MTMxNTU3Mzkz)",
            "[<b>6. Hematology - 4. Techniques in Haematology - Basics of Normal Bone Marrow Topography and Needles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTg0NjE2MTU1OTEyMzIw)",
            "[<b>7. Blood Banking, Blood Grouping - Abo Rh Kell Lewis Duffy Blood Groups and Methods of Blood Grouping atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTg1NjE4MTgwMjY3MjQ3)",
            "[<b>7. Blood Banking, Blood Grouping - Blood Bags atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTg2NjIwMjA0NjIyMTc0)",
            "[<b>7. Blood Banking, Blood Grouping - Blood Transfusion Reaction Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTg3NjIyMjI4OTc3MTAx)",
            "[<b>7. Blood Banking, Blood Grouping - Blood Transfusion Reaction Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTg4NjI0MjUzMzMyMDI4)",
            "[<b>7. Blood Banking, Blood Grouping - Questions on Blood Grouping atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTg5NjI2Mjc3Njg2OTU1)",
            "[<b>7. Blood Banking, Blood Grouping - Test for Blood Grouping atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTkwNjI4MzAyMDQxODgy)",
            "[<b>8. Techniques Section - Cytoplasmic Protiens and Focus on Immunohistochemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTkxNjMwMzI2Mzk2ODA5)",
            "[<b>8. Techniques Section - Flow Cytometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTkyNjMyMzUwNzUxNzM2)",
            "[<b>8. Techniques Section - Histopathology Fixation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTkzNjM0Mzc1MTA2NjYz)",
            "[<b>8. Techniques Section - Pap Smear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTk0NjM2Mzk5NDYxNTkw)",
            "[<b>9. Qrp - Ini Cet Qrp Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTk1NjM4NDIzODE2NTE3)",
            "[<b>9. Qrp - Pathology Session 1 by Dr Vandana Puri atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTk2NjQwNDQ4MTcxNDQ0)",
            "[<b>9. Qrp - Pathology Session 2 by Dr Vandana Puri atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTk3NjQyNDcyNTI2Mzcx)",
            "[<b>9. Qrp - Pathology by Dr Vandana Puri atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTk4NjQ0NDk2ODgxMjk4)",
            "[<b>Sinusoidal Obstruction Syndrome Sos or Vod Aiims atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMTk5NjQ2NTIxMjM2MjI1)",
            "[<b>Approach to Anemia and Understanding Hematocrit Esr and Mcv Red Cell Parameters Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjAwNjQ4NTQ1NTkxMTUy)",
            "[<b>Approach to B Cell Lymphomas Part 2 With Focus on Hairy Cell Leukemia and Castleman Disease Aiims atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjAxNjUwNTY5OTQ2MDc5)",
            "[<b>Astrocytoma With Special Mention of Pilocytic Astrocytoma and Glioblastoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjAyNjUyNTk0MzAxMDA2)",
            "[<b>Autoimmune Cholangiopathies Primary Sclerosing Cholangitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjAzNjU0NjE4NjU1OTMz)",
            "[<b>Biliary Cirrhosis Difference Between Primary and Secondary atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjA0NjU2NjQzMDEwODYw)",
            "[<b>Cellular Adaptations Part 2  Hyperplasia and Metaplasia and Questions on Cellular Adaptations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjA1NjU4NjY3MzY1Nzg3)",
            "[<b>Cholangiocarcinoma Angiosarcoma Metastasis and Hepatoblastoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjA2NjYwNjkxNzIwNzE0)",
            "[<b>Chronic Myeloproliferative Neoplasms Polycythemia Vera Essential Thrombocytosis Primary Myelofibrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjA3NjYyNzE2MDc1NjQx)",
            "[<b>Classification of Hepatitis Detailed Discussion of Viral Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjA4NjY0NzQwNDMwNTY4)",
            "[<b>Classification of Liver Tumors Cavernous Hemangioma and Differentiation From Peliosis Hepatis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjA5NjY2NzY0Nzg1NDk1)",
            "[<b>Ependymoma With Special Mention of New Who Types Chordoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjEwNjY4Nzg5MTQwNDIy)",
            "[<b>Hepatic Malignancies Hepatocellular Ca and Fibrolamellar Ca atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjExNjcwODEzNDk1MzQ5)",
            "[<b>Introduction to Red Blood Cells Precursors With Emphasis on Reticulocyte Count Assessment Supravital Stains and Its Use atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjEyNjcyODM3ODUwMjc2)",
            "[<b>Mechanism of Apoptosis and Various Types of Programmed Cell Deaths Necroptosis Pyroptosis Entosis and Net atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjEzNjc0ODYyMjA1MjAz)",
            "[<b>Neuronal Tumor Poorly Differentiated Tumors Medulloblastoma Atrt and Cns Lymphoma and Hemangic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjE0Njc2ODg2NTYwMTMw)",
            "[<b>Restrictive Lung Disease Smoking Related Rld and Pulmonary Alveolar Protienosis and Jist All of Restrictive Lung Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjE1Njc4OTEwOTE1MDU3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pathologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pathologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pathologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pathologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("microbiologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. General 1. General Micro - Bacterial Cell Anatomy Structure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjE2NjgwOTM1MjY5OTg0)",
            "[<b>1. General 1. General Micro - Bacterial Genetics Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjE3NjgyOTU5NjI0OTEx)",
            "[<b>1. General 1. General Micro - Bacterial Genetics Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjE4Njg0OTgzOTc5ODM4)",
            "[<b>1. General 1. General Micro - Bacterial Growth Curve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjE5Njg3MDA4MzM0NzY1)",
            "[<b>1. General 1. General Micro - Bacterial Spores atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjIwNjg5MDMyNjg5Njky)",
            "[<b>1. General 1. General Micro - Classification of Microbes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjIxNjkxMDU3MDQ0NjE5)",
            "[<b>1. General 1. General Micro - Introduction and Definition of Microbiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjIyNjkzMDgxMzk5NTQ2)",
            "[<b>1. General 1. General Micro - Microscope atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjIzNjk1MTA1NzU0NDcz)",
            "[<b>1. General 1. General Micro - Temperature Oxygen Carbon Dioxide Ph and Salt Requirements of Microbes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjI0Njk3MTMwMTA5NDAw)",
            "[<b>1. General 1. General Micro - Virulence Factors of Microbes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjI1Njk5MTU0NDY0MzI3)",
            "[<b>1. General 2. Stains - Differential Stains Gram Stain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjI2NzAxMTc4ODE5MjU0)",
            "[<b>1. General 2. Stains - Differential Stains Ziehl Neelsene atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjI3NzAzMjAzMTc0MTgx)",
            "[<b>1. General 2. Stains - Negative Stain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjI4NzA1MjI3NTI5MTA4)",
            "[<b>1. General 2. Stains - Silver Impregnation Stain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjI5NzA3MjUxODg0MDM1)",
            "[<b>1. General 2. Stains - Simple Stains atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjMwNzA5Mjc2MjM4OTYy)",
            "[<b>1. General 3. Sterilisation and Disinfection - Chemical Methods of Sterilization and Disinfection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjMxNzExMzAwNTkzODg5)",
            "[<b>1. General 3. Sterilisation and Disinfection - Introduction and Physical Methods Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjMyNzEzMzI0OTQ4ODE2)",
            "[<b>1. General 3. Sterilisation and Disinfection - Introduction and Physical Methods Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjMzNzE1MzQ5MzAzNzQz)",
            "[<b>2. Immunology - Active and Passive Immunity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjM0NzE3MzczNjU4Njcw)",
            "[<b>2. Immunology - Antibody Diversity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjM1NzE5Mzk4MDEzNTk3)",
            "[<b>2. Immunology - Antibody Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjM2NzIxNDIyMzY4NTI0)",
            "[<b>2. Immunology - Antibody Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjM3NzIzNDQ2NzIzNDUx)",
            "[<b>2. Immunology - Antibody Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjM4NzI1NDcxMDc4Mzc4)",
            "[<b>2. Immunology - Antigen Antibody Reactions Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjM5NzI3NDk1NDMzMzA1)",
            "[<b>2. Immunology - Antigen Antibody Reactions Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQwNzI5NTE5Nzg4MjMy)",
            "[<b>2. Immunology - Antigen Antibody Reactions Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQxNzMxNTQ0MTQzMTU5)",
            "[<b>2. Immunology - Antigen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQyNzMzNTY4NDk4MDg2)",
            "[<b>2. Immunology - Complement Proteins Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQzNzM1NTkyODUzMDEz)",
            "[<b>2. Immunology - Complement Proteins Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQ0NzM3NjE3MjA3OTQw)",
            "[<b>2. Immunology - Generation of Th1 Th2 Cells and Pathogenesis of Hypersensitivity Reactions and Role of Tc Cells and Interplay Between Th and Tc Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQ1NzM5NjQxNTYyODY3)",
            "[<b>2. Immunology - Innate and Acquired Immunity Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQ2NzQxNjY1OTE3Nzk0)",
            "[<b>2. Immunology - Innate and Acquired Immunity Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQ3NzQzNjkwMjcyNzIx)",
            "[<b>2. Immunology - Introduction to Immunology Innate and Acquired Immunity Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQ4NzQ1NzE0NjI3NjQ4)",
            "[<b>2. Immunology - Members of Acquired Immunity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjQ5NzQ3NzM4OTgyNTc1)",
            "[<b>2. Immunology - Mhc Complex and Antigen Processing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjUwNzQ5NzYzMzM3NTAy)",
            "[<b>2. Immunology - Superantigen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjUxNzUxNzg3NjkyNDI5)",
            "[<b>2. Immunology - Td and Ti Antigens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjUyNzUzODEyMDQ3MzU2)",
            "[<b>2. Immunology - Tolerance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjUzNzU1ODM2NDAyMjgz)",
            "[<b>2. Immunology - Type 1 Hypersensitivity Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjU0NzU3ODYwNzU3MjEw)",
            "[<b>2. Immunology - Type 2 Hypersensitivity Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjU1NzU5ODg1MTEyMTM3)",
            "[<b>2. Immunology - Type 3 Hypersensitivity Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjU2NzYxOTA5NDY3MDY0)",
            "[<b>2. Immunology - Type 4 Hypersensitivity Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjU3NzYzOTMzODIxOTkx)",
            "[<b>3. Bacteriology - 1. Organisms Not Seen on Gram Stain - Organisms Not Seen on Gram Stain Chlamydiae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjU4NzY1OTU4MTc2OTE4)",
            "[<b>3. Bacteriology - 1. Organisms Not Seen on Gram Stain - Organisms Not Seen on Gram Stain Mycoplasma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjU5NzY3OTgyNTMxODQ1)",
            "[<b>3. Bacteriology - 1. Organisms Not Seen on Gram Stain - Organisms Not Seen on Gram Stain Rickettsiae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjYwNzcwMDA2ODg2Nzcy)",
            "[<b>3. Bacteriology - 1. Organisms Not Seen on Gram Stain - Organisms Not Seen on Gram Stain Spirochaetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjYxNzcyMDMxMjQxNjk5)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Escherichia Coli atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjYyNzc0MDU1NTk2NjI2)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Klebsiellae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjYzNzc2MDc5OTUxNTUz)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Proteus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjY0Nzc4MTA0MzA2NDgw)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Salmonella atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjY1NzgwMTI4NjYxNDA3)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Serratia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjY2NzgyMTUzMDE2MzM0)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Shigella atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjY3Nzg0MTc3MzcxMjYx)",
            "[<b>3. Bacteriology - 2. Enterobacteriaceae Family - Yersinia Pestis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjY4Nzg2MjAxNzI2MTg4)",
            "[<b>3. Bacteriology - 3. Gram Positive Spore Bearing Rods - Bacillus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjY5Nzg4MjI2MDgxMTE1)",
            "[<b>3. Bacteriology - 3. Gram Positive Spore Bearing Rods - Clostridium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjcwNzkwMjUwNDM2MDQy)",
            "[<b>3. Bacteriology - 4. Gram Positive Non Sporing Rods - Corynebacterium Diphtheriae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjcxNzkyMjc0NzkwOTY5)",
            "[<b>3. Bacteriology - 4. Gram Positive Non Sporing Rods - Listeria Monocytogenes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjcyNzk0Mjk5MTQ1ODk2)",
            "[<b>Gram Positive Filamentous Bacteria Nocardia and Actinomyces atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjczNzk2MzIzNTAwODIz)",
            "[<b>3. Bacteriology - 6. Gram Negative Cocci Neisseria - Gram Negative Cocci Neisseria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjc0Nzk4MzQ3ODU1NzUw)",
            "[<b>3. Bacteriology - 7. Gram Positive Cocci - Staphylococcus Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjc1ODAwMzcyMjEwNjc3)",
            "[<b>3. Bacteriology - 7. Gram Positive Cocci - Staphylococcus Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjc2ODAyMzk2NTY1NjA0)",
            "[<b>3. Bacteriology - 7. Gram Positive Cocci - Streptococcus Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjc3ODA0NDIwOTIwNTMx)",
            "[<b>3. Bacteriology - 7. Gram Positive Cocci - Streptococcus Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjc4ODA2NDQ1Mjc1NDU4)",
            "[<b>3. Bacteriology - 7. Gram Positive Cocci - Streptococcus Pneumoniae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjc5ODA4NDY5NjMwMzg1)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Bordetella Pertussis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjgwODEwNDkzOTg1MzEy)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Brucella atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjgxODEyNTE4MzQwMjM5)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Campylobacter Jejuni atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjgyODE0NTQyNjk1MTY2)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Haemophilus Aegyptius and H Ducreyi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjgzODE2NTY3MDUwMDkz)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Haemophilus Influenzae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjg0ODE4NTkxNDA1MDIw)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Helicobacter Pylori atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjg1ODIwNjE1NzU5OTQ3)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Pseudomonas Aeruginosa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjg2ODIyNjQwMTE0ODc0)",
            "[<b>3. Bacteriology - 8. Gram Negative Oxidase Positive Rods Coccobacilli - Vibrio Cholerae Halophilic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjg3ODI0NjY0NDY5ODAx)",
            "[<b>3. Bacteriology - 9. Mycobacteria - Atypical Mycobacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjg4ODI2Njg4ODI0NzI4)",
            "[<b>3. Bacteriology - 9. Mycobacteria - Mycobacterium Leprae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjg5ODI4NzEzMTc5NjU1)",
            "[<b>3. Bacteriology - 9. Mycobacteria - Mycobacterium Tuberculosis Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjkwODMwNzM3NTM0NTgy)",
            "[<b>3. Bacteriology - 9. Mycobacteria - Mycobacterium Tuberculosis Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjkxODMyNzYxODg5NTA5)",
            "[<b>4. Clinical Mycology - Introduction to Medical Mycology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjkyODM0Nzg2MjQ0NDM2)",
            "[<b>4. Clinical Mycology - Opportunistic Mycoses Aspergillosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjkzODM2ODEwNTk5MzYz)",
            "[<b>4. Clinical Mycology - Opportunistic Mycoses Candidiasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjk0ODM4ODM0OTU0Mjkw)",
            "[<b>4. Clinical Mycology - Opportunistic Mycoses Cryptococcosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjk1ODQwODU5MzA5MjE3)",
            "[<b>4. Clinical Mycology - Opportunistic Mycoses Pneumocystosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjk2ODQyODgzNjY0MTQ0)",
            "[<b>4. Clinical Mycology - Opportunistic Mycoses Zygomycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjk3ODQ0OTA4MDE5MDcx)",
            "[<b>4. Clinical Mycology - Subcutaneous Mycoses Chromoblastomycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjk4ODQ2OTMyMzczOTk4)",
            "[<b>4. Clinical Mycology - Subcutaneous Mycoses Mycetoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMjk5ODQ4OTU2NzI4OTI1)",
            "[<b>4. Clinical Mycology - Subcutaneous Mycoses Rhinosporidiosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzAwODUwOTgxMDgzODUy)",
            "[<b>4. Clinical Mycology - Subcutaneous Mycoses Sporotrichosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzAxODUzMDA1NDM4Nzc5)",
            "[<b>4. Clinical Mycology - Superficial Mycoses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzAyODU1MDI5NzkzNzA2)",
            "[<b>4. Clinical Mycology - Systemic Mycoses Blastomycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzAzODU3MDU0MTQ4NjMz)",
            "[<b>4. Clinical Mycology - Systemic Mycoses Coccidioidomycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzA0ODU5MDc4NTAzNTYw)",
            "[<b>4. Clinical Mycology - Systemic Mycoses Histoplasmosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzA1ODYxMTAyODU4NDg3)",
            "[<b>4. Clinical Mycology - Systemic Mycoses Paracoccidioidomycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzA2ODYzMTI3MjEzNDE0)",
            "[<b>4. Clinical Mycology - Systemic Mycoses Penicilliosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzA3ODY1MTUxNTY4MzQx)",
            "[<b>5. Clinical Virology - Adenovirus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzA4ODY3MTc1OTIzMjY4)",
            "[<b>5. Clinical Virology - Arboviruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzA5ODY5MjAwMjc4MTk1)",
            "[<b>5. Clinical Virology - Coxsackie Viruses Enteroviruses Echoviruses Rhinoviruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzEwODcxMjI0NjMzMTIy)",
            "[<b>5. Clinical Virology - Hepatitis Viruses Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzExODczMjQ4OTg4MDQ5)",
            "[<b>5. Clinical Virology - Hepatitis Viruses Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzEyODc1MjczMzQyOTc2)",
            "[<b>5. Clinical Virology - Hepatitis Viruses Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzEzODc3Mjk3Njk3OTAz)",
            "[<b>5. Clinical Virology - Herpes Viruses Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzE0ODc5MzIyMDUyODMw)",
            "[<b>5. Clinical Virology - Herpes Viruses Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzE1ODgxMzQ2NDA3NzU3)",
            "[<b>5. Clinical Virology - Herpes Viruses Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzE2ODgzMzcwNzYyNjg0)",
            "[<b>5. Clinical Virology - Herpes Viruses Part 4 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzE3ODg1Mzk1MTE3NjEx)",
            "[<b>5. Clinical Virology - Herpes Viruses Part 5 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzE4ODg3NDE5NDcyNTM4)",
            "[<b>5. Clinical Virology - Hiv atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzE5ODg5NDQzODI3NDY1)",
            "[<b>5. Clinical Virology - Human Papillomavirus Hpv atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzIwODkxNDY4MTgyMzky)",
            "[<b>5. Clinical Virology - Introduction to Rna Viruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzIxODkzNDkyNTM3MzE5)",
            "[<b>5. Clinical Virology - Introduction to Virology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzIyODk1NTE2ODkyMjQ2)",
            "[<b>5. Clinical Virology - Myxoviruses Orthomyxoviruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzIzODk3NTQxMjQ3MTcz)",
            "[<b>5. Clinical Virology - Paramyxoviruses Measles Virus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzI0ODk5NTY1NjAyMTAw)",
            "[<b>5. Clinical Virology - Paramyxoviruses Mumps Virus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzI1OTAxNTg5OTU3MDI3)",
            "[<b>5. Clinical Virology - Paramyxoviruses Respiratory Syncytial Virus Parainfluenza Viruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzI2OTAzNjE0MzExOTU0)",
            "[<b>5. Clinical Virology - Parvovirus B19 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzI3OTA1NjM4NjY2ODgx)",
            "[<b>5. Clinical Virology - Poliovirus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzI4OTA3NjYzMDIxODA4)",
            "[<b>5. Clinical Virology - Poxviruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzI5OTA5Njg3Mzc2NzM1)",
            "[<b>5. Clinical Virology - Rabies Virus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzMwOTExNzExNzMxNjYy)",
            "[<b>5. Clinical Virology - Rubella Virus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzMxOTEzNzM2MDg2NTg5)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Babesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzMyOTE1NzYwNDQxNTE2)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Entamoeba Histolytica atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzMzOTE3Nzg0Nzk2NDQz)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Free Living Amoeba atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzM0OTE5ODA5MTUxMzcw)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Giardia Lamblia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzM1OTIxODMzNTA2Mjk3)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Introduction to Parasitology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzM2OTIzODU3ODYxMjI0)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Leishmaniae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzM3OTI1ODgyMjE2MTUx)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Plasmodium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzM4OTI3OTA2NTcxMDc4)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Toxoplasma Gondii atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzM5OTI5OTMwOTI2MDA1)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Trichomonas Vaginalis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQwOTMxOTU1MjgwOTMy)",
            "[<b>6. Clinical Parasitology - 1. Protozoa - Trypanosoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQxOTMzOTc5NjM1ODU5)",
            "[<b>6. Clinical Parasitology - 2. Nematodes - Large Intestinal Nematodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQyOTM2MDAzOTkwNzg2)",
            "[<b>6. Clinical Parasitology - 2. Nematodes - Small Intestinal Nematodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQzOTM4MDI4MzQ1NzEz)",
            "[<b>6. Clinical Parasitology - 2. Nematodes - Tissue Nematodes Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQ0OTQwMDUyNzAwNjQw)",
            "[<b>6. Clinical Parasitology - 2. Nematodes - Tissue Nematodes Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQ1OTQyMDc3MDU1NTY3)",
            "[<b>6. Clinical Parasitology - 2. Nematodes - Tissue Nematodes Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQ2OTQ0MTAxNDEwNDk0)",
            "[<b>6. Clinical Parasitology - 3. Cestodes - Hymenolepis Nana atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQ3OTQ2MTI1NzY1NDIx)",
            "[<b>6. Clinical Parasitology - 3. Cestodes - Echinococcus Granulosus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQ4OTQ4MTUwMTIwMzQ4)",
            "[<b>6. Clinical Parasitology - 3. Cestodes - Introduction to Cestodes Taenia Solium Taenia Saginata atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzQ5OTUwMTc0NDc1Mjc1)",
            "[<b>6. Clinical Parasitology - 4. Trematodes - Trematodes Intestinal Flukes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzUwOTUyMTk4ODMwMjAy)",
            "[<b>6. Clinical Parasitology - 4. Trematodes - Trematodes Blood Flukes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzUxOTU0MjIzMTg1MTI5)",
            "[<b>6. Clinical Parasitology - 4. Trematodes - Trematodes Lung Fluke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzUyOTU2MjQ3NTQwMDU2)",
            "[<b>6. Clinical Parasitology - 4. Trematodes - Trematodes Liver Flukes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzUzOTU4MjcxODk0OTgz)",
            "[<b>8. Qrp - Microbiology by Dr Mamta Jawa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzU0OTYwMjk2MjQ5OTEw)",
            "[<b>7. Covid9 - Mucormycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzU1OTYyMzIwNjA0ODM3)",
            "[<b>8. Qrp - Ini Cet Qrp 2021 Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzU2OTY0MzQ0OTU5NzY0)",
            "[<b>8. Qrp - Microbiology Recall Questions   Ini Cet Nov '21 by Dr Mamta Jawa  Ini atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzU3OTY2MzY5MzE0Njkx)",
            "[<b>8. Qrp - Microbiology by Dr Mamta Jawa 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzU4OTY4MzkzNjY5NjE4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        microbiologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"microbiologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"microbiologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(microbiologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pharmacologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Fundamental Principles of Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzU5OTcwNDE4MDI0NTQ1)",
            "[<b>1. Fundamental Principles of Drug Absorption atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzYwOTcyNDQyMzc5NDcy)",
            "[<b>1. Fundamental Principles of Drug Action atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzYxOTc0NDY2NzM0Mzk5)",
            "[<b>1. Fundamental Principles of Drug Distribution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzYyOTc2NDkxMDg5MzI2)",
            "[<b>1. Fundamental Principles of Excretion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzYzOTc4NTE1NDQ0MjUz)",
            "[<b>1. Fundamental Principles of Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzY0OTgwNTM5Nzk5MTgw)",
            "[<b>1. Fundamental Principles of Pharmacodynamics Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzY1OTgyNTY0MTU0MTA3)",
            "[<b>1. Fundamental Principles of Pharmacodynamics Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzY2OTg0NTg4NTA5MDM0)",
            "[<b>1. Fundamental Principles of Pharmacodynamics Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzY3OTg2NjEyODYzOTYx)",
            "[<b>1. Spm Free Videos - Determinants or Rf Study atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzY4OTg4NjM3MjE4ODg4)",
            "[<b>Adrenergic Pharmacology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzY5OTkwNjYxNTczODE1)",
            "[<b>Anti Adrenergic Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzcwOTkyNjg1OTI4NzQy)",
            "[<b>Cholinergic Pharmacology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzcxOTk0NzEwMjgzNjY5)",
            "[<b>Local Anaesthetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzcyOTk2NzM0NjM4NTk2)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Psychosis Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzczOTk4NzU4OTkzNTIz)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Psychosis Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzc1MDAwNzgzMzQ4NDUw)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Opioids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzc2MDAyODA3NzAzMzc3)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Sedative Hypnotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzc3MDA0ODMyMDU4MzA0)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Psychosis Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzc4MDA2ODU2NDEzMjMx)",
            "[<b>3. Neuro1. Drugs Affectiong Autonomic and Peripheral Nervous System - Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzc5MDA4ODgwNzY4MTU4)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Depression Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzgwMDEwOTA1MTIzMDg1)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Depression Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzgxMDEyOTI5NDc4MDEy)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Epilepsy Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzgyMDE0OTUzODMyOTM5)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Epilepsy Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzgzMDE2OTc4MTg3ODY2)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Cns Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzg0MDE5MDAyNTQyNzkz)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Mania atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzg1MDIxMDI2ODk3NzIw)",
            "[<b>3. Neuro2. Drugs Affecting Central Nervous System2 - Drugs for Movement Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzg2MDIzMDUxMjUyNjQ3)",
            "[<b>2. Fundamental of Drug Development and Regulation - Clinical Trails atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzg3MDI1MDc1NjA3NTc0)",
            "[<b>4. Cardiovascular 1. Drugs Affecting Vascular Tone - Anti Anginal Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzg4MDI3MDk5OTYyNTAx)",
            "[<b>4. Cardiovascular 1. Drugs Affecting Vascular Tone - Anti Hypertensive Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzg5MDI5MTI0MzE3NDI4)",
            "[<b>4. Cardiovascular 1. Drugs Affecting Vascular Tone - Nitric Oxide atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzkwMDMxMTQ4NjcyMzU1)",
            "[<b>4. Cardiovascular 1. Drugs Affecting Vascular Tone - Vasoactive Peptides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzkxMDMzMTczMDI3Mjgy)",
            "[<b>4. Cardiovascular 2. Pharmacology of Volume Regulation - Diuretics Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzkyMDM1MTk3MzgyMjA5)",
            "[<b>4. Cardiovascular 2. Pharmacology of Volume Regulation - Drugs for Congestive Cardiac Failure Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzkzMDM3MjIxNzM3MTM2)",
            "[<b>4. Cardiovascular 2. Pharmacology of Volume Regulation - Drugs for Congestive Cardiac Failure Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzk0MDM5MjQ2MDkyMDYz)",
            "[<b>4. Cardiovascular 2. Pharmacology of Volume Regulation - Diuretics Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzk1MDQxMjcwNDQ2OTkw)",
            "[<b>4. Cardiovascular 3. Drugs Affecting Cardiac Rythm - Anti Arrhythmic Drugs Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzk2MDQzMjk0ODAxOTE3)",
            "[<b>4. Cardiovascular 3. Drugs Affecting Cardiac Rythm - Anti Arrhythmic Drugs Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzk3MDQ1MzE5MTU2ODQ0)",
            "[<b>4. Cardiovascular 3. Drugs Affecting Cardiac Rythm - Anti Arrhythmic Drugs Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzk4MDQ3MzQzNTExNzcx)",
            "[<b>4. Cardiovascular 4. Pharmacology of Hemostasis and Thrombosis - Anti Coagulants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyMzk5MDQ5MzY3ODY2Njk4)",
            "[<b>4. Cardiovascular 4. Pharmacology of Hemostasis and Thrombosis - Anti Platelet atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDAwMDUxMzkyMjIxNjI1)",
            "[<b>4. Cardiovascular 4. Pharmacology of Hemostasis and Thrombosis - Fibrinolytics Hematinics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDAxMDUzNDE2NTc2NTUy)",
            "[<b>4. Cardiovascular 4. Pharmacology of Hemostasis and Thrombosis - Hematinics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDAyMDU1NDQwOTMxNDc5)",
            "[<b>Drugs Used for Dyslipidemia Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDAzMDU3NDY1Mjg2NDA2)",
            "[<b>Drugs Used for Dyslipidemia Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDA0MDU5NDg5NjQxMzMz)",
            "[<b>5. Endocrine 2. Drugs Affecting Thyroid Gland - Drugs Used for Hyperthyroidism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDA1MDYxNTEzOTk2MjYw)",
            "[<b>5. Endocrine 2. Drugs Affecting Thyroid Gland - Drugs Used for Hypothyroidism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDA2MDYzNTM4MzUxMTg3)",
            "[<b>5. Endocrine 7. Insulin and Antidiabetic Drugs - Insulin and Analogues atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDA3MDY1NTYyNzA2MTE0)",
            "[<b>5. Endocrine 7. Insulin and Antidiabetic Drugs - Non Insulin Anti Diabetic Agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDA4MDY3NTg3MDYxMDQx)",
            "[<b>5. Endocrine 6. Androgens and Drugs for Erectile Dysfunction - Sex Hormones Androgen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDA5MDY5NjExNDE1OTY4)",
            "[<b>5. Endocrine 5. Ocps, Estrogens and Progestins - Sex Hormone Estrogen Progestins and Oc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDEwMDcxNjM1NzcwODk1)",
            "[<b>5. Endocrine 4. Osteoporosis and Ca Metabolism - Bisphosphonates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDExMDczNjYwMTI1ODIy)",
            "[<b>5. Endocrine 4. Osteoporosis and Ca Metabolism - Calcitonin Vitamin D atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDEyMDc1Njg0NDgwNzQ5)",
            "[<b>5. Endocrine 4. Osteoporosis and Ca Metabolism - Calcium Pth atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDEzMDc3NzA4ODM1Njc2)",
            "[<b>5. Endocrine 4. Osteoporosis and Ca Metabolism - Drugs Affecting Calcium Balance Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDE0MDc5NzMzMTkwNjAz)",
            "[<b>5. Endocrine 3. Corticosteroids - Corticosteroids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDE1MDgxNzU3NTQ1NTMw)",
            "[<b>5. Endocrine 1. Drugs Affecting Hypothalamus and Pituitary - Drugs Affecting Anterior Pituitary atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDE2MDgzNzgxOTAwNDU3)",
            "[<b>5. Endocrine 1. Drugs Affecting Hypothalamus and Pituitary - Drugs Affecting Hypothalamus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDE3MDg1ODA2MjU1Mzg0)",
            "[<b>5. Endocrine 1. Drugs Affecting Hypothalamus and Pituitary - Drugs Affecting Posterior Pituitary atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDE4MDg3ODMwNjEwMzEx)",
            "[<b>6. Inflammation and Immune 4. Applied Pharmacology Drugs for Gout - Drugs for Gout Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDE5MDg5ODU0OTY1MjM4)",
            "[<b>6. Inflammation and Immune 4. Applied Pharmacology Drugs for Gout - Drugs for Gout Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDIwMDkxODc5MzIwMTY1)",
            "[<b>Dmard Disease Modifying Anti Rheumatoid Drugs Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDIxMDkzOTAzNjc1MDky)",
            "[<b>Dmard Disease Modifying Anti Rheumatoid Drugs Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDIyMDk1OTI4MDMwMDE5)",
            "[<b>Prostaglandins Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDIzMDk3OTUyMzg0OTQ2)",
            "[<b>Prostaglandins Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDI0MDk5OTc2NzM5ODcz)",
            "[<b>6. Inflammation and Immune 1. Histaminergic Histamine Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDI1MTAyMDAxMDk0ODAw)",
            "[<b>6. Inflammation and Immune 1. Histaminergic Histamine Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDI2MTA0MDI1NDQ5NzI3)",
            "[<b>6. Inflammation and Immune 2. Serotonergic Serotonin Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDI3MTA2MDQ5ODA0NjU0)",
            "[<b>6. Inflammation and Immune 2. Serotonergic Serotonin Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDI4MTA4MDc0MTU5NTgx)",
            "[<b>6. Inflammation and Immune 2. Serotonergic Serotonin Part 3 Drugs for Migraine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDI5MTEwMDk4NTE0NTA4)",
            "[<b>6. Inflammation and Immune 4. Applied Pharmacology Drugs for Gout - Drugs for Gout Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDMwMTEyMTIyODY5NDM1)",
            "[<b>7. Infectious Chemotherapy - 1. Introduction - Introduction Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDMxMTE0MTQ3MjI0MzYy)",
            "[<b>7. Infectious Chemotherapy - 1. Introduction - Introduction Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDMyMTE2MTcxNTc5Mjg5)",
            "[<b>7. Infectious Chemotherapy - 7. Anti Mycobacterial Drugs - Anti Leprotic Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDMzMTE4MTk1OTM0MjE2)",
            "[<b>7. Infectious Chemotherapy - 7. Anti Mycobacterial Drugs - Anti Tb Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDM0MTIwMjIwMjg5MTQz)",
            "[<b>7. Infectious Chemotherapy - 10. Antiviral Drugs - Anti Viral Drugs Anti Covid Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDM1MTIyMjQ0NjQ0MDcw)",
            "[<b>7. Infectious Chemotherapy - 10. Antiviral Drugs - Anti Viral Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDM2MTI0MjY4OTk4OTk3)",
            "[<b>7. Infectious Chemotherapy - 10. Antiviral Drugs - Anti Retroviral Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDM3MTI2MjkzMzUzOTI0)",
            "[<b>7. Infectious Chemotherapy - 9. Anti Fungal Drugs - Anti Fungal Agents Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDM4MTI4MzE3NzA4ODUx)",
            "[<b>7. Infectious Chemotherapy - 9. Anti Fungal Drugs - Anti Fungal Agents Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDM5MTMwMzQyMDYzNzc4)",
            "[<b>7. Infectious Chemotherapy - 8. Anti Parasitic Drugs - Anti Helmintic Agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQwMTMyMzY2NDE4NzA1)",
            "[<b>7. Infectious Chemotherapy - 8. Anti Parasitic Drugs - Anti Malarial Drugs Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQxMTM0MzkwNzczNjMy)",
            "[<b>7. Infectious Chemotherapy - 8. Anti Parasitic Drugs - Anti Malarial Drugs Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQyMTM2NDE1MTI4NTU5)",
            "[<b>7. Infectious Chemotherapy - 5. Folic Acid Synthesis Inhibitors - Drugs Affecting Folic Acid Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQzMTM4NDM5NDgzNDg2)",
            "[<b>7. Infectious Chemotherapy - 4. Nucleic Acid Synthesis Inhibitors - Drugs Affecting Bacterial Nucleic Acid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQ0MTQwNDYzODM4NDEz)",
            "[<b>7. Infectious Chemotherapy - 3. Protein Synthesis Inhibitors - Drug Affecting Bacterial Protein Synthesis Part 2 Macrolides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQ1MTQyNDg4MTkzMzQw)",
            "[<b>Drug Affecting Bacterial Protein Synthesis Part 1 Aminoglycosides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQ2MTQ0NTEyNTQ4MjY3)",
            "[<b>Drug Affecting Bacterial Protein Synthesis Part 3 Tetracyclines and Chloramphenicol atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQ3MTQ2NTM2OTAzMTk0)",
            "[<b>Drug Affecting Bacterial Protein Synthesis Part 4 Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQ4MTQ4NTYxMjU4MTIx)",
            "[<b>7. Infectious Chemotherapy - 2. Cell Membrane Synthesis Inhibitors - Drugs Affecting Bacterial Cell Membrane atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDQ5MTUwNTg1NjEzMDQ4)",
            "[<b>7. Infectious Chemotherapy - 6. Miscellaneous - Drugs for Pseudomembranous Enterocolitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDUwMTUyNjA5OTY3OTc1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pharmacologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pharmacologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pharmacologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pharmacologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("fmtd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Legal Procedure - Introduction Legal Procedure Part 1 Basic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDUxMTU0NjM0MzIyOTAy)",
            "[<b>1. Legal Procedure - Legal Procedure Part 2 Court Procedures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDUyMTU2NjU4Njc3ODI5)",
            "[<b>2. Medical Law and Ethics - Medical Law and Ethics Part 1 Basics and Consatf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDUzMTU4NjgzMDMyNzU2)",
            "[<b>2. Medical Law and Ethics - Medical Law and Ethics Part 2 Medical Negligence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDU0MTYwNzA3Mzg3Njgz)",
            "[<b>3. Identification - Identification Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDU1MTYyNzMxNzQyNjEw)",
            "[<b>3. Identification - Identification Part 2 Dentition atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDU2MTY0NzU2MDk3NTM3)",
            "[<b>3. Identification - Identification Part 3 Bones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDU3MTY2NzgwNDUyNDY0)",
            "[<b>4. Medico Legal Autopsy - Medico Legal Autopsy Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDU4MTY4ODA0ODA3Mzkx)",
            "[<b>4. Medico Legal Autopsy - Medico Legal Autopsy Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDU5MTcwODI5MTYyMzE4)",
            "[<b>5. Thanotology - Thanatology Part 1 Death Early Changes After Death atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDYwMTcyODUzNTE3MjQ1)",
            "[<b>5. Thanotology - Thanatology Part Late Changes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDYxMTc0ODc3ODcyMTcy)",
            "[<b>11. Ballistics - Ballistics Part 2 Wound Ballistics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDYyMTc2OTAyMjI3MDk5)",
            "[<b>11. Ballistics - Ballistics Part 1 Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDYzMTc4OTI2NTgyMDI2)",
            "[<b>10. Medico Legal Aspects of Injuries - Medico Legal Aspects of Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDY0MTgwOTUwOTM2OTUz)",
            "[<b>6. Mechanical Injuries - Mechanical Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDY1MTgyOTc1MjkxODgw)",
            "[<b>7. Regional Injuries - Regional Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDY2MTg0OTk5NjQ2ODA3)",
            "[<b>8. Rta and Bomb Blast - Road Traffic Accidents and Bomb Blast atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDY3MTg3MDI0MDAxNzM0)",
            "[<b>9. Thermal Injuries - Thermal Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDY4MTg5MDQ4MzU2NjYx)",
            "[<b>12. Mechanical Asphyxia - Mechanical Asphyxia Part 2 Suffocation Drowning atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDY5MTkxMDcyNzExNTg4)",
            "[<b>12. Mechanical Asphyxia - Mchanical Asphyxia Part 1 Basics Hanging Strangulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDcwMTkzMDk3MDY2NTE1)",
            "[<b>13. Impotence, Sterility and Virginity - Impotence Sterility and Virginity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDcxMTk1MTIxNDIxNDQy)",
            "[<b>14. Pregnancy, Delivery and Abortions - Pregnancy Delivery and Abortion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDcyMTk3MTQ1Nzc2MzY5)",
            "[<b>15. Natural Sexual Offences - Natural Sexual Offences atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDczMTk5MTcwMTMxMjk2)",
            "[<b>17. Infanticide, Child Abuse and Sids - Infanticide Child Abuse and Sids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDc0MjAxMTk0NDg2MjIz)",
            "[<b>16. Unnatural Sexual Offences 1 - Unnatural Sexual Offences atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDc1MjAzMjE4ODQxMTUw)",
            "[<b>18. Forensic Psychiatry - Forensic Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDc2MjA1MjQzMTk2MDc3)",
            "[<b>20. Death Certificate, Starvation, Torture and Artefact - Death Certificate Starvation Torture and Artefact atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDc3MjA3MjY3NTUxMDA0)",
            "[<b>21. Euthanasia, Dowry Death and Acts Copra, Thoa and Pcpndt - Euthanasia Dowry Deaths and Acts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDc4MjA5MjkxOTA1OTMx)",
            "[<b>20. Death Certificate, Starvation, Torture and Artefact - Death Certificate Starvation Torture and Artefact atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDc5MjExMzE2MjYwODU4)",
            "[<b>21. Euthanasia, Dowry Death and Acts Copra, Thoa and Pcpndt - Euthanasia Dowry Deaths and Acts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDgwMjEzMzQwNjE1Nzg1)",
            "[<b>27. Asphyxiants, Cardiac Poisons and Miscellaneous - Asphyxiants Cardiac Poisons and Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDgxMjE1MzY0OTcwNzEy)",
            "[<b>28. Neet Pg Qrp 2021 - by Dr Jayaprakash atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDgyMjE3Mzg5MzI1NjM5)",
            "[<b>25. Pesticide and Insecticides and Poisonous Food - Pesticide Insecticides and Poisonous Food atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDgzMjE5NDEzNjgwNTY2)",
            "[<b>28. Neet Pg Qrp 2021 - Fmt by Dr Jayaprakash atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDg0MjIxNDM4MDM1NDkz)",
            "[<b>28. Neet Pg Qrp 2021 - Neet Pg 2021 Quick Revision Program by Dr Jayaprakash atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDg1MjIzNDYyMzkwNDIw)",
            "[<b>26. Neurotoxics - Neurotoxics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDg2MjI1NDg2NzQ1MzQ3)",
            "[<b>22. General Toxicology and Caustics - General Toxicology Caustics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDg3MjI3NTExMTAwMjc0)",
            "[<b>23. Inorganic Irritants - Inorganic Irritants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDg4MjI5NTM1NDU1MjAx)",
            "[<b>24. Organic Irritants - Organic Irritants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDg5MjMxNTU5ODEwMTI4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        fmtd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"fmtd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"fmtd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(fmtd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psmd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Spm Free Videos - Time Distribution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDkwMjMzNTg0MTY1MDU1)",
            "[<b>1. Spm Free Videos - Type 1 Error and Type 2 Error atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDkxMjM1NjA4NTE5OTgy)",
            "[<b>2. Concept of Health and Disease - Compare and Contrast atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDkyMjM3NjMyODc0OTA5)",
            "[<b>2. Concept of Health and Disease - Health Index atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDkzMjM5NjU3MjI5ODM2)",
            "[<b>3. Epidemiology - 1. Introduction Types of Studies, Methods - Introduction to Epidemiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDk0MjQxNjgxNTg0NzYz)",
            "[<b>3. Epidemiology - 2. Frequency Measurement - Disability Frequency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDk1MjQzNzA1OTM5Njkw)",
            "[<b>3. Epidemiology - 2. Frequency Measurement - International Classification of Diseases Icd and Icf atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDk2MjQ1NzMwMjk0NjE3)",
            "[<b>3. Epidemiology - 2. Frequency Measurement - International Death Certificate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDk3MjQ3NzU0NjQ5NTQ0)",
            "[<b>3. Epidemiology - 2. Frequency Measurement - Mcqs in Mortality and Standardisation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDk4MjQ5Nzc5MDA0NDcx)",
            "[<b>3. Epidemiology - 2. Frequency Measurement - Morbidity Measures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNDk5MjUxODAzMzU5Mzk4)",
            "[<b>3. Epidemiology - 2. Frequency Measurement - Mortality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTAwMjUzODI3NzE0MzI1)",
            "[<b>3. Epidemiology - 3. Descriptive Epidemiology - Person Distribution and Place Distribution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTAxMjU1ODUyMDY5MjUy)",
            "[<b>3. Epidemiology - 3. Descriptive Epidemiology - Time Distribution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTAyMjU3ODc2NDI0MTc5)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Determinants or Rf Study atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTAzMjU5OTAwNzc5MTA2)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Ecological Study Design atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTA0MjYxOTI1MTM0MDMz)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Introduction to Study Design atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTA1MjYzOTQ5NDg4OTYw)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Rct atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTA2MjY1OTczODQzODg3)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Study Design Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTA3MjY3OTk4MTk4ODE0)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Study Designs Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTA4MjcwMDIyNTUzNzQx)",
            "[<b>3. Epidemiology - 4. Analytical Epidemiology - Study Designs Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTA5MjcyMDQ2OTA4NjY4)",
            "[<b>3. Epidemiology - 5. Meta Analysis - Meta Analysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTEwMjc0MDcxMjYzNTk1)",
            "[<b>4. International Health - International Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTExMjc2MDk1NjE4NTIy)",
            "[<b>5. Image Based Questions - History of Public Health Image Based Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTEyMjc4MTE5OTczNDQ5)",
            "[<b>5. Image Based Questions - Image Based Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTEzMjgwMTQ0MzI4Mzc2)",
            "[<b>6. Screening of Diseases - Combination of Tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTE0MjgyMTY4NjgzMzAz)",
            "[<b>6. Screening of Diseases - Factors Affecting Ppv atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTE1Mjg0MTkzMDM4MjMw)",
            "[<b>6. Screening of Diseases - Lead Time and Lead Time Bias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTE2Mjg2MjE3MzkzMTU3)",
            "[<b>6. Screening of Diseases - Levels of Prevention atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTE3Mjg4MjQxNzQ4MDg0)",
            "[<b>6. Screening of Diseases - Relationship Between Sensitivity Specificity and Predictive Values atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTE4MjkwMjY2MTAzMDEx)",
            "[<b>6. Screening of Diseases - Reliability atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTE5MjkyMjkwNDU3OTM4)",
            "[<b>6. Screening of Diseases - Sensitivity Specificity Predictive Values atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTIwMjk0MzE0ODEyODY1)",
            "[<b>6. Screening of Diseases - Type 1 Error and Type 2 Error atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTIxMjk2MzM5MTY3Nzky)",
            "[<b>6. Screening of Diseases - Types of Screening atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTIyMjk4MzYzNTIyNzE5)",
            "[<b>6. Screening of Diseases - Validity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTIzMzAwMzg3ODc3NjQ2)",
            "[<b>7. Demography - Demographic Cycle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTI0MzAyNDEyMjMyNTcz)",
            "[<b>7. Demography - Dependency Ratio and Literacy Rate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTI1MzA0NDM2NTg3NTAw)",
            "[<b>7. Demography - Fertility Rates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTI2MzA2NDYwOTQyNDI3)",
            "[<b>7. Demography - Introduction to Demography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTI3MzA4NDg1Mjk3MzU0)",
            "[<b>7. Demography - Sex Ratio and Age Population Pyramid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTI4MzEwNTA5NjUyMjgx)",
            "[<b>7. Demography - Tools or Sources of Population Data atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTI5MzEyNTM0MDA3MjA4)",
            "[<b>8. Family Planning - Barrier Methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTMwMzE0NTU4MzYyMTM1)",
            "[<b>8. Family Planning - Contraceptive Efficacy Ce atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTMxMzE2NTgyNzE3MDYy)",
            "[<b>8. Family Planning - Couple Protection Rate Cpr atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTMyMzE4NjA3MDcxOTg5)",
            "[<b>8. Family Planning - Emergency Contraceptives atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTMzMzIwNjMxNDI2OTE2)",
            "[<b>8. Family Planning - Family Planning Clinic and Field Delivery Practices atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTM0MzIyNjU1NzgxODQz)",
            "[<b>8. Family Planning - Hormonal Methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTM1MzI0NjgwMTM2Nzcw)",
            "[<b>8. Family Planning - Iucd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTM2MzI2NzA0NDkxNjk3)",
            "[<b>8. Family Planning - Miscellaneous Methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTM3MzI4NzI4ODQ2NjI0)",
            "[<b>8. Family Planning - Mtp Act atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTM4MzMwNzUzMjAxNTUx)",
            "[<b>8. Family Planning - Post Conception Method atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTM5MzMyNzc3NTU2NDc4)",
            "[<b>8. Family Planning - Sterilisation Terminal Methods of Contraception atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQwMzM0ODAxOTExNDA1)",
            "[<b>9. Maternal and Child Health - Antenatal Diet Immunisation Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQxMzM2ODI2MjY2MzMy)",
            "[<b>9. Maternal and Child Health - Antenatal Rh Incompatibility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQyMzM4ODUwNjIxMjU5)",
            "[<b>9. Maternal and Child Health - Birth Weight Apgar Score atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQzMzQwODc0OTc2MTg2)",
            "[<b>9. Maternal and Child Health - Breast Feeding atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQ0MzQyODk5MzMxMTEz)",
            "[<b>9. Maternal and Child Health - Childhood Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQ1MzQ0OTIzNjg2MDQw)",
            "[<b>9. Maternal and Child Health - Growth Chart atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQ2MzQ2OTQ4MDQwOTY3)",
            "[<b>9. Maternal and Child Health - Intranatal Period atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQ3MzQ4OTcyMzk1ODk0)",
            "[<b>9. Maternal and Child Health - Iron Folic Acid Ifa Schedule in Mother and Child atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQ4MzUwOTk2NzUwODIx)",
            "[<b>9. Maternal and Child Health - Malnutrition atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTQ5MzUzMDIxMTA1NzQ4)",
            "[<b>9. Maternal and Child Health - Mch Indicators atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTUwMzU1MDQ1NDYwNjc1)",
            "[<b>9. Maternal and Child Health - Newer Technologies in Mch atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTUxMzU3MDY5ODE1NjAy)",
            "[<b>10. Nutrition - Assessment of Protein atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTUyMzU5MDk0MTcwNTI5)",
            "[<b>10. Nutrition - Dietary Fibres Glycemic Index atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTUzMzYxMTE4NTI1NDU2)",
            "[<b>10. Nutrition - Essential Fatty Acids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTU0MzYzMTQyODgwMzgz)",
            "[<b>10. Nutrition - Essential and Limiting Amino Acids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTU1MzY1MTY3MjM1MzEw)",
            "[<b>10. Nutrition - Indian Reference Man and Woman atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTU2MzY3MTkxNTkwMjM3)",
            "[<b>10. Nutrition - Introduction to Nutrition atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTU3MzY5MjE1OTQ1MTY0)",
            "[<b>10. Nutrition - Minerals atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTU4MzcxMjQwMzAwMDkx)",
            "[<b>10. Nutrition - Nutritional Values of Food Items atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTU5MzczMjY0NjU1MDE4)",
            "[<b>10. Nutrition - Rda and Par atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTYwMzc1Mjg5MDA5OTQ1)",
            "[<b>10. Nutrition - Vitamins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTYxMzc3MzEzMzY0ODcy)",
            "[<b>11. Statistics - 1. Statistics2 - Data Presentation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTYyMzc5MzM3NzE5Nzk5)",
            "[<b>11. Statistics - 1. Statistics2 - Box Whisker Plote atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTYzMzgxMzYyMDc0NzI2)",
            "[<b>1. Spm Free Videos - Time Distribution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTY0MzgzMzg2NDI5NjUz)",
            "[<b>11. Statistics - 1. Statistics2 - Measures of Central Tendency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTY1Mzg1NDEwNzg0NTgw)",
            "[<b>11. Statistics - 1. Statistics2 - Measures of Dispersion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTY2Mzg3NDM1MTM5NTA3)",
            "[<b>11. Statistics - 1. Statistics2 - Data and Variables atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTY3Mzg5NDU5NDk0NDM0)",
            "[<b>11. Statistics - 1. Statistics2 - Normal Distribution Curve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTY4MzkxNDgzODQ5MzYx)",
            "[<b>11. Statistics - 1. Statistics2 - Quartiles Percentiles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTY5MzkzNTA4MjA0Mjg4)",
            "[<b>11. Statistics - 1. Statistics2 - Sample Size Calculation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTcwMzk1NTMyNTU5MjE1)",
            "[<b>11. Statistics - 1. Statistics2 - Sampling Technique atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTcxMzk3NTU2OTE0MTQy)",
            "[<b>11. Statistics - 2. Statistics - Correlation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTcyMzk5NTgxMjY5MDY5)",
            "[<b>11. Statistics - 1. Statistics2 - Scales of Measurement atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTczNDAxNjA1NjIzOTk2)",
            "[<b>11. Statistics - 2. Statistics - Chisquare Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTc0NDAzNjI5OTc4OTIz)",
            "[<b>11. Statistics - 2. Statistics - Degrees of Freedom atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTc1NDA1NjU0MzMzODUw)",
            "[<b>11. Statistics - 2. Statistics - Regression atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTc2NDA3Njc4Njg4Nzc3)",
            "[<b>11. Statistics - 2. Statistics - Coefficient of Variation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTc3NDA5NzAzMDQzNzA0)",
            "[<b>11. Statistics - 2. Statistics - Likelihood Ratio atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTc4NDExNzI3Mzk4NjMx)",
            "[<b>11. Statistics - 2. Statistics - Roc Curve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTc5NDEzNzUxNzUzNTU4)",
            "[<b>11. Statistics - 2. Statistics - Probability atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTgwNDE1Nzc2MTA4NDg1)",
            "[<b>11. Statistics - 1. Statistics2 - Skewing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTgxNDE3ODAwNDYzNDEy)",
            "[<b>11. Statistics - 2. Statistics - Types of Distribution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTgyNDE5ODI0ODE4MzM5)",
            "[<b>11. Statistics - 1. Statistics2 - Z Score atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTgzNDIxODQ5MTczMjY2)",
            "[<b>Truely Clinical - 1. PSM - Biomedical Waste Disposal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTg0NDIzODczNTI4MTkz)",
            "[<b>12. Biomedical Waste Management - Biomedical Waste Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTg1NDI1ODk3ODgzMTIw)",
            "[<b>13. Disaster Management - Types of Disasters atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTg2NDI3OTIyMjM4MDQ3)",
            "[<b>14. Occupational Health - Occupational Cancers and Caisson S Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTg3NDI5OTQ2NTkyOTc0)",
            "[<b>15. Genetics - Genetics and Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTg4NDMxOTcwOTQ3OTAx)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 1. Tb and Ntep - Advancements in Tb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTg5NDMzOTk1MzAyODI4)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 1. Tb and Ntep - Co Morbidities in Tb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTkwNDM2MDE5NjU3NzU1)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 1. Tb and Ntep - Diagnosis of Pulmonary Tb in Adults atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTkxNDM4MDQ0MDEyNjgy)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 2. Hiv and Nacp - Hiv and Nacp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTkyNDQwMDY4MzY3NjA5)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 1. Tb and Ntep - Treatment of Pulmonary Tb in Adults atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTkzNDQyMDkyNzIyNTM2)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 1. Tb and Ntep - Extrapulmonary and Pediatric Tb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTk0NDQ0MTE3MDc3NDYz)",
            "[<b>16. Diseases and Their National Programs in India New Topic - 3. Uip - Uip atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTk1NDQ2MTQxNDMyMzkw)",
            "[<b>Ncd Control Program atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTk2NDQ4MTY1Nzg3MzE3)",
            "[<b>Communicable Diseases and Their Control Program atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTk3NDUwMTkwMTQyMjQ0)",
            "[<b>Blindness Control Program and Nvbdcp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTk4NDUyMjE0NDk3MTcx)",
            "[<b>Reproductive and Child Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNTk5NDU0MjM4ODUyMDk4)",
            "[<b>17. Mosquito - Mosquito Control Measures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjAwNDU2MjYzMjA3MDI1)",
            "[<b>18. Water Pollution - Water Purification Methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjAxNDU4Mjg3NTYxOTUy)",
            "[<b>18. Water Pollution - Sewage and Diseases Caused by Water atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjAyNDYwMzExOTE2ODc5)",
            "[<b>18. Water Pollution - Indicators of Fecal Pollution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjAzNDYyMzM2MjcxODA2)",
            "[<b>18. Water Pollution - Problem Village and Water Requirement atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjA0NDY0MzYwNjI2NzMz)",
            "[<b>19. Air Pollution - Effects of Air Pollution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjA1NDY2Mzg0OTgxNjYw)",
            "[<b>19. Air Pollution - Indicators of Air Pollution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjA2NDY4NDA5MzM2NTg3)",
            "[<b>19. Air Pollution - Instruments for Measuring Air Pollution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjA3NDcwNDMzNjkxNTE0)",
            "[<b>19. Air Pollution - Types of Ventilation and Mcqs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjA4NDcyNDU4MDQ2NDQx)",
            "[<b>21. Entomology - Biological Transmission and Insecticides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjA5NDc0NDgyNDAxMzY4)",
            "[<b>21. Entomology - Vectors of Public Health Importance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjEwNDc2NTA2NzU2Mjk1)",
            "[<b>20. Noise Pollution - Noise Pollution atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjExNDc4NTMxMTExMjIy)",
            "[<b>22. Health Communication - Components of Communication and Types of Communication atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjEyNDgwNTU1NDY2MTQ5)",
            "[<b>22. Health Communication - Special Methods of Communication atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjEzNDgyNTc5ODIxMDc2)",
            "[<b>22. Health Communication - Group Discussion Methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjE0NDg0NjA0MTc2MDAz)",
            "[<b>23. Sociology - Family atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjE1NDg2NjI4NTMwOTMw)",
            "[<b>23. Sociology - Society and Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjE2NDg4NjUyODg1ODU3)",
            "[<b>24. Mental Health - Mental Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjE3NDkwNjc3MjQwNzg0)",
            "[<b>25. Health Care Delivery System in India - Health System in India atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjE4NDkyNzAxNTk1NzEx)",
            "[<b>25. Health Care Delivery System in India - Health Committees and International Summits atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjE5NDk0NzI1OTUwNjM4)",
            "[<b>26. Diseases and Their National Programs in India - Adult Immunisation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjIwNDk2NzUwMzA1NTY1)",
            "[<b>27. Covid Vaccination and Covid Mutants - Updates in Covid Vaccines and Covid Mutants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjIxNDk4Nzc0NjYwNDky)",
            "[<b>28. Qrp - Psm by Dr Rajasi 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjIyNTAwNzk5MDE1NDE5)",
            "[<b>28. Qrp - Ini Cet Qrp Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjIzNTAyODIzMzcwMzQ2)",
            "[<b>28. Qrp - Psm by Dr Rajasi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjI0NTA0ODQ3NzI1Mjcz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psmd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psmd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psmd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psmd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("entd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Cochlear Implantation and Hearing Aids 1 - Cochlear Implantation Auditory Brainstem Implantation Baha and Hearing Aids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjI1NTA2ODcyMDgwMjAw)",
            "[<b>1. Introduction to 1 - Introduction to atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjI2NTA4ODk2NDM1MTI3)",
            "[<b>2. Nose and Paranasal Sunuses - Anatomy of Nose and Nasal Septum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjI3NTEwOTIwNzkwMDU0)",
            "[<b>2. Nose and Paranasal Sunuses - Anatomy of Nose atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjI4NTEyOTQ1MTQ0OTgx)",
            "[<b>2. Nose and Paranasal Sunuses - Anatomy of Pns atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjI5NTE0OTY5NDk5OTA4)",
            "[<b>2. Nose and Paranasal Sunuses - Csf Rhinorrhoea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjMwNTE2OTkzODU0ODM1)",
            "[<b>2. Nose and Paranasal Sunuses - Epistaxis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjMxNTE5MDE4MjA5NzYy)",
            "[<b>2. Nose and Paranasal Sunuses - Fess Surgery Landmarks Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjMyNTIxMDQyNTY0Njg5)",
            "[<b>2. Nose and Paranasal Sunuses - Inverted Papilloma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjMzNTIzMDY2OTE5NjE2)",
            "[<b>2. Nose and Paranasal Sunuses - Juvenile Nasopharnyngel Angiofibroma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjM0NTI1MDkxMjc0NTQz)",
            "[<b>2. Nose and Paranasal Sunuses - Maxillofacial Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjM1NTI3MTE1NjI5NDcw)",
            "[<b>2. Nose and Paranasal Sunuses - Nasal Polyps atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjM2NTI5MTM5OTg0Mzk3)",
            "[<b>2. Nose and Paranasal Sunuses - Nasal Septum and Its Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjM3NTMxMTY0MzM5MzI0)",
            "[<b>2. Nose and Paranasal Sunuses - Nasopharyngeal Carcinoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjM4NTMzMTg4Njk0MjUx)",
            "[<b>2. Nose and Paranasal Sunuses - Rhinoscleroma Rhinosporidiosis Midline Lethal Granuloma Rhinophyma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjM5NTM1MjEzMDQ5MTc4)",
            "[<b>2. Nose and Paranasal Sunuses - Sinusitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQwNTM3MjM3NDA0MTA1)",
            "[<b>3. Oral Cavity and Pharynx - Adenoids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQxNTM5MjYxNzU5MDMy)",
            "[<b>3. Oral Cavity and Pharynx - Lesions of Oral Cavity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQyNTQxMjg2MTEzOTU5)",
            "[<b>3. Oral Cavity and Pharynx - Ludwing S Angina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQzNTQzMzEwNDY4ODg2)",
            "[<b>3. Oral Cavity and Pharynx - Parapharyngeal Abcess atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQ0NTQ1MzM0ODIzODEz)",
            "[<b>3. Oral Cavity and Pharynx - Peritonsillar Abcess atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQ1NTQ3MzU5MTc4NzQw)",
            "[<b>3. Oral Cavity and Pharynx - Retropharyngeal Abcess atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQ2NTQ5MzgzNTMzNjY3)",
            "[<b>3. Oral Cavity and Pharynx - Tonsils atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQ3NTUxNDA3ODg4NTk0)",
            "[<b>4. Larynx and Trachea - Anatomy of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQ4NTUzNDMyMjQzNTIx)",
            "[<b>4. Larynx and Trachea - Dysphonia Plica Ventricularis Functional Aphonia Puberphonia Phonasthenia Spasmodic Dysphonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjQ5NTU1NDU2NTk4NDQ4)",
            "[<b>4. Larynx and Trachea - Foreign Bodies in Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjUwNTU3NDgwOTUzMzc1)",
            "[<b>4. Larynx and Trachea - Inflammatory Conditions of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjUxNTU5NTA1MzA4MzAy)",
            "[<b>4. Larynx and Trachea - Laryngeal Paralysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjUyNTYxNTI5NjYzMjI5)",
            "[<b>4. Larynx and Trachea - Paediatric Laryngology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjUzNTYzNTU0MDE4MTU2)",
            "[<b>4. Larynx and Trachea - Tracheostomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjU0NTY1NTc4MzczMDgz)",
            "[<b>9. Complications of Suppurative Otitis Media 1 - Chronic Suppurative Otitis Media atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjU1NTY3NjAyNzI4MDEw)",
            "[<b>9. Operative Surgeries - Adenoids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjU2NTY5NjI3MDgyOTM3)",
            "[<b>9. Operative Surgeries - Caldwell Luc Operation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjU3NTcxNjUxNDM3ODY0)",
            "[<b>9. Operative Surgeries - Diagnostic Nasal Endoscopy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjU4NTczNjc1NzkyNzkx)",
            "[<b>9. Operative Surgeries - Fess Surgery Landmarks Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjU5NTc1NzAwMTQ3NzE4)",
            "[<b>9. Operative Surgeries - Microlaryngeal Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjYwNTc3NzI0NTAyNjQ1)",
            "[<b>9. Operative Surgeries - Neck Dissection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjYxNTc5NzQ4ODU3NTcy)",
            "[<b>9. Operative Surgeries - Parotid Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjYyNTgxNzczMjEyNDk5)",
            "[<b>9. Operative Surgeries - Septoplasty atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjYzNTgzNzk3NTY3NDI2)",
            "[<b>9. Operative Surgeries - Surgery of Ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjY0NTg1ODIxOTIyMzUz)",
            "[<b>9. Operative Surgeries - Thyroid Surgery and Rln Landmarks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjY1NTg3ODQ2Mjc3Mjgw)",
            "[<b>9. Operative Surgeries - Thyroplasty atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjY2NTg5ODcwNjMyMjA3)",
            "[<b>9. Operative Surgeries - Tonsils atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjY3NTkxODk0OTg3MTM0)",
            "[<b>8. Cholesteatoma 1 - Cholesteatoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjY4NTkzOTE5MzQyMDYx)",
            "[<b>8. Clinical Methods in - Ear History and Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjY5NTk1OTQzNjk2OTg4)",
            "[<b>8. Clinical Methods in - Larynx History and Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjcwNTk3OTY4MDUxOTE1)",
            "[<b>8. Clinical Methods in - Nose History and Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjcxNTk5OTkyNDA2ODQy)",
            "[<b>7. RecAdvances - Chemoradiotherapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjcyNjAyMDE2NzYxNzY5)",
            "[<b>7. RecAdvances - Coblation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjczNjA0MDQxMTE2Njk2)",
            "[<b>7. RecAdvances - Image Guided Navigation System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjc0NjA2MDY1NDcxNjIz)",
            "[<b>7. RecAdvances - Laser atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjc1NjA4MDg5ODI2NTUw)",
            "[<b>7. RecAdvances - Robotic Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjc2NjEwMTE0MTgxNDc3)",
            "[<b>10. Clinical Case Discussion - Non Healing Tangue Ulcer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjc3NjEyMTM4NTM2NDA0)",
            "[<b>10. Otosclerosis 2 - Cochlear Otosclerosis Stapedial Otosclerosis and Stapedoyomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjc4NjE0MTYyODkxMzMx)",
            "[<b>10. Otosclerosis 2 - Stapedotomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjc5NjE2MTg3MjQ2MjU4)",
            "[<b>11. Covid 19 - Mucormycosis Black Fungus in Covid 19 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjgwNjE4MjExNjAxMTg1)",
            "[<b>11. Meniere's Disease 1 - Meniere S Disease Disorders of Vertigo atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjgxNjIwMjM1OTU2MTEy)",
            "[<b>12. Facial Nerve and Its Disorders 1 - Facial Nerve Bells Palsy Melkerson Rosenthal Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjgyNjIyMjYwMzExMDM5)",
            "[<b>12. Qrp - Ini Cet Qrp 2021 Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjgzNjI0Mjg0NjY1OTY2)",
            "[<b>12. Qrp - Session 1 by Dr Darwin Kaushal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjg0NjI2MzA5MDIwODkz)",
            "[<b>12. Qrp - Session 2 by Dr Darwin Kaushal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjg1NjI4MzMzMzc1ODIw)",
            "[<b>12. Qrp - by Dr Darwin Kaushal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjg2NjMwMzU3NzMwNzQ3)",
            "[<b>13. Acoustic Neuroma 1 - Acoustic Neuroma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjg3NjMyMzgyMDg1Njc0)",
            "[<b>14. Glomus Tumors 1 - Glomus Tumours atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjg4NjM0NDA2NDQwNjAx)",
            "[<b>15. Surgery of Ear and Its Landmarks 1 - Surgery of Ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjg5NjM2NDMwNzk1NTI4)",
            "[<b>5. Diseases of External Ear 1 - Eustachian Tube atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjkwNjM4NDU1MTUwNDU1)",
            "[<b>5. Parotid Tumors, Surgery and Facial Nerve Landmarks - Parotid Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjkxNjQwNDc5NTA1Mzgy)",
            "[<b>6. Eustachian Tube and Its Disorders 1 - Furunculosis Otitis Externa Otomycosis Ramsay Hunt Syndrome and Malignant Otitis Ecterna atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjkyNjQyNTAzODYwMzA5)",
            "[<b>6. Thyroid Tumors, Surgery and RecurrLaryngeal Nerve Landmarks - Thyroid Surgery and Rln Landmarks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjkzNjQ0NTI4MjE1MjM2)",
            "[<b>7. Disorders of Middle Ear 1 - Disorders of Middle Ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjk0NjQ2NTUyNTcwMTYz)",
            "[<b>9. Complications of Suppurative Otitis Media 1 - Chronic Suppurative Otitis Media atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjk1NjQ4NTc2OTI1MDkw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        entd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"entd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"entd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(entd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("ophthalmologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Mda - Mda Optic Neuritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjk2NjUwNjAxMjgwMDE3)",
            "[<b>2. Basics of Anatomy of Eyeball atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjk3NjUyNjI1NjM0OTQ0)",
            "[<b>2. Basics of Cavities of Eyeball atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjk4NjU0NjQ5OTg5ODcx)",
            "[<b>2. Basics of Orbital Cavity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNjk5NjU2Njc0MzQ0Nzk4)",
            "[<b>3. Embryology of Eyeball - Embryology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzAwNjU4Njk4Njk5NzI1)",
            "[<b>4. Conjunctiva - Anatomy of Conjunctiva atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzAxNjYwNzIzMDU0NjUy)",
            "[<b>4. Conjunctiva - Phlyctenular Keratoconjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzAyNjYyNzQ3NDA5NTc5)",
            "[<b>4. Conjunctiva - Trachoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzAzNjY0NzcxNzY0NTA2)",
            "[<b>4. Conjunctiva - Vernal Keratoconjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzA0NjY2Nzk2MTE5NDMz)",
            "[<b>4. Conjunctiva - Conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzA1NjY4ODIwNDc0MzYw)",
            "[<b>4. Conjunctiva - Pterygium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzA2NjcwODQ0ODI5Mjg3)",
            "[<b>5. Cornea - Corneal Degenerations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzA3NjcyODY5MTg0MjE0)",
            "[<b>5. Cornea - Corneal Opacities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzA4Njc0ODkzNTM5MTQx)",
            "[<b>5. Cornea - Anatomy of Cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzA5Njc2OTE3ODk0MDY4)",
            "[<b>5. Cornea - Corneal Ulcer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzEwNjc4OTQyMjQ4OTk1)",
            "[<b>5. Cornea - Corneal Dystrophies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzExNjgwOTY2NjAzOTIy)",
            "[<b>5. Cornea - Deposits in Cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzEyNjgyOTkwOTU4ODQ5)",
            "[<b>5. Cornea - Investigations of Cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzEzNjg1MDE1MzEzNzc2)",
            "[<b>5. Cornea - Keratoconus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzE0Njg3MDM5NjY4NzAz)",
            "[<b>5. Cornea - Herpes Zoster Ophthalmicus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzE1Njg5MDY0MDIzNjMw)",
            "[<b>6. Lens - Congenital Cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzE2NjkxMDg4Mzc4NTU3)",
            "[<b>6. Lens - Ectopia Lentis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzE3NjkzMTEyNzMzNDg0)",
            "[<b>6. Lens - Cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzE4Njk1MTM3MDg4NDEx)",
            "[<b>6. Lens - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzE5Njk3MTYxNDQzMzM4)",
            "[<b>6. Lens - Iol Types Formulae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzIwNjk5MTg1Nzk4MjY1)",
            "[<b>6. Lens - Lens Anatomy Anomalies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzIxNzAxMjEwMTUzMTky)",
            "[<b>6. Lens - Nuclear Sclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzIyNzAzMjM0NTA4MTE5)",
            "[<b>6. Lens - Cataract Surgeries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzIzNzA1MjU4ODYzMDQ2)",
            "[<b>7. Uvea - Anatomy of Uveal Tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzI0NzA3MjgzMjE3OTcz)",
            "[<b>7. Uvea - Classification of Uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzI1NzA5MzA3NTcyOTAw)",
            "[<b>7. Uvea - Clinical Conditions of Iris atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzI2NzExMzMxOTI3ODI3)",
            "[<b>7. Uvea - Intermediate Uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzI3NzEzMzU2MjgyNzU0)",
            "[<b>7. Uvea - Panuveitis Sympathetic Ophthalmia and Vkh Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzI4NzE1MzgwNjM3Njgx)",
            "[<b>7. Uvea - Anterior Uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzI5NzE3NDA0OTkyNjA4)",
            "[<b>7. Uvea - Posterior Uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzMwNzE5NDI5MzQ3NTM1)",
            "[<b>8. Retina - Diabetic Htn Retinopathies Eale S Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzMxNzIxNDUzNzAyNDYy)",
            "[<b>8. Retina - Diseases of the Macula atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzMyNzIzNDc4MDU3Mzg5)",
            "[<b>8. Retina - Retinal Layers and Fundus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzMzNzI1NTAyNDEyMzE2)",
            "[<b>8. Retina - Retinitis Pigmentosa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzM0NzI3NTI2NzY3MjQz)",
            "[<b>8. Retina - Retinal Vascular Occlusions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzM1NzI5NTUxMTIyMTcw)",
            "[<b>8. Retina - Retinal Detachment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzM2NzMxNTc1NDc3MDk3)",
            "[<b>9. Glaucoma - Anti Glaucoma Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzM3NzMzNTk5ODMyMDI0)",
            "[<b>9. Glaucoma - Optic Disc Changes in Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzM4NzM1NjI0MTg2OTUx)",
            "[<b>9. Glaucoma - Congenital Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzM5NzM3NjQ4NTQxODc4)",
            "[<b>9. Glaucoma - Definition and Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQwNzM5NjcyODk2ODA1)",
            "[<b>9. Glaucoma - Investigation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQxNzQxNjk3MjUxNzMy)",
            "[<b>9. Glaucoma - Risk Factors of Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQyNzQzNzIxNjA2NjU5)",
            "[<b>9. Glaucoma - Special Types of Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQzNzQ1NzQ1OTYxNTg2)",
            "[<b>9. Glaucoma - Visual Field Defects of Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQ0NzQ3NzcwMzE2NTEz)",
            "[<b>9. Glaucoma - Angle Closure Glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQ1NzQ5Nzk0NjcxNDQw)",
            "[<b>10. Neuro Optic Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQ2NzUxODE5MDI2MzY3)",
            "[<b>10. Neuro Papilledema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQ3NzUzODQzMzgxMjk0)",
            "[<b>10. Neuro Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQ4NzU1ODY3NzM2MjIx)",
            "[<b>10. Neuro Primary Visual Center atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzQ5NzU3ODkyMDkxMTQ4)",
            "[<b>10. Neuro Pupillary Reflex Pathway Lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzUwNzU5OTE2NDQ2MDc1)",
            "[<b>10. Neuro Third Cranial Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzUxNzYxOTQwODAxMDAy)",
            "[<b>10. Neuro Visual Pathway Lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzUyNzYzOTY1MTU1OTI5)",
            "[<b>10. Neuro Third Nerve Palsy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzUzNzY1OTg5NTEwODU2)",
            "[<b>10. Neuro Gaze Pathway Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzU0NzY4MDEzODY1Nzgz)",
            "[<b>11. Squint - Compensatory Head Posture Park S 3 Step Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzU1NzcwMDM4MjIwNzEw)",
            "[<b>11. Squint - Extraocular Muscle Actions Laws atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzU2NzcyMDYyNTc1NjM3)",
            "[<b>11. Squint - Gazes Yoke Muscles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzU3Nzc0MDg2OTMwNTY0)",
            "[<b>11. Squint - Management of Squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzU4Nzc2MTExMjg1NDkx)",
            "[<b>12. Refraction - Accomodation Presbyopia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzU5Nzc4MTM1NjQwNDE4)",
            "[<b>12. Refraction - Refraction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzYwNzgwMTU5OTk1MzQ1)",
            "[<b>12. Refraction - Myopia Hypermetropia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzYxNzgyMTg0MzUwMjcy)",
            "[<b>12. Refraction - Astigmatism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzYyNzg0MjA4NzA1MTk5)",
            "[<b>12. Refraction - Spectacle Prescription Numericals atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzYzNzg2MjMzMDYwMTI2)",
            "[<b>13. Orbit - Orbit Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzY0Nzg4MjU3NDE1MDUz)",
            "[<b>13. Orbit - Proptosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzY1NzkwMjgxNzY5OTgw)",
            "[<b>13. Orbit - Thyroid Eye Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzY2NzkyMzA2MTI0OTA3)",
            "[<b>14. Eyelids and Lacrimal Apparatus - Eyelid Anatomy Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzY3Nzk0MzMwNDc5ODM0)",
            "[<b>14. Eyelids and Lacrimal Apparatus - Lacrimal System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzY4Nzk2MzU0ODM0NzYx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        ophthalmologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ophthalmologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ophthalmologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ophthalmologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("medicined"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Pulmonology - Ards atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzY5Nzk4Mzc5MTg5Njg4)",	
            "[<b>1. Pulmonology - Basics of Spirometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzcwODAwNDAzNTQ0NjE1)",	
            "[<b>1. Pulmonology - Bronchial Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzcxODAyNDI3ODk5NTQy)",	
            "[<b>1. Pulmonology - Bronchiectasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzcyODA0NDUyMjU0NDY5)",	
            "[<b>1. Pulmonology - Copd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzczODA2NDc2NjA5Mzk2)",	
            "[<b>1. Pulmonology - Hypersensitivity Pneumonitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzc0ODA4NTAwOTY0MzIz)",	
            "[<b>1. Pulmonology - Interstitial Lung Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzc1ODEwNTI1MzE5MjUw)",	
            "[<b>1. Pulmonology - Obstructive Sleep Apnea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzc2ODEyNTQ5Njc0MTc3)",	
            "[<b>1. Pulmonology - Pleural Effusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzc3ODE0NTc0MDI5MTA0)",	
            "[<b>1. Pulmonology - Pneumoconiosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzc4ODE2NTk4Mzg0MDMx)",	
            "[<b>1. Pulmonology - Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzc5ODE4NjIyNzM4OTU4)",	
            "[<b>1. Pulmonology - Pneumothorax atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzgwODIwNjQ3MDkzODg1)",	
            "[<b>1. Pulmonology - Pulmonary Thromboembolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzgxODIyNjcxNDQ4ODEy)",	
            "[<b>1. Pulmonology - Respiratory Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzgyODI0Njk1ODAzNzM5)",	
            "[<b>1. Pulmonology - Tuberculosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzgzODI2NzIwMTU4NjY2)",	
            "[<b>2. Seizures and Epilepsy - Status Epilepticus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzg0ODI4NzQ0NTEzNTkz)",	
            "[<b>2. Seizures and Epilepsy - Women and Epilepsy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzg1ODMwNzY4ODY4NTIw)",	
            "[<b>2. Seizures and Epilepsy - Basics of Eeg atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzg2ODMyNzkzMjIzNDQ3)",	
            "[<b>2. Seizures and Epilepsy - Causes of Seizures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzg3ODM0ODE3NTc4Mzc0)",	
            "[<b>2. Seizures and Epilepsy - Classification of Seizures Epilepsy and Epilepsy Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzg4ODM2ODQxOTMzMzAx)",	
            "[<b>2. Seizures and Epilepsy - Drug Resistant Epilepsy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzg5ODM4ODY2Mjg4MjI4)",	
            "[<b>2. Seizures and Epilepsy - Epilepsy Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzkwODQwODkwNjQzMTU1)",	
            "[<b>2. Seizures and Epilepsy - Evaluation of First Onset Seizure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzkxODQyOTE0OTk4MDgy)",	
            "[<b>2. Seizures and Epilepsy - General Principles in Management of Seizures and Epilepsy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzkyODQ0OTM5MzUzMDA5)",	
            "[<b>2. Seizures and Epilepsy - Seizure Versus Syncope atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzkzODQ2OTYzNzA3OTM2)",	
            "[<b>3. Cerebrovascular Diseases Module Part - Arterial Supply of Brain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzk0ODQ4OTg4MDYyODYz)",	
            "[<b>3. Cerebrovascular Diseases Module Part - Basic Principles of Stroke Localization atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzk1ODUxMDEyNDE3Nzkw)",	
            "[<b>3. Cerebrovascular Diseases Module Part - Etiopathogenesis of Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzk2ODUzMDM2NzcyNzE3)",	
            "[<b>3. Cerebrovascular Diseases Module Part - Genetic Causes of Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzk3ODU1MDYxMTI3NjQ0)",	
            "[<b>3. Cerebrovascular Diseases Module Part - Subtypes of Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzk4ODU3MDg1NDgyNTcx)",	
            "[<b>3. Cerebrovascular Diseases Module Part - Young Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyNzk5ODU5MTA5ODM3NDk4)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Cerebral Venous Thrombosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODAwODYxMTM0MTkyNDI1)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Intracranial Hemorrhage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODAxODYzMTU4NTQ3MzUy)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Management of Acute Ischemic Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODAyODY1MTgyOTAyMjc5)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Posterior Reversible Encephalopathy Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODAzODY3MjA3MjU3MjA2)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Secondary Prophylaxis of Stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODA0ODY5MjMxNjEyMTMz)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Stroke Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODA1ODcxMjU1OTY3MDYw)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Transient Global Amnesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODA2ODczMjgwMzIxOTg3)",	
            "[<b>4. Cerebrovascular Diseases Module Part - Transient Ischemic Attacks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODA3ODc1MzA0Njc2OTE0)",	
            "[<b>5. Headache and Other Related Disorders - Cdh Ndph atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODA4ODc3MzI5MDMxODQx)",	
            "[<b>5. Headache and Other Related Disorders - Introduction and Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODA5ODc5MzUzMzg2NzY4)",	
            "[<b>5. Headache and Other Related Disorders - Migraine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODEwODgxMzc3NzQxNjk1)",	
            "[<b>5. Headache and Other Related Disorders - Secondary Headaches atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODExODgzNDAyMDk2NjIy)",	
            "[<b>5. Headache and Other Related Disorders - Tension Type Headache atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODEyODg1NDI2NDUxNTQ5)",	
            "[<b>5. Headache and Other Related Disorders - Trigeminal Autonomic Cephalalgias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODEzODg3NDUwODA2NDc2)",	
            "[<b>6. Hypokinetic Movement Disorders Module - Atypical Parkinsonian Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODE0ODg5NDc1MTYxNDAz)",	
            "[<b>6. Hypokinetic Movement Disorders Module - Basal Ganglia Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODE1ODkxNDk5NTE2MzMw)",	
            "[<b>6. Hypokinetic Movement Disorders Module - Parkinson S Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODE2ODkzNTIzODcxMjU3)",	
            "[<b>7. Hyperkinetic Movement Disorders - Chorea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODE3ODk1NTQ4MjI2MTg0)",	
            "[<b>7. Hyperkinetic Movement Disorders - Drug Induced Movement Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODE4ODk3NTcyNTgxMTEx)",	
            "[<b>7. Hyperkinetic Movement Disorders - Dystonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODE5ODk5NTk2OTM2MDM4)",	
            "[<b>7. Hyperkinetic Movement Disorders - Myoclonus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODIwOTAxNjIxMjkwOTY1)",	
            "[<b>7. Hyperkinetic Movement Disorders - Nbia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODIxOTAzNjQ1NjQ1ODky)",	
            "[<b>7. Hyperkinetic Movement Disorders - Restless Legs Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODIyOTA1NjcwMDAwODE5)",	
            "[<b>7. Hyperkinetic Movement Disorders - Tics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODIzOTA3Njk0MzU1NzQ2)",	
            "[<b>7. Hyperkinetic Movement Disorders - Tremor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODI0OTA5NzE4NzEwNjcz)",	
            "[<b>7. Hyperkinetic Movement Disorders - Wilson S Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODI1OTExNzQzMDY1NjAw)",	
            "[<b>8. Dementia - Alzheimer S Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODI2OTEzNzY3NDIwNTI3)",	
            "[<b>8. Dementia - Cortical Versus Subcortical Dementias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODI3OTE1NzkxNzc1NDU0)",	
            "[<b>8. Dementia - Delirium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODI4OTE3ODE2MTMwMzgx)",	
            "[<b>8. Dementia - Frontotemporal Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODI5OTE5ODQwNDg1MzA4)",	
            "[<b>8. Dementia - Normal Pressure Hydrocephalus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODMwOTIxODY0ODQwMjM1)",	
            "[<b>8. Dementia - Parkinsonian Dementias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODMxOTIzODg5MTk1MTYy)",	
            "[<b>8. Dementia - Prion Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODMyOTI1OTEzNTUwMDg5)",	
            "[<b>8. Dementia - Reversible Dementias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODMzOTI3OTM3OTA1MDE2)",	
            "[<b>8. Dementia - Vascular Cognitive Impairment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODM0OTI5OTYyMjU5OTQz)",	
            "[<b>9. Multiple Sclerosis and Other Cns Demyelinationg Disorders - Adem atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODM1OTMxOTg2NjE0ODcw)",	
            "[<b>Multiple Sclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODM2OTM0MDEwOTY5Nzk3)",	
            "[<b>Nmo Spectrum Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODM3OTM2MDM1MzI0NzI0)",	
            "[<b>Non Functional Tumors Suprasellar Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODM4OTM4MDU5Njc5NjUx)",	
            "[<b>10. Ataxia - Ataxias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODM5OTQwMDg0MDM0NTc4)",	
            "[<b>11. Lmn Disorders - Als and Other Motor Neuron Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQwOTQyMTA4Mzg5NTA1)",	
            "[<b>11. Lmn Disorders - Disorders of Neuromuscular Junction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQxOTQ0MTMyNzQ0NDMy)",	
            "[<b>11. Lmn Disorders - Disorders of Peripheral Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQyOTQ2MTU3MDk5MzU5)",	
            "[<b>11. Lmn Disorders - Muscle Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQzOTQ4MTgxNDU0Mjg2)",	
            "[<b>12. Diseases of Spinal Cord - Checklist in a Case of Paraplegia Quadriplegia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQ0OTUwMjA1ODA5MjEz)",	
            "[<b>12. Diseases of Spinal Cord - Classification of Myelopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQ1OTUyMjMwMTY0MTQw)",	
            "[<b>12. Diseases of Spinal Cord - Diseases of Spinal Cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQ2OTU0MjU0NTE5MDY3)",	
            "[<b>12. Diseases of Spinal Cord - Neurogenic Bladder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQ3OTU2Mjc4ODczOTk0)",	
            "[<b>12. Diseases of Spinal Cord - Spinal Cord Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQ4OTU4MzAzMjI4OTIx)",	
            "[<b>13. Cardiology - 1. Cardiomyopathies - Arrhythmogenic Right Ventricular Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODQ5OTYwMzI3NTgzODQ4)",	
            "[<b>13. Cardiology - 1. Cardiomyopathies - Dilated Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODUwOTYyMzUxOTM4Nzc1)",	
            "[<b>13. Cardiology - 1. Cardiomyopathies - Hypertrophic Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODUxOTY0Mzc2MjkzNzAy)",	
            "[<b>13. Cardiology - 1. Cardiomyopathies - Left Ventricular Non Compaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODUyOTY2NDAwNjQ4NjI5)",	
            "[<b>13. Cardiology - 1. Cardiomyopathies - Restrictive Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODUzOTY4NDI1MDAzNTU2)",	
            "[<b>13. Cardiology - 1. Cardiomyopathies - Takotsubo Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODU0OTcwNDQ5MzU4NDgz)",	
            "[<b>13. Cardiology - 2. Hypertension - Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODU1OTcyNDczNzEzNDEw)",	
            "[<b>13. Cardiology - 3. Ischemic Heart Diseases - Atherosclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODU2OTc0NDk4MDY4MzM3)",	
            "[<b>13. Cardiology - 3. Ischemic Heart Diseases - Basics Introduction to ACS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODU3OTc2NTIyNDIzMjY0)",	
            "[<b>13. Cardiology - 3. Ischemic Heart Diseases - Chronic Stable Angina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODU4OTc4NTQ2Nzc4MTkx)",	
            "[<b>13. Cardiology - 3. Ischemic Heart Diseases - Evaluation Management of Nstemi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODU5OTgwNTcxMTMzMTE4)",	
            "[<b>13. Cardiology - 3. Ischemic Heart Diseases - Management of Stemie atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODYwOTgyNTk1NDg4MDQ1)",	
            "[<b>13. Cardiology - 3. Ischemic Heart Diseases - Types of Myocardial Infarction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODYxOTg0NjE5ODQyOTcy)",	
            "[<b>13. Cardiology - 4. Ecg - Basics of Electrocardiography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODYyOTg2NjQ0MTk3ODk5)",	
            "[<b>13. Cardiology - 4. Ecg - Interpretation of Ecg atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODYzOTg4NjY4NTUyODI2)",	
            "[<b>13. Cardiology - 5. Heart Sounds - Heart Sounds atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODY0OTkwNjkyOTA3NzUz)",	
            "[<b>14. Endocrinology - 1. Disorders of Anterior Pituitary Gland - Acquired Hypopituitarism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODY1OTkyNzE3MjYyNjgw)",	
            "[<b>14. Endocrinology - 1. Disorders of Anterior Pituitary Gland - Acromegaly atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODY2OTk0NzQxNjE3NjA3)",	
            "[<b>14. Endocrinology - 1. Disorders of Anterior Pituitary Gland - Congenital Hypopituitarism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODY3OTk2NzY1OTcyNTM0)",	
            "[<b>14. Endocrinology - 1. Disorders of Anterior Pituitary Gland - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODY4OTk4NzkwMzI3NDYx)",	
            "[<b>14. Endocrinology - 1. Disorders of Anterior Pituitary Gland - Pituitary Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODcwMDAwODE0NjgyMzg4)",	
            "[<b>14. Endocrinology - 2. Disorders of Posterior Pituitary Gland - Diabetes Insipidus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODcxMDAyODM5MDM3MzE1)",	
            "[<b>14. Endocrinology - 2. Disorders of Posterior Pituitary Gland - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODcyMDA0ODYzMzkyMjQy)",	
            "[<b>14. Endocrinology - 2. Disorders of Posterior Pituitary Gland - Siadh atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODczMDA2ODg3NzQ3MTY5)",	
            "[<b>14. Endocrinology - 3. Disorders of Thyroid Gland - Basics of Thyroid Function Tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODc0MDA4OTEyMTAyMDk2)",	
            "[<b>14. Endocrinology - 3. Disorders of Thyroid Gland - Hypothyroidism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODc1MDEwOTM2NDU3MDIz)",	
            "[<b>14. Endocrinology - 3. Disorders of Thyroid Gland - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODc2MDEyOTYwODExOTUw)",	
            "[<b>14. Endocrinology - 3. Disorders of Thyroid Gland - Thyrotoxicosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODc3MDE0OTg1MTY2ODc3)",	
            "[<b>14. Endocrinology - 4. Disorders Fo Parathyroid Gland - Hypoparathyroidism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODc4MDE3MDA5NTIxODA0)",	
            "[<b>14. Endocrinology - 4. Disorders Fo Parathyroid Gland - Introduction Hyperparathyroidism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODc5MDE5MDMzODc2NzMx)",	
            "[<b>14. Endocrinology - 4. Disorders Fo Parathyroid Gland - Pseudohypoparathyroidism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODgwMDIxMDU4MjMxNjU4)",	
            "[<b>14. Endocrinology - 5. Disorders of Adrenal - Adrenal Insufficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODgxMDIzMDgyNTg2NTg1)",	
            "[<b>14. Endocrinology - 5. Disorders of Adrenal - Cushing S Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODgyMDI1MTA2OTQxNTEy)",	
            "[<b>14. Endocrinology - 5. Disorders of Adrenal - Hyperaldosteronism  atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODgzMDI3MTMxMjk2NDM5)",	
            "[<b>14. Endocrinology - 5. Disorders of Adrenal - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODg0MDI5MTU1NjUxMzY2)",	
            "[<b>14. Endocrinology - 5. Disorders of Adrenal - Pheochromocytoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODg1MDMxMTgwMDA2Mjkz)",	
            "[<b>14. Endocrinology - 6. Men & Meons - Men Meons atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODg2MDMzMjA0MzYxMjIw)",	
            "[<b>14. Endocrinology - 7. Diabetes Mellitus - Acute Complications of Diabetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODg3MDM1MjI4NzE2MTQ3)",	
            "[<b>14. Endocrinology - 7. Diabetes Mellitus - Chronic Complications of Diabetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODg4MDM3MjUzMDcxMDc0)",	
            "[<b>14. Endocrinology - 7. Diabetes Mellitus - Diagnosis of Diabetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODg5MDM5Mjc3NDI2MDAx)",	
            "[<b>14. Endocrinology - 7. Diabetes Mellitus - Introduction and Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODkwMDQxMzAxNzgwOTI4)",	
            "[<b>14. Endocrinology - 7. Diabetes Mellitus - Management of Diabetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODkxMDQzMzI2MTM1ODU1)",	
            "[<b>15. Nephrology - 1. Approach to Proteinuria - Approach to Proteinuria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODkyMDQ1MzUwNDkwNzgy)",	
            "[<b>15. Nephrology - 2. Approach to Hematuria - Approach to Hematuria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODkzMDQ3Mzc0ODQ1NzA5)",	
            "[<b>15. Nephrology - 3. Urine Anlaysis - Urine Analysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODk0MDQ5Mzk5MjAwNjM2)",	
            "[<b>15. Nephrology - 4. Acute Kidney Injury - Acute Kidney Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODk1MDUxNDIzNTU1NTYz)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Cardiovascular Manifestations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODk2MDUzNDQ3OTEwNDkw)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Dermatological Manifestations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODk3MDU1NDcyMjY1NDE3)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Hematological Manifestations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODk4MDU3NDk2NjIwMzQ0)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Introduction Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyODk5MDU5NTIwOTc1Mjcx)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Mineral Bone Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTAwMDYxNTQ1MzMwMTk4)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Neurologic Manifestations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTAxMDYzNTY5Njg1MTI1)",	
            "[<b>15. Nephrology - 5. Chronic Kidney Disease - Overview of Clinical Manifestations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTAyMDY1NTk0MDQwMDUy)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Alport Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTAzMDY3NjE4Mzk0OTc5)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Basic Structure of Glomerulus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTA0MDY5NjQyNzQ5OTA2)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Clinical Presentations of Glomerular Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTA1MDcxNjY3MTA0ODMz)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - FSGS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTA2MDczNjkxNDU5NzYw)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Iga Nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTA3MDc1NzE1ODE0Njg3)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Membranous Nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTA4MDc3NzQwMTY5NjE0)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Minimal Change Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTA5MDc5NzY0NTI0NTQx)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Mpgn atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTEwMDgxNzg4ODc5NDY4)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Psgn atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTExMDgzODEzMjM0Mzk1)",	
            "[<b>15. Nephrology - 6. Glomerular Disorders - Rpgn Goodpasture Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTEyMDg1ODM3NTg5MzIy)",	
            "[<b>15. Nephrology - 7. Vascular Diseases of Kidney - Renal Artery Stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTEzMDg3ODYxOTQ0MjQ5)",	
            "[<b>15. Nephrology - 8. Hereditary Cystic Diseases of Kidney - Adpkd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTE0MDg5ODg2Mjk5MTc2)",	
            "[<b>15. Nephrology - 8. Hereditary Cystic Diseases of Kidney - Arpkd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTE1MDkxOTEwNjU0MTAz)",	
            "[<b>15. Nephrology - 8. Hereditary Cystic Diseases of Kidney - Medullary Sponge Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTE2MDkzOTM1MDA5MDMw)",	
            "[<b>15. Nephrology - 8. Hereditary Cystic Diseases of Kidney - Nephronophthisis Adtkd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTE3MDk1OTU5MzYzOTU3)",	
            "[<b>15. Nephrology - 8. Hereditary Cystic Diseases of Kidney - Tuberous Sclerosis Vhl Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTE4MDk3OTgzNzE4ODg0)",	
            "[<b>16. Rheumatology - Apla Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTE5MTAwMDA4MDczODEx)",	
            "[<b>16. Rheumatology - Crystal Associated Arthropathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTIwMTAyMDMyNDI4NzM4)",	
            "[<b>16. Rheumatology - Igg4 Related Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTIxMTA0MDU2NzgzNjY1)",	
            "[<b>16. Rheumatology - Inflammatory Myopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTIyMTA2MDgxMTM4NTky)",	
            "[<b>16. Rheumatology - Rheumatoid Arthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTIzMTA4MTA1NDkzNTE5)",	
            "[<b>16. Rheumatology - Sarcoidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTI0MTEwMTI5ODQ4NDQ2)",	
            "[<b>16. Rheumatology - Seronegative Spondyloarthritides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTI1MTEyMTU0MjAzMzcz)",	
            "[<b>16. Rheumatology - Sjogren S Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTI2MTE0MTc4NTU4MzAw)",	
            "[<b>16. Rheumatology - Sle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTI3MTE2MjAyOTEzMjI3)",	
            "[<b>16. Rheumatology - Systemic Sclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTI4MTE4MjI3MjY4MTU0)",	
            "[<b>16. Rheumatology - Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTI5MTIwMjUxNjIzMDgx)",	
            "[<b>17. Hematology - 1. Hemolytic Anemias - Introduction and Basics0 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTMwMTIyMjc1OTc4MDA4)",	
            "[<b>17. Hematology - 1. Hemolytic Anemias - Paroxysmal Nocturnal Hemoglobinuria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTMxMTI0MzAwMzMyOTM1)",	
            "[<b>17. Hematology - 2. Plasma Cell Disorders - Introduction and Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTMyMTI2MzI0Njg3ODYy)",	
            "[<b>17. Hematology - 2. Plasma Cell Disorders - Multiple Myeloma Etiopathogenesis and Clinical Features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTMzMTI4MzQ5MDQyNzg5)",	
            "[<b>17. Hematology - 2. Plasma Cell Disorders - Multiple Myeloma Work Up and Staging atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTM0MTMwMzczMzk3NzE2)",	
            "[<b>17. Hematology - 2. Plasma Cell Disorders - Treatment of Multiple Myeloma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTM1MTMyMzk3NzUyNjQz)",	
            "[<b>17. Hematology - 3. Von Willebrand Disease - Von Willebrand Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTM2MTM0NDIyMTA3NTcw)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Chronic Myeloid Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTM3MTM2NDQ2NDYyNDk3)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Essential Thrombocytosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTM4MTM4NDcwODE3NDI0)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Introduction Classification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTM5MTQwNDk1MTcyMzUx)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Polycythemia Vera atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQwMTQyNTE5NTI3Mjc4)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Primary Myelofibrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQxMTQ0NTQzODgyMjA1)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Treatment of Cml atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQyMTQ2NTY4MjM3MTMy)",	
            "[<b>17. Hematology - 4. Myeloproliferative Neoplasms - Treatment of Polycthemia Vera atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQzMTQ4NTkyNTkyMDU5)",	
            "[<b>18. Infectious Diseases - Acute Bacterial Meningitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQ0MTUwNjE2OTQ2OTg2)",	
            "[<b>18. Infectious Diseases - Infective Endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQ1MTUyNjQxMzAxOTEz)",	
            "[<b>18. Infectious Diseases - Management of Covid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQ2MTU0NjY1NjU2ODQw)",	
            "[<b>18. Infectious Diseases - Oxygen Therapy in Covid 19 Patients atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQ3MTU2NjkwMDExNzY3)",	
            "[<b>19. Gastroenterology and Hepatology - Autoimmune Hepatits atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQ4MTU4NzE0MzY2Njk0)",	
            "[<b>19. Gastroenterology and Hepatology - Hemochromatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTQ5MTYwNzM4NzIxNjIx)",	
            "[<b>19. Gastroenterology and Hepatology - Overview of Liver Cirrhosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTUwMTYyNzYzMDc2NTQ4)",	
            "[<b>19. Gastroenterology and Hepatology - Overview of Portal Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTUxMTY0Nzg3NDMxNDc1)",	
            "[<b>19. Gastroenterology and Hepatology - Treatment of Portal Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTUyMTY2ODExNzg2NDAy)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        medicined_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"medicined_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"medicined_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(medicined_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("surgeryd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. General Aspects - Blood Transfusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTUzMTY4ODM2MTQxMzI5)",
            "[<b>1. General Aspects - Inside the Operation Theatre atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTU0MTcwODYwNDk2MjU2)",
            "[<b>1. General Aspects - Instruments Used in Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTU1MTcyODg0ODUxMTgz)",
            "[<b>1. General Aspects - Nutrition in Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTU2MTc0OTA5MjA2MTEw)",
            "[<b>1. General Aspects - Operation Theatre Protocols atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTU3MTc2OTMzNTYxMDM3)",
            "[<b>1. General Aspects - Shock atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTU4MTc4OTU3OTE1OTY0)",
            "[<b>1. General Aspects - Surgical Site Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTU5MTgwOTgyMjcwODkx)",
            "[<b>1. General Aspects - Sutures Needles Blades atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTYwMTgzMDA2NjI1ODE4)",
            "[<b>2. Trauma - Abdominal Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTYxMTg1MDMwOTgwNzQ1)",
            "[<b>2. Trauma - Atls Latest Protocols atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTYyMTg3MDU1MzM1Njcy)",
            "[<b>2. Trauma - Burns atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTYzMTg5MDc5NjkwNTk5)",
            "[<b>2. Trauma - Head Injury Face Injury and Neck Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTY0MTkxMTA0MDQ1NTI2)",
            "[<b>2. Trauma - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTY1MTkzMTI4NDAwNDUz)",
            "[<b>2. Trauma - Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTY2MTk1MTUyNzU1Mzgw)",
            "[<b>2. Trauma - Scoring System in Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTY3MTk3MTc3MTEwMzA3)",
            "[<b>2. Trauma - Thoracic Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTY4MTk5MjAxNDY1MjM0)",
            "[<b>3. Head and Neck, Thyoid and Breast - 1. Head and Neck - Module 2 Salivary Gland atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTY5MjAxMjI1ODIwMTYx)",
            "[<b>3. Head and Neck, Thyoid and Breast - 1. Head and Neck - Module 3 Neck Swellings atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTcwMjAzMjUwMTc1MDg4)",
            "[<b>3. Head and Neck, Thyoid and Breast - 1. Head and Neck - Oral Cavity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTcxMjA1Mjc0NTMwMDE1)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTcyMjA3Mjk4ODg0OTQy)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Clinical Aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTczMjA5MzIzMjM5ODY5)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Graves Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTc0MjExMzQ3NTk0Nzk2)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Investigation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTc1MjEzMzcxOTQ5NzIz)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Miscellaneous Thyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTc2MjE1Mzk2MzA0NjUw)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTc3MjE3NDIwNjU5NTc3)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Thyroid Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTc4MjE5NDQ1MDE0NTA0)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Thyroid Images atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTc5MjIxNDY5MzY5NDMx)",
            "[<b>3. Head and Neck, Thyoid and Breast - 2. Thyroid - Thyroid Surgical Aspect atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTgwMjIzNDkzNzI0MzU4)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Adjuvant Therapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTgxMjI1NTE4MDc5Mjg1)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Clinical Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTgyMjI3NTQyNDM0MjEy)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Images atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTgzMjI5NTY2Nzg5MTM5)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Miscellaneous Topics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTg0MjMxNTkxMTQ0MDY2)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Pathological Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTg1MjMzNjE1NDk4OTkz)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Radiological Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTg2MjM1NjM5ODUzOTIw)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Risk Factors of Cancer Breast atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTg3MjM3NjY0MjA4ODQ3)",
            "[<b>3. Head and Neck, Thyoid and Breast - 3. Breast - Surgical Aspects in Breast Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTg4MjM5Njg4NTYzNzc0)",
            "[<b>3. Head and Neck, Thyoid and Breast - 4. Anatomy of Hernia - Hernia Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTg5MjQxNzEyOTE4NzAx)",
            "[<b>3. Head and Neck, Thyoid and Breast - 4. Anatomy of Hernia - Hernia Surgeries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTkwMjQzNzM3MjczNjI4)",
            "[<b>3. Head and Neck, Thyoid and Breast - 5. Types of Hernia - Named Hernias 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTkxMjQ1NzYxNjI4NTU1)",
            "[<b>3. Head and Neck, Thyoid and Breast - 5. Types of Hernia - Named Hernias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTkyMjQ3Nzg1OTgzNDgy)",
            "[<b>3. Head and Neck, Thyoid and Breast - 6. Laproscopic Anatomy and Hernia Repair - Laparoscopic Hernial Repairs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTkzMjQ5ODEwMzM4NDA5)",
            "[<b>4. Gastrointestinal 1. Esophagus - Barrett S Esophagus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTk0MjUxODM0NjkzMzM2)",
            "[<b>4. Gastrointestinal 1. Esophagus - Diverticulum in Esophagus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTk1MjUzODU5MDQ4MjYz)",
            "[<b>4. Gastrointestinal 1. Esophagus - Esophagus Perforation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTk2MjU1ODgzNDAzMTkw)",
            "[<b>4. Gastrointestinal 1. Esophagus - Gerd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTk3MjU3OTA3NzU4MTE3)",
            "[<b>4. Gastrointestinal 1. Esophagus - Hiatus Hernia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTk4MjU5OTMyMTEzMDQ0)",
            "[<b>4. Gastrointestinal 1. Esophagus - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEyOTk5MjYxOTU2NDY3OTcx)",
            "[<b>4. Gastrointestinal 1. Esophagus - Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDAwMjYzOTgwODIyODk4)",
            "[<b>4. Gastrointestinal 1. Esophagus - Motility Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDAxMjY2MDA1MTc3ODI1)",
            "[<b>4. Gastrointestinal 1. Esophagus - Tumors of Esophagus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDAyMjY4MDI5NTMyNzUy)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Cancer Stomach Intro atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDAzMjcwMDUzODg3Njc5)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Complications of Peptic Ulcer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDA0MjcyMDc4MjQyNjA2)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric H Pylon atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDA1Mjc0MTAyNTk3NTMz)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Miscellaneous Lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDA2Mjc2MTI2OTUyNDYw)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Other Tumors in Stomach atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDA3Mjc4MTUxMzA3Mzg3)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Peptic Ulcer Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDA4MjgwMTc1NjYyMzE0)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Stomach Cancer Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDA5MjgyMjAwMDE3MjQx)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Upper Gi Bleed Protocol atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDEwMjg0MjI0MzcyMTY4)",
            "[<b>4. Gastrointestinal 2. Stomach and Bariatric Vagus Nave Applied Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDExMjg2MjQ4NzI3MDk1)",
            "[<b>4. Gastrointestinal 3. Intestines - Appendix atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDEyMjg4MjczMDgyMDIy)",
            "[<b>4. Gastrointestinal 3. Intestines - Carcinoid Sb Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDEzMjkwMjk3NDM2OTQ5)",
            "[<b>4. Gastrointestinal 3. Intestines - Colon Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDE0MjkyMzIxNzkxODc2)",
            "[<b>4. Gastrointestinal 3. Intestines - Diverticulum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDE1Mjk0MzQ2MTQ2ODAz)",
            "[<b>4. Gastrointestinal 3. Intestines - Hairspring S Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDE2Mjk2MzcwNTAxNzMw)",
            "[<b>4. Gastrointestinal 3. Intestines - Inflammatory Bowel Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDE3Mjk4Mzk0ODU2NjU3)",
            "[<b>4. Gastrointestinal 3. Intestines - Intestinal Obstruction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDE4MzAwNDE5MjExNTg0)",
            "[<b>4. Gastrointestinal 3. Intestines - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDE5MzAyNDQzNTY2NTEx)",
            "[<b>4. Gastrointestinal 3. Intestines - Polyps in Intestine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDIwMzA0NDY3OTIxNDM4)",
            "[<b>4. Gastrointestinal 3. Intestines - Small Bowel Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDIxMzA2NDkyMjc2MzY1)",
            "[<b>4. Gastrointestinal 3. Intestines - Stomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDIyMzA4NTE2NjMxMjky)",
            "[<b>4. Gastrointestinal 3. Intestines - Vascular Diseases of Bowel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDIzMzEwNTQwOTg2MjE5)",
            "[<b>4. Gastrointestinal 4. Rectum and Anus - Malignant Diseases of Rectum and Anus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDI0MzEyNTY1MzQxMTQ2)",
            "[<b>4. Gastrointestinal 4. Rectum and Anus - Rectum and Anus Benign atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDI1MzE0NTg5Njk2MDcz)",
            "[<b>4. Gastrointestinal 5. Miscellaneous - Miscellaneous Topics in Git atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDI2MzE2NjE0MDUxMDAw)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Bile Duct Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDI3MzE4NjM4NDA1OTI3)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Biliary Malignancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDI4MzIwNjYyNzYwODU0)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Cbd Stones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDI5MzIyNjg3MTE1Nzgx)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Gall Stones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDMwMzI0NzExNDcwNzA4)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Gallbladder and Bile Duct atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDMxMzI2NzM1ODI1NjM1)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Management of Gall Stones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDMyMzI4NzYwMTgwNTYy)",
            "[<b>5. Hepatobiliary and Pancreatic System - 1. Gallbladder and Biliary System - Miscellaneous Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDMzMzMwNzg0NTM1NDg5)",
            "[<b>5. Hepatobiliary and Pancreatic System - 2. Pancreas - Chronic Pancreatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDM0MzMyODA4ODkwNDE2)",
            "[<b>5. Hepatobiliary and Pancreatic System - 2. Pancreas - Pancreas Acute Pancreatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDM1MzM0ODMzMjQ1MzQz)",
            "[<b>5. Hepatobiliary and Pancreatic System - 2. Pancreas - Pancreas Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDM2MzM2ODU3NjAwMjcw)",
            "[<b>5. Hepatobiliary and Pancreatic System - 2. Pancreas - Pancreatic Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDM3MzM4ODgxOTU1MTk3)",
            "[<b>5. Hepatobiliary and Pancreatic System - 3. Liver - Infections in Liver atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDM4MzQwOTA2MzEwMTI0)",
            "[<b>5. Hepatobiliary and Pancreatic System - 3. Liver - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDM5MzQyOTMwNjY1MDUx)",
            "[<b>5. Hepatobiliary and Pancreatic System - 3. Liver - Liver Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQwMzQ0OTU1MDE5OTc4)",
            "[<b>5. Hepatobiliary and Pancreatic System - 3. Liver - Portal Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQxMzQ2OTc5Mzc0OTA1)",
            "[<b>5. Hepatobiliary and Pancreatic System - 4. Spleen - Spleen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQyMzQ5MDAzNzI5ODMy)",
            "[<b>6. Surgical Speciality Topics - 1. Urology - Urology 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQzMzUxMDI4MDg0NzU5)",
            "[<b>6. Surgical Speciality Topics - 1. Urology - Urology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQ0MzUzMDUyNDM5Njg2)",
            "[<b>6. Surgical Speciality Topics - 2. Vascular - Artery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQ1MzU1MDc2Nzk0NjEz)",
            "[<b>6. Surgical Speciality Topics - 2. Vascular - Lymphatics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQ2MzU3MTAxMTQ5NTQw)",
            "[<b>6. Surgical Speciality Topics - 2. Vascular - Venous System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQ3MzU5MTI1NTA0NDY3)",
            "[<b>6. Surgical Speciality Topics - 3. Plastic Surgery and Skin Lesions - Plastic Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQ4MzYxMTQ5ODU5Mzk0)",
            "[<b>6. Surgical Speciality Topics - 4. Paediatrics Paediatrics Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDQ5MzYzMTc0MjE0MzIx)",
            "[<b>6. Surgical Speciality Topics - 5. OncoSkin Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDUwMzY1MTk4NTY5MjQ4)",
            "[<b>6. Surgical Speciality Topics - 6. Cardiothoracic Cardiothoracic Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDUxMzY3MjIyOTI0MTc1)",
            "[<b>6. Surgical Speciality Topics - 6. Cardiothoracic Thoracic Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDUyMzY5MjQ3Mjc5MTAy)",
            "[<b>6. Surgical Speciality Topics - 7. Endocrine Adrenal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDUzMzcxMjcxNjM0MDI5)",
            "[<b>6. Surgical Speciality Topics - 7. Endocrine Men Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDU0MzczMjk1OTg4OTU2)",
            "[<b>6. Surgical Speciality Topics - 7. Endocrine Parathyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDU1Mzc1MzIwMzQzODgz)",
            "[<b>6. Surgical Speciality Topics - 8. NeuroNeurosurgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDU2Mzc3MzQ0Njk4ODEw)",
            "[<b>6. Surgical Speciality Topics - 9. Transplantation - Advance Transplant atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDU3Mzc5MzY5MDUzNzM3)",
            "[<b>6. Surgical Speciality Topics - 9. Transplantation - Basics of Transplant atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDU4MzgxMzkzNDA4NjY0)",
            "[<b>7. Qrp - Ini Cet Qrp 2021 Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDU5MzgzNDE3NzYzNTkx)",
            "[<b>7. Qrp - Surgery by Dr Rajamahendran atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDYwMzg1NDQyMTE4NTE4)",
            "[<b>7. Qrp - Surgery Session 1 by Dr Rajamahendran atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDYxMzg3NDY2NDczNDQ1)",
            "[<b>7. Qrp - Surgery Session 2 by Dr Rajamahendran atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDYyMzg5NDkwODI4Mzcy)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        surgeryd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"surgeryd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"surgeryd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(surgeryd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("obgyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Basics of Obstetrics - Amniotic Fluid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDYzMzkxNTE1MTgzMjk5)",
            "[<b>1. Basics of Obstetrics - Anatomy of Female Genital Tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDY0MzkzNTM5NTM4MjI2)",
            "[<b>1. Basics of Obstetrics - Cardiovascular Changes of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDY1Mzk1NTYzODkzMTUz)",
            "[<b>1. Basics of Obstetrics - Diagnosis of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDY2Mzk3NTg4MjQ4MDgw)",
            "[<b>1. Basics of Obstetrics - Fetal Circulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDY3Mzk5NjEyNjAzMDA3)",
            "[<b>1. Basics of Obstetrics - Fetal Endocrinology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDY4NDAxNjM2OTU3OTM0)",
            "[<b>1. Basics of Obstetrics - Fundamentals of Reproduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDY5NDAzNjYxMzEyODYx)",
            "[<b>1. Basics of Obstetrics - Hematological Changes of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDcwNDA1Njg1NjY3Nzg4)",
            "[<b>1. Basics of Obstetrics - Nst and Ctg atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDcxNDA3NzEwMDIyNzE1)",
            "[<b>1. Basics of Obstetrics - Physiological Changes of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDcyNDA5NzM0Mzc3NjQy)",
            "[<b>1. Basics of Obstetrics - Placenta and Umbilical Cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDczNDExNzU4NzMyNTY5)",
            "[<b>1. Basics of Obstetrics - Placental Hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDc0NDEzNzgzMDg3NDk2)",
            "[<b>1. Basics of Obstetrics - Respiratory Urinary System and Gi Changes of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDc1NDE1ODA3NDQyNDIz)",
            "[<b>2. Normal Labour - Induction Augmentation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDc2NDE3ODMxNzk3MzUw)",
            "[<b>2. Normal Labour - Maternal Pelvis and Fetal Skull atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDc3NDE5ODU2MTUyMjc3)",
            "[<b>2. Normal Labour - Normal Puerperium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDc4NDIxODgwNTA3MjA0)",
            "[<b>2. Normal Labour - Physiology of Labor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDc5NDIzOTA0ODYyMTMx)",
            "[<b>2. Normal Labour - Stages of Labour and Partogram atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDgwNDI1OTI5MjE3MDU4)",
            "[<b>3. Abnormal Labour - Breech Presentation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDgxNDI3OTUzNTcxOTg1)",
            "[<b>3. Abnormal Labour - Caesarean Section atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDgyNDI5OTc3OTI2OTEy)",
            "[<b>3. Abnormal Labour - Cord Prolapse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDgzNDMyMDAyMjgxODM5)",
            "[<b>3. Abnormal Labour - Episiotomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDg0NDM0MDI2NjM2NzY2)",
            "[<b>3. Abnormal Labour - Face and Brow Presentation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDg1NDM2MDUwOTkxNjkz)",
            "[<b>3. Abnormal Labour - Occipitoposterior Position atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDg2NDM4MDc1MzQ2NjIw)",
            "[<b>3. Abnormal Labour - Post Dated Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDg3NDQwMDk5NzAxNTQ3)",
            "[<b>3. Abnormal Labour - Preterm Labor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDg4NDQyMTI0MDU2NDc0)",
            "[<b>3. Abnormal Labour - Prolonged Labour Obstructed Labour and Precipitate Labour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDg5NDQ0MTQ4NDExNDAx)",
            "[<b>3. Abnormal Labour - Shoulder Dystocia Contracted Pelvis and Cpd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDkwNDQ2MTcyNzY2MzI4)",
            "[<b>3. Abnormal Labour - Transverse Lie Unstable Lie and Compound Presentation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDkxNDQ4MTk3MTIxMjU1)",
            "[<b>4. Third Stage Abnormalities - Amniotic Fluid Embolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDkyNDUwMjIxNDc2MTgy)",
            "[<b>4. Third Stage Abnormalities - Placenta Accreta and Retained Placenta atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDkzNDUyMjQ1ODMxMTA5)",
            "[<b>4. Third Stage Abnormalities - Postpartum Hemorrhage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDk0NDU0MjcwMTg2MDM2)",
            "[<b>4. Third Stage Abnormalities - Third and Fourth Degree Perineal Tears atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDk1NDU2Mjk0NTQwOTYz)",
            "[<b>4. Third Stage Abnormalities - Uteine Inversion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDk2NDU4MzE4ODk1ODkw)",
            "[<b>5. Complication of Pregnancy - Acute Fatty Liver of Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDk3NDYwMzQzMjUwODE3)",
            "[<b>5. Complication of Pregnancy - Antepartum Haemorrhage atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDk4NDYyMzY3NjA1NzQ0)",
            "[<b>5. Complication of Pregnancy - Apla atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMDk5NDY0MzkxOTYwNjcx)",
            "[<b>5. Complication of Pregnancy - Causes of Abortion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTAwNDY2NDE2MzE1NTk4)",
            "[<b>5. Complication of Pregnancy - Cx Incompetence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTAxNDY4NDQwNjcwNTI1)",
            "[<b>5. Complication of Pregnancy - Definition and Types of Abortion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTAyNDcwNDY1MDI1NDUy)",
            "[<b>5. Complication of Pregnancy - Diabities Complicating Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTAzNDcyNDg5MzgwMzc5)",
            "[<b>5. Complication of Pregnancy - Drugs in Obstetric atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTA0NDc0NTEzNzM1MzA2)",
            "[<b>5. Complication of Pregnancy - Ectopic Pregnancy 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTA1NDc2NTM4MDkwMjMz)",
            "[<b>5. Complication of Pregnancy - Ectopic Pregnancy 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTA2NDc4NTYyNDQ1MTYw)",
            "[<b>5. Complication of Pregnancy - Fetal Anomalies in Pregnancy Prenatal Testing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTA3NDgwNTg2ODAwMDg3)",
            "[<b>5. Complication of Pregnancy - Gestational Trophoblastic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTA4NDgyNjExMTU1MDE0)",
            "[<b>5. Complication of Pregnancy - Heart Disease in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTA5NDg0NjM1NTA5OTQx)",
            "[<b>5. Complication of Pregnancy - Hiv in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTEwNDg2NjU5ODY0ODY4)",
            "[<b>5. Complication of Pregnancy - Hyperemesis Gravidarum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTExNDg4Njg0MjE5Nzk1)",
            "[<b>5. Complication of Pregnancy - Hypertensive Disorders in Pregnancy 1 Definition Risk Factors 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTEyNDkwNzA4NTc0NzIy)",
            "[<b>5. Complication of Pregnancy - Hypertensive Disorders in Pregnancy 2 Pathophysiology Markers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTEzNDkyNzMyOTI5NjQ5)",
            "[<b>5. Complication of Pregnancy - Hypertensive Disorders in Pregnancy 3 End Organ Changes Prediction Prevention atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTE0NDk0NzU3Mjg0NTc2)",
            "[<b>5. Complication of Pregnancy - Intrahepatic Cholestasis of Pregnency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTE1NDk2NzgxNjM5NTAz)",
            "[<b>5. Complication of Pregnancy - Intrauterine Growth Retardation Iugr atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTE2NDk4ODA1OTk0NDMw)",
            "[<b>5. Complication of Pregnancy - Iron Deficiency Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTE3NTAwODMwMzQ5MzU3)",
            "[<b>5. Complication of Pregnancy - Malaria in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTE4NTAyODU0NzA0Mjg0)",
            "[<b>5. Complication of Pregnancy - Mcqs on Pregnency After Previeus Caesarean atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTE5NTA0ODc5MDU5MjEx)",
            "[<b>5. Complication of Pregnancy - Multifetal Pregnancy Complications of Twin Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTIwNTA2OTAzNDE0MTM4)",
            "[<b>5. Complication of Pregnancy - Multifetal Pregnancy Diagnosis of Twin Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTIxNTA4OTI3NzY5MDY1)",
            "[<b>5. Complication of Pregnancy - Multifetal Pregnancy Management of Twin Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTIyNTEwOTUyMTIzOTky)",
            "[<b>5. Complication of Pregnancy - Multifetal Pregnancy Types Risk Factors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTIzNTEyOTc2NDc4OTE5)",
            "[<b>5. Complication of Pregnancy - Pregnency After Previeus Caesarean atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTI0NTE1MDAwODMzODQ2)",
            "[<b>5. Complication of Pregnancy - Red Cell Alloimmunisation in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTI1NTE3MDI1MTg4Nzcz)",
            "[<b>5. Complication of Pregnancy - Rh Negative Mother atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTI2NTE5MDQ5NTQzNzAw)",
            "[<b>5. Complication of Pregnancy - Rubella in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTI3NTIxMDczODk4NjI3)",
            "[<b>5. Complication of Pregnancy - Sickle Cell Disease in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTI4NTIzMDk4MjUzNTU0)",
            "[<b>5. Complication of Pregnancy - Thyroid Disorders in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTI5NTI1MTIyNjA4NDgx)",
            "[<b>5. Complication of Pregnancy - Torch in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTMwNTI3MTQ2OTYzNDA4)",
            "[<b>5. Complication of Pregnancy - Varicella in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTMxNTI5MTcxMzE4MzM1)",
            "[<b>5. Complication of Pregnancy - Venous Thromboembolism in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTMyNTMxMTk1NjczMjYy)",
            "[<b>5. Complication of Pregnancy - Viral Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTMzNTMzMjIwMDI4MTg5)",
            "[<b>5. Cpcr - Complications in or Cpr atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTM0NTM1MjQ0MzgzMTE2)",
            "[<b>6. General Gynaecology - Anatomy of Female Genital Tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTM1NTM3MjY4NzM4MDQz)",
            "[<b>6. General Gynaecology - Dysmenorrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTM2NTM5MjkzMDkyOTcw)",
            "[<b>6. General Gynaecology - Physiology of Menstruation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTM3NTQxMzE3NDQ3ODk3)",
            "[<b>6. General Gynaecology - Precocious Puberty atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTM4NTQzMzQxODAyODI0)",
            "[<b>6. General Gynaecology - Premenstrual Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTM5NTQ1MzY2MTU3NzUx)",
            "[<b>7. Benign Diseases of Genital Tract - Abnormal Uterine Bleeding Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQwNTQ3MzkwNTEyNjc4)",
            "[<b>7. Benign Diseases of Genital Tract - Abnormal Uterine Bleeding Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQxNTQ5NDE0ODY3NjA1)",
            "[<b>7. Benign Diseases of Genital Tract - Degeneration atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQyNTUxNDM5MjIyNTMy)",
            "[<b>7. Benign Diseases of Genital Tract - Endometriosis and Adenomyosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQzNTUzNDYzNTc3NDU5)",
            "[<b>7. Benign Diseases of Genital Tract - Genital Tuberculosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQ0NTU1NDg3OTMyMzg2)",
            "[<b>7. Benign Diseases of Genital Tract - Lower Genital Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQ1NTU3NTEyMjg3MzEz)",
            "[<b>7. Benign Diseases of Genital Tract - Pelvic Inflammatory Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQ2NTU5NTM2NjQyMjQw)",
            "[<b>7. Benign Diseases of Genital Tract - Risk Fctors Types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQ3NTYxNTYwOTk3MTY3)",
            "[<b>7. Benign Diseases of Genital Tract - Symptoms Treatment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQ4NTYzNTg1MzUyMDk0)",
            "[<b>8. Disorders of Menstruation - Androgen Insensitivity Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTQ5NTY1NjA5NzA3MDIx)",
            "[<b>8. Disorders of Menstruation - Developmental Anomalies of Mullerian Duct atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTUwNTY3NjM0MDYxOTQ4)",
            "[<b>8. Disorders of Menstruation - Differential Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTUxNTY5NjU4NDE2ODc1)",
            "[<b>8. Disorders of Menstruation - Female Infertility Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTUyNTcxNjgyNzcxODAy)",
            "[<b>8. Disorders of Menstruation - Female Infertility Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTUzNTczNzA3MTI2NzI5)",
            "[<b>8. Disorders of Menstruation - Male Infertility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTU0NTc1NzMxNDgxNjU2)",
            "[<b>8. Disorders of Menstruation - Ovulation Induction and Hyperstimulation Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTU1NTc3NzU1ODM2NTgz)",
            "[<b>8. Disorders of Menstruation - Pcos and Anovulation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTU2NTc5NzgwMTkxNTEw)",
            "[<b>8. Disorders of Menstruation - Primary Amenorrhea 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTU3NTgxODA0NTQ2NDM3)",
            "[<b>8. Disorders of Menstruation - Primary Amenorrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTU4NTgzODI4OTAxMzY0)",
            "[<b>8. Disorders of Menstruation - Secondary Amenorrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTU5NTg1ODUzMjU2Mjkx)",
            "[<b>8. Disorders of Menstruation - Swyers Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTYwNTg3ODc3NjExMjE4)",
            "[<b>8. Disorders of Menstruation - Turner Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTYxNTg5OTAxOTY2MTQ1)",
            "[<b>9. Gynaecological Oncology - Cancer Cervix atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTYyNTkxOTI2MzIxMDcy)",
            "[<b>9. Gynaecological Oncology - Classification Risk Factors Familial Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTYzNTkzOTUwNjc1OTk5)",
            "[<b>9. Gynaecological Oncology - Endometrial Cancer Diagnosis Staging Treatment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTY0NTk1OTc1MDMwOTI2)",
            "[<b>9. Gynaecological Oncology - Endometrial Cancer Histology Types Grading atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTY1NTk3OTk5Mzg1ODUz)",
            "[<b>9. Gynaecological Oncology - Epithelial Ovarian Cancer Clasification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTY2NjAwMDIzNzQwNzgw)",
            "[<b>9. Gynaecological Oncology - Epithelial Ovarian Cancer Staging Treatment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTY3NjAyMDQ4MDk1NzA3)",
            "[<b>9. Gynaecological Oncology - Germ Cell Sex Cord Stromal Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTY4NjA0MDcyNDUwNjM0)",
            "[<b>9. Gynaecological Oncology - Premalignant Lesions of Cervix atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTY5NjA2MDk2ODA1NTYx)",
            "[<b>9. Gynaecological Oncology - Uterine Sacroma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTcwNjA4MTIxMTYwNDg4)",
            "[<b>9. Gynaecological Oncology - Vulval Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTcxNjEwMTQ1NTE1NDE1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        obgyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"obgyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"obgyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(obgyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pediatricsd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Free Videos - Multi Discplinary Approach Mda to a Child With Abdominal Mass atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTcyNjEyMTY5ODcwMzQy)",
            "[<b>2. General - Abnormal Head Sizes Craniosynostosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTczNjE0MTk0MjI1MjY5)",
            "[<b>2. General - AdolescDevelopmatf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTc0NjE2MjE4NTgwMTk2)",
            "[<b>2. General - Behavioral Disorders in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTc1NjE4MjQyOTM1MTIz)",
            "[<b>2. General - Growth and Anthropometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTc2NjIwMjY3MjkwMDUw)",
            "[<b>2. General - Normal DevelopmAssessmatf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTc3NjIyMjkxNjQ0OTc3)",
            "[<b>3. Nutrition - Rickets MicronutriDeficiencies a Clinical Perspective atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTc4NjI0MzE1OTk5OTA0)",
            "[<b>3. Nutrition - Severe Acute Malnutrition in Depth Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTc5NjI2MzQwMzU0ODMx)",
            "[<b>3. Nutrition - Obesity in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTgwNjI4MzY0NzA5NzU4)",
            "[<b>3. Nutrition - Nutritional Assessmand Pem Grades atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTgxNjMwMzg5MDY0Njg1)",
            "[<b>3. Nutrition - Short Stature in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTgyNjMyNDEzNDE5NjEy)",
            "[<b>4. Neonatology - Breast Feeding Nutrition in Neonates atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTgzNjM0NDM3Nzc0NTM5)",
            "[<b>4. Neonatology - Neonatal Respiratory Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTg0NjM2NDYyMTI5NDY2)",
            "[<b>4. Neonatology - Neonatal Resuscitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTg1NjM4NDg2NDg0Mzkz)",
            "[<b>4. Neonatology - Neonatal Sepsis Nec atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTg2NjQwNTEwODM5MzIw)",
            "[<b>4. Neonatology - Normal Neonate Prematurity High Risk Newborns atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTg3NjQyNTM1MTk0MjQ3)",
            "[<b>4. Neonatology - Neonatal Jaundice Including Neonatal Cholestasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTg4NjQ0NTU5NTQ5MTc0)",
            "[<b>4. Neonatology - Neonatal Hypothermia Neonatal Hypoglycemia and Infant of Diabetic Mother atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTg5NjQ2NTgzOTA0MTAx)",
            "[<b>5. Pediatric Infections - Bacterial Infections in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTkwNjQ4NjA4MjU5MDI4)",
            "[<b>5. Pediatric Infections - Congenital Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTkxNjUwNjMyNjEzOTU1)",
            "[<b>5. Pediatric Infections - Covid in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTkyNjUyNjU2OTY4ODgy)",
            "[<b>5. Pediatric Infections - Viral Infections in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTkzNjU0NjgxMzIzODA5)",
            "[<b>6. Genetics and Syndromes - Trisomies and Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTk0NjU2NzA1Njc4NzM2)",
            "[<b>7. Pulmonology - Asthma Acute Bronchiolitis Foreign Body Aspiration atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTk1NjU4NzMwMDMzNjYz)",
            "[<b>7. Pulmonology - Cystic Fibrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTk2NjYwNzU0Mzg4NTkw)",
            "[<b>7. Pulmonology - Pneumonias in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTk3NjYyNzc4NzQzNTE3)",
            "[<b>7. Pulmonology - Cong Disorders and Upper Respiratory Tract Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTk4NjY0ODAzMDk4NDQ0)",
            "[<b>8. Immunization and Immunodeficiency - Vaccines and Related Clinical Scenarios atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMTk5NjY2ODI3NDUzMzcx)",
            "[<b>8. Immunization and Immunodeficiency - Primary Immunodeficiency 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjAwNjY4ODUxODA4Mjk4)",
            "[<b>8. Immunization and Immunodeficiency - Primary Immunodeficiency 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjAxNjcwODc2MTYzMjI1)",
            "[<b>9. Rheumatology and Vasculitis - Jia Jdm4 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjAyNjcyOTAwNTE4MTUy)",
            "[<b>9. Rheumatology and Vasculitis - Vasculitis Kawasaki Disease Hsp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjAzNjc0OTI0ODczMDc5)",
            "[<b>10. Nephrology - Nephrotic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjA0Njc2OTQ5MjI4MDA2)",
            "[<b>10. Nephrology - Nocturnal Enuresis in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjA1Njc4OTczNTgyOTMz)",
            "[<b>10. Nephrology - Acute Kidney Injury Aki Chronic Kidney Disease Ckd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjA2NjgwOTk3OTM3ODYw)",
            "[<b>10. Nephrology - Cong Disorders Uti Husc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjA3NjgzMDIyMjkyNzg3)",
            "[<b>10. Nephrology - Childhood Glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjA4Njg1MDQ2NjQ3NzE0)",
            "[<b>10. Nephrology - Key Tubular Disorders in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjA5Njg3MDcxMDAyNjQx)",
            "[<b>11. Pediatric Neurology - Cerebral Palsy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjEwNjg5MDk1MzU3NTY4)",
            "[<b>11. Pediatric Neurology - Cns Infections Raised Icp in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjExNjkxMTE5NzEyNDk1)",
            "[<b>11. Pediatric Neurology - Neurocutaneous Syndromes in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjEyNjkzMTQ0MDY3NDIy)",
            "[<b>11. Pediatric Neurology - Ntd Hydrocephalus Other Congenital Cns Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjEzNjk1MTY4NDIyMzQ5)",
            "[<b>11. Pediatric Neurology - Seizures Epilepsy in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjE0Njk3MTkyNzc3Mjc2)",
            "[<b>12. Metabolic Disorders and Pediatric Endocrinology - Congenital Adrenal Hyperplasia a Conceptual Approach atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjE1Njk5MjE3MTMyMjAz)",
            "[<b>12. Metabolic Disorders and Pediatric Endocrinology - Diabetes Mellitus in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjE2NzAxMjQxNDg3MTMw)",
            "[<b>12. Metabolic Disorders and Pediatric Endocrinology - General Carb Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjE3NzAzMjY1ODQyMDU3)",
            "[<b>12. Metabolic Disorders and Pediatric Endocrinology - Pituitary Thyroid Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjE4NzA1MjkwMTk2OTg0)",
            "[<b>12. Metabolic Disorders and Pediatric Endocrinology - Key Amino Acid Metabolism Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjE5NzA3MzE0NTUxOTEx)",
            "[<b>13. Pediatric Git - Esophagus Stomach Intestines atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjIwNzA5MzM4OTA2ODM4)",
            "[<b>13. Pediatric Git - Miscellaneous Git Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjIxNzExMzYzMjYxNzY1)",
            "[<b>13. Pediatric Git - Childhood Diarrheas and Related Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjIyNzEzMzg3NjE2Njky)",
            "[<b>14. Pediatric Hematology and Oncology - Anemias in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjIzNzE1NDExOTcxNjE5)",
            "[<b>14. Pediatric Hematology and Oncology - Childhood Lymphomas and Brain Tumours atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjI0NzE3NDM2MzI2NTQ2)",
            "[<b>14. Pediatric Hematology and Oncology - Wilms Tumor Neuroblastoma Retinoblastoma Langerhans Cell Histiocytosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjI1NzE5NDYwNjgxNDcz)",
            "[<b>14. Pediatric Hematology and Oncology - General Oncology Leukemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjI2NzIxNDg1MDM2NDAw)",
            "[<b>14. Pediatric Hematology and Oncology - Bleeding Coagulation Disorders in Children atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjI3NzIzNTA5MzkxMzI3)",
            "[<b>15. Pediatric Critical Care - Shock in Children ManagemProtocol atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjI4NzI1NTMzNzQ2MjU0)",
            "[<b>15. Pediatric Critical Care - Pals 2020 Summary Cpr Pediatric Tachycardia Managematf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjI5NzI3NTU4MTAxMTgx)",
            "[<b>18. Pediatric Cardiology - Acyanotic Congenital Heart Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjMwNzI5NTgyNDU2MTA4)",
            "[<b>18. Pediatric Cardiology - Acute Rheumatic Fever and Infective Endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjMxNzMxNjA2ODExMDM1)",
            "[<b>18. Pediatric Cardiology - Ccf Fetal Circulation Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjMyNzMzNjMxMTY1OTYy)",
            "[<b>18. Pediatric Cardiology - Cyanotic Congenital Heart Diseases Ductus DependLesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjMzNzM1NjU1NTIwODg5)",
            "[<b>18. Pediatric Cardiology - Classification of Congenital Heart Disease Epidemiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjM0NzM3Njc5ODc1ODE2)",
            "[<b>17. Extra Edge Topics for Inicet - Hlh Syndrome and Macrophage Activation Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjM1NzM5NzA0MjMwNzQz)",
            "[<b>16. Pediatric Integrated Topics - Cdh Tef atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjM2NzQxNzI4NTg1Njcw)",
            "[<b>19. Qrp - Ini Cet Qrp 2021 Mcq S Discussion 791F3b2d 509B 4046 Bede F9a4be359307 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjM3NzQzNzUyOTQwNTk3)",
            "[<b>19. Qrp - Ini Cet Quick Revision Program by Dr Sandeep Sharma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjM4NzQ1Nzc3Mjk1NTI0)",
            "[<b>19. Qrp - Ini Cet Quick Revision Program 2021 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjM5NzQ3ODAxNjUwNDUx)",
            "[<b>19. Qrp - by Dr Sandeep Sharma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQwNzQ5ODI2MDA1Mzc4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pediatricsd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pediatricsd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pediatricsd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pediatricsd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psychiatryd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Introduction to Psychiatry, History Taking and Mental Status Examination - Diagnosis in Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQxNzUxODUwMzYwMzA1)",
            "[<b>1. Introduction to Psychiatry, History Taking and Mental Status Examination - History Taking Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQyNzUzODc0NzE1MjMy)",
            "[<b>1. Introduction to Psychiatry, History Taking and Mental Status Examination - Mental Status Examination Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQzNzU1ODk5MDcwMTU5)",
            "[<b>1. Introduction to Psychiatry, History Taking and Mental Status Examination - Mental Status Examination Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQ0NzU3OTIzNDI1MDg2)",
            "[<b>1. Introduction to Psychiatry, History Taking and Mental Status Examination - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQ1NzU5OTQ3NzgwMDEz)",
            "[<b>1. Introduction to Psychiatry, History Taking and Mental Status Examination - Mental Status Examination Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQ2NzYxOTcyMTM0OTQw)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Attention Deficit Hyperactivity Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQ3NzYzOTk2NDg5ODY3)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Autism Spectrum Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQ4NzY2MDIwODQ0Nzk0)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Communication Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjQ5NzY4MDQ1MTk5NzIx)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Intellectual Disability atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjUwNzcwMDY5NTU0NjQ4)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Motor Disorders Tic Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjUxNzcyMDkzOTA5NTc1)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjUyNzc0MTE4MjY0NTAy)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Movement Disorders Others atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjUzNzc2MTQyNjE5NDI5)",
            "[<b>2. Neurodevelopmental Disorders Dsm - Specific Learning Disability atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjU0Nzc4MTY2OTc0MzU2)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Atpd Brief Psychotic Disorders Schizoaffective Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjU1NzgwMTkxMzI5Mjgz)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Catatonia Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjU2NzgyMjE1Njg0MjEw)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Schizophrenia Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjU3Nzg0MjQwMDM5MTM3)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Overview of Psychosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjU4Nzg2MjY0Mzk0MDY0)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Delusional Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjU5Nzg4Mjg4NzQ4OTkx)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Important Points About Schizophrenia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjYwNzkwMzEzMTAzOTE4)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Schizophrenia Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjYxNzkyMzM3NDU4ODQ1)",
            "[<b>3. Schizophrenia and Other Psychotic Spect Disorders - Schizophrenia Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjYyNzk0MzYxODEzNzcy)",
            "[<b>4. Mood Disorders - Cyclothymia vs Dysthymia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjYzNzk2Mzg2MTY4Njk5)",
            "[<b>4. Mood Disorders - Dmdd Pmdd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjY0Nzk4NDEwNTIzNjI2)",
            "[<b>4. Mood Disorders - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjY1ODAwNDM0ODc4NTUz)",
            "[<b>4. Mood Disorders - Major Depressive Episode atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjY2ODAyNDU5MjMzNDgw)",
            "[<b>4. Mood Disorders - Manic and Hypomanic Episodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjY3ODA0NDgzNTg4NDA3)",
            "[<b>4. Mood Disorders - Specifiers in Mood Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjY4ODA2NTA3OTQzMzM0)",
            "[<b>4. Mood Disorders - Miscellaneous Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjY5ODA4NTMyMjk4MjYx)",
            "[<b>5. Anxiety Spectrum Disorders - Important Points Mcqs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjcwODEwNTU2NjUzMTg4)",
            "[<b>5. Anxiety Spectrum Disorders - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjcxODEyNTgxMDA4MTE1)",
            "[<b>5. Anxiety Spectrum Disorders - Panic Disorder Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjcyODE0NjA1MzYzMDQy)",
            "[<b>5. Anxiety Spectrum Disorders - Panic Disorder Neurobiology Pani Cogens Differential Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjczODE2NjI5NzE3OTY5)",
            "[<b>5. Anxiety Spectrum Disorders - Separation Anxiety Disorder Selective Mutismaca atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjc0ODE4NjU0MDcyODk2)",
            "[<b>5. Anxiety Spectrum Disorders - Phobia Agoraphobia Social Phobia Specific Phobia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjc1ODIwNjc4NDI3ODIz)",
            "[<b>6. Ocd and Related Disorders - Neurobiology Salient Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjc2ODIyNzAyNzgyNzUw)",
            "[<b>6. Ocd and Related Disorders - Obsessions Compulsions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjc3ODI0NzI3MTM3Njc3)",
            "[<b>6. Ocd and Related Disorders - Ocd Related Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjc4ODI2NzUxNDkyNjA0)",
            "[<b>6. Ocd and Related Disorders - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjc5ODI4Nzc1ODQ3NTMx)",
            "[<b>6. Ocd and Related Disorders - Management of Ocd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjgwODMwODAwMjAyNDU4)",
            "[<b>7. Trauma and Stress Related Disorders - Acute Stress Disorder Post Traumatic Stress Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjgxODMyODI0NTU3Mzg1)",
            "[<b>8. Dissociative Disorders - Derealization Depersonalization Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjgyODM0ODQ4OTEyMzEy)",
            "[<b>8. Dissociative Disorders - Dissociative Amnesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjgzODM2ODczMjY3MjM5)",
            "[<b>8. Dissociative Disorders - Dissociative Identity Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjg0ODM4ODk3NjIyMTY2)",
            "[<b>8. Dissociative Disorders - Introduction Overview atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjg1ODQwOTIxOTc3MDkz)",
            "[<b>8. Dissociative Disorders - Miscellaneous Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjg2ODQyOTQ2MzMyMDIw)",
            "[<b>9. Somatic Symptom and Related Disorders - Dsm v Conditions in Psychosomatic Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjg3ODQ0OTcwNjg2OTQ3)",
            "[<b>9. Somatic Symptom and Related Disorders - Factions Disorder Malingering atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjg4ODQ2OTk1MDQxODc0)",
            "[<b>9. Somatic Symptom and Related Disorders - Dsm Iv Conditions in Psychosomatic Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjg5ODQ5MDE5Mzk2ODAx)",
            "[<b>9. Somatic Symptom and Related Disorders - Functional Neurological Symptom Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjkwODUxMDQzNzUxNzI4)",
            "[<b>9. Somatic Symptom and Related Disorders - Chronic Fatigue Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjkxODUzMDY4MTA2NjU1)",
            "[<b>9. Somatic Symptom and Related Disorders - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjkyODU1MDkyNDYxNTgy)",
            "[<b>10. Feeding and Eating Disorders - Anorexia Nervosa Neuroendocrine Features Examination Findings Rx Prognosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjkzODU3MTE2ODE2NTA5)",
            "[<b>10. Feeding and Eating Disorders - Anorexia Nervosa Diagnosis Severity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjk0ODU5MTQxMTcxNDM2)",
            "[<b>10. Feeding and Eating Disorders - Bulimia Nervosa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjk1ODYxMTY1NTI2MzYz)",
            "[<b>10. Feeding and Eating Disorders - Binge Eating Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjk2ODYzMTg5ODgxMjkw)",
            "[<b>10. Feeding and Eating Disorders - Mcq Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjk3ODY1MjE0MjM2MjE3)",
            "[<b>10. Feeding and Eating Disorders - Overview atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjk4ODY3MjM4NTkxMTQ0)",
            "[<b>10. Feeding and Eating Disorders - Pica Rumination Disorder Arfid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMjk5ODY5MjYyOTQ2MDcx)",
            "[<b>11. Elimination Disorders - Encopresis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzAwODcxMjg3MzAwOTk4)",
            "[<b>11. Elimination Disorders - Enuresis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzAxODczMzExNjU1OTI1)",
            "[<b>11. Elimination Disorders - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzAyODc1MzM2MDEwODUy)",
            "[<b>11. Elimination Disorders - Mcq Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzAzODc3MzYwMzY1Nzc5)",
            "[<b>12. Disorders of Sleep Wake Cycle - Breathing Related to Circadianrrhythm Sleep Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzA0ODc5Mzg0NzIwNzA2)",
            "[<b>12. Disorders of Sleep Wake Cycle - Insomnia Disorder Hypersomnolence Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzA1ODgxNDA5MDc1NjMz)",
            "[<b>12. Disorders of Sleep Wake Cycle - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzA2ODgzNDMzNDMwNTYw)",
            "[<b>12. Disorders of Sleep Wake Cycle - Parasomnias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzA3ODg1NDU3Nzg1NDg3)",
            "[<b>12. Disorders of Sleep Wake Cycle - Narcolepsy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzA4ODg3NDgyMTQwNDE0)",
            "[<b>12. Disorders of Sleep Wake Cycle - Stages of Sleep and Brain Wavesacde atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzA5ODg5NTA2NDk1MzQx)",
            "[<b>13. Gender Dysphoria, Sexual Dysfunction and Paraphilic Disorders - Paraphilic Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzEwODkxNTMwODUwMjY4)",
            "[<b>13. Gender Dysphoria, Sexual Dysfunction and Paraphilic Disorders - Sexual Dysfunction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzExODkzNTU1MjA1MTk1)",
            "[<b>13. Gender Dysphoria, Sexual Dysfunction and Paraphilic Disorders - Gender Dysphoria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzEyODk1NTc5NTYwMTIy)",
            "[<b>14. Disruptive, Impulse Control and Conduct Disorder - Conduct Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzEzODk3NjAzOTE1MDQ5)",
            "[<b>14. Disruptive, Impulse Control and Conduct Disorder - Intermittent Explosive Disorder Pyromania Kleptomania atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzE0ODk5NjI4MjY5OTc2)",
            "[<b>14. Disruptive, Impulse Control and Conduct Disorder - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzE1OTAxNjUyNjI0OTAz)",
            "[<b>14. Disruptive, Impulse Control and Conduct Disorder - Oppositional Defiant Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzE2OTAzNjc2OTc5ODMw)",
            "[<b>15. Substance Related and Addictive Disorders - Alcohol Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzE3OTA1NzAxMzM0NzU3)",
            "[<b>15. Substance Related and Addictive Disorders - Alcohol Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzE4OTA3NzI1Njg5Njg0)",
            "[<b>15. Substance Related and Addictive Disorders - Cannabis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzE5OTA5NzUwMDQ0NjEx)",
            "[<b>15. Substance Related and Addictive Disorders - Caffeine Sedative Hypnotic Inhalants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzIwOTExNzc0Mzk5NTM4)",
            "[<b>15. Substance Related and Addictive Disorders - Hallucinogens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzIxOTEzNzk4NzU0NDY1)",
            "[<b>15. Substance Related and Addictive Disorders - Introduction Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzIyOTE1ODIzMTA5Mzky)",
            "[<b>15. Substance Related and Addictive Disorders - Nicotine Physiology Withdrawal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzIzOTE3ODQ3NDY0MzE5)",
            "[<b>15. Substance Related and Addictive Disorders - Opioids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzI0OTE5ODcxODE5MjQ2)",
            "[<b>15. Substance Related and Addictive Disorders - Introduction Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzI1OTIxODk2MTc0MTcz)",
            "[<b>15. Substance Related and Addictive Disorders - Neurobiology of Addiction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzI2OTIzOTIwNTI5MTAw)",
            "[<b>15. Substance Related and Addictive Disorders - Summary Revision Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzI3OTI1OTQ0ODg0MDI3)",
            "[<b>15. Substance Related and Addictive Disorders - Stimulants Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzI4OTI3OTY5MjM4OTU0)",
            "[<b>15. Substance Related and Addictive Disorders - Stimulants Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzI5OTI5OTkzNTkzODgx)",
            "[<b>15. Substance Related and Addictive Disorders - Transtheoretical Model of Change atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzMwOTMyMDE3OTQ4ODA4)",
            "[<b>15. Substance Related and Addictive Disorders - Stimulants Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzMxOTM0MDQyMzAzNzM1)",
            "[<b>16. Neurocognitive Disorders - Cortical vs Subcortical Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzMyOTM2MDY2NjU4NjYy)",
            "[<b>16. Neurocognitive Disorders - Delirium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzMzOTM4MDkxMDEzNTg5)",
            "[<b>16. Neurocognitive Disorders - Dementia Introductory Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzM0OTQwMTE1MzY4NTE2)",
            "[<b>16. Neurocognitive Disorders - Frontotemporal Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzM1OTQyMTM5NzIzNDQz)",
            "[<b>16. Neurocognitive Disorders - Due to Other Medical Condition Amnesic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzM2OTQ0MTY0MDc4Mzcw)",
            "[<b>16. Neurocognitive Disorders - Delirium vs Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzM3OTQ2MTg4NDMzMjk3)",
            "[<b>16. Neurocognitive Disorders - Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzM4OTQ4MjEyNzg4MjI0)",
            "[<b>16. Neurocognitive Disorders - Alzheimer S Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzM5OTUwMjM3MTQzMTUx)",
            "[<b>16. Neurocognitive Disorders - Lewy Body Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQwOTUyMjYxNDk4MDc4)",
            "[<b>16. Neurocognitive Disorders - Miscellaneous Points Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQxOTU0Mjg1ODUzMDA1)",
            "[<b>16. Neurocognitive Disorders - Vascular Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQyOTU2MzEwMjA3OTMy)",
            "[<b>17. Personality Disorders - Cluster B Borderline Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQzOTU4MzM0NTYyODU5)",
            "[<b>17. Personality Disorders - Cluster B Narcissistic Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQ0OTYwMzU4OTE3Nzg2)",
            "[<b>17. Personality Disorders - Cluster B Histrionic Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQ1OTYyMzgzMjcyNzEz)",
            "[<b>17. Personality Disorders - Cluster B Antisocial Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQ2OTY0NDA3NjI3NjQw)",
            "[<b>17. Personality Disorders - Cluster C Avoidant Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQ3OTY2NDMxOTgyNTY3)",
            "[<b>17. Personality Disorders - Cluster a Schizoid Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQ4OTY4NDU2MzM3NDk0)",
            "[<b>17. Personality Disorders - General Features of Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzQ5OTcwNDgwNjkyNDIx)",
            "[<b>17. Personality Disorders - Cluster C Obsessive Compulsive Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzUwOTcyNTA1MDQ3MzQ4)",
            "[<b>17. Personality Disorders - Cluster C Dependent Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzUxOTc0NTI5NDAyMjc1)",
            "[<b>17. Personality Disorders - Cluster a Schizotypal Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzUyOTc2NTUzNzU3MjAy)",
            "[<b>17. Personality Disorders - Cluster a Paranoid Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzUzOTc4NTc4MTEyMTI5)",
            "[<b>17. Personality Disorders - Miscellaneous Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzU0OTgwNjAyNDY3MDU2)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Antipsychotic Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzU1OTgyNjI2ODIxOTgz)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Antidepressants Important Points atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzU2OTg0NjUxMTc2OTEw)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Extra Pyramidal Side Effects of Antipsychotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzU3OTg2Njc1NTMxODM3)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Mood Disorder Lithium Lamotrigine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzU4OTg4Njk5ODg2NzY0)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Antidepressant Classification Examples atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzU5OTkwNzI0MjQxNjkx)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Opioid Withdrawal Intoxication Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzYwOTkyNzQ4NTk2NjE4)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Mood Disorder Valproate Carbamazepine Cbz  Oxcarbazepine Oxc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzYxOTk0NzcyOTUxNTQ1)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Other Treatment Modalities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzYyOTk2Nzk3MzA2NDcy)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Pharmacotherapy of Alcohol Addiction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzYzOTk4ODIxNjYxMzk5)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Pharmacotherapy of Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzY1MDAwODQ2MDE2MzI2)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Pharmacotherapy of Nicotine Dependence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzY2MDAyODcwMzcxMjUz)",
            "[<b>18. Psychopharmacology and Other Treatment Modalities - Second Generation Third Generation Antipsychotics Sda atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzY3MDA0ODk0NzI2MTgw)",
            "[<b>19. Psychology - Defense Mechanisms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzY4MDA2OTE5MDgxMTA3)",
            "[<b>19. Psychology - Dreams atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzY5MDA4OTQzNDM2MDM0)",
            "[<b>19. Psychology - Psychoanalysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzcwMDEwOTY3NzkwOTYx)",
            "[<b>19. Psychology - Operant Conditioning atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzcxMDEyOTkyMTQ1ODg4)",
            "[<b>19. Psychology - Sigmund Freud atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzcyMDE1MDE2NTAwODE1)",
            "[<b>19. Psychology - Maslow S Hierarchy of Needs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzczMDE3MDQwODU1NzQy)",
            "[<b>19. Psychology - Topographical and Structural Theory of Mind atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzc0MDE5MDY1MjEwNjY5)",
            "[<b>19. Psychology - Stages of Psychosexual Development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzc1MDIxMDg5NTY1NTk2)",
            "[<b>19. Psychology - Erik Erikson Stages of Development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzc2MDIzMTEzOTIwNTIz)",
            "[<b>19. Psychology - Tests of Personality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzc3MDI1MTM4Mjc1NDUw)",
            "[<b>19. Psychology - Jean Piaget S Stages of Cognitive Development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzc4MDI3MTYyNjMwMzc3)",
            "[<b>20. Qrp - Jipmer 2019 Recall Session atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzc5MDI5MTg2OTg1MzA0)",
            "[<b>20. Qrp - Psychiatry by Dr Anoop 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzgwMDMxMjExMzQwMjMx)",
            "[<b>20. Qrp - Psychiatry by Dr Anoop 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzgxMDMzMjM1Njk1MTU4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psychiatryd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psychiatryd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psychiatryd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psychiatryd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("orthopedicsd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Introduction to - Introduction to Orthopaedics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzgyMDM1MjYwMDUwMDg1)",
            "[<b>1. Introduction to - Complications of Fractures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzgzMDM3Mjg0NDA1MDEy)",
            "[<b>2. Peripheral Nerve Injury - Complications of Fractures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzg0MDM5MzA4NzU5OTM5)",
            "[<b>2. Peripheral Nerve Injury - Peripheral Nerve Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzg1MDQxMzMzMTE0ODY2)",
            "[<b>3. Bone Infections - Infections Acute Om Chronic Om Sclerosing Om atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzg2MDQzMzU3NDY5Nzkz)",
            "[<b>3. Bone Infections - Tuberculosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzg3MDQ1MzgxODI0NzIw)",
            "[<b>4. Upper Limb Trauma - Injuries Around Elbow Forearm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzg4MDQ3NDA2MTc5NjQ3)",
            "[<b>4. Upper Limb Trauma - Injuries Around Shoulder Arm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzg5MDQ5NDMwNTM0NTc0)",
            "[<b>5. Tumors - Classification Location Moss atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzkwMDUxNDU0ODg5NTAx)",
            "[<b>5. Tumors - Xrayfandinas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzkxMDUzNDc5MjQ0NDI4)",
            "[<b>5. Parotid Tumors, Surgery and Facial Nerve Landmarks - Parotid Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzkyMDU1NTAzNTk5MzU1)",
            "[<b>6. Pediatric - Hip Abnormality Foor Abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzkzMDU3NTI3OTU0Mjgy)",
            "[<b>6. Pediatric - Regional Genaral atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzk0MDU5NTUyMzA5MjA5)",
            "[<b>7. Metabolic Bone Diseases - Achondroplasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzk1MDYxNTc2NjY0MTM2)",
            "[<b>7. Metabolic Bone Diseases - Ankylosing Spondylitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzk2MDYzNjAxMDE5MDYz)",
            "[<b>7. Metabolic Bone Diseases - Gout Pseudogout atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzk3MDY1NjI1MzczOTkw)",
            "[<b>7. Metabolic Bone Diseases - Neuropathic Joint Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzk4MDY3NjQ5NzI4OTE3)",
            "[<b>7. Metabolic Bone Diseases - Osteomalaciae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzMzk5MDY5Njc0MDgzODQ0)",
            "[<b>7. Metabolic Bone Diseases - Osteoporosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDAwMDcxNjk4NDM4Nzcx)",
            "[<b>7. Metabolic Bone Diseases - Osteopetrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDAxMDczNzIyNzkzNjk4)",
            "[<b>7. Metabolic Bone Diseases - Scurvy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDAyMDc1NzQ3MTQ4NjI1)",
            "[<b>7. Metabolic Bone Diseases - Pagets Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDAzMDc3NzcxNTAzNTUy)",
            "[<b>7. Metabolic Bone Diseases - Vitamin D Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDA0MDc5Nzk1ODU4NDc5)",
            "[<b>7. Metabolic Bone Diseases - Rickets atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDA1MDgxODIwMjEzNDA2)",
            "[<b>7. Metabolic Bone Diseases - Picture Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDA2MDgzODQ0NTY4MzMz)",
            "[<b>8. Lower Limb Trauma - Dislocation of Hip atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDA3MDg1ODY4OTIzMjYw)",
            "[<b>8. Lower Limb Trauma - Eponymous Fractures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDA4MDg3ODkzMjc4MTg3)",
            "[<b>8. Lower Limb Trauma - Fracture Acetabulum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDA5MDg5OTE3NjMzMTE0)",
            "[<b>8. Lower Limb Trauma - Fracture Intertrochanteric Region atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDEwMDkxOTQxOTg4MDQx)",
            "[<b>8. Lower Limb Trauma - Fracture Neck of Femur atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDExMDkzOTY2MzQyOTY4)",
            "[<b>8. Lower Limb Trauma - Fracture Head of Femur atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDEyMDk1OTkwNjk3ODk1)",
            "[<b>8. Lower Limb Trauma - Fractures Pelvis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDEzMDk4MDE1MDUyODIy)",
            "[<b>8. Lower Limb Trauma - Picture Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDE0MTAwMDM5NDA3NzQ5)",
            "[<b>8. Lower Limb Trauma - Soft Tissue Injury in the Knee atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDE1MTAyMDYzNzYyNjc2)",
            "[<b>8. Lower Limb Trauma - Subtrochanteric Fracture atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDE2MTA0MDg4MTE3NjAz)",
            "[<b>9. Examination of Hip - Examination of Hip atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDE3MTA2MTEyNDcyNTMw)",
            "[<b>10. Avascular Necrosis of the Bone - Avascular Necrosis of Bone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDE4MTA4MTM2ODI3NDU3)",
            "[<b>11. Amputations - Amputations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDE5MTEwMTYxMTgyMzg0)",
            "[<b>12. Abnormal Gait - Abnormal Gait atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDIwMTEyMTg1NTM3MzEx)",
            "[<b>13. Spine - Reflexes in Orthopaedic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDIxMTE0MjA5ODkyMjM4)",
            "[<b>13. Spine - Spine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDIyMTE2MjM0MjQ3MTY1)",
            "[<b>14. Qrp - Ini Cet Qrp Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDIzMTE4MjU4NjAyMDky)",
            "[<b>14. Qrp - Orthopaedics by Dr Yusuf Ali Tyagi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDI0MTIwMjgyOTU3MDE5)",
            "[<b>3. Ultrasound - Gynae Ultrasound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDI1MTIyMzA3MzExOTQ2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        orthopedicsd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"orthopedicsd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"orthopedicsd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(orthopedicsd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("radiologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Introduction to - Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDI2MTI0MzMxNjY2ODcz)",
            "[<b>1. Introduction to - Radiation Units atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDI3MTI2MzU2MDIxODAw)",
            "[<b>2. Xray - Mammography and X Ray Views atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDI4MTI4MzgwMzc2NzI3)",
            "[<b>2. Xray - X Ray Physics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDI5MTMwNDA0NzMxNjU0)",
            "[<b>3. Ultrasound - Color Spectral Doppler atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDMwMTMyNDI5MDg2NTgx)",
            "[<b>3. Ultrasound - Fast E Fast atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDMxMTM0NDUzNDQxNTA4)",
            "[<b>3. Ultrasound - Ultrasound Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDMyMTM2NDc3Nzk2NDM1)",
            "[<b>3. Ultrasound - Obstetric Ultrasound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDMzMTM4NTAyMTUxMzYy)",
            "[<b>4. Ct Scan - Ct Scan Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDM0MTQwNTI2NTA2Mjg5)",
            "[<b>4. Ct Scan - Ct Scan Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDM1MTQyNTUwODYxMjE2)",
            "[<b>5. Dental - Dental atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDM2MTQ0NTc1MjE2MTQz)",
            "[<b>6. Contrast Agents - Contrast Agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDM3MTQ2NTk5NTcxMDcw)",
            "[<b>7. Git - Git Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDM4MTQ4NjIzOTI1OTk3)",
            "[<b>7. Git - Git Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDM5MTUwNjQ4MjgwOTI0)",
            "[<b>7. Git - Git Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQwMTUyNjcyNjM1ODUx)",
            "[<b>8. Respiratory - Respiratory Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQxMTU0Njk2OTkwNzc4)",
            "[<b>8. Respiratory - Respiratory Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQyMTU2NzIxMzQ1NzA1)",
            "[<b>9. Angiography - Imaging of Vessels atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQzMTU4NzQ1NzAwNjMy)",
            "[<b>10. Uro- UroPart 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQ0MTYwNzcwMDU1NTU5)",
            "[<b>10. Uro- UroPart 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQ1MTYyNzk0NDEwNDg2)",
            "[<b>11. Pancreatic - Pancreatic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQ2MTY0ODE4NzY1NDEz)",
            "[<b>12. Cardiovascular - Cardiovascular atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQ3MTY2ODQzMTIwMzQw)",
            "[<b>13. Women Imaging - Women Imaging atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQ4MTY4ODY3NDc1MjY3)",
            "[<b>14. Nuclear Medicine - Nuclear Medicine Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDQ5MTcwODkxODMwMTk0)",
            "[<b>14. Nuclear Medicine - Nuclear Medicine Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDUwMTcyOTE2MTg1MTIx)",
            "[<b>14. Nuclear Medicine - Pet Scan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDUxMTc0OTQwNTQwMDQ4)",
            "[<b>15. Magnetic Resonance Imaging - Magnetic Resonance Imaging Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDUyMTc2OTY0ODk0OTc1)",
            "[<b>15. Magnetic Resonance Imaging - Magnetic Resonance Imaging Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDUzMTc4OTg5MjQ5OTAy)",
            "[<b>16. Radiotherapy - Radiotherapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDU0MTgxMDEzNjA0ODI5)",
            "[<b>17. Qrp - Ini Cet Qrp 2021 Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDU1MTgzMDM3OTU5NzU2)",
            "[<b>17. Qrp - Ini Cet Quick Revision Program 2021 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDU2MTg1MDYyMzE0Njgz)",
            "[<b>17. Qrp - by Dr Khaleel Ahmed atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDU3MTg3MDg2NjY5NjEw)",
            "[<b>17. Qrp - Ini Cet Quick Revision Program by Dr Khaleel Ahmed atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDU4MTg5MTExMDI0NTM3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        radiologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"radiologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"radiologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(radiologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("dermatologyd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Basics of - Basics of Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDU5MTkxMTM1Mzc5NDY0)",	
            "[<b>1. Basics of - Basics of Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDYwMTkzMTU5NzM0Mzkx)",	
            "[<b>2. Appendages and Disorders - Appendegeal Disorders Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDYxMTk1MTg0MDg5MzE4)",	
            "[<b>2. Appendages and Disorders - Appendegeal Disorders Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDYyMTk3MjA4NDQ0MjQ1)",	
            "[<b>2. Appendages and Disorders - Appendegeal Disorders Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDYzMTk5MjMyNzk5MTcy)",	
            "[<b>2. Appendages and Disorders - Appendegeal Disorders Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDY0MjAxMjU3MTU0MDk5)",	
            "[<b>3. Bacterial Infections - Bacterial Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDY1MjAzMjgxNTA5MDI2)",	
            "[<b>4. Mycobacterial Infections - Mycobacterial Skin Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDY2MjA1MzA1ODYzOTUz)",	
            "[<b>5. Leprosy - Leprosy Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDY3MjA3MzMwMjE4ODgw)",	
            "[<b>5. Leprosy - Leprosy Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDY4MjA5MzU0NTczODA3)",	
            "[<b>6. Fungal Infections - Fungal Infections Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDY5MjExMzc4OTI4NzM0)",	
            "[<b>6. Fungal Infections - Fungal Infections Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDcwMjEzNDAzMjgzNjYx)",	
            "[<b>7. Viral Infections - Viral Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDcxMjE1NDI3NjM4NTg4)",	
            "[<b>8. Parasitic Infections - Parasitic Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDcyMjE3NDUxOTkzNTE1)",	
            "[<b>9. Examination of Hip - Examination of Hip atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDczMjE5NDc2MzQ4NDQy)",	
            "[<b>9. Sexually Transmitted Diseases - Sexually Transmitted Diseases Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDc0MjIxNTAwNzAzMzY5)",	
            "[<b>9. Sexually Transmitted Diseases - Sexually Transmitted Diseases Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDc1MjIzNTI1MDU4Mjk2)",	
            "[<b>9. Sexually Transmitted Diseases - Sexually Transmitted Diseases Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDc2MjI1NTQ5NDEzMjIz)",	
            "[<b>10. Papulosquamous Disorders - Papulosquamous Disorders Part 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDc3MjI3NTczNzY4MTUw)",	
            "[<b>10. Papulosquamous Disorders - Papulosquamous Disorders Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDc4MjI5NTk4MTIzMDc3)",	
            "[<b>10. Papulosquamous Disorders - Papulosquamous Disorders Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDc5MjMxNjIyNDc4MDA0)",	
            "[<b>11. Vesiculobullous Disorders - Vesiculobullous Disorders Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDgwMjMzNjQ2ODMyOTMx)",	
            "[<b>11. Vesiculobullous Disorders - Vesiculobullous Disorders Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDgxMjM1NjcxMTg3ODU4)",	
            "[<b>12. Pigementation Disorders - Pigmentation Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDgyMjM3Njk1NTQyNzg1)",	
            "[<b>13. Eczema - Eczema Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDgzMjM5NzE5ODk3NzEy)",	
            "[<b>13. Eczema - Eczema Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDg0MjQxNzQ0MjUyNjM5)",	
            "[<b>14. Urticaria and Angiodema - Urticaria Angiodema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDg1MjQzNzY4NjA3NTY2)",	
            "[<b>15. Cutaneous Drug Eruptions - Cutaneous Drug Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDg2MjQ1NzkyOTYyNDkz)",	
            "[<b>15. Cutaneous Drug Eruptions - Drug Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDg3MjQ3ODE3MzE3NDIw)",	
            "[<b>16. Genodermatoses - Genodermatose atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDg4MjQ5ODQxNjcyMzQ3)",	
            "[<b>17. Skin Tumors - Skin Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDg5MjUxODY2MDI3Mjc0)",	
            "[<b>18. Skin and Ctds - Skin in Ctds atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDkwMjUzODkwMzgyMjAx)",	
            "[<b>19. Skin and Systemic Diseases - Skin Systems atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDkxMjU1OTE0NzM3MTI4)",	
            "[<b>20. Short Topics - Short Topics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDkyMjU3OTM5MDkyMDU1)",	
            "[<b>21. Qrp - by Dr Pallavi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDkzMjU5OTYzNDQ2OTgy)",	
            "[<b>21. Qrp - by Dr Pallavi 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDk0MjYxOTg3ODAxOTA5)",	
            "[<b>21. Qrp - Ini Cet Qrp 2021 Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDk1MjY0MDEyMTU2ODM2)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        dermatologyd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"dermatologyd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"dermatologyd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(dermatologyd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("anesthesiad"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. History of Anaesthesia - History Anaesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDk2MjY2MDM2NTExNzYz)",
            "[<b>2. Monitoring - Advanced Monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDk3MjY4MDYwODY2Njkw)",
            "[<b>2. Monitoring - Basic Monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDk4MjcwMDg1MjIxNjE3)",
            "[<b>3. Anaesthesia Machines and Cylinders - Anaesthesia Machines atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNDk5MjcyMTA5NTc2NTQ0)",
            "[<b>3. Anaesthesia Machines and Cylinders - Cylinders and Pipelines atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTAwMjc0MTMzOTMxNDcx)",
            "[<b>4. General Anaesthesia - General Anaesthesia Part B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTAxMjc2MTU4Mjg2Mzk4)",
            "[<b>4. General Anaesthesia - General Anaesthesia Part A atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTAyMjc4MTgyNjQxMzI1)",
            "[<b>5. Cpcr - Complications in or Cpr atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTAzMjgwMjA2OTk2MjUy)",
            "[<b>6. Miscellaneous - Anatomy Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTA0MjgyMjMxMzUxMTc5)",
            "[<b>6. Miscellaneous - Breathing Circuits atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTA1Mjg0MjU1NzA2MTA2)",
            "[<b>7. Regional Anaesthesia - Regional Anaesthesia Part 1 Ivra Blocks Others atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTA2Mjg2MjgwMDYxMDMz)",
            "[<b>7. Regional Anaesthesia - Regional Anaesthesia Part 2 Central Neuraxial Blocks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTA3Mjg4MzA0NDE1OTYw)",
            "[<b>8. Intensive Care Unit - Critical Care Blood Fluids Abg and Ventilators atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTA4MjkwMzI4NzcwODg3)",
            "[<b>9. Complications - Complications Part A atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTA5MjkyMzUzMTI1ODE0)",
            "[<b>10. Pain and Palliative Care - Pain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTEwMjk0Mzc3NDgwNzQx)",
            "[<b>11. Drugs - Intravenous Induction Agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTExMjk2NDAxODM1NjY4)",
            "[<b>11. Drugs - Volatile Induction Agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTEyMjk4NDI2MTkwNTk1)",
            "[<b>11. Drugs - Local Anaesthetic Agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTEzMzAwNDUwNTQ1NTIy)",
            "[<b>11. Drugs - Muscle Relaxants Part B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTE0MzAyNDc0OTAwNDQ5)",
            "[<b>11. Drugs - Muscle Relaxants Part A atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTE1MzA0NDk5MjU1Mzc2)",
            "[<b>12. Airway and Airway Gadgets - O2 Delivery System Hyperbaric and Toxicity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTE2MzA2NTIzNjEwMzAz)",
            "[<b>12. Airway and Airway Gadgets - General Anaesthesia Airway Gadgets atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTE3MzA4NTQ3OTY1MjMw)",
            "[<b>13. Subspeciality - Special Populations Obstetrics Pediatrics and Obesity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTE4MzEwNTcyMzIwMTU3)",
            "[<b>14. Image Based Questions - Image Based Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTE5MzEyNTk2Njc1MDg0)",
            "[<b>15. Qrp - Anaesthesia by Dr Ashish Karthik 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTIwMzE0NjIxMDMwMDEx)",
            "[<b>15. Qrp - Anaesthesia by Dr Ashish Karthik atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTIxMzE2NjQ1Mzg0OTM4)",
            "[<b>15. Qrp - Difficult Airway Gadgets Maintennace of Anaesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTIyMzE4NjY5NzM5ODY1)",
            "[<b>15. Qrp - Icu Abg Ecg Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTIzMzIwNjk0MDk0Nzky)",
            "[<b>15. Qrp - Intubation Endotracheal Tubes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTI0MzIyNzE4NDQ5NzE5)",
            "[<b>15. Qrp - Ini Cet Qrp Mcq S Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTI1MzI0NzQyODA0NjQ2)",
            "[<b>15. Qrp - Ini Cet 2020 Recall Questions Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTI2MzI2NzY3MTU5NTcz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anesthesiad_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anesthesiad_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anesthesiad_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anesthesiad_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data == "damse":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomyde"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistryde")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiologyde"), InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacologyde")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathologyde"), InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiologyde")],
            [InlineKeyboardButton("PSM", callback_data="psmde"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="ophthalmologyde")],
            [InlineKeyboardButton("ENT", callback_data="entde"), InlineKeyboardButton("FMT", callback_data="fmtde")],
            [InlineKeyboardButton("SURGERY", callback_data="surgeryde"), InlineKeyboardButton("MEDICINE", callback_data="medicinede")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="dermatologyde"), InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatryde")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesiade"), InlineKeyboardButton("RADIOLOGY", callback_data="radiologyde")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedicsde"), InlineKeyboardButton("PEDIATRICS", callback_data="pediatricsde")],
            [InlineKeyboardButton("OBGY", callback_data="obgyde"), InlineKeyboardButton("RECENT UPDATES", callback_data="recentupdatesde")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data == "damsh":
        marrow_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="anatomydh"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="biochemistrydh")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="physiologydh"), InlineKeyboardButton("PHARMACOLOGY", callback_data="pharmacologydh")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="pathologydh"), InlineKeyboardButton("MICROBIOLOGY", callback_data="microbiologydh")],
            [InlineKeyboardButton("PSM", callback_data="psmdh"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="ophthalmologydh")],
            [InlineKeyboardButton("ENT", callback_data="entdh"), InlineKeyboardButton("FMT", callback_data="fmtdh")],
            [InlineKeyboardButton("SURGERY", callback_data="surgerydh"), InlineKeyboardButton("MEDICINE", callback_data="medicinedh")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="dermatologydh"), InlineKeyboardButton("PSYCHIATRY", callback_data="psychiatrydh")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="anesthesiadh"), InlineKeyboardButton("RADIOLOGY", callback_data="radiologydh")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="orthopedicsdh"), InlineKeyboardButton("PEDIATRICS", callback_data="pediatricsdh")],
            [InlineKeyboardButton("OBGY", callback_data="obgydh"), InlineKeyboardButton("RECENT UPDATES", callback_data="recentupdatesdh")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(marrow_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("anesthesiade"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Anesthesia machine & breathing circuit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTM4MzUxMDU5NDE4Njk3)",
            "[<b>Cardiopulmonary resuscitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTM5MzUzMDgzNzczNjI0)",
            "[<b>Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQwMzU1MTA4MTI4NTUx)",
            "[<b>1 Thiopentone and ketamine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQxMzU3MTMyNDgzNDc4)",
            "[<b>Anesthesia machine & breathing circuit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQyMzU5MTU2ODM4NDA1)",
            "[<b>Cardiopulmonary resuscitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQzMzYxMTgxMTkzMzMy)",
            "[<b>Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQ0MzYzMjA1NTQ4MjU5)",
            "[<b>1 Thiopentone and ketamine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQ1MzY1MjI5OTAzMTg2)",
            "[<b>2 Propofol and etomidate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQ2MzY3MjU0MjU4MTEz)",
            "[<b>2 Propofol and etomidate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQ3MzY5Mjc4NjEzMDQw)",
            "[<b>1 Inhaled agents basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQ4MzcxMzAyOTY3OTY3)",
            "[<b>1 Inhaled agents basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTQ5MzczMzI3MzIyODk0)",
            "[<b>2 Inhaled agents detailed atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTUwMzc1MzUxNjc3ODIx)",
            "[<b>2 Inhaled agents detailed atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTUxMzc3Mzc2MDMyNzQ4)",
            "[<b>Local anesthetic pharmacology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTUyMzc5NDAwMzg3Njc1)",
            "[<b>Local anesthetic pharmacology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTUzMzgxNDI0NzQyNjAy)",
            "[<b>Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTU0MzgzNDQ5MDk3NTI5)",
            "[<b>1 Monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTU1Mzg1NDczNDUyNDU2)",
            "[<b>Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTU2Mzg3NDk3ODA3Mzgz)",
            "[<b>1 Monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTU3Mzg5NTIyMTYyMzEw)",
            "[<b>1 Scoline atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTU4MzkxNTQ2NTE3MjM3)",
            "[<b>1 Scoline atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTU5MzkzNTcwODcyMTY0)",
            "[<b>2 Ndmr & reversal agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTYwMzk1NTk1MjI3MDkx)",
            "[<b>2 Ndmr & reversal agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTYxMzk3NjE5NTgyMDE4)",
            "[<b>3 Neuromuscular monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTYyMzk5NjQzOTM2OTQ1)",
            "[<b>3 Neuromuscular monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTYzNDAxNjY4MjkxODcy)",
            "[<b>1.Introduction to Anesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTY0NDAzNjkyNjQ2Nzk5)",
            "[<b>1.Introduction to Anesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTY1NDA1NzE3MDAxNzI2)",
            "[<b>2 Preop Assessment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTY2NDA3NzQxMzU2NjUz)",
            "[<b>3 Airway management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTY3NDA5NzY1NzExNTgw)",
            "[<b>2 Preop Assessment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTY4NDExNzkwMDY2NTA3)",
            "[<b>4 Preop preparation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTY5NDEzODE0NDIxNDM0)",
            "[<b>3 Airway management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTcwNDE1ODM4Nzc2MzYx)",
            "[<b>4 Preop preparation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTcxNDE3ODYzMTMxMjg4)",
            "[<b>1 Central neuraxial block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTcyNDE5ODg3NDg2MjE1)",
            "[<b>1 Central neuraxial block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTczNDIxOTExODQxMTQy)",
            "[<b>2 Peripheral nerve blocks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTc0NDIzOTM2MTk2MDY5)",
            "[<b>2 Peripheral nerve blocks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTc1NDI1OTYwNTUwOTk2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anesthesiade_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anesthesiade_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anesthesiade_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anesthesiade_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("anesthesiadh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Anesthesia machine & breathing circuits atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTc2NDI3OTg0OTA1OTIz)",
            "[<b>Cardio pulmonary resusitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTc3NDMwMDA5MjYwODUw)",
            "[<b>Complications in anesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTc4NDMyMDMzNjE1Nzc3)",
            "[<b>1 Thiopentone and ketamine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTc5NDM0MDU3OTcwNzA0)",
            "[<b>2 Propofol & etomidate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTgwNDM2MDgyMzI1NjMx)",
            "[<b>1 Inhaled agents basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTgxNDM4MTA2NjgwNTU4)",
            "[<b>2 Inhaled ganets detailled atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTgyNDQwMTMxMDM1NDg1)",
            "[<b>Local anesthetic pharmacology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTgzNDQyMTU1MzkwNDEy)",
            "[<b>Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTg0NDQ0MTc5NzQ1MzM5)",
            "[<b>Monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTg1NDQ2MjA0MTAwMjY2)",
            "[<b>1 Scoline atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTg2NDQ4MjI4NDU1MTkz)",
            "[<b>2 Ndmr & reversal agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTg3NDUwMjUyODEwMTIw)",
            "[<b>3 Neuromuscular monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTg4NDUyMjc3MTY1MDQ3)",
            "[<b>1 Preoperative assessment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTg5NDU0MzAxNTE5OTc0)",
            "[<b>2 Airway management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTkwNDU2MzI1ODc0OTAx)",
            "[<b>3 Preoperative preparation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTkxNDU4MzUwMjI5ODI4)",
            "[<b>Introduction to Anesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTkyNDYwMzc0NTg0NzU1)",
            "[<b>1 Central neuraxial block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTkzNDYyMzk4OTM5Njgy)",
            "[<b>2 Peripheral nerve blocks atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTk0NDY0NDIzMjk0NjA5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anesthesiadh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anesthesiadh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anesthesiadh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anesthesiadh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("microbiologydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>M leprae, nocardia actinomyces, neisseria Day 20 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTk1NDY2NDQ3NjQ5NTM2)",
            "[<b>Clostridium & listeria Day 18 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTk2NDY4NDcyMDA0NDYz)",
            "[<b>Diphtheria, mycobacteria Day 19 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTk3NDcwNDk2MzU5Mzkw)",
            "[<b>Enterobacteriaceae - E coli Day 23 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTk4NDcyNTIwNzE0MzE3)",
            "[<b>Enterobacteriaceae Day 24 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNTk5NDc0NTQ1MDY5MjQ0)",
            "[<b>Gram Negative Oxidase Positive Aerobes Day 21 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjAwNDc2NTY5NDI0MTcx)",
            "[<b>Leptospira, borellia, rickettsia, chlamydia mycoplasma & other fastidious bacteria Day 26 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjAxNDc4NTkzNzc5MDk4)",
            "[<b>Microaerophilic bacteria, vitrio & haemophilus Day 22 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjAyNDgwNjE4MTM0MDI1)",
            "[<b>Shigella, Proteus, Yersinia & Syphilis Day 25 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjAzNDgyNjQyNDg4OTUy)",
            "[<b>beta hemolytic streptococcus Day 16 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjA0NDg0NjY2ODQzODc5)",
            "[<b>pneumococci, enterococci, bacillus, clostridium tetani Day 17 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjA1NDg2NjkxMTk4ODA2)",
            "[<b>Biosafety & bioterrorism Structure of immune system Day 6 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjA2NDg4NzE1NTUzNzMz)",
            "[<b>General Microbiology - Bacterial morphology Day 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjA3NDkwNzM5OTA4NjYw)",
            "[<b>General Microbiology - Scientists & microscope Day 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjA4NDkyNzY0MjYzNTg3)",
            "[<b>General Microbiology-Physiology of Bacteria Day 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjA5NDk0Nzg4NjE4NTE0)",
            "[<b>General microbiology - bacterial genetics Day 4 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjEwNDk2ODEyOTczNDQx)",
            "[<b>Sterilisation disinfection Biomedical waste management Day 5 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjExNDk4ODM3MzI4MzY4)",
            "[<b>Mycology Day 27 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjEyNTAwODYxNjgzMjk1)",
            "[<b>mycology & virology Day 28 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjEzNTAyODg2MDM4MjIy)",
            "[<b>Helminths Day 36 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjE0NTA0OTEwMzkzMTQ5)",
            "[<b>Parasitology Day 34 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjE1NTA2OTM0NzQ4MDc2)",
            "[<b>Protozoa Day 35 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjE2NTA4OTU5MTAzMDAz)",
            "[<b>DNA Virus Day 29 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjE3NTEwOTgzNDU3OTMw)",
            "[<b>Hepatitis & HIV Day 33 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjE4NTEzMDA3ODEyODU3)",
            "[<b>RNA Virus Day 32 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjE5NTE1MDMyMTY3Nzg0)",
            "[<b>RNA virus Day 30 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjIwNTE3MDU2NTIyNzEx)",
            "[<b>RNA virus Day 31 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjIxNTE5MDgwODc3NjM4)",
            "[<b>immunology - maturation of cells, Antigen Day 7 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjIyNTIxMTA1MjMyNTY1)",
            "[<b>Antibody Day 8 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjIzNTIzMTI5NTg3NDky)",
            "[<b>Antigen processing & presentation, MHC & transplant immunology Day 9 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjI0NTI1MTUzOTQyNDE5)",
            "[<b>B and T cells deficiency autoimmunity Day 12 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjI1NTI3MTc4Mjk3MzQ2)",
            "[<b>Complement system mucosal immunity Day 10 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjI2NTI5MjAyNjUyMjcz)",
            "[<b>Resistance in Scotland aureus & CONS Day 15 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjI3NTMxMjI3MDA3MjAw)",
            "[<b>Serology Day 13 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjI4NTMzMjUxMzYyMTI3)",
            "[<b>Staph Aureus Day 14 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjI5NTM1Mjc1NzE3MDU0)",
            "[<b>hypersensitivity & deficiency of phagocytosis Day 11 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjMwNTM3MzAwMDcxOTgx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        microbiologydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"microbiologydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"microbiologydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(microbiologydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("ophthalmologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Conjuctiva- Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjMxNTM5MzI0NDI2OTA4)",	
            "[<b>1. Conjunctivitis pterygium episcleritis scleritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjMyNTQxMzQ4NzgxODM1)",	
            "[<b>2. Allergic conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjMzNTQzMzczMTM2NzYy)",	
            "[<b>3. Infective conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjM0NTQ1Mzk3NDkxNjg5)",	
            "[<b>4. Cicatricial conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjM1NTQ3NDIxODQ2NjE2)",	
            "[<b>5. Conjunctival degenerations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjM2NTQ5NDQ2MjAxNTQz)",	
            "[<b>6. Conjunctiva MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjM3NTUxNDcwNTU2NDcw)",	
            "[<b>1. Cornea basics keratitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjM4NTUzNDk0OTExMzk3)",	
            "[<b>2. Cornea degeneration dystrophy keratoplasty atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjM5NTU1NTE5MjY2MzI0)",	
            "[<b>3. Cornea Refractive surgeries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQwNTU3NTQzNjIxMjUx)",	
            "[<b>1. Anatomy of cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQxNTU5NTY3OTc2MTc4)",	
            "[<b>2. Physiology of Cornea and applied aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQyNTYxNTkyMzMxMTA1)",	
            "[<b>3. Investigations in cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQzNTYzNjE2Njg2MDMy)",	
            "[<b>4. Corneal ectasiaKeratoconus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQ0NTY1NjQxMDQwOTU5)",	
            "[<b>5. Corneal dystrophies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQ1NTY3NjY1Mzk1ODg2)",	
            "[<b>6. Corneal depositions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQ2NTY5Njg5NzUwODEz)",	
            "[<b>7. Infectious keratitis-Clinical features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQ3NTcxNzE0MTA1NzQw)",	
            "[<b>8. Infectious keratitis-Acanthamoeba and Fungal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQ4NTczNzM4NDYwNjY3)",	
            "[<b>9. Infectious keratitis-Viral and Bacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjQ5NTc1NzYyODE1NTk0)",	
            "[<b>10. Infectious keratitis-Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjUwNTc3Nzg3MTcwNTIx)",	
            "[<b>11. Corneal surgeries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjUxNTc5ODExNTI1NDQ4)",	
            "[<b>12. Sclera and staphylomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjUyNTgxODM1ODgwMzc1)",	
            "[<b>13 Cornea and Sclera MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjUzNTgzODYwMjM1MzAy)",	
            "[<b>1. Embryology of eye atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjU0NTg1ODg0NTkwMjI5)",	
            "[<b>1. Eyelid anatomy and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjU1NTg3OTA4OTQ1MTU2)",	
            "[<b>2. Eyelid embryology and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjU2NTg5OTMzMzAwMDgz)",	
            "[<b>3. Eyelid margin anatomy and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjU3NTkxOTU3NjU1MDEw)",	
            "[<b>4. Levator muscle and clinical aspcts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjU4NTkzOTgyMDA5OTM3)",	
            "[<b>5. Orbicularis muscle and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjU5NTk2MDA2MzY0ODY0)",	
            "[<b>6. Eyelids MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjYwNTk4MDMwNzE5Nzkx)",	
            "[<b>1. Glaucoma Classification tonometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjYxNjAwMDU1MDc0NzE4)",	
            "[<b>2. Gonioscopy ONH changes DO IDO atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjYyNjAyMDc5NDI5NjQ1)",	
            "[<b>3. Perimetry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjYzNjA0MTAzNzg0NTcy)",	
            "[<b>4. PACG,PAOG and Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjY0NjA2MTI4MTM5NDk5)",	
            "[<b>5. Congenital glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjY1NjA4MTUyNDk0NDI2)",	
            "[<b>6. Secondary glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjY2NjEwMTc2ODQ5MzUz)",	
            "[<b>1. Aqueous humour dynamics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjY3NjEyMjAxMjA0Mjgw)",	
            "[<b>2. Glaucoma definition and pathogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjY4NjE0MjI1NTU5MjA3)",	
            "[<b>3. Investigations in glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjY5NjE2MjQ5OTE0MTM0)",	
            "[<b>4. Primary glaucoms Clinical features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjcwNjE4Mjc0MjY5MDYx)",	
            "[<b>5. Primary glaucoma Types and Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjcxNjIwMjk4NjIzOTg4)",	
            "[<b>6. Acute angle closure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjcyNjIyMzIyOTc4OTE1)",	
            "[<b>7. Primary congenital glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjczNjI0MzQ3MzMzODQy)",	
            "[<b>8. Secondary glaucomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjc0NjI2MzcxNjg4NzY5)",	
            "[<b>9.Glaucoma MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjc1NjI4Mzk2MDQzNjk2)",	
            "[<b>Images review atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjc2NjMwNDIwMzk4NjIz)",	
            "[<b>1. Basic Anatomy of eyeball and Orbit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjc3NjMyNDQ0NzUzNTUw)",	
            "[<b>2. Vascular supply of eyeball atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjc4NjM0NDY5MTA4NDc3)",	
            "[<b>3. Embryology of eye atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjc5NjM2NDkzNDYzNDA0)",	
            "[<b>4. Visual Pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjgwNjM4NTE3ODE4MzMx)",	
            "[<b>5. Light reflex pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjgxNjQwNTQyMTczMjU4)",	
            "[<b>7. Basic examination of eyesVision senses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjgyNjQyNTY2NTI4MTg1)",	
            "[<b>8. Basic examination of eyes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjgzNjQ0NTkwODgzMTEy)",	
            "[<b>9. Blindness, Basic Milestones and symptoms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjg0NjQ2NjE1MjM4MDM5)",	
            "[<b>10. Introductio Basic Anatomy, Embryology, Physiology, Investigations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjg1NjQ4NjM5NTkyOTY2)",	
            "[<b>1. Snellens Chart atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjg2NjUwNjYzOTQ3ODkz)",	
            "[<b>2. Etiological classification of cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjg3NjUyNjg4MzAyODIw)",	
            "[<b>3. Clinical features and management of cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjg4NjU0NzEyNjU3NzQ3)",	
            "[<b>4. Complications of cataract surgery paediatric cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjg5NjU2NzM3MDEyNjc0)",	
            "[<b>1. Anatomy and Physiology of lens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjkwNjU4NzYxMzY3NjAx)",	
            "[<b>2. Applied Physiology of lensEtiology and Morphology of cataracts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjkxNjYwNzg1NzIyNTI4)",	
            "[<b>3. Senile cataract Stages and symptoms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjkyNjYyODEwMDc3NDU1)",	
            "[<b>4. Management of senile cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjkzNjY0ODM0NDMyMzgy)",	
            "[<b>5. Management of congenital cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjk0NjY2ODU4Nzg3MzA5)",	
            "[<b>6. Complications of cataract surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjk1NjY4ODgzMTQyMjM2)",	
            "[<b>7. Ectopia lentis and congenital anomalies of lens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjk2NjcwOTA3NDk3MTYz)",	
            "[<b>8.Lens and cataract MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjk3NjcyOTMxODUyMDkw)",	
            "[<b>1. Clinical application of Visual light and near pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjk4Njc0OTU2MjA3MDE3)",	
            "[<b>1. Pupils optic neuritis optic atrophy aion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNjk5Njc2OTgwNTYxOTQ0)",	
            "[<b>2. Clinical application of Visual, light and near pathway Extra poimts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzAwNjc5MDA0OTE2ODcx)",	
            "[<b>2. Papilledema Horners VFDs INO atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzAxNjgxMDI5MjcxNzk4)",	
            "[<b>3. Light-Near dissociation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzAyNjgzMDUzNjI2NzI1)",	
            "[<b>4. Sympathetic pathway Horner syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzAzNjg1MDc3OTgxNjUy)",	
            "[<b>5. Sympathetic pathway Horner syndrome advanced atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzA0Njg3MTAyMzM2NTc5)",	
            "[<b>6. Optic neuritis types and features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzA1Njg5MTI2NjkxNTA2)",	
            "[<b>7. Optic atrophy Types and examples atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzA2NjkxMTUxMDQ2NDMz)",	
            "[<b>8. Supranuclear control of eye movements atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzA3NjkzMTc1NDAxMzYw)",	
            "[<b>9.Neuro-Ophthalmology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzA4Njk1MTk5NzU2Mjg3)",	
            "[<b>Ocular Adenexa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzA5Njk3MjI0MTExMjE0)",	
            "[<b>1. Ocular injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzEwNjk5MjQ4NDY2MTQx)",	
            "[<b>2. Oribal aand Ocular tumours atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzExNzAxMjcyODIxMDY4)",	
            "[<b>3. Ocular injuries and tumours MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzEyNzAzMjk3MTc1OTk1)",	
            "[<b>1. Refractive errors and far point concept atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzEzNzA1MzIxNTMwOTIy)",	
            "[<b>2. Aphakia and correction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzE0NzA3MzQ1ODg1ODQ5)",	
            "[<b>3. Near point concept and Presbyopia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzE1NzA5MzcwMjQwNzc2)",	
            "[<b>4. Astigmatism and clinical applications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzE2NzExMzk0NTk1NzAz)",	
            "[<b>5. Determination of refractive error atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzE3NzEzNDE4OTUwNjMw)",	
            "[<b>6. Questions on refraction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzE4NzE1NDQzMzA1NTU3)",	
            "[<b>7. Pin hole and stenopic slit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzE5NzE3NDY3NjYwNDg0)",	
            "[<b>8. Refarctive surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzIwNzE5NDkyMDE1NDEx)",	
            "[<b>9 Optics MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzIxNzIxNTE2MzcwMzM4)",	
            "[<b>Optics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzIyNzIzNTQwNzI1MjY1)",	
            "[<b>1. Clinical syndromes in orbit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzIzNzI1NTY1MDgwMTky)",	
            "[<b>1. Orbit anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzI0NzI3NTg5NDM1MTE5)",	
            "[<b>2. Orbital apex syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzI1NzI5NjEzNzkwMDQ2)",	
            "[<b>2. Proptosis and types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzI2NzMxNjM4MTQ0OTcz)",	
            "[<b>3. Orbital cellulitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzI3NzMzNjYyNDk5OTAw)",	
            "[<b>3. Thyroid eye disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzI4NzM1Njg2ODU0ODI3)",	
            "[<b>4. Orbital cellulitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzI5NzM3NzExMjA5NzU0)",	
            "[<b>4. Thyroid eye disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzMwNzM5NzM1NTY0Njgx)",	
            "[<b>5. Orbit MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzMxNzQxNzU5OTE5NjA4)",	
            "[<b>Rapid fire MCQ discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzMyNzQzNzg0Mjc0NTM1)",	
            "[<b>1. Retina basics and detachment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzMzNzQ1ODA4NjI5NDYy)",	
            "[<b>2. Diabetic retinopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzM0NzQ3ODMyOTg0Mzg5)",	
            "[<b>3. HTR CRVO CRAO CME CSR atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzM1NzQ5ODU3MzM5MzE2)",	
            "[<b>4. ARMD ROP RP BEST STARG RB atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzM2NzUxODgxNjk0MjQz)",	
            "[<b>1. Structure and Layers of retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzM3NzUzOTA2MDQ5MTcw)",	
            "[<b>2. Vascular supply and barriers of retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzM4NzU1OTMwNDA0MDk3)",	
            "[<b>3. Investigations in Retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzM5NzU3OTU0NzU5MDI0)",	
            "[<b>4. Posterior vitreous detachment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQwNzU5OTc5MTEzOTUx)",	
            "[<b>5. Retinal detachment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQxNzYyMDAzNDY4ODc4)",	
            "[<b>6. Central serous retinopathy and Cystoid macular edema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQyNzY0MDI3ODIzODA1)",	
            "[<b>7. Retinal degenerations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQzNzY2MDUyMTc4NzMy)",	
            "[<b>8. Retinal dystrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQ0NzY4MDc2NTMzNjU5)",	
            "[<b>9. Cone dystrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQ1NzcwMTAwODg4NTg2)",	
            "[<b>10. Choroidal dystrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQ2NzcyMTI1MjQzNTEz)",	
            "[<b>11. Diabetic Retinopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQ3Nzc0MTQ5NTk4NDQw)",	
            "[<b>12. Hypertensive Retinopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQ4Nzc2MTczOTUzMzY3)",	
            "[<b>13. Retinal Vein occlusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzQ5Nzc4MTk4MzA4Mjk0)",	
            "[<b>14. Retinal artery occlusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzUwNzgwMjIyNjYzMjIx)",	
            "[<b>15. Retinopathy of prematurity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzUxNzgyMjQ3MDE4MTQ4)",	
            "[<b>16. Retina and Vitreous MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzUyNzg0MjcxMzczMDc1)",	
            "[<b>1. Extraocular muscles and actions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzUzNzg2Mjk1NzI4MDAy)",	
            "[<b>2. Squint-Definitiona and types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzU0Nzg4MzIwMDgyOTI5)",	
            "[<b>3. Basic tests for squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzU1NzkwMzQ0NDM3ODU2)",	
            "[<b>4. Diplopia and clinical applications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzU2NzkyMzY4NzkyNzgz)",	
            "[<b>5. Examples of paralytic squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzU3Nzk0MzkzMTQ3NzEw)",	
            "[<b>6. Examples of comitant squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzU4Nzk2NDE3NTAyNjM3)",	
            "[<b>7. Management of squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzU5Nzk4NDQxODU3NTY0)",	
            "[<b>8. Tests for Binocularity and Stereopsis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzYwODAwNDY2MjEyNDkx)",	
            "[<b>9. Nystagmus and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzYxODAyNDkwNTY3NDE4)",	
            "[<b>10. Squint MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzYyODA0NTE0OTIyMzQ1)",	
            "[<b>Squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzYzODA2NTM5Mjc3Mjcy)",	
            "[<b>1. Tear film and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzY0ODA4NTYzNjMyMTk5)",	
            "[<b>2. Lacrimal apparatus and tests for watering eyes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzY1ODEwNTg3OTg3MTI2)",	
            "[<b>3. Features of nasolacrimal duct obstruction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzY2ODEyNjEyMzQyMDUz)",	
            "[<b>4. Tear film and Lacrimal apparatus MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzY3ODE0NjM2Njk2OTgw)",	
            "[<b>1. Uveal tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzY4ODE2NjYxMDUxOTA3)",	
            "[<b>2. Uveal tract MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzY5ODE4Njg1NDA2ODM0)",	
            "[<b>1. Anatomy of uvea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzcwODIwNzA5NzYxNzYx)",	
            "[<b>2. Ant Int post fuchs uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzcxODIyNzM0MTE2Njg4)",	
            "[<b>3. Granulomatous non granulomatous uveitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzcyODI0NzU4NDcxNjE1)",	
            "[<b>4. Sympathetic ophthalmitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzczODI2NzgyODI2NTQy)",	
            "[<b>5. Endophthalmitis Panophthalmitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzc0ODI4ODA3MTgxNDY5)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        ophthalmologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ophthalmologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ophthalmologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ophthalmologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("orthopedicsde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Osteomyelitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzc1ODMwODMxNTM2Mzk2)",	
            "[<b>2. Joint Infections (Septic Arthritis, TB Hip and knee) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzc2ODMyODU1ODkxMzIz)",	
            "[<b>1. Biological Fracture Healing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzc3ODM0ODgwMjQ2MjUw)",	
            "[<b>2.Open Fracture atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzc4ODM2OTA0NjAxMTc3)",	
            "[<b>3.Introduction to Bone (Physiology + Biochemistry) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzc5ODM4OTI4OTU2MTA0)",	
            "[<b>4.Trauma around Hip (Fracture Pelvis + Hip Dislocation + Fracture Proximal Femur) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzgwODQwOTUzMzExMDMx)",	
            "[<b>5. Clinical Testing in Orthopaedics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzgxODQyOTc3NjY1OTU4)",	
            "[<b>6. Physeal Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzgyODQ1MDAyMDIwODg1)",	
            "[<b>1. Anatomy of Elbow Joint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzgzODQ3MDI2Mzc1ODEy)",	
            "[<b>2. Supracondylar Fracture Humerus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzg0ODQ5MDUwNzMwNzM5)",	
            "[<b>3.Fracture Lateral Condyle Humerus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzg1ODUxMDc1MDg1NjY2)",	
            "[<b>Fracture of the Forearm,wrist and Hand atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzg2ODUzMDk5NDQwNTkz)",	
            "[<b>1. Anatomy of Hip Joint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzg3ODU1MTIzNzk1NTIw)",	
            "[<b>2. Pediatric Hip Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzg4ODU3MTQ4MTUwNDQ3)",	
            "[<b>1. Implants And Instruments atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzg5ODU5MTcyNTA1Mzc0)",	
            "[<b>2. Splints atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzkwODYxMTk2ODYwMzAx)",	
            "[<b>1. Basics of Knee Ligaments atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzkxODYzMjIxMjE1MjI4)",	
            "[<b>2. Meniscal & Collateral Ligament Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzkyODY1MjQ1NTcwMTU1)",	
            "[<b>3.Cruciate Ligament Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzkzODY3MjY5OTI1MDgy)",	
            "[<b>4. Osteoarthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzk0ODY5Mjk0MjgwMDA5)",	
            "[<b>5. MCQ Practise Knee atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzk1ODcxMzE4NjM0OTM2)",	
            "[<b>1. Basic Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzk2ODczMzQyOTg5ODYz)",	
            "[<b>2. CTEV Club Foot atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzk3ODc1MzY3MzQ0Nzkw)",	
            "[<b>3. Lower Limb Fractures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzk4ODc3MzkxNjk5NzE3)",	
            "[<b>1. Osteogenesis Imperfecta atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzNzk5ODc5NDE2MDU0NjQ0)",	
            "[<b>2. Osteopetrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODAwODgxNDQwNDA5NTcx)",	
            "[<b>3. Pagets Disease of Bone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODAxODgzNDY0NzY0NDk4)",	
            "[<b>4. Approach to Osteoporosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODAyODg1NDg5MTE5NDI1)",	
            "[<b>5. MCQ Practice of Metabolic Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODAzODg3NTEzNDc0MzUy)",	
            "[<b>Miscellaenous 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODA0ODg5NTM3ODI5Mjc5)",	
            "[<b>1.Chondroblastoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODA1ODkxNTYyMTg0MjA2)",	
            "[<b>2. Osteochondroma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODA2ODkzNTg2NTM5MTMz)",	
            "[<b>3. Osteoid Osteoma and Osteoblastoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODA3ODk1NjEwODk0MDYw)",	
            "[<b>4. Osteosarcoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODA4ODk3NjM1MjQ4OTg3)",	
            "[<b>5.GCT & ABC atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODA5ODk5NjU5NjAzOTE0)",	
            "[<b>6.Enchondma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODEwOTAxNjgzOTU4ODQx)",	
            "[<b>7.Tubercular Dactylitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODExOTAzNzA4MzEzNzY4)",	
            "[<b>8.Ewing's Sarcoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODEyOTA1NzMyNjY4Njk1)",	
            "[<b>9. Mirel's Score atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODEzOTA3NzU3MDIzNjIy)",	
            "[<b>1. Anatomy of Shoulder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODE0OTA5NzgxMzc4NTQ5)",	
            "[<b>2.Rotator Cuff Tear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODE1OTExODA1NzMzNDc2)",	
            "[<b>3. Shoulder Dislocation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODE2OTEzODMwMDg4NDAz)",	
            "[<b>4.Recurrent Shoulder Dislocation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODE3OTE1ODU0NDQzMzMw)",	
            "[<b>MCQ Practice Shoulder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODE4OTE3ODc4Nzk4MjU3)",	
            "[<b>1. Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODE5OTE5OTAzMTUzMTg0)",	
            "[<b>2. One Liners atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODIwOTIxOTI3NTA4MTEx)",	
            "[<b>3. Terms used in Spine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODIxOTIzOTUxODYzMDM4)",	
            "[<b>4. Spinal Fractures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODIyOTI1OTc2MjE3OTY1)",	
            "[<b>5. Spinal Cord injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODIzOTI4MDAwNTcyODky)",	
            "[<b>6. Klippel Fiel Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODI0OTMwMDI0OTI3ODE5)",	
            "[<b>7. Congenital muscular torticolis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODI1OTMyMDQ5MjgyNzQ2)",	
            "[<b>8.Idiopathic Adoloscent Scoliosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODI2OTM0MDczNjM3Njcz)",	
            "[<b>9.Entrapment Neuropathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODI3OTM2MDk3OTkyNjAw)",	
            "[<b>10.Peripheral Nerve Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODI4OTM4MTIyMzQ3NTI3)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        orthopedicsde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"orthopedicsde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"orthopedicsde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(orthopedicsde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("obgyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>17. APH atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODI5OTQwMTQ2NzAyNDU0)",
            "[<b>12. Amniotic fluid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODMwOTQyMTcxMDU3Mzgx)",
            "[<b>11. Anemia in Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODMxOTQ0MTk1NDEyMzA4)",
            "[<b>1.Applied Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODMyOTQ2MjE5NzY3MjM1)",
            "[<b>2.Applied Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODMzOTQ4MjQ0MTIyMTYy)",
            "[<b>Combined estrogen progesterone contraceptives atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODM0OTUwMjY4NDc3MDg5)",
            "[<b>LARC and progesterone only methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODM1OTUyMjkyODMyMDE2)",
            "[<b>Sterilization technique atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODM2OTU0MzE3MTg2OTQz)",
            "[<b>14. Diabetes in pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODM3OTU2MzQxNTQxODcw)",
            "[<b>4.Diagnosis of pregnancy and physiological changes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODM4OTU4MzY1ODk2Nzk3)",
            "[<b>6. Down Syndrome Screening atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODM5OTYwMzkwMjUxNzI0)",
            "[<b>7. Ectopic Pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQwOTYyNDE0NjA2NjUx)",
            "[<b>11. Endometrial Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQxOTY0NDM4OTYxNTc4)",
            "[<b>12. Endometriosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQyOTY2NDYzMzE2NTA1)",
            "[<b>23. Fetal Monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQzOTY4NDg3NjcxNDMy)",
            "[<b>13. Fibroid and Adenomyosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQ0OTcwNTEyMDI2MzU5)",
            "[<b>5. First Antenatal Visit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQ1OTcyNTM2MzgxMjg2)",
            "[<b>21. Heart diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQ2OTc0NTYwNzM2MjEz)",
            "[<b>22. IOL and CS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQ3OTc2NTg1MDkxMTQw)",
            "[<b>16. IUGR atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQ4OTc4NjA5NDQ2MDY3)",
            "[<b>9. Induced Abortions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODQ5OTgwNjMzODAwOTk0)",
            "[<b>8.Infertility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODUwOTgyNjU4MTU1OTIx)",
            "[<b>5.Menopause atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODUxOTg0NjgyNTEwODQ4)",
            "[<b>10. Molar Pregnancy and GTN atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODUyOTg2NzA2ODY1Nzc1)",
            "[<b>25. Normal labour and maternal pelvis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODUzOTg4NzMxMjIwNzAy)",
            "[<b>1.Reproductive Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODU0OTkwNzU1NTc1NjI5)",
            "[<b>10. Ovarian Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODU1OTkyNzc5OTMwNTU2)",
            "[<b>7.PCOS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODU2OTk0ODA0Mjg1NDgz)",
            "[<b>24. PPH atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODU3OTk2ODI4NjQwNDEw)",
            "[<b>19. PROM Premature Rupture of Membranes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODU4OTk4ODUyOTk1MzM3)",
            "[<b>26. Partograph malpresentation and instrumental delivery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODYwMDAwODc3MzUwMjY0)",
            "[<b>3.Placenta atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODYxMDAyOTAxNzA1MTkx)",
            "[<b>9.Pre Invasive and Invasive lesion of Cervix atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODYyMDA0OTI2MDYwMTE4)",
            "[<b>13. Preeclampsia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODYzMDA2OTUwNDE1MDQ1)",
            "[<b>18. Preterm Labour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODY0MDA4OTc0NzY5OTcy)",
            "[<b>6.Primary and secondary amenorrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODY1MDEwOTk5MTI0ODk5)",
            "[<b>14. Prolapse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODY2MDEzMDIzNDc5ODI2)",
            "[<b>4.Puberty atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODY3MDE1MDQ3ODM0NzUz)",
            "[<b>3.Reproductive physiology and menstrual cycle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODY4MDE3MDcyMTg5Njgw)",
            "[<b>15. Rh negative atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODY5MDE5MDk2NTQ0NjA3)",
            "[<b>15. SUI, PID and Vaginal infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODcwMDIxMTIwODk5NTM0)",
            "[<b>8. Spontaneous Abortion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODcxMDIzMTQ1MjU0NDYx)",
            "[<b>2.Teratogens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODcyMDI1MTY5NjA5Mzg4)",
            "[<b>20.Twin pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODczMDI3MTkzOTY0MzE1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        obgyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"obgyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"obgyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(obgyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("obgydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>3.1. ANC and USG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODc0MDI5MjE4MzE5MjQy)",
            "[<b>3.2. trisomy screenings and confirmations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODc1MDMxMjQyNjc0MTY5)",
            "[<b>1.1 Anatomyexternal genitalia. atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODc2MDMzMjY3MDI5MDk2)",
            "[<b>1.2.Anatomy internal genitalia. atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODc3MDM1MjkxMzg0MDIz)",
            "[<b>1.3.oogenesis fertilisation and implantation. atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODc4MDM3MzE1NzM4OTUw)",
            "[<b>1.4. placenta and disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODc5MDM5MzQwMDkzODc3)",
            "[<b>1.5. amniotic fluid and disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODgwMDQxMzY0NDQ4ODA0)",
            "[<b>2.1.early pregnancy evaluation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODgxMDQzMzg4ODAzNzMx)",
            "[<b>2.2.ectopic pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODgyMDQ1NDEzMTU4NjU4)",
            "[<b>2.3. abortions and mtp act atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODgzMDQ3NDM3NTEzNTg1)",
            "[<b>2.4. Recurrent pregnancy losses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODg0MDQ5NDYxODY4NTEy)",
            "[<b>2.5. GTD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODg1MDUxNDg2MjIzNDM5)",
            "[<b>4. FETAL CARE atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODg2MDUzNTEwNTc4MzY2)",
            "[<b>1.1 Development and Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODg3MDU1NTM0OTMzMjkz)",
            "[<b>1.2.Mullerian Anomalies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODg4MDU3NTU5Mjg4MjIw)",
            "[<b>4.1.Amenorrhoea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODg5MDU5NTgzNjQzMTQ3)",
            "[<b>4.2.Menopause and HRT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODkwMDYxNjA3OTk4MDc0)",
            "[<b>4.3.Puberty and Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODkxMDYzNjMyMzUzMDAx)",
            "[<b>4.4.PCOS and Hirsutism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODkyMDY1NjU2NzA3OTI4)",
            "[<b>4.5. Infertility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODkzMDY3NjgxMDYyODU1)",
            "[<b>2.1.Pid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODk0MDY5NzA1NDE3Nzgy)",
            "[<b>2.2.Genital TB atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODk1MDcxNzI5NzcyNzA5)",
            "[<b>2.3.Vulvo Vaginal Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODk2MDczNzU0MTI3NjM2)",
            "[<b>7.1 power, passenger, passager atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODk3MDc1Nzc4NDgyNTYz)",
            "[<b>7.2 normal and abnormal labour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODk4MDc3ODAyODM3NDkw)",
            "[<b>7.3 Partogram atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzODk5MDc5ODI3MTkyNDE3)",
            "[<b>7.4 Intrapartum fetal monitoring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTAwMDgxODUxNTQ3MzQ0)",
            "[<b>7.5 Morbidly adherent placventa and uterine inversion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTAxMDgzODc1OTAyMjcx)",
            "[<b>7.6 malpositions and malpresentations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTAyMDg1OTAwMjU3MTk4)",
            "[<b>7.7 operative vaginal delivery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTAzMDg3OTI0NjEyMTI1)",
            "[<b>6.1 skin and IHCP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTA0MDg5OTQ4OTY3MDUy)",
            "[<b>6.2 Hematological changes and anemia in pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTA1MDkxOTczMzIxOTc5)",
            "[<b>6.3 Metabolic system, thyroid dysfunction and diabetes in pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTA2MDkzOTk3Njc2OTA2)",
            "[<b>6.4 Cardiorespiratory Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTA3MDk2MDIyMDMxODMz)",
            "[<b>6.5 heart diseases in pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTA4MDk4MDQ2Mzg2NzYw)",
            "[<b>6.6 Genitourinary and gastrointestinal physio and patho atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTA5MTAwMDcwNzQxNjg3)",
            "[<b>3.1.Fibroids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTEwMTAyMDk1MDk2NjE0)",
            "[<b>3.2.Adenomyosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTExMTA0MTE5NDUxNTQx)",
            "[<b>3.3.Endometriosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTEyMTA2MTQzODA2NDY4)",
            "[<b>3.4.Dysmenorrhoea and PMS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTEzMTA4MTY4MTYxMzk1)",
            "[<b>3.5.Abnormal Uterine Bleeding atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTE0MTEwMTkyNTE2MzIy)",
            "[<b>9. Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTE1MTEyMjE2ODcxMjQ5)",
            "[<b>5.1. multifetal pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTE2MTE0MjQxMjI2MTc2)",
            "[<b>5.2 APH atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTE3MTE2MjY1NTgxMTAz)",
            "[<b>5.3 Rh NEGATIVE PREGNANCY atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTE4MTE4Mjg5OTM2MDMw)",
            "[<b>5.4 Hypertension in pregnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTE5MTIwMzE0MjkwOTU3)",
            "[<b>5.5 Previous cesarean section atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTIwMTIyMzM4NjQ1ODg0)",
            "[<b>5.6 PRETERM LABOUR, PROM, PPROM atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTIxMTI0MzYzMDAwODEx)",
            "[<b>5.7 FETAL GROWTH RESTRICTION atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTIyMTI2Mzg3MzU1NzM4)",
            "[<b>5.8 IUFD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTIzMTI4NDExNzEwNjY1)",
            "[<b>6.1.Uterus Oncology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTI0MTMwNDM2MDY1NTky)",
            "[<b>6.2.Cervical Premalignancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTI1MTMyNDYwNDIwNTE5)",
            "[<b>6.3. Cervical Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTI2MTM0NDg0Nzc1NDQ2)",
            "[<b>6.4. Ovarian Tumours atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTI3MTM2NTA5MTMwMzcz)",
            "[<b>6.5.Vulval Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTI4MTM4NTMzNDg1MzAw)",
            "[<b>8.1 post partum care including puerperal sepsis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTI5MTQwNTU3ODQwMjI3)",
            "[<b>8.2 PPH atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTMwMTQyNTgyMTk1MTU0)",
            "[<b>5.1.POP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTMxMTQ0NjA2NTUwMDgx)",
            "[<b>5.2.Incontinence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTMyMTQ2NjMwOTA1MDA4)",
            "[<b>5.3.Genito Urinary Fistula atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTMzMTQ4NjU1MjU5OTM1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        obgydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"obgydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"obgydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(obgydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("medicinede"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. ABB defects in renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTM0MTUwNjc5NjE0ODYy)",	
            "[<b>2.Hormonal defects in renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTM1MTUyNzAzOTY5Nzg5)",	
            "[<b>1.ABB Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTM2MTU0NzI4MzI0NzE2)",	
            "[<b>2.Respiratory ABB Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTM3MTU2NzUyNjc5NjQz)",	
            "[<b>3.Metabolic ABB Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTM4MTU4Nzc3MDM0NTcw)",	
            "[<b>4. Renal Tubular Acidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTM5MTYwODAxMzg5NDk3)",	
            "[<b>5. Inherited channelopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQwMTYyODI1NzQ0NDI0)",	
            "[<b>6.Classification of RS disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQxMTY0ODUwMDk5MzUx)",	
            "[<b>13.ABG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQyMTY2ODc0NDU0Mjc4)",	
            "[<b>ABG extra edge and Lung cancer staging by Dr Bharat Kathi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQzMTY4ODk4ODA5MjA1)",	
            "[<b>4.ACTH atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQ0MTcwOTIzMTY0MTMy)",	
            "[<b>1.Definition of AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQ1MTcyOTQ3NTE5MDU5)",	
            "[<b>2.Stages of AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQ2MTc0OTcxODczOTg2)",	
            "[<b>3.Difference Between Pre Renal and Intrinsic AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQ3MTc2OTk2MjI4OTEz)",	
            "[<b>4.Causes of pre renal AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQ4MTc5MDIwNTgzODQw)",	
            "[<b>5.Treatment of Prerenal AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTQ5MTgxMDQ0OTM4NzY3)",	
            "[<b>6.Causes and Managment of Intrinsic AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTUwMTgzMDY5MjkzNjk0)",	
            "[<b>7.Acute kidney injury MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTUxMTg1MDkzNjQ4NjIx)",	
            "[<b>5.Adrenal Gland atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTUyMTg3MTE4MDAzNTQ4)",	
            "[<b>3.1.Apex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTUzMTg5MTQyMzU4NDc1)",	
            "[<b>3.2 Apex MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTU0MTkxMTY2NzEzNDAy)",	
            "[<b>1.Approach to Jaundice atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTU1MTkzMTkxMDY4MzI5)",	
            "[<b>1. Approach to Renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTU2MTk1MjE1NDIzMjU2)",	
            "[<b>2.Approach to AKI and management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTU3MTk3MjM5Nzc4MTgz)",	
            "[<b>1. Approach to Arthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTU4MTk5MjY0MTMzMTEw)",	
            "[<b>2.Inflammatory Pauciarthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTU5MjAxMjg4NDg4MDM3)",	
            "[<b>3. Inflammatory Polyarthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTYwMjAzMzEyODQyOTY0)",	
            "[<b>1.Assessment methods in Nephrology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTYxMjA1MzM3MTk3ODkx)",	
            "[<b>1.Assesments methods PFT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTYyMjA3MzYxNTUyODE4)",	
            "[<b>2.ABG Analysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTYzMjA5Mzg1OTA3NzQ1)",	
            "[<b>3.Gas Exchange Defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTY0MjExNDEwMjYyNjcy)",	
            "[<b>1.Autoimmune Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTY1MjEzNDM0NjE3NTk5)",	
            "[<b>2.Primary Biliary Cholangitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTY2MjE1NDU4OTcyNTI2)",	
            "[<b>9.Brainstem disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTY3MjE3NDgzMzI3NDUz)",	
            "[<b>1.CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTY4MjE5NTA3NjgyMzgw)",	
            "[<b>2.DM nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTY5MjIxNTMyMDM3MzA3)",	
            "[<b>3. Inherited causes of CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTcwMjIzNTU2MzkyMjM0)",	
            "[<b>4. Renal Replacement therapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTcxMjI1NTgwNzQ3MTYx)",	
            "[<b>1.Seizure diorder Clinical types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTcyMjI3NjA1MTAyMDg4)",	
            "[<b>2.Seizure disorder -Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTczMjI5NjI5NDU3MDE1)",	
            "[<b>10.CNS Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTc0MjMxNjUzODExOTQy)",	
            "[<b>1.1.Pulse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTc1MjMzNjc4MTY2ODY5)",	
            "[<b>1.2 Pulse MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTc2MjM1NzAyNTIxNzk2)",	
            "[<b>1.Approach to Medicine & Introduction to Cardiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTc3MjM3NzI2ODc2NzIz)",	
            "[<b>2.Approach to Breathlessness atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTc4MjM5NzUxMjMxNjUw)",	
            "[<b>3.Approach to Chest pain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTc5MjQxNzc1NTg2NTc3)",	
            "[<b>4. Approach to Palpitations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTgwMjQzNzk5OTQxNTA0)",	
            "[<b>5. Approach to Syncope atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTgxMjQ1ODI0Mjk2NDMx)",	
            "[<b>6.Approach to Edema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTgyMjQ3ODQ4NjUxMzU4)",	
            "[<b>1. Cardiomyopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTgzMjQ5ODczMDA2Mjg1)",	
            "[<b>1.Cortical functions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTg0MjUxODk3MzYxMjEy)",	
            "[<b>2.Aphasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTg1MjUzOTIxNzE2MTM5)",	
            "[<b>3.Ischemic stroke localization atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTg2MjU1OTQ2MDcxMDY2)",	
            "[<b>4.Etiology of treatment ischemic stroke atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTg3MjU3OTcwNDI1OTkz)",	
            "[<b>5.Hemorrhagic cva atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTg4MjU5OTk0NzgwOTIw)",	
            "[<b>1.Definition of CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTg5MjYyMDE5MTM1ODQ3)",	
            "[<b>2. Stages of CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTkwMjY0MDQzNDkwNzc0)",	
            "[<b>3.Causes of CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTkxMjY2MDY3ODQ1NzAx)",	
            "[<b>4.Complications of CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTkyMjY4MDkyMjAwNjI4)",	
            "[<b>5.Hyperkalemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTkzMjcwMTE2NTU1NTU1)",	
            "[<b>6.Hypokalemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTk0MjcyMTQwOTEwNDgy)",	
            "[<b>7.Hyponatremia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTk1Mjc0MTY1MjY1NDA5)",	
            "[<b>8.Hypocalcemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTk2Mjc2MTg5NjIwMzM2)",	
            "[<b>9.Hyperphosphotemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTk3Mjc4MjEzOTc1MjYz)",	
            "[<b>10.Dialysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTk4MjgwMjM4MzMwMTkw)",	
            "[<b>11.Chronic kidney Diseases MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTEzOTk5MjgyMjYyNjg1MTE3)",	
            "[<b>1. Assessment and approach to Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDAwMjg0Mjg3MDQwMDQ0)",	
            "[<b>2.Arterial pulse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDAxMjg2MzExMzk0OTcx)",	
            "[<b>3.JVP examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDAyMjg4MzM1NzQ5ODk4)",	
            "[<b>4. Pulsus Paradoxus and Kussmauls sign atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDAzMjkwMzYwMTA0ODI1)",	
            "[<b>5. Heart sounds atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDA0MjkyMzg0NDU5NzUy)",	
            "[<b>6. Cardiac murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDA1Mjk0NDA4ODE0Njc5)",	
            "[<b>1.Ascites atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDA2Mjk2NDMzMTY5NjA2)",	
            "[<b>2.Portal Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDA3Mjk4NDU3NTI0NTMz)",	
            "[<b>3.Hepatic Encephalopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDA4MzAwNDgxODc5NDYw)",	
            "[<b>4.Hepato-Pulmonary Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDA5MzAyNTA2MjM0Mzg3)",	
            "[<b>5.Spontaneous Bacterial Peritonitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDEwMzA0NTMwNTg5MzE0)",	
            "[<b>6.Hepatio- Renal Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDExMzA2NTU0OTQ0MjQx)",	
            "[<b>1.Clinical Feature of CAD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDEyMzA4NTc5Mjk5MTY4)",	
            "[<b>2.ECG and Cardiac Markers in CAD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDEzMzEwNjAzNjU0MDk1)",	
            "[<b>3.Management of CAD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDE0MzEyNjI4MDA5MDIy)",	
            "[<b>11.4 Coronary Artery Diseases MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDE1MzE0NjUyMzYzOTQ5)",	
            "[<b>1.Alzheimer disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDE2MzE2Njc2NzE4ODc2)",	
            "[<b>2.Huntington disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDE3MzE4NzAxMDczODAz)",	
            "[<b>3.Normal pressure hydrocephalus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDE4MzIwNzI1NDI4NzMw)",	
            "[<b>4.Prion diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDE5MzIyNzQ5NzgzNjU3)",	
            "[<b>5.Wernicke encephalopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDIwMzI0Nzc0MTM4NTg0)",	
            "[<b>8.Diabetes and Hypoglycemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDIxMzI2Nzk4NDkzNTEx)",	
            "[<b>D8. Diabetes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDIyMzI4ODIyODQ4NDM4)",	
            "[<b>1.Diarrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDIzMzMwODQ3MjAzMzY1)",	
            "[<b>12.1.Electrophysiological Events & ECG Manifestation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDI0MzMyODcxNTU4Mjky)",	
            "[<b>12.2.ECG Paper & Heart rate Calculation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDI1MzM0ODk1OTEzMjE5)",	
            "[<b>12.3.Principle of ECG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDI2MzM2OTIwMjY4MTQ2)",	
            "[<b>12.4.Bipolar limb leads atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDI3MzM4OTQ0NjIzMDcz)",	
            "[<b>12.5.Unipolar limb leads atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDI4MzQwOTY4OTc4MDAw)",	
            "[<b>12.6.Chest leads atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDI5MzQyOTkzMzMyOTI3)",	
            "[<b>12.7.Normal & Abnormal P wave atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDMwMzQ1MDE3Njg3ODU0)",	
            "[<b>12.8.PR Interval atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDMxMzQ3MDQyMDQyNzgx)",	
            "[<b>12.9. QRS Complex width atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDMyMzQ5MDY2Mzk3NzA4)",	
            "[<b>12.10.QRS Normal & Abnormal Morphology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDMzMzUxMDkwNzUyNjM1)",	
            "[<b>12.11. QRS Axis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDM0MzUzMTE1MTA3NTYy)",	
            "[<b>12.12.J wave,ST segment,T wave & QT Interval atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDM1MzU1MTM5NDYyNDg5)",	
            "[<b>12.13.Sinus Bradycardia & Sinus arrest atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDM2MzU3MTYzODE3NDE2)",	
            "[<b>12.14.AV block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDM3MzU5MTg4MTcyMzQz)",	
            "[<b>12.15.Sinus Tachycardia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDM4MzYxMjEyNTI3Mjcw)",	
            "[<b>12.16.Atrial Tachycardia,Flutter & Fibrillation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDM5MzYzMjM2ODgyMTk3)",	
            "[<b>12.18.Ventricular Tachyarrythmia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQwMzY1MjYxMjM3MTI0)",	
            "[<b>12.19 ECG MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQxMzY3Mjg1NTkyMDUx)",	
            "[<b>12.17.PSVT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQyMzY5MzA5OTQ2OTc4)",	
            "[<b>1. ECG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQzMzcxMzM0MzAxOTA1)",	
            "[<b>2. Introduction to arrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQ0MzczMzU4NjU2ODMy)",	
            "[<b>3. Heart block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQ1Mzc1MzgzMDExNzU5)",	
            "[<b>4. Approach to Tachyarrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQ2Mzc3NDA3MzY2Njg2)",	
            "[<b>5. Supraventricular arrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQ3Mzc5NDMxNzIxNjEz)",	
            "[<b>7.Ventricular Tachyarrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQ4MzgxNDU2MDc2NTQw)",	
            "[<b>1.Echocardiography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDQ5MzgzNDgwNDMxNDY3)",	
            "[<b>2.Pericardial disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDUwMzg1NTA0Nzg2Mzk0)",	
            "[<b>6.1.1.Aortic Stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDUxMzg3NTI5MTQxMzIx)",	
            "[<b>6.1.2.Mitral Stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDUyMzg5NTUzNDk2MjQ4)",	
            "[<b>6.1.3.Aortic Regurgitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDUzMzkxNTc3ODUxMTc1)",	
            "[<b>6.1.4.Mitral Regurgitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDU0MzkzNjAyMjA2MTAy)",	
            "[<b>6.1.5. Mitral Valve Prolapse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDU1Mzk1NjI2NTYxMDI5)",	
            "[<b>6.1.6.TS,TR,PS,PR atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDU2Mzk3NjUwOTE1OTU2)",	
            "[<b>6.1.7. Valvular Diseases MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDU3Mzk5Njc1MjcwODgz)",	
            "[<b>6.2.1.Infective Endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDU4NDAxNjk5NjI1ODEw)",	
            "[<b>6.2.2. Infective Endocarditis MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDU5NDAzNzIzOTgwNzM3)",	
            "[<b>6.3.1. Acute Rheumatic Fever atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDYwNDA1NzQ4MzM1NjY0)",	
            "[<b>6.3.2. Acute Rheumatic Fever MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDYxNDA3NzcyNjkwNTkx)",	
            "[<b>1.Introduction to Endocrinology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDYyNDA5Nzk3MDQ1NTE4)",	
            "[<b>1.Alcohol Liver Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDYzNDExODIxNDAwNDQ1)",	
            "[<b>2.Non-Alcoholic Fatty Liver Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDY0NDEzODQ1NzU1Mzcy)",	
            "[<b>1.Disorders of Bilirubin Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDY1NDE1ODcwMTEwMjk5)",	
            "[<b>2.Liver Enzyme atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDY2NDE3ODk0NDY1MjI2)",	
            "[<b>12.Gullian Barre Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDY3NDE5OTE4ODIwMTUz)",	
            "[<b>1.Introduction to Gastroenterology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDY4NDIxOTQzMTc1MDgw)",	
            "[<b>2.Malabsorption atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDY5NDIzOTY3NTMwMDA3)",	
            "[<b>3.Malabsorption Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDcwNDI1OTkxODg0OTM0)",	
            "[<b>4.Inflammatory bowel diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDcxNDI4MDE2MjM5ODYx)",	
            "[<b>5. Irritable Bowel Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDcyNDMwMDQwNTk0Nzg4)",	
            "[<b>6.Diarrhea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDczNDMyMDY0OTQ5NzE1)",	
            "[<b>7. Peptic Ulcer Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDc0NDM0MDg5MzA0NjQy)",	
            "[<b>1.Wilson Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDc1NDM2MTEzNjU5NTY5)",	
            "[<b>2.Hemochromatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDc2NDM4MTM4MDE0NDk2)",	
            "[<b>1.Basics of Glomerular Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDc3NDQwMTYyMzY5NDIz)",	
            "[<b>2.Nephrotic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDc4NDQyMTg2NzI0MzUw)",	
            "[<b>3.Nephritic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDc5NDQ0MjExMDc5Mjc3)",	
            "[<b>4.Diabetes Nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDgwNDQ2MjM1NDM0MjA0)",	
            "[<b>5.Glomerular Diseases MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDgxNDQ4MjU5Nzg5MTMx)",	
            "[<b>1. Glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDgyNDUwMjg0MTQ0MDU4)",	
            "[<b>3.Growth Hormone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDgzNDUyMzA4NDk4OTg1)",	
            "[<b>1.Headache atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDg0NDU0MzMyODUzOTEy)",	
            "[<b>1. Heart Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDg1NDU2MzU3MjA4ODM5)",	
            "[<b>1.Heart Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDg2NDU4MzgxNTYzNzY2)",	
            "[<b>2. Heart Failure MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDg3NDYwNDA1OTE4Njkz)",	
            "[<b>4.1.S1 Heart sound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDg4NDYyNDMwMjczNjIw)",	
            "[<b>4.2. S2 Heart sound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDg5NDY0NDU0NjI4NTQ3)",	
            "[<b>4.3.Ejection and Non-Ejection Click atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDkwNDY2NDc4OTgzNDc0)",	
            "[<b>4.5 Heart Sounda MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDkxNDY4NTAzMzM4NDAx)",	
            "[<b>1.Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDkyNDcwNTI3NjkzMzI4)",	
            "[<b>2. Hypertension MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDkzNDcyNTUyMDQ4MjU1)",	
            "[<b>1. Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDk0NDc0NTc2NDAzMTgy)",	
            "[<b>2. Coronary artery disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDk1NDc2NjAwNzU4MTA5)",	
            "[<b>1.Risk factors for IBD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDk2NDc4NjI1MTEzMDM2)",	
            "[<b>2.Clinical features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDk3NDgwNjQ5NDY3OTYz)",	
            "[<b>3.Investigations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDk4NDgyNjczODIyODkw)",	
            "[<b>4.Treatment of IBD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MDk5NDg0Njk4MTc3ODE3)",	
            "[<b>1.Managment of ILD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTAwNDg2NzIyNTMyNzQ0)",	
            "[<b>2. Idiopathic ILDs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTAxNDg4NzQ2ODg3Njcx)",	
            "[<b>1.Irritable Bewel Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTAyNDkwNzcxMjQyNTk4)",	
            "[<b>2.1.Normal JVP waveforms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTAzNDkyNzk1NTk3NTI1)",	
            "[<b>2.1.a wave abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTA0NDk0ODE5OTUyNDUy)",	
            "[<b>2.3.x descent abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTA1NDk2ODQ0MzA3Mzc5)",	
            "[<b>2.4.v wave abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTA2NDk4ODY4NjYyMzA2)",	
            "[<b>2.5. y descent abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTA3NTAwODkzMDE3MjMz)",	
            "[<b>2.6.Kussmauls sign atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTA4NTAyOTE3MzcyMTYw)",	
            "[<b>2.7.Hepatojuglar Reflex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTA5NTA0OTQxNzI3MDg3)",	
            "[<b>2.8 JVP MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTEwNTA2OTY2MDgyMDE0)",	
            "[<b>1. Bilirubin physiology and hyperbilirubinemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTExNTA4OTkwNDM2OTQx)",	
            "[<b>2. Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTEyNTExMDE0NzkxODY4)",	
            "[<b>3. Liver Function Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTEzNTEzMDM5MTQ2Nzk1)",	
            "[<b>4. ALD and NAFLD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTE0NTE1MDYzNTAxNzIy)",	
            "[<b>5. Autoimmune diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTE1NTE3MDg3ODU2NjQ5)",	
            "[<b>6. Ascites & SBP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTE2NTE5MTEyMjExNTc2)",	
            "[<b>7. Hepatitis E,A,B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTE3NTIxMTM2NTY2NTAz)",	
            "[<b>8. Hepatitis C atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTE4NTIzMTYwOTIxNDMw)",	
            "[<b>9. Hepatopulmonary syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTE5NTI1MTg1Mjc2MzU3)",	
            "[<b>10. Hepatorenal syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTIwNTI3MjA5NjMxMjg0)",	
            "[<b>11. Esophageal varices and liver transplant atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTIxNTI5MjMzOTg2MjEx)",	
            "[<b>1.S.L.E atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTIyNTMxMjU4MzQxMTM4)",	
            "[<b>2. Systemic sclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTIzNTMzMjgyNjk2MDY1)",	
            "[<b>3.Sicca syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTI0NTM1MzA3MDUwOTky)",	
            "[<b>11.Multiple Sclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTI1NTM3MzMxNDA1OTE5)",	
            "[<b>1.Fat Malabsorption Tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTI2NTM5MzU1NzYwODQ2)",	
            "[<b>2.Carbohydrate Malabsorption Tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTI3NTQxMzgwMTE1Nzcz)",	
            "[<b>3.Schillings Tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTI4NTQzNDA0NDcwNzAw)",	
            "[<b>4.Celiac Sprue atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTI5NTQ1NDI4ODI1NjI3)",	
            "[<b>5.Tropical Sprue atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTMwNTQ3NDUzMTgwNTU0)",	
            "[<b>6.Whipple disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTMxNTQ5NDc3NTM1NDgx)",	
            "[<b>7.Bacterial overgrowth syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTMyNTUxNTAxODkwNDA4)",	
            "[<b>1.OSAH syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTMzNTUzNTI2MjQ1MzM1)",	
            "[<b>2. Pulmonary Embolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTM0NTU1NTUwNjAwMjYy)",	
            "[<b>3. Pulmonary Embolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTM1NTU3NTc0OTU1MTg5)",	
            "[<b>5.Lung Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTM2NTU5NTk5MzEwMTE2)",	
            "[<b>1.Motor Neuron Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTM3NTYxNjIzNjY1MDQz)",	
            "[<b>1.Movement disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTM4NTYzNjQ4MDE5OTcw)",	
            "[<b>5.1.Systolic Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTM5NTY1NjcyMzc0ODk3)",	
            "[<b>5.2.Diastolic Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQwNTY3Njk2NzI5ODI0)",	
            "[<b>5.3.Continous Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQxNTY5NzIxMDg0NzUx)",	
            "[<b>5.4.Factors affecting Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQyNTcxNzQ1NDM5Njc4)",	
            "[<b>5.5 Murmur MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQzNTczNzY5Nzk0NjA1)",	
            "[<b>1.Myasthenia gravis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQ0NTc1Nzk0MTQ5NTMy)",	
            "[<b>8.1.Dilated Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQ1NTc3ODE4NTA0NDU5)",	
            "[<b>8.2. Restrictive Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQ2NTc5ODQyODU5Mzg2)",	
            "[<b>8.3.HOCM atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQ3NTgxODY3MjE0MzEz)",	
            "[<b>8.4 Myocardial Diseases - Cardiomyopathy MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQ4NTgzODkxNTY5MjQw)",	
            "[<b>1. Myositis syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTQ5NTg1OTE1OTI0MTY3)",	
            "[<b>2. Overlap syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTUwNTg3OTQwMjc5MDk0)",	
            "[<b>1.Approach to Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTUxNTg5OTY0NjM0MDIx)",	
            "[<b>2.Symptomatology of renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTUyNTkxOTg4OTg4OTQ4)",	
            "[<b>1.Urine Colour Abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTUzNTk0MDEzMzQzODc1)",	
            "[<b>2.Urine Volume Abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTU0NTk2MDM3Njk4ODAy)",	
            "[<b>3.Hematuria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTU1NTk4MDYyMDUzNzI5)",	
            "[<b>4.Proteinuria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTU2NjAwMDg2NDA4NjU2)",	
            "[<b>5.Urinary Casts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTU3NjAyMTEwNzYzNTgz)",	
            "[<b>6.Urine Analysis MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTU4NjA0MTM1MTE4NTEw)",	
            "[<b>1.Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTU5NjA2MTU5NDczNDM3)",	
            "[<b>2.Bronchiectasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTYwNjA4MTgzODI4MzY0)",	
            "[<b>3.ABPA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTYxNjEwMjA4MTgzMjkx)",	
            "[<b>4.COLD vs ILD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTYyNjEyMjMyNTM4MjE4)",	
            "[<b>5.Managment of COLD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTYzNjE0MjU2ODkzMTQ1)",	
            "[<b>9.1 Parathyroid MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTY0NjE2MjgxMjQ4MDcy)",	
            "[<b>9.Parathyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTY1NjE4MzA1NjAyOTk5)",	
            "[<b>D9. Parathyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTY2NjIwMzI5OTU3OTI2)",	
            "[<b>7.1.Acute Pericarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTY3NjIyMzU0MzEyODUz)",	
            "[<b>7.2.Cardiac Tamponade and Constrictive Pericarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTY4NjI0Mzc4NjY3Nzgw)",	
            "[<b>7.3 Pericardial Diseases MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTY5NjI2NDAzMDIyNzA3)",	
            "[<b>7.Pituitary apoplexy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTcwNjI4NDI3Mzc3NjM0)",	
            "[<b>1. Pleural Effusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTcxNjMwNDUxNzMyNTYx)",	
            "[<b>2. Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTcyNjMyNDc2MDg3NDg4)",	
            "[<b>3.Ventilatory support ARDS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTczNjM0NTAwNDQyNDE1)",	
            "[<b>6.1 Posterior pituitary atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTc0NjM2NTI0Nzk3MzQy)",	
            "[<b>6. Posterior pituitary atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTc1NjM4NTQ5MTUyMjY5)",	
            "[<b>2.Prolactin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTc2NjQwNTczNTA3MTk2)",	
            "[<b>1.Introduction and surfactant disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTc3NjQyNTk3ODYyMTIz)",	
            "[<b>2.1.Wiebels lung model , broncho pul segments & hemoptysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTc4NjQ0NjIyMjE3MDUw)",	
            "[<b>2.2 Intra pleural pressure, airway resistance & pathophysiology of emphysema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTc5NjQ2NjQ2NTcxOTc3)",	
            "[<b>2.3.mechanisms of hypoxemia & dlco atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTgwNjQ4NjcwOTI2OTA0)",	
            "[<b>3.1.Spirometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTgxNjUwNjk1MjgxODMx)",	
            "[<b>3.2.breath sounds & clinical entities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTgyNjUyNzE5NjM2NzU4)",	
            "[<b>4.1.Respiratory failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTgzNjU0NzQzOTkxNjg1)",	
            "[<b>4.2.ARDS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTg0NjU2NzY4MzQ2NjEy)",	
            "[<b>5.1.Pulmonary embolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTg1NjU4NzkyNzAxNTM5)",	
            "[<b>5.2.Pulmonary HTN atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTg2NjYwODE3MDU2NDY2)",	
            "[<b>6.1.Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTg3NjYyODQxNDExMzkz)",	
            "[<b>6.2.Covid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTg4NjY0ODY1NzY2MzIw)",	
            "[<b>7.1. Pleural effusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTg5NjY2ODkwMTIxMjQ3)",	
            "[<b>7.2. Pneumothorax atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTkwNjY4OTE0NDc2MTc0)",	
            "[<b>8.1.Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTkxNjcwOTM4ODMxMTAx)",	
            "[<b>8.2. COPD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTkyNjcyOTYzMTg2MDI4)",	
            "[<b>8.3.Bronchiectasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTkzNjc0OTg3NTQwOTU1)",	
            "[<b>9.1. Eosinophilic lung diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTk0Njc3MDExODk1ODgy)",	
            "[<b>9.2.Aspergillus and lung hypersensitivity pneumonitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTk1Njc5MDM2MjUwODA5)",	
            "[<b>10.1.ILD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTk2NjgxMDYwNjA1NzM2)",	
            "[<b>10.2.Sarcoidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTk3NjgzMDg0OTYwNjYz)",	
            "[<b>10.3.Occupational Lung Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTk4Njg1MTA5MzE1NTkw)",	
            "[<b>11.1. Obstructive sleep apnea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MTk5Njg3MTMzNjcwNTE3)",	
            "[<b>11.2.Lung cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjAwNjg5MTU4MDI1NDQ0)",	
            "[<b>Tuberclosis Update Clinical & Programme aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjAxNjkxMTgyMzgwMzcx)",	
            "[<b>1.Approach to Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjAyNjkzMjA2NzM1Mjk4)",	
            "[<b>2.Review of Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjAzNjk1MjMxMDkwMjI1)",	
            "[<b>3.Symptomatology of RS Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjA0Njk3MjU1NDQ1MTUy)",	
            "[<b>1.Approach to Medicine & Introduction to Rheumatology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjA1Njk5Mjc5ODAwMDc5)",	
            "[<b>2.Auto-inflammatory disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjA2NzAxMzA0MTU1MDA2)",	
            "[<b>3.Auto-immune disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjA3NzAzMzI4NTA5OTMz)",	
            "[<b>4.Approach to Rheumatology disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjA4NzA1MzUyODY0ODYw)",	
            "[<b>5.ANA testing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjA5NzA3Mzc3MjE5Nzg3)",	
            "[<b>1.Clinical Neuroanatomy of Spinal cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjEwNzA5NDAxNTc0NzE0)",	
            "[<b>2.Brown sequard syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjExNzExNDI1OTI5NjQx)",	
            "[<b>3.Intra vs Extra Medullary Spinal lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjEyNzEzNDUwMjg0NTY4)",	
            "[<b>4.Syringomyelia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjEzNzE1NDc0NjM5NDk1)",	
            "[<b>5.Conus Medullaris and Cauda Equina Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjE0NzE3NDk4OTk0NDIy)",	
            "[<b>6.Myelopathy localization atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjE1NzE5NTIzMzQ5MzQ5)",	
            "[<b>7.Trigeminal and facial nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjE2NzIxNTQ3NzA0Mjc2)",	
            "[<b>11.Thyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjE3NzIzNTcyMDU5MjAz)",	
            "[<b>D11. Thyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjE4NzI1NTk2NDE0MTMw)",	
            "[<b>1.Basic of Renal Tubular Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjE5NzI3NjIwNzY5MDU3)",	
            "[<b>2.Bartter & Gitelman Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjIwNzI5NjQ1MTIzOTg0)",	
            "[<b>3.Gordon & Liddle syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjIxNzMxNjY5NDc4OTEx)",	
            "[<b>4.Pseudohypoaldosteronism type 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjIyNzMzNjkzODMzODM4)",	
            "[<b>5.Simplified approach to diagnose Na Channelopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjIzNzM1NzE4MTg4NzY1)",	
            "[<b>6.Renal Tubular Acidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjI0NzM3NzQyNTQzNjky)",	
            "[<b>7.Cystic Kidney Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjI1NzM5NzY2ODk4NjE5)",	
            "[<b>8.Tublar Diseases MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjI2NzQxNzkxMjUzNTQ2)",	
            "[<b>10.Tumor lysis syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjI3NzQzODE1NjA4NDcz)",	
            "[<b>D10.Tumor Lysis Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjI4NzQ1ODM5OTYzNDAw)",	
            "[<b>1. Valvular defects MS and AS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjI5NzQ3ODY0MzE4MzI3)",	
            "[<b>2. MR and MVP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjMwNzQ5ODg4NjczMjU0)",	
            "[<b>3. Infective Endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjMxNzUxOTEzMDI4MTgx)",	
            "[<b>1.Approach of Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjMyNzUzOTM3MzgzMTA4)",	
            "[<b>2.Vasculitis syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjMzNzU1OTYxNzM4MDM1)",	
            "[<b>1.Hepatitis A atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjM0NzU3OTg2MDkyOTYy)",	
            "[<b>2.Mode of Transmission and Prophylaxis Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjM1NzYwMDEwNDQ3ODg5)",	
            "[<b>3.Clinical Features Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjM2NzYyMDM0ODAyODE2)",	
            "[<b>4.Serology Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjM3NzY0MDU5MTU3NzQz)",	
            "[<b>5. Treatment Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjM4NzY2MDgzNTEyNjcw)",	
            "[<b>6.Hepatitis C atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjM5NzY4MTA3ODY3NTk3)",	
            "[<b>7.Hepatitis D atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQwNzcwMTMyMjIyNTI0)",	
            "[<b>8.Hepatitis E atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQxNzcyMTU2NTc3NDUx)",	
            "[<b>1 to 5 topics post class questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQyNzc0MTgwOTMyMzc4)",	
            "[<b>6 to 15 topics Post class questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQzNzc2MjA1Mjg3MzA1)",	
            "[<b>8.Acts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQ0Nzc4MjI5NjQyMjMy)",	
            "[<b>11.Ashpyxia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQ1NzgwMjUzOTk3MTU5)",	
            "[<b>3.Consent atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQ2NzgyMjc4MzUyMDg2)",	
            "[<b>10.Forensic Ballistics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQ3Nzg0MzAyNzA3MDEz)",	
            "[<b>5.IPC SECTIONS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQ4Nzg2MzI3MDYxOTQw)",	
            "[<b>6.Identification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjQ5Nzg4MzUxNDE2ODY3)",	
            "[<b>13.Impotence and Sterility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjUwNzkwMzc1NzcxNzk0)",	
            "[<b>1 Introduction to Forensic Medicine and Ethics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjUxNzkyNDAwMTI2NzIx)",	
            "[<b>2 Legal Procedures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjUyNzk0NDI0NDgxNjQ4)",	
            "[<b>9.Mechinical Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjUzNzk2NDQ4ODM2NTc1)",	
            "[<b>4.Negligence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjU0Nzk4NDczMTkxNTAy)",	
            "[<b>14.Post Mortem Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjU1ODAwNDk3NTQ2NDI5)",	
            "[<b>7 Thanatology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjU2ODAyNTIxOTAxMzU2)",	
            "[<b>12.Thermal Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjU3ODA0NTQ2MjU2Mjgz)",	
            "[<b>15.Toxicology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjU4ODA2NTcwNjExMjEw)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        medicinede_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"medicinede_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"medicinede_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(medicinede_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("dermatologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>11.1.Allergic Disorders and Dermatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjU5ODA4NTk0OTY2MTM3)",
            "[<b>3.1.Appendegeal Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjYwODEwNjE5MzIxMDY0)",
            "[<b>1.1.Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjYxODEyNjQzNjc1OTkx)",
            "[<b>1.2.Structure of Nail atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjYyODE0NjY4MDMwOTE4)",
            "[<b>3.MCQ Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjYzODE2NjkyMzg1ODQ1)",
            "[<b>14.Cutaneous Lesions in Systemic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjY0ODE4NzE2NzQwNzcy)",
            "[<b>13.Cutaneous Malignancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjY1ODIwNzQxMDk1Njk5)",
            "[<b>8.1 Disorders of Keratinization and Genodermatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjY2ODIyNzY1NDUwNjI2)",
            "[<b>2.1.Basics of Hair atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjY3ODI0Nzg5ODA1NTUz)",
            "[<b>2.2.Disorders of Hairs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjY4ODI2ODE0MTYwNDgw)",
            "[<b>4.1.Bacterial Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjY5ODI4ODM4NTE1NDA3)",
            "[<b>4.2.Fungal Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjcwODMwODYyODcwMzM0)",
            "[<b>4.3.Mycobacterial disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjcxODMyODg3MjI1MjYx)",
            "[<b>4.4.Parasitic infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjcyODM0OTExNTgwMTg4)",
            "[<b>4.5.Protozoal Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjczODM2OTM1OTM1MTE1)",
            "[<b>4.6.Viral Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjc0ODM4OTYwMjkwMDQy)",
            "[<b>12.Leprosy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjc1ODQwOTg0NjQ0OTY5)",
            "[<b>15.1.Drug Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjc2ODQzMDA4OTk5ODk2)",
            "[<b>15.2.Paraneoplastic Dermatoses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjc3ODQ1MDMzMzU0ODIz)",
            "[<b>9.1.Nutritional deficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjc4ODQ3MDU3NzA5NzUw)",
            "[<b>5.1.Psoriasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjc5ODQ5MDgyMDY0Njc3)",
            "[<b>5.2.Lichen planus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjgwODUxMTA2NDE5NjA0)",
            "[<b>5.3.Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjgxODUzMTMwNzc0NTMx)",
            "[<b>7.1 Pigmentary disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjgyODU1MTU1MTI5NDU4)",
            "[<b>10.STD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjgzODU3MTc5NDg0Mzg1)",
            "[<b>6.1 Vesciculobullous disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjg0ODU5MjAzODM5MzEy)",
            "[<b>3.Appendageal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjg1ODYxMjI4MTk0MjM5)",
            "[<b>1.Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjg2ODYzMjUyNTQ5MTY2)",
            "[<b>8.Disorders of Keratinization and Genodermatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjg3ODY1Mjc2OTA0MDkz)",
            "[<b>2.Hair and Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjg4ODY3MzAxMjU5MDIw)",
            "[<b>1.Bacterial Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjg5ODY5MzI1NjEzOTQ3)",
            "[<b>2.Fungal Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjkwODcxMzQ5OTY4ODc0)",
            "[<b>3.Mycobacterial Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjkxODczMzc0MzIzODAx)",
            "[<b>4.Protozoal and Parasitic Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjkyODc1Mzk4Njc4NzI4)",
            "[<b>5.Viral Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MjkzODc3NDIzMDMzNjU1)",
            "[<b>15.1.Drug Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjk0ODc5NDQ3Mzg4NTgy)",
            "[<b>9.1.Nutritional deficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjk1ODgxNDcxNzQzNTA5)",
            "[<b>1. Psoriasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjk2ODgzNDk2MDk4NDM2)",
            "[<b>2.Lichen planus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjk3ODg1NTIwNDUzMzYz)",
            "[<b>3. Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjk4ODg3NTQ0ODA4Mjkw)",
            "[<b>5.4 MCQ Papulosqamous disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mjk5ODg5NTY5MTYzMjE3)",
            "[<b>Pigmentary Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzAwODkxNTkzNTE4MTQ0)",
            "[<b>1.STD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzAxODkzNjE3ODczMDcx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        dermatologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"dermatologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"dermatologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(dermatologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pathologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Arteriosclerosis & Atherosclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzAyODk1NjQyMjI3OTk4)",	
            "[<b>2.Aneurysm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzAzODk3NjY2NTgyOTI1)",	
            "[<b>3.Aortic dissection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzA0ODk5NjkwOTM3ODUy)",	
            "[<b>4.Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzA1OTAxNzE1MjkyNzc5)",	
            "[<b>5.Vascular Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzA2OTAzNzM5NjQ3NzA2)",	
            "[<b>1. Developmental disease & tumors of bone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzA3OTA1NzY0MDAyNjMz)",	
            "[<b>2. Soft Tissue tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzA4OTA3Nzg4MzU3NTYw)",	
            "[<b>1 Hypertension, Atherosclerosis, Aneurysms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzA5OTA5ODEyNzEyNDg3)",	
            "[<b>2 Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzEwOTExODM3MDY3NDE0)",	
            "[<b>3 Cardiac Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzExOTEzODYxNDIyMzQx)",	
            "[<b>1.Cellular adaptations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzEyOTE1ODg1Nzc3MjY4)",	
            "[<b>2.Cell Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzEzOTE3OTEwMTMyMTk1)",	
            "[<b>3.Cell Death atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzE0OTE5OTM0NDg3MTIy)",	
            "[<b>1 Salivary glands, Esophagus & Stomach atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzE1OTIxOTU4ODQyMDQ5)",	
            "[<b>1.Oral & salivary glands atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzE2OTIzOTgzMTk2OTc2)",	
            "[<b>2 Enteropathy & Inflammatory bowel disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzE3OTI2MDA3NTUxOTAz)",	
            "[<b>2.Esophagus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzE4OTI4MDMxOTA2ODMw)",	
            "[<b>3 Polyps & tumors in Intestine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzE5OTMwMDU2MjYxNzU3)",	
            "[<b>3.Gastritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzIwOTMyMDgwNjE2Njg0)",	
            "[<b>4 Liver & Pancreas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzIxOTM0MTA0OTcxNjEx)",	
            "[<b>4.Stomach Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzIyOTM2MTI5MzI2NTM4)",	
            "[<b>5.Malabsorption syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzIzOTM4MTUzNjgxNDY1)",	
            "[<b>1.Cellular adaptation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzI0OTQwMTc4MDM2Mzky)",	
            "[<b>2.Cell injury & reversible irreversible atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzI1OTQyMjAyMzkxMzE5)",	
            "[<b>3.Necrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzI2OTQ0MjI2NzQ2MjQ2)",	
            "[<b>4. Apoptosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzI3OTQ2MjUxMTAxMTcz)",	
            "[<b>5.Necroptosis Ferroptosis and Pyroptosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzI4OTQ4Mjc1NDU2MTAw)",	
            "[<b>1. Genetics Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzI5OTUwMjk5ODExMDI3)",	
            "[<b>2. Mutations & Chromosomal Abnormalities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzMwOTUyMzI0MTY1OTU0)",	
            "[<b>3. Inheritance of genetic diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzMxOTU0MzQ4NTIwODgx)",	
            "[<b>4. Genetic diagnostic tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzMyOTU2MzcyODc1ODA4)",	
            "[<b>1. Testicular & prostatic carcinoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzMzOTU4Mzk3MjMwNzM1)",	
            "[<b>2. Tumors of Female genital tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzM0OTYwNDIxNTg1NjYy)",	
            "[<b>3. Neoplastic & Preneoplastic Breast lesions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzM1OTYyNDQ1OTQwNTg5)",	
            "[<b>1.Heart failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzM2OTY0NDcwMjk1NTE2)",	
            "[<b>2.IHD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzM3OTY2NDk0NjUwNDQz)",	
            "[<b>3.MI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzM4OTY4NTE5MDA1Mzcw)",	
            "[<b>4.RHD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzM5OTcwNTQzMzYwMjk3)",	
            "[<b>5.Infective endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQwOTcyNTY3NzE1MjI0)",	
            "[<b>6.Valvular disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQxOTc0NTkyMDcwMTUx)",	
            "[<b>7.Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQyOTc2NjE2NDI1MDc4)",	
            "[<b>8.Cardiac tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQzOTc4NjQwNzgwMDA1)",	
            "[<b>1. Edema & Congestion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQ0OTgwNjY1MTM0OTMy)",	
            "[<b>2. Shock atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQ1OTgyNjg5NDg5ODU5)",	
            "[<b>1. Hemostasis & thromboelastography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQ2OTg0NzEzODQ0Nzg2)",	
            "[<b>2. Thrombosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQ3OTg2NzM4MTk5NzEz)",	
            "[<b>3. Primary Plug disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQ4OTg4NzYyNTU0NjQw)",	
            "[<b>4. Secondary plug disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzQ5OTkwNzg2OTA5NTY3)",	
            "[<b>1. Imunity Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzUwOTkyODExMjY0NDk0)",	
            "[<b>2. Hypersensitivity Transplant immunology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzUxOTk0ODM1NjE5NDIx)",	
            "[<b>3. Primary Immunodeficiency disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzUyOTk2ODU5OTc0MzQ4)",	
            "[<b>4. Amyloidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzUzOTk4ODg0MzI5Mjc1)",	
            "[<b>1.Acute Inflammation Mechanism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzU1MDAwOTA4Njg0MjAy)",	
            "[<b>2.Effects Mediators of Acute inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzU2MDAyOTMzMDM5MTI5)",	
            "[<b>3. Chronic inflammation Wound healing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzU3MDA0OTU3Mzk0MDU2)",	
            "[<b>1. Endocrine tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzU4MDA2OTgxNzQ4OTgz)",	
            "[<b>2. CNS tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzU5MDA5MDA2MTAzOTEw)",	
            "[<b>1. Basic terminology Carcinogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzYwMDExMDMwNDU4ODM3)",	
            "[<b>2. Molecular mechanisms of cancers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzYxMDEzMDU0ODEzNzY0)",	
            "[<b>3. Warburg Effect & immune escape by tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzYyMDE1MDc5MTY4Njkx)",	
            "[<b>4. metastasis, clinical features & prognosis of tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzYzMDE3MTAzNTIzNjE4)",	
            "[<b>1. RBC Indices atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzY0MDE5MTI3ODc4NTQ1)",	
            "[<b>2. Microcytic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzY1MDIxMTUyMjMzNDcy)",	
            "[<b>3. Macro & Normocytic anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzY2MDIzMTc2NTg4Mzk5)",	
            "[<b>4.Acquired Hemolytic anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzY3MDI1MjAwOTQzMzI2)",	
            "[<b>5. Inherited Hemolytic anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzY4MDI3MjI1Mjk4MjUz)",	
            "[<b>1.Basics of glomerulonephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzY5MDI5MjQ5NjUzMTgw)",	
            "[<b>2. Acute Nephritic Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzcwMDMxMjc0MDA4MTA3)",	
            "[<b>3. Nephrotic Syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzcxMDMzMjk4MzYzMDM0)",	
            "[<b>4. Alports & Cystic disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzcyMDM1MzIyNzE3OTYx)",	
            "[<b>5. Renal tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzczMDM3MzQ3MDcyODg4)",	
            "[<b>1.Introduction to Renal-Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzc0MDM5MzcxNDI3ODE1)",	
            "[<b>2.Nephritic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzc1MDQxMzk1NzgyNzQy)",	
            "[<b>3.Nephrotic Syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzc2MDQzNDIwMTM3NjY5)",	
            "[<b>4.Diabetis and lupus nephritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzc3MDQ1NDQ0NDkyNTk2)",	
            "[<b>5.Renal casts and stones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzc4MDQ3NDY4ODQ3NTIz)",	
            "[<b>6.Renal Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzc5MDQ5NDkzMjAyNDUw)",	
            "[<b>1 ARDS, Obstructive disease, Cystic fibrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzgwMDUxNTE3NTU3Mzc3)",	
            "[<b>2. Pneumoconiosis, Granulomatous diseases of Lung atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzgxMDUzNTQxOTEyMzA0)",	
            "[<b>3. Tumors of Lungs & Pleura atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzgyMDU1NTY2MjY3MjMx)",	
            "[<b>1.Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzgzMDU3NTkwNjIyMTU4)",	
            "[<b>2.Chronic bronchitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzg0MDU5NjE0OTc3MDg1)",	
            "[<b>3.Emphysema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzg1MDYxNjM5MzMyMDEy)",	
            "[<b>4.Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzg2MDYzNjYzNjg2OTM5)",	
            "[<b>5.Bronchiectasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzg3MDY1Njg4MDQxODY2)",	
            "[<b>6.Sarcoidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzg4MDY3NzEyMzk2Nzkz)",	
            "[<b>7.Hypernsitivity pneumonitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzg5MDY5NzM2NzUxNzIw)",	
            "[<b>8.ARDS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzkwMDcxNzYxMTA2NjQ3)",	
            "[<b>9.PAP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzkxMDczNzg1NDYxNTc0)",	
            "[<b>10.Pneumoconiasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzkyMDc1ODA5ODE2NTAx)",	
            "[<b>11.Lung Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0MzkzMDc3ODM0MTcxNDI4)",	
            "[<b>1.Blood Vessels atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzk0MDc5ODU4NTI2MzU1)",	
            "[<b>2.Blood vessels and Heart atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzk1MDgxODgyODgxMjgy)",	
            "[<b>3.Lungs & GIT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzk2MDgzOTA3MjM2MjA5)",	
            "[<b>4.GIT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzk3MDg1OTMxNTkxMTM2)",	
            "[<b>6.kidney , CNS tumors , Breast Carcinoma , Testicular tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzk4MDg3OTU1OTQ2MDYz)",	
            "[<b>7.BPH, Prostate Adenocarcinoma, Ovarian Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Mzk5MDg5OTgwMzAwOTkw)",	
            "[<b>8.Endometrial Cancer , LIVER , Bone tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDAwMDkyMDA0NjU1OTE3)",	
            "[<b>GIT , KIDNEY Day 23 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDAxMDk0MDI5MDEwODQ0)",	
            "[<b>1 Blood banking atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDAyMDk2MDUzMzY1Nzcx)",	
            "[<b>2 Transfusion Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDAzMDk4MDc3NzIwNjk4)",	
            "[<b>1 Approach to WBC neoplasms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDA0MTAwMTAyMDc1NjI1)",	
            "[<b>2 CD Markers in Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDA1MTAyMTI2NDMwNTUy)",	
            "[<b>3 Lymphoid Neoplasms ( Lymphom,as, CLL, ALL) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDA2MTA0MTUwNzg1NDc5)",	
            "[<b>4 Multiple myeloma & Langerhan cell histiocytosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDA3MTA2MTc1MTQwNDA2)",	
            "[<b>5 Myeloid Neoplasms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDA4MTA4MTk5NDk1MzMz)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pathologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pathologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pathologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pathologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("entde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Anatomy of Middle Ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDA5MTEwMjIzODUwMjYw)",
            "[<b>2. Anatomy of External Ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDEwMTEyMjQ4MjA1MTg3)",
            "[<b>3.Anatomy of Inner Ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDExMTE0MjcyNTYwMTE0)",
            "[<b>1.Otosclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDEyMTE2Mjk2OTE1MDQx)",
            "[<b>2.Meniere Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDEzMTE4MzIxMjY5OTY4)",
            "[<b>3.Acoustic Neuroma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDE0MTIwMzQ1NjI0ODk1)",
            "[<b>1. Subjective Audiometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDE1MTIyMzY5OTc5ODIy)",
            "[<b>2. Objective Audiometry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDE2MTI0Mzk0MzM0NzQ5)",
            "[<b>1.Clinical disorders of external ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDE3MTI2NDE4Njg5Njc2)",
            "[<b>1. Clinical disorders of middle ear atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDE4MTI4NDQzMDQ0NjAz)",
            "[<b>1.Rehabilitation of Deaf Patient atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDE5MTMwNDY3Mzk5NTMw)",
            "[<b>2. Facial Nerve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDIwMTMyNDkxNzU0NDU3)",
            "[<b>3.Inner ear Assessment & Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDIxMTM0NTE2MTA5Mzg0)",
            "[<b>1. Clinical Anatomy of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDIyMTM2NTQwNDY0MzEx)",
            "[<b>2.Congenital Anomalies of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDIzMTM4NTY0ODE5MjM4)",
            "[<b>3.Carcinoma Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDI0MTQwNTg5MTc0MTY1)",
            "[<b>4.Vocal Cord Paralysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDI1MTQyNjEzNTI5MDky)",
            "[<b>1.Pharynx & Tonsil atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDI2MTQ0NjM3ODg0MDE5)",
            "[<b>1. Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDI3MTQ2NjYyMjM4OTQ2)",
            "[<b>2. Sinusitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDI4MTQ4Njg2NTkzODcz)",
            "[<b>3. Rhinitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDI5MTUwNzEwOTQ4ODAw)",
            "[<b>4. Malignancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDMwMTUyNzM1MzAzNzI3)",
            "[<b>5. Facial Fracture atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDMxMTU0NzU5NjU4NjU0)",
            "[<b>6. Epistaxis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDMyMTU2Nzg0MDEzNTgx)",
            "[<b>7. Nasal Polyposis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDMzMTU4ODA4MzY4NTA4)",
            "[<b>8. Granulomatosis Disease of Nose atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDM0MTYwODMyNzIzNDM1)",
            "[<b>9. DNS and Associated Abnormalities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDM1MTYyODU3MDc4MzYy)",
            "[<b>10. Endoscopy in Rhinology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDM2MTY0ODgxNDMzMjg5)",
            "[<b>11. X-Rays in Rhinology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDM3MTY2OTA1Nzg4MjE2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        entde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"entde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"entde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(entde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("biochemistryde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Amino Acid classification & Urea Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDM4MTY4OTMwMTQzMTQz)",
            "[<b>2. Branched chain Amino Acid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDM5MTcwOTU0NDk4MDcw)",
            "[<b>3. Phenylalanine, Tyrosine , Tryptophann , Methionine metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQwMTcyOTc4ODUyOTk3)",
            "[<b>4.Biological Oxidation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQxMTc1MDAzMjA3OTI0)",
            "[<b>1.1.Carbohydrate chemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQyMTc3MDI3NTYyODUx)",
            "[<b>1.2.Carbohydrate Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQzMTc5MDUxOTE3Nzc4)",
            "[<b>1.3 Carbohydrate MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQ0MTgxMDc2MjcyNzA1)",
            "[<b>1.1 Carbohydrate chemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQ1MTgzMTAwNjI3NjMy)",
            "[<b>Electron Transport Chain & oxidative phosphorylation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQ2MTg1MTI0OTgyNTU5)",
            "[<b>Enzyme atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQ3MTg3MTQ5MzM3NDg2)",
            "[<b>3.5 Enzymes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQ4MTg5MTczNjkyNDEz)",
            "[<b>1.Purine and Pyrimidine nucleotide metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDQ5MTkxMTk4MDQ3MzQw)",
            "[<b>2.DNA Replication atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDUwMTkzMjIyNDAyMjY3)",
            "[<b>3.DNA Repair atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDUxMTk1MjQ2NzU3MTk0)",
            "[<b>4. Transcription atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDUyMTk3MjcxMTEyMTIx)",
            "[<b>5. RNA Types and Translation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDUzMTk5Mjk1NDY3MDQ4)",
            "[<b>6.Genetic Technology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDU0MjAxMzE5ODIxOTc1)",
            "[<b>3.6 HEME atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDU1MjAzMzQ0MTc2OTAy)",
            "[<b>1. HEME Synthesis & Porphyria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDU2MjA1MzY4NTMxODI5)",
            "[<b>3.4 Higher Order Structure of Protein atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDU3MjA3MzkyODg2NzU2)",
            "[<b>1. Lac Operon Model atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDU4MjA5NDE3MjQxNjgz)",
            "[<b>2.1.Lipid Chemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDU5MjExNDQxNTk2NjEw)",
            "[<b>2.2.Lipid Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDYwMjEzNDY1OTUxNTM3)",
            "[<b>2.3.Lipoproteins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDYxMjE1NDkwMzA2NDY0)",
            "[<b>2.4 Lipid MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDYyMjE3NTE0NjYxMzkx)",
            "[<b>2.1 Lipid Chemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDYzMjE5NTM5MDE2MzE4)",
            "[<b>1.2.1 Glycolysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDY0MjIxNTYzMzcxMjQ1)",
            "[<b>1.2.2 PDH complex & TCA cycle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDY1MjIzNTg3NzI2MTcy)",
            "[<b>1.2.3 Anaplerotic and Cataplerotic Reaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDY2MjI1NjEyMDgxMDk5)",
            "[<b>1.2.4 Gluconeogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDY3MjI3NjM2NDM2MDI2)",
            "[<b>1.2.5 Fructose and Galactose Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDY4MjI5NjYwNzkwOTUz)",
            "[<b>1.2.6 HMP Pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDY5MjMxNjg1MTQ1ODgw)",
            "[<b>1.2.7 Glycogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDcwMjMzNzA5NTAwODA3)",
            "[<b>1.2.8 Glycogenolysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDcxMjM1NzMzODU1NzM0)",
            "[<b>1.2.9 Glycogen storage disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDcyMjM3NzU4MjEwNjYx)",
            "[<b>1.2.10 Uronic Acid Pathways atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDczMjM5NzgyNTY1NTg4)",
            "[<b>2.2.1 Chylomicron & VLDL Metabolisim atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDc0MjQxODA2OTIwNTE1)",
            "[<b>2.2.2 LDL Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDc1MjQzODMxMjc1NDQy)",
            "[<b>2.2.3 HDL Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDc2MjQ1ODU1NjMwMzY5)",
            "[<b>2.2.4 Dyslipidemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDc3MjQ3ODc5OTg1Mjk2)",
            "[<b>2.2.5 Fatty Acid Synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDc4MjQ5OTA0MzQwMjIz)",
            "[<b>2.2.6. Fatty Acid Oxidation and Carnitine shuttle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDc5MjUxOTI4Njk1MTUw)",
            "[<b>2.2.7. Ketone body metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDgwMjUzOTUzMDUwMDc3)",
            "[<b>2.2.8. Cholesterol and Bile acid synthesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDgxMjU1OTc3NDA1MDA0)",
            "[<b>8.1.1.DNA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDgyMjU4MDAxNzU5OTMx)",
            "[<b>8.1.2 DNA repair atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDgzMjYwMDI2MTE0ODU4)",
            "[<b>8.1.3 Mitochondrial DNA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDg0MjYyMDUwNDY5Nzg1)",
            "[<b>7.Nulcleotide atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDg1MjY0MDc0ODI0NzEy)",
            "[<b>Nulcleotide MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDg2MjY2MDk5MTc5NjM5)",
            "[<b>3.1.Protein Chemistry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDg3MjY4MTIzNTM0NTY2)",
            "[<b>3.2.Protein N Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDg4MjcwMTQ3ODg5NDkz)",
            "[<b>3.3.Protein C Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDg5MjcyMTcyMjQ0NDIw)",
            "[<b>3.4 Protein MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDkwMjc0MTk2NTk5MzQ3)",
            "[<b>8.3.1.Protein-Translation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDkxMjc2MjIwOTU0Mjc0)",
            "[<b>8.2.1 EUK- Transcription atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDkyMjc4MjQ1MzA5MjAx)",
            "[<b>8.2.2 PROK- Transcription atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDkzMjgwMjY5NjY0MTI4)",
            "[<b>8.2.3 Types of RNA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDk0MjgyMjk0MDE5MDU1)",
            "[<b>8.4.1 Prok atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDk1Mjg0MzE4MzczOTgy)",
            "[<b>8.4..2 EUK atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDk2Mjg2MzQyNzI4OTA5)",
            "[<b>5.1.PCR atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDk3Mjg4MzY3MDgzODM2)",
            "[<b>5.2.RFLP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDk4MjkwMzkxNDM4NzYz)",
            "[<b>1. Vitamins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NDk5MjkyNDE1NzkzNjkw)",
            "[<b>6.1.Fat Soluble Vitamins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTAwMjk0NDQwMTQ4NjE3)",
            "[<b>6.2 Water Soluble Vitamins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTAxMjk2NDY0NTAzNTQ0)",
            "[<b>6.3 Vitamins MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTAyMjk4NDg4ODU4NDcx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        biochemistryde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"biochemistryde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"biochemistryde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(biochemistryde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pathologydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Cellular Adaptations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTAzMzAwNTEzMjEzMzk4)",
            "[<b>2 Cell Injury atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTA0MzAyNTM3NTY4MzI1)",
            "[<b>3. Cell Death atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTA1MzA0NTYxOTIzMjUy)",
            "[<b>1. Mechanism of Acute inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTA2MzA2NTg2Mjc4MTc5)",
            "[<b>2. Effects & Mediators of Acute inflammation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTA3MzA4NjEwNjMzMTA2)",
            "[<b>3. Chronic Inflammation & Wound Healing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTA4MzEwNjM0OTg4MDMz)",
            "[<b>1. Immunity Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTA5MzEyNjU5MzQyOTYw)",
            "[<b>2. Hypersensitivity & Transplant pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTEwMzE0NjgzNjk3ODg3)",
            "[<b>3. Immunodeficiency disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTExMzE2NzA4MDUyODE0)",
            "[<b>4. Amyloidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTEyMzE4NzMyNDA3NzQx)",
            "[<b>1. Edema & Congestion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTEzMzIwNzU2NzYyNjY4)",
            "[<b>2. Shock atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTE0MzIyNzgxMTE3NTk1)",
            "[<b>1. Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTE1MzI0ODA1NDcyNTIy)",
            "[<b>2. Mutations & Chromosomal Abnormalities atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTE2MzI2ODI5ODI3NDQ5)",
            "[<b>3. Inheritance of Genetic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTE3MzI4ODU0MTgyMzc2)",
            "[<b>4. Genetic Diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTE4MzMwODc4NTM3MzAz)",
            "[<b>1. Basics terminology & Carcinogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTE5MzMyOTAyODkyMjMw)",
            "[<b>2. Molecular mechanism of carcinogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTIwMzM0OTI3MjQ3MTU3)",
            "[<b>3. Warburg Effect & immune escape by tumor cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTIxMzM2OTUxNjAyMDg0)",
            "[<b>4. Metastasis, Clinical featrure and prognosis of cancers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTIyMzM4OTc1OTU3MDEx)",
            "[<b>1 ARDS, Obstructive disease, Cystic fibrosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTIzMzQxMDAwMzExOTM4)",
            "[<b>2. Pneumoconiosis, Granulomatous diseases of Lung atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTI0MzQzMDI0NjY2ODY1)",
            "[<b>3. Tumors of Lungs & Pleura atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTI1MzQ1MDQ5MDIxNzky)",
            "[<b>1 Salivary glands, Esophagus & Stomach atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTI2MzQ3MDczMzc2NzE5)",
            "[<b>2 Enteropathy & Inflammatory bowel disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTI3MzQ5MDk3NzMxNjQ2)",
            "[<b>3 Polyps & tumors in Intestine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTI4MzUxMTIyMDg2NTcz)",
            "[<b>4 Liver & Pancreas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTI5MzUzMTQ2NDQxNTAw)",
            "[<b>1.Hemostasis & Thromboelastography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTMwMzU1MTcwNzk2NDI3)",
            "[<b>2. Thrombosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTMxMzU3MTk1MTUxMzU0)",
            "[<b>3. Primary plug disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTMyMzU5MjE5NTA2Mjgx)",
            "[<b>4. Secondary Plug disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTMzMzYxMjQzODYxMjA4)",
            "[<b>1. RBC Indices atf (1).mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTM0MzYzMjY4MjE2MTM1)",
            "[<b>1. RBC Indices atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTM1MzY1MjkyNTcxMDYy)",
            "[<b>2. Microcytic Anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTM2MzY3MzE2OTI1OTg5)",
            "[<b>3. Macro & Normocytic anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTM3MzY5MzQxMjgwOTE2)",
            "[<b>4.Acquired Hemolytic anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTM4MzcxMzY1NjM1ODQz)",
            "[<b>5. Inherited Hemolytic anemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTM5MzczMzg5OTkwNzcw)",
            "[<b>1 Hypertension, Atherosclerosi, Aneurysms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQwMzc1NDE0MzQ1Njk3)",
            "[<b>2 Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQxMzc3NDM4NzAwNjI0)",
            "[<b>3 Cardiac Pathology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQyMzc5NDYzMDU1NTUx)",
            "[<b>1. Blood banking atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQzMzgxNDg3NDEwNDc4)",
            "[<b>2. Transfusion reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQ0MzgzNTExNzY1NDA1)",
            "[<b>1. Approach to WBC neoplasms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQ1Mzg1NTM2MTIwMzMy)",
            "[<b>2.CD Markers in diagnosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQ2Mzg3NTYwNDc1MjU5)",
            "[<b>3. Lymphomas & lymphoid leukaemias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQ3Mzg5NTg0ODMwMTg2)",
            "[<b>4. Multiple myeloma & Langerhan cell histiocytosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQ4MzkxNjA5MTg1MTEz)",
            "[<b>5. Myeloid Neoplasms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTQ5MzkzNjMzNTQwMDQw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pathologydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pathologydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pathologydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pathologydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("surgerydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.Appendix atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTUwMzk1NjU3ODk0OTY3)",
            "[<b>1. Esophagus- Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTUxMzk3NjgyMjQ5ODk0)",
            "[<b>2- Esophagus Zenker dverticulum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTUyMzk5NzA2NjA0ODIx)",
            "[<b>3.Web and Ring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTUzNDAxNzMwOTU5NzQ4)",
            "[<b>4.Perforation- Boerhaave synd atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTU0NDAzNzU1MzE0Njc1)",
            "[<b>5. Tracheo-esophageal fistula atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTU1NDA1Nzc5NjY5NjAy)",
            "[<b>6.Motility disorder Achalasia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTU2NDA3ODA0MDI0NTI5)",
            "[<b>7. Esophagus- Hiatus henia and GERD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTU3NDA5ODI4Mzc5NDU2)",
            "[<b>8. Esophagus - Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTU4NDExODUyNzM0Mzgz)",
            "[<b>1.Meckel's Diverticulum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTU5NDEzODc3MDg5MzEw)",
            "[<b>2.Intussusception atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTYwNDE1OTAxNDQ0MjM3)",
            "[<b>3.Carcinoid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTYxNDE3OTI1Nzk5MTY0)",
            "[<b>4.Intestinal obstruction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTYyNDE5OTUwMTU0MDkx)",
            "[<b>1. CHPS- Congenital Hypertrophic pyloric stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTYzNDIxOTc0NTA5MDE4)",
            "[<b>2. Stomach- Menetriers, Volvulus, Bezoar atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTY0NDIzOTk4ODYzOTQ1)",
            "[<b>3. ACID Peptic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTY1NDI2MDIzMjE4ODcy)",
            "[<b>4. Stomach Gastirc Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTY2NDI4MDQ3NTczNzk5)",
            "[<b>5.GIST atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTY3NDMwMDcxOTI4NzI2)",
            "[<b>6.Duodenum-duodenal atresia, sma syndrome, ipsid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTY4NDMyMDk2MjgzNjUz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        surgerydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"surgerydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"surgerydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(surgerydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psychiatryde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Child Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTY5NDM0MTIwNjM4NTgw)",	
            "[<b>2. MCQ discussion chapter 7 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTcwNDM2MTQ0OTkzNTA3)",	
            "[<b>1.History taking atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTcxNDM4MTY5MzQ4NDM0)",	
            "[<b>2.Examination thought disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTcyNDQwMTkzNzAzMzYx)",	
            "[<b>3. Examination perception, Mood and behaviour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTczNDQyMjE4MDU4Mjg4)",	
            "[<b>4. Examination cognitive functions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTc0NDQ0MjQyNDEzMjE1)",	
            "[<b>5. Mcq Discussion Chapter 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTc1NDQ2MjY2NzY4MTQy)",	
            "[<b>Introduction to psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTc2NDQ4MjkxMTIzMDY5)",	
            "[<b>1. Eating Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTc3NDUwMzE1NDc3OTk2)",	
            "[<b>2. Sleep Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTc4NDUyMzM5ODMyOTIz)",	
            "[<b>3. Sexual Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTc5NDU0MzY0MTg3ODUw)",	
            "[<b>4. Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTgwNDU2Mzg4NTQyNzc3)",	
            "[<b>5. MCQ Discussion chapter 8 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTgxNDU4NDEyODk3NzA0)",	
            "[<b>1. Mania and antimanic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTgyNDYwNDM3MjUyNjMx)",	
            "[<b>2. Depression and antidepressants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTgzNDYyNDYxNjA3NTU4)",	
            "[<b>3. Bipolar disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTg0NDY0NDg1OTYyNDg1)",	
            "[<b>4. Mcq Discussion Chapter 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTg1NDY2NTEwMzE3NDEy)",	
            "[<b>1. Anxiety disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTg2NDY4NTM0NjcyMzM5)",	
            "[<b>2. Ocd and related disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTg3NDcwNTU5MDI3MjY2)",	
            "[<b>3. Impulse control disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTg4NDcyNTgzMzgyMTkz)",	
            "[<b>4. Trauma and stress related disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTg5NDc0NjA3NzM3MTIw)",	
            "[<b>5. Somatoform disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTkwNDc2NjMyMDkyMDQ3)",	
            "[<b>6. Conversion disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTkxNDc4NjU2NDQ2OTc0)",	
            "[<b>7. Dissociative disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTkyNDgwNjgwODAxOTAx)",	
            "[<b>8. Mcq Discussion Chapter 4 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTkzNDgyNzA1MTU2ODI4)",	
            "[<b>1. Delirium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTk0NDg0NzI5NTExNzU1)",	
            "[<b>2. Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTk1NDg2NzUzODY2Njgy)",	
            "[<b>3. Amnestic syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTk2NDg4Nzc4MjIxNjA5)",	
            "[<b>4. MCQ Chapter 5 discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTk3NDkwODAyNTc2NTM2)",	
            "[<b>1. Learning Models atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTk4NDkyODI2OTMxNDYz)",	
            "[<b>2. Psychosexual stages atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NTk5NDk0ODUxMjg2Mzkw)",	
            "[<b>3. Models of mind and defense mechanisms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjAwNDk2ODc1NjQxMzE3)",	
            "[<b>4. Psychotherapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjAxNDk4ODk5OTk2MjQ0)",	
            "[<b>5. Community Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjAyNTAwOTI0MzUxMTcx)",	
            "[<b>6. MCQ discussion chapter 9 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjAzNTAyOTQ4NzA2MDk4)",	
            "[<b>1 Schizophrenia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjA0NTA0OTczMDYxMDI1)",	
            "[<b>2 Antipsychotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjA1NTA2OTk3NDE1OTUy)",	
            "[<b>3 Delusional disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjA2NTA5MDIxNzcwODc5)",	
            "[<b>4. Mcq Discussion Chapter 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjA3NTExMDQ2MTI1ODA2)",	
            "[<b>1. Deaddiction psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjA4NTEzMDcwNDgwNzMz)",	
            "[<b>2.Drugs used in deaddiction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjA5NTE1MDk0ODM1NjYw)",	
            "[<b>3. MCQ discussion chapter 6 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjEwNTE3MTE5MTkwNTg3)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psychiatryde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psychiatryde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psychiatryde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psychiatryde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psychiatrydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Child Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjExNTE5MTQzNTQ1NTE0)",	
            "[<b>2. MCQ discussion chapter 7 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjEyNTIxMTY3OTAwNDQx)",	
            "[<b>1.History Taking atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjEzNTIzMTkyMjU1MzY4)",	
            "[<b>2.Examination thought disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjE0NTI1MjE2NjEwMjk1)",	
            "[<b>3. Examination perception Mood and behaviour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjE1NTI3MjQwOTY1MjIy)",	
            "[<b>4. Examination cognitive functions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjE2NTI5MjY1MzIwMTQ5)",	
            "[<b>5. Mcq Discussion Chapter 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjE3NTMxMjg5Njc1MDc2)",	
            "[<b>Introduction to Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjE4NTMzMzE0MDMwMDAz)",	
            "[<b>1. Eating Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjE5NTM1MzM4Mzg0OTMw)",	
            "[<b>2. Sleep Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjIwNTM3MzYyNzM5ODU3)",	
            "[<b>3. Sexual Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjIxNTM5Mzg3MDk0Nzg0)",	
            "[<b>4. Personality Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjIyNTQxNDExNDQ5NzEx)",	
            "[<b>5. MCQ Discussion chapter 8 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjIzNTQzNDM1ODA0NjM4)",	
            "[<b>1. Mania and antimanic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjI0NTQ1NDYwMTU5NTY1)",	
            "[<b>2. Depression and antidepressants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjI1NTQ3NDg0NTE0NDky)",	
            "[<b>3. Bipolar disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjI2NTQ5NTA4ODY5NDE5)",	
            "[<b>4. Mcq Discussion Chapter 3 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjI3NTUxNTMzMjI0MzQ2)",	
            "[<b>1. Anxiety disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjI4NTUzNTU3NTc5Mjcz)",	
            "[<b>2. Ocd and related disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjI5NTU1NTgxOTM0MjAw)",	
            "[<b>3. Impulse control disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjMwNTU3NjA2Mjg5MTI3)",	
            "[<b>4. Trauma and stress related disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjMxNTU5NjMwNjQ0MDU0)",	
            "[<b>5. Somatoform disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjMyNTYxNjU0OTk4OTgx)",	
            "[<b>6. Conversion disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjMzNTYzNjc5MzUzOTA4)",	
            "[<b>7. Dissociative disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjM0NTY1NzAzNzA4ODM1)",	
            "[<b>8. Mcq Discussion Chapter 4 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjM1NTY3NzI4MDYzNzYy)",	
            "[<b>1. Delirium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjM2NTY5NzUyNDE4Njg5)",	
            "[<b>2. Dementia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjM3NTcxNzc2NzczNjE2)",	
            "[<b>3. Amnestic syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjM4NTczODAxMTI4NTQz)",	
            "[<b>4. MCQ Chapter 5 discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjM5NTc1ODI1NDgzNDcw)",	
            "[<b>1. Learning Models atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQwNTc3ODQ5ODM4Mzk3)",	
            "[<b>2. Psychosexual stages atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQxNTc5ODc0MTkzMzI0)",	
            "[<b>3. Models of mind and defense mechanisms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQyNTgxODk4NTQ4MjUx)",	
            "[<b>4. Psychotherapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQzNTgzOTIyOTAzMTc4)",	
            "[<b>5. Community Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQ0NTg1OTQ3MjU4MTA1)",	
            "[<b>6. MCQ discussion chapter 9 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQ1NTg3OTcxNjEzMDMy)",	
            "[<b>1 Schizophrenia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQ2NTg5OTk1OTY3OTU5)",	
            "[<b>2 Antipsychotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQ3NTkyMDIwMzIyODg2)",	
            "[<b>3 Delusional disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQ4NTk0MDQ0Njc3ODEz)",	
            "[<b>4. Mcq Discussion Chapter 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjQ5NTk2MDY5MDMyNzQw)",	
            "[<b>1. Deaddiction psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjUwNTk4MDkzMzg3NjY3)",	
            "[<b>2.Drugs used in deaddiction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjUxNjAwMTE3NzQyNTk0)",	
            "[<b>3. MCQ discussion chapter 6 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjUyNjAyMTQyMDk3NTIx)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psychiatrydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psychiatrydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psychiatrydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psychiatrydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("surgeryde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.Appendix atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjUzNjA0MTY2NDUyNDQ4)",
            "[<b>8.Bariatric surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjU0NjA2MTkwODA3Mzc1)",
            "[<b>1. Introduction and Anatomy of Urinary Bladder and Urethra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjU1NjA4MjE1MTYyMzAy)",
            "[<b>2. Bladder and Urethral Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjU2NjEwMjM5NTE3MjI5)",
            "[<b>3. Benign Disease Bladder and Urethra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjU3NjEyMjYzODcyMTU2)",
            "[<b>4.Bladder Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjU4NjE0Mjg4MjI3MDgz)",
            "[<b>1.Breast- Anatomy and Congenital disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjU5NjE2MzEyNTgyMDEw)",
            "[<b>2.Breast Cancer-Risk, Clinical features, Investigation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjYwNjE4MzM2OTM2OTM3)",
            "[<b>3. Breast cancer- Staging, Treatment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjYxNjIwMzYxMjkxODY0)",
            "[<b>4. Benign breast diseases, Breast examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjYyNjIyMzg1NjQ2Nzkx)",
            "[<b>1.Colo rectal cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjYzNjI0NDEwMDAxNzE4)",
            "[<b>1.Sigmoid volvulus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjY0NjI2NDM0MzU2NjQ1)",
            "[<b>2.Diverticulosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjY1NjI4NDU4NzExNTcy)",
            "[<b>3. Hirschsprung disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjY2NjMwNDgzMDY2NDk5)",
            "[<b>1.Thyroid-anatomy, congenital disorders, Neck dissection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjY3NjMyNTA3NDIxNDI2)",
            "[<b>2.Hypothyroidism STN atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjY4NjM0NTMxNzc2MzUz)",
            "[<b>3. Graves, Thyroiditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjY5NjM2NTU2MTMxMjgw)",
            "[<b>4. Thyroid Malingnancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjcwNjM4NTgwNDg2MjA3)",
            "[<b>5.Complication of thyroid surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjcxNjQwNjA0ODQxMTM0)",
            "[<b>6.Parathyroid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjcyNjQyNjI5MTk2MDYx)",
            "[<b>7.Adrenal, MEN atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjczNjQ0NjUzNTUwOTg4)",
            "[<b>1. Esophagus Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njc0NjQ2Njc3OTA1OTE1)",
            "[<b>2- Zenker dverticulum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njc1NjQ4NzAyMjYwODQy)",
            "[<b>3. Webs and Ring atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njc2NjUwNzI2NjE1NzY5)",
            "[<b>4.Tracheo esophageal fistula atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njc3NjUyNzUwOTcwNjk2)",
            "[<b>5. Esophagus perforation- Boerhaave syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njc4NjU0Nzc1MzI1NjIz)",
            "[<b>6. Achalasia Cardia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njc5NjU2Nzk5NjgwNTUw)",
            "[<b>7. Hiatus hernia and GERD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjgwNjU4ODI0MDM1NDc3)",
            "[<b>8. Esophagus - Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjgxNjYwODQ4MzkwNDA0)",
            "[<b>1.Biliary systemAnatomy and Congen atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjgyNjYyODcyNzQ1MzMx)",
            "[<b>2.Gall Bladder Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjgzNjY0ODk3MTAwMjU4)",
            "[<b>3.Bile Duct Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njg0NjY2OTIxNDU1MTg1)",
            "[<b>1.Trauma TriageATLS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njg1NjY4OTQ1ODEwMTEy)",
            "[<b>2.Trauma Scores atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njg2NjcwOTcwMTY1MDM5)",
            "[<b>3.Thoracic trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njg3NjcyOTk0NTE5OTY2)",
            "[<b>4.Abdominal Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njg4Njc1MDE4ODc0ODkz)",
            "[<b>5. Brain Trauma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njg5Njc3MDQzMjI5ODIw)",
            "[<b>6.Trauma Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjkwNjc5MDY3NTg0NzQ3)",
            "[<b>7. Burns atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjkxNjgxMDkxOTM5Njc0)",
            "[<b>1.HBP-Introduction and Liver Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjkyNjgzMTE2Mjk0NjAx)",
            "[<b>2.Liver Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NjkzNjg1MTQwNjQ5NTI4)",
            "[<b>3.Portal Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njk0Njg3MTY1MDA0NDU1)",
            "[<b>4.Liver Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njk1Njg5MTg5MzU5Mzgy)",
            "[<b>7.Hernia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njk2NjkxMjEzNzE0MzA5)",
            "[<b>1.Meckels Diverticulum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njk3NjkzMjM4MDY5MjM2)",
            "[<b>2.Intussusception atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njk4Njk1MjYyNDI0MTYz)",
            "[<b>3.Carcinoid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Njk5Njk3Mjg2Nzc5MDkw)",
            "[<b>4.Intestinal obstruction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzAwNjk5MzExMTM0MDE3)",
            "[<b>5.Celiac, Mesenteric cyst, Short bowel synd, Malrotation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzAxNzAxMzM1NDg4OTQ0)",
            "[<b>1 Anatomy of Upper Urinary Tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzAyNzAzMzU5ODQzODcx)",
            "[<b>2 Congenital Diseases of Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzAzNzA1Mzg0MTk4Nzk4)",
            "[<b>3. Benign Diseases of Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzA0NzA3NDA4NTUzNzI1)",
            "[<b>4 Renal and Ureteric stone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzA1NzA5NDMyOTA4NjUy)",
            "[<b>5 Renal Neoplasm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzA2NzExNDU3MjYzNTc5)",
            "[<b>1.Shock atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzA3NzEzNDgxNjE4NTA2)",
            "[<b>2.Transplant atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzA4NzE1NTA1OTczNDMz)",
            "[<b>3. Transplant Organ-Specific atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzA5NzE3NTMwMzI4MzYw)",
            "[<b>4. Sutures and suturing techniques atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzEwNzE5NTU0NjgzMjg3)",
            "[<b>5. Oral Cavity Cancer atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzExNzIxNTc5MDM4MjE0)",
            "[<b>6. Salivary glands & Neck swellings atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzEyNzIzNjAzMzkzMTQx)",
            "[<b>7. Basics of laparoscopy energy sources surgical nutrition atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzEzNzI1NjI3NzQ4MDY4)",
            "[<b>8.Infections, Ulcer,Swelling, Drains, Instruments, Incision, Instruments atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzE0NzI3NjUyMTAyOTk1)",
            "[<b>1.Pancreas Anatomy & Congenital Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzE1NzI5Njc2NDU3OTIy)",
            "[<b>2.Acute Pancreatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzE2NzMxNzAwODEyODQ5)",
            "[<b>3.Chronic pancreatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzE3NzMzNzI1MTY3Nzc2)",
            "[<b>4.Pancreatic malignancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzE4NzM1NzQ5NTIyNzAz)",
            "[<b>1. Skin grafts & flaps atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzE5NzM3NzczODc3NjMw)",
            "[<b>2. Cleft Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzIwNzM5Nzk4MjMyNTU3)",
            "[<b>3. Skin Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzIxNzQxODIyNTg3NDg0)",
            "[<b>4.Wound Healing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzIyNzQzODQ2OTQyNDEx)",
            "[<b>1.Introduction and Prostate Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzIzNzQ1ODcxMjk3MzM4)",
            "[<b>2.Benign Prostate Hypertrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzI0NzQ3ODk1NjUyMjY1)",
            "[<b>3.Carcinoma Prostate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzI1NzQ5OTIwMDA3MTky)",
            "[<b>1.Piles Fissure Fistula piloniodal sinus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzI2NzUxOTQ0MzYyMTE5)",
            "[<b>2.Rectal prolapse and SRUS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzI3NzUzOTY4NzE3MDQ2)",
            "[<b>1. Stomach- CHPS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzI4NzU1OTkzMDcxOTcz)",
            "[<b>2. Stomach- Menetriers, Volvulus, Bezoar atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzI5NzU4MDE3NDI2OTAw)",
            "[<b>3. Acid Peptic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzMwNzYwMDQxNzgxODI3)",
            "[<b>4. Gastirc Cancer and GIST atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzMxNzYyMDY2MTM2NzU0)",
            "[<b>5.DUODENUM- Atresia, SMA syndrome, ipsid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzMyNzY0MDkwNDkxNjgx)",
            "[<b>1. Kidney & Ureter-Anatomy & Congenital disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzMzNzY2MTE0ODQ2NjA4)",
            "[<b>2. Benign Disorders of Kidney, Ureter atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzM0NzY4MTM5MjAxNTM1)",
            "[<b>3. Renal Tumors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzM1NzcwMTYzNTU2NDYy)",
            "[<b>4. Urinary Bladder- Anatomy Neurogenic Bladder, congenital disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzM2NzcyMTg3OTExMzg5)",
            "[<b>5. Urinary Bladder- Stone, VUR, Infection, Tumours atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzM3Nzc0MjEyMjY2MzE2)",
            "[<b>6. Prostate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzM4Nzc2MjM2NjIxMjQz)",
            "[<b>7. Urethra & Penis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzM5Nzc4MjYwOTc2MTcw)",
            "[<b>8. Testis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQwNzgwMjg1MzMxMDk3)",
            "[<b>1.Venous Anatomy Varicose Vein atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQxNzgyMzA5Njg2MDI0)",
            "[<b>2.Deep Vein Thrombosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQyNzg0MzM0MDQwOTUx)",
            "[<b>3. Arterial Occlusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQzNzg2MzU4Mzk1ODc4)",
            "[<b>4. Aneurysm, AV Fistula,TOS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQ0Nzg4MzgyNzUwODA1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        surgeryde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"surgeryde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"surgeryde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(surgeryde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("psmde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Topic 0 How to Approach Statistics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQ1NzkwNDA3MTA1NzMy)",	
            "[<b>Topic 1 Measure of Central Tendency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQ2NzkyNDMxNDYwNjU5)",	
            "[<b>Topic 2 Measure of Dispersion of Data atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQ3Nzk0NDU1ODE1NTg2)",	
            "[<b>Topic 3 Distribution of Data atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQ4Nzk2NDgwMTcwNTEz)",	
            "[<b>Topic 4 Variable and Scales of Measurement atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzQ5Nzk4NTA0NTI1NDQw)",	
            "[<b>Topic 5 A Graphical Representation of Data atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzUwODAwNTI4ODgwMzY3)",	
            "[<b>Topic 5 B Scatter Diagram atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzUxODAyNTUzMjM1Mjk0)",	
            "[<b>Topic 5 C Miscellaneous Diagrams atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzUyODA0NTc3NTkwMjIx)",	
            "[<b>Topic 6 Probability atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzUzODA2NjAxOTQ1MTQ4)",	
            "[<b>Topic 7 A Sample size atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzU0ODA4NjI2MzAwMDc1)",	
            "[<b>Topic 7 B Sampling atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzU1ODEwNjUwNjU1MDAy)",	
            "[<b>Topic 7 C Sampling atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzU2ODEyNjc1MDA5OTI5)",	
            "[<b>Topic 8 Confidence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzU3ODE0Njk5MzY0ODU2)",	
            "[<b>Topic 9 Statistical Tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzU4ODE2NzIzNzE5Nzgz)",	
            "[<b>Topic 10 Hypothesis Testing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzU5ODE4NzQ4MDc0NzEw)",	
            "[<b>Rabies and Animal Bite Wound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzYwODIwNzcyNDI5NjM3)",	
            "[<b>HIV atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzYxODIyNzk2Nzg0NTY0)",	
            "[<b>Vector borne diseases and NBVDCP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzYyODI0ODIxMTM5NDkx)",	
            "[<b>Yellow Fever atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzYzODI2ODQ1NDk0NDE4)",	
            "[<b>1 Concepts of Health and Disease Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzY0ODI4ODY5ODQ5MzQ1)",	
            "[<b>2 Concepts of Health and Disease Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzY1ODMwODk0MjA0Mjcy)",	
            "[<b>1.Biomedical Medical Waste atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzY2ODMyOTE4NTU5MTk5)",	
            "[<b>1.Occupational Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzY3ODM0OTQyOTE0MTI2)",	
            "[<b>1.Disaster Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzY4ODM2OTY3MjY5MDUz)",	
            "[<b>1.Heatlh Care System in India atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzY5ODM4OTkxNjIzOTgw)",	
            "[<b>Environnent atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzcwODQxMDE1OTc4OTA3)",	
            "[<b>Entomology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzcxODQzMDQwMzMzODM0)",	
            "[<b>Sociology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzcyODQ1MDY0Njg4NzYx)",	
            "[<b>TB and NTEP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzczODQ3MDg5MDQzNjg4)",	
            "[<b>1.Biostats atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzc0ODQ5MTEzMzk4NjE1)",	
            "[<b>2.Standard Error atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzc1ODUxMTM3NzUzNTQy)",	
            "[<b>1. Vaccine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzc2ODUzMTYyMTA4NDY5)",	
            "[<b>2.Cold Chain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzc3ODU1MTg2NDYzMzk2)",	
            "[<b>1 Measurment in Epidemiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzc4ODU3MjEwODE4MzIz)",	
            "[<b>2 Study Design atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzc5ODU5MjM1MTczMjUw)",	
            "[<b>3 Case control and Cohort Study atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzgwODYxMjU5NTI4MTc3)",	
            "[<b>4 Experimental studies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzgxODYzMjgzODgzMTA0)",	
            "[<b>5 EBM & MIsc atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzgyODY1MzA4MjM4MDMx)",	
            "[<b>1 Screening part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzgzODY3MzMyNTkyOTU4)",	
            "[<b>2 Screening part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzg0ODY5MzU2OTQ3ODg1)",	
            "[<b>1 Demography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzg1ODcxMzgxMzAyODEy)",	
            "[<b>2 Family planning atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzg2ODczNDA1NjU3NzM5)",	
            "[<b>1.NCD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzg3ODc1NDMwMDEyNjY2)",	
            "[<b>1 MCH atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzg4ODc3NDU0MzY3NTkz)",	
            "[<b>1 Health Programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzg5ODc5NDc4NzIyNTIw)",	
            "[<b>1 Nutritions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzkwODgxNTAzMDc3NDQ3)",	
            "[<b>MCQ Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzkxODgzNTI3NDMyMzc0)",	
            "[<b>Topic 1 Basic terminolgies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzkyODg1NTUxNzg3MzAx)",	
            "[<b>Topic 2 Morbidity and Mortality Indicators atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0NzkzODg3NTc2MTQyMjI4)",	
            "[<b>Topic 3 Classification of Study Designs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzk0ODg5NjAwNDk3MTU1)",	
            "[<b>Topic 4 Master Study Design atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzk1ODkxNjI0ODUyMDgy)",	
            "[<b>Topic 5 Types of Cohort part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzk2ODkzNjQ5MjA3MDA5)",	
            "[<b>Topic 6 Doll and Hill Criteria of Causality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzk3ODk1NjczNTYxOTM2)",	
            "[<b>Topic 7 Systematic Review and Meta analysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzk4ODk3Njk3OTE2ODYz)",	
            "[<b>Topic 8 Advanced Cohort atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0Nzk5ODk5NzIyMjcxNzkw)",	
            "[<b>Topic 9 Case Crossover atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODAwOTAxNzQ2NjI2NzE3)",	
            "[<b>Topic 10 Equivalence Margin graph atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODAxOTAzNzcwOTgxNjQ0)",	
            "[<b>MDG to SDG & Counterfeit medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODAyOTA1Nzk1MzM2NTcx)",	
            "[<b>Topic 1 Introduction to health programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODAzOTA3ODE5NjkxNDk4)",	
            "[<b>Topic 2 M Maternal Health Programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODA0OTA5ODQ0MDQ2NDI1)",	
            "[<b>Topic 3 NCh Neonatal and Child health Programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODA1OTExODY4NDAxMzUy)",	
            "[<b>Topic 4 Adolescent Programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODA2OTEzODkyNzU2Mjc5)",	
            "[<b>Topic 5 Summary of RMNCHA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODA3OTE1OTE3MTExMjA2)",	
            "[<b>Topic 6 NCD Programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODA4OTE3OTQxNDY2MTMz)",	
            "[<b>Topic 7 Nutrition programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODA5OTE5OTY1ODIxMDYw)",	
            "[<b>Topic 8 Mixed bag Programs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODEwOTIxOTkwMTc1OTg3)",	
            "[<b>Topic 9 Ayushmann Bharat atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODExOTI0MDE0NTMwOTE0)",	
            "[<b>Topic 10 IDSP IHIP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODEyOTI2MDM4ODg1ODQx)",	
            "[<b>Part 0 How to approach PSM atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODEzOTI4MDYzMjQwNzY4)",	
            "[<b>Image Question Bank atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODE0OTMwMDg3NTk1Njk1)",	
            "[<b>Chapter2 Health and Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODE1OTMyMTExOTUwNjIy)",	
            "[<b>Chapter 5 Topic 1 Water atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODE2OTM0MTM2MzA1NTQ5)",	
            "[<b>Chapter 5 Topic 2 Air atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODE3OTM2MTYwNjYwNDc2)",	
            "[<b>Chapter 5 Topic 3 Entomology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODE4OTM4MTg1MDE1NDAz)",	
            "[<b>Chapter 6 Non communicable diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODE5OTQwMjA5MzcwMzMw)",	
            "[<b>Chapter 10 Demography and Family Planning atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODIwOTQyMjMzNzI1MjU3)",	
            "[<b>Chapter 11 Topic 1 Preventive Obstetrics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODIxOTQ0MjU4MDgwMTg0)",	
            "[<b>Chapter 11 Topic 2 Preventive Paediatrics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODIyOTQ2MjgyNDM1MTEx)",	
            "[<b>Chapter 16 Hospital Waste Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODIzOTQ4MzA2NzkwMDM4)",	
            "[<b>Chapter 23 Health Planning and Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODI0OTUwMzMxMTQ0OTY1)",	
            "[<b>Chapter 24 Health Care of Community atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODI1OTUyMzU1NDk5ODky)",	
            "[<b>Nutrition atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODI2OTU0Mzc5ODU0ODE5)",	
            "[<b>Trible Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODI3OTU2NDA0MjA5NzQ2)",	
            "[<b>Chapter 5 Topic 1 Basics of Infectious Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODI4OTU4NDI4NTY0Njcz)",	
            "[<b>Chapter 5 Topic 3 Vaccination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODI5OTYwNDUyOTE5NjAw)",	
            "[<b>Chapter 5 Topic 4 Polio atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODMwOTYyNDc3Mjc0NTI3)",	
            "[<b>Chapter 5 Topic 5 HIV atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODMxOTY0NTAxNjI5NDU0)",	
            "[<b>Chapter 5 Topic 6 TB atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODMyOTY2NTI1OTg0Mzgx)",	
            "[<b>Chapter 5 Topic 7 NVBDCP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODMzOTY4NTUwMzM5MzA4)",	
            "[<b>Chapter 5 Topic 8 Yellow Fever atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODM0OTcwNTc0Njk0MjM1)",	
            "[<b>Chapter 5 Topic 9 Tetanus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODM1OTcyNTk5MDQ5MTYy)",	
            "[<b>Chapter 5 Topic 10 Rabies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODM2OTc0NjIzNDA0MDg5)",	
            "[<b>Chapter 5 Topic 11 GI Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODM3OTc2NjQ3NzU5MDE2)",	
            "[<b>Topic 2 Respiratory Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODM4OTc4NjcyMTEzOTQz)",	
            "[<b>Waste Management MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODM5OTgwNjk2NDY4ODcw)",	
            "[<b>Disaster Management MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQwOTgyNzIwODIzNzk3)",	
            "[<b>Environment MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQxOTg0NzQ1MTc4NzI0)",	
            "[<b>Epidemiology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQyOTg2NzY5NTMzNjUx)",	
            "[<b>Epidemiology MCQ(1) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQzOTg4NzkzODg4NTc4)",	
            "[<b>Health Planning and Management MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQ0OTkwODE4MjQzNTA1)",	
            "[<b>Health Programs MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQ1OTkyODQyNTk4NDMy)",	
            "[<b>Health care of community MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQ2OTk0ODY2OTUzMzU5)",	
            "[<b>Infectious Disease MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQ3OTk2ODkxMzA4Mjg2)",	
            "[<b>Nutrition MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODQ4OTk4OTE1NjYzMjEz)",	
            "[<b>Occupational Health MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODUwMDAwOTQwMDE4MTQw)",	
            "[<b>Preventive Obstetirics and Paediatrics MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODUxMDAyOTY0MzczMDY3)",	
            "[<b>Screening of Disease MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODUyMDA0OTg4NzI3OTk0)",	
            "[<b>Sociology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODUzMDA3MDEzMDgyOTIx)",	
            "[<b>Statistics MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODU0MDA5MDM3NDM3ODQ4)",	
            "[<b>PSM June Updates 2023 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODU1MDExMDYxNzkyNzc1)",	
            "[<b>PSM May Updates 2023 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODU2MDEzMDg2MTQ3NzAy)",	
            "[<b>Updates April 2023 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODU3MDE1MTEwNTAyNjI5)",	
            "[<b>Mental Health & Genetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODU4MDE3MTM0ODU3NTU2)",	
            "[<b>Topic 1 2 by 2 Table Screening of Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODU5MDE5MTU5MjEyNDgz)",	
            "[<b>Topic 2 Interpretation of Screening of Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODYwMDIxMTgzNTY3NDEw)",	
            "[<b>Topic 3 Time in Screening of Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODYxMDIzMjA3OTIyMzM3)",	
            "[<b>Topic 4 Principles of Screening of Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODYyMDI1MjMyMjc3MjY0)",	
            "[<b>Topic 5 Cutoffs in Screening of Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODYzMDI3MjU2NjMyMTkx)",	
            "[<b>Chapter 13 Sociology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODY0MDI5MjgwOTg3MTE4)",	
            "[<b>Chapter 17 Disaster atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODY1MDMxMzA1MzQyMDQ1)",	
            "[<b>Chapter 18 Occupational Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODY2MDMzMzI5Njk2OTcy)",	
            "[<b>Chapter 22 Communication atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODY3MDM1MzU0MDUxODk5)",	
            "[<b>Chapter 25 International Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODY4MDM3Mzc4NDA2ODI2)",	
            "[<b>Trible Health atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0ODY5MDM5NDAyNzYxNzUz)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        psmde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"psmde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"psmde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(psmde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("radiologydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. CT Scan Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTEyMTI2NDUwMDIzNjE0)",
            "[<b>10. PET, Radiotherapy, Nuclear Scan atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTEzMTI4NDc0Mzc4NTQx)",
            "[<b>11. Post Class Test atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTE0MTMwNDk4NzMzNDY4)",
            "[<b>2. MRI Applications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTE1MTMyNTIzMDg4Mzk1)",
            "[<b>3. Neuroimaging atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTE2MTM0NTQ3NDQzMzIy)",
            "[<b>4. CXR Basics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTE3MTM2NTcxNzk4MjQ5)",
            "[<b>5. Chest disease and CVS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTE4MTM4NTk2MTUzMTc2)",
            "[<b>6. Bone Tumour atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTE5MTQwNjIwNTA4MTAz)",
            "[<b>7. Orthopedics,USG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTIwMTQyNjQ0ODYzMDMw)",
            "[<b>8. IVP,Barium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTIxMTQ0NjY5MjE3OTU3)",
            "[<b>9. CT abdomen, Mammography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTIyMTQ2NjkzNTcyODg0)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        radiologydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"radiologydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"radiologydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(radiologydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pharmacologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>2.1 Cholinergic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTIzMTQ4NzE3OTI3ODEx)",
            "[<b>2.3 Adrenergic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTI0MTUwNzQyMjgyNzM4)",
            "[<b>2.4 Alpha blockers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTI1MTUyNzY2NjM3NjY1)",
            "[<b>2.5 Beta blockers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTI2MTU0NzkwOTkyNTky)",
            "[<b>2. 2 Anti cholinergic Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTI3MTU2ODE1MzQ3NTE5)",
            "[<b>2. 6 Sympatholytic - MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTI4MTU4ODM5NzAyNDQ2)",
            "[<b>Adrenergic MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTI5MTYwODY0MDU3Mzcz)",
            "[<b>Cholinergic mcq atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTMwMTYyODg4NDEyMzAw)",
            "[<b>8.1. General Anaesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTMxMTY0OTEyNzY3MjI3)",
            "[<b>8.2. Local Anaesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTMyMTY2OTM3MTIyMTU0)",
            "[<b>8.3. Skeletal muscle relaxants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTMzMTY4OTYxNDc3MDgx)",
            "[<b>Anesthesia MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTM0MTcwOTg1ODMyMDA4)",
            "[<b>13.Anti cancer drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTM1MTczMDEwMTg2OTM1)",
            "[<b>Anticancer drugs- MCQs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTM2MTc1MDM0NTQxODYy)",
            "[<b>12.1. Antimicrobial drugs general considerations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTM3MTc3MDU4ODk2Nzg5)",
            "[<b>12.2. Beta lactam antibiotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTM4MTc5MDgzMjUxNzE2)",
            "[<b>12.3. Macrolide mrsa vrsa . miscellaneous & utility atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTM5MTgxMTA3NjA2NjQz)",
            "[<b>12.4 Sulfonamides, Quinolones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQwMTgzMTMxOTYxNTcw)",
            "[<b>12.5 Aminoglycosides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQxMTg1MTU2MzE2NDk3)",
            "[<b>12.6 Tetracycline and chloramphenicol atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQyMTg3MTgwNjcxNDI0)",
            "[<b>12.7. Anti TB drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQzMTg5MjA1MDI2MzUx)",
            "[<b>12.8 Drugs for leprosy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQ0MTkxMjI5MzgxMjc4)",
            "[<b>12.9. Antifungal agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQ1MTkzMjUzNzM2MjA1)",
            "[<b>12.10. Antimalarial drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQ2MTk1Mjc4MDkxMTMy)",
            "[<b>12.11 Antiretroviral drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQ3MTk3MzAyNDQ2MDU5)",
            "[<b>12.12 Non retroviral drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQ4MTk5MzI2ODAwOTg2)",
            "[<b>12.13 Anti amoebic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTQ5MjAxMzUxMTU1OTEz)",
            "[<b>12.14 Anti helminthic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTUwMjAzMzc1NTEwODQw)",
            "[<b>ANTIMICROBIAL MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTUxMjA1Mzk5ODY1NzY3)",
            "[<b>6.1 Anti histamines atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTUyMjA3NDI0MjIwNjk0)",
            "[<b>6.3. PG analogues and leukotriene modifiers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTUzMjA5NDQ4NTc1NjIx)",
            "[<b>6.5 drugs for rheumatoid arthritis and for gout arthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTU0MjExNDcyOTMwNTQ4)",
            "[<b>6. 2 Serotonin receptor modulators and drugs for migraine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTU1MjEzNDk3Mjg1NDc1)",
            "[<b>6.4. Non steroidal antiinflammatory drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTU2MjE1NTIxNjQwNDAy)",
            "[<b>Autocoid mcq atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTU3MjE3NTQ1OTk1MzI5)",
            "[<b>4.1.Thrombholytics, anticoagulants and antiplatelet drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTU4MjE5NTcwMzUwMjU2)",
            "[<b>4.2 Hypolipidaemic Drug atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTU5MjIxNTk0NzA1MTgz)",
            "[<b>7.1 Sedative and hypnotic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTYwMjIzNjE5MDYwMTEw)",
            "[<b>7.2.Anti epileptic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTYxMjI1NjQzNDE1MDM3)",
            "[<b>7.3. Drugs for parkinson disease & other movement disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTYyMjI3NjY3NzY5OTY0)",
            "[<b>7.4 Antipsychotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTYzMjI5NjkyMTI0ODkx)",
            "[<b>7.5 Antidepressants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTY0MjMxNzE2NDc5ODE4)",
            "[<b>7.6 Bipolar disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTY1MjMzNzQwODM0NzQ1)",
            "[<b>7.7 Opioid analgesics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTY2MjM1NzY1MTg5Njcy)",
            "[<b>7.8. ALCOHOL atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTY3MjM3Nzg5NTQ0NTk5)",
            "[<b>CNS MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTY4MjM5ODEzODk5NTI2)",
            "[<b>3.1 Antianginal and other anti ischemic drugs. atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTY5MjQxODM4MjU0NDUz)",
            "[<b>3.2 Anti Arrhythmic Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTcwMjQzODYyNjA5Mzgw)",
            "[<b>3.3 Cardiac Glycosides and Drugs for Heart Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTcxMjQ1ODg2OTY0MzA3)",
            "[<b>3.4 Antihypertensive Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTcyMjQ3OTExMzE5MjM0)",
            "[<b>9.1 Introduction and anti pituitary hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTczMjQ5OTM1Njc0MTYx)",
            "[<b>9.2 Anti thyroid drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTc0MjUxOTYwMDI5MDg4)",
            "[<b>9.3 Anti diabetic drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTc1MjUzOTg0Mzg0MDE1)",
            "[<b>9.4 Steroids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTc2MjU2MDA4NzM4OTQy)",
            "[<b>9.5 Female sex hormone atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTc3MjU4MDMzMDkzODY5)",
            "[<b>9.6 Drugs acting on uterus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTc4MjYwMDU3NDQ4Nzk2)",
            "[<b>9.7 Male sex hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTc5MjYyMDgxODAzNzIz)",
            "[<b>9.8 Calcium vit D. osteoporosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTgwMjY0MTA2MTU4NjUw)",
            "[<b>Endo MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTgxMjY2MTMwNTEzNTc3)",
            "[<b>10.1 Acid Peptic Disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTgyMjY4MTU0ODY4NTA0)",
            "[<b>10.2 Antiemetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTgzMjcwMTc5MjIzNDMx)",
            "[<b>10.3.IBD and IBS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTg0MjcyMjAzNTc4MzU4)",
            "[<b>GIT MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTg1Mjc0MjI3OTMzMjg1)",
            "[<b>1.1 Pharmacokinetic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTg2Mjc2MjUyMjg4MjEy)",
            "[<b>1.2 Pharmacodyanamic atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTg3Mjc4Mjc2NjQzMTM5)",
            "[<b>1.3 Adverse drug reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTg4MjgwMzAwOTk4MDY2)",
            "[<b>General Pharmacology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTg5MjgyMzI1MzUyOTkz)",
            "[<b>14.2. Monoclonal antibodies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTkwMjg0MzQ5NzA3OTIw)",
            "[<b>14.3. Tyrosine kinase inhibitors drugs & Other small molecule inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTkxMjg2Mzc0MDYyODQ3)",
            "[<b>14.Immunomodulators atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTkyMjg4Mzk4NDE3Nzc0)",
            "[<b>Immunosuppressants- MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTkzMjkwNDIyNzcyNzAx)",
            "[<b>5.1.Diuretics & Anti Diuretics drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTk0MjkyNDQ3MTI3NjI4)",
            "[<b>15.1.Drugs for glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTk1Mjk0NDcxNDgyNTU1)",
            "[<b>15.2. Chelating agents atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTk2Mjk2NDk1ODM3NDgy)",
            "[<b>15.3. Drug therapy for obesity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTk3Mjk4NTIwMTkyNDA5)",
            "[<b>15.4 Anti smoking drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTk4MzAwNTQ0NTQ3MzM2)",
            "[<b>Miscellaneous MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE0OTk5MzAyNTY4OTAyMjYz)",
            "[<b>11 Bronchial asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDAwMzA0NTkzMjU3MTkw)",
            "[<b>Respiratory System MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDAxMzA2NjE3NjEyMTE3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pharmacologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pharmacologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pharmacologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pharmacologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("physiologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Impulse Conduction Pathway, Time of Arrival of Impulse, Plateau potential & Pacemaker Potential. atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDAyMzA4NjQxOTY3MDQ0)",
            "[<b>2.Hemodynamics & Functional Classification of vascular system atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDAzMzEwNjY2MzIxOTcx)",
            "[<b>3. Cardiac cycle atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDA0MzEyNjkwNjc2ODk4)",
            "[<b>4.Cardiac output atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDA1MzE0NzE1MDMxODI1)",
            "[<b>5. Regulation of blood pressure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDA2MzE2NzM5Mzg2NzUy)",
            "[<b>1. Sensory System- Classification of Receptors, Laws of Sensory Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDA3MzE4NzYzNzQxNjc5)",
            "[<b>2. Laws of Sensory Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDA4MzIwNzg4MDk2NjA2)",
            "[<b>3. Sensory Tracts and Pain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDA5MzIyODEyNDUxNTMz)",
            "[<b>4. Gate Control Theory of Pain and Supraspinal Control of pain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDEwMzI0ODM2ODA2NDYw)",
            "[<b>5. Motor Descending Tracts Cortico spinal tract and Reflexes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDExMzI2ODYxMTYxMzg3)",
            "[<b>7. Thalamus & Hypothalamus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDEyMzI4ODg1NTE2MzE0)",
            "[<b>6. Cerebellum & Basal Ganglia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDEzMzMwOTA5ODcxMjQx)",
            "[<b>1. Intoduction to hormones, IInd messengers & Hypothalamic and Pituitary hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDE0MzMyOTM0MjI2MTY4)",
            "[<b>2. Adrenal gland, Pancreas, Thyroid gland & Calcium metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDE1MzM0OTU4NTgxMDk1)",
            "[<b>1. BER, Mechanism of contraction of smooth muscle, GIT hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDE2MzM2OTgyOTM2MDIy)",
            "[<b>2. Git secretions and git motility, git reflexes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDE3MzM5MDA3MjkwOTQ5)",
            "[<b>1.Body Fluids & Basic Concepts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDE4MzQxMDMxNjQ1ODc2)",
            "[<b>2.Darrow Yannet Diagram & Starling Forces atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDE5MzQzMDU2MDAwODAz)",
            "[<b>3.Transport across cell membrane atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDIwMzQ1MDgwMzU1NzMw)",
            "[<b>4.Cell Membrane & Intercellular Junctions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDIxMzQ3MTA0NzEwNjU3)",
            "[<b>5.Positive & Negative Feed back systems & Gibbs Donnan Equilibrium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDIyMzQ5MTI5MDY1NTg0)",
            "[<b>1. Neuromuscular Junction, Structure of Sliding Filament theory atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDIzMzUxMTUzNDIwNTEx)",
            "[<b>2. Isometric & Isotonic contraction, Types of training atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDI0MzUzMTc3Nzc1NDM4)",
            "[<b>1.Neuron structure types & Axoplasmic transport atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDI1MzU1MjAyMTMwMzY1)",
            "[<b>2.RMP , Nernst Potential & Goldmann Hodgkin katz Equation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDI2MzU3MjI2NDg1Mjky)",
            "[<b>3.Local Potential & Action Potential atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDI3MzU5MjUwODQwMjE5)",
            "[<b>4. Strength Duration Curve atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDI4MzYxMjc1MTk1MTQ2)",
            "[<b>5. Myelination on Nerve Impulse Inbition in CNS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDI5MzYzMjk5NTUwMDcz)",
            "[<b>1. Renal Physiology & Glomerular Filtration Barrier atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDMwMzY1MzIzOTA1MDAw)",
            "[<b>2.GFR, NFP and Effect of various factors on GFR atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDMxMzY3MzQ4MjU5OTI3)",
            "[<b>3. Autoregulation of GFR and Mechanisms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDMyMzY5MzcyNjE0ODU0)",
            "[<b>4. Renal Handling of Various Substances by Kidney atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDMzMzcxMzk2OTY5Nzgx)",
            "[<b>5.Clearance and Free water clearance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDM0MzczNDIxMzI0NzA4)",
            "[<b>6.Renal Handling of Na+, K+, Glucose and Water atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDM1Mzc1NDQ1Njc5NjM1)",
            "[<b>7.Acid Secretion Counter Current Systems atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDM2Mzc3NDcwMDM0NTYy)",
            "[<b>1. Introduction, vq line , pressures in lung, compliance & surfactant ,vq ratio atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDM3Mzc5NDk0Mzg5NDg5)",
            "[<b>2.Gas exchange, perfusion limited & diffusion limited gases & transport of o2 & co2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDM4MzgxNTE4NzQ0NDE2)",
            "[<b>3.Tidal volumes & capacities , flow volume loops & airway resistance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDM5MzgzNTQzMDk5MzQz)",
            "[<b>4. Regulation of respiration - Neural & Chemical control, Zones of flow in lung atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQwMzg1NTY3NDU0Mjcw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        physiologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"physiologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"physiologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(physiologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("anatomyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>8.1 Anterior Abdominal Wall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQxMzg3NTkxODA5MTk3)",
            "[<b>8.2 Posterior Abdominal Wall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQyMzg5NjE2MTY0MTI0)",
            "[<b>8.3 Peritoneum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQzMzkxNjQwNTE5MDUx)",
            "[<b>8.4 Viscera atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQ0MzkzNjY0ODczOTc4)",
            "[<b>8.5 Perineum and Development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQ1Mzk1Njg5MjI4OTA1)",
            "[<b>8.7.Abdomen MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQ2Mzk3NzEzNTgzODMy)",
            "[<b>1.1.GENERAL ANATOMY MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQ3Mzk5NzM3OTM4NzU5)",
            "[<b>1.General Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQ4NDAxNzYyMjkzNjg2)",
            "[<b>4.1 Gametogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDQ5NDAzNzg2NjQ4NjEz)",
            "[<b>4.2 Gastrulation and further Development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDUwNDA1ODExMDAzNTQw)",
            "[<b>4.3.General Embryo MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDUxNDA3ODM1MzU4NDY3)",
            "[<b>2.1 Foramen of skull atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDUyNDA5ODU5NzEzMzk0)",
            "[<b>2.2 Cranial Nerves atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDUzNDExODg0MDY4MzIx)",
            "[<b>2.3 Dural Venous Sinus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDU0NDEzOTA4NDIzMjQ4)",
            "[<b>2.4 Deep Cervical Fascia and Neck Triangles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDU1NDE1OTMyNzc4MTc1)",
            "[<b>2.5 Arteries of Head and Neck and TMJ joint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDU2NDE3OTU3MTMzMTAy)",
            "[<b>2.6.HEAD AND NECK MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDU3NDE5OTgxNDg4MDI5)",
            "[<b>9 Histo atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDU4NDIyMDA1ODQyOTU2)",
            "[<b>9.1.HISTO MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDU5NDI0MDMwMTk3ODgz)",
            "[<b>7.1 Front and Medial thigh atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDYwNDI2MDU0NTUyODEw)",
            "[<b>7.2 Gluteal region and Hamstring Muscles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDYxNDI4MDc4OTA3NzM3)",
            "[<b>7.3 Popliteal fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDYyNDMwMTAzMjYyNjY0)",
            "[<b>7.4 Leg & Foot atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDYzNDMyMTI3NjE3NTkx)",
            "[<b>7.5 Knee, Ankle, Superficial Veins and lymphatics of lower limb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDY0NDM0MTUxOTcyNTE4)",
            "[<b>7.6.LOWER LIMB MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDY1NDM2MTc2MzI3NDQ1)",
            "[<b>3.1 CNS Development and Spinal cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDY2NDM4MjAwNjgyMzcy)",
            "[<b>3.2 Brain Stem atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDY3NDQwMjI1MDM3Mjk5)",
            "[<b>3.3 Cerebellum ,Basal Nuclei, Internal Capsule atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDY4NDQyMjQ5MzkyMjI2)",
            "[<b>3.4 Diencephalon and Ventricles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDY5NDQ0MjczNzQ3MTUz)",
            "[<b>3.5 Cerebrum and Blood supply atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDcwNDQ2Mjk4MTAyMDgw)",
            "[<b>3.6.NEURO ANATOMY MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDcxNDQ4MzIyNDU3MDA3)",
            "[<b>5.1 Intercostal spaces, Diaphragm, Mediastinum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDcyNDUwMzQ2ODExOTM0)",
            "[<b>5.2 Lung, Pleura and Pericardium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDczNDUyMzcxMTY2ODYx)",
            "[<b>5.3 Heart and Development of CVS Final atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDc0NDU0Mzk1NTIxNzg4)",
            "[<b>5.4.THROAX MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDc1NDU2NDE5ODc2NzE1)",
            "[<b>6.1 Axilla atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDc2NDU4NDQ0MjMxNjQy)",
            "[<b>6.2 Pectoral, Deltoid & Scapular region atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDc3NDYwNDY4NTg2NTY5)",
            "[<b>6.3 Arm & Cubital Fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDc4NDYyNDkyOTQxNDk2)",
            "[<b>6.4 Forearm, Snuff box & Carpal tunnel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDc5NDY0NTE3Mjk2NDIz)",
            "[<b>6.5 Palm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDgwNDY2NTQxNjUxMzUw)",
            "[<b>6.6 Radial N. , Median N & Ulnar N atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDgxNDY4NTY2MDA2Mjc3)",
            "[<b>6.7.UPPER LIMB MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDgyNDcwNTkwMzYxMjA0)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anatomyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anatomyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anatomyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anatomyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("fmtdh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>8. Acts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDgzNDcyNjE0NzE2MTMx)",
            "[<b>3. Near point concept and Presbyopia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDg0NDc0NjM5MDcxMDU4)",
            "[<b>11.Asphyxia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDg1NDc2NjYzNDI1OTg1)",
            "[<b>3.1 Consent Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDg2NDc4Njg3NzgwOTEy)",
            "[<b>3.Consent atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDg3NDgwNzEyMTM1ODM5)",
            "[<b>10.1 Forensic Ballistics MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDg4NDgyNzM2NDkwNzY2)",
            "[<b>10. Forensic Ballistics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDg5NDg0NzYwODQ1Njkz)",
            "[<b>6.1 Identification MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDkwNDg2Nzg1MjAwNjIw)",
            "[<b>6.Identification atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDkxNDg4ODA5NTU1NTQ3)",
            "[<b>13.1 Impotance and Sterilite Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDkyNDkwODMzOTEwNDc0)",
            "[<b>13. Impotance and Sterilite atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDkzNDkyODU4MjY1NDAx)",
            "[<b>1 Introduction to Forensic Medicine and Ethics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDk0NDk0ODgyNjIwMzI4)",
            "[<b>1.1 Introduction to Forensic Medicine and Ethics Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDk1NDk2OTA2OTc1MjU1)",
            "[<b>5. IPC Sections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDk2NDk4OTMxMzMwMTgy)",
            "[<b>5.1 IPC QUESTIONS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDk3NTAwOTU1Njg1MTA5)",
            "[<b>2 Legal Procedures atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDk4NTAyOTgwMDQwMDM2)",
            "[<b>2.1 Legal Procedures Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MDk5NTA1MDA0Mzk0OTYz)",
            "[<b>9.1 Mechanical Injuries MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTAwNTA3MDI4NzQ5ODkw)",
            "[<b>9.Mechanical Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTAxNTA5MDUzMTA0ODE3)",
            "[<b>4. 1 Negligence MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTAyNTExMDc3NDU5NzQ0)",
            "[<b>4.Negligence atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTAzNTEzMTAxODE0Njcx)",
            "[<b>14.1 Autopsy Infanticide Stain Question atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTA0NTE1MTI2MTY5NTk4)",
            "[<b>14.Autopsy Infanticide Stain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTA1NTE3MTUwNTI0NTI1)",
            "[<b>7.1 Thanatology Question atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTA2NTE5MTc0ODc5NDUy)",
            "[<b>7.Thanatology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTA3NTIxMTk5MjM0Mzc5)",
            "[<b>12.1 Thermial Injuries Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTA4NTIzMjIzNTg5MzA2)",
            "[<b>12. Thrmeal Injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTA5NTI1MjQ3OTQ0MjMz)",
            "[<b>15.1 Toxicology Questions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTEwNTI3MjcyMjk5MTYw)",
            "[<b>15.Toxicology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTExNTI5Mjk2NjU0MDg3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        fmtdh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"fmtdh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"fmtdh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(fmtdh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("anatomyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>8.1 Anterior Abdominal Wall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTEyNTMxMzIxMDA5MDE0)",
            "[<b>8.2 Posterior Abdominal Wall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTEzNTMzMzQ1MzYzOTQx)",
            "[<b>8.3 Peritoneum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTE0NTM1MzY5NzE4ODY4)",
            "[<b>8.4 viscera atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTE1NTM3Mzk0MDczNzk1)",
            "[<b>8.5 Perineum and Development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTE2NTM5NDE4NDI4NzIy)",
            "[<b>8.7.Abdomen MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTE3NTQxNDQyNzgzNjQ5)",
            "[<b>1.1.GENERAL ANAT MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTE4NTQzNDY3MTM4NTc2)",
            "[<b>1.General Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTE5NTQ1NDkxNDkzNTAz)",
            "[<b>4.1 Gametogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTIwNTQ3NTE1ODQ4NDMw)",
            "[<b>4.2 gatrulation and further development atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTIxNTQ5NTQwMjAzMzU3)",
            "[<b>4.3.General Embryo MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTIyNTUxNTY0NTU4Mjg0)",
            "[<b>2.1 Foramen of skull atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTIzNTUzNTg4OTEzMjEx)",
            "[<b>2.2 Ceranial Nerves atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTI0NTU1NjEzMjY4MTM4)",
            "[<b>2.3 Dural Venous Sinus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTI1NTU3NjM3NjIzMDY1)",
            "[<b>2.4 Deep Cervical Fascia and Neck triangles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTI2NTU5NjYxOTc3OTky)",
            "[<b>2.5 Arteries of Head and Neck and TMJ joint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTI3NTYxNjg2MzMyOTE5)",
            "[<b>2.6.HEAD AND NECK MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTI4NTYzNzEwNjg3ODQ2)",
            "[<b>9.1.HISTO MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTI5NTY1NzM1MDQyNzcz)",
            "[<b>9.Histo atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTMwNTY3NzU5Mzk3NzAw)",
            "[<b>7.1 Front and Medial thigh atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTMxNTY5NzgzNzUyNjI3)",
            "[<b>7.2 Gluteal region and Hamstring Muscles atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTMyNTcxODA4MTA3NTU0)",
            "[<b>7.3 Popliteal fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTMzNTczODMyNDYyNDgx)",
            "[<b>7.4 Leg and Foot atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTM0NTc1ODU2ODE3NDA4)",
            "[<b>7.5 Knee, Ankle, Superficial Veins and lymphatics of lower limb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTM1NTc3ODgxMTcyMzM1)",
            "[<b>7.6.LOWER LIMB MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTM2NTc5OTA1NTI3MjYy)",
            "[<b>3.1 Devlopment and Spinal cord atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTM3NTgxOTI5ODgyMTg5)",
            "[<b>3.2.Brain Stem atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTM4NTgzOTU0MjM3MTE2)",
            "[<b>3.3 cerebellum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTM5NTg1OTc4NTkyMDQz)",
            "[<b>3.4 diencephalon atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQwNTg4MDAyOTQ2OTcw)",
            "[<b>3.5Cerebrum and Blood supply atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQxNTkwMDI3MzAxODk3)",
            "[<b>3.6.NEURO ANATOMY MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQyNTkyMDUxNjU2ODI0)",
            "[<b>5.1 Intercostal spaces, Diaphragm, Mediastinum atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQzNTk0MDc2MDExNzUx)",
            "[<b>5.2 Lung, Plura and Pericardium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQ0NTk2MTAwMzY2Njc4)",
            "[<b>5.3 Heart and Development of CVS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQ1NTk4MTI0NzIxNjA1)",
            "[<b>5.4.THROAX MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQ2NjAwMTQ5MDc2NTMy)",
            "[<b>6.1 Axilla atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQ3NjAyMTczNDMxNDU5)",
            "[<b>6.2 Pectoral, Deltoid and Scapular region atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQ4NjA0MTk3Nzg2Mzg2)",
            "[<b>6.3 Arm and Cubital Fossa atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTQ5NjA2MjIyMTQxMzEz)",
            "[<b>6.4 Forearm, Snuff box and Carpal tunnel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTUwNjA4MjQ2NDk2MjQw)",
            "[<b>6.5 Palm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTUxNjEwMjcwODUxMTY3)",
            "[<b>6.6 Radial N. , Median N & Ulnar N atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTUyNjEyMjk1MjA2MDk0)",
            "[<b>6.7.UPPER LIMB MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTUzNjE0MzE5NTYxMDIx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        anatomyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"anatomyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"anatomyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(anatomyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("medicinedh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. ABB Physiology in renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTU0NjE2MzQzOTE1OTQ4)",
            "[<b>2.Renal Tubular Acidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTU1NjE4MzY4MjcwODc1)",
            "[<b>3. Inherited channelopathies of renal tubules atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTU2NjIwMzkyNjI1ODAy)",
            "[<b>4. Hormonal defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTU3NjIyNDE2OTgwNzI5)",
            "[<b>1. Approach to ABB defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTU4NjI0NDQxMzM1NjU2)",
            "[<b>2. Respiratory ABB defects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTU5NjI2NDY1NjkwNTgz)",
            "[<b>3. Metabolic Acidosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTYwNjI4NDkwMDQ1NTEw)",
            "[<b>4. Metabolic Alkalosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTYxNjMwNTE0NDAwNDM3)",
            "[<b>5. Classification of RS disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTYyNjMyNTM4NzU1MzY0)",
            "[<b>1.Acute Rheumatic Fever atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTYzNjM0NTYzMTEwMjkx)",
            "[<b>Apex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTY0NjM2NTg3NDY1MjE4)",
            "[<b>1. Approach to Renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTY1NjM4NjExODIwMTQ1)",
            "[<b>2. Approach to AKI atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTY2NjQwNjM2MTc1MDcy)",
            "[<b>3. TubuloInterstitial disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTY3NjQyNjYwNTI5OTk5)",
            "[<b>1. Approach to Arthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTY4NjQ0Njg0ODg0OTI2)",
            "[<b>2. Inflammatory Pauciarthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTY5NjQ2NzA5MjM5ODUz)",
            "[<b>3.Inflammatory Polyarthritis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTcwNjQ4NzMzNTk0Nzgw)",
            "[<b>1. Pumonary function tests atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTcxNjUwNzU3OTQ5NzA3)",
            "[<b>2. Approach to ABG analysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTcyNjUyNzgyMzA0NjM0)",
            "[<b>3. Approach to Hypoxemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTczNjU0ODA2NjU5NTYx)",
            "[<b>4. Hypo and Hyperventilation syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTc0NjU2ODMxMDE0NDg4)",
            "[<b>8. Respiratory Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTc1NjU4ODU1MzY5NDE1)",
            "[<b>1. Screening tests in Renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTc2NjYwODc5NzI0MzQy)",
            "[<b>2. Urinanalysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTc3NjYyOTA0MDc5MjY5)",
            "[<b>3. USG in Renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTc4NjY0OTI4NDM0MTk2)",
            "[<b>4. GFR estimation methods atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTc5NjY2OTUyNzg5MTIz)",
            "[<b>1.Autoimmune Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTgwNjY4OTc3MTQ0MDUw)",
            "[<b>2.Primary Biliary Cholangitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTgxNjcxMDAxNDk4OTc3)",
            "[<b>1. CKD Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTgyNjczMDI1ODUzOTA0)",
            "[<b>2. DM Nephropathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTgzNjc1MDUwMjA4ODMx)",
            "[<b>3. Inherited Causes of CKD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTg0Njc3MDc0NTYzNzU4)",
            "[<b>4. Renal Replacement Therapy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTg1Njc5MDk4OTE4Njg1)",
            "[<b>1. Approach to Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTg2NjgxMTIzMjczNjEy)",
            "[<b>2. Physiology of CVS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTg3NjgzMTQ3NjI4NTM5)",
            "[<b>3. Approach to Chest pain atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTg4Njg1MTcxOTgzNDY2)",
            "[<b>4. Approach to Breathlessness atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTg5Njg3MTk2MzM4Mzkz)",
            "[<b>5. Approach to Palpitations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTkwNjg5MjIwNjkzMzIw)",
            "[<b>6. Approach to Syncope atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTkxNjkxMjQ1MDQ4MjQ3)",
            "[<b>7. Approach to Edema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTkyNjkzMjY5NDAzMTc0)",
            "[<b>8. Assessment methods in CVS disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTkzNjk1MjkzNzU4MTAx)",
            "[<b>1. Cardiomyopathies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTk0Njk3MzE4MTEzMDI4)",
            "[<b>2. Variants of CMP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTk1Njk5MzQyNDY3OTU1)",
            "[<b>1. Dilated Cardiomyopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTk2NzAxMzY2ODIyODgy)",
            "[<b>2.Hypertrophic Obstructive CMP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTk3NzAzMzkxMTc3ODA5)",
            "[<b>3. Restrictive CMP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTk4NzA1NDE1NTMyNzM2)",
            "[<b>1.Alcohol Liver Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MTk5NzA3NDM5ODg3NjYz)",
            "[<b>2.Non-Alcoholic Fatty Liver Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjAwNzA5NDY0MjQyNTkw)",
            "[<b>1. Peripheral pulse examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjAxNzExNDg4NTk3NTE3)",
            "[<b>2. Carotid pulse examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjAyNzEzNTEyOTUyNDQ0)",
            "[<b>3. JVP waveform examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjAzNzE1NTM3MzA3Mzcx)",
            "[<b>4. Pulsus paradoxus Kussmuals sign atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjA0NzE3NTYxNjYyMjk4)",
            "[<b>5. Heart sounds atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjA1NzE5NTg2MDE3MjI1)",
            "[<b>6. Cardiac murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjA2NzIxNjEwMzcyMTUy)",
            "[<b>1.Coronary Artery Diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjA3NzIzNjM0NzI3MDc5)",
            "[<b>2.ECG and Cardiac Markers in CAD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjA4NzI1NjU5MDgyMDA2)",
            "[<b>3.Management of CAD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjA5NzI3NjgzNDM2OTMz)",
            "[<b>1.Electrophysiological Events & ECG Manifestation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjEwNzI5NzA3NzkxODYw)",
            "[<b>2.ECG Paper & Heart rate Calculation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjExNzMxNzMyMTQ2Nzg3)",
            "[<b>3.Principle of ECG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjEyNzMzNzU2NTAxNzE0)",
            "[<b>4.Bipolar limb leads,Unipolar limb leads & Chest leads atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjEzNzM1NzgwODU2NjQx)",
            "[<b>5.Normal & Abnormal P wave atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjE0NzM3ODA1MjExNTY4)",
            "[<b>6.PR Interval atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjE1NzM5ODI5NTY2NDk1)",
            "[<b>7. QRS Complex width atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjE2NzQxODUzOTIxNDIy)",
            "[<b>8.QRS Normal & Abnormal Morphology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjE3NzQzODc4Mjc2MzQ5)",
            "[<b>9. QRS Axis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjE4NzQ1OTAyNjMxMjc2)",
            "[<b>10.J wave,ST segment,T wave & QT Interval atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjE5NzQ3OTI2OTg2MjAz)",
            "[<b>11.Sinus Bradycardia & Sinus arrest atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjIwNzQ5OTUxMzQxMTMw)",
            "[<b>12.AV block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjIxNzUxOTc1Njk2MDU3)",
            "[<b>13.Sinus Tachycardia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjIyNzU0MDAwMDUwOTg0)",
            "[<b>14.Atrial Tachycardia,Flutter & Fibrillation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjIzNzU2MDI0NDA1OTEx)",
            "[<b>15.PSVT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjI0NzU4MDQ4NzYwODM4)",
            "[<b>16.Ventricular Tachyarrythmia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjI1NzYwMDczMTE1NzY1)",
            "[<b>1. ECG Interpretation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjI2NzYyMDk3NDcwNjky)",
            "[<b>2. Introduction to Arrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjI3NzY0MTIxODI1NjE5)",
            "[<b>3. Heart block atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjI4NzY2MTQ2MTgwNTQ2)",
            "[<b>4. Introduction to Tachyarrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjI5NzY4MTcwNTM1NDcz)",
            "[<b>5. Supraventricular tacharrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjMwNzcwMTk0ODkwNDAw)",
            "[<b>6. Ventricular tachyarrythmias atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjMxNzcyMjE5MjQ1MzI3)",
            "[<b>1. Echocardiography atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjMyNzc0MjQzNjAwMjU0)",
            "[<b>2. Pericardial disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjMzNzc2MjY3OTU1MTgx)",
            "[<b>1.Wilson Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjM0Nzc4MjkyMzEwMTA4)",
            "[<b>2.Hemochromatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjM1NzgwMzE2NjY1MDM1)",
            "[<b>1. Approach to GN atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjM2NzgyMzQxMDE5OTYy)",
            "[<b>2. Postpharyngitic GN atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjM3Nzg0MzY1Mzc0ODg5)",
            "[<b>3. Pulmonary Renal syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjM4Nzg2Mzg5NzI5ODE2)",
            "[<b>4. Adult onset Nephrotic syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjM5Nzg4NDE0MDg0NzQz)",
            "[<b>1. Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQwNzkwNDM4NDM5Njcw)",
            "[<b>2. Coronary artery disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQxNzkyNDYyNzk0NTk3)",
            "[<b>1. Classification and Clinical Features of HF atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQyNzk0NDg3MTQ5NTI0)",
            "[<b>1.Heart Failure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQzNzk2NTExNTA0NDUx)",
            "[<b>2. Investigations of HF atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQ0Nzk4NTM1ODU5Mzc4)",
            "[<b>1. S1 Heart sound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQ1ODAwNTYwMjE0MzA1)",
            "[<b>2. S2 Heart Sound atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQ2ODAyNTg0NTY5MjMy)",
            "[<b>3. Ejection and Non Ejection Click atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQ3ODA0NjA4OTI0MTU5)",
            "[<b>4.S3,S4,OS,Pericardial Knock and Tumor Plop atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQ4ODA2NjMzMjc5MDg2)",
            "[<b>Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjQ5ODA4NjU3NjM0MDEz)",
            "[<b>1.Causes of IE atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjUwODEwNjgxOTg4OTQw)",
            "[<b>2.DUKES Criteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjUxODEyNzA2MzQzODY3)",
            "[<b>3.Treatment & Prophylaxis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjUyODE0NzMwNjk4Nzk0)",
            "[<b>1. Interstitial Lung diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjUzODE2NzU1MDUzNzIx)",
            "[<b>2. Idiopathic Lung diseases atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjU0ODE4Nzc5NDA4NjQ4)",
            "[<b>1.Normal JVP atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjU1ODIwODAzNzYzNTc1)",
            "[<b>2. a wave abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjU2ODIyODI4MTE4NTAy)",
            "[<b>3. x descent abnomality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjU3ODI0ODUyNDczNDI5)",
            "[<b>4.v wave abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjU4ODI2ODc2ODI4MzU2)",
            "[<b>5. y descent abnormality atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjU5ODI4OTAxMTgzMjgz)",
            "[<b>6. Kussmaul Sign atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjYwODMwOTI1NTM4MjEw)",
            "[<b>7. Hepatojugular Reflex atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjYxODMyOTQ5ODkzMTM3)",
            "[<b>1.Disorders of Bilirubin Metabolism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjYyODM0OTc0MjQ4MDY0)",
            "[<b>2.Liver Enzyme atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjYzODM2OTk4NjAyOTkx)",
            "[<b>1. Systemic Lupus Erythematosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjY0ODM5MDIyOTU3OTE4)",
            "[<b>2. Systemic Sclerosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjY1ODQxMDQ3MzEyODQ1)",
            "[<b>1. OSAH syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjY2ODQzMDcxNjY3Nzcy)",
            "[<b>2. Pulmonary Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjY3ODQ1MDk2MDIyNjk5)",
            "[<b>3. Pulmonary Embolisim atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjY4ODQ3MTIwMzc3NjI2)",
            "[<b>4. Lung cancers atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjY5ODQ5MTQ0NzMyNTUz)",
            "[<b>1.Systolic Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjcwODUxMTY5MDg3NDgw)",
            "[<b>2.Diastolic Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjcxODUzMTkzNDQyNDA3)",
            "[<b>3.Continous Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjcyODU1MjE3Nzk3MzM0)",
            "[<b>4.Factors affecting Murmurs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjczODU3MjQyMTUyMjYx)",
            "[<b>1. Myositis syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjc0ODU5MjY2NTA3MTg4)",
            "[<b>2. Overlap syndromes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjc1ODYxMjkwODYyMTE1)",
            "[<b>1. Approach to Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjc2ODYzMzE1MjE3MDQy)",
            "[<b>2. Symptomatology of Renal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjc3ODY1MzM5NTcxOTY5)",
            "[<b>1. ABPA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjc4ODY3MzYzOTI2ODk2)",
            "[<b>1. Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjc5ODY5Mzg4MjgxODIz)",
            "[<b>3. Bronchiectasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjgwODcxNDEyNjM2NzUw)",
            "[<b>5. COLD vs ILDs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjgxODczNDM2OTkxNjc3)",
            "[<b>5. GOLD guidelines for COLD management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjgyODc1NDYxMzQ2NjA0)",
            "[<b>1. Acute Pericarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjgzODc3NDg1NzAxNTMx)",
            "[<b>2. Tamponade and Constrictive pericarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjg0ODc5NTEwMDU2NDU4)",
            "[<b>1. Pleural Effusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjg1ODgxNTM0NDExMzg1)",
            "[<b>2. Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjg2ODgzNTU4NzY2MzEy)",
            "[<b>3. Pneumocystis Pneumonia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjg3ODg1NTgzMTIxMjM5)",
            "[<b>1.Pulse Rate atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjg4ODg3NjA3NDc2MTY2)",
            "[<b>2.Pulse Rhythm atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjg5ODg5NjMxODMxMDkz)",
            "[<b>3.Pulse Pressure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjkwODkxNjU2MTg2MDIw)",
            "[<b>4.Pulse Character atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjkxODkzNjgwNTQwOTQ3)",
            "[<b>5.Radio femoral delay atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjkyODk1NzA0ODk1ODc0)",
            "[<b>6.Pulse Deficit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MjkzODk3NzI5MjUwODAx)",
            "[<b>7.Pulsus Paradoxus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjk0ODk5NzUzNjA1NzI4)",
            "[<b>1. Approach to Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjk1OTAxNzc3OTYwNjU1)",
            "[<b>2. Introduction to RS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjk2OTAzODAyMzE1NTgy)",
            "[<b>3. Symptomatology of RS disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjk3OTA1ODI2NjcwNTA5)",
            "[<b>1. Approach to Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjk4OTA3ODUxMDI1NDM2)",
            "[<b>2. Physiology of Immune system atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mjk5OTA5ODc1MzgwMzYz)",
            "[<b>3.Immune excess disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzAwOTExODk5NzM1Mjkw)",
            "[<b>4. ANA testing atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzAxOTEzOTI0MDkwMjE3)",
            "[<b>1. Tuberculosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzAyOTE1OTQ4NDQ1MTQ0)",
            "[<b>1.Aortic Stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzAzOTE3OTcyODAwMDcx)",
            "[<b>2.Mitral Stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzA0OTE5OTk3MTU0OTk4)",
            "[<b>3.Aortic Regurgitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzA1OTIyMDIxNTA5OTI1)",
            "[<b>4.Mitral Regurgitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzA2OTI0MDQ1ODY0ODUy)",
            "[<b>6.TS,TR,PS,PR atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzA3OTI2MDcwMjE5Nzc5)",
            "[<b>1. Mitral Stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzA4OTI4MDk0NTc0NzA2)",
            "[<b>2. Aortic stenosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzA5OTMwMTE4OTI5NjMz)",
            "[<b>3. Mitral regurgitation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzEwOTMyMTQzMjg0NTYw)",
            "[<b>4. Mitral Valve Prolapse atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzExOTM0MTY3NjM5NDg3)",
            "[<b>5. Infective Endocarditis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzEyOTM2MTkxOTk0NDE0)",
            "[<b>1. Approch to Vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzEzOTM4MjE2MzQ5MzQx)",
            "[<b>2. Large vessel vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzE0OTQwMjQwNzA0MjY4)",
            "[<b>3. Medium and small vessel vasculitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzE1OTQyMjY1MDU5MTk1)",
            "[<b>1.Hepatitis A atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzE2OTQ0Mjg5NDE0MTIy)",
            "[<b>2.Mode of Transmission and Prophylaxis - Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzE3OTQ2MzEzNzY5MDQ5)",
            "[<b>3.Clinical Features - Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzE4OTQ4MzM4MTIzOTc2)",
            "[<b>4.Serology - Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzE5OTUwMzYyNDc4OTAz)",
            "[<b>5. Treatment - Hepatitis B atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzIwOTUyMzg2ODMzODMw)",
            "[<b>6.Hepatitis C atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzIxOTU0NDExMTg4NzU3)",
            "[<b>7.Hepatitis D atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzIyOTU2NDM1NTQzNjg0)",
            "[<b>8.Hepatitis E atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzIzOTU4NDU5ODk4NjEx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        medicinedh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"medicinedh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"medicinedh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(medicinedh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("dermatologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>3.Appendageal disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzI0OTYwNDg0MjUzNTM4)",
            "[<b>1.Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzI1OTYyNTA4NjA4NDY1)",
            "[<b>8.Disorders of Keratinization and Genodermatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzI2OTY0NTMyOTYzMzky)",
            "[<b>2.Hair and Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzI3OTY2NTU3MzE4MzE5)",
            "[<b>1.Bacterial Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzI4OTY4NTgxNjczMjQ2)",
            "[<b>2.Fungal Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzI5OTcwNjA2MDI4MTcz)",
            "[<b>3.Mycobacterial Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzMwOTcyNjMwMzgzMTAw)",
            "[<b>4.Protozoal and Parasitic Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzMxOTc0NjU0NzM4MDI3)",
            "[<b>5.Viral Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzMyOTc2Njc5MDkyOTU0)",
            "[<b>15.1.Drug Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzMzOTc4NzAzNDQ3ODgx)",
            "[<b>9.1.Nutritional deficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzM0OTgwNzI3ODAyODA4)",
            "[<b>1. Psoriasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzM1OTgyNzUyMTU3NzM1)",
            "[<b>2.Lichen planus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzM2OTg0Nzc2NTEyNjYy)",
            "[<b>3. Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzM3OTg2ODAwODY3NTg5)",
            "[<b>5.4 MCQ Papulosqamous disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzM4OTg4ODI1MjIyNTE2)",
            "[<b>Pigmentary Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzM5OTkwODQ5NTc3NDQz)",
            "[<b>1.STD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQwOTkyODczOTMyMzcw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        dermatologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"dermatologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"dermatologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(dermatologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("microbiologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Gram Positive Cocci - Staphylococcus and Streptococcus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQxOTk0ODk4Mjg3Mjk3)",
            "[<b>2. Gram Positive Bacilli - Bacillus and Clostridium atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQyOTk2OTIyNjQyMjI0)",
            "[<b>3. Gram Positive Bacilli - Corynebacterium, Listeria, Nocardia, Actinomyces and Mycobacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQzOTk4OTQ2OTk3MTUx)",
            "[<b>4. Gram Negative Cocci - Neisseria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQ1MDAwOTcxMzUyMDc4)",
            "[<b>5 Gram Negative Bacilli - Pseudomonas, Vibrio, Hemophilus, Bordetella, Brucella, Legionella, Helicobacter, Campylobacter and Francisella atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQ2MDAyOTk1NzA3MDA1)",
            "[<b>6. Gram Negative Bacilli - Enterobactericiae atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQ3MDA1MDIwMDYxOTMy)",
            "[<b>7. Spirochetes, Mycoplasma, chlamydia, Rickettsia and miscellaneous bacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQ4MDA3MDQ0NDE2ODU5)",
            "[<b>8. Bacteriology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzQ5MDA5MDY4NzcxNzg2)",
            "[<b>1 Bacterial Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzUwMDExMDkzMTI2NzEz)",
            "[<b>2. Bacterial Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzUxMDEzMTE3NDgxNjQw)",
            "[<b>3. Bacterial Genetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzUyMDE1MTQxODM2NTY3)",
            "[<b>4. Bacterial Toxins atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzUzMDE3MTY2MTkxNDk0)",
            "[<b>5. Microscopy and Stains atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzU0MDE5MTkwNTQ2NDIx)",
            "[<b>6. Bacterial Culture atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzU1MDIxMjE0OTAxMzQ4)",
            "[<b>7. Biochemical Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzU2MDIzMjM5MjU2Mjc1)",
            "[<b>8. Sterilization and Disinfection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzU3MDI1MjYzNjExMjAy)",
            "[<b>9. General Microbiology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzU4MDI3Mjg3OTY2MTI5)",
            "[<b>1. Basic Immunology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzU5MDI5MzEyMzIxMDU2)",
            "[<b>2. Applied Immunology - Ag, Ab, Ag-Ab reactions and Complements atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzYwMDMxMzM2Njc1OTgz)",
            "[<b>3. Clinical immunology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzYxMDMzMzYxMDMwOTEw)",
            "[<b>4. Immunology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzYyMDM1Mzg1Mzg1ODM3)",
            "[<b>1. Infectious Diseases 1 - basics and CNS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzYzMDM3NDA5NzQwNzY0)",
            "[<b>2. Infectious Diseases 2 -GIT and GUT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzY0MDM5NDM0MDk1Njkx)",
            "[<b>3. Infectious Diseases 3 - RS and CVS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzY1MDQxNDU4NDUwNjE4)",
            "[<b>4. Infectious Diseases 4 - Bone and Joints atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzY2MDQzNDgyODA1NTQ1)",
            "[<b>5. Infectious Diseases 5 -MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzY3MDQ1NTA3MTYwNDcy)",
            "[<b>1. Introduction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzY4MDQ3NTMxNTE1Mzk5)",
            "[<b>2. Superficial and Cutaneous Mycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzY5MDQ5NTU1ODcwMzI2)",
            "[<b>3. Subcutaneous Mycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzcwMDUxNTgwMjI1MjUz)",
            "[<b>4. Systemic Mycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzcxMDUzNjA0NTgwMTgw)",
            "[<b>5. Opportunistic Mycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzcyMDU1NjI4OTM1MTA3)",
            "[<b>6. Mycology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzczMDU3NjUzMjkwMDM0)",
            "[<b>1. Protozoology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzc0MDU5Njc3NjQ0OTYx)",
            "[<b>2. Cestodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzc1MDYxNzAxOTk5ODg4)",
            "[<b>3. Trematodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzc2MDYzNzI2MzU0ODE1)",
            "[<b>4. Nematodes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzc3MDY1NzUwNzA5NzQy)",
            "[<b>5. Parasitology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzc4MDY3Nzc1MDY0NjY5)",
            "[<b>1. General Virology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzc5MDY5Nzk5NDE5NTk2)",
            "[<b>2. DNA Viruses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzgwMDcxODIzNzc0NTIz)",
            "[<b>3. Hepatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzgxMDczODQ4MTI5NDUw)",
            "[<b>4. RNA Viruses 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzgyMDc1ODcyNDg0Mzc3)",
            "[<b>5. RNA Viruses 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzgzMDc3ODk2ODM5MzA0)",
            "[<b>6. Virology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzg0MDc5OTIxMTk0MjMx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        microbiologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"microbiologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"microbiologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(microbiologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("ophthalmologydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1. Conjuctiva- Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzg1MDgxOTQ1NTQ5MTU4)",
            "[<b>2. Allergic conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzg2MDgzOTY5OTA0MDg1)",
            "[<b>3. Infective conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzg3MDg1OTk0MjU5MDEy)",
            "[<b>4. Cicatricial conjunctivitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzg4MDg4MDE4NjEzOTM5)",
            "[<b>5. Conjunctival degenerations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzg5MDkwMDQyOTY4ODY2)",
            "[<b>6. Conjunctiva MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzkwMDkyMDY3MzIzNzkz)",
            "[<b>1. Anatomy of cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzkxMDk0MDkxNjc4NzIw)",
            "[<b>2. Physiology of Cornea and applied aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzkyMDk2MTE2MDMzNjQ3)",
            "[<b>3. Investigations in cornea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1MzkzMDk4MTQwMzg4NTc0)",
            "[<b>4. Corneal ectasiaKeratoconus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzk0MTAwMTY0NzQzNTAx)",
            "[<b>5. Corneal dystrophies atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzk1MTAyMTg5MDk4NDI4)",
            "[<b>6. Corneal depositions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzk2MTA0MjEzNDUzMzU1)",
            "[<b>7. Infectious keratitisClinical features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzk3MTA2MjM3ODA4Mjgy)",
            "[<b>8. Infectious keratitis-Acanthamoeba and Fungal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzk4MTA4MjYyMTYzMjA5)",
            "[<b>9. Infectious keratitisViral and Bacteria atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Mzk5MTEwMjg2NTE4MTM2)",
            "[<b>10. Infectious keratitis-Complications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDAwMTEyMzEwODczMDYz)",
            "[<b>12. Sclera and staphylomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDAxMTE0MzM1MjI3OTkw)",
            "[<b>14 Cornea and Sclera MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDAyMTE2MzU5NTgyOTE3)",
            "[<b>1. Eyelid anatomy and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDAzMTE4MzgzOTM3ODQ0)",
            "[<b>2. Eyelid embryology and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDA0MTIwNDA4MjkyNzcx)",
            "[<b>3. Eyelid margin anatomy and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDA1MTIyNDMyNjQ3Njk4)",
            "[<b>4. Levator muscle and clinical aspcts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDA2MTI0NDU3MDAyNjI1)",
            "[<b>5. Orbicularis muscle and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDA3MTI2NDgxMzU3NTUy)",
            "[<b>6. Eyelids MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDA4MTI4NTA1NzEyNDc5)",
            "[<b>1. Aqueous humour dynamics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDA5MTMwNTMwMDY3NDA2)",
            "[<b>2. Glaucoma definition and pathogenesis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDEwMTMyNTU0NDIyMzMz)",
            "[<b>3. Investigations in glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDExMTM0NTc4Nzc3MjYw)",
            "[<b>4. Primary glaucoms Clinical features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDEyMTM2NjAzMTMyMTg3)",
            "[<b>5. Primary glaucoma Types and Management atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDEzMTM4NjI3NDg3MTE0)",
            "[<b>6. Acute angle closure atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDE0MTQwNjUxODQyMDQx)",
            "[<b>7. Primary congenital glaucoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDE1MTQyNjc2MTk2OTY4)",
            "[<b>8. Secondary glaucomas atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDE2MTQ0NzAwNTUxODk1)",
            "[<b>9.Glaucoma MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDE3MTQ2NzI0OTA2ODIy)",
            "[<b>1. Basic Anatomy of eyeball and Orbit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDE4MTQ4NzQ5MjYxNzQ5)",
            "[<b>2. Vascular supply of eyeball atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDE5MTUwNzczNjE2Njc2)",
            "[<b>3. Embryology of eye atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDIwMTUyNzk3OTcxNjAz)",
            "[<b>4. Visual Pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDIxMTU0ODIyMzI2NTMw)",
            "[<b>5. Light reflex pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDIyMTU2ODQ2NjgxNDU3)",
            "[<b>6. Near pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDIzMTU4ODcxMDM2Mzg0)",
            "[<b>7. Basic examination of eyes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDI0MTYwODk1MzkxMzEx)",
            "[<b>8. Blindness, Basic Milestones and symptoms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDI1MTYyOTE5NzQ2MjM4)",
            "[<b>9. Introductio Basic Anatomy, Embryology, Physiology, Investigations MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDI2MTY0OTQ0MTAxMTY1)",
            "[<b>1. Anatomy and Pysiology of lens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDI3MTY2OTY4NDU2MDky)",
            "[<b>2. Applied Physiology of lens Etiology and Morphology of cataracts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDI4MTY4OTkyODExMDE5)",
            "[<b>3. Senile cataract Stages and symptoms atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDI5MTcxMDE3MTY1OTQ2)",
            "[<b>4. Management of senile cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDMwMTczMDQxNTIwODcz)",
            "[<b>5. Management of congenital cataract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDMxMTc1MDY1ODc1ODAw)",
            "[<b>6. Complications of cataract surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDMyMTc3MDkwMjMwNzI3)",
            "[<b>7. Ectopia lentis and congenital anomalies of lens atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDMzMTc5MTE0NTg1NjU0)",
            "[<b>8. Lens and cataract MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDM0MTgxMTM4OTQwNTgx)",
            "[<b>1. Clinical application of Visual light and near pathway atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDM1MTgzMTYzMjk1NTA4)",
            "[<b>2. Clinical application of Visual, light and near pathway Extra poimts atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDM2MTg1MTg3NjUwNDM1)",
            "[<b>3. Light-Near dissociation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDM3MTg3MjEyMDA1MzYy)",
            "[<b>4. Sympathetic pathway Horner syndrome atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDM4MTg5MjM2MzYwMjg5)",
            "[<b>5. Sympathetic pathway Horner syndrome advanced atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDM5MTkxMjYwNzE1MjE2)",
            "[<b>6. Optic neuritis types and features atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQwMTkzMjg1MDcwMTQz)",
            "[<b>7. Optic atrophy Types and examples atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQxMTk1MzA5NDI1MDcw)",
            "[<b>8.Neuro-Ophthalmology MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQyMTk3MzMzNzc5OTk3)",
            "[<b>1. Ocular injuries atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQzMTk5MzU4MTM0OTI0)",
            "[<b>2. Oribal aand Ocular tumours atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQ0MjAxMzgyNDg5ODUx)",
            "[<b>3. Ocular injuries and tumours MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQ1MjAzNDA2ODQ0Nzc4)",
            "[<b>1. Refractive errors and far point concept atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQ2MjA1NDMxMTk5NzA1)",
            "[<b>2. Aphakia and correction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQ3MjA3NDU1NTU0NjMy)",
            "[<b>3. Near point concept and Presbyopia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQ4MjA5NDc5OTA5NTU5)",
            "[<b>4. Astigmatism and clinical applications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDQ5MjExNTA0MjY0NDg2)",
            "[<b>5. Determination of refractive error atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDUwMjEzNTI4NjE5NDEz)",
            "[<b>6. Questions on refraction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDUxMjE1NTUyOTc0MzQw)",
            "[<b>7. Pin hole and stenopic slit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDUyMjE3NTc3MzI5MjY3)",
            "[<b>8. Refarctive surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDUzMjE5NjAxNjg0MTk0)",
            "[<b>9 Optics MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDU0MjIxNjI2MDM5MTIx)",
            "[<b>1. Clinical syndromes in orbit atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDU1MjIzNjUwMzk0MDQ4)",
            "[<b>2. Proptosis and types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDU2MjI1Njc0NzQ4OTc1)",
            "[<b>3. Thyroid eye disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDU3MjI3Njk5MTAzOTAy)",
            "[<b>4. Orbital cellulitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDU4MjI5NzIzNDU4ODI5)",
            "[<b>5. Orbit MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDU5MjMxNzQ3ODEzNzU2)",
            "[<b>1. Structure and Layers of retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDYwMjMzNzcyMTY4Njgz)",
            "[<b>2. Vascular supply and barriers of retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDYxMjM1Nzk2NTIzNjEw)",
            "[<b>3. Investigations in Retina atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDYyMjM3ODIwODc4NTM3)",
            "[<b>4. Posterior vitreous detachment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDYzMjM5ODQ1MjMzNDY0)",
            "[<b>5. Retinal detachment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDY0MjQxODY5NTg4Mzkx)",
            "[<b>6. Central serous retinopathy and Cystoid macular edema atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDY1MjQzODkzOTQzMzE4)",
            "[<b>7. Retinal degenerations atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDY2MjQ1OTE4Mjk4MjQ1)",
            "[<b>8. Retinal dystrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDY3MjQ3OTQyNjUzMTcy)",
            "[<b>9. Cone dystrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDY4MjQ5OTY3MDA4MDk5)",
            "[<b>10. Choroidal dystrophy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDY5MjUxOTkxMzYzMDI2)",
            "[<b>11. Diabetic Retinopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDcwMjU0MDE1NzE3OTUz)",
            "[<b>12. Hypertensive Retinopathy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDcxMjU2MDQwMDcyODgw)",
            "[<b>13. Retinal Vein occlusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDcyMjU4MDY0NDI3ODA3)",
            "[<b>14. Retinal artery occlusion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDczMjYwMDg4NzgyNzM0)",
            "[<b>15. Retinopathy of prematurity atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDc0MjYyMTEzMTM3NjYx)",
            "[<b>16. Retina and Vitreous MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDc1MjY0MTM3NDkyNTg4)",
            "[<b>1.RAAS Inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDc2MjY2MTYxODQ3NTE1)",
            "[<b>2. Squint-Definitiona and types atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDc3MjY4MTg2MjAyNDQy)",
            "[<b>3. Basic tests for squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDc4MjcwMjEwNTU3MzY5)",
            "[<b>4. Diplopia and clinical applications atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDc5MjcyMjM0OTEyMjk2)",
            "[<b>5. Examples of paralytic squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDgwMjc0MjU5MjY3MjIz)",
            "[<b>6. Examples of comitant squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDgxMjc2MjgzNjIyMTUw)",
            "[<b>7. Management of squint atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDgyMjc4MzA3OTc3MDc3)",
            "[<b>8. Tests for Binocularity and Stereopsis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDgzMjgwMzMyMzMyMDA0)",
            "[<b>9. Nystagmus and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDg0MjgyMzU2Njg2OTMx)",
            "[<b>10. Supranuclear control of eye movements atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDg1Mjg0MzgxMDQxODU4)",
            "[<b>11. Squint MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDg2Mjg2NDA1Mzk2Nzg1)",
            "[<b>1. Tear film and clinical aspects atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDg3Mjg4NDI5NzUxNzEy)",
            "[<b>2. Lacrimal apparatus and tests for watering eyes atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDg4MjkwNDU0MTA2NjM5)",
            "[<b>3. Features of nasolacrimal duct obstruction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDg5MjkyNDc4NDYxNTY2)",
            "[<b>4. Tear film and Lacrimal apparatus MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDkwMjk0NTAyODE2NDkz)",
            "[<b>1. Uveal tract atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDkxMjk2NTI3MTcxNDIw)",
            "[<b>2. Uveal tract MCQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDkyMjk4NTUxNTI2MzQ3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        ophthalmologydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ophthalmologydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ophthalmologydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(ophthalmologydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("dermatologyde"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>11.1.Allergic Disorders and Dermatitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDkzMzAwNTc1ODgxMjc0)",	
            "[<b>3.1.Appendegeal Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDk0MzAyNjAwMjM2MjAx)",	
            "[<b>1.1.Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDk1MzA0NjI0NTkxMTI4)",	
            "[<b>1.2.Structure of Nail atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDk2MzA2NjQ4OTQ2MDU1)",	
            "[<b>3.MCQ Basics of Skin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDk3MzA4NjczMzAwOTgy)",	
            "[<b>14.Cutaneous Lesions in Systemic Disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDk4MzEwNjk3NjU1OTA5)",	
            "[<b>13.Cutaneous Malignancy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NDk5MzEyNzIyMDEwODM2)",	
            "[<b>8.1 Disorders of Keratinization and Genodermatosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTAwMzE0NzQ2MzY1NzYz)",	
            "[<b>2.1.Basics of Hair atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTAxMzE2NzcwNzIwNjkw)",	
            "[<b>2.2.Disorders of Hairs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTAyMzE4Nzk1MDc1NjE3)",	
            "[<b>4.1.Bacterial Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTAzMzIwODE5NDMwNTQ0)",	
            "[<b>4.2.Fungal Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTA0MzIyODQzNzg1NDcx)",	
            "[<b>4.3.Mycobacterial disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTA1MzI0ODY4MTQwMzk4)",	
            "[<b>4.4.Parasitic infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTA2MzI2ODkyNDk1MzI1)",	
            "[<b>4.5.Protozoal Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTA3MzI4OTE2ODUwMjUy)",	
            "[<b>4.6.Viral Infections atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTA4MzMwOTQxMjA1MTc5)",	
            "[<b>12.Leprosy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTA5MzMyOTY1NTYwMTA2)",	
            "[<b>15.1.Drug Reactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTEwMzM0OTg5OTE1MDMz)",	
            "[<b>15.2.Paraneoplastic Dermatoses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTExMzM3MDE0MjY5OTYw)",	
            "[<b>9.1.Nutritional deficiency atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTEyMzM5MDM4NjI0ODg3)",	
            "[<b>5.1.Psoriasis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTEzMzQxMDYyOTc5ODE0)",	
            "[<b>5.2.Lichen planus atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTE0MzQzMDg3MzM0NzQx)",	
            "[<b>5.3.Miscellaneous atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTE1MzQ1MTExNjg5NjY4)",	
            "[<b>7.1 Pigmentary disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTE2MzQ3MTM2MDQ0NTk1)",	
            "[<b>10.STD atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTE3MzQ5MTYwMzk5NTIy)",	
            "[<b>6.1 Vesciculobullous disorder atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTE4MzUxMTg0NzU0NDQ5)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        dermatologyde_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"dermatologyde_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"dermatologyde_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(dermatologyde_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("pharmacologydh"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.Introduction to ANS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTE5MzUzMjA5MTA5Mzc2)",
            "[<b>2. Cholinergic System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTIwMzU1MjMzNDY0MzAz)",
            "[<b>3.Cholinergics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTIxMzU3MjU3ODE5MjMw)",
            "[<b>4.Anti Cholinergis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTIyMzU5MjgyMTc0MTU3)",
            "[<b>5.Clinical Pharmacology (Eyes and Bladder) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTIzMzYxMzA2NTI5MDg0)",
            "[<b>6.Sympathetic System atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTI0MzYzMzMwODg0MDEx)",
            "[<b>7.Adrenergics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTI1MzY1MzU1MjM4OTM4)",
            "[<b>8. Anti Adrenergics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTI2MzY3Mzc5NTkzODY1)",
            "[<b>1. Cell wall inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTI3MzY5NDAzOTQ4Nzky)",
            "[<b>2. Cell membrane Inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTI4MzcxNDI4MzAzNzE5)",
            "[<b>3.Protein synthesis inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTI5MzczNDUyNjU4NjQ2)",
            "[<b>4.DNA inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTMwMzc1NDc3MDEzNTcz)",
            "[<b>5. Quinolones & Sulfonamides atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTMxMzc3NTAxMzY4NTAw)",
            "[<b>6. Special points in Antibiotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTMyMzc5NTI1NzIzNDI3)",
            "[<b>7. Anti-Tubercular Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTMzMzgxNTUwMDc4MzU0)",
            "[<b>8. Anti-Leprotic Drugs & MAC infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTM0MzgzNTc0NDMzMjgx)",
            "[<b>9. Antiviral Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTM1Mzg1NTk4Nzg4MjA4)",
            "[<b>1.Histamine & Antihistaminics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTM2Mzg3NjIzMTQzMTM1)",
            "[<b>2. Serotonin & Drugs acting on Serotonin receptors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTM3Mzg5NjQ3NDk4MDYy)",
            "[<b>3.Drugs for Migraine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTM4MzkxNjcxODUyOTg5)",
            "[<b>4.Prostaglandins & Drugs for Pulmonary Hypertension atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTM5MzkzNjk2MjA3OTE2)",
            "[<b>5.NSAIDs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQwMzk1NzIwNTYyODQz)",
            "[<b>6.Gout atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQxMzk3NzQ0OTE3Nzcw)",
            "[<b>7.Drugs to treat RA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQyMzk5NzY5MjcyNjk3)",
            "[<b>1.Sedative & Hypnotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQzNDAxNzkzNjI3NjI0)",
            "[<b>2.Alcohol atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQ0NDAzODE3OTgyNTUx)",
            "[<b>3.Antiepileptics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQ1NDA1ODQyMzM3NDc4)",
            "[<b>4.Antipsychotics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQ2NDA3ODY2NjkyNDA1)",
            "[<b>5.Drug for Mood Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQ3NDA5ODkxMDQ3MzMy)",
            "[<b>6.Opioids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQ4NDExOTE1NDAyMjU5)",
            "[<b>7.Antiparkinsonism atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTQ5NDEzOTM5NzU3MTg2)",
            "[<b>8.SMR & GA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTUwNDE1OTY0MTEyMTEz)",
            "[<b>1.RAAS Inhibitors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTUxNDE3OTg4NDY3MDQw)",
            "[<b>2. Anti HTN Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTUyNDIwMDEyODIxOTY3)",
            "[<b>3. Drugs to treat CHF atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTUzNDIyMDM3MTc2ODk0)",
            "[<b>4. Anti Anginal Drugs atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTU0NDI0MDYxNTMxODIx)",
            "[<b>5. Anti Arrhythmics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTU1NDI2MDg1ODg2NzQ4)",
            "[<b>1.Diuretics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTU2NDI4MTEwMjQxNjc1)",
            "[<b>2.Anti-Diuretics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTU3NDMwMTM0NTk2NjAy)",
            "[<b>1.Anti Diabetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTU4NDMyMTU4OTUxNTI5)",
            "[<b>2.Drugs for Thyroid disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTU5NDM0MTgzMzA2NDU2)",
            "[<b>3.Drugs to treat Osteoporosis & Calcium imbalance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTYwNDM2MjA3NjYxMzgz)",
            "[<b>4.Hypothalamus & Pituitary Hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTYxNDM4MjMyMDE2MzEw)",
            "[<b>5. Sex Hormones atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTYyNDQwMjU2MzcxMjM3)",
            "[<b>6. Uterine Stimulants & Tocolytics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTYzNDQyMjgwNzI2MTY0)",
            "[<b>7. Adrenal gland hormones & Corticosteroids atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTY0NDQ0MzA1MDgxMDkx)",
            "[<b>1.Drugs to treat Acid peptic disease atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTY1NDQ2MzI5NDM2MDE4)",
            "[<b>2.Antiemetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTY2NDQ4MzUzNzkwOTQ1)",
            "[<b>3. Drugs to treat Constipation atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTY3NDUwMzc4MTQ1ODcy)",
            "[<b>4. Drugs to treat Diarrhoea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTY4NDUyNDAyNTAwNzk5)",
            "[<b>1.Introduction and routes of drug administration atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTY5NDU0NDI2ODU1NzI2)",
            "[<b>2. New drug devellopment atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTcwNDU2NDUxMjEwNjUz)",
            "[<b>3. Pharmacokinetics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTcxNDU4NDc1NTY1NTgw)",
            "[<b>4. Pharmacodynamics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTcyNDYwNDk5OTIwNTA3)",
            "[<b>5.Drug Interactions atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTczNDYyNTI0Mjc1NDM0)",
            "[<b>6. Pharmacovigilance atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTc0NDY0NTQ4NjMwMzYx)",
            "[<b>1.Antiplatelets atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTc1NDY2NTcyOTg1Mjg4)",
            "[<b>2. Anticoagulants atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTc2NDY4NTk3MzQwMjE1)",
            "[<b>3. Thrombolytics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTc3NDcwNjIxNjk1MTQy)",
            "[<b>4. Drugs for Dyslipidemia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTc4NDcyNjQ2MDUwMDY5)",
            "[<b>1. Drugs to treat Cough atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTc5NDc0NjcwNDA0OTk2)",
            "[<b>2. Drugs to treat Asthma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTgwNDc2Njk0NzU5OTIz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        pharmacologydh_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pharmacologydh_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pharmacologydh_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(pharmacologydh_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("damsdvt"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTgxNDc4NzE5MTE0ODUw)",
            "[<b>Anesthesia atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTgyNDgwNzQzNDY5Nzc3)",
            "[<b>Biochemistry - Dr. Poonam atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTgzNDgyNzY3ODI0NzA0)",
            "[<b>Biochemistry - Dr. Sonam atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTg0NDg0NzkyMTc5NjMx)",
            "[<b>Gold Standard Revision for NEETPG DAMS DVT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTg1NDg2ODE2NTM0NTU4)",
            "[<b>Message from the Mentors atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTg2NDg4ODQwODg5NDg1)",
            "[<b>Post DVT Revision Strategy NEETPG atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTg3NDkwODY1MjQ0NDEy)",
            "[<b>Dermatology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTg4NDkyODg5NTk5MzM5)",
            "[<b>ENT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTg5NDk0OTEzOTU0MjY2)",
            "[<b>FMT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTkwNDk2OTM4MzA5MTkz)",
            "[<b>Medicine CNS - Dr. Achin atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTkxNDk4OTYyNjY0MTIw)",
            "[<b>Medicine Cvs Git - Dr. Arvind atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTkyNTAwOTg3MDE5MDQ3)",
            "[<b>Medicine Endocrinology - Dr. Rahul Nikumbe atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTkzNTAzMDExMzczOTc0)",
            "[<b>Medicine Nephrology Rheumatology - Dr. Srinath atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTk0NTA1MDM1NzI4OTAx)",
            "[<b>Medicine Resp Abb - Dr. Bharath Kathi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTk1NTA3MDYwMDgzODI4)",
            "[<b>Microbiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTk2NTA5MDg0NDM4NzU1)",
            "[<b>IMAGES OF OBGY - Dr. Anil Mirchandani atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTk3NTExMTA4NzkzNjgy)",
            "[<b>OBGY - Dr. Deepti Bahl atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTk4NTEzMTMzMTQ4NjA5)",
            "[<b>Ophthalmology Dr. Manish Chhabra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NTk5NTE1MTU3NTAzNTM2)",
            "[<b>Ophthalmology Dr. Sourabh Sharma (1) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjAwNTE3MTgxODU4NDYz)",
            "[<b>Ophthalmology Dr. Sourabh Sharma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjAxNTE5MjA2MjEzMzkw)",
            "[<b>Orthopaedics atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjAyNTIxMjMwNTY4MzE3)",
            "[<b>PSM Dr Kasish Grover atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjAzNTIzMjU0OTIzMjQ0)",
            "[<b>PSM Dr Sidharth Mishra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjA0NTI1Mjc5Mjc4MTcx)",
            "[<b>Pathology (Gen-Pathology) Dr. Shagun atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjA1NTI3MzAzNjMzMDk4)",
            "[<b>Pathology (Hemat & Sys-Path ) Dr Sanjeev atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjA2NTI5MzI3OTg4MDI1)",
            "[<b>Paediactrics Dr. Ashutosh Aggarwal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjA3NTMxMzUyMzQyOTUy)",
            "[<b>Paediactrics Dr. Sidharth Sethi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjA4NTMzMzc2Njk3ODc5)",
            "[<b>Pharmacology Dr. Dinesh atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjA5NTM1NDAxMDUyODA2)",
            "[<b>Pharmacology Dr. Thiru atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjEwNTM3NDI1NDA3NzMz)",
            "[<b>Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjExNTM5NDQ5NzYyNjYw)",
            "[<b>Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjEyNTQxNDc0MTE3NTg3)",
            "[<b>Radiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjEzNTQzNDk4NDcyNTE0)",
            "[<b>Surgery Dr. Gaurav Patel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjE0NTQ1NTIyODI3NDQx)",
            "[<b>Surgery Dr. Rajeev Tewari atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjE1NTQ3NTQ3MTgyMzY4)",
            "[<b>Surgery Dr. Sujoy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjE2NTQ5NTcxNTM3Mjk1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        damsdvt_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"damsdvt_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"damsdvt_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(damsdvt_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("damstnd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Anatomy NEET App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjE3NTUxNTk1ODkyMjIy)",
            "[<b>Anatomy Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjE4NTUzNjIwMjQ3MTQ5)",
            "[<b>Anesthesia Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjE5NTU1NjQ0NjAyMDc2)",
            "[<b>Anesthesia Test and discussion (1) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjIwNTU3NjY4OTU3MDAz)",
            "[<b>Biochemistry App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjIxNTU5NjkzMzExOTMw)",
            "[<b>Biochemistry NEET App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjIyNTYxNzE3NjY2ODU3)",
            "[<b>Dermatology App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjIzNTYzNzQyMDIxNzg0)",
            "[<b>Dermatology Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjI0NTY1NzY2Mzc2NzEx)",
            "[<b>ENT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjI1NTY3NzkwNzMxNjM4)",
            "[<b>ENT Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjI2NTY5ODE1MDg2NTY1)",
            "[<b>FMT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjI3NTcxODM5NDQxNDky)",
            "[<b>FMT Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjI4NTczODYzNzk2NDE5)",
            "[<b>How to Best Use DAMS TND I Strategy & TipsI I by Dr. Deepti Bahl atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjI5NTc1ODg4MTUxMzQ2)",
            "[<b>Medicine -CVS GIT GEN Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjMwNTc3OTEyNTA2Mjcz)",
            "[<b>Medicine CNS  ENDO Test and Discussion Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjMxNTc5OTM2ODYxMjAw)",
            "[<b>Medicine CNS  ENDO Test and Discussion Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjMyNTgxOTYxMjE2MTI3)",
            "[<b>Medicine CNS ENDO App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjMzNTgzOTg1NTcxMDU0)",
            "[<b>Medicine CVS GIT  Gen App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjM0NTg2MDA5OTI1OTgx)",
            "[<b>Medicine Nephro-Rheumat App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjM1NTg4MDM0MjgwOTA4)",
            "[<b>Medicine Nephrology Rhumat Resp Test & Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjM2NTkwMDU4NjM1ODM1)",
            "[<b>Microbiology App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjM3NTkyMDgyOTkwNzYy)",
            "[<b>Microbiology NEET App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjM4NTk0MTA3MzQ1Njg5)",
            "[<b>Gynaecology App test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjM5NTk2MTMxNzAwNjE2)",
            "[<b>Obstetrics Discussion by Dr Deepti atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQwNTk4MTU2MDU1NTQz)",
            "[<b>Ophthalmology App T&D (Dr. Sourabh Sharma) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQxNjAwMTgwNDEwNDcw)",
            "[<b>Ophthalmology Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQyNjAyMjA0NzY1Mzk3)",
            "[<b>Ophthalmology test and discussion by Dr Manish chabbra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQzNjA0MjI5MTIwMzI0)",
            "[<b>Orthopaedics App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQ0NjA2MjUzNDc1MjUx)",
            "[<b>PSM App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQ1NjA4Mjc3ODMwMTc4)",
            "[<b>Patho(Gen path (except neoplasia) and hematology (except WBC) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQ2NjEwMzAyMTg1MTA1)",
            "[<b>Patho(Sys+Neoplasia & WBC) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQ3NjEyMzI2NTQwMDMy)",
            "[<b>Pathology (Sys+Neoplasia & WBC) Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQ4NjE0MzUwODk0OTU5)",
            "[<b>Pathology NEET App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjQ5NjE2Mzc1MjQ5ODg2)",
            "[<b>Pediatrics Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjUwNjE4Mzk5NjA0ODEz)",
            "[<b>Pediatrics-(Systemics) App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjUxNjIwNDIzOTU5NzQw)",
            "[<b>Pharmacology (ANS,CNS,PNS,CVS,RENAL,BLOOD,RS,GIT ) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjUyNjIyNDQ4MzE0NjY3)",
            "[<b>Pharmacology (GP Endo anti-cancer Anti-microbial Autacoids Miscellaneous) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjUzNjI0NDcyNjY5NTk0)",
            "[<b>Pharmacology NEET APP Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjU0NjI2NDk3MDI0NTIx)",
            "[<b>Pharmacology Neet App Test and Discussion (1) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjU1NjI4NTIxMzc5NDQ4)",
            "[<b>Physiology App test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjU2NjMwNTQ1NzM0Mzc1)",
            "[<b>Psychiatry Neet App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjU3NjMyNTcwMDg5MzAy)",
            "[<b>Psychiatry Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjU4NjM0NTk0NDQ0MjI5)",
            "[<b>Radiology Neet App Test and discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjU5NjM2NjE4Nzk5MTU2)",
            "[<b>Surgery (Uro,Thyroid,Parathryoid,Adrenals,Oral malignancy Glands) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjYwNjM4NjQzMTU0MDgz)",
            "[<b>Surgery GIT App Test and Discussion (26 Q to 29 Q) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjYxNjQwNjY3NTA5MDEw)",
            "[<b>Surgery GIT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjYyNjQyNjkxODYzOTM3)",
            "[<b>Surgery(Gen Breast Trauma Vascular Shock Plastic Surgery Nutrition Transplant Hernia) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjYzNjQ0NzE2MjE4ODY0)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        _message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("damspyq"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.Medicine CNS ENDO atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjY0NjQ2NzQwNTczNzkx)",	
            "[<b>1.PYQ ANESTHESIA atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjY1NjQ4NzY0OTI4NzE4)",	
            "[<b>1.PYQ Dermatology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjY2NjUwNzg5MjgzNjQ1)",	
            "[<b>2.Medicine Rheumat Nephro atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjY3NjUyODEzNjM4NTcy)",	
            "[<b>3.Medicine Resp abb atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjY4NjU0ODM3OTkzNDk5)",	
            "[<b>Anaesthesia INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjY5NjU2ODYyMzQ4NDI2)",	
            "[<b>Anatomy INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjcwNjU4ODg2NzAzMzUz)",	
            "[<b>Anatomy NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjcxNjYwOTExMDU4Mjgw)",	
            "[<b>Biochemistry INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjcyNjYyOTM1NDEzMjA3)",	
            "[<b>Biochemistry NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjczNjY0OTU5NzY4MTM0)",	
            "[<b>Dermatology INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njc0NjY2OTg0MTIzMDYx)",	
            "[<b>Dermatology NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njc1NjY5MDA4NDc3OTg4)",	
            "[<b>ENT NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njc2NjcxMDMyODMyOTE1)",	
            "[<b>General Surgery INICET PYQ Dr Gaurav Patel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njc3NjczMDU3MTg3ODQy)",	
            "[<b>Medicine Endo INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njc4Njc1MDgxNTQyNzY5)",	
            "[<b>Medicine GIT INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njc5Njc3MTA1ODk3Njk2)",	
            "[<b>Medicine NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjgwNjc5MTMwMjUyNjIz)",	
            "[<b>Microbiology NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjgxNjgxMTU0NjA3NTUw)",	
            "[<b>OBG INICET PYQ Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjgyNjgzMTc4OTYyNDc3)",	
            "[<b>OBG INICET PYQ Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjgzNjg1MjAzMzE3NDA0)",	
            "[<b>OBG NEETPG Recall 2023 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njg0Njg3MjI3NjcyMzMx)",	
            "[<b>Ophthalmology INICET PYQ Dr Manish Chabra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njg1Njg5MjUyMDI3MjU4)",	
            "[<b>Ophthalmology INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njg2NjkxMjc2MzgyMTg1)",	
            "[<b>Ophthalmology NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njg3NjkzMzAwNzM3MTEy)",	
            "[<b>Orthopedic NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njg4Njk1MzI1MDkyMDM5)",	
            "[<b>PSM INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njg5Njk3MzQ5NDQ2OTY2)",	
            "[<b>PSM NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjkwNjk5MzczODAxODkz)",	
            "[<b>PYQ Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjkxNzAxMzk4MTU2ODIw)",	
            "[<b>PYQ Biochemistry 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjkyNzAzNDIyNTExNzQ3)",	
            "[<b>PYQ Biochemistry 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NjkzNzA1NDQ2ODY2Njc0)",	
            "[<b>PYQ ENT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njk0NzA3NDcxMjIxNjAx)",	
            "[<b>PYQ FMT atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njk1NzA5NDk1NTc2NTI4)",	
            "[<b>PYQ Medicine atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njk2NzExNTE5OTMxNDU1)",	
            "[<b>PYQ Microbiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njk3NzEzNTQ0Mjg2Mzgy)",	
            "[<b>PYQ NEETPG OBGY Dr Deepti Bahl atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njk4NzE1NTY4NjQxMzA5)",	
            "[<b>PYQ OBGY Dr Anil atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Njk5NzE3NTkyOTk2MjM2)",	
            "[<b>PYQ OPHTHALMOLOGY 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzAwNzE5NjE3MzUxMTYz)",	
            "[<b>PYQ OPHTHALMOLOGY 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzAxNzIxNjQxNzA2MDkw)",	
            "[<b>PYQ ORTHOPAEDICS atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzAyNzIzNjY2MDYxMDE3)",	
            "[<b>PYQ PSM 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzAzNzI1NjkwNDE1OTQ0)",	
            "[<b>PYQ PSM 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzA0NzI3NzE0NzcwODcx)",	
            "[<b>PYQ Pathology 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzA1NzI5NzM5MTI1Nzk4)",	
            "[<b>PYQ Pathology 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzA2NzMxNzYzNDgwNzI1)",	
            "[<b>PYQ Pediatrics 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzA3NzMzNzg3ODM1NjUy)",	
            "[<b>PYQ Pediatrics 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzA4NzM1ODEyMTkwNTc5)",	
            "[<b>PYQ Pharmacology 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzA5NzM3ODM2NTQ1NTA2)",	
            "[<b>PYQ Pharmacology 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzEwNzM5ODYwOTAwNDMz)",	
            "[<b>PYQ Physiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzExNzQxODg1MjU1MzYw)",	
            "[<b>PYQ Psychiatry atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzEyNzQzOTA5NjEwMjg3)",	
            "[<b>PYQ Radiology atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzEzNzQ1OTMzOTY1MjE0)",	
            "[<b>PYQ Surgery 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzE0NzQ3OTU4MzIwMTQx)",	
            "[<b>PYQ Surgery 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzE1NzQ5OTgyNjc1MDY4)",	
            "[<b>Pathology General INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzE2NzUyMDA3MDI5OTk1)",	
            "[<b>Pathology INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzE3NzU0MDMxMzg0OTIy)",	
            "[<b>Pediatrics INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzE4NzU2MDU1NzM5ODQ5)",	
            "[<b>Pediatrics INICET PYQ by Dr Sidharth Sethi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzE5NzU4MDgwMDk0Nzc2)",	
            "[<b>Pediatrics NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzIwNzYwMTA0NDQ5NzAz)",	
            "[<b>Pharmacology INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzIxNzYyMTI4ODA0NjMw)",	
            "[<b>Pharmacology NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzIyNzY0MTUzMTU5NTU3)",	
            "[<b>Psychiatry INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzIzNzY2MTc3NTE0NDg0)",	
            "[<b>Psychiatry INICET PYQ(1) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzI0NzY4MjAxODY5NDEx)",	
            "[<b>Psychiatry NEET PG 2023 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzI1NzcwMjI2MjI0MzM4)",	
            "[<b>Radiology INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzI2NzcyMjUwNTc5MjY1)",	
            "[<b>Radiology NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzI3Nzc0Mjc0OTM0MTky)",	
            "[<b>Respiratory Medicine INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzI4Nzc2Mjk5Mjg5MTE5)",	
            "[<b>Surgery INICET PYQ Dr Rajeev Tewari atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzI5Nzc4MzIzNjQ0MDQ2)",	
            "[<b>Surgery INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzMwNzgwMzQ3OTk4OTcz)",	
            "[<b>Surgery NEETPG Recall atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzMxNzgyMzcyMzUzOTAw)",	
            "[<b>Surgery Urology INICET PYQ atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzMyNzg0Mzk2NzA4ODI3)",	
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        damspyq_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"damspyq_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"damspyq_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(damspyq_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("damsspecialtnd"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Anatomy Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzMzNzg2NDIxMDYzNzU0)",
            "[<b>Anesthesia Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzM0Nzg4NDQ1NDE4Njgx)",
            "[<b>Biochemistry App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzM1NzkwNDY5NzczNjA4)",
            "[<b>Dermatology App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzM2NzkyNDk0MTI4NTM1)",
            "[<b>ENT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzM3Nzk0NTE4NDgzNDYy)",
            "[<b>FMT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzM4Nzk2NTQyODM4Mzg5)",
            "[<b>Medicine CNS ENDO App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzM5Nzk4NTY3MTkzMzE2)",
            "[<b>Medicine CVS GIT  Gen App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQwODAwNTkxNTQ4MjQz)",
            "[<b>Medicine Nephro-Rheumat App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQxODAyNjE1OTAzMTcw)",
            "[<b>Microbiology App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQyODA0NjQwMjU4MDk3)",
            "[<b>Gynaecology App test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQzODA2NjY0NjEzMDI0)",
            "[<b>Obstetrics Discussion by Dr Deepti atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQ0ODA4Njg4OTY3OTUx)",
            "[<b>Ophthalmology App T&D (Dr. Sourabh Sharma) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQ1ODEwNzEzMzIyODc4)",
            "[<b>Orthopaedics App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQ2ODEyNzM3Njc3ODA1)",
            "[<b>Patho(Gen path (except neoplasia) and hematology (except WBC) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQ3ODE0NzYyMDMyNzMy)",
            "[<b>Patho(Sys+Neoplasia & WBC) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQ4ODE2Nzg2Mzg3NjU5)",
            "[<b>Pharmacology (ANS,CNS,PNS,CVS,RENAL,BLOOD,RS,GIT ) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzQ5ODE4ODEwNzQyNTg2)",
            "[<b>Pharmacology (GP Endo anti-cancer Anti-microbial Autacoids Miscellaneous) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzUwODIwODM1MDk3NTEz)",
            "[<b>Physiology App test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzUxODIyODU5NDUyNDQw)",
            "[<b>Psychiatry Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzUyODI0ODgzODA3MzY3)",
            "[<b>Radiology Neet App Test and discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzUzODI2OTA4MTYyMjk0)",
            "[<b>Surgery (Uro,Thyroid,Parathryoid,Adrenals,Oral malignancy Glands) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzU0ODI4OTMyNTE3MjIx)",
            "[<b>Surgery GIT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzU1ODMwOTU2ODcyMTQ4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        damsspecialtnd_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"damsspecialtnd_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"damsspecialtnd_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(damsspecialtnd_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("damsclinical"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Anatomy Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzU2ODMyOTgxMjI3MDc1)",
            "[<b>Anesthesia Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzU3ODM1MDA1NTgyMDAy)",
            "[<b>Biochemistry App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzU4ODM3MDI5OTM2OTI5)",
            "[<b>Dermatology App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzU5ODM5MDU0MjkxODU2)",
            "[<b>ENT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzYwODQxMDc4NjQ2Nzgz)",
            "[<b>FMT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzYxODQzMTAzMDAxNzEw)",
            "[<b>Medicine CNS ENDO App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzYyODQ1MTI3MzU2NjM3)",
            "[<b>Medicine CVS GIT  Gen App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzYzODQ3MTUxNzExNTY0)",
            "[<b>Medicine Nephro-Rheumat App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzY0ODQ5MTc2MDY2NDkx)",
            "[<b>Microbiology App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzY1ODUxMjAwNDIxNDE4)",
            "[<b>Gynaecology App test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzY2ODUzMjI0Nzc2MzQ1)",
            "[<b>Obstetrics Discussion by Dr Deepti atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzY3ODU1MjQ5MTMxMjcy)",
            "[<b>Ophthalmology App T&D (Dr. Sourabh Sharma) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzY4ODU3MjczNDg2MTk5)",
            "[<b>Orthopaedics App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzY5ODU5Mjk3ODQxMTI2)",
            "[<b>Patho(Gen path (except neoplasia) and hematology (except WBC) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzcwODYxMzIyMTk2MDUz)",
            "[<b>Patho(Sys+Neoplasia & WBC) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzcxODYzMzQ2NTUwOTgw)",
            "[<b>Pharmacology (ANS,CNS,PNS,CVS,RENAL,BLOOD,RS,GIT ) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzcyODY1MzcwOTA1OTA3)",
            "[<b>Pharmacology (GP Endo anti-cancer Anti-microbial Autacoids Miscellaneous) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzczODY3Mzk1MjYwODM0)",
            "[<b>Physiology App test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzc0ODY5NDE5NjE1NzYx)",
            "[<b>Psychiatry Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzc1ODcxNDQzOTcwNjg4)",
            "[<b>Radiology Neet App Test and discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzc2ODczNDY4MzI1NjE1)",
            "[<b>Surgery (Uro,Thyroid,Parathryoid,Adrenals,Oral malignancy Glands) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzc3ODc1NDkyNjgwNTQy)",
            "[<b>Surgery GIT App Test and Discussion atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzc4ODc3NTE3MDM1NDY5)",
            "[<b>Ear clinical anatomy and disorders - Dr. Deepak Arora atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzc5ODc5NTQxMzkwMzk2)",
            "[<b>Acute kidney injury-Dr. Srinath atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzgwODgxNTY1NzQ1MzIz)",
            "[<b>Chronic Renal Failure, Renal replacement - Dr. Srinath atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzgxODgzNTkwMTAwMjUw)",
            "[<b>Liver-Dr. Arvind atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzgyODg1NjE0NDU1MTc3)",
            "[<b>Respiratory symptoms, PFT , Respiratory disorders-Dr. Bharat Kathi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzgzODg3NjM4ODEwMTA0)",
            "[<b>Basics of Obstetrics - Dr. Anil Mirchandani atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzg0ODg5NjYzMTY1MDMx)",
            "[<b>Early pregnancy complications - Dr. Deepti Bahl atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzg1ODkxNjg3NTE5OTU4)",
            "[<b>Cornea & Conjuctiva - Dr. Manish Chhabra atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzg2ODkzNzExODc0ODg1)",
            "[<b>Genetics-Dr. Sidharth Sethi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzg3ODk1NzM2MjI5ODEy)",
            "[<b>Neonatology-Dr. Ashutosh Aggrawal atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzg4ODk3NzYwNTg0NzM5)",
            "[<b>Nephrology-Dr. Sidharth Sethi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzg5ODk5Nzg0OTM5NjY2)",
            "[<b>Pediatric Endocrine - Dr. Siddharth Sethi atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzkwOTAxODA5Mjk0NTkz)",
            "[<b>Bariatric Surgery & Hernia -Dr. Rajeev Tewari atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzkxOTAzODMzNjQ5NTIw)",
            "[<b>Breast, Thyroid parathyroid - Dr. Gaurav Patel atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzkyOTA1ODU4MDA0NDQ3)",
            "[<b>Esophagus, Stomach, UGI haemorrhage - Dr. Rajeev Tewari atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1NzkzOTA3ODgyMzU5Mzc0)",
            "[<b>Kidney & Adrenal - Dr. Sujoy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1Nzk0OTA5OTA2NzE0MzAx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        damsclinical_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"damsclinical_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"damsclinical_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(damsclinical_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data == "mist":
        mist_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="manatomym"), InlineKeyboardButton("BIOCHEMISTRY", callback_data="mbiochemistrym")],
            [InlineKeyboardButton("PHYSIOLOGY", callback_data="mphysiologym"), InlineKeyboardButton("PHARMACOLOGY", callback_data="mpharmacologym")],
            [InlineKeyboardButton("PATHOLOGY", callback_data="mpathologym"), InlineKeyboardButton("MICROBIOLOGY", callback_data="mmicrobiologym")],
            [InlineKeyboardButton("PSM", callback_data="mpsmm"), InlineKeyboardButton("OPHTHALMOLOGY", callback_data="mophthalmologym")],
            [InlineKeyboardButton("ENT", callback_data="mentm"), InlineKeyboardButton("FMT", callback_data="mfmtm")],
            [InlineKeyboardButton("SURGERY", callback_data="msurgerym"), InlineKeyboardButton("MEDICINE", callback_data="mmedicinem")],
            [InlineKeyboardButton("DERMATOLOGY", callback_data="mdermatologym"), InlineKeyboardButton("PSYCHIATRY", callback_data="mpsychiatrym")],
            [InlineKeyboardButton("ANESTHESIA", callback_data="manesthesiam"), InlineKeyboardButton("RADIOLOGY", callback_data="mradiologym")],
            [InlineKeyboardButton("ORTHOPEDICS", callback_data="morthopedicsm"), InlineKeyboardButton("PEDIATRICS", callback_data="mpediatricsm")],
            [InlineKeyboardButton("OBGY", callback_data="mobgym"), InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(mist_buttons)
        await query.message.edit_reply_markup(reply_markup)

    
    elif query.data.startswith("manatomym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>ANATOMY PART 1 MIST Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTA3MTM2NjM0NDY2MTI1)",
            "[<b>ANATOMY MIST PART 2 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTA4MTM4NjU4ODIxMDUy)",
            "[<b>ANATOMY MIST PART 3  Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTA5MTQwNjgzMTc1OTc5)",
            "[<b>ANATOMY MIST PART 4 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTEwMTQyNzA3NTMwOTA2)",
            "[<b>ANATOMY MIST PART 5 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTExMTQ0NzMxODg1ODMz)",
            "[<b>ANATOMY MIST PART 6 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTEyMTQ2NzU2MjQwNzYw)",
            "[<b>ANATOMY MIST PART 7 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTEzMTQ4NzgwNTk1Njg3)",
            "[<b>ANATOMY MIST PART 7 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTE0MTUwODA0OTUwNjE0)",
            "[<b>ANATOMY MIST PART 8 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTE1MTUyODI5MzA1NTQx)",
            "[<b>ANATOMY MIST PART 9 Dr. Shilpa Agarwal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTE2MTU0ODUzNjYwNDY4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        manatomym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"manatomym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"manatomym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(manatomym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mphysiologm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST PATHOLOGY DR. KUNAL PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTE4MTU4OTAyMzcwMzIy)",
            "[<b>MIST PATHOLOGY DR. KUNAL PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTE5MTYwOTI2NzI1MjQ5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mphysiologm_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mphysiologm_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mphysiologm_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mphysiologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mbiochemistrym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST BIOCHEMISTRY PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTIxMTY0OTc1NDM1MTAz)",
            "[<b>MIST BIOCHEMISTRY PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTIyMTY2OTk5NzkwMDMw)",
            "[<b>MIST BIOCHEMISTRY PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTIzMTY5MDI0MTQ0OTU3)",
            "[<b>MIST BIOCHEMISTRY PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTI0MTcxMDQ4NDk5ODg0)",
            "[<b>MIST BIOCHEMISTRY PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTI1MTczMDcyODU0ODEx)",
            "[<b>MIST BIOCHEMISTRY PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTI2MTc1MDk3MjA5NzM4)",
            "[<b>MIST BIOCHEMISTRY PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTI3MTc3MTIxNTY0NjY1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mbiochemistrym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mbiochemistrym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mbiochemistrym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mbiochemistrym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mpathologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST PATHOLOGY DR. KUNAL PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTI5MTgxMTcwMjc0NTE5)",
            "[<b>MIST PATHOLOGY DR. KUNAL PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTMwMTgzMTk0NjI5NDQ2)",
            "[<b>MIST PATHOLOGY DR. KUNAL PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTMxMTg1MjE4OTg0Mzcz)",
            "[<b>MIST PATHOLOGY DR. KUNAL PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTMyMTg3MjQzMzM5MzAw)",
            "[<b>MIST PATHOLOGY DR. KUNAL PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTMzMTg5MjY3Njk0MjI3)",
            "[<b>MIST PATHOLOGY DR. KUNAL PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTM0MTkxMjkyMDQ5MTU0)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mpathologym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mpathologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mpathologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mpathologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mpharmacologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTM2MTk1MzQwNzU5MDA4)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTM3MTk3MzY1MTEzOTM1)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTM4MTk5Mzg5NDY4ODYy)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTM5MjAxNDEzODIzNzg5)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQwMjAzNDM4MTc4NzE2)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQxMjA1NDYyNTMzNjQz)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQyMjA3NDg2ODg4NTcw)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQzMjA5NTExMjQzNDk3)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQ0MjExNTM1NTk4NDI0)",
            "[<b>MIST PHARMACOLOGY Dr. Saurabh Bhatiya PART 10</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQ1MjEzNTU5OTUzMzUx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mpharmacologym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mpharmacologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mpharmacologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mpharmacologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mpediatricsm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST PEDIATRICS PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQ3MjE3NjA4NjYzMjA1)",
            "[<b>MIST PEDIATRICS PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQ4MjE5NjMzMDE4MTMy)",
            "[<b>MIST PEDIATRICS PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTQ5MjIxNjU3MzczMDU5)",
            "[<b>MIST PEDIATRICS PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTUwMjIzNjgxNzI3OTg2)",
            "[<b>MIST PEDIATRICS PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTUxMjI1NzA2MDgyOTEz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mpediatricsm_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mpediatricsm_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mpediatricsm_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mpediatricsm_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mradiologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST RADIOLOGY PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTUzMjI5NzU0NzkyNzY3)",
            "[<b>MIST RADIOLOGY PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTU0MjMxNzc5MTQ3Njk0)",
            "[<b>MIST RADIOLOGY PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTU1MjMzODAzNTAyNjIx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mradiologym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mradiologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mradiologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mradiologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mpsychiatrym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST PSYCHIATRY PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTU3MjM3ODUyMjEyNDc1)",
            "[<b>MIST PSYCHIATRY PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTU4MjM5ODc2NTY3NDAy)",
            "[<b>MIST PSYCHIATRY PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTU5MjQxOTAwOTIyMzI5)",
            "[<b>MIST PSYCHIATRY PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTYwMjQzOTI1Mjc3MjU2)",
            "[<b>MIST PSYCHIATRY PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTYxMjQ1OTQ5NjMyMTgz)",
            "[<b>MIST PSYCHIATRY PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTYyMjQ3OTczOTg3MTEw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mpsychiatrym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mpsychiatrym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mpsychiatrym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mpsychiatrym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mpsmm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST PSM PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTYzMjQ5OTk4MzQyMDM3)",
            "[<b>MIST PSM PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTY0MjUyMDIyNjk2OTY0)",
            "[<b>MIST PSM PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTY1MjU0MDQ3MDUxODkx)",
            "[<b>MIST PSM PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTY2MjU2MDcxNDA2ODE4)",
            "[<b>MIST PSM PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTY3MjU4MDk1NzYxNzQ1)",
            "[<b>MIST PSM PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTY4MjYwMTIwMTE2Njcy)",
            "[<b>MIST PSM PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTY5MjYyMTQ0NDcxNTk5)",
            "[<b>MIST PSM PART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTcwMjY0MTY4ODI2NTI2)",
            "[<b>MIST PSM PART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTcxMjY2MTkzMTgxNDUz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mpsmm_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mpsmm_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mpsmm_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mpsmm_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mmicrobiologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST MICROBIOLOGY PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTcyMjY4MjE3NTM2Mzgw)",
            "[<b>MIST MICROBIOLOGY PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTczMjcwMjQxODkxMzA3)",
            "[<b>MIST MICROBIOLOGY PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTc0MjcyMjY2MjQ2MjM0)",
            "[<b>MIST MICROBIOLOGY PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTc1Mjc0MjkwNjAxMTYx)",
            "[<b>MIST MICROBIOLOGY PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTc2Mjc2MzE0OTU2MDg4)",
            "[<b>MIST MICROBIOLOGY PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTc3Mjc4MzM5MzExMDE1)",
            "[<b>MIST MICROBIOLOGY PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTc4MjgwMzYzNjY1OTQy)",
            "[<b>MIST MICROBIOLOGY PART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTc5MjgyMzg4MDIwODY5)",
            "[<b>MIST MICROBIOLOGY PART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTgwMjg0NDEyMzc1Nzk2)",
            "[<b>MIST MICROBIOLOGY PART 10</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTgxMjg2NDM2NzMwNzIz)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mmicrobiologym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mmicrobiologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mmicrobiologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mmicrobiologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data.startswith("mophthalmologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST OPHTHALMOLOGY PART 1 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTgyMjg4NDYxMDg1NjUw)",
            "[<b>MIST OPHTHALMOLOGY PART 2 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTgzMjkwNDg1NDQwNTc3)",
            "[<b>MIST OPHTHALMOLOGY PART 3 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTg0MjkyNTA5Nzk1NTA0)",
            "[<b>MIST OPHTHALMOLOGY PART 4 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTg1Mjk0NTM0MTUwNDMx)",
            "[<b>MIST OPHTHALMOLOGY PART 5 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTg2Mjk2NTU4NTA1MzU4)",
            "[<b>MIST OPHTHALMOLOGY PART 6 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTg3Mjk4NTgyODYwMjg1)",
            "[<b>MIST OPHTHALMOLOGY PART 7 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTg4MzAwNjA3MjE1MjEy)",
            "[<b>MIST OPHTHALMOLOGY PART 8 Dr. Anuradha Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTg5MzAyNjMxNTcwMTM5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        m_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mophthalmologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mophthalmologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mophthalmologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("msurgerym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST SURGERY PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTkwMzA0NjU1OTI1MDY2)",
            "[<b>MIST SURGERY PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTkxMzA2NjgwMjc5OTkz)",
            "[<b>MIST SURGERY PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTkyMzA4NzA0NjM0OTIw)",
            "[<b>MIST SURGERY PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTkzMzEwNzI4OTg5ODQ3)",
            "[<b>MIST SURGERY PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTk0MzEyNzUzMzQ0Nzc0)",
            "[<b>MIST SURGERY PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTk1MzE0Nzc3Njk5NzAx)",
            "[<b>MIST SURGERY PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTk2MzE2ODAyMDU0NjI4)",
            "[<b>MIST SURGERY PART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTk3MzE4ODI2NDA5NTU1)",
            "[<b>MIST SURGERY PART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTk4MzIwODUwNzY0NDgy)",
            "[<b>MIST SURGERY PART 10</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE1OTk5MzIyODc1MTE5NDA5)",
            "[<b>MIST SURGERY PART 11</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDAwMzI0ODk5NDc0MzM2)",
            "[<b>MIST SURGERY PART 12</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDAxMzI2OTIzODI5MjYz)",
            "[<b>MIST SURGERY PART 13</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDAyMzI4OTQ4MTg0MTkw)",
            "[<b>MIST SURGERY PART 14</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDAzMzMwOTcyNTM5MTE3)",
            "[<b>MIST SURGERY PART 15</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDA0MzMyOTk2ODk0MDQ0)",
            "[<b>MIST SURGERY PART 16</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDA1MzM1MDIxMjQ4OTcx)",
            "[<b>MIST SURGERY PART 17</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDA2MzM3MDQ1NjAzODk4)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        msurgerym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"msurgerym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"msurgerym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(msurgerym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mentm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST ENT PART 1 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDA3MzM5MDY5OTU4ODI1)",
            "[<b>MIST ENT PART 2 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDA4MzQxMDk0MzEzNzUy)",
            "[<b>MIST ENT PART 3 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDA5MzQzMTE4NjY4Njc5)",
            "[<b>MIST ENT PART 4 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDEwMzQ1MTQzMDIzNjA2)",
            "[<b>MIST ENT PART 5 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDExMzQ3MTY3Mzc4NTMz)",
            "[<b>MIST ENT PART 6 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDEyMzQ5MTkxNzMzNDYw)",
            "[<b>MIST ENT PART 7 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDEzMzUxMjE2MDg4Mzg3)",
            "[<b>MIST ENT PART 8 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDE0MzUzMjQwNDQzMzE0)",
            "[<b>MIST ENT PART 9 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDE1MzU1MjY0Nzk4MjQx)",
            "[<b>MIST ENT PART 10 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDE2MzU3Mjg5MTUzMTY4)",
            "[<b>MIST ENT PART 11 Dr. Rajiv Dhawan</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDE3MzU5MzEzNTA4MDk1)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mentm_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mentm_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mentm_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mentm_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mdermatologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST DERMATOLOGY PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDE4MzYxMzM3ODYzMDIy)",
            "[<b>MIST DERMATOLOGY PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDE5MzYzMzYyMjE3OTQ5)",
            "[<b>MIST DERMATOLOGY PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDIwMzY1Mzg2NTcyODc2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mdermatologym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mdermatologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mdermatologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mdermatologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mobgym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST OBS & GYNE PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDIxMzY3NDEwOTI3ODAz)",
            "[<b>MIST OBS & GYNE PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDIyMzY5NDM1MjgyNzMw)",
            "[<b>MIST OBS & GYNE PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDIzMzcxNDU5NjM3NjU3)",
            "[<b>MIST OBS & GYNE PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDI0MzczNDgzOTkyNTg0)",
            "[<b>MIST OBS & GYNE PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDI1Mzc1NTA4MzQ3NTEx)",
            "[<b>MIST OBS & GYNE PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDI2Mzc3NTMyNzAyNDM4)",
            "[<b>MIST OBS & GYNE PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDI3Mzc5NTU3MDU3MzY1)",
            "[<b>MIST OBS & GYNE PART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDI4MzgxNTgxNDEyMjky)",
            "[<b>MIST OBS & GYNE PART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDI5MzgzNjA1NzY3MjE5)",
            "[<b>MIST OBS & GYNE PART 10</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDMwMzg1NjMwMTIyMTQ2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mobgym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mobgym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mobgym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mobgym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("morthedicsm"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>MIST ORTHOPAEDICS PART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDMxMzg3NjU0NDc3MDcz)",
            "[<b>MIST ORTHOPAEDICS PART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDMyMzg5Njc4ODMyMDAw)",
            "[<b>MIST ORTHOPAEDICS PART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDMzMzkxNzAzMTg2OTI3)",
            "[<b>MIST ORTHOPAEDICS PART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDM0MzkzNzI3NTQxODU0)",
            "[<b>MIST ORTHOPAEDICS PART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDM1Mzk1NzUxODk2Nzgx)",
            "[<b>MIST ORTHOPAEDICS PART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDM2Mzk3Nzc2MjUxNzA4)",
            "[<b>MIST ORTHOPAEDICS PART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDM3Mzk5ODAwNjA2NjM1)",
            "[<b>MIST ORTHOPAEDICS PART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDM4NDAxODI0OTYxNTYy)",
            "[<b>MIST ORTHOPAEDICS PART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDM5NDAzODQ5MzE2NDg5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        morthedicsm_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"morthedicsm_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"morthedicsm_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(morthedicsm_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("mphysiologym"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Mist physiology part 1 Dr Arun Swami</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQwNDA1ODczNjcxNDE2)",
            "[<b>Mist physiology part 2 Dr Arun Swami</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQxNDA3ODk4MDI2MzQz)",
            "[<b>Mist physiology part 3 Dr Arun Swami</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQyNDA5OTIyMzgxMjcw)",
            "[<b>Mist physiology part 4 Dr Arun Swami</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQzNDExOTQ2NzM2MTk3)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        mphysiologym_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"mphysiologym_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"mphysiologym_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(mphysiologym_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("zvradiology"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01. Introduction.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQ0NDEzOTcxMDkxMTI0)",
            "[<b>02. Introduction to Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQ1NDE1OTk1NDQ2MDUx)",
            "[<b>03. Basic Concepts- X-Ray.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQ2NDE4MDE5ODAwOTc4)",
            "[<b>04. Basic Concepts- CT.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQ3NDIwMDQ0MTU1OTA1)",
            "[<b>05. Basic Concepts- MRI.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQ4NDIyMDY4NTEwODMy)",
            "[<b>06. Basic Concepts- USG and DOPPLER.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDQ5NDI0MDkyODY1NzU5)",
            "[<b>07. Basic Concepts- Contrast Media.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDUwNDI2MTE3MjIwNjg2)",
            "[<b>08. Gastrointestinal Radiology - 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDUxNDI4MTQxNTc1NjEz)",
            "[<b>09. Gastrointestinal Radiology - 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDUyNDMwMTY1OTMwNTQw)",
            "[<b>10. Hepatobiliary- Pancreatic Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDUzNDMyMTkwMjg1NDY3)",
            "[<b>11. Cardiovascular Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDU0NDM0MjE0NjQwMzk0)",
            "[<b>12. Respiratory Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDU1NDM2MjM4OTk1MzIx)",
            "[<b>13. Musculoskeletal Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDU2NDM4MjYzMzUwMjQ4)",
            "[<b>14. Neuroradiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDU3NDQwMjg3NzA1MTc1)",
            "[<b>15. Uro- Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDU4NDQyMzEyMDYwMTAy)",
            "[<b>16. Gynecology-Obstetrics Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDU5NDQ0MzM2NDE1MDI5)",
            "[<b>17. Breast Radiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDYwNDQ2MzYwNzY5OTU2)",
            "[<b>18. Nuclear Medicine.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDYxNDQ4Mzg1MTI0ODgz)",
            "[<b>19. Radiotherapy.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDYyNDUwNDA5NDc5ODEw)",
            "[<b>100 Radiology Images in order of importance - Part 1 ｜ Dr Zainab Vora 720p30fps 430.webm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDYzNDUyNDMzODM0NzM3)",
            "[<b>100 Radiology Images in order of importance - Part 2 ｜ Dr Zainab Vora 720p30fps 430.webm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDY0NDU0NDU4MTg5NjY0)",
            "[<b>100 Radiology Images in order of importance - Part 3 ｜ Dr Zainab Vora 720p30fps 485.webm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDY1NDU2NDgyNTQ0NTkx)",
            "[<b>Radiology Crash Course ｜ FMGE & NEET PG  ｜ Dr Zainab Vora 720p30fps 370.webm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDY2NDU4NTA2ODk5NTE4)",
            "[<b>Radiology Crash Course - 3 ｜ FMGE & NEET PG  ｜ Dr Zainab Vora 720p30fps 467.webm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDY3NDYwNTMxMjU0NDQ1)",
            "[<b>Radiology Crash Course - 4 ｜ FMGE & NEET PG  ｜ Dr Zainab Vora 720p30fps 525.webm</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDY4NDYyNTU1NjA5Mzcy)",
            "[<b>Radio Rapid revision  by Dr Zainab Vohra part 1 720p25.0fps 1177.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDY5NDY0NTc5OTY0Mjk5)",
            "[<b>Radio Rapid revision  by Dr Zainab Vohra part 2 720p25.0fps 1311.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDcwNDY2NjA0MzE5MjI2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        zvradiology_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"zvradiology_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"zvradiology_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(zvradiology_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    
    elif query.data.startswith("rdent"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>01. Cartilages of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDg4NTAzMDQyNzA3OTEy)",
            "[<b>02. Membranes of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDg5NTA1MDY3MDYyODM5)",
            "[<b>03. Mucosa of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDkwNTA3MDkxNDE3NzY2)",
            "[<b>04. Pitch Disorders of Voice atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDkxNTA5MTE1NzcyNjkz)",
            "[<b>05. Supraglottis and Subglottis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDkyNTExMTQwMTI3NjIw)",
            "[<b>06. Glottis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDkzNTEzMTY0NDgyNTQ3)",
            "[<b>07. Lymphatic Drainage and Spaces of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDk0NTE1MTg4ODM3NDc0)",
            "[<b>08. Difference between Paediatric and Adult Larynx Stridor atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDk1NTE3MjEzMTkyNDAx)",
            "[<b>09. Paediatric Laryngeal Infection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDk2NTE5MjM3NTQ3MzI4)",
            "[<b>10. Congenital Disorders of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDk3NTIxMjYxOTAyMjU1)",
            "[<b>11. Methods of Larynx Examination atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDk4NTIzMjg2MjU3MTgy)",
            "[<b>12. Voice Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDk5NTI1MzEwNjEyMTA5)",
            "[<b>13. Functions, Muscles & Nerve supply atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTAwNTI3MzM0OTY3MDM2)",
            "[<b>14. Vocal Cord Paralysis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTAxNTI5MzU5MzIxOTYz)",
            "[<b>15. Cancer Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTAyNTMxMzgzNjc2ODkw)",
            "[<b>16. Neck Nodes & Radical Neck Dissection atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTAzNTMzNDA4MDMxODE3)",
            "[<b>17. Tracheostomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTA0NTM1NDMyMzg2NzQ0)",
            "[<b>18. Airway Foreign Body atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTA1NTM3NDU2NzQxNjcx)",
            "[<b>19. Miscellaneous diseases of Larynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTA2NTM5NDgxMDk2NTk4)",
            "[<b>01. Applied Anatomy atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTA3NTQxNTA1NDUxNTI1)",
            "[<b>02. Laryngopharynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTA4NTQzNTI5ODA2NDUy)",
            "[<b>03. Adenoid atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTA5NTQ1NTU0MTYxMzc5)",
            "[<b>04. Angiofibroma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTEwNTQ3NTc4NTE2MzA2)",
            "[<b>05. Nasopharyngeal Carcinoma atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTExNTQ5NjAyODcxMjMz)",
            "[<b>06. Oropharynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTEyNTUxNjI3MjI2MTYw)",
            "[<b>07. Tonsil atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTEzNTUzNjUxNTgxMDg3)",
            "[<b>08. Abscesses of Pharynx atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTE0NTU1Njc1OTM2MDE0)",
            "[<b>01. External Nose atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTE1NTU3NzAwMjkwOTQx)",
            "[<b>02. Lateral Wall of Nose atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTE2NTU5NzI0NjQ1ODY4)",
            "[<b>03. Paranasal Sinuses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTE3NTYxNzQ5MDAwNzk1)",
            "[<b>04. Ethmoid Air Cells atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTE4NTYzNzczMzU1NzIy)",
            "[<b>05. Sinuses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTE5NTY1Nzk3NzEwNjQ5)",
            "[<b>06. Sinusitis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTIwNTY3ODIyMDY1NTc2)",
            "[<b>07. Nasal Polyp atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTIxNTY5ODQ2NDIwNTAz)",
            "[<b>08. Allergic fungal Rhinosinusitis and Mucormycosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTIyNTcxODcwNzc1NDMw)",
            "[<b>09. Neoplasm of Nose and Sinuses atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTIzNTczODk1MTMwMzU3)",
            "[<b>10. Atrophic Rhinitis, Rhinoscleroma, Rhinosporidiosis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTI0NTc1OTE5NDg1Mjg0)",
            "[<b>11. Facial Trauma, CSF Rhinorrhoea atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTI1NTc3OTQzODQwMjEx)",
            "[<b>12. Nasal Septum & Disorders atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTI2NTc5OTY4MTk1MTM4)",
            "[<b>13. Olfaction atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTI3NTgxOTkyNTUwMDY1)",
            "[<b>14. Blood Supply of Nose & Epistaxis atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTI4NTg0MDE2OTA0OTky)",
            "[<b>15. Miscellaneous disorders of Nose atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTI5NTg2MDQxMjU5OTE5)",
            "[<b>01. Embryological Development of Ear.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTMwNTg4MDY1NjE0ODQ2)",
            "[<b>02. Middle Ear Ossicles & Mechanics.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTMxNTkwMDg5OTY5Nzcz)",
            "[<b>03. Pinna.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTMyNTkyMTE0MzI0NzAw)",
            "[<b>04. Exteral Auditory Canal.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTMzNTk0MTM4Njc5NjI3)",
            "[<b>05. Tympanic Membrane.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTM0NTk2MTYzMDM0NTU0)",
            "[<b>06. Eustachian Tube.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTM1NTk4MTg3Mzg5NDgx)",
            "[<b>07. Middle Ear.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTM2NjAwMjExNzQ0NDA4)",
            "[<b>08. Middle Ear Cleft - ASOM - Safe CSOM.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTM3NjAyMjM2MDk5MzM1)",
            "[<b>09. Acute Mastoiditis -Petrositis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTM4NjA0MjYwNDU0MjYy)",
            "[<b>10. Unsafe CSOM.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTM5NjA2Mjg0ODA5MTg5)",
            "[<b>11. Inner Ear -Basics, Cochlea, Utricle, Saccule.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQwNjA4MzA5MTY0MTE2)",
            "[<b>12. Inner Ear-Semicircular Canals, Vestibular Tests, Vertigo.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQxNjEwMzMzNTE5MDQz)",
            "[<b>13. Inner Ear-VEMP, Superior SCC dehiscence.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQyNjEyMzU3ODczOTcw)",
            "[<b>14. Inner Ear-VC Nerve, IAC & Auditory Pathway.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQzNjE0MzgyMjI4ODk3)",
            "[<b>15. Basics, Tuning Fork Tests.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQ0NjE2NDA2NTgzODI0)",
            "[<b>16. Pure Tone Audiometry ,ABLB, SISI, SDS & Tone Decay.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQ1NjE4NDMwOTM4NzUx)",
            "[<b>17. BERA, OAE, ECochG, Impedance Audiometry.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQ2NjIwNDU1MjkzNjc4)",
            "[<b>18. Miscellaneous Disorders of Ear.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQ3NjIyNDc5NjQ4NjA1)",
            "[<b>19. Glomus Jugulare.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQ4NjI0NTA0MDAzNTMy)",
            "[<b>20. Otosclerosis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTQ5NjI2NTI4MzU4NDU5)",
            "[<b>21. Acoustic Neuroma.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTUwNjI4NTUyNzEzMzg2)",
            "[<b>22. Meniere& Disease.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTUxNjMwNTc3MDY4MzEz)",
            "[<b>23. Anatomy of Facial Nerve.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTUyNjMyNjAxNDIzMjQw)",
            "[<b>24. Bell& Palsy.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTUzNjM0NjI1Nzc4MTY3)",
            "[<b>25. Syndromes of Facial Nerve disorders.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTU0NjM2NjUwMTMzMDk0)",
            "[<b>26. Surgical Landmarks and Injury.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTU1NjM4Njc0NDg4MDIx)",
            "[<b>27. Hearing Devices & Implants.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTU2NjQwNjk4ODQyOTQ4)",
            "[<b>01. ENT Instruments Part 1 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTU3NjQyNzIzMTk3ODc1)",
            "[<b>02. ENT Instruments Part 2 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTU4NjQ0NzQ3NTUyODAy)",
            "[<b>03. Examination Under Microscope(EUM) atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTU5NjQ2NzcxOTA3NzI5)",
            "[<b>04. Functional Endoscopic Sinus Surgery Instruments atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTYwNjQ4Nzk2MjYyNjU2)",
            "[<b>05. Cochlear Implant Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTYxNjUwODIwNjE3NTgz)",
            "[<b>06. MLS - Micro Laryngeal Surgery atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTYyNjUyODQ0OTcyNTEw)",
            "[<b>07. Various steps of Septoplasty atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTYzNjU0ODY5MzI3NDM3)",
            "[<b>01. NEET PG 2023 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTY0NjU2ODkzNjgyMzY0)",
            "[<b>02. NEET PG 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTY1NjU4OTE4MDM3Mjkx)",
            "[<b>03. NEET PG 2021 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTY2NjYwOTQyMzkyMjE4)",
            "[<b>04. NEET PG 2020 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTY3NjYyOTY2NzQ3MTQ1)",
            "[<b>01. INI CET May 2022 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTY4NjY0OTkxMTAyMDcy)",
            "[<b>02. INI CET Nov 2021 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTY5NjY3MDE1NDU2OTk5)",
            "[<b>03. INI CET July 2021 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTcwNjY5MDM5ODExOTI2)",
            "[<b>04. INI CET May & Nov 2020 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTcxNjcxMDY0MTY2ODUz)",
            "[<b>05. INI CET May & Nov 2019 atf.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MTcyNjczMDg4NTIxNzgw)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        rdent_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"rdent_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"rdent_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(rdent_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data == "cerebellum":
        cerebellum_buttons = [
            [InlineKeyboardButton("ANATOMY", callback_data="canatomyr"), InlineKeyboardButton("PHARMACOLOGY", callback_data="cpharmacologyr")],     
            [InlineKeyboardButton("ANESTHESIA", callback_data="canesthesiar"), InlineKeyboardButton("RADIOLOGY", callback_data="cradiologyr")],
            [InlineKeyboardButton("PEDIATRICS", callback_data="cpediatricsr")],            
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(cerebellum_buttons)
        await query.message.edit_reply_markup(reply_markup)

    elif query.data.startswith("canesthesiar"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.How to Study Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjQ5NjM2NjgxNDY3MDMy)",
            "[<b>1.How to Study Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjUwNjM4NzA1ODIxOTU5)",
            "[<b>10.Neuromuscular Blocking Drugs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjUxNjQwNzMwMTc2ODg2)",
            "[<b>11.Regional Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjUyNjQyNzU0NTMxODEz)",
            "[<b>12.Cardiopulmonary Resuscitation.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjUzNjQ0Nzc4ODg2NzQw)",
            "[<b>13.Pediatric Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjU0NjQ2ODAzMjQxNjY3)",
            "[<b>14.Obstetric Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjU1NjQ4ODI3NTk2NTk0)",
            "[<b>15.Anesthetic Implication of Concurrent Diseases.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjU2NjUwODUxOTUxNTIx)",
            "[<b>2.Introduction of Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjU3NjUyODc2MzA2NDQ4)",
            "[<b>3.Day Care Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjU4NjU0OTAwNjYxMzc1)",
            "[<b>4.Monitoring in Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjU5NjU2OTI1MDE2MzAy)",
            "[<b>5.Pre-Anesthesia Evaluation.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjYwNjU4OTQ5MzcxMjI5)",
            "[<b>6.Instruments in Anesthesia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjYxNjYwOTczNzI2MTU2)",
            "[<b>7.Inhalational Anesthetic Agents.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjYyNjYyOTk4MDgxMDgz)",
            "[<b>8.Intravenous Anesthetic Agents.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjYzNjY1MDIyNDM2MDEw)",
            "[<b>9.Local Anesthetics.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjY0NjY3MDQ2NzkwOTM3)",
            "[<b>How & Where to Start.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjY1NjY5MDcxMTQ1ODY0)",
            "[<b>Amsterdam Dwarfism, Patau Syndrome, Types of Dactyly.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjY2NjcxMDk1NTAwNzkx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        canesthesiar_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"canesthesiar_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"canesthesiar_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(canesthesiar_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("cpediatricsr"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>How & Where to Start.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjY3NjczMTE5ODU1NzE4)",
            "[<b>Amsterdam Dwarfism, Patau Syndrome, Types of Dactyly.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjY4Njc1MTQ0MjEwNjQ1)",
            "[<b>Case Presentation 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjY5Njc3MTY4NTY1NTcy)",
            "[<b>Case Presentation 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjcwNjc5MTkyOTIwNDk5)",
            "[<b>Case Presentation 3.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjcxNjgxMjE3Mjc1NDI2)",
            "[<b>Case Presentation 4.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjcyNjgzMjQxNjMwMzUz)",
            "[<b>Case Presentation 5.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjczNjg1MjY1OTg1Mjgw)",
            "[<b>Dentition.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njc0Njg3MjkwMzQwMjA3)",
            "[<b>Down Syndrome PYQs with Recent Updates.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njc1Njg5MzE0Njk1MTM0)",
            "[<b>Growth Chart & X-ray Wrist.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njc2NjkxMzM5MDUwMDYx)",
            "[<b>Head Circumference.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njc3NjkzMzYzNDA0OTg4)",
            "[<b>Fetal Alcohol, Crouzon, Waardenburg Syndrome, Cleidocranial Dystosis, Turner Syndrome, Treacher Collins & Weaver Syndrome.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njc4Njk1Mzg3NzU5OTE1)",
            "[<b>Important Dates, Definition, Anthropometry, Legal Age Definition.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njc5Njk3NDEyMTE0ODQy)",
            "[<b>Marfan Syndrome, Potter Sequence & Down Syndrome.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjgwNjk5NDM2NDY5NzY5)",
            "[<b>Microcephaly vs Macrocephaly.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjgxNzAxNDYwODI0Njk2)",
            "[<b>Mile Stones – Fine Motor, Personal & Social, Language, Vision & Hearing.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjgyNzAzNDg1MTc5NjIz)",
            "[<b>Mile Stones – Gross Motor.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjgzNzA1NTA5NTM0NTUw)",
            "[<b>Rubinstein Taybi, Cri Du Chat & Edward Syndrome.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njg0NzA3NTMzODg5NDc3)",
            "[<b>Short Stature.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njg1NzA5NTU4MjQ0NDA0)",
            "[<b>SMR Staging.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njg2NzExNTgyNTk5MzMx)",
            "[<b>APGAR Score .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njg3NzEzNjA2OTU0MjU4)",
            "[<b>Approach to a Newborn with Hepatitis B+ Mother, Pulse Oximeter.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njg4NzE1NjMxMzA5MTg1)",
            "[<b>Babinski Response, Types of Hypothermia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njg5NzE3NjU1NjY0MTEy)",
            "[<b>Birth Asphyxia-HIE .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjkwNzE5NjgwMDE5MDM5)",
            "[<b>Caput Succedaneum vs Cephal Hematoma .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjkxNzIxNzA0MzczOTY2)",
            "[<b>Definition, Classification.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjkyNzIzNzI4NzI4ODkz)",
            "[<b>Delayed Cord Clamping.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NjkzNzI1NzUzMDgzODIw)",
            "[<b>Hyaline Membrane Disease .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njk0NzI3Nzc3NDM4NzQ3)",
            "[<b>Infant of Diabetic Mother .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njk1NzI5ODAxNzkzNjc0)",
            "[<b>IUGR (Intrauterine Growth Restriction) .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njk2NzMxODI2MTQ4NjAx)",
            "[<b>IVH .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njk3NzMzODUwNTAzNTI4)",
            "[<b>Kangaroo Mother Care .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njk4NzM1ODc0ODU4NDU1)",
            "[<b>LGA, Causes, Beckwith Widemann Syndrome, Wilm's Tumour.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Njk5NzM3ODk5MjEzMzgy)",
            "[<b>Meconium Aspiration Syndrome .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzAwNzM5OTIzNTY4MzA5)",
            "[<b>Microdeletion Syndromes, Vitals, Stool Colour, Expanded New Ballard Score.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzAxNzQxOTQ3OTIzMjM2)",
            "[<b>Necrotising Enterocolitis .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzAyNzQzOTcyMjc4MTYz)",
            "[<b>Neonatal Hyperbilirubinemia .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzAzNzQ1OTk2NjMzMDkw)",
            "[<b>Neonatal Hypoglycemia .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzA0NzQ4MDIwOTg4MDE3)",
            "[<b>Neonatal Seizure - PYQs .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzA1NzUwMDQ1MzQyOTQ0)",
            "[<b>Neonatal Resuscitation Protocol.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzA2NzUyMDY5Njk3ODcx)",
            "[<b>Neonatal Seizure .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzA3NzU0MDk0MDUyNzk4)",
            "[<b>pediatric dermatology .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzA4NzU2MTE4NDA3NzI1)",
            "[<b>Pediatric Orthopedics, Ortolani & Barlow Tests.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzA5NzU4MTQyNzYyNjUy)",
            "[<b>pyqs Neonatal Reflexes.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzEwNzYwMTY3MTE3NTc5)",
            "[<b>PYQs Birth Asphyxia .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzExNzYyMTkxNDcyNTA2)",
            "[<b>Pediatric Ophthalmology - ROP .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzEyNzY0MjE1ODI3NDMz)",
            "[<b>PYQs - Neonatal Jaundice .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzEzNzY2MjQwMTgyMzYw)",
            "[<b>ROP - PYQs .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzE0NzY4MjY0NTM3Mjg3)",
            "[<b>Neonatal Sepsis .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzE1NzcwMjg4ODkyMjE0)",
            "[<b>Silverman Anderson Score, Downe Score, Neonatal Reflexes (intro).mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzE2NzcyMzEzMjQ3MTQx)",
            "[<b>Transient Tachypnea of Newborn & Apnea of Prematurity .mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzE3Nzc0MzM3NjAyMDY4)",
            "[<b>Types of Fat, Non-shivering Thermogenesis, Hypothermia, Warm Chain.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzE4Nzc2MzYxOTU2OTk1)",
            "[<b>Acute Pharyngitis, Croup, Acute Epiglottitis, Diphtheria.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzE5Nzc4Mzg2MzExOTIy)",
            "[<b>Asthma - PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzIwNzgwNDEwNjY2ODQ5)",
            "[<b>Asthma.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzIxNzgyNDM1MDIxNzc2)",
            "[<b>Bronchiolitis, Whooping Cough, Bronchiolitis Obliterans.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzIyNzg0NDU5Mzc2NzAz)",
            "[<b>Congenital Malformations.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzIzNzg2NDgzNzMxNjMw)",
            "[<b>Cystic Fibrosis.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzI0Nzg4NTA4MDg2NTU3)",
            "[<b>IMNCI Protocol - Pneumonia Atypical vs Typical.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzI1NzkwNTMyNDQxNDg0)",
            "[<b>Kartagener Syndrome, Stridor, Laryngomalacia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzI2NzkyNTU2Nzk2NDEx)",
            "[<b>Acute Rheumatic Fever Part 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzI3Nzk0NTgxMTUxMzM4)",
            "[<b>Acute Rheumatic Fever Part 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzI4Nzk2NjA1NTA2MjY1)",
            "[<b>ASD.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzI5Nzk4NjI5ODYxMTky)",
            "[<b>Case Presentation 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzMwODAwNjU0MjE2MTE5)",
            "[<b>Case Presentation 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzMxODAyNjc4NTcxMDQ2)",
            "[<b>Case Presentation 3.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzMyODA0NzAyOTI1OTcz)",
            "[<b>Case Presentation 4.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzMzODA2NzI3MjgwOTAw)",
            "[<b>Case Presentation 5.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzM0ODA4NzUxNjM1ODI3)",
            "[<b>Congenital Heart Disease Classification.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzM1ODEwNzc1OTkwNzU0)",
            "[<b>Congestive Cardiac Failure.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzM2ODEyODAwMzQ1Njgx)",
            "[<b>Fetal Circulation.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzM3ODE0ODI0NzAwNjA4)",
            "[<b>How to Calculate Heart Rate in ECG, NADAS Criteria.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzM4ODE2ODQ5MDU1NTM1)",
            "[<b>Innocent Murmur, Normal Heart Rate, Small Case, PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzM5ODE4ODczNDEwNDYy)",
            "[<b>PDA.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQwODIwODk3NzY1Mzg5)",
            "[<b>Rheumatic Heart Disease with Cardio Revision.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQxODIyOTIyMTIwMzE2)",
            "[<b>Syndromes with Radial Deficiency, William Syndrome, Di George Syndrome.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQyODI0OTQ2NDc1MjQz)",
            "[<b>TAPVC, Ebstein, Truncus Arteriosus & TOF - Part 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQzODI2OTcwODMwMTcw)",
            "[<b>TGA, Lutembacher's Syndrome, Differential vs Reverse Differential Cyanosis.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQ0ODI4OTk1MTg1MDk3)",
            "[<b>TOF - Part 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQ1ODMxMDE5NTQwMDI0)",
            "[<b>VSD.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQ2ODMzMDQzODk0OTUx)",
            "[<b>Breath Holding Spells, Nocturnal Enuresis, Autism, Asperger Syndrome, ADHD.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQ3ODM1MDY4MjQ5ODc4)",
            "[<b>Pica, Thumb Sucking, Tics, Bruxism, Anorexia Nervosa.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQ4ODM3MDkyNjA0ODA1)",
            "[<b>Case Presentation.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzQ5ODM5MTE2OTU5NzMy)",
            "[<b>Examination of CNS.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzUwODQxMTQxMzE0NjU5)",
            "[<b>Febrile Seizures with PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzUxODQzMTY1NjY5NTg2)",
            "[<b>Hydrocephalus.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzUyODQ1MTkwMDI0NTEz)",
            "[<b>Neural Tube Defects Part-1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzUzODQ3MjE0Mzc5NDQw)",
            "[<b>Neural Tube Defects Part-2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzU0ODQ5MjM4NzM0MzY3)",
            "[<b>Neurocutaneous Syndromes.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzU1ODUxMjYzMDg5Mjk0)",
            "[<b>Neurocysticerosis.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzU2ODUzMjg3NDQ0MjIx)",
            "[<b>WEST Sydrome, Status Epilepticus, Bacterial Meningitis, Tubercular Meningitis with PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzU3ODU1MzExNzk5MTQ4)",
            "[<b>TORCH Profile.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzU4ODU3MzM2MTU0MDc1)",
            "[<b>Churg Strauss syndrome, Wegener’s granulomatosis, Bechet syndrome, Juvenile dermatomyositis.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzU5ODU5MzYwNTA5MDAy)",
            "[<b>Henoch Schonlein Purpura.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzYwODYxMzg0ODYzOTI5)",
            "[<b>Composition  Colostrum  Foremilk  Hind milk  Anti Infective Factors.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzYxODYzNDA5MjE4ODU2)",
            "[<b>Takayasu Arteritis.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzYyODY1NDMzNTczNzgz)",
            "[<b>Kawasaki Disease.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzYzODY3NDU3OTI4NzEw)",
            "[<b>Introduction.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzY0ODY5NDgyMjgzNjM3)",
            "[<b>MCQs  PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzY1ODcxNTA2NjM4NTY0)",
            "[<b>WHO classification  Features  Complication.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzY2ODczNTMwOTkzNDkx)",
            "[<b>Vitamin C - Scurvy, PYQs & Discussion of all Other Micronutrients.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzY3ODc1NTU1MzQ4NDE4)",
            "[<b>BCG Vaccine.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzY4ODc3NTc5NzAzMzQ1)",
            "[<b>DPT, Hib, PCV Vaccine.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzY5ODc5NjA0MDU4Mjcy)",
            "[<b>Introduction.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzcwODgxNjI4NDEzMTk5)",
            "[<b>MMR, Chicken Pox, Rotavirus, Rabies Vaccine.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzcxODgzNjUyNzY4MTI2)",
            "[<b>Polio Vaccine + Hepatitis B Vaccine.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzcyODg1Njc3MTIzMDUz)",
            "[<b>Approach to a Case of Anaemia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzczODg3NzAxNDc3OTgw)",
            "[<b>Approach to Fever with Rash, Measles, Roseola Infantum, Erythema Infectiosum, Varicella, Mumps.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzc0ODg5NzI1ODMyOTA3)",
            "[<b>Dengue Fever.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzc1ODkxNzUwMTg3ODM0)",
            "[<b>Enteric Fever.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzc2ODkzNzc0NTQyNzYx)",
            "[<b>Iron Deficiency Anaemia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzc3ODk1Nzk4ODk3Njg4)",
            "[<b>Malaria.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzc4ODk3ODIzMjUyNjE1)",
            "[<b>PYQs of Malaria & ITP.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzc5ODk5ODQ3NjA3NTQy)",
            "[<b>Sickle Cell Anemia, Acute Chest Syndrome.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzgwOTAxODcxOTYyNDY5)",
            "[<b>Tuberculosis, Rubella.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzgxOTAzODk2MzE3Mzk2)",
            "[<b>Management of Nephrotic Syndrome with PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzgyOTA1OTIwNjcyMzIz)",
            "[<b>Nephrotic Syndrome.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzgzOTA3OTQ1MDI3MjUw)",
            "[<b>Urinary Tract Infection.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzg0OTA5OTY5MzgyMTc3)",
            "[<b>CHPS - Congenital Hypertropic Pyloric Stenosis.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzg1OTExOTkzNzM3MTA0)",
            "[<b>Hirschsprung's Disease & Full System Revision PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzg2OTE0MDE4MDkyMDMx)",
            "[<b>Muscular Dystrophy.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzg3OTE2MDQyNDQ2OTU4)",
            "[<b>Osteogenesis Imperfecta.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzg4OTE4MDY2ODAxODg1)",
            "[<b>TEF.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzg5OTIwMDkxMTU2ODEy)",
            "[<b>Acute Liver Failure.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzkwOTIyMTE1NTExNzM5)",
            "[<b>Celiac Disease.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzkxOTI0MTM5ODY2NjY2)",
            "[<b>Diarrhea + Acrodermatitis Enteropathica with PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzkyOTI2MTY0MjIxNTkz)",
            "[<b>Diarrhea.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2NzkzOTI4MTg4NTc2NTIw)",
            "[<b>GERD.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzk0OTMwMjEyOTMxNDQ3)",
            "[<b>Hypocalcemia & Hypercalcemia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzk1OTMyMjM3Mjg2Mzc0)",
            "[<b>Hyponatremia.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzk2OTM0MjYxNjQxMzAx)",
            "[<b>Galactosemia, Hereditary Fructose Intolerance.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzk3OTM2Mjg1OTk2MjI4)",
            "[<b>How to Approach a Case of IEM with Glycogen Storage Disease.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzk4OTM4MzEwMzUxMTU1)",
            "[<b>Mapple Syrup Urine Disease.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2Nzk5OTQwMzM0NzA2MDgy)",
            "[<b>Menke Disease.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODAwOTQyMzU5MDYxMDA5)",
            "[<b>Organic Acidemias, Multiple Carboxylase Deficiency.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODAxOTQ0MzgzNDE1OTM2)",
            "[<b>Phenylalanine Metabolism Pathway, Alkaptonuria, PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODAyOTQ2NDA3NzcwODYz)",
            "[<b>Tay Sachs Disease, Phenylketonuria.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODAzOTQ4NDMyMTI1Nzkw)",
            "[<b>Tyrosinemia, Hartnup Disorder, Homocysteinuria, PYQs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODA0OTUwNDU2NDgwNzE3)",
            "[<b>White Matter Disease, Krabbe Disease, Canavan Disease, Metachromatic Leukodystrophy.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODA1OTUyNDgwODM1NjQ0)",
            "[<b>Wilson Disease.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODA2OTU0NTA1MTkwNTcx)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        cpediatricsr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"cpediatricsr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"cpediatricsr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(cpediatricsr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("cradiologyr"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>1.Introduction.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODA3OTU2NTI5NTQ1NDk4)",
            "[<b>Radiology quick revision.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODA4OTU4NTUzOTAwNDI1)",
            "[<b>1.Introduction.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODA5OTYwNTc4MjU1MzUy)",
            "[<b>10.Women's Imaging.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODEwOTYyNjAyNjEwMjc5)",
            "[<b>11.Neuroradiology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODExOTY0NjI2OTY1MjA2)",
            "[<b>12.Respiratory Radiology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODEyOTY2NjUxMzIwMTMz)",
            "[<b>13.CVS Radiology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODEzOTY4Njc1Njc1MDYw)",
            "[<b>15.Nuclear Medicine.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODE0OTcwNzAwMDI5OTg3)",
            "[<b>16.Radiotherapy.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODE1OTcyNzI0Mzg0OTE0)",
            "[<b>18.Named X-Ray Views.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODE2OTc0NzQ4NzM5ODQx)",
            "[<b>14.MSK Imaging.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODE3OTc2NzczMDk0NzY4)",
            "[<b>17.Radiological Anatomy.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODE4OTc4Nzk3NDQ5Njk1)",
            "[<b>4.MRI.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODE5OTgwODIxODA0NjIy)",
            "[<b>2.X-rays.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODIwOTgyODQ2MTU5NTQ5)",
            "[<b>3.CT.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODIxOTg0ODcwNTE0NDc2)",
            "[<b>5.USG.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODIyOTg2ODk0ODY5NDAz)",
            "[<b>6.Contrast Media.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODIzOTg4OTE5MjI0MzMw)",
            "[<b>7.Gastrointestinal Radiology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODI0OTkwOTQzNTc5MjU3)",
            "[<b>8.Genito-Urinary Radiology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODI1OTkyOTY3OTM0MTg0)",
            "[<b>9.Hepatobiliary-Pancreatic Radiology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODI2OTk0OTkyMjg5MTEx)",
            "[<b>Radiology quick revision.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODI3OTk3MDE2NjQ0MDM4)",
            "[<b>revision-2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODI4OTk5MDQwOTk4OTY1)",
            "[<b>revision-1.part001.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODMwMDAxMDY1MzUzODky)",
            "[<b>revision-1.part002.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODMxMDAzMDg5NzA4ODE5)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        cradiologyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"cradiologyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"cradiologyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(cradiologyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("canatomyr"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>abdominal viscera.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODMyMDA1MTE0MDYzNzQ2)",
            "[<b>anterior abdominal wall.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODMzMDA3MTM4NDE4Njcz)",
            "[<b>arteries and veins of git.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODM0MDA5MTYyNzczNjAw)",
            "[<b>esophagus and stomach.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODM1MDExMTg3MTI4NTI3)",
            "[<b>perineum and pelvic viscera part 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODM2MDEzMjExNDgzNDU0)",
            "[<b>perineum and pelvic viscera part 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODM3MDE1MjM1ODM4Mzgx)",
            "[<b>peritoneum and abdominal ligaments.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODM4MDE3MjYwMTkzMzA4)",
            "[<b>small intestine and large intestine.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODM5MDE5Mjg0NTQ4MjM1)",
            "[<b>Basic Concept, Tricks and Magic of Anatomy.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQwMDIxMzA4OTAzMTYy)",
            "[<b>blood supply of brain.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQxMDIzMzMzMjU4MDg5)",
            "[<b>brain stem.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQyMDI1MzU3NjEzMDE2)",
            "[<b>cerebellum.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQzMDI3MzgxOTY3OTQz)",
            "[<b>cerebral hemisphere.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQ0MDI5NDA2MzIyODcw)",
            "[<b>cranial nerves.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQ1MDMxNDMwNjc3Nzk3)",
            "[<b>spinal cord.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQ2MDMzNDU1MDMyNzI0)",
            "[<b>white matter and basal nuclei.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQ3MDM1NDc5Mzg3NjUx)",
            "[<b>CNS development.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQ4MDM3NTAzNzQyNTc4)",
            "[<b>CVS development.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODQ5MDM5NTI4MDk3NTA1)",
            "[<b>general embryology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODUwMDQxNTUyNDUyNDMy)",
            "[<b>GIT development.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODUxMDQzNTc2ODA3MzU5)",
            "[<b>kidney,male and female genital tract development.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODUyMDQ1NjAxMTYyMjg2)",
            "[<b>pharyngeal apparatus part 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODUzMDQ3NjI1NTE3MjEz)",
            "[<b>pharyngeal apparatus part 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODU0MDQ5NjQ5ODcyMTQw)",
            "[<b>joints summary.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODU1MDUxNjc0MjI3MDY3)",
            "[<b>joints.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODU2MDUzNjk4NTgxOTk0)",
            "[<b>muscles and movements.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODU3MDU1NzIyOTM2OTIx)",
            "[<b>position, planes, terminology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODU4MDU3NzQ3MjkxODQ4)",
            "[<b>arteries, veins and nerves of face.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODU5MDU5NzcxNjQ2Nzc1)",
            "[<b>cranial cavity , cranial nerves and vessels.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODYwMDYxNzk2MDAxNzAy)",
            "[<b>folds of duramater and sinuses of brain.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODYxMDYzODIwMzU2NjI5)",
            "[<b>neck.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODYyMDY1ODQ0NzExNTU2)",
            "[<b>parasympathetic ganglion.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODYzMDY3ODY5MDY2NDgz)",
            "[<b>pharynx,larynx,nose and palate.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODY0MDY5ODkzNDIxNDEw)",
            "[<b>scalp and face.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODY1MDcxOTE3Nzc2MzM3)",
            "[<b>basics of histopathology.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODY2MDczOTQyMTMxMjY0)",
            "[<b>cartilage and bone.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODY3MDc1OTY2NDg2MTkx)",
            "[<b>epithelium and glands.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODY4MDc3OTkwODQxMTE4)",
            "[<b>lymphoid tissue.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODY5MDgwMDE1MTk2MDQ1)",
            "[<b>anterior comparment of thigh.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODcwMDgyMDM5NTUwOTcy)",
            "[<b>back of thigh and popliteal fossa.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODcxMDg0MDYzOTA1ODk5)",
            "[<b>foot.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODcyMDg2MDg4MjYwODI2)",
            "[<b>leg compartments.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODczMDg4MTEyNjE1NzUz)",
            "[<b>medial and posterior comparments of thigh.mp4.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODc0MDkwMTM2OTcwNjgw)",
            "[<b>arteries and veins of lower limbs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODc1MDkyMTYxMzI1NjA3)",
            "[<b>nerves of lower limb.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODc2MDk0MTg1NjgwNTM0)",
            "[<b>mediastinum, pericardium and pericardial sinuses.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODc3MDk2MjEwMDM1NDYx)",
            "[<b>pleura and lung.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODc4MDk4MjM0MzkwMzg4)",
            "[<b>heart and coronary circulation.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODc5MTAwMjU4NzQ1MzE1)",
            "[<b>axilla-1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODgwMTAyMjgzMTAwMjQy)",
            "[<b>arteries and veins of  upper limbs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODgxMTA0MzA3NDU1MTY5)",
            "[<b>thoracic wall and intercostal space.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODgyMTA2MzMxODEwMDk2)",
            "[<b>back.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODgzMTA4MzU2MTY1MDIz)",
            "[<b>axilla-2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODg0MTEwMzgwNTE5OTUw)",
            "[<b>arm.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODg1MTEyNDA0ODc0ODc3)",
            "[<b>forearm.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODg2MTE0NDI5MjI5ODA0)",
            "[<b>arm.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODg3MTE2NDUzNTg0NzMx)",
            "[<b>arteries and veins of  upper limbs.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODg4MTE4NDc3OTM5NjU4)",
            "[<b>axilla-1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODg5MTIwNTAyMjk0NTg1)",
            "[<b>axilla-2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODkwMTIyNTI2NjQ5NTEy)",
            "[<b>back.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODkxMTI0NTUxMDA0NDM5)",
            "[<b>forearm.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODkyMTI2NTc1MzU5MzY2)",
            "[<b>hand.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODkzMTI4NTk5NzE0Mjkz)",
            "[<b>important nerves of upper limb part 1.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODk0MTMwNjI0MDY5MjIw)",
            "[<b>important nerves of upper limb part 2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODk1MTMyNjQ4NDI0MTQ3)",
            "[<b>shoulder region.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODk2MTM0NjcyNzc5MDc0)",
            "[<b>pectoral region.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODk3MTM2Njk3MTM0MDAx)",
            "[<b>revision-2.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODk4MTM4NzIxNDg4OTI4)",
            "[<b>revision-1.part001.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2ODk5MTQwNzQ1ODQzODU1)",
            "[<b>revision-1.part002.mp4  </b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTAwMTQyNzcwMTk4Nzgy)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        canatomyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"canatomyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"canatomyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(canatomyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))

    elif query.data.startswith("cpharmacologyr"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
    
        links_x = [
            "[<b>Introduction and Routes of Drug Administration</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTAxMTQ0Nzk0NTUzNzA5)",
            "[<b>Pharmacokinetics Absorption</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTAyMTQ2ODE4OTA4NjM2)",
            "[<b>Pharmacokinetics Distribution</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTAzMTQ4ODQzMjYzNTYz)",
            "[<b>Pharmacokinetics Metabolism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTA0MTUwODY3NjE4NDkw)",
            "[<b>Pharmacokinetics Excretion</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTA1MTUyODkxOTczNDE3)",
            "[<b>Kinetics of Elimination</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTA2MTU0OTE2MzI4MzQ0)",
            "[<b>Pharmacodynamics Introduction and Enzyme inhibitors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTA3MTU2OTQwNjgzMjcx)",
            "[<b>Pharmacodynamics Receptors</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTA4MTU4OTY1MDM4MTk4)",
            "[<b>Dose Response Curve</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTA5MTYwOTg5MzkzMTI1)",
            "[<b>Clinical trial and pharmacovigilance</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTEwMTYzMDEzNzQ4MDUy)",
            "[<b>Factors affecting Drug Action</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTExMTY1MDM4MTAyOTc5)",
            "[<b>Combined Effect of Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTEyMTY3MDYyNDU3OTA2)",
            "[<b>Practicals in General Pharmacology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTEzMTY5MDg2ODEyODMz)",
            "[<b>Basics and Cholinergic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTE0MTcxMTExMTY3NzYw)",
            "[<b>Anti-cholinergic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTE1MTczMTM1NTIyNjg3)",
            "[<b>Anti-Adrenergic Drugs.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTE2MTc1MTU5ODc3NjE0)",
            "[<b>Adrenergic Drugs.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTE3MTc3MTg0MjMyNTQx)",
            "[<b>Glaucoma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTE4MTc5MjA4NTg3NDY4)",
            "[<b>Practicals in ANS</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTE5MTgxMjMyOTQyMzk1)",
            "[<b>Histamine and Serotonin</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTIwMTgzMjU3Mjk3MzIy)",
            "[<b>Migraine</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTIxMTg1MjgxNjUyMjQ5)",
            "[<b>Gout and Rheumatoid Arthritis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTIyMTg3MzA2MDA3MTc2)",
            "[<b>PG and NSAIDs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTIzMTg5MzMwMzYyMTAz)",
            "[<b>Drug Used in Hypertension</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTI0MTkxMzU0NzE3MDMw)",
            "[<b>Ischemic Heart Disease</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTI1MTkzMzc5MDcxOTU3)",
            "[<b>Anti-Arrhythmic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTI2MTk1NDAzNDI2ODg0)",
            "[<b>Congestive Heart Failure</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTI3MTk3NDI3NzgxODEx)",
            "[<b>Anti-Dyslipidemic</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTI4MTk5NDUyMTM2NzM4)",
            "[<b>Diuretics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTI5MjAxNDc2NDkxNjY1)",
            "[<b>Adrenal</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTMwMjAzNTAwODQ2NTky)",
            "[<b>oral contraceptives</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTMxMjA1NTI1MjAxNTE5)",
            "[<b>Pancreas</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTMyMjA3NTQ5NTU2NDQ2)",
            "[<b>Osteoporosis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTMzMjA5NTczOTExMzcz)",
            "[<b>Thyroid</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTM0MjExNTk4MjY2MzAw)",
            "[<b>Pituitary Hypothalamic System</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTM1MjEzNjIyNjIxMjI3)",
            "[<b>sex hormones</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTM2MjE1NjQ2OTc2MTU0)",
            "[<b>Anti-epileptic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTM3MjE3NjcxMzMxMDgx)",
            "[<b>drug of abuse</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTM4MjE5Njk1Njg2MDA4)",
            "[<b>Neurodegenerative Diseases</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTM5MjIxNzIwMDQwOTM1)",
            "[<b>Anti-psychotics Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQwMjIzNzQ0Mzk1ODYy)",
            "[<b>Drugs for Mania and Depression</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQxMjI1NzY4NzUwNzg5)",
            "[<b>Sedative hypnotics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQyMjI3NzkzMTA1NzE2)",
            "[<b>Local Anaesthetics and Skeletal Muscle Relaxants</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQzMjI5ODE3NDYwNjQz)",
            "[<b>General Anaesthetics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQ0MjMxODQxODE1NTcw)",
            "[<b>Drugs Affecting Blood Flow</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQ1MjMzODY2MTcwNDk3)",
            "[<b>Drugs Affecting Cells of Blood</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQ2MjM1ODkwNTI1NDI0)",
            "[<b>Cough and Bronchial Asthma</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQ3MjM3OTE0ODgwMzUx)",
            "[<b>Gastro-Intestinal Tract (GIT)</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQ4MjM5OTM5MjM1Mjc4)",
            "[<b>Anti-Fungal Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTQ5MjQxOTYzNTkwMjA1)",
            "[<b>Anti-Viral Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTUwMjQzOTg3OTQ1MTMy)",
            "[<b>Malaria and Other Parasites</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTUxMjQ2MDEyMzAwMDU5)",
            "[<b>Tuberculosis and Leprosy</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTUyMjQ4MDM2NjU0OTg2)",
            "[<b>Ama acting by other mechanism</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTUzMjUwMDYxMDA5OTEz)",
            "[<b>Drugs Inhibiting Cell Wall Synthesis</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTU0MjUyMDg1MzY0ODQw)",
            "[<b>General Considerations about Anti-Microbial Agents</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTU1MjU0MTA5NzE5NzY3)",
            "[<b>Immunospuressants</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTU2MjU2MTM0MDc0Njk0)",
            "[<b>Cytotoxic Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTU3MjU4MTU4NDI5NjIx)",
            "[<b>Monoclonal Antibodies</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTU4MjYwMTgyNzg0NTQ4)",
            "[<b>Targeted Anti-Cancer Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTU5MjYyMjA3MTM5NDc1)",
            "[<b>Drug Interactions and Antidotes</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTYwMjY0MjMxNDk0NDAy)",
            "[<b>Miscellaneous Topics</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTYxMjY2MjU1ODQ5MzI5)",
            "[<b>New Drugs</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTYyMjY4MjgwMjA0MjU2)",
        ]
    
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
    
        page_links, has_more = paginate_links(links, page)
        cpharmacologyr_message = "\n".join(page_links)
    
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"cpharmacologyr_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"cpharmacologyr_{page+1}"))
    
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
    
        msg = await query.message.reply_text(cpharmacologyr_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))    
    
    elif query.data.startswith("srikantanatomy"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
      
        links_x = [
            "[<b>aPART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTYzMjcwMzA0NTU5MTgz)",
            "[<b>bPART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY0MjcyMzI4OTE0MTEw)",
            "[<b>cPART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY1Mjc0MzUzMjY5MDM3)",
            "[<b>dPART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY2Mjc2Mzc3NjIzOTY0)",
            "[<b>ePART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY3Mjc4NDAxOTc4ODkx)",
            "[<b>fPART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY4MjgwNDI2MzMzODE4)",
            "[<b>gPART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY5MjgyNDUwNjg4NzQ1)",
            "[<b>hPART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTcwMjg0NDc1MDQzNjcy)",
            "[<b>iPART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTcxMjg2NDk5Mzk4NTk5)",
            "[<b>jPART 10</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTcyMjg4NTIzNzUzNTI2)",
            "[<b>kPART 11</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTczMjkwNTQ4MTA4NDUz)",
            "[<b>lPART 12</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc0MjkyNTcyNDYzMzgw)",
            "[<b>Chapter 1 hypertension.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc1Mjk0NTk2ODE4MzA3)",
        ]
      
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
      
        page_links, has_more = paginate_links(links, page)
        srikantanatomy_message = "\n".join(page_links)
      
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"srikantanatomy_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"srikantanatomy_{page+1}"))
      
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
      
        msg = await query.message.reply_text(srikantanatomy_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))
    
    
    elif query.data.startswith("ashishphysiok"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
      
        links_x = [
            "[<b>General Physiology Part - 1 By Dr. Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDcxNDY4NjI4Njc0MTUz)",
            "[<b>General Physiology Part - 2 By Dr. Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDcyNDcwNjUzMDI5MDgw)",
            "[<b>Endocrine Physiology Part - 1 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDczNDcyNjc3Mzg0MDA3)",
            "[<b>Endocrine Physiology Part - 2 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDc0NDc0NzAxNzM4OTM0)",
            "[<b>Endocrine Physiology Part - 3 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDc1NDc2NzI2MDkzODYx)",
            "[<b>Endocrine Physiology Part - 4 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDc2NDc4NzUwNDQ4Nzg4)",
            "[<b>Endocrine Physiology Part - 5 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDc3NDgwNzc0ODAzNzE1)",
            "[<b>GIT Physiology By Dr. Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDc4NDgyNzk5MTU4NjQy)",
            "[<b>Respiratory Physiology Part - 1 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDc5NDg0ODIzNTEzNTY5)",
            "[<b>Respiratory Physiology Part - 2 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDgwNDg2ODQ3ODY4NDk2)",
            "[<b>Respiratory Physiology Part - 3 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDgxNDg4ODcyMjIzNDIz)",
            "[<b>Respiratory Physiology Part - 4 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDgyNDkwODk2NTc4MzUw)",
            "[<b>Cardiovascular Physiology Part - 1 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDgzNDkyOTIwOTMzMjc3)",
            "[<b>Cardiovascular Physiology Part - 2 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDg0NDk0OTQ1Mjg4MjA0)",
            "[<b>Cardiovascular Physiology Part - 3 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDg1NDk2OTY5NjQzMTMx)",
            "[<b>Cardiovascular Physiology Part - 4 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDg2NDk4OTkzOTk4MDU4)",
            "[<b>Cardiovascular Physiology Part - 5 By Ashish Sir</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2MDg3NTAxMDE4MzUyOTg1)",
            "[<b>Chapter 1 hypertension.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc1Mjk0NTk2ODE4MzA3)",
        ]
      
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]
      
        page_links, has_more = paginate_links(links, page)
        ashishphysiok_message = "\n".join(page_links)
      
        navigation_buttons = []
        if page > 0:
            navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"ashishphysiok_{page-1}"))
        if has_more:
            navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"ashishphysiok_{page+1}"))
      
        reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
      
        msg = await query.message.reply_text(ashishphysiok_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


    elif query.data.startswith("pjmedicine"):
        try:
            page = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            page = 0
      
        links_x = [
            "[<b>aPART 1</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTYzMjcwMzA0NTU5MTgz)",
            "[<b>bPART 2</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY0MjcyMzI4OTE0MTEw)",
            "[<b>cPART 3</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY1Mjc0MzUzMjY5MDM3)",
            "[<b>dPART 4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY2Mjc2Mzc3NjIzOTY0)",
            "[<b>ePART 5</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY3Mjc4NDAxOTc4ODkx)",
            "[<b>fPART 6</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY4MjgwNDI2MzMzODE4)",
            "[<b>gPART 7</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTY5MjgyNDUwNjg4NzQ1)",
            "[<b>hPART 8</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTcwMjg0NDc1MDQzNjcy)",
            "[<b>iPART 9</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTcxMjg2NDk5Mzk4NTk5)",
            "[<b>jPART 10</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTcyMjg4NTIzNzUzNTI2)",
            "[<b>kPART 11</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTczMjkwNTQ4MTA4NDUz)",
            "[<b>lPART 12</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc0MjkyNTcyNDYzMzgw)",
            "[<b>Chapter 1 hypertension.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc1Mjk0NTk2ODE4MzA3)",            
            "[<b>Chapter 8 Renal transplant & renal cystic disease.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDYwNDY2NjY2OTg3MTAy)",
        ]      
        
        X = "testingclonepavo_bot"
        links = [link.replace('{{"X"}}', X) for link in links_x]

        page_links, has_more = paginate_links(links, page)

        if len(page_links) < 20:
            # Less than 20 links, include "Back to Main Menu" button
            reply_markup = None
        else:
            # More than 20 links, include navigation buttons
            navigation_buttons = []
            if page > 0:
                navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pjmedicine_{page-1}"))
            if has_more:
                navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pjmedicine_{page+1}"))

            reply_markup = InlineKeyboardMarkup([navigation_buttons])

        pjmedicine_message = "\n".join(page_links)
        
        # Send the message
        msg = await query.message.reply_text(pjmedicine_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
        asyncio.create_task(schedule_deletion([msg], SECONDS))


