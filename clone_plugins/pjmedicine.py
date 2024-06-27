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
    
    elif query.data == "others":
        others_buttons = [
            [InlineKeyboardButton("ZAINAB VOHRA RADIOLOGY", callback_data="zvradiology")],
            [InlineKeyboardButton("ASHISH SIR PHYSIOLOGY", callback_data="ashishphysiok")],
            [InlineKeyboardButton("RAJIV DHAWAN ENT", callback_data="rdent")],
            [InlineKeyboardButton("SRIKANT ANATOMY", callback_data="srikantanatomys")],
            [InlineKeyboardButton("PRIYANSH JAIN MEDICINE", callback_data="pjmedicine")],
            [InlineKeyboardButton("BACK TO MAIN MENU", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(others_buttons)
        await query.message.edit_reply_markup(reply_markup)
      
    elif query.data.startswith("pjmedicine"):
          try:
              page = int(query.data.split('_')[1])
          except (IndexError, ValueError):
              page = 0
      
          links_x = [
              "[<b>Chapter 1 hypertension.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc1Mjk0NTk2ODE4MzA3)",
              "[<b>Chapter_2_Right_ventricular_failure_VS_left_ventricular_failure.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc2Mjk2NjIxMTczMjM0)",
              "[<b>Chapter 3 Heart failure.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc3Mjk4NjQ1NTI4MTYx)",
              "[<b>Chapter 4 CAD part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc4MzAwNjY5ODgzMDg4)",
              "[<b>Chapter 4 CAD part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTc5MzAyNjk0MjM4MDE1)",
              "[<b>Chapter 4 CAD part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTgwMzA0NzE4NTkyOTQy)",
              "[<b>Chapter 5 jugular venous pressure.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTgxMzA2NzQyOTQ3ODY5)",
              "[<b>Chapter 6 pericardial disorder.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTgyMzA4NzY3MzAyNzk2)",
              "[<b>Chapter 7 cardiomyopathy part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTgzMzEwNzkxNjU3NzIz)",
              "[<b>Chapter 7 cardiomyopathy part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTg0MzEyODE2MDEyNjUw)",
              "[<b>Chapter 7 cardiomyopathy part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTg1MzE0ODQwMzY3NTc3)",
              "[<b>Chapter 8 rheumatic fever.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTg2MzE2ODY0NzIyNTA0)",
              "[<b>Chapter 9 infections endocarditis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTg3MzE4ODg5MDc3NDMx)",
              "[<b>Chapter 10 ECG part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTg4MzIwOTEzNDMyMzU4)",
              "[<b>Chapter 10 ECG part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTg5MzIyOTM3Nzg3Mjg1)",
              "[<b>Chapter 10 ECG part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTkwMzI0OTYyMTQyMjEy)",
              "[<b>Chapter 10 ECG part 4.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTkxMzI2OTg2NDk3MTM5)",
              "[<b>Chapter 10 mitral stenosis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTkyMzI5MDEwODUyMDY2)",
              "[<b>Chapter 11 aortic regurgitation.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTkzMzMxMDM1MjA2OTkz)",
              "[<b>Chapter 12 Murmur.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTk0MzMzMDU5NTYxOTIw)",
              "[<b>Endocrinology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTk1MzM1MDgzOTE2ODQ3)",
              "[<b>Chapter 1 pathogenesis of DM.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTk2MzM3MTA4MjcxNzc0)",
              "[<b>Chapter_2_diabetic_presentation_diagnosis_&_complications_part_1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTk3MzM5MTMyNjI2NzAx)",
              "[<b>Chapter_2_diabetic_presentation_diagnosis_&_complications_part_2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTk4MzQxMTU2OTgxNjI4)",
              "[<b>Chapter_3_diabetic_ketoacidosis_&_hyperglycemic_hyperosmolar.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE2OTk5MzQzMTgxMzM2NTU1)",
              "[<b>Chapter 4 thyroid physiology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDAwMzQ1MjA1NjkxNDgy)",
              "[<b>Chapter 5 interpretation of thyroid profile test.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDAxMzQ3MjMwMDQ2NDA5)",
              "[<b>Chapter 6 hyperthyroidism & hypothyroidism.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDAyMzQ5MjU0NDAxMzM2)",
              "[<b>Chapter 7 raiu and thyroid part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDAzMzUxMjc4NzU2MjYz)",
              "[<b>Chapter 7 thyroid pathology part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDA0MzUzMzAzMTExMTkw)",
              "[<b>Chapter 8 basic of adrenal gland.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDA1MzU1MzI3NDY2MTE3)",
              "[<b>Chapter 9 hyperaldosteronism.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDA2MzU3MzUxODIxMDQ0)",
              "[<b>Chapter 10 Cushing syndrome.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDA3MzU5Mzc2MTc1OTcx)",
              "[<b>Chapter 11 pheochromocytoma.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDA4MzYxNDAwNTMwODk4)",
              "[<b>Chapter 12 adrenal insufficiency.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDA5MzYzNDI0ODg1ODI1)",
              "[<b>Chapter 13 &14 hypoparathyroidism part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDEwMzY1NDQ5MjQwNzUy)",
              "[<b>Chapter 13 physiology of parathyroid gland .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDExMzY3NDczNTk1Njc5)",
              "[<b>Chapter 15_16_17 basic of pituitary gland .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDEyMzY5NDk3OTUwNjA2)",
              "[<b>Chapter 16&17 acromegaly part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDEzMzcxNTIyMzA1NTMz)",
              "[<b>Chapter 16&17 acromegay part3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDE0MzczNTQ2NjYwNDYw)",
              "[<b>Neurology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDE1Mzc1NTcxMDE1Mzg3)",
              "[<b>Chapter 1 stroke-cerebrovascular accident part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDE2Mzc3NTk1MzcwMzE0)",
              "[<b>Chapter 1 stroke-cerebrovascular accident part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDE3Mzc5NjE5NzI1MjQx)",
              "[<b>Chapter 1 stroke-cerebrovascular accident part 3.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDE4MzgxNjQ0MDgwMTY4)",
              "[<b>Chapter 2 meningitis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDE5MzgzNjY4NDM1MDk1)",
              "[<b>Chapter 3 dementia.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDIwMzg1NjkyNzkwMDIy)",
              "[<b>Chapter 3B parkinsonism.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDIxMzg3NzE3MTQ0OTQ5)",
              "[<b>Chapter 4 headache.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDIyMzg5NzQxNDk5ODc2)",
              "[<b>Chapter 5 aphasia.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDIzMzkxNzY1ODU0ODAz)",
              "[<b>Chapter 6 epilepsy.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDI0MzkzNzkwMjA5NzMw)",
              "[<b>Chapter 7 neuromuscular junction discord.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDI1Mzk1ODE0NTY0NjU3)",
              "[<b>Chapter 8 dystropinopathies.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDI2Mzk3ODM4OTE5NTg0)",
              "[<b>Chapter 8B multiple sclerosis and GBS part 1.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDI3Mzk5ODYzMjc0NTEx)",
              "[<b>Chapter 8B multiple sclerosis and GBS part 2.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDI4NDAxODg3NjI5NDM4)",
              "[<b>Chapter 9 motor neuron disease.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDI5NDAzOTExOTg0MzY1)",
              "[<b>Chapter 10 spinal cord.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDMwNDA1OTM2MzM5Mjky)",
              "[<b>Chapter 11 brain stem disorder.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDMxNDA3OTYwNjk0MjE5)",
              "[<b>Chapter 12 facial party.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDMyNDA5OTg1MDQ5MTQ2)",
              "[<b>Pulmonary</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDMzNDEyMDA5NDA0MDcz)",
              "[<b>Chapter 1 lung function test .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDM0NDE0MDMzNzU5MDAw)",
              "[<b>Chapter 2 diffusion capacity of carbon monoxide .mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDM1NDE2MDU4MTEzOTI3)",
              "[<b>Chapter 3 chronic bronchitis & emphysema.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDM2NDE4MDgyNDY4ODU0)",
              "[<b>Chapter 4 Asthma.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDM3NDIwMTA2ODIzNzgx)",
              "[<b>Chapter 5 sarcoidosis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDM4NDIyMTMxMTc4NzA4)",
              "[<b>Chapter 6 pneumonia.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDM5NDI0MTU1NTMzNjM1)",
              "[<b>Chapter 7 ARDS.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQwNDI2MTc5ODg4NTYy)",
              "[<b>Chapter 8 pulmonary TB.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQxNDI4MjA0MjQzNDg5)",
              "[<b>Chapter 9 pulmonary embolism.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQyNDMwMjI4NTk4NDE2)",
              "[<b>Chapter 10 pulmonary hypertension.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQzNDMyMjUyOTUzMzQz)",
              "[<b>Chapter 11 obstructive sleep apnea.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQ0NDM0Mjc3MzA4Mjcw)",
              "[<b>Chapter 12 pleural effusion.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQ1NDM2MzAxNjYzMTk3)",
              "[<b>Chapter 13 pneumothorax.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQ2NDM4MzI2MDE4MTI0)",
              "[<b>Chapter 14 respiratory failure.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQ3NDQwMzUwMzczMDUx)",
              "[<b>Chapter 15 ciliaer dyskinesia & cystic fibrosis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQ4NDQyMzc0NzI3OTc4)",
              "[<b>Chapter 16 bronchiectasis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDQ5NDQ0Mzk5MDgyOTA1)",
              "[<b>Chapter 17 interstitial lung disease.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDUwNDQ2NDIzNDM3ODMy)",
              "[<b>Chapter 18 ABG.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDUxNDQ4NDQ3NzkyNzU5)",
              "[<b>Nephrology</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDUyNDUwNDcyMTQ3Njg2)",
              "[<b>Chapter 1 renal tubular acidosis.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDUzNDUyNDk2NTAyNjEz)",
              "[<b>Chapter 2 batter synd_gittleman synd_lidddle synd.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDU0NDU0NTIwODU3NTQw)",
              "[<b>Chapter 3 investigation in nephrology.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDU1NDU2NTQ1MjEyNDY3)",
              "[<b>Chapter 4 nephrotic syndrome.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDU2NDU4NTY5NTY3Mzk0)",
              "[<b>Chapter 5 nephritic syndrome.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDU3NDYwNTkzOTIyMzIx)",
              "[<b>Chapter 6 acute kidney injury.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDU4NDYyNjE4Mjc3MjQ4)",
              "[<b>Chapter 7 chronic kidney injury.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDU5NDY0NjQyNjMyMTc1)",
              "[<b>Chapter 8 Renal transplant & renal cystic disease.mp4</b>](https://t.me/{{\"X\"}}?start=Z2V0LTE3MDYwNDY2NjY2OTg3MTAy)",
          ]
      
          X = "testingclonepavo_bot"
          links = [link.replace('{{"X"}}', X) for link in links_x]
      
          page_links, has_more = paginate_links(links, page)
          pjmedicine_message = "\n".join(page_links)
      
          navigation_buttons = []
          if page > 0:
              navigation_buttons.append(InlineKeyboardButton("Back", callback_data=f"pjmedicine_{page-1}"))
          if has_more:
              navigation_buttons.append(InlineKeyboardButton("Next 20 Links", callback_data=f"pjmedicine_{page+1}"))
      
          reply_markup = InlineKeyboardMarkup([navigation_buttons] if navigation_buttons else [])
      
          msg = await query.message.reply_text(pjmedicine_message, protect_content=PROTECT_CONTENT, reply_markup=reply_markup)
          asyncio.create_task(schedule_deletion([msg], SECONDS))
