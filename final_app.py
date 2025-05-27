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

@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('پین'))
def pin(m):
    print("دستور پین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.id)
            bot.reply_to(m, "پیام پین شد.")
        else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن")
    else:
        bot.reply_to(m, "فقط ادمین‌ها می‌تونن پین کنن")

# حذف پین
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('حذف پین'))
def unpin(m):
    print("دستور حذف پین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        bot.unpin_chat_message(m.chat.id)
        bot.reply_to(m, "پین پیام حذف شد.")
    else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")
  

# بن کاربر
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('بن'))
def ban(m):
    print("دستور بن اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.reply_to(m, f"کاربر {m.reply_to_message.from_user.first_name} بن شد")
        else:
            bot.reply_to(m, "روی پیام کاربر ریپلای کن")

# حذف بن
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('حذف بن'))
def unban(m):
    print("دستور حذف بن اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.reply_to(m, "کاربر از بن خارج شد")
        else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")

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
        else:
           bot.reply_to(m, "روی پیام کاربر ریپلای کن")
   

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
            bot.reply_to(m, "سکوت کاربر برداشته شد")
        else:
            bot.reply_to(m, "روی پیام کاربر ریپلای کن")


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
            bot.reply_to(m, "کاربر به ادمین ارتقا یافت")
        else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")

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
            bot.reply_to(m, "ادمین برکنار شد")
        else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")
            
            

        
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

    if text == 'شروع':
        bot.reply_to(message, 'سلام من علی بات🤖 هستم\n\nبرای اطلاع از قابلیت‌هام، بنویس «لیست»', parse_mode="HTML")
    
    elif text == 'مدیریت گروه🤵‍♂️':
        bot.reply_to(message, 'برای استفاده از امکانات مدیریتی، ربات را به گروه اضافه و ادمین کنید.')

    elif text == 'ارتباط با ما📞':
        bot.reply_to(message, 'آیدی سازنده ربات: @AliamA7931')
        
    elif text == 'جرعت حقیقت❓':
         bot.send_message(chat_id,           
            '1. اگر زندگی ات یک فیلم بود کدام فیلم می شد؟\n\n 2. آیا آلرژی خاصی داری؟\n\n 3. اگر میتوانستی به یک زمان خاص در تاریخ برگردی کدام زمان بود؟\n\n 4. اگر ابر قدرت بودی چه قدرتی داشتی؟\n\n 5. وقتی آلارم گوشیت زنگ میزند بلافاصله بیدار میشوید یا دکمه بعدا را فشار میدهد؟\n\n 6. اولین کاری که هر روز صبح انجام میدی چیه؟\n\n 7. آخرین کاری که هر شب انجام میدی چیه؟\n\n 8. آخرین باری که گریه کردی کی بوده و چرا؟\n\n 9. عجیب ترین کاری که در تنهایی هایت انجام دادی چه بوده؟\n\n 10. بدترین بحثی که در آن شرکت کرده ای چه بوده؟\n\n 11. مسخره ترین لباسی که تابحال پوشیده ای چه بوده؟\n\n 12. اگر می توانستی یک چیز را در خودت تغییر دهی چه چیزی را تغییر می دادی؟\n\n 13. بزرگ ترین رازت چیه؟\n\n 14. چه چیزی باعث خجالتت میشه؟\n\n 15. خجالت آورترین اتفاقی که تاحالا برات افتاده؟\n\n 16. بزرگترین اشتباهی که تاحالا مرتکب شدی؟\n\n 17. توی چه کاری اصلا خوب نیستی؟\n\n 18. بزرگ ترین دروغی که تا حالا گفتی؟\n\n 19. تا حالا توی بازی تقلب کردی؟\n\n 20. عجیب ترین عادتی که داری؟\n\n 21. عجیب ترین غذایی که عاشقشی؟\n\n 22. بزرگ ترین ترس دوران بچگیت؟\n\n 23. پایین ترین نمره ای که توی دانشگاه یا مدرسه گرفتی؟\n\n 24. تا حالا یه چیز گرون قیمت رو شکستی؟\n\n 25. اگه یه دفعه صد میلیون تومن به دست بیاری، چطوری خرجش می کنی؟\n\n 26. بدترین غذایی که تا حالا امتحان کردی؟\n\n 27. خجالت آورترین چیزی که تا حالا توی فضای مجازی پست کردی؟\n\n 28. تا حالا راز دوستت رو به کسی گفتی؟\n\n 29. دوست داری در آینده چندتا بچه داشته باشی؟\n\n 30. اگه قرار باشه تا آخر عمرت فقط یه غذا رو بخوری، چه غذاییه؟\n\n 31. آخرین پیامی که برای دوست صمیمیت ارسال کردی؟\n\n 32. بدترین درد فیزیکی که تا حالا داشتی؟\n\n 33. از لحاظ شخصیتی، بیشتر شبیه مامانتی یا بابات؟\n\n 34. آخرین باری که از کسی عذرخواهی کردی کی بود؟ بابت چه کاری؟\n\n 35. اگه خونت آتش بگیره و فقط بتونی 3 تا چیزو برداری (به غیر از افراد)، چه چیزهایی رو بر می داری؟\n\n 36. توی بچگیات دوست داشتی چه سرگرمی یا ورزشی رو تجربه کنی؟\n\n 37. عجیب ترین کاری که تا حالا توی مکان عمومی انجام دادی؟\n\n 38. آخرین بهانه ای که برای کنسل کردن برنامه هات آوردی؟\n\n 39. بدترین اشتباهی که توی مدرسه یا سر کارت انجام دادی؟\n\n 40. کدوم یکی از اعضای خانوادت خیلی رو اعصابته؟')
         bot.reply_to(message, 'لیست جرعت حقیقت ارسال شد')                                   

    elif text == 'ربات':
        username = message.from_user.username or first_name
        bot.send_message(chat_id, f'جانم @{username}،        چه کمکی ازم بر میاد ؟ ' , parse_mode="HTML")

    elif text in ['سلام خوبی', 'خوبی', 'خوب هستی', 'چطوری']:
        bot.reply_to(message, 'سلام خوبم حال خودت خوبه؟')
        
    elif text == 'سلام':
        bot.reply_to(message, 'سلام خوبی عزیز')    

    elif text == 'چه خبرا':
        bot.reply_to(message, 'خبر سلامتیت، خودت چه خبر؟')

    elif text in ['فدات', 'فدابشم']:
        bot.reply_to(message, 'قربونت عزیز')

    elif text in ['خداحافظ', 'بای']:
        bot.reply_to(message, 'خدانگهدار')

    elif text in ['کجایی', 'اهل کجایی']:
        bot.reply_to(message, 'من از سیاره ربات‌ها اومدم!')

    elif text == 'اسمت چیه':
        bot.reply_to(message, 'اسمم علی بات🤖 هست')

    elif text == 'درود':
        bot.reply_to(message, 'درود بر تو گل🌹')

    elif text in ['سلام خاری', 'خاری']:
        bot.reply_to(message, 'خارمه ته خاری')

    elif text == 'چه خبر':
        bot.reply_to(message, 'سلامتی ته چه خبر')

    elif text == 'منم سلامتی خبری نیه':
        bot.reply_to(message, ' آها همیشه سلامت بوشی')

    elif text == 'گم بواش':
        bot.reply_to(message, 'گم نوومبه شه سره راه ره بلدمه')

    elif text == 'گیخار':
        bot.reply_to(message, 'برو مه گی ره بخار')

    elif text in ['چیکار کندی', 'چیکار کاندی']:
        bot.reply_to(message, 'چیکار خاستی هاکانم درمه ته جه گپ زمبه😑')

    elif text == 'کجه دری':
        bot.reply_to(message, 'تلگرام دله درمه دیگه اینتا هم بییه سوال🙄')

    elif text in ['ته اسم چیه', 'ته اسم چیچیه']:
        bot.reply_to(message, 'من علی بات🤖هستمه شما مه ره نشناسنی😁')

    elif text == 'ربات ته ره دوست دارمه':
        bot.reply_to(message, 'منم ته ره خله دوست دارمه ولی از یه نظر دیگه🙂😊')

    elif text == 'ربات مه جه رل زندی':
        bot.reply_to(message, 'اره ته فدابووشم ناز ره بخارم😁')

    elif text == 'من بورم':
        bot.reply_to(message, 'به سلامت شه هوا ره دار')

    elif text == 'بات':
        bot.send_message(chat_id, f'جان @{message.from_user.username} مه ره کار داشتی؟\n\n🔸 برای گپ بزوعن با من کلمه <b> «گپ» </b> ره راهی هاکان', parse_mode="HTML")

    elif text == 'گپ':
        bot.reply_to(message, 'سلام من علی بات🤖 هستمه\n\n برای اطلاع داشتن از مه قابلیت کلمه <b> «لیست» </b> ره راهی هاکان', parse_mode="HTML")

    elif text == 'کیر':
        bot.set_message_reaction(chat_id=chat_id, message_id=message.message_id, reaction=[types.ReactionTypeEmoji(emoji='🖕')])


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

weekday_names = {
    'Saturday': 'شنبه',
    'Sunday': 'یک‌شنبه',
    'Monday': 'دوشنبه',
    'Tuesday': 'سه‌شنبه',
    'Wednesday': 'چهارشنبه',
    'Thursday': 'پنج‌شنبه',
    'Friday': 'جمعه'
}

month_names = {
    'Farvardin': 'فروردین',
    'Ordibehesht': 'اردیبهشت',
    'Khordad': 'خرداد',
    'Tir': 'تیر',
    'Mordad': 'مرداد',
    'Shahrivar': 'شهریور',
    'Mehr': 'مهر',
    'Aban': 'آبان',
    'Azar': 'آذر',
    'Dey': 'دی',
    'Bahman': 'بهمن',
    'Esfand': 'اسفند'
}

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_user(message):
    for new_member in message.new_chat_members:
        iran_time = datetime.now(pytz.timezone('Asia/Tehran'))
        shamsi_time = jdatetime.datetime.fromgregorian(datetime=iran_time)

        weekday_en = shamsi_time.strftime('%A')     # مثلاً Saturday
        month_en = shamsi_time.strftime('%B')       # مثلاً Farvardin

        weekday_fa = weekday_names.get(weekday_en, weekday_en)
        month_fa = month_names.get(month_en, month_en)

        date_str = f"{shamsi_time.day} {month_fa} {shamsi_time.year}"
        time_str = shamsi_time.strftime('%H:%M:%S')
        response = f' {weekday_fa} {date_str} \n\nزمان: {time_str}  '
        bot.send_message(message.chat.id, f'درود به گپمون خوش اومدی✨❤️{message.from_user.first_name}\n\nامروز{response}')


@bot.message_handler(content_types=['left_chat_member'])
def handle_left_member(message):
    bot.reply_to(message, "به سلامت👋")



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

