import psycopg2
from aiogram import Bot, Dispatcher, executor, types


bot = Bot(token="")
dp = Dispatcher(bot)

try:
	conn = psycopg2.connect(
		dbname='',
		user='',
		password='',
		host=''
	)
	conn.autocommit = True
	cursor = conn.cursor()
except Exception as _ex:
	print("[INFO] Connection to PostgreSQL failed!")



@dp.message_handler()
async def message(message: types.Message):
	await	message.answer("Привет!")
	firstname = message.from_user.first_name
	username = message.from_user.username
	userid = str(message.from_user.id)
	cursor.execute('SELECT first_name FROM users WHERE userid = %s', (userid,))
	if cursor.fetchone() == None:
		cursor.execute('INSERT INTO users (first_name, username, userid) VALUES (%s, %s, %s)', (firstname, username, userid))
		print("[INFO] New user "+firstname+".")
	else:
		print("[INFO] User "+firstname+".")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)