import os
import random
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Загружаем токен
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# Загружаем промты
with open("data/prompts.json", "r", encoding="utf-8") as f:
    PROMPTS = json.load(f)

# --- Хендлеры ---

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
    await message.answer("📖 Доступные команды:\n"
                         "/prompt — получить промт\n"
                         "/chat — поболтать со мной\n"
                         "/help — помощь")


# Простейший чат-бот (дружелюбный стиль)
@dp.message_handler(commands=["chat"])
async def chat_mode(message: types.Message):
    await message.answer("Окей, давай поболтаем 🤟 Напиши что угодно!")

@dp.message_handler(lambda msg: True)
async def casual_chat(message: types.Message):
    responses = [
        "Четко 🔥 А чем занимаешься?",
        "Понимаю тебя, бро 😎",
        "Хаха, это топчик 😂",
        "Слушай, а не хочешь промтик словить? Напиши /prompt 😉",
        "Бро, звучит как вайб ✨"
    ]
    if not message.text.startswith("/"):
        await message.answer(random.choice(responses))


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
