import telebot
from telebot import types
import config

from threading import Thread
from time import time

token = "1505673717:AAGbj_khs5di7W9_t1Kg5ljac0-aixdXqGg"
chat = '-1001489902826'

bot = telebot.TeleBot(token)

temp = dict()

@bot.message_handler(commands=["start", "geo"])
def geo(message):
	keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
	button_geo = types.KeyboardButton(text="Я на месте", request_location=True)
	keyboard.add(button_geo)
	temp.update({message.chat.id: time()})
	bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение, у тебя 3 секунды", reply_markup=keyboard)



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
def clexel(message):
	print(message.chat.id)
	if message.chat.id in config.ADMINS:
		
		bot.send_message(message.chat.id, 'Очищено!')

		with open('clearwork.xlsx', 'rb') as f:
			data = f.read()


		with open('work.xlsx', 'wb') as f:
			f.write(data)
	else:
		bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=["document"])
def get_dock(message):
	try:
		if message.chat.id in config.ADMINS:
			bot.send_message(message.chat.id, 'Старый отчет:')
			exel(message)

			chat_id = message.chat.id
			file_info = bot.get_file(message.document.file_id)
			downloaded_file = bot.download_file(file_info.file_path)

			with open('work.xlsx', 'wb') as f:
				f.write(downloaded_file)

			bot.send_message(message.chat.id, 'Все ок!')
	except:
		bot.send_message(message.chat.id, 'ОШИБКА!')
@bot.message_handler(content_types=["location"])
def location(message):
	print(message)
	if not message.forward_from:
		if message.location is not None:
			if message.chat.id in temp.keys():
				st = temp[message.chat.id]

				if time() - st > 3:
					bot.send_message(message.chat.id, 'Вы не успели')
					temp.pop(message.chat.id)
				else:	

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
					elif callback == 'green':
						bot.send_message(message.chat.id, 'Вы уже отметились!')
					elif callback == 'coord':
						bot.send_message(message.chat.id, 'Я подозреваю это сообщение в пересылке')
					else:
						bot.send_message(message.chat.id, 'Что то пошло не так')

			
			else:
				bot.send_message(message.chat.id, 'Вы не успели')

		else:

			bot.send_message(message.chat.id, 'Попробуйте еще раз')
	else:
		bot.send_message(message.chat.id, 'Это пересланое сообщение')


if __name__ == '__main__':
	while 1:
		try:
			bot.polling(none_stop=True)
		except:
			print('err')
	# bot.infinity_polling(True)