#!/usr/bin/python

import telebot
import config
import cherrypy

WEBHOOK_HOST = '62.109.19.45'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '62.109.19.45'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

from datetime import datetime
from telebot import types

bot = telebot.TeleBot(config.token)

special_deal = "AgADAgAD5KcxG0x78gvqpMjZiqcAAU_QD0sNAASTNV0rnJV4y8_pAQABAg"
menu = "AgADAgAD5acxG0x78gu69VnqGWsdcJIVSw0ABA-s_bbCJMHQquQBAAEC"

text_messages = {
    'contacts':
        u'\nМы находимся по адресу:'
        u'\nг. Челябинск, ул. Кирова, 167\n\n'
        u'Работаем каждый день \nс 16:00 до 4:00\n\n'
        u'Задать вопрос или забронировать столик по телефону: \n+7 (351) 222-40-90\n\n'
        u'Группа ВК: vk.com/topkabar\n\n'
        u'Сайт: topkabar.ru\n\n',
    'special_offer':
        u'Теперь каждое воскресенье мы делаем скидку в 20% для всех сотрудников заведений общепита России!'
        u'\nПредъяви свой рабочий бейдж или карту, расскажи, где работаешь и получи бонус.'
        u'\nМы знаем, как хочется отдохнуть в приличном месте, но не у себя на работе, поэтому, Топка – твой выбор.'
        u'\n\nНаш телефон для бронирования: +7 (351) 222-40-90.\n',
    'feedback':
        u'Вы можете оставить отзыв или пожелание по работе Топка-Бара и бота.'
        u'\n\nНаберите ваше сообщение, \nа затем подтвердите отправку отзыва.'
        u'\n\n(Не менее 30 символов)'
}

food = {
    0: "AgADAgAD66cxG0x78gv8Qgp_ST_0aefLgQ0ABDs_hlF2dQABDemoAgABAg",
    1: "AgADAgAD7KcxG0x78gsU5rCQ2qSjhAI7Sw0ABMEY_Y2ljv0d2_wBAAEC"
}

drinks = {
    0: "AgADAgAD4qcxG0x78gtxiZdAZ_6zrIsOSw0ABGpcZojXVcO3XekBAAEC",
    1: "AgADAgAD5qcxG0x78guLrAABjvHmmVvVEEsNAAS0CA5OzZnTB8LlAQABAg",
    2: "AgADAgAD56cxG0x78gvN8RFHtcwwXKHZgQ0ABA_yEgs6bstqJakCAAEC",
    3: "AgADAgAD6KcxG0x78gtPaVz2r_IJb6LXgQ0ABKRTwRjMUhR-N6MCAAEC",
    4: "AgADAgAD6acxG0x78gtE1vYY-lzcGx4TSw0ABIJ-c_SEVmkyEeYBAAEC",
    5: "AgADAgAD6qcxG0x78gtGhL6V12k200zUgQ0ABOr69tv_6IRUY6YCAAEC"
}

global food_page
food_page = 0
global drinks_page
drinks_page = 0
global curr_page
curr_page = "🏠 Главная"

class WebhookServer(object):
	@cherrypy.expose
	def index(self):
		if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
		    length = int(cherrypy.request.headers['content-length'])
		    json_string = cherrypy.request.body.read(length).decode("utf-8")
		    update = telebot.types.Update.de_json(json_string)
		    # Эта функция обеспечивает проверку входящего сообщения
		    bot.process_new_updates([update])
            return ''
        	else:
    			raise cherrypy.HTTPError(403)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def function(message):

    def Главная():
        global food_page
        food_page = 0
        global drinks_page
        drinks_page = 0
        global curr_page
        curr_page = message.text
        print("Current Page:" + curr_page)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'📕 Меню')
        keyboard.row(u'❗ Акции')
        keyboard.row(u'📞 Контакты')
        keyboard.row(u'✉ Оставить отзыв')
        bot.send_message(message.chat.id, "🏠 Главная", reply_markup=keyboard)

    def Меню():
        global food_page
        food_page = 0
        global drinks_page
        drinks_page = 0
        global curr_page
        curr_page = message.text
        print("Current Page:" + curr_page)
        bot.send_photo(message.chat.id, menu)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'🍽 Блюда и Закуски', u'🍺 Напитки')
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "📕 Меню", reply_markup=keyboard)

    def Акции():
        global curr_page
        curr_page = message.text
        print("Current Page:" + curr_page)
        bot.send_photo(message.chat.id, special_deal)
        global curr_date
        curr_date = datetime.now()
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "Актуальные акции на " + str(curr_date.strftime('%d/%m/%Y %H:%M\n\n')) + text_messages['special_offer'], reply_markup=keyboard)

    def Контакты():
        global curr_page
        curr_page = message.text
        print("Current Page:" + curr_page)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "📞 Контакты:", reply_markup=keyboard)
        bot.send_message(message.chat.id, text_messages['contacts'], disable_web_page_preview=True)

    def Донат():
        global curr_page
        curr_page = message.text
        print("Current Page:" + curr_page)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "Помогите разработчику накопить на учебники по программированию\
                                        \n\nЯндекс-кошелек: money.yandex.ru/to/410013576076940/30\
                                        \n\nНаписать разработчику: telegram.me/linexer", disable_web_page_preview=True, reply_markup=keyboard)

    def Подтверждение_отзыва():
        global curr_page
        curr_page = "Подтверждение Отзыва"
        print("Verifying feedback...")
        print("Current Page:" + curr_page)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'✔ Подтвердить')
        keyboard.row(u'💰 Поддержать')
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "Отправить отзыв?", reply_markup=keyboard)

    def Отзыв():
        global curr_page
        curr_page = "✉ Оставить Отзыв"
        print("Current Page:" + curr_page)
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'💰 Поддержать')
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, text_messages['feedback'], reply_markup=keyboard)

    def Блюда_и_Закуски():
        global curr_page
        curr_page = "🍽 Блюда и Закуски"
        print("Current Page:" + curr_page)
        #global food_page
        bot.send_photo(message.chat.id, food[food_page])
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row(u'◀', u'▶')
        keyboard.row(u'📕 Меню')
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "Меню / Блюда и Закуски / Страница " + str(food_page+1) + "/2", reply_markup=keyboard)

    def Напитки():
        global curr_page
        curr_page = "🍺 Напитки"
        print("Current Page:" + curr_page)
        # global food_page
        bot.send_photo(message.chat.id, drinks[drinks_page])
        keyboard = types.ReplyKeyboardMarkup(True, False)
        keyboard.row('◀ ', ' ▶')
        keyboard.row(u'📕 Меню')
        keyboard.row(u'🏠 Главная')
        bot.send_message(message.chat.id, "Меню / Напитки / Страница " + str(drinks_page + 1) + "/6",
                         reply_markup=keyboard)

    #curr_page = "Главная"
    if (message.text) == "/start" or (message.text) == "🏠 Главная":
        message.text = '🏠 Главная'
        Главная()
    elif (message.text) == "/donate" or (message.text) == "💰 Поддержать":
        message.text = 'Донат'
        Донат()
    elif (message.text) == "/menu" or (message.text) == "📕 Меню":
        Меню()
    elif (message.text) == "/special" or (message.text) == "❗ Акции":
        Акции()
    elif (message.text) == "/contacts" or (message.text) == "📞 Контакты":
        Контакты()
    elif (message.text) == "/feedback" or (message.text) == "✉ Оставить отзыв":
        Отзыв()
    elif (message.text) == "/food" or (message.text) == "🍽 Блюда и Закуски":
        Блюда_и_Закуски()
    elif curr_page == "🍽 Блюда и Закуски":
        if(message.text) == u'▶':
            global food_page
            food_page = food_page + 1
            food_page = abs(food_page % 2)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            Блюда_и_Закуски()
        elif (message.text) == u'◀':
            food_page = food_page - 1
            food_page = abs(food_page % 2)
            bot.send_chat_action(message.chat.id, 'upload_photo')
            Блюда_и_Закуски()
    elif (message.text) == "/drinks" or (message.text) == "🍺 Напитки":
        Напитки()
    elif curr_page == "🍺 Напитки":
        if (message.text) == u'▶':
            global drinks_page
            print("food_page before: " + str(drinks_page))
            drinks_page = drinks_page + 1
            drinks_page = abs(drinks_page % 6)
            print("food_page after: " + str(drinks_page))
            Напитки()
        elif (message.text) == u'◀':
            print("food_page before: " + str(drinks_page))
            drinks_page = drinks_page - 1
            drinks_page = abs(drinks_page % 6)
            print("food_page after: " + str(drinks_page))
            Напитки()
    elif (message.text) == "Назад" and curr_page == "📕 Меню":
        Главная()
    elif (message.text) == "Назад" and curr_page == "📞 Контакты":
        Главная()
    elif curr_page == "✉ Оставить Отзыв":
        if len(message.text) > 30:
            print("Current Page:" + curr_page)
            global feedback_message
            global feedback_message_id
            feedback_message = message.text
            feedback_message_id = message.message_id
            print("Feedback:" + feedback_message)
            print("Feedback Message ID:" + str(feedback_message_id))
            Подтверждение_отзыва()
        elif len(message.text) < 30:
            print("Current Page:" + curr_page)
            bot.send_message(message.chat.id, "Символов в сообщении: " + str(len(message.text)) + "\nДлина отзыва должна быть больше 30 символов")
    elif curr_page == "Подтверждение Отзыва":
        if(message.text) == "✔ Подтвердить":
            bot.send_message(message.chat.id, "Спасибо за Ваш отзыв!")
            bot.send_message(config.admin_chat, "💬 Новый отзыв: " + feedback_message)
            Главная()

def listener(message):
    for m in message:
        print("====================================")
        print("Listener Chat ID: " + str(m.chat.id))
        print("Listener Message Id:" + str(m.message_id))
        print("Listener Text:" + m.text)

bot.set_update_listener(listener)

bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})

bot.polling(none_stop=True)