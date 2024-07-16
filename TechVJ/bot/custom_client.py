from pyrogram import Client
from pyrogram.errors import FloodWait
import asyncio
from config import CHANNEL_ID

class CustomClient(Client):
    def __init__(self, db_channel, *args, **kwargs):
        self.db_channel = db_channel
        super().__init__(*args, **kwargs)
        

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.namebot}\n└ Username: @{self.username}\n——"
            )
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info(
                "Bot Stopped. Join https://t.me/CodeXBotzSupport for support"
            )
            sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message", disable_notification=True)
            await test.delete()
            self.LOGGER(__name__).info(
                f"CHANNEL_ID Database detected!\n┌ Title: {db_channel.title}\n└ Chat ID: {db_channel.id}\n——"
            )
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(
                f"Make Sure @{self.username} is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Bot Stopped. Join https://t.me/CodeXBotzSupport for support"
            )
            sys.exit()
