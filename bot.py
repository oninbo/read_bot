import config
import telebot
import urllib

bot = telebot.TeleBot(config.token)
max_text_length = 1000


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Чтобы отправить текст для чтения, отправьте текст сообщением (не более "+str(max_text_length)+" символов)")


def text_to_audio(text):
    urllib.request.urlretrieve(
        "https://tts.voicetech.yandex.net/generate?format=opus&lang=ru-RU&speaker=oksana&emotion=neutral&key=3a5d9637-997e-4f41-a560-79f74d173eaa&text=" + urllib.parse.quote_plus(
            text),
        "voice.ogg")


def send_audio(chat_id):
    voice = open('voice.ogg', 'rb')
    bot.send_voice(chat_id, voice)


@bot.message_handler(content_types=["text"])
def reply(message):
    text = message.text
    chat_id = message.chat.id
    print(text)
    parts_number = 1
    text_length = len(text)
    while text_length // parts_number > 1000:
        parts_number = parts_number*2
    part_length = text_length // parts_number
    bot.send_message(chat_id, "Готовлюсь. Ждите...")
    for i in range(0, parts_number):
        if i == parts_number - 1:
            end = text_length
        else:
            end = part_length*(i+1)
        try:
            text_to_audio(text[part_length*i:end])
            if parts_number > 1:
                bot.send_message(chat_id, str(i+1)+" часть из "+ str(parts_number))
            send_audio(chat_id)
        except urllib.error.HTTPError as e:
            print(e)
            print(len(text))
            bot.send_message(chat_id, "Слишком длинный текст (более "+str(max_text_length)+" сиволов). Попробуйте еще раз")
        except urllib.error.URLError as e:
            print(e)
            bot.send_message(chat_id, "Ошибка. Попробуйсте еще раз")
    bot.send_message(chat_id, "Чтобы отправить текст для чтения снова, отправьте текст сообщением")


if __name__ == '__main__':
    bot.polling(none_stop=True)