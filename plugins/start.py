# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de
import re
import os
import random
import asyncio
import pymongo
from datetime import datetime, timedelta
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
    DB_URI,
    START_MSG,
    API_ID,
    API_HASH,
)
#from database.sql import add_user, delete_user, full_userbase, query_msg
from database.mongo import collection, adds_user, del_user, fulls_userbase, present_user
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, ChannelInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, KeyboardButton

from helper_func import decode, get_messages, subsall, subsch, subsgc
from helper import b64_to_str, str_to_b64, get_current_time, shorten_url

from .button import fsub_button, start_button

mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client["cloned_vjbotz"]
mongo_collection = mongo_db["bots"]

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]
video_requests = database["video_requests"]

MAX_VIDEOS_PER_DAY = 20
TIME_LIMIT = timedelta(hours=24)

async def record_video_request(user_id: int):
    now = datetime.utcnow()
    video_requests.insert_one({"user_id": user_id, "timestamp": now})

def has_exceeded_limit(user_id: int):
    now = datetime.utcnow()
    start_time = now - TIME_LIMIT
    request_count = video_requests.count_documents({
        "user_id": user_id,
        "timestamp": {"$gte": start_time}
    })
    return request_count >= MAX_VIDEOS_PER_DAY
    
SECONDS = int(os.getenv("SECONDS", "10")) #add time im seconds for waitingwaiting before delete

async def schedule_deletion(msgs, delay):
    await asyncio.sleep(delay)
    for msg in msgs:
        try:
            await msg.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60**2 * 24),
    ("hour", 60**2),
    ("min", 60),
    ("sec", 1),
)

import re




async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append(f'{amount} {unit}{"" if amount == 1 else "s"}')
    return ", ".join(parts)


@Bot.on_message(filters.command("start") & filters.private & subsall & subsch & subsgc)
async def start_command(client: Bot, message: Message):
    id = message.from_user.id
    if has_exceeded_limit(id):
        await message.reply_text("You have exceeded the limit of 20 videos in 24 hours. Please try again later.")
        return
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass

    if message.text.startswith("/start token_"):
        user_id = message.from_user.id
        try:
            ad_msg = b64_to_str(message.text.split("/start token_")[1])
            if int(user_id) != int(ad_msg.split(":")[0]):
                await client.send_message(
                    message.chat.id,
                    "This Token Is Not For You \nor maybe you using 2 telegram apps if yes then uninstall this one...",
                    reply_to_message_id=message.id,
                )
                return
            if int(ad_msg.split(":")[1]) < get_current_time():
                await client.send_message(
                    message.chat.id,
                    "Token Expired Regenerate A New Token",
                    reply_to_message_id=message.id,
                )
                return
            if int(ad_msg.split(":")[1]) > int(get_current_time() + 72000):
                await client.send_message(
                    message.chat.id,
                    "Dont Try To Be Over Smart",
                    reply_to_message_id=message.id,
                )
                return
            query = {"user_id": user_id}
            collection.update_one(
                query, {"$set": {"time_out": int(ad_msg.split(":")[1])}}, upsert=True
            )
            await client.send_message(
                message.chat.id,
                f"Congratulations! Ads token refreshed successfully! It will expire after 10 Hour \n\nClone your bot /clone \n\n<b>NOTE:-</b>DONT CLONE THE BOT TWICE, CLONE YOUR BOT ONE TIME WHICH BE ACTIVE FOREVER.\n\nBELOW GIVEN VIDEO TUTORIAL FOR STEP-2 - HOW TO CLONE YOUR OWN LECTURE BOT</b>",
                disable_web_page_preview = True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('STEP-2 VIDEO TUTORIAL', web_app=WebAppInfo(url="https://youtu.be/LnpT4AGiaGg?si=D0fBTOXPNUDnBNR6")
                            )
                        ]
                    ]
                ),
                reply_to_message_id=message.id,
            )
            return
        except BaseException:
            await client.send_message(
                message.chat.id,
                "Invalid Token",
                reply_to_message_id=message.id,
            )
            return

    uid = message.from_user.id
    if uid not in ADMINS:
        result = collection.find_one({"user_id": uid})
        if result is None:
            temp_msg = await message.reply("Please wait...")
            ad_code = str_to_b64(f"{uid}:{str(get_current_time() + 72000)}")
            ad_url = shorten_url(f"https://telegram.dog/{client.username}?start=token_{ad_code}")
            await client.send_message(
                message.chat.id,
                f"Hey 👨‍⚕️ Dr.<b>{message.from_user.mention}</b> \n<b>GET ALL FREE MEDICAL LECTURES</b>\n\nTo Get Free Lectures You Have To Follow Three Steps:-\nSTEP-1 - REFRESH YOUR TOKEN\nSTEP-2 - CLONE YOUR OWN BOT\nSTEP-3 - WATCH LECTURE\n\nSTEP-1 is permanent step and you have to do after every 24 hours.Some basic instructions given below before starting step-1\n\n<b>STEPS :- </b> \n1. Make Google Chrome as your default browser - <a href='https://t.me/c/2045440584/7'>Click Here</a> \n2. Diasable Your AD Blocker ✋- <a href='https://t.me/c/2045440584/10'>Click Here</a> \n3. How to Verify - <a href='https://t.me/c/2045440584/9'>Telegraph</a> or <a href='https://t.me/c/2045440584/8'>Watch Here</a> \nTELEGRAPH - <a href='https://graph.org/HOW-TO-VERIFY-11-08-2'>Click Here</a> \n\n<b>APPLE/IPHONE USERS COPY TOKEN LINK AND OPEN IN CHROME BROWSER\n\nBELOW GIVEN VIDEO TUTORIAL FOR STEP-1</b>",
                disable_web_page_preview = True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('STEP-1 VIDEO TUTORIAL', web_app=WebAppInfo(url="https://youtu.be/nSokAn8S8CE?si=hvnw0y-f-0uqrD4K")),
                            InlineKeyboardButton(
                                "Click Here To Refresh Token",
                                url=ad_url,
                            )
                        ]
                    ]
                ),
                reply_to_message_id=message.id,
            )
            await temp_msg.delete()
            return
        elif int(result["time_out"]) < get_current_time():
            temp_msg = await message.reply("Please wait...")
            ad_code = str_to_b64(f"{uid}:{str(get_current_time() + 72000)}")
            ad_url = shorten_url(f"https://telegram.dog/{client.username}?start=token_{ad_code}")
            await client.send_message(
                message.chat.id,
                f"Hey 👨‍⚕️ Dr.<b>{message.from_user.mention}</b> \n<b>GET ALL FREE MEDICAL LECTURES</b>\n\nTo Get Free Lectures You Have To Follow Three Steps:-\nSTEP-1 - REFRESH YOUR TOKEN\nSTEP-2 - CLONE YOUR OWN BOT\nSTEP-3 - WATCH LECTURE\n\n<b>VIDEO TUTORIAL FOR STEP-1</b> - <a href='https://opposite-vilhelmina-nextpulse2-4506220f.koyeb.app/watch/9900/InShot_20240817_054425271.mp4?hash=AgADtg'>Click Here</a>  \nSTEP-1 is permanent step and you have to do after every 24 hours.Some basic instructions given below before starting step-1\n\n<b>STEPS :- </b> \n1. Make Google Chrome as your default browser - <a href='https://t.me/c/2045440584/7'>Click Here</a> \n2. Diasable Your AD Blocker ✋- <a href='https://t.me/c/2045440584/10'>Click Here</a> \n3. How to Verify - <a href='https://t.me/c/2045440584/9'>Telegraph</a> or <a href='https://t.me/c/2045440584/8'>Watch Here</a> \nTELEGRAPH - <a href='https://graph.org/HOW-TO-VERIFY-11-08-2'>Click Here</a> \n\n<b>APPLE/IPHONE USERS COPY TOKEN LINK AND OPEN IN CHROME BROWSER</b>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Click Here To Refresh Token",
                                url=ad_url,
                            )
                        ]
                    ]
                ),
                reply_to_message_id=message.id,
            )
            await temp_msg.delete()
            return

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
        except Exception:
            await message.reply_text("Something went wrong..!")
            return
        finally:
            await temp_msg.delete()

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except Exception:
            await message.reply_text("Something went wrong..!")
            return
        finally:
            await temp_msg.delete()

        

        # List of possible replacement URLs
        replacement_urls = [
            "https://t.me/testingdoubletera_bot?",
            "https://t.me/testingclonepavo2_bot?",
            "https://t.me/Mynextpulsembbs_bot?",
            "https://t.me/Mynextpulsembbs1_bot?"
        ]

        snt_msgs = []
        
        for msg in messages:
            # Check and replace the specific URL pattern in the message text
            if msg.text and "https://t.me/{\"X\"}?" in msg.text:
                # Choose a random URL from the list
                replacement_url = random.choice(replacement_urls)
                msg.text = msg.text.replace("https://t.me/{\"X\"}?", replacement_url)
                
            if msg.caption and "https://t.me/{\"X\"}?" in msg.caption:
                # Choose a random URL from the list
                replacement_url = random.choice(replacement_urls)
                msg.caption = msg.caption.replace("https://t.me/{\"X\"}?", replacement_url)
        

            caption = (CUSTOM_CAPTION.format(
                previouscaption=msg.caption.html if msg.caption else "",
                filename=msg.document.file_name
            ) if bool(CUSTOM_CAPTION) and bool(msg.document) else
            msg.caption.html if msg.caption else "")

            reply_markup = msg.reply_markup if not DISABLE_CHANNEL_BUTTON else None

            try:
                snt_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    protect_content=PROTECT_CONTENT,
                    reply_markup=reply_markup,
                )
                await asyncio.sleep(0.5)
                snt_msgs.append(snt_msg)
                
                await record_video_request(id)
                
            except FloodWait as e:
                await asyncio.sleep(e.x)
                snt_msg = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    protect_content=PROTECT_CONTENT,
                    reply_markup=reply_markup,
                )
                snt_msgs.append(snt_msg)
            except BaseException:
                pass

        asyncio.create_task(schedule_deletion(snt_msgs, SECONDS))
    else:
        out = start_button(client)
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=f"@{message.from_user.username}"
                if message.from_user.username
                else None,
                mention=message.from_user.mention,
                id=message.from_user.id,
            ),
            reply_markup=InlineKeyboardMarkup(out),
            disable_web_page_preview=True,
            quote=True,
        )


    return
                

@Bot.on_message(filters.command("start") & filters.private)
async def not_joined(client: Bot, message: Message):
    buttons = fsub_button(client, message)
    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=f"@{message.from_user.username}"
            if message.from_user.username
            else None,
            mention=message.from_user.mention,
            id=message.from_user.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True,
    )


@Bot.on_message(filters.command(["users", "stats"]) & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(
        chat_id=message.chat.id, text="<code>Processing ...</code>"
    )
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")


@Bot.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await query_msg()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply(
            "<i>Broadcasting Message.. This will Take Some Time</i>"
        )
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        return await pls_wait.edit(status)
    else:
        msg = await message.reply(
            "<code>Use this command as a replay to any telegram message with out any spaces.</code>"
        )
        await asyncio.sleep(8)
        await msg.delete()


@Bot.on_message(filters.command("ping"))
async def ping_pong(client, m: Message):
    start = time()
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    m_reply = await m.reply_text("Pinging...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "<b>PONG!!</b>🏓 \n"
        f"<b>• Pinger -</b> <code>{delta_ping * 1000:.3f}ms</code>\n"
        f"<b>• Uptime -</b> <code>{uptime}</code>\n"
    )


@Bot.on_message(filters.command("uptime"))
async def get_uptime(client, m: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await m.reply_text(
        "🤖 <b>Bot Status:</b>\n"
        f"• <b>Uptime:</b> <code>{uptime}</code>\n"
        f"• <b>Start Time:</b> <code>{START_TIME_ISO}</code>"
    )
