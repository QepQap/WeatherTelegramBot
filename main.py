import telebot
import open_weather_data

# API токен бота в Telegram
API_TOKEN = '5776980836:AAE3av3rhFb80KB4kItkMV2rpiO3vxN_lPc'
bot = telebot.TeleBot(API_TOKEN)


# Функция срабатывает на команды /help и /start
@bot.message_handler(commands=['help', 'start'])
def welcome_message(message):
    bot.send_message(message.chat.id, 'Напиши название пункта',)
    bot.register_next_step_handler(message, get_weather)

# Функция срабатывает ввод названия города
@bot.message_handler(func=lambda message: True)
def get_weather(message):
    # Добавляем клавиатуру
    keywords_city = telebot.types.ReplyKeyboardMarkup(True)
    keywords_city.row(message.text)

    # Просим сервер сказать какая погода будет
    weather_data = open_weather_data.get_open_weather_one_day(message.text)
    if weather_data == 'Напишите название пункта правильно':
        bot.send_message(message.chat.id, weather_data)
    else:
        bot.send_message(message.chat.id, weather_data,
                     reply_markup=keywords_city)

    bot.register_next_step_handler(message, get_weather)

bot.polling(none_stop=True, interval=0)
