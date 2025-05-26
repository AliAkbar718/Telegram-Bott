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
CHANNEL_ID =  -1002317714854

bot = telebot.TeleBot(TOKEN)

WEBHOOK_URL = 'https://telegram-bott-xuhm.onrender.com/webhook'
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

app = Flask(__name__)

WEBHOOK_SECRET_PATH = '/webhook'  



# بررسی عضویت
def is_user_member(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# استارت
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('لیست')
    if is_user_member(user_id):
        bot.send_message(user_id, "سلام من علی بات🤖 هستم!\n\nبرای مشاهده قابلیت‌هام روی دکمه «لیست» بزن یا تایپ کن", reply_markup=markup)
    else:
        join_btn = types.InlineKeyboardMarkup()
        join_btn.add(types.InlineKeyboardButton("عضویت در کانال✅", url="https://t.me/rap_family1"))  # لینک کانالتو بذار
        bot.send_message(user_id, "توی کانال عضو نیستی ❌\n\n برای استفاده از قابلیت ربات باید عضو کانال بشی\n\n ", reply_markup=join_btn)
        bot.send_message(user_id, "وقتی عضو شدی روی دکمه «لیست» بزن:", reply_markup=markup)

# لیست
@bot.message_handler(func=lambda msg: msg.text == 'لیست')
def send_features(message):
    user_id = message.from_user.id
    if is_user_member(user_id):
        bot.send_message(user_id, '-<code> مدیریت گروه🤵‍♂️</code>\n\n-<code> بیوگرافی🗨️</code>\n\n-<code> اصطلاحات انگلیسی🔠</code>\n\n-<code> جرعت حقیقت❓</code>\n\n-<code> جوک😄</code>\n\n-<code> فونت اسم♍</code>\n\n-<code> زبان هخامنشی𐎠</code>\n\n-<code> دانستنی⁉️</code>\n\n-<code> ارتباط با ما📞</code>\n\n<b>متن ها به صورت مونو هستند روی متن بزنید کپی میشوند</b>', parse_mode="HTML")
    else:
        join_btn = types.InlineKeyboardMarkup()
        join_btn.add(types.InlineKeyboardButton("عضویت در کانال✅", url="https://t.me/rap_family1"))
        bot.send_message(user_id, "هنوز عضو کانال نیستی❌\n\nبرای استفاده از ربات ابتدا عضو شو.", reply_markup=join_btn)



@app.route(WEBHOOK_SECRET_PATH, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return 'ok', 200

@app.route('/', methods=['GET'])
def index():
    return 'ربات فعال است', 200
   


reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
reply_keyboard.add('ارتباط با ما📞 ', 'مدیریت گروه🤵‍♂️', 'بیوگرافی🗨️', 'اصطلاحات انگلیسی🔠', 'جوک😄', 'زبان هخامنشی𐎠', 'فونت اسم♍', 'جرعت حقیقت❔', 'دانستنی⁉️')


# حروف فارسی به حروف میخی
farsi_to_cuneiform = {
    'ا': '𐎠', 'آ': '𐎠', 'ب': '𐎲', 'پ': '𐎱', 'ت': '𐎫', 'ث': '𐎰', 'تو': '𐎬', 'طو': '𐎬', 'ج': '𐎢', 'جی': '𐎪', 'چ': '𐎨', 'ح': '𐏃', 'خ': '𐎧',
    'د': '𐎭', 'دی': '𐎮', 'دو': '𐎯', 'ذ': '𐏀', 'ر': '𐎼', 'رو': '𐎽', 'ز': '𐏀', 'س': '𐎿', 'ش': '𐎤', 'ص': '𐎿', 'ض': '𐏀', 'ط': '𐎫', 'ظ': '𐏀', 'ع': '𐎠', 'غ': '𐎥', 'ک': '𐎣',
    'کو': '𐎤', 'قو': '𐎦', 'گ': '𐎥', 'م': '𐎶', 'مو': '𐎸', 'می': '𐎷', 'ن': '𐎴', 'نو': '𐎵', 'و': '𐎺', 'وی': '𐎻', 'ه': '𐎱', 'ی': '𐎡',
    'ف': '𐎳', 'ق': '𐎨', 'ل': '𐎾'
}

# تابع تبدیل
def convert_to_cuneiform(text):
    return ''.join(farsi_to_cuneiform.get(ch, ch) for ch in text)

# شروع
@bot.message_handler(func= lambda m: m.text == 'زبان هخامنشی𐎠')
def hakhmaneshi(message):
    bot.send_message(message.chat.id, "یک متن فارسی بفرست تا برات به خط میخی هخامنشی تبدیل کنم")
    bot.register_next_step_handler(message, handle_text)
    
def handle_text(message):
    original = message.text
    converted = convert_to_cuneiform(original)
    bot.reply_to(message, f"متن میخی:\n{converted}")   
    bot.send_message(message.chat.id, 'برای اینکه متن جدیدی را وارد کنید\n\nمجددا کلمه <b>زبان هخامنشی𐎠</b>را ارسال کنید', parse_mode="HTML")

 
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    if message.audio:
        bot.reply_to(message, 'این یک فایل صوتی🎛️ هست')
    elif message.document:
        bot.reply_to(message, 'این یک سند📄 هست')  

@bot.message_handler(content_types=['photo'])    
def handle_photo(message):
    if message.photo:
        bot.reply_to(message, 'این یک تصویر🖼️ هست')
        
@bot.message_handler(content_types=['video'])    
def handle_photo(message):
    if message.video:
        bot.reply_to(message, 'این یک ویدیو📽️ هست')

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



def is_user_admin(chat_id, user_id):
    try:
        admins = bot.get_chat_administrators(chat_id)
        for admin in admins:
            if admin.user.id == user_id:
                return True
        return False
    except Exception as e:
        print(f"خطا در بررسی مدیر بودن: {e}")
        return False




# دیکشنری برای شمارش تخلف‌ها
user_warnings = {}

# تشخیص لینک در متن پیام
def contains_link(text):
    if not text:
        return False
    return any(word in text.lower() for word in ['http', 'https', 't.me', '@'])

# بررسی اینکه آیا کاربر ادمین هست یا نه
def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

@bot.message_handler(func=lambda m: True, content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if contains_link(message.text):
        if is_admin(chat_id, user_id):
            return

        try:
            # حذف پیام
            bot.delete_message(chat_id, message.message_id)

            # افزایش شمارش تخلف
            user_warnings[user_id] = user_warnings.get(user_id, 0) + 1
            warn_count = user_warnings[user_id]

            if warn_count == 1:
                bot.send_message(
                    chat_id,
                    f"⚠️ کاربر {first_name}\nارسال لینک 1 از 2\nلطفاً از ارسال لینک خودداری کنید. در صورت تکرار حذف خواهید شد."
                )
            elif warn_count >= 2:
                bot.send_message(
                    chat_id,
                    f"⛔️ کاربر {first_name}\nارسال لینک 2 از 2\nشما از گروه حذف شدید."
                )
                bot.ban_chat_member(chat_id, user_id)

        except Exception as e:
            print(f"خطا در هشدار یا حذف: {e}")


@bot.message_handler(content_types=['left_chat_member'])
def handle_left_member(message):
    bot.reply_to(message, "به سلامت👋")






@bot.message_handler(func=lambda m: m.text == 'پین')
def pin(m):
 chat_id = m.chat.id
 user_id = m.from_user.id
 
 if is_user_admin(chat_id, user_id):
     if m.reply_to_message:
         bot.pin_chat_message(m.chat.id, m.reply_to_message.id)
         bot.reply_to(m, "پیام مورد نظر پین شد")
     else:
        bot.reply_to(m, "برای پین کردن لطفا روی آن پیام ریپلای بزنین")
 else:
        bot.reply_to(m, 'فقط ادمین و مالک گروه میتونه پیامی رو پین کنه!')

 
@bot.message_handler(func=lambda m: m.text == 'حذف پین')
def unpin(m):
    bot.unpin_chat_message(m.chat.id, m.reply_to_message.id)
    bot.reply_to(m, 'پین پیام موردنظر حذف شد ')


@bot.message_handler(func=lambda m: m.text == 'افزودن ادمین')
def promote(m):
    bot.promote_chat_member(
        m.chat.id,
        m.reply_to_message.json['from']['id'],
        can_change_info=True,
        can_delete_messages=True,
        can_edit_messages=True,
        can_invite_users=True,
        can_manage_chat=True,
        can_manage_topics=False,
        can_manage_video_chats=True,
        can_manage_voice_chats=True,
        can_pin_messages=True,
        can_post_messages=True,
        can_promote_members=True,
        can_restrict_members=True,
    )
    bot.reply_to(m, 'ادمین جدید اضافه شد')


@bot.message_handler(func=lambda m: m.text == 'حذف ادمین')
def demote(m):
    bot.promote_chat_member(
        m.chat.id,
        m.reply_to_message.json['from']['id'],
        can_change_info=False,
        can_delete_messages=False,
        can_edit_messages=False,
        can_invite_users=False,
        can_manage_chat=False,
        can_manage_topics=False,
        can_manage_video_chats=False,
        can_manage_voice_chats=False,
        can_pin_messages=False,
        can_post_messages=False,
        can_promote_members=False,
        can_restrict_members=False,
    )
    bot.reply_to(m, 'ادمین از مقام برکنار شد ')


@bot.message_handler(func=lambda m: m.text == 'بن')
def ban(m):
 chat_id = m.chat.id
 user_id = m.from_user.id
 if is_user_admin(chat_id, user_id):
     if m.reply_to_message:
         bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
         bot.reply_to(m, f" کاربر {m.reply_to_message.from_user.first_name} بن شد ")
     else:
        bot.reply_to(m, "برای بن کردن کاربر لطفا روی پیام  ریپلای بزنین")
 else:
     bot.reply_to(m, 'فقط ادمین و مالک گروه میتونه کاربری رو بن کنه!')
    


@bot.message_handler(func=lambda m: m.text == 'حذف بن')
def unban(m):
    bot.unban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
    bot.reply_to(
        m, f" کاربر {m.reply_to_message.from_user.first_name} از لیست بن خارج شد ")


@bot.message_handler(func=lambda m: m.text == 'سکوت')
def restrict(m):
 chat_id = m.chat.id
 user_id = m.from_user.id
 if is_user_admin(chat_id, user_id):
     if m.reply_to_message:
        bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, can_add_web_page_previews=False, can_change_info=False, can_invite_users=False,
                             can_pin_messages=False, can_send_media_messages=False, can_send_messages=False, can_send_other_messages=False, can_send_polls=False)
        bot.reply_to(m, 'کاربر موردنظر سکوت شد')
     else:
        bot.reply_to(m, "برای سکوت کردن کاربر لطفا روی پیام آن ریپلای بزنین")
 else:
        bot.reply_to(m, 'فقط ادمین و مالک گروه میتونه کاربری رو سکوت کنه!')

@bot.message_handler(func=lambda m: m.text == 'حذف سکوت')
def derestrict(m):
    bot.restrict_chat_member(m.chat.id, m.reply_to_message.from_user.id, can_add_web_page_previews=True, can_change_info=True, can_invite_users=True,
                             can_pin_messages=True, can_send_media_messages=True, can_send_messages=True, can_send_other_messages=True, can_send_polls=True)
    bot.reply_to(m, 'سکوت کاربر موردنظر حذف شد')


@bot.message_handler(func=lambda m: m.text == 'فونت اسم♍')
def text_formatting(m):
    bot.send_message(m.chat.id, "اسم را وارد کنید")
    bot.register_next_step_handler(m, process_text)


def process_text(m):
    text = m.text
    text1 = f"<b>➷➷☠{text}☠➶➶</b>"
    text2 = f"<i>¯°•º¤ϟϞ҂ ♛{text}♛ ҂Ϟϟ¤º•°¯ </i>"
    text3 = f"<ins>ıllıllı ⦳⦳{text}⦳⦳ ıllıllı</ins>"
    text4 = f"<s>ஜ۩۞۩ஜ ♬{text}♬ ஜ۩۞۩ஜ</s>"
    text5 = f"<code>╔╝✞ ஜ☣{text}☣ஜ ✞╚╗</code>"
   

    bot.send_message(m.chat.id, text1, parse_mode="HTML")
    bot.send_message(m.chat.id, text2, parse_mode="HTML")
    bot.send_message(m.chat.id, text3, parse_mode="HTML")
    bot.send_message(m.chat.id, text4, parse_mode="HTML")
    bot.send_message(m.chat.id, text5, parse_mode="HTML")
   


@bot.message_handler(func=lambda m: m.text.startswith('سکوت تایمری'))
def mute_user(m):
    duration = int(m.text.split()[-1])

    date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    until_date = int(date.timestamp())

    bot.restrict_chat_member(
        m.chat.id, m.reply_to_message.from_user.id,
        until_date=until_date,
        can_send_media_messages=False,
        can_send_messages=False,
        can_send_other_messages=False,
        can_send_polls=False
    )
    bot.reply_to(m, f"  کاربر به مدت {duration} دقیقه سکوت شد ")


@bot.message_handler(func=lambda m: m.text.startswith('بن تایمری'))
def mute_user(m):
    duration = int(m.text.split()[-1])

    date = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    until_date = int(date.timestamp())

    bot.ban_chat_member(
        m.chat.id, m.reply_to_message.from_user.id,
        until_date=until_date,

    )
    bot.reply_to(m, f"کاربر به مدت {duration} دقیقه بن شد ")


media = []




@bot.message_handler(func=lambda message: message.text == 'جوک😄')
def random1(message):
    jock = ["آش رشته تنها جایی بود که گیاهان موفق شدن بدون کمک گوشت و خودشون\n\n به تنهایی طعم مطبوعی تولید کنن بقیه تجربه هاشون به شکست مطلق منجر شد", "چوپان دروغگو میمیره توی قبر ازش میپرسن اسمت چیه\n\n میگه دهقان فداکار", "با دختری که میگه “میسیییی” به جای “مرسی” باید درجا قطع رابطه کرد\n\nچون تا بیای براش توضیح بدی که نگو “میسییی” بهت میگه “چلااااااا؟”", "استقاده از آسانسو در فیلم ها چه ایرانی چه خارجی!\n\n یارو باعجله میره سمت آسانسور و فقط دکمشو میزنه بعد از پله ها میره بالا!!", "غضنفر می ره عروسی ‌‌‌ تو عروسی\n\n برف شادی می زنن  سرما می خوره!!", "غضنفر با کلید گوشش رو تمیز می کرده گردنش قفل می کنه!!", "مردی در هوای سرد، اسبی را دید که از\n\n بینی اش بخار بیرون می آمد با خود گفت فهمیدم پس اسب بخار که می گن همینه", "الان یکی زنگ زد گفت: شما!!!!!؟!\n\n منم گفتم: ببخشید اشتباه برداشتم خودش مرد از خنده فردا تشییع جنازشه", "هر کی میگه پول خوشبختی نمیاره پیام بده\n\n شماره حسابمو بدم پولاشو بریزه تو حسابم", "غضنفر به دوستش می گه: می دونستی آب سه تا جن داره؟\n\n دوستش: نه اسمش چیه؟ غضنفر : یکی اکسی جن و دو تا هیدرو جن.!!", "برای یه گوسفند فرق نمی کنه قراره\n\n کباب سلطانی، کالباس یا حلیم بشه سعی میکنه از علف خوردنش لذت ببره.", "می‌دونین اگه یه ماهی تو بانک کار کنه بهش چی می‌گن؟\n\n بهش می‌گن: فیش بانکی.", "به پشهه می گن: چرا زمستون پیداتون نیست؟ می گه:\n\n نه اینکه تابستون ها خیلی برخوردتون خوبه!", "به مرغه می‌گن: می‌تونی روزی پونزده‌ تا\n\n تخم بذاری؟ می‌گه: اون کار رو فقط ج**ده‌های تلاونگ می‌کنن.", "گلبول سفید میره تو خون می‌بینه\n\n همه گولبول‌ها قرمزن می‌گه »ای بابا چرا منو در شریان نذاشتین»", "یک روز دوتا سیاره داشتن دعوا می‌کردن\n\n نپتون می‌گه «آقا ولش کن همیشه حق با مشتریه…»", "می‌دونی کیبوردها چرا هم روزها کار می‌کنن هم شب‌ها؟\n\n چون دوتا شیفت دارن.", "سه نفر رو میندازن جهنم بعد چند روز میان\n\n می‌بینن خاکی و درب و داغونن می‌پرسن\n\n داستان چیه؟ می‌گن: خدایی کار ۳نفر نبود ولی بالاخره خاموشش کردیم.", "خره داشته می‌رفته چشمش به یه\n\n اسب میفته با حسرت می‌گه: ای کاش تحصیلاتم رو ادامه می‌دادم.", "غضنفر هی نگاه به گوشیش میکرده و میخندیده بهش میگن اس ام اس اومده ؟\n\nمیگه آره ، میگن چیه ؟\n\nمیگه یکی هی اس ام اس میده \nLow Battery"]
    random_message = random.choice(jock)
    bot.reply_to(message, random_message)
    

@bot.message_handler(func= lambda message: message.text == 'دانستنی⁉️')
def random2(message):
    messages = [
    "آیا می دانید کهکشان راه شیری 100 میلیون ستاره و یا بیشتر دارد.", "آیا می دانید ستاره دریایی مغز ندارد",  "آیا می دانید مساحت کره زمین 515 میلیون کیلومتر می باشد",  "آیا می دانید چینی ها بیشتر از آمریکایی ها انگلیسی بلدند", "آیا می دانید سیاره زهره گرمترین سیاره است و درجه حرارت آن درجه462 می باشد", "آیا می دانید 33 میلیارد الکترون در هر قطره آب وجود دارد", "آیا می دانید حلزون قادر است سه سال بخوابد", "آیا می دانید کوتاهترین جمله کامل در زبان انگلیسی جمله I am است", "آیا می دانید حیوانی که چشمانش از مغزش بزرگ تر است شتر مرغ می باشد", "آیا می دانید عمر خورشید 5 میلیارد سال است", "آیا می دانید نقره می تواند 650 نوع میکروب را از بین ببرد ومواد ضد عفونی قوی است", "آیا می دانید زبان مقاوم ترین ماهیچه در بدن است", "آیا می دانید پخش موسیقی برای مرغ سبب می شود او بزرگترین تخم را بگذارد", "آیا می دانید عسل تنها غذایی فاسد نشدنی است", "آیا می دانید تمام رگ های خونی بدن 97 هزار کیلومتر است", "اسب های دریایی تنها حیواناتی هستند که در آن ها جنس نر باردار می شود", "آیا می دانید قلب میگو در سرش قرار گرفته است", "آیا می دانید یونانیان باستان از ادرار خود\n\n برای تمیز کردن و سفید کردن دندان های شان استفاده می کردند", "آیا می دانید هشت پا سه قلب در بدنش دارد", "آیا می دانید شیر اسب آبی صورتی رنگ است"]
    random_message = random.choice(messages)
    bot.reply_to(message, random_message)


@bot.message_handler(func=lambda message: message.text == 'بیوگرافی🗨️' )
def random3(message):
    bio = [" <code> میان تمام نداشته‌هایم هنوز «خودی» دارم که سرسختانه پای من ایستاده است.🫂🤍️ </code>", "<code> دِل مَن میگه بِمونو بِساز، غُرورَم میگه وِلِش کُن بِباز:)️ </code>", "<code> بهترین حس ..؟ وقتی که تنهایی و تو آهنگات غرق شدی... </code>", "<code> -عَـقلتو‌ دنبـال ‌کـن، قَـلبت‌ احمقـه.️   </code>", "<code> 𝒂 𝒎𝒊𝒏𝒅 𝒇𝒖𝒍𝒍 𝒐𝒇 𝒖𝒏𝒔𝒂𝒊𝒅 𝒕𝒉𝒊𝒏𝒈𝒔 یه ذهن پر از چیزای نگفته️   </code>", " <code> بی تفاوت به هر تفاوت🕸🕷</code>", " <code> معرفتاشون‌ وصله‌ به‌ منفعت‌‌‌‌؛ </code>", " <code> «بهش نگو رويا، بگو هدف!»‌</code>", " <code> جوری باش که حتی مغزتم منت فکر کردنشو گذاشت خیلی راحت درش بیاری😏️</code>", " <code> گمشده در جنگل متروکه افکار....  </code>", " <code> از لحظه لحظه زندگیت لذت ببر شاید فردایی نباشد..  </code>", " <code> بلاخره یه روزی یه جایی دفتر زندگی منم بسته میشه و راحت میخوابم....  </code>", " <code> گاهی وقتا کلمات مانند شیشه میشند: «اگه سکوت کنی درد داره » «اگه حرف بزنی خونریزی میکنه» </code>", " <code> اما چـہ باید گفتـ... انسان نمایانی ڪ ننگِ نام انسانند🙂  </code>", " <code>-جوانہ باور کرد،درخت شُد!🌱✨.  </code>", " <code> آرامش یعنی نگاه به گذشته و شـــــکر خـــــــدا ، نگاه به آینده و اعتمــــاد به خــــــــــــــدا </code>", " <code> برای کشف اقیانوس های جدید باید جرات ترک ساحل را داشت، این دنیا، دنیای تغییر است نه تقدیر </code>", " <code> خری کِه از پُل گذشتِه باشِه هار میشِه!🖤 </code>", " <code> موفقیت داده نمیشه، بدست میاد🤞🏻🕊 </code>", " <code> خسته ام مثل لاک پشتی که یک خیابان را اشتباه رفته است🐢:) </code> "]
    random_message = random.choice(bio)
    bot.reply_to(message, random_message, parse_mode="HTML")
    bot.send_message(message.chat.id, 'متن به صورت مونو هست و با زدن روی متن کپی میشود')
    

@bot.message_handler(func=lambda message: message.text == 'اصطلاحات انگلیسی🔠')
def random4(message):
    essential = [ "<code> After Blood\n\nخونخواهی و انتقام</code>", "<code> A Busy Body\n\nآدم فوضول </code>", "<code> A Proper Meal\n\nیه غذای درست و حسابی  </code> ", "<code> All In Stitches\n\nاز خنده روده بر شدن </code>", "<code>Appearances Are Deceptive\n\nظاهر افراد فریبنده هست </code>", "<code> A Ray of Sunshine\n\nکورسوی امید</code>", "<code> Are You Sulking?\n\nقهری؟ </code>", "<code> Are You Ticklish\n\nقلقلکی هستی؟ </code>", "<code> As They Say\n\nبه قول معروف... </code>", "<code> At The Eleventh Hour\n\nدقیقه نود (لحظه آخر) </code>", " <code> Beet Red\n\nسرخ شدن از خجالت </code>", " <code> Bend Over Backwards\n\nجون کندن </code>", " <code> Being Broke Hurts!\n\nبی پولی بد دردیه </code>", " <code> Better Late Than Never\n\nدیر رسیدن بهتر از هرگز نرسیدنه </code>", " <code> Blow Hot And Cold\n\nهر دفعه یه سازی میزنه </code>", "<code> Blue In The Face\n\nزبونم مو در آورد </code>", "<code> Bust Hump\n\nبرو گمشو </code>",  "<code> Buy The Farm\n\nنخود هر آشی شدن </code>", "<code> Catch Someone Red Handed\n\nمچ کسی رو گرفتن </code>", "<code> Cat Got Your Tongue?\n\nگربه زبونتو خورده؟ </code>" ]
    random_message = random.choice(essential)
    bot.reply_to(message, random_message, parse_mode="HTML")
    bot.send_message(message.chat.id, 'متن به صورت مونو هست و با زدن روی متن کپی میشود')
    


@bot.message_handler(func=lambda m: m.text == 'جرعت حقیقت❓')
def joraat_haghighat(m): 
    bot.send_message(m.chat.id,           
'1. اگر زندگی ات یک فیلم بود کدام فیلم می شد؟\n\n 2. آیا آلرژی خاصی داری؟\n\n 3. اگر میتوانستی به یک زمان خاص در تاریخ برگردی کدام زمان بود؟\n\n 4. اگر ابر قدرت بودی چه قدرتی داشتی؟\n\n 5. وقتی آلارم گوشیت زنگ میزند بلافاصله بیدار میشوید یا دکمه بعدا را فشار میدهد؟\n\n 6. اولین کاری که هر روز صبح انجام میدی چیه؟\n\n 7. آخرین کاری که هر شب انجام میدی چیه؟\n\n 8. آخرین باری که گریه کردی کی بوده و چرا؟\n\n 9. عجیب ترین کاری که در تنهایی هایت انجام دادی چه بوده؟\n\n 10. بدترین بحثی که در آن شرکت کرده ای چه بوده؟\n\n 11. مسخره ترین لباسی که تابحال پوشیده ای چه بوده؟\n\n 12. اگر می توانستی یک چیز را در خودت تغییر دهی چه چیزی را تغییر می دادی؟\n\n 13. بزرگ ترین رازت چیه؟\n\n 14. چه چیزی باعث خجالتت میشه؟\n\n 15. خجالت آورترین اتفاقی که تاحالا برات افتاده؟\n\n 16. بزرگترین اشتباهی که تاحالا مرتکب شدی؟\n\n 17. توی چه کاری اصلا خوب نیستی؟\n\n 18. بزرگ ترین دروغی که تا حالا گفتی؟\n\n 19. تا حالا توی بازی تقلب کردی؟\n\n 20. عجیب ترین عادتی که داری؟\n\n 21. عجیب ترین غذایی که عاشقشی؟\n\n 22. بزرگ ترین ترس دوران بچگیت؟\n\n 23. پایین ترین نمره ای که توی دانشگاه یا مدرسه گرفتی؟\n\n 24. تا حالا یه چیز گرون قیمت رو شکستی؟\n\n 25. اگه یه دفعه صد میلیون تومن به دست بیاری، چطوری خرجش می کنی؟\n\n 26. بدترین غذایی که تا حالا امتحان کردی؟\n\n 27. خجالت آورترین چیزی که تا حالا توی فضای مجازی پست کردی؟\n\n 28. تا حالا راز دوستت رو به کسی گفتی؟\n\n 29. دوست داری در آینده چندتا بچه داشته باشی؟\n\n 30. اگه قرار باشه تا آخر عمرت فقط یه غذا رو بخوری، چه غذاییه؟\n\n 31. آخرین پیامی که برای دوست صمیمیت ارسال کردی؟\n\n 32. بدترین درد فیزیکی که تا حالا داشتی؟\n\n 33. از لحاظ شخصیتی، بیشتر شبیه مامانتی یا بابات؟\n\n 34. آخرین باری که از کسی عذرخواهی کردی کی بود؟ بابت چه کاری؟\n\n 35. اگه خونت آتش بگیره و فقط بتونی 3 تا چیزو برداری (به غیر از افراد)، چه چیزهایی رو بر می داری؟\n\n 36. توی بچگیات دوست داشتی چه سرگرمی یا ورزشی رو تجربه کنی؟\n\n 37. عجیب ترین کاری که تا حالا توی مکان عمومی انجام دادی؟\n\n 38. آخرین بهانه ای که برای کنسل کردن برنامه هات آوردی؟\n\n 39. بدترین اشتباهی که توی مدرسه یا سر کارت انجام دادی؟\n\n 40. کدوم یکی از اعضای خانوادت خیلی رو اعصابته؟')
    bot.reply_to(m, 'لیست جرعت حقیقت ارسال شد')                                 
                                                                               

@bot.message_handler(commands=['bot'])
def welcome(message):
    bot.reply_to(message,"از منوی زیر در صفحه کلید گزینه ای را انتخاب نمایید:", reply_markup=reply_keyboard)

@bot.message_handler(content_types=['text'])
def handle_all_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text.lower().strip()
    first_name = message.from_user.first_name

    # بررسی لینک و اخطار
    if any(word in text for word in ['http', 'https', 't.me', '@']):
        if not is_admin(chat_id, user_id):
            try:
                bot.delete_message(chat_id, message.message_id)
                user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

                if user_warnings[user_id] == 1:
                    bot.send_message(chat_id, f"⚠️ کاربر {first_name} ارسال لینک 1 از 2 — در صورت تکرار حذف خواهید شد.")
                elif user_warnings[user_id] >= 2:
                    bot.send_message(chat_id, f"⛔️ کاربر {first_name} ارسال لینک 2 از 2 — شما از گروه حذف شدید.")
                    bot.ban_chat_member(chat_id, user_id)

            except Exception as e:
                print(f"خطا در حذف لینک یا بن: {e}")
        return

    # پاسخ به پیام‌های مشخص
    if text == 'شروع':
        bot.reply_to(message, 'سلام من علی بات🤖 هستم\n\nبرای اطلاع از قابلیت‌هام، بنویس «لیست»', parse_mode="HTML")

    elif text == 'مدیریت گروه🤵‍♂️':
        bot.reply_to(message, 'برای استفاده از امکانات مدیریتی، ربات را به گروه اضافه و ادمین کنید.')

    elif text == 'ارتباط با ما📞':
        bot.reply_to(message, 'آیدی سازنده ربات: @AliamA7931')

    elif text == 'ربات':
        username = message.from_user.username or first_name
        bot.send_message(chat_id, f'جانم @{username}، برای شروع بنویس «شروع»', parse_mode="HTML")

    elif text in ['سلام', 'سلام خوبی', 'خوبی', 'خوب هستی', 'چطوری']:
        bot.reply_to(message, 'سلام! حالت چطوره؟')

    elif text == 'چه خبرا':
        bot.reply_to(message, 'خبر سلامتیت، خودت چه خبر؟')

    elif text in ['فدات', 'فدابشم']:
        bot.reply_to(message, 'قربونت عزیز!')

    elif text in ['خداحافظ', 'بای']:
        bot.reply_to(message, 'خدانگهدار!')

    elif text in ['کجایی', 'اهل کجایی']:
        bot.reply_to(message, 'من از سیاره ربات‌ها اومدم!')

    elif text == 'اسمت چیه':
        bot.reply_to(message, 'اسمم علی بات🤖 هست')

    elif text == 'درود':
        bot.reply_to(message, 'درود بر تو گل🌹')

    elif text in ['سلام خاری', 'خاری', 'اره خارمه', 'بد نیمه']:
        bot.reply_to(message, 'خار بووشی!')

    elif text == 'چه خبر':
        bot.reply_to(message, 'سلامتی ته چه خبر')


    elif text == 'منم سلامتی خبری نیه':
        bot.reply_to(message, ' آها همیشه سلامت بوشی')

    elif text == 'گم بواش':
        bot.reply_to(message, 'گم نوومبه شه سره راه ره بلدمه')
        
    elif text == 'گیخار':
        bot.reply_to(message, 'برو مه گی ره بخار')
        
    elif text == 'چیکار کندی':
        bot.reply_to(message, 'چیکار خاستی هاکانم درمه ته جه گپ زمبه😑') 
           
    elif text == 'چیکار کاندی':
        bot.reply_to(message, 'چیکار خاستی هاکانم درمه ته جه گپ زمبه😑') 
        
    elif text == 'کجه دری':
        bot.reply_to(message, 'تلگرام دله درمه دیگه اینتا هم بییه سوال🙄')
        
    elif text == 'ته اسم چیچیه':
        bot.reply_to(message, 'من علی بات🤖هستمه شما مه ره نشناسنی😁')   
                
    elif text == 'ته اسم چیه':
        bot.reply_to(message, 'من علی بات🤖هستمه شما مه ره نشناسنی😁')           

    elif text == 'ربات ته ره دوست دارمه':
        bot.reply_to(message, 'منم ته ره خله دوست دارمه ولی از یه نظر دیگه🙂😊')
        
    elif text == 'ربات ته ره دوست دارمه':
        bot.reply_to(message, 'منم ته ره خله دوست دارمه ولی از یه نظر دیگه🙂😊')
         
    elif text == 'ربات مه جه رل زندی':
        bot.reply_to(message, 'اره ته فدابووشم ناز ره بخارم😁')
        
    elif text == 'کیر':
        bot.set_message_reaction(chat_id=message.chat.id, message_id=message.message_id,  reaction=[ReactionTypeEmoji(emoji='🖕')])
        
    elif text == 'من بورم':
        bot.reply_to(message, 'به سلامت شه هوا ره دار')        
    
    elif text == 'بات':
        Bot_Response = f'جان @{message.from_user.username} مه ره کار داشتی؟\n\n🔸 برای گپ بزوعن با من کلمه <b> «گپ» </b>  ره راهی هاکان'
        bot.send_message(message.chat.id, text=Bot_Response, parse_mode= 'HTML') 
   
    elif text == 'گپ':
        bot.reply_to(message, 'سلام من علی بات🤖 هستمه\n\n برای اطلاع داشتن از مه قابلیت کلمه \n\n <b> «لیست» </b> ره راهی هاکان', parse_mode= 'HTML')
        
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render به PORT مقدار می‌ده
    app.run(host='0.0.0.0', port=port)

#