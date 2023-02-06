from telebot import *
from config import TOKEN, keys
from extensions import ApiException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<название валюты> \
<в какую валюту перевести><количество переводимой валюты>\
(через пробел)\
\nУвидеть список всех доступных валют - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        print(values)
        if len(values) != 3:
            raise ApiException('Неверно задано количество параметров!(нужно 3)')
        print(message.from_user.username)
        base, quote, amount = values
        base = base.lower()
        quote = quote.lower()

        total_quote = Converter.convert(base, quote, amount)
    except ApiException as e:
        bot.reply_to(message, f"ошибка пользователя: \n {e}")
    except Exception as e:
        bot.reply_to(message, f"не удалось обработать команду: \n {e}")
    else:
        total_price = float(total_quote) * float(amount)
        total_price = '{:f}'.format(total_price)
        text = f"{amount} {base} = {total_price} {quote}"
        bot.send_message(message.chat.id, text)

bot.polling()