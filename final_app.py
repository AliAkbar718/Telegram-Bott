import telebot
from pyexpat.errors import messages
from telebot import types
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReactionTypeEmoji)
import time
import datetime
import platform
from datetime import datetime
import jdatetime
import os
from flask import Flask, request
import random
import pytz


TOKEN = '7579645804:AAHt5O6hHdXtdigsQQ-WMGiIm7cJexySTVc'
CHANNEL_USERNAME = '@rap_family1' 
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

WEBHOOK_URL = 'https://telegram-bott-xuhm.onrender.com/webhook'
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

WEBHOOK_SECRET_PATH = '/webhook'  
 

user_warnings = {}

# -------------------- توابع کمکی --------------------

def contains_link(text):
    if not text:
        return False
    return any(word in text.lower() for word in ['http', 'https', 't.me', '@'])

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# -------------------- /start --------------------

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('لیست')
    if is_user_member(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "سلام من علی بات🤖 هستم!\n\nبرای مشاهده قابلیت‌هام روی دکمه «لیست» بزن یا تایپ کن",
            reply_markup=markup
        )
    else:
        join_btn = types.InlineKeyboardMarkup()
        join_btn.add(types.InlineKeyboardButton("عضویت در کانال✅", url="https://t.me/rap_family1"))
        bot.send_message(
            message.chat.id,
            "توی کانال عضو نیستی ❌\n\nبرای استفاده از ربات اول عضو شو.",
            reply_markup=join_btn
        )
        bot.send_message(message.chat.id, "وقتی عضو شدی، روی «لیست» بزن.", reply_markup=markup)

# -------------------- پیام‌های عمومی --------------------

@bot.message_handler(content_types=['text'])
def handle_all_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.lower().strip()
    first_name = message.from_user.first_name

    # جلوگيری از درگیری با دستورات مدیریتی
    if text in ['پین', 'حذف پین', 'بن', 'حذف بن', 'سکوت', 'حذف سکوت', 'افزودن ادمین', 'حذف ادمین']:
        return

    # حذف لینک با اخطار
    if contains_link(text):
        if not is_admin(chat_id, user_id):
            try:
                bot.delete_message(chat_id, message.message_id)
                user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
                if user_warnings[user_id] == 1:
                    bot.send_message(chat_id, f"⚠️ {first_name} - ارسال لینک 1 از 2 (تکرار = حذف)")
                elif user_warnings[user_id] >= 2:
                    bot.send_message(chat_id, f"⛔️ {first_name} حذف شد (ارسال لینک 2 از 2)")
                    bot.ban_chat_member(chat_id, user_id)
            except:
                pass
        return

    # پاسخ به لیست
    if text == 'لیست':
        if is_user_member(user_id):
            bot.send_message(chat_id,
                '-<code> مدیریت گروه🤵‍♂️</code>\n\n'
                '-<code> بیوگرافی🗨️</code>\n\n'
                '-<code> اصطلاحات انگلیسی🔠</code>\n\n'
                '-<code> جرعت حقیقت❓</code>\n\n'
                '-<code> جوک😄</code>\n\n'
                '-<code> فونت اسم♍</code>\n\n'
                '-<code> زبان هخامنشی𐎠</code>\n\n'
                '-<code> دانستنی⁉️</code>\n\n'
                '-<code> ارتباط با ما📞</code>\n\n'
                '<b>برای کپی، روی متن‌ها بزن</b>', parse_mode="HTML")
        else:
            join_btn = types.InlineKeyboardMarkup()
            join_btn.add(types.InlineKeyboardButton("عضویت در کانال✅", url="https://t.me/rap_family1"))
            bot.send_message(chat_id, "عضو کانال نیستی. اول عضو شو:", reply_markup=join_btn)

# -------------------- قابلیت‌های مدیریتی --------------------

# پین پیام
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('پین'))
def pin(m):
    print("دستور پین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.id)
            bot.reply_to(m, "پیام پین شد.")
        else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")
    else:
        bot.reply_to(m, "فقط ادمین‌ها می‌تونن پین کنن.")

# حذف پین
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('حذف پین'))
def unpin(m):
    print("دستور حذف پین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        bot.unpin_chat_message(m.chat.id)
        bot.reply_to(m, "پین پیام حذف شد.")

# بن کاربر
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('بن'))
def ban(m):
    print("دستور بن اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.reply_to(m, f"کاربر {m.reply_to_message.from_user.first_name} بن شد.")
        else:
            bot.reply_to(m, "روی پیام کاربر ریپلای کن.")

# حذف بن
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('حذف بن'))
def unban(m):
    print("دستور حذف بن اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.reply_to(m, "کاربر از بن خارج شد.")

# سکوت
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('سکوت'))
def restrict(m):
    print("دستور سکوت اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.restrict_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                permissions=types.ChatPermissions(can_send_messages=False)
            )
            bot.reply_to(m, "کاربر سکوت شد.")

# حذف سکوت
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('حذف سکوت'))
def unrestrict(m):
    print("دستور حذف سکوت اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.restrict_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                permissions=types.ChatPermissions(can_send_messages=True)
            )
            bot.reply_to(m, "سکوت کاربر برداشته شد.")

# افزودن ادمین
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('افزودن ادمین'))
def promote(m):
    print("دستور افزودن ادمین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.promote_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                can_manage_chat=True,
                can_delete_messages=True,
                can_invite_users=True,
                can_pin_messages=True,
                can_promote_members=True
            )
            bot.reply_to(m, "کاربر به ادمین ارتقا یافت.")

# حذف ادمین
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('حذف ادمین'))
def demote(m):
    print("دستور حذف ادمین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.promote_chat_member(
                m.chat.id,
                m.reply_to_message.from_user.id,
                can_manage_chat=False,
                can_delete_messages=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False
            )
            bot.reply_to(m, "ادمین حذف شد.")


@app.route(WEBHOOK_SECRET_PATH, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/', methods=['GET'])
def index():
    return 'ربات فعال است', 200
   



        
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render به PORT مقدار می‌ده
    app.run(host='0.0.0.0', port=port)

