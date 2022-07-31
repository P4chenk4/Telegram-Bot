import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from config import *

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN,)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

try:
	conn = psycopg2.connect(
		dbname=DBNAME,
		user=USER,
		password=PASSWORD,
		host=HOST
	)
	conn.autocommit = True
	cursor = conn.cursor()
	print("[INFO] Connection to PostgreSQL success!")
except Exception as _ex:
	print("[ERROR] Connection to PostgreSQL failed!")

@dp.message_handler()
async def message(message: types.Message):
	await bot.send_message(message.chat.id, "Привет!")
	firstname = message.from_user.first_name
	username = message.from_user.username
	userid = str(message.from_user.id)
	cursor.execute('SELECT first_name FROM '+TABLENAME+' WHERE userid = %s', (userid,))
	if cursor.fetchone() == None:
		cursor.execute('INSERT INTO '+TABLENAME+' (first_name, username, userid) VALUES (%s, %s, %s)', (firstname, username, userid))
		print("[INFO] New user "+firstname+" added to database.")
	else:
		print("[INFO] User "+firstname+" send message.")


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()

if __name__ == '__main__':
	start_webhook(
    	dispatcher=dp, 
  		webhook_path=WEBHOOK_PATH,
  		on_startup=on_startup,
  		on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )