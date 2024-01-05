
@Bot.on_message(filters.private & filters.incoming)
async def useless(_,message: Message):
    if USER_REPLY_TEXT:
        await message.reply(USER_REPLY_TEXT)


@client.on(events.NewMessage(chats=events.PeerUser()))
async def forward_to_admin(event):
    # Check if the message is from a private chat
    if event.is_private:
        # Forward the user's message to the admin
        await client.send_message(ADMIN_ID, f"User ID: {event.sender_id}\nMessage: {event.raw_text}")

