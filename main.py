import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from config import *
import horoscope
import random

def write_msg(sender, message):
    authorize.method('messages.send', {'chat_id': sender, 'message': message, "random_id": 0})

def send_picture(sender):
    authorize.method('messages.send', {'chat_id': sender, 'attachment': 'photo-201338515_457239018', 'random_id': 0})

def pin_message(user_id, msg_ID):
    authorize.method('messages.pin', {'peer_id': 2000000000 + user_id, 'conversation_message_id': msg_ID})

def unpin_message(user_id):
    authorize.method('messages.unpin', {'peer_id': 2000000000 + user_id})

def search_msg(msg_context, user_id):
    return authorize.method('messages.search', {'q': msg_context, 'peer_id': user_id, 'preview_length': 0, 'group_id': 201338515})

authorize = vk_api.VkApi(token = main_token)
longpoll = VkBotLongPoll(authorize, group_id=201338515)


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get('text') != "":
        msg = event.message.get('text')
        msg_words = event.message.get('text').lower().split()

        sender = event.chat_id
        print(sender)

        user_id = event.message.get('from_id')

        msg_id = event.message.get('conversation_message_id')
        print(msg_id)

        print(msg_words)

        for i in msg_words:
            if i in welcome_words:
                write_msg(sender, 'Мeow,sweety')
                break

        if msg_words[0] == '/гороскоп':
            if msg == '/гороскоп':
                write_msg(sender, 'Укажите знак зодиака 👺')
            elif msg_words[1].lower() in zz:
                write_msg(sender, horoscope.parse(msg_words[1].lower()))
            else:
                write_msg(sender, 'Моими лапами невозможно найти подобный знак зодиака 😿')

        if msg == '/help':
            write_msg(sender, commands)

        if msg == 'негрывсе':
            print(search_msg("Meow,sweety", user_id))

        if msg == '/bibametr':
            a = random.randint(1, 100)
            if a >= 50:
                smile = ' 👍🏻'
            else:
                smile = ' 😭'
            write_msg(sender, 'Биба ' + str(a) + 'см' + smile)

        if msg == 'ping':
            write_msg(sender, 'pong')

        if msg == '/пикча_с_котиком':
            send_picture(sender)

        for i in msg_words:
            if i in badwords:
                pin_message(sender, msg_id)
                if user_id not in bad_people_list:
                    bad_people_list.append(user_id)
                write_msg(sender, 'осуждаю, быдло!')
                unpin_message(sender)
                break

        if msg.lower() == '/нарушители':
            for i in bad_people_list:
                write_msg(sender, '@id' + str(i))