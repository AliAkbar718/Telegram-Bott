from telebot import types
from googletrans import Translator

translator = Translator()
user_translation_mode = {}

def register_translation_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == 'ترجمه متن 🔤')
    def ask_for_translation(message):
        user_translation_mode[message.from_user.id] = True
        bot.send_message(message.chat.id, "📝 لطفاً متنی که می‌خوای ترجمه کنم رو بفرست.")

    @bot.message_handler(func=lambda m: True)
    def handle_translation(message):
        user_id = message.from_user.id
        if user_translation_mode.get(user_id):
            text = message.text
            lang = 'fa' if is_english(text) else 'en'
            try:
                result = translator.translate(text, dest=lang)
                bot.send_message(message.chat.id, f"✅ ترجمه:\n\n{result.origin} → {result.text}")
            except Exception as e:
                bot.send_message(message.chat.id, "❌ خطا در ترجمه. لطفاً دوباره امتحان کن.")
            finally:
                user_translation_mode[user_id] = False  # خاموش کردن حالت ترجمه

def is_english(text):
    return all(ord(c) < 128 for c in text)