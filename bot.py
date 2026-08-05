import telebot
import google.generativeai as genai
import os

# ===== БЕРЕМ КЛЮЧИ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not TOKEN or not GEMINI_KEY:
    raise Exception("❌ Не найдены переменные окружения! Настрой TELEGRAM_TOKEN и GEMINI_API_KEY на Render.")

# ===== НАСТРОЙКА GEMINI =====
genai.configure(api_key=GEMINI_KEY)

# 🔥 ВОТ ТУТ ВЫБИРАЕМ МОДЕЛЬ (работает 100%)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

# ===== СОЗДАЕМ БОТА =====
bot = telebot.TeleBot(TOKEN)

# ===== КОМАНДА /start =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "🤖 *Привет! Я твой личный ИИ-помощник на базе Gemini 2.0 Flash!*\n\n"
        "Просто напиши мне что угодно — я отвечу на любой вопрос.\n\n"
        "📌 *Команды:*\n"
        "/start — показать это сообщение\n"
        "/help — помощь\n"
        "/info — информация о боте",
        parse_mode="Markdown"
    )

# ===== КОМАНДА /help =====
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message,
        "🆘 *Помощь*\n\n"
        "Я отвечаю на любые вопросы, пиши как другу.\n"
        "Могу помочь с учебой, работой, идеями или просто поболтать.\n\n"
        "⚡ *Совет:* Чем точнее вопрос — тем лучше ответ.",
        parse_mode="Markdown"
    )

# ===== КОМАНДА /info =====
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(
        message,
        "ℹ️ *Информация о боте*\n\n"
        "🧠 *Модель:* Gemini 2.0 Flash (самая быстрая)\n"
        "👨‍💻 *Создатель:* твой братан\n"
        "🌐 *Хостинг:* Render.com\n"
        "💬 *Особенности:* отвечает на любые вопросы, помнит диалог в рамках одного сообщения",
        parse_mode="Markdown"
    )

# ===== ОБРАБОТЧИК ЛЮБОГО ТЕКСТА =====
@bot.message_handler(func=lambda m: True)
def reply_to_message(message):
    try:
        # Отправляем запрос в Gemini
        response = model.generate_content(message.text)
        # Отвечаем пользователю (обрезаем до 4000 символов)
        bot.reply_to(message, response.text[:4000])
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}\n\nПопробуй позже или напиши /help")

# ===== ЗАПУСК =====
print("✅ Бот запущен и готов к работе!")
print("🚀 Иди в Телеграм и напиши /start")
bot.infinity_polling()
