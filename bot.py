import telebot
import requests
import os
import json

TOKEN = os.environ.get("TELEGRAM_TOKEN")
VENICE_KEY = os.environ.get("VENICE_API_KEY")

bot = telebot.TeleBot(TOKEN)

# ===== КОМАНДА /start =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "🤖 *Привет! Я твой личный ИИ-помощник на базе Venice.ai!*\n\n"
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
        "🧠 *Модель:* Llama 3.3 70B (Venice.ai)\n"
        "👨‍💻 *Создатель:* твой братан\n"
        "🌐 *Хостинг:* Render.com\n"
        "💬 *Особенности:* отвечает на любые вопросы, 60 запросов в минуту, бесплатно!",
        parse_mode="Markdown"
    )

# ===== ОБРАБОТЧИК ЛЮБОГО ТЕКСТА (С ОТЛАДКОЙ!) =====
@bot.message_handler(func=lambda m: True)
def reply_to_message(message):
    try:
        # Отправляем запрос в Venice API
        response = requests.post(
            "https://api.venice.ai/api/v1/chat/completions",
            headers={
                "X-Venice-API-Key": VENICE_KEY,
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-instruct",
                "messages": [{"role": "user", "content": message.text}]
            },
            timeout=30
        )
        
        # Проверяем статус HTTP
        if response.status_code != 200:
            error_text = f"❌ HTTP {response.status_code}\n\n{response.text[:500]}"
            bot.reply_to(message, error_text)
            return
        
        # Парсим JSON
        data = response.json()
        
        # Проверяем, есть ли поле choices
        if "choices" not in data:
            debug_info = f"🔍 Странный ответ от Venice:\n\n```json\n{json.dumps(data, indent=2)[:1000]}\n```"
            bot.reply_to(message, debug_info, parse_mode="Markdown")
            return
        
        # Всё хорошо — отправляем ответ
        bot.reply_to(message, data["choices"][0]["message"]["content"][:4000])
        
    except requests.exceptions.Timeout:
        bot.reply_to(message, "⏰ Превышено время ожидания от Venice API. Попробуй ещё раз.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

# ===== ЗАПУСК =====
print("✅ Бот запущен на Venice.ai с отладкой!")
print(f"🔑 Ключ Venice: {VENICE_KEY[:20]}... (скрыто)")
bot.infinity_polling()
