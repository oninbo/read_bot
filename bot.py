import time
import config
import telebot
import urllib
import os

bot = telebot.TeleBot(config.token)
max_text_length = 1000
handling = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Чтобы отправить текст для чтения, отправьте текст сообщением")


@bot.message_handler(commands=['help'])
def handle_start(message):
    bot.send_message(message.chat.id, "Чтобы отправить текст для чтения, отправьте текст сообщением")


def text_to_audio(text, index):
    urllib.request.urlretrieve(
        "https://tts.voicetech.yandex.net/generate?format=opus&lang=ru-RU&speaker=oksana&emotion=neutral&key=3a5d9637-997e-4f41-a560-79f74d173eaa&text=" + urllib.parse.quote_plus(
            text),
        "voice" + index + ".ogg")


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
    bot.send_message(chat_id, "Готовлюсь. Ждите...")
    for i in range(0, parts_number):
        if i == parts_number - 1:
            end = text_length
        else:
            end = part_length*(i+1)
        try:
            number = i + 1
            index = str(number) +'_'+ str(message_id)
            text_to_audio(text[part_length*i:end], index)
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