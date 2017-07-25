import time
import config
import telebot
import urllib
import os

bot = telebot.TeleBot(config.token)
max_text_length = 1000
handling = {}
user_data = {}


def set_user(chat_id):
    if chat_id not in user_data.keys():
        user_data[chat_id] = {}
    user_data[chat_id]['speaker'] = 'oksana'
    user_data[chat_id]['speed'] = '0.9'


@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    bot.send_message(message.chat.id, '''Привет! Чтобы отправить текст для чтения, отправьте текст сообщением''')
    bot.send_message(message.chat.id, 'Для справки нажмите /help')
    set_user(chat_id)


@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     'Чтобы поменять голос,\n нажмите /voice\nЧтобы поменять скорость,\n нажмите /speed\nЧтобы установить настройки поумолчанию,\n нажмите /default')


@bot.message_handler(commands=['voice'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Чтобы установить мужской голос,\n нажмите /male\nЧтобы установить женский голос,\n нажмите /female')


@bot.message_handler(commands=['male'])
def handle_start(message):
    try:
        user_data[message.chat.id]['speaker'] = 'ermil'
    except:
        set_user(message.chat.id)
        user_data[message.chat.id]['speaker'] = 'ermil'
    bot.send_message(message.chat.id, '''Мужской голос установлен''')


@bot.message_handler(commands=['female'])
def handle_start(message):
    try:
        user_data[message.chat.id]['speaker'] = 'oksana'
    except:
        set_user(message.chat.id)
        user_data[message.chat.id]['speaker'] = 'oksana'
    bot.send_message(message.chat.id, '''Женский голос установлен''')


@bot.message_handler(commands=['speed'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Чтобы установить медленный голос,\n нажмите /slow\nЧтобы установить быстрый голос,\n нажмите /fast')


@bot.message_handler(commands=['slow'])
def handle_start(message):
    try:
        user_data[message.chat.id]['speed'] = '0.8'
    except:
        set_user(message.chat.id)
        user_data[message.chat.id]['speed'] = '0.8'
    bot.send_message(message.chat.id, 'Медленный голос установлен')


@bot.message_handler(commands=['fast'])
def handle_start(message):
    try:
        user_data[message.chat.id]['speed'] = '0.9'
    except:
        set_user(message.chat.id)
        user_data[message.chat.id]['speed'] = '0.9'
    bot.send_message(message.chat.id, 'Быстрый голос установлен')


@bot.message_handler(commands=['default'])
def handle_start(message):
    set_user(message.chat.id)
    bot.send_message(message.chat.id, 'Настройки по умолчанию установлены')


@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Чтобы отправить текст для чтения, отправьте текст сообщением")


def text_to_audio(text, speed, speaker, index):
    params = {'speed': speed, "format": 'opus', 'lang': 'ru-RU', 'speaker': speaker,
              'key': '3a5d9637-997e-4f41-a560-79f74d173eaa', 'text': text}
    urllib.request.urlretrieve(
        "https://tts.voicetech.yandex.net/generate?" + urllib.parse.urlencode(params),"voice" + index + ".ogg")


def send_audio(chat_id, index):
    voice = open("voice" + index + ".ogg", 'rb')
    bot.send_voice(chat_id, voice)



def delete_audio(index):
    os.remove("voice" + index + ".ogg")


@bot.message_handler(content_types=["text"])
def reply(message):
    chat_id = message.chat.id
    global handling
    while chat_id in handling and handling[chat_id]:
        time.sleep(10)
    handling[chat_id] = True
    text = message.text
    message_id = message.message_id
    print(message)
    parts_number = 1
    text_length = len(text)
    while text_length // parts_number > max_text_length:
        parts_number = parts_number*2
    part_length = text_length // parts_number
    try:
        user_obj = user_data[chat_id]
    except:
        set_user(chat_id)
        user_obj = user_data[chat_id]
    print(text)
    bot.send_message(chat_id, "Готовлюсь. Ждите...")
    for i in range(0, parts_number):
        if i == parts_number - 1:
            end = text_length
        else:
            end = part_length*(i+1)
        try:
            number = i + 1
            index = str(number) +'_'+ str(message_id)
            text_to_audio(text[part_length*i:end], user_obj['speed'], user_obj['speaker'], index)
        except urllib.error.HTTPError as e:
            print(e)
            print(len(text))
            bot.send_message(chat_id, "Слишком длинный текст (более "+str(max_text_length)+" сиволов). Попробуйте еще раз")
        except urllib.error.URLError as e:
            print(e)
            bot.send_message(chat_id, "Ошибка. Попробуйсте еще раз")
    for i in range(0, parts_number):
        number = i + 1
        index = str(number) +'_'+ str(message_id)
        if parts_number > 1:
            bot.send_message(chat_id, str(number)+" часть из "+ str(parts_number))
        send_audio(chat_id, index)
        delete_audio(index)
    #bot.send_message(chat_id, "Чтобы отправить текст для чтения снова, отправьте текст сообщением")
    handling[chat_id] = False



if __name__ == '__main__':
     bot.polling(none_stop=True)