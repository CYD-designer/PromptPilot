import os
import random
import json
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# -----------------------------
# Загружаем переменные окружения
# -----------------------------
load_dotenv()  # читаем .env

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Ошибка: проверь BOT_TOKEN и OPENAI_API_KEY в переменных окружения")

openai.api_key = OPENAI_API_KEY

# -----------------------------
# Инициализация бота
# -----------------------------
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# -----------------------------
# Загружаем промты
# -----------------------------
with open("data/prompts.json", "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)

# -----------------------------
# Функция общения с GPT
# -----------------------------
def ai_reply(user_message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный Telegram-бот по имени PromptPilot. Общайся как живой человек, используй юмор, смайлы и немного зумерский стиль."},
                {"role": "user", "content": user_message}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Ошибка GPT:", e)
        return "Ой, что-то пошло не так 😅 Попробуй ещё раз!"

# -----------------------------
# Хендлеры
# -----------------------------
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    text = (
        f"Йоу, {message.from_user.first_name} 👋\n\n"
        "Я твой карманный <b>PromptPilot</b> ✈️\n"
        "Давай бахнем тебе свежий промт для генерации? 🔥\n\n"
        "Команды:\n"
        "👉 /prompt — случайный промт\n"
        "👉 /chat — поболтать со мной\n"
        "👉 /help — помощь"
    )
    await message.answer(text)

@dp.message_handler(commands=["prompt"])
async def get_prompt(message: types.Message):
    prompt = random.choice(PROMPTS)
    await message.answer(f"🎨 Вот тебе промт:\n\n<code>{prompt}</code>")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.answer(
        "📖 Доступные команды:\n"
        "/prompt — получить промт\n"
        "/chat — поболтать со мной\n"
        "/help — помощь"
    )

# Чат с GPT
@dp.message_handler(commands=["chat"])
async def chat_mode(message: types.Message):
    await message.answer("Окей, бро, давай потрещим 🤟 Пиши что угодно!")

@dp.message_handler(lambda msg: True)
async def casual_chat(message: types.Message):
    if not message.text.startswith("/"):
        reply = ai_reply(message.text)
        await message.answer(reply)

# -----------------------------
# Запуск бота
# -----------------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
