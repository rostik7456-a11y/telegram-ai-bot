import telebot
import requests
import os
import json
import time

# ===== ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ =====
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GATEWAY_URL = os.environ.get("GATEWAY_URL", "https://ai-gateway.onrender.com/v1/chat/completions")

bot = telebot.TeleBot(TOKEN)

# ===== КОМАНДА /start =====
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "🤖 *Привет! Я твой личный ИИ-помощник!*\n\n"
        "Я работаю через AI Gateway, который объединяет 5+ бесплатных ИИ-провайдеров.\n"
        "Просто напиши мне что угодно — я отвечу на любой вопрос.\n\n"
        "📌 *Команды:*\n"
        "/start — показать это сообщение\n"
        "/help — помощь\n"
        "/info — информация о боте\n"
        "/status — статус шлюза",
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
        "🧠 *Модели:* Llama 3.3 70B, Qwen, Gemma и другие\n"
        "🔗 *Шлюз:* AI Gateway (5+ провайдеров)\n"
        "👨‍💻 *Создатель:* твой братан\n"
        "🌐 *Хостинг:* Render.com\n"
        "💬 *Особенности:* автоматическое переключение при ошибках, 100+ запросов в минуту",
        parse_mode="Markdown"
    )

# ===== КОМАНДА /status =====
@bot.message_handler(commands=['status'])
def send_status(message):
    try:
        response = requests.get(
            GATEWAY_URL.replace("/v1/chat/completions", "/health"),
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            status_text = "🟢 *Статус шлюза:* Работает\n\n"
            status_text += "📊 *Провайдеры:*\n"
            for name, available in data.get("providers", {}).items():
                status_text += f"  {'✅' if available else '❌'} {name}\n"
            bot.reply_to(message, status_text, parse_mode="Markdown")
        else:
            bot.reply_to(message, "🔴 Шлюз недоступен. Проверь настройки.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка при проверке статуса: {e}")

# ===== ОБРАБОТЧИК ЛЮБОГО ТЕКСТА =====
@bot.message_handler(func=lambda m: True)
def reply_to_message(message):
    try:
        # Отправляем запрос к шлюзу
        response = requests.post(
            GATEWAY_URL,
            headers={"Content-Type": "application/json"},
            json={
                "messages": [{"role": "user", "content": message.text}]
            },
            timeout=60
        )
        
        # Проверяем статус
        if response.status_code != 200:
            error_text = f"❌ Шлюз вернул ошибку {response.status_code}\n\n{response.text[:300]}"
            bot.reply_to(message, error_text)
            return
        
        # Парсим ответ
        data = response.json()
        
        if "choices" not in data:
            bot.reply_to(message, f"❌ Странный ответ от шлюза:\n{json.dumps(data, indent=2)[:500]}")
            return
        
        # Отправляем ответ
        bot.reply_to(message, data["choices"][0]["message"]["content"][:4000])
        
    except requests.exceptions.Timeout:
        bot.reply_to(message, "⏰ Превышено время ожидания. Попробуй ещё раз.")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {str(e)}")

# ===== ЗАПУСК =====
print("✅ Бот запущен с AI Gateway!")
print(f"🔗 Шлюз: {GATEWAY_URL}")
bot.infinity_polling()
