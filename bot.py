import telebot
from telebot import types
from KRC import ParserKRC
from push_to_google_sheets import GoogleSheet

bot = telebot.TeleBot('6270832355:AAGb0phBLovlvAOwcU-TSGm2mZIn8jFHDlM')

@bot.message_handler(commands=['start'])
def start_message(message, msc):
    bot.send_message(message.chat.id, msc)
'https://www.ozon.ru/api/composer-api.bx/page/json/v1?url=https://www.ozon.ru/category/elektroinstrumenty-9857/hammer-26303172/%2F%3Fpage%3D11'

@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    item1 = types.KeyboardButton("Запустить все")
    item2 = types.KeyboardButton("Запустить Ozon")
    item3 = types.KeyboardButton("Запустить WB")
    item4 = types.KeyboardButton("Запустить SBER")
    item5 = types.KeyboardButton("Запустить VI")
    item6 = types.KeyboardButton("Запустить citilink")
    item7 = types.KeyboardButton("Запустить Mvideo")
    item8 = types.KeyboardButton("Запустить eldorado")
    item9 = types.KeyboardButton("Запустить holodilnik")

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    bot.send_message(message.chat.id,'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Запустить все":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить все')
            GoogleSheet().delete_all()
            ParserKRC().main()
            bot.send_message(message.chat.id, 'Закончили парсить ')
    if message.text == "Запустить Ozon":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить Ozon')
            ParserKRC().parser_ozon()
            bot.send_message(message.chat.id, 'Закончили парсить Ozon')
    if message.text == "Запустить WB":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить WB')
            ParserKRC().parser_ozon()
            bot.send_message(message.chat.id, 'Закончили парсить WB')
    if message.text == "Запустить SBER":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить SBER')
            ParserKRC().parser_sber()
            bot.send_message(message.chat.id, 'Закончили парсить SBER')
    if message.text == "Запустить VI":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить VI')
            ParserKRC().parser_vi()
            bot.send_message(message.chat.id, 'Закончили парсить VI')
    if message.text == "Запустить citilink":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить citilink')
            ParserKRC().parser_citilink()
            bot.send_message(message.chat.id, 'Закончили парсить citilink')
    if message.text == "Запустить Mvideo":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить Mvideo')
            ParserKRC().parserMvideo()
            bot.send_message(message.chat.id, 'Закончили парсить Mvideo')
    if message.text == "Запустить eldorado":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить eldorado')
            ParserKRC().parser_eldorado()
            bot.send_message(message.chat.id, 'Закончили парсить eldorado')
    if message.text == "Запустить holodilnik":
        if __name__ == '__main__':
            bot.send_message(message.chat.id, 'Начали парсить holodilnik')
            ParserKRC().parser_holodilnik()
            bot.send_message(message.chat.id, 'Закончили парсить holodilnik')


bot.infinity_polling()