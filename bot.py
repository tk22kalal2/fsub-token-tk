# (©)Codexbotz
# Recode by @mrismanaziz
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import pyromod.listen
import sys
import socket
from tenacity import retry, wait_fixed, stop_after_attempt
from pyrogram import Client, enums
from pyrogram import idle
from pyrogram.errors import FloodWait, RPCError
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
from plugins.keepalive import ping_server
from plugins.clone import restart_bots

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN,
        )
        self.LOGGER = LOGGER

    @retry(wait=wait_fixed(5), stop=stop_after_attempt(5))
    async def start_bot(self):
        try:
            await self.start()
        except socket.error as e:
            self.LOGGER(__name__).warning(f"Socket error: {e}")
            raise e
        except RPCError as e:
            self.LOGGER(__name__).warning(f"RPC error: {e}")
            raise e

    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(
                f"TG_BOT_TOKEN detected!\n┌ First Name: {self.namebot}\n└ Username: @{self.username}\n——"
            )
        except FloodWait as e:
            self.LOGGER(__name__).warning(f"Flood wait error: {e}")
            await asyncio.sleep(e.x)
            sys.exit()
        except RPCError as e:
            self.LOGGER(__name__).warning(f"RPC error: {e}")
            self.LOGGER(__name__).info(
                "Bot Stopped. Join https://t.me/CodeXBotzSupport for support"
            )
            sys.exit()

        if FORCE_SUB_CHANNEL:
            try:
                info = await self.get_chat(FORCE_SUB_CHANNEL)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = info.invite_link
                self.invitelink = link
                self.LOGGER(__name__).info(
                    f"FORCE_SUB_CHANNEL detected!\n┌ Title: {info.title}\n└ Chat ID: {info.id}\n——"
                )
            except FloodWait as e:
                self.LOGGER(__name__).warning(f"Flood wait error: {e}")
                await asyncio.sleep(e.x)
                sys.exit()
            except RPCError as e:
                self.LOGGER(__name__).warning(f"RPC error: {e}")
                self.LOGGER(__name__).warning(
                    "Bot can't Export Invite link from Force Sub Channel!"
                )
                self.LOGGER(__name__).warning(
                    f"Make sure @{self.username} is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}"
                )
                self.LOGGER(__name__).info(
                    "Bot Stopped. Join https://t.me/CodeXBotzSupport for support"
                )
                sys.exit()

        if FORCE_SUB_GROUP:
            try:
                info = await self.get_chat(FORCE_SUB_GROUP)
                link = info.invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_GROUP)
                    link = info.invite_link
                self.invitelink2 = link
                self.LOGGER(__name__).info(
                    f"FORCE_SUB_GROUP detected!\n┌ Title: {info.title}\n└ Chat ID: {info.id}\n——"
                )
            except FloodWait as e:
                self.LOGGER(__name__).warning(f"Flood wait error: {e}")
                await asyncio.sleep(e.x)
                sys.exit()
            except RPCError as e:
                self.LOGGER(__name__).warning(f"RPC error: {e}")
                self.LOGGER(__name__).warning(
                    "Bot can't Export Invite link from Force Sub Channel!"
                )
                self.LOGGER(__name__).warning(
                    f"Make sure @{self.username} is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_GROUP}"
                )
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
        except FloodWait as e:
            self.LOGGER(__name__).warning(f"Flood wait error: {e}")
            await asyncio.sleep(e.x)
            sys.exit()
        except RPCError as e:
            self.LOGGER(__name__).warning(f"RPC error: {e}")
            self.LOGGER(__name__).warning(
                f"Make Sure @{self.username} is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}"
            )
            self.LOGGER(__name__).info(
                "Bot Stopped. Join https://t.me/CodeXBotzSupport for support"
            )
            sys.exit()

        await restart_bots()
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"[🔥 SUCCESSFULLY ACTIVATED! 🔥]"
        )
        self.keepalive_task = asyncio.create_task(ping_server())
        await idle()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

if __name__ == "__main__":
    bot = Bot()
    while True:
        try:
            asyncio.run(bot.start_bot())
        except (socket.error, RetryError) as e:
            bot.LOGGER(__name__).warning(f"Retrying due to socket error: {e}")
            continue
        except (KeyboardInterrupt, SystemExit):
            bot.LOGGER(__name__).info("Bot stopped.")
            sys.exit()
