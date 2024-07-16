from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from config import CHANNEL_ID

class CustomClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_channel = None

    async def start(self):
        await super().start()
        self.db_channel = await self.get_chat(CHANNEL_ID)
