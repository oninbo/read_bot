import config
import telebot
import urllib

bot = telebot.TeleBot(config.token)
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
    user_data[message.chat.id]['speaker'] = 'ermil'
    bot.send_message(message.chat.id, '''Мужской голос установлен''')


@bot.message_handler(commands=['female'])
def handle_start(message):
    user_data[message.chat.id]['speaker'] = 'oksana'
    bot.send_message(message.chat.id, '''Женский голос установлен''')


@bot.message_handler(commands=['speed'])
def handle_start(message):
    bot.send_message(message.chat.id, 'Чтобы установить медленный голос,\n нажмите /slow\nЧтобы установить быстрый голос,\n нажмите /fast')


@bot.message_handler(commands=['slow'])
def handle_start(message):
    user_data[message.chat.id]['speed'] = '0.8'
    bot.send_message(message.chat.id, 'Медленный голос установлен')


@bot.message_handler(commands=['fast'])
def handle_start(message):
    user_data[message.chat.id]['speed'] = '0.8'
    bot.send_message(message.chat.id, 'Медленный голос установлен')


@bot.message_handler(commands=['default'])
def handle_start(message):
    set_user(message.chat.id)
    bot.send_message(message.chat.id, 'Настройки по умолчанию установлены')


@bot.message_handler(content_types=["text"])
def send_audio(message):
    text = message.text
    chat_id = message.chat.id
    user_obj = user_data[chat_id]
    print(text)
    bot.send_message(chat_id, "Готовлюсь. Ждите...")
    params = { 'speed': user_obj['speed'], "format": 'opus', 'lang': 'ru-RU', 'speaker': user_obj['speaker'],
              'key': '3a5d9637-997e-4f41-a560-79f74d173eaa', 'text': text}
    try:
        urllib.request.urlretrieve(
            "https://tts.voicetech.yandex.net/generate?" + urllib.parse.urlencode(params),"voice.ogg")
        voice = open('voice.ogg', 'rb')
        bot.send_voice(chat_id, voice)
        #bot.send_message(message.chat.id, "Чтобы отправить текст для чтения снова, отправьте текст сообщением")
    except urllib.error.HTTPError as e:
        print(e)
        if e.code == 414:
            bot.send_message(chat_id, "Слишком длинный текст. Попробуйте еще раз")
        else:
            bot.send_message(chat_id, "Неизвестная ошибка. Попробуйте еще раз")



if __name__ == '__main__':
     bot.polling(none_stop=True)