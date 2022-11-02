from settings import *
from extensions import *
import telebot


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help', ])
def show_info(message: telebot.types.Message):
    bot.send_message(message.chat.id, INFO_TEXT)


@bot.message_handler(commands=['values', ])
def show_values(message: telebot.types.Message):
    try:
        values = APIManager().get_symbols()
        text = 'Список доступных валют:\n'
        for key in values:
            text = f'{text}{values[key]} ({key})\n'
    except APIException as exception:
        text = f'{type(exception).__name__}\n{exception}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    data = message.text.split()
    try:
        text = f"Цена валюты: {APIManager().get_price(data[0], data[1], float(data[2]))}"
    except APIException as exception:
        text = f'{type(exception).__name__}\n{exception}'
    except (ValueError, IndexError) as exception:
        text = f'{type(exception).__name__}\nЗапрос введен неврено\n/help - подсказа по формату запроса'
    bot.reply_to(message, text)


bot.polling(none_stop=True)