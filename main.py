import asyncio
import horoscope
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from config import *

authorize = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(authorize, group_id)
upload = vk_api.VkUpload(authorize)

async def write_chat_msg(chat_id, message):
    authorize.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': 0})

async def send_picture(chat_id, message, attachment):
    authorize.method('messages.send', {'chat_id': chat_id, 'message': message, 'attachment': attachment, 'random_id': 0})

async def main():
    for event in longpoll.listen():
        try:
            await asyncio.gather(event_handle(event))
        except:
             continue
                     
async def event_handle(event):
    try:
        if event.type == VkBotEventType.MESSAGE_NEW: 
            if event.from_chat and event.message.get('text') != "":
                
                ### Часто использующиеся параметры
                msg = event.message.get('text').lower()
                words = msg.split()
                user_id = event.message.get('from_id') 
                chat_id = event.chat_id
                
                if words[0] == '/гороскоп':
                    await horoscope(chat_id, words)
 except:
        continue
        
async def horoscope(chat_id, words):
    try:
        if words[1] in zodiac_signs:
            photo = upload.photo_messages('Ваш путь к картинке')
            attachment = "photo" + str(photo[0]['owner_id']) + "_" + str(photo[0]['id']) + "_" + str(photo[0]['access_key'])
            if len(words) > 2:
                await send_picture(chat_id, await horoscope.get_horoscope(words[1], words[2]), attachment)
            else:
                await send_picture(chat_id, await horoscope.get_horoscope(words[1]), attachment)
        else:
            await write_chat_msg(chat_id, 'Моими лапами невозможно найти подобный знак зодиака 😿') 
    except:
        await write_chat_msg(chat_id, 'Укажите знак зодиака 👺')
   
asyncio.run(main())
