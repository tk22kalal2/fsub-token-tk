# custom_client.py

from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from config import CHANNEL_ID
import pyromod.listen
import sys
from pyrogram import enums

from config import (
    API_HASH,
    APP_ID,
    CHANNEL_ID,
    FORCE_SUB_CHANNEL,
    FORCE_SUB_GROUP,
    LOGGER,
    TG_BOT_TOKEN,
    TG_BOT_WORKERS,
)


class CustomClient(Client):
    def __init__(self, db_channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_channel = db_channel

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message", disable_notification=True)
            await test.delete()
            
