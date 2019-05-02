import telegram
import logging
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

bot = telegram.Bot(token = '#########')

from telegram.ext import Updater
updater = Updater(token='##############')
dispatcher = updater.dispatcher

def say_start(bot, update):
	bot.sendMessage(chat_id = update.message.chat_id, text="Привет!! Если вы планируете прямо сейчас пойти в кино, данный бот поможет вам сделать выбор. Введите / чтобы увидеть все функции бота. Удачи))")

from telegram.ext import CommandHandler
start_handler = CommandHandler('start', say_start)
dispatcher.add_handler(start_handler)

def kinolist (bot, update):
	import requests
	from bs4 import BeautifulSoup 
	url = 'http://m.kino.kz/index.htm?city=2&sort=1'
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, "html.parser")
	row = soup.select("body table tr:nth-of-type(3) td.stripe-body div a")[1:]
	for item in row:
		url = item['href']
		name = item.text
		bot.sendMessage(chat_id = update.message.chat_id, text = name)
		uurl = url.replace('htm', 'asp')
		b = 'http://kino.kz'                      
		if "movie" in uurl:
			gg = b + uurl
			import requests
			from bs4 import BeautifulSoup
			if "movie" in gg:
				r = requests.get(gg)
				html = r.text
				soup = BeautifulSoup(html, "html.parser")
				rows = soup.select("div.detail_content table td:nth-of-type(2) div.movie_detail div:nth-of-type(11) a")[:1]
				for item in rows:
					urrl = item['href']
					if "kinopoisk" in urrl:
						dd = urrl + " "
						bot.sendMessage(chat_id = update.message.chat_id, text = dd)
					else:
						bot.sendMessage(chat_id = update.message.chat_id, text = "Ссылка отсутствует")
kinolist_handler = CommandHandler('kinolist', kinolist)
dispatcher.add_handler(kinolist_handler)

def rating (bot, update):
	file = open ("rating.json", "r", encoding = 'utf-8')
	data = json.loads(file.read())
	for item in data:
		if item['rating'] != 0:
			text  = item['Название']
			t = "IMDb"
			tt = "Рейтинг Кинопоиска"
			ttt = "Мой Рейтинг"
			bot.sendMessage(chat_id = update.message.chat_id, text = text)
			bot.sendMessage(chat_id = update.message.chat_id, text = t)
			bot.sendMessage(chat_id = update.message.chat_id, text = (item['IMDb']))
			bot.sendMessage(chat_id = update.message.chat_id, text = tt)
			bot.sendMessage(chat_id = update.message.chat_id, text = (item['kinopoisk']))
			bot.sendMessage(chat_id = update.message.chat_id, text = ttt)
			bot.sendMessage(chat_id = update.message.chat_id, text = (item['rating']))
		else:
			pass

	hh = "Я рекомендую пойти на " + data[0]['Название']
	bot.sendMessage(chat_id = update.message.chat_id, text = hh)

rating_handler = CommandHandler('rating', rating)
dispatcher.add_handler(rating_handler)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


dispatcher.add_error_handler(error)


updater.start_polling()
