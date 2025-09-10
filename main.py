import os
import random
import json
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# -----------------------------
# Переменные окружения
# -----------------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -----------------------------
# Инициализация бота
# -----------------------------
bot = Bot(token=BOT_TOKEN or "DUMMY", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())

# -----------------------------
# Загружаем промты
# -----------------------------
PROMPTS = []
try:
    with open("data/prompts.json", "r", encoding="utf-8") as f:
        PROMPTS = json.load(f)
except Exception as e:
    print("Не удалось загрузить промты:", e)

# -----------------------------
# Функция общения с GPT
# -----------------------------
def ai_reply(user_message):
    if not OPENAI_API_KEY:
        return "Бот пока не настроен, админ должен добавить ключи 🛠"
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты дружелюбный Telegram-бот, используй эмодзи и юмор."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print("Ошибка GPT:", e)
        return "Ой, что-то пошло не так 😅 Попробуй ещё раз!"

# -----------------------------
# Клавиатура
# -----------------------------
def main_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🎨 Новый промт", callback_data="new_prompt"))
    keyboard.add(InlineKeyboardButton("💬 Поговорить с ботом", callback_data="chat_mode"))
    return keyboard

# -----------------------------
# Стартовый хендлер
# -----------------------------
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    if not BOT_TOKEN or not OPENAI_API_KEY:
        await message.answer(
            "Привет! 🚨 Бот пока не настроен. Админ должен добавить ключи в Variables проекта."
        )
        return

    text = (
        f"Йоу, {message.from_user.first_name} 👋\n\n"
        "Я твой карманный <b>PromptPilot</b> ✈️\n"
        "Я могу дать тебе свежие промты для генерации и поболтать 😎\n\n"
        "Выбирай, что хочешь сделать ниже 👇"
    )
    await message.answer(text, reply_markup=main_keyboard())

# -----------------------------
# Обработка кнопок
# -----------------------------
@dp.callback_query_handler(lambda c: True)
async def process_callback(callback_query: types.CallbackQuery):
    if not BOT_TOKEN or not OPENAI_API_KEY:
        await bot.send_message(callback_query.from_user.id, "Бот пока не настроен 🚨")
        return

    if callback_query.data == "new_prompt":
        if PROMPTS:
            prompt = random.choice(PROMPTS)
        else:
            prompt = "Список промтов пуст 😅"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("🎨 Ещё промт", callback_data="new_prompt"))
        await bot.send_message(callback_query.from_user.id, f"🎯 Вот твой промт:\n\n<code>{prompt}</code>", reply_markup=keyboard)
    elif callback_query.data == "chat_mode":
        await bot.send_message(callback_query.from_user.id, "Окей, давай потрещим 🤟 Пиши что угодно!")

# -----------------------------
# Чат с GPT
# -----------------------------
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
