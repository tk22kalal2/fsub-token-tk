@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "start":
        buttons = [
            [InlineKeyboardButton('MARROW', callback_data='marrow')],
            [InlineKeyboardButton('PREPLADDER 5', callback_data='prepladder')],
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

    elif query.data == "others":
        others_buttons = [
            [InlineKeyboardButton("ZAINAB VOHRA RADIOLOGY", callback_data="zvradiology")],
            [InlineKeyboardButton("ASHISH SIR PHYSIOLOGY", callback_data="asphysiology")],
            [InlineKeyboardButton("RAJIV DHAWAN ENT", callback_data="rdent")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(others_buttons)
        await query.message.edit_reply_markup(reply_markup)
