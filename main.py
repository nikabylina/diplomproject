import telebot
import sqlite3
import webbrowser
from telebot import types

bot = telebot.TeleBot('6691246671:AAE4BknDUIJH4F7tJnFrTSgxHyinv_YOfF0')


name = 'None'


@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('bottelegram.sql')
    curs = connect.cursor()

    curs.execute('CREATE TABLE IF NOT EXISTS users (id int primary key,name varchar(50), pass varchar(50))')
    connect.commit()
    curs.close()
    connect.close()

    bot.send_message(message.chat.id, 'Привет, введите ваше имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    connect = sqlite3.connect('bottelegram.sql')
    curs = connect.cursor()

    curs.execute("INSERT INTO users (name,pass) VALUES ('%s', '%s')" % (name, password))
    connect.commit()
    curs.close()
    connect.close()

    knopka = telebot.types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован,переходи в /menu и выбирай нужную категорию', reply_markup=knopka)


@bot.message_handler(commands=['menu'])
def menu(message):
    button = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Новости Беларуси')
    button.row(btn1)
    btn2 = types.KeyboardButton('Погода Беларуси')
    button.row(btn2)
    btn3 = types.KeyboardButton('Курс валют на сегодня')
    button.row(btn3)
    btn4 = types.KeyboardButton('Гороскоп')
    button.row(btn4)

    bot.send_message(message.chat.id, (f'Привет, {message.from_user.first_name}'), reply_markup=button)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Новости Беларуси':
        webbrowser.open('https://dzen.ru/news/region/Belarus?issue_tld=ru')
    bot.register_next_step_handler(message, on_click1)


def on_click1(message):
    if message.text == 'Погода Беларуси':
        # def get_weather(message):
        #     city = message.text.strip().lower()
        webbrowser.open('https://yandex.by/pogoda/region/149')
    bot.register_next_step_handler(message, on_click2)


def on_click2(message):
    if message.text == 'Курс валют на сегодня':
        webbrowser.open('https://bankibel.by/kursy-valut')
    bot.register_next_step_handler(message, on_click3)


def on_click3(message):
    if message.text == 'Гороскоп':
        webbrowser.open('https://horo.mail.ru/')


@bot.message_handler(commands=['news', 'новости', 'новости беларуси'])
def news(message):
    webbrowser.open('https://dzen.ru/news/region/Belarus?issue_tld=ru')


@bot.message_handler(commands=['weather', 'погода', 'погода в беларуси', 'погода беларусь'])
def weather(message):
    webbrowser.open('https://yandex.by/pogoda/region/149')


@bot.message_handler(commands=['horoscope', 'горокоп', 'гороскоп на сегодня'])
def horoscope(message):
    webbrowser.open('https://horo.mail.ru/')


@bot.message_handler(commands=['exchange rates', 'курс валют', 'курс валют на сегодня'])
def exchange_rates(message):
    webbrowser.open('https://bankibel.by/kursy-valut')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')


@bot.message_handler(commands=['information'])
def information(message):
    bot.send_message(message.chat.id,
                     'Бот может поделиться с тобой информацией: о погоде в беларуси, новостях беларуси, курсе валют на сегодня, гороскопе,'
                     'выбирай в меню подходящую категорию! ')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID: {message.from_user.id}')


bot.polling(none_stop=True)
