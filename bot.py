import telebot
import google.generativeai as genai
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not TOKEN or not GEMINI_KEY:
    raise Exception("Не найдены переменные окружения! Настрой TELEGRAM_TOKEN и GEMINI_API_KEY на Render.")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-lite")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def reply(m):
    try:
        r = model.generate_content(m.text)
        bot.reply_to(m, r.text[:4000])
    except Exception as e:
        bot.reply_to(m, f"Ошибка: {e}")

print("Бот запущен!")
bot.infinity_polling()
