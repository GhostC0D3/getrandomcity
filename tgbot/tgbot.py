import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
from aiogram.utils import executor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Настройки бота
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())

# Настройки для доступа к Google Sheets API
GOOGLE_SHEETS_CREDS_FILE = 'credentials.json'
SPREADSHEET_NAME = 'Your Spreadsheet Name'
WORKSHEET_NAME = 'Your Worksheet Name'

# Функция для записи сообщения в Google Sheets
def write_to_google_sheet(login, text, time):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_SHEETS_CREDS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)
    sheet.append_row([login, text, time])

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    await message.answer("Привет! Отправь мне своё сообщение.")

# Обработчик всех текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def on_text_message(message: types.Message):
    try:
        login = f"@{message.from_user.username}"
        text = message.text
        time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        write_to_google_sheet(login, text, time)
        await message.answer("Сообщение успешно записано в Google документ.")
    except Exception as e:
        error_message = f"Ошибка: {type(e).__name__} - {str(e)}"
        with open("error_log.txt", "a") as file:
            file.write(f"{datetime.datetime.now()} - {error_message}\n")
        await message.answer("Произошла ошибка при записи сообщения. Пожалуйста, попробуйте позже.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
