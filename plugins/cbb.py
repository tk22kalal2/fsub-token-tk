# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de
from TechVJ.bot import StreamBot
from bot import Bot
from pyrogram import filters
from pyrogram.errors import MessageNotModified
from pyrogram.types import CallbackQuery, Message

@StreamBot.on_callback_query()
async def cb_handler(client: StreamBot, query: CallbackQuery):
    data = query.data
    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except BaseException:
            pass
