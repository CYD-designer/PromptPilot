import os
import random
import json
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# -----------------------------
# Настройки
# -----------------------------
# Используй прямой ключ для теста или через .env:
openai.api_key = "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"

BOT_TOKEN = "твой_бот_токен_из_BotFather"

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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты дружелюбный Telegram-бот по имени PromptPilot. Общайся как живой человек, используй юмор, смайлы и немного зумерский стиль."},
            {"role": "user", "content": user_message}
        ]
    )
    return response["choices"][0]["message"]["content"]

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


# Чат с ботом
@dp.message_handler(commands=["chat"])
async def chat_mode(message: types.Message):
    await message.answer("Окей, бро, давай потрещим 🤟 Пиши что угодно!")


@dp.message_handler(lambda msg: True)
async def casual_chat(message: types.Message):
    if not message.text.startswith("/"):
        try:
            reply = ai_reply(message.text)
            await message.answer(reply)
        except Exception as e:
            # На случай ошибок OpenAI API
            await message.answer("Ой, что-то пошло не так 😅 Попробуй ещё раз!")
            print("Error GPT:", e)


# -----------------------------
# Запуск бота
# -----------------------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
