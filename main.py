import telebot
from telebot import types
import config

from threading import Thread

token = "1505673717:AAGbj_khs5di7W9_t1Kg5ljac0-aixdXqGg"
chat = '-1001489902826'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def geo(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_geo = types.KeyboardButton(text="Я на месте", request_location=True)
	keyboard.add(button_geo)
	bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)

@bot.message_handler(commands=["excel"])
def exel(message):
	print(message.chat.id)
	if message.chat.id in config.ADMINS:
		
		bot.send_message(message.chat.id, 'Отчет:')

		with open('work.xlsx', 'rb') as f:
			bot.send_document(message.chat.id, f)
	else:
		bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(commands=["clearexcel"])
def exel(message):
	print(message.chat.id)
	if message.chat.id in config.ADMINS:
		
		bot.send_message(message.chat.id, 'Очищено!')

		with open('clearwork.xlsx', 'rb') as f:
			data = f.read()


		with open('work.xlsx', 'wb') as f:
			f.write(data)
	else:
		bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(content_types=["location"])
def location(message):
	if message.location is not None:
		
		print(message)

		callback = config.add_coords(message.chat.first_name + (' ' + str(message.chat.last_name) if message.chat.last_name else ''), message.location.latitude, message.location.longitude)

		if callback == 'errad':
			bot.send_message(message.chat.id, 'Вы очень далеко от ТЦ')
		elif callback == 'errtime-':
			bot.send_message(message.chat.id, 'Вы пришли слишком рано')
		elif callback == 'errtime+':
			bot.send_message(message.chat.id, 'Вы опоздали')
			bot.send_message(chat, message.chat.first_name + (' ' + str(message.chat.last_name) if message.chat.last_name else '') + ' опоздал!')
		elif callback == 'good':
			bot.send_message(message.chat.id, 'Красавчик, пришёл вовремя, сегодня твой день👍')
		else:
			bot.send_message(message.chat.id, 'Что то пошло не так')

	else:

		bot.send_message(message.chat.id, 'Отправьте геопозицию еще раз')



if __name__ == '__main__':
	bot.infinity_polling(True)