# custom_client.py

from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from config import CHANNEL_ID

class CustomClient(Client):
    def __init__(self, db_channel, *args, **kwargs):
        db_channel = await self.get_chat(CHANNEL_ID)
        self.db_channel = db_channel
        test = await self.send_message(chat_id=db_channel.id, text="Test Message", disable_notification=True)
        await test.delete()
        super().__init__(*args, **kwargs)

