import config
import telebot
import urllib

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Чтобы отправить текст для чтения, отправьте текст сообщением")


@bot.message_handler(content_types=["text"])
def send_audio(message):
    text = message.text
    chat_id = message.chat.id
    print(text)
    bot.send_message(chat_id, "Готовлюсь. Ждите...")
    try:
        urllib.request.urlretrieve(
            "https://tts.voicetech.yandex.net/generate?format=opus&lang=ru-RU&speaker=oksana&emotion=neutral&key=3a5d9637-997e-4f41-a560-79f74d173eaa&text=" + urllib.parse.quote_plus(text),
            "voice.ogg")
        voice = open('voice.ogg', 'rb')
        bot.send_voice(chat_id, voice)
    except urllib.error.HTTPError as e:
        print(e)
        if e.code == 414:
            bot.send_message(chat_id, "Слишком длинный текст. Попробуйте еще раз")
        else:
            bot.send_message(chat_id, "Неизвестная ошибка. Попробуйте еще раз")



if __name__ == '__main__':
     bot.polling(none_stop=True)