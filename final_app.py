import telebot
from pyexpat.errors import messages
from telebot import types
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton)
import time
import datetime
import platform
from datetime import datetime
import jdatetime
import os
from flask import Flask, request
import random
import pytz
from googletrans import Translator
import re



TOKEN = '7579645804:AAF5V1dumlyrbyHj0RQkOZO402la4csirAI'
Channel_1 = '@rap_family1' 
Channel_2 = "@alibotteleg"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


translator = Translator()
user_translation_mode = {}

user_warnings = {}  # دیکشنری برای نگه‌داری اخطار کاربران





 
farsi_to_cuneiform = {
    'ا': '𐎠', 'آ': '𐎠', 'ب': '𐎲', 'پ': '𐎱', 'ت': '𐎫', 'ث': '𐎰', 'تو': '𐎬', 'طو': '𐎬', 'ج': '𐎢', 'جی': '𐎪', 'چ': '𐎨', 'ح': '𐏃', 'خ': '𐎧',
    'د': '𐎭', 'دی': '𐎮', 'دو': '𐎯', 'ذ': '𐏀', 'ر': '𐎼', 'رو': '𐎽', 'ز': '𐏀', 'س': '𐎿', 'ش': '𐎤', 'ص': '𐎿', 'ض': '𐏀', 'ط': '𐎫', 'ظ': '𐏀', 'ع': '𐎠', 'غ': '𐎥', 'ک': '𐎣',
    'کو': '𐎤', 'قو': '𐎦', 'گ': '𐎥', 'م': '𐎶', 'مو': '𐎸', 'می': '𐎷', 'ن': '𐎴', 'نو': '𐎵', 'و': '𐎺', 'وی': '𐎻', 'ه': '𐎱', 'ی': '𐎡',
    'ف': '𐎳', 'ق': '𐎨', 'ل': '𐎾'
}
 
 # تابع تبدیل
def convert_to_cuneiform(text):
    converted = ''.join(farsi_to_cuneiform.get(ch, ch) for ch in text)
    return '\u200F' + converted[::-1]  # ← برعکس کردن + راست‌چین کردن


# شروع
@bot.message_handler(func= lambda m: m.text == 'زبان هخامنشی𐎠')
def hakhmaneshi(message):
    bot.send_message(message.chat.id, "یک متن فارسی بفرست تا برات به خط میخی هخامنشی تبدیل کنم")
    bot.register_next_step_handler(message, handle_text)
    
def handle_text(message):
    original = message.text
    converted = convert_to_cuneiform(original)
    reversed_text = converted[::-1]
    bot.reply_to(message, f"متن میخی:\n\n<code>{reversed_text}</code>", parse_mode="HTML")
    bot.send_message(message.chat.id, 'برای اینکه متن جدیدی را وارد کنید\n\nمجددا کلمه «زبان هخامنشی» را ارسال کنید ')
 

############### translate text #################
def is_english(text):
        return all(ord(c) < 128 for c in text)

# فعال‌سازی حالت ترجمه برای کاربر
@bot.message_handler(func=lambda m: m.text == 'ترجمه متن🔁')
def activate_translation_mode(message):
    user_id = message.from_user.id
    user_translation_mode[user_id] = True
    bot.send_message(message.chat.id, "📝 لطفاً متنی که می‌خوای ترجمه کنم رو ارسال کن")
    bot.register_next_step_handler(message, handle_messages)
    
def handle_messages(message):
    user_id = message.from_user.id
    text = message.text
    
    # حالت ترجمه فعال بود؟
    if user_translation_mode.get(user_id):
        lang = 'fa' if is_english(text) else 'en'
        try:
            result = translator.translate(text, dest=lang)
            bot.send_message(message.chat.id, f"✅ ترجمه:\n\n{result.origin} \n\n⬅️ {result.text}")
        except Exception:
            bot.send_message(message.chat.id, "❌ خطا در ترجمه. لطفاً دوباره امتحان کن.")
        finally:
            user_translation_mode[user_id] = False  # خاموش کردن حالت ترجمه
        return  # جلوگیری از برخورد با بقیه کدها در همین handler




   
user_warnings = {}

@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('پین'))
def pin(m):
    print("دستور پین اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.pin_chat_message(m.chat.id, m.reply_to_message.id)
            bot.reply_to(m, "📌 پیام پین شد")
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
        bot.reply_to(m, "پین پیام حذف شد ☑️")
    else:
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")
  

# بن کاربر
@bot.message_handler(func=lambda m: m.text and m.text.strip().lower().startswith('بن'))
def ban(m):
    print("دستور بن اجرا شد:", m.text)
    if is_admin(m.chat.id, m.from_user.id):
        if m.reply_to_message:
            bot.ban_chat_member(m.chat.id, m.reply_to_message.from_user.id)
            bot.reply_to(m, f"کاربر <b> {m.reply_to_message.from_user.first_name} </b> بن شد 🚫", parse_mode="HTML")
        else:
            bot.reply_to(m, "روی پیام کاربر ریپلای کن")


#### حذف بن و افزودن کاربر به گروه ####
@bot.message_handler(func=lambda m: m.reply_to_message and m.text.lower() == 'افزودن')
def add_back_user(m):
    user_id = m.reply_to_message.from_user.id
    chat_id = m.chat.id

    try:
        # حذف بن کاربر
        bot.unban_chat_member(chat_id, user_id)

        # ساخت لینک دعوت فقط برای یک بار
        invite_link = bot.create_chat_invite_link(chat_id, member_limit=1)

        # ساخت دکمه
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("📥 ورود به گروه", url=invite_link.invite_link)
        markup.add(button)

        # تلاش برای ارسال پیوی به کاربر بن‌شده
        try:
            bot.send_message(user_id,
                f"سلام ✨\nدر گروه <b>«{m.chat.title}»</b> از حالت بن خارج شدی\n\nبرای ورود دوباره، روی دکمه زیر کلیک کن 👇",                                                                                                                    
                reply_markup=markup, parse_mode="HTML")
            bot.reply_to(m, "لینک به پیوی کاربر ارسال شد ✅")
        except:
            # اگر ربات بلاک شده باشه یا استارت نشده باشه
            start_link = f"https://t.me/{bot.get_me().username}?start=start"
            bot.reply_to(m,  f"""❗ کاربر هنوز ربات را استارت نکرده یا پیام‌های خصوصیش بسته هست\n\n1. این لینک را برای کاربر ارسال کن:
➡️ {start_link}
               
2. به او بگو پیام بده یا بنویسه /start """)
            bot.send_message(chat_id, 'حالا دوباره پیامش رو ریپلای کن و بنویس: افزودن ✅')
    except Exception as e:
        bot.reply_to(m, f"❌ خطا در عملیات:\n{e}")
   


# سکوت
@bot.message_handler(func=lambda m: m.text.strip() == 'سکوت')
def mute_forever(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "برای سکوت دائم،\n روی پیام کاربر ریپلای کن ")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "فقط ادمین‌ها می‌تونن سکوت کنن")

    bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(can_send_messages=False)
    )

    bot.reply_to(message, "کاربر به صورت دائم سکوت شد 🔕")




@bot.message_handler(func=lambda m: m.text.startswith('سکوت ') and m.text[6:].isdigit())
def mute_timed(message):
    if not message.reply_to_message:
        return bot.reply_to(message, "برای سکوت زمان‌دار،\n\n روی پیام کاربر ریپلای کن و \nمثلا بنویس: سکوت  5")

    if not is_admin(message.chat.id, message.from_user.id):
        return bot.reply_to(message, "فقط ادمین‌ها می‌تونن سکوت کنن.")

    minutes = int(message.text[6:])
    until = int(time.time()) + (minutes * 60)

    bot.restrict_chat_member(
        chat_id=message.chat.id,
        user_id=message.reply_to_message.from_user.id,
        permissions=types.ChatPermissions(can_send_messages=False),
        until_date=until
    )

    bot.reply_to(message, f"⏱ کاربر<b> {message.reply_to_message.from_user.first_name}</b> به مدت {minutes} دقیقه\nسکوت شد", parse_mode="HTML")




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
            bot.reply_to(m, "سکوت کاربر برداشته شد ✅")
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
            bot.reply_to(m, "کاربر به ادمین🤵‍♂️ارتقا یافت")
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
            bot.reply_to(m, "ادمین برکنار شد 📛")
        else: 
            bot.reply_to(m, "لطفاً روی پیام ریپلای کن.")
            
            
@bot.message_handler(func=lambda m: m.text.lower() == 'لیست')
def show_command_list(message):
    text = (
        "📋  لیست دستورات:\n\n"
        "🤵‍♂️ /Group  ←مدیریت گروه\n\n"
        "🗨️ /Bio  ←بیوگرافی\n\n"
        "😄 /Joke  ←جوک\n\n"
        "🔠 /Terms  ←اصطلاح انگلیسی\n\n"
        "❓ /DareTruth  ←جرأت حقیقت\n\n"
        "𐎠 /Ancient  ←زبان هخامنشی\n\n"
        "⁉️ /Facts  ←دانستنی\n\n"
        "📞 /Contact  ←ارتباط با ما\n\n"
        "🔁 /Translate  ←ترجمه متن\n\n"
    )
    bot.send_message(message.chat.id, text)


            
            
        
# -------------------- توابع کمکی --------------------

def handle_link(text):
    if not text:
        return False
    return any(word in text.lower() for word in ['http', 'https', 't.me', '@'])

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ['administrator', 'creator']
    except:
        return False

def is_user_members(channel, user_id):
    try:
        member = bot.get_chat_member(channel, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
# -------------------- /start --------------------

# هندلر /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if is_user_members(Channel_1, user_id) and is_user_members(Channel_2, user_id):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        keyboard.add(
            types.KeyboardButton('مدیریت گروه🤵‍♂️'),
            types.KeyboardButton('بیوگرافی🗨️'),
            types.KeyboardButton('اصطلاح انگلیسی🔠'),
            types.KeyboardButton('جرعت حقیقت❓'),
            types.KeyboardButton('جوک😄'),
            types.KeyboardButton('زبان هخامنشی𐎠'),
            types.KeyboardButton('دانستنی⁉️'),
            types.KeyboardButton('ارتباط با ما📞'),
            types.KeyboardButton('ترجمه متن🔁')
        )
        bot.send_message(
            chat_id,
            "سلام من علی بات 🤖 هستم\n\nاز منوی زیر در صفحه کلید یکی از قابلیت‌ها رو انتخاب کن👇",
            reply_markup=keyboard
        )
    else:
        # اگر عضو نبود → ساخت دکمه‌های عضویت
        join_btn = types.InlineKeyboardMarkup()
        join_btn.add(
            types.InlineKeyboardButton("عضویت در کانال اول 📢", url="https://t.me/rap_family1"),
            types.InlineKeyboardButton("عضویت در کانال دوم 📢", url="https://t.me/alibotteleg")
        )
        bot.send_message(
            chat_id,
            "توی هر دو کانال عضو نیستی ❌\n\nبرای استفاده از ربات، باید توی هر دو کانال زیر عضو بشی 👇",
            reply_markup=join_btn
        )
        bot.send_message(chat_id, "وقتی عضو شدی، دوباره /start رو بزن.")
     


@bot.message_handler(commands=['Group'])
def group_handler(m):
    bot.send_message(m.chat.id, "برای استفاده از امکانات مدیریتی،\n\n ابتدا ربات را به گروه خود اضافه و سپس ادمین کامل کنید")

@bot.message_handler(commands=['Bio'])
def bio_handler(m):
   bios = [" <code> میان تمام نداشته‌هایم هنوز «خودی» دارم که سرسختانه پای من ایستاده است.🫂🤍️ </code>",
          "<code> دِل مَن میگه بِمونو بِساز، غُرورَم میگه وِلِش کُن بِباز:)️ </code>",
          "<code> بهترین حس ..؟ وقتی که تنهایی و تو آهنگات غرق شدی... </code>",
          "<code> -عَـقلتو‌ دنبـال ‌کـن، قَـلبت‌ احمقـه.️   </code>",
          "<code> 𝒂 𝒎𝒊𝒏𝒅 𝒇𝒖𝒍𝒍 𝒐𝒇 𝒖𝒏𝒔𝒂𝒊𝒅 𝒕𝒉𝒊𝒏𝒈𝒔 یه ذهن پر از چیزای نگفته️   </code>",
          " <code> بی تفاوت به هر تفاوت🕸🕷</code>",
          " <code> معرفتاشون‌ وصله‌ به‌ منفعت‌‌‌‌؛ </code>",
          " <code> «بهش نگو رويا، بگو هدف!»‌</code>",
          " <code> جوری باش که حتی مغزتم منت فکر کردنشو گذاشت خیلی راحت درش بیاری😏️</code>",
          " <code> گمشده در جنگل متروکه افکار....  </code>",
          " <code> از لحظه لحظه زندگیت لذت ببر شاید فردایی نباشد..  </code>",
          " <code> بلاخره یه روزی یه جایی دفتر زندگی منم بسته میشه و راحت میخوابم....  </code>",
          " <code> گاهی وقتا کلمات مانند شیشه میشند: «اگه سکوت کنی درد داره » «اگه حرف بزنی خونریزی میکنه» </code>",
          " <code> اما چـہ باید گفتـ... انسان نمایانی ڪ ننگِ نام انسانند🙂  </code>",
          " <code>-جوانہ باور کرد،درخت شُد!🌱✨.  </code>",
          " <code> آرامش یعنی نگاه به گذشته و شـــــکر خـــــــدا ، نگاه به آینده و اعتمــــاد به خــــــــــــــدا </code>",
          " <code> برای کشف اقیانوس های جدید باید جرات ترک ساحل را داشت، این دنیا، دنیای تغییر است نه تقدیر </code>",
          " <code> خری کِه از پُل گذشتِه باشِه هار میشِه!🖤 </code>",
          " <code> موفقیت داده نمیشه، بدست میاد🤞🏻🕊 </code>",
          " <code> خسته ام مثل لاک پشتی که یک خیابان را اشتباه رفته است🐢:) </code> "]
   bot.send_message(m.chat.id, random.choice(bios), parse_mode="HTML")

@bot.message_handler(commands=['Joke'])
def joke_handler(m):
    jokes = [
       "آش رشته تنها جایی بود که گیاهان موفق شدن بدون کمک گوشت و خودشون\n\n به تنهایی طعم مطبوعی تولید کنن بقیه تجربه هاشون به شکست مطلق منجر شد",
       "چوپان دروغگو میمیره توی قبر ازش میپرسن اسمت چیه\n\n میگه دهقان فداکار",
       "با دختری که میگه “میسیییی” به جای “مرسی” باید درجا قطع رابطه کرد\n\nچون تا بیای براش توضیح بدی که نگو “میسییی” بهت میگه “چلااااااا؟”",
       "استقاده از آسانسو در فیلم ها چه ایرانی چه خارجی!\n\n یارو باعجله میره سمت آسانسور و فقط دکمشو میزنه بعد از پله ها میره بالا!!",
       "غضنفر می ره عروسی ‌‌‌ تو عروسی\n\n برف شادی می زنن  سرما می خوره!!",
       "غضنفر با کلید گوشش رو تمیز می کرده گردنش قفل می کنه!!",
       "مردی در هوای سرد، اسبی را دید که از\n\n بینی اش بخار بیرون می آمد با خود گفت فهمیدم پس اسب بخار که می گن همینه",
       "الان یکی زنگ زد گفت: شما!!!!!؟!\n\n منم گفتم: ببخشید اشتباه برداشتم خودش مرد از خنده فردا تشییع جنازشه",
       "هر کی میگه پول خوشبختی نمیاره پیام بده\n\n شماره حسابمو بدم پولاشو بریزه تو حسابم",
       "غضنفر به دوستش می گه: می دونستی آب سه تا جن داره؟\n\n دوستش: نه اسمش چیه؟ غضنفر : یکی اکسی جن و دو تا هیدرو جن.!!",
       "برای یه گوسفند فرق نمی کنه قراره\n\n کباب سلطانی، کالباس یا حلیم بشه سعی میکنه از علف خوردنش لذت ببره.",
       "می‌دونین اگه یه ماهی تو بانک کار کنه بهش چی می‌گن؟\n\n بهش می‌گن: فیش بانکی.",
       "به پشهه می گن: چرا زمستون پیداتون نیست؟ می گه:\n\n نه اینکه تابستون ها خیلی برخوردتون خوبه!",
       "به مرغه می‌گن: می‌تونی روزی پونزده‌ تا\n\n تخم بذاری؟ می‌گه: اون کار رو فقط ج**ده‌های تلاونگ می‌کنن.",
       "گلبول سفید میره تو خون می‌بینه\n\n همه گولبول‌ها قرمزن می‌گه »ای بابا چرا منو در شریان نذاشتین»",
       "یک روز دوتا سیاره داشتن دعوا می‌کردن\n\n نپتون می‌گه «آقا ولش کن همیشه حق با مشتریه…»",
       "می‌دونی کیبوردها چرا هم روزها کار می‌کنن هم شب‌ها؟\n\n چون دوتا شیفت دارن.",
       "سه نفر رو میندازن جهنم بعد چند روز میان\n\n می‌بینن خاکی و درب و داغونن می‌پرسن\n\n داستان چیه؟ می‌گن: خدایی کار ۳نفر نبود ولی بالاخره خاموشش کردیم.",
       "خره داشته می‌رفته چشمش به یه\n\n اسب میفته با حسرت می‌گه: ای کاش تحصیلاتم رو ادامه می‌دادم.",
       "غضنفر هی نگاه به گوشیش میکرده و میخندیده بهش میگن اس ام اس اومده ؟\n\nمیگه آره ، میگن چیه ؟\n\nمیگه یکی هی اس ام اس میده \nLow Battery"]
    bot.send_message(m.chat.id, random.choice(jokes))

@bot.message_handler(commands=['Terms'])
def terms_handler(m):
    terms = [
      "<code> After Blood\n\nخونخواهی و انتقام</code>",
      "<code> A Busy Body\n\nآدم فوضول </code>",
      "<code> A Proper Meal\n\nیه غذای درست و حسابی  </code> ",
      "<code> All In Stitches\n\nاز خنده روده بر شدن </code>",
      "<code>Appearances Are Deceptive\n\nظاهر افراد فریبنده هست </code>",
      "<code> A Ray of Sunshine\n\nکورسوی امید</code>",
      "<code> Are You Sulking?\n\nقهری؟ </code>",
      "<code> Are You Ticklish\n\nقلقلکی هستی؟ </code>",
      "<code> As They Say\n\nبه قول معروف... </code>",
      "<code> At The Eleventh Hour\n\nدقیقه نود (لحظه آخر) </code>",
      " <code> Beet Red\n\nسرخ شدن از خجالت </code>",
      " <code> Bend Over Backwards\n\nجون کندن </code>",
      " <code> Being Broke Hurts!\n\nبی پولی بد دردیه </code>",
      " <code> Better Late Than Never\n\nدیر رسیدن بهتر از هرگز نرسیدنه </code>",
      " <code> Blow Hot And Cold\n\nهر دفعه یه سازی میزنه </code>",
      "<code> Blue In The Face\n\nزبونم مو در آورد </code>",
      "<code> Bust Hump\n\nبرو گمشو </code>",
      "<code> Buy The Farm\n\nنخود هر آشی شدن </code>",
      "<code> Catch Someone Red Handed\n\nمچ کسی رو گرفتن </code>",
      "<code> Cat Got Your Tongue?\n\nگربه زبونتو خورده؟ </code>" ]
    bot.send_message(m.chat.id, random.choice(terms), parse_mode="HTML")


@bot.message_handler(commands=['DareTruth'])
def dare_handler(m):
    bot.send_message(m.chat.id, '1. اگر زندگی ات یک فیلم بود کدام فیلم می شد؟\n\n 2. آیا آلرژی خاصی داری؟\n\n 3. اگر میتوانستی به یک زمان خاص در تاریخ برگردی کدام زمان بود؟\n\n 4. اگر ابر قدرت بودی چه قدرتی داشتی؟\n\n 5. وقتی آلارم گوشیت زنگ میزند بلافاصله بیدار میشوید یا دکمه بعدا را فشار میدهد؟\n\n 6. اولین کاری که هر روز صبح انجام میدی چیه؟\n\n 7. آخرین کاری که هر شب انجام میدی چیه؟\n\n 8. آخرین باری که گریه کردی کی بوده و چرا؟\n\n 9. عجیب ترین کاری که در تنهایی هایت انجام دادی چه بوده؟\n\n 10. بدترین بحثی که در آن شرکت کرده ای چه بوده؟\n\n 11. مسخره ترین لباسی که تابحال پوشیده ای چه بوده؟\n\n 12. اگر می توانستی یک چیز را در خودت تغییر دهی چه چیزی را تغییر می دادی؟\n\n 13. بزرگ ترین رازت چیه؟\n\n 14. چه چیزی باعث خجالتت میشه؟\n\n 15. خجالت آورترین اتفاقی که تاحالا برات افتاده؟\n\n 16. بزرگترین اشتباهی که تاحالا مرتکب شدی؟\n\n 17. توی چه کاری اصلا خوب نیستی؟\n\n 18. بزرگ ترین دروغی که تا حالا گفتی؟\n\n 19. تا حالا توی بازی تقلب کردی؟\n\n 20. عجیب ترین عادتی که داری؟\n\n 21. عجیب ترین غذایی که عاشقشی؟\n\n 22. بزرگ ترین ترس دوران بچگیت؟\n\n 23. پایین ترین نمره ای که توی دانشگاه یا مدرسه گرفتی؟\n\n 24. تا حالا یه چیز گرون قیمت رو شکستی؟\n\n 25. اگه یه دفعه صد میلیون تومن به دست بیاری، چطوری خرجش می کنی؟\n\n 26. بدترین غذایی که تا حالا امتحان کردی؟\n\n 27. خجالت آورترین چیزی که تا حالا توی فضای مجازی پست کردی؟\n\n 28. تا حالا راز دوستت رو به کسی گفتی؟\n\n 29. دوست داری در آینده چندتا بچه داشته باشی؟\n\n 30. اگه قرار باشه تا آخر عمرت فقط یه غذا رو بخوری، چه غذاییه؟\n\n 31. آخرین پیامی که برای دوست صمیمیت ارسال کردی؟\n\n 32. بدترین درد فیزیکی که تا حالا داشتی؟\n\n 33. از لحاظ شخصیتی، بیشتر شبیه مامانتی یا بابات؟\n\n 34. آخرین باری که از کسی عذرخواهی کردی کی بود؟ بابت چه کاری؟\n\n 35. اگه خونت آتش بگیره و فقط بتونی 3 تا چیزو برداری (به غیر از افراد)، چه چیزهایی رو بر می داری؟\n\n 36. توی بچگیات دوست داشتی چه سرگرمی یا ورزشی رو تجربه کنی؟\n\n 37. عجیب ترین کاری که تا حالا توی مکان عمومی انجام دادی؟\n\n 38. آخرین بهانه ای که برای کنسل کردن برنامه هات آوردی؟\n\n 39. بدترین اشتباهی که توی مدرسه یا سر کارت انجام دادی؟\n\n 40. کدوم یکی از اعضای خانوادت خیلی رو اعصابته؟')
    bot.reply_to(m, 'لیست جرعت حقیقت ارسال شد')                 
          
                     
@bot.message_handler(commands=['Ancient'])
def ancient_handler(m):
     bot.send_message(m.chat.id, "یک متن فارسی بفرست تا برات به خط میخی هخامنشی تبدیل کنم")
     bot.register_next_step_handler(m, handle_text)
    
def handle_text(m):
    original = m.text
    converted = convert_to_cuneiform(original)
    bot.reply_to(m, f"متن میخی:\n\n<code>{converted}</code>", parse_mode="HTML")   
    bot.send_message(m.chat.id, 'برای اینکه متن جدیدی را وارد کنید\n\nمجددا کلمه «زبان هخامنشی» را ارسال کنید ')
 

@bot.message_handler(commands=['Facts'])
def facts_handler(m):
    facts = [
        "آیا می دانید کهکشان راه شیری 100 میلیون ستاره و یا بیشتر دارد.",
        "آیا می دانید ستاره دریایی مغز ندارد",
        "آیا می دانید مساحت کره زمین 515 میلیون کیلومتر می باشد",
        "آیا می دانید چینی ها بیشتر از آمریکایی ها انگلیسی بلدند",
        "آیا می دانید سیاره زهره گرمترین سیاره است و درجه حرارت آن درجه462 می باشد",
        "آیا می دانید 33 میلیارد الکترون در هر قطره آب وجود دارد",
        "آیا می دانید حلزون قادر است سه سال بخوابد",
        "آیا می دانید کوتاهترین جمله کامل در زبان انگلیسی جمله I am است",
        "آیا می دانید حیوانی که چشمانش از مغزش بزرگ تر است شتر مرغ می باشد",
        "آیا می دانید عمر خورشید 5 میلیارد سال است",
        "آیا می دانید نقره می تواند 650 نوع میکروب را از بین ببرد ومواد ضد عفونی قوی است",
        "آیا می دانید زبان مقاوم ترین ماهیچه در بدن است",
        "آیا می دانید پخش موسیقی برای مرغ سبب می شود او بزرگترین تخم را بگذارد",
        "آیا می دانید عسل تنها غذایی فاسد نشدنی است",
        "آیا می دانید تمام رگ های خونی بدن 97 هزار کیلومتر است",
        "اسب های دریایی تنها حیواناتی هستند که در آن ها جنس نر باردار می شود",
        "آیا می دانید قلب میگو در سرش قرار گرفته است",
        "آیا می دانید یونانیان باستان از ادرار خود\n\n برای تمیز کردن و سفید کردن دندان های شان استفاده می کردند",
        "آیا می دانید هشت پا سه قلب در بدنش دارد",
        "آیا می دانید شیر اسب آبی صورتی رنگ است"]
    bot.send_message(m.chat.id, random.choice(facts))


@bot.message_handler(commands=['Contact'])
def contact_handler(m):
    bot.send_message(m.chat.id, "ارتباط با سازنده: @AliamA7931")


@bot.message_handler(commands=['Translate'])
def translate_handler(m):
    user_id = m.from_user.id
    user_translation_mode[user_id] = True
    bot.send_message(m.chat.id, "📝 لطفاً متنی که می‌خوای ترجمه کنم رو ارسال کن")
    bot.register_next_step_handler(m, handle_messages)
    
def handle_messages(m):
    user_id = m.from_user.id
    text = m.text
    
    # حالت ترجمه فعال بود؟
    if user_translation_mode.get(user_id):
        lang = 'fa' if is_english(text) else 'en'
        try:
            result = translator.translate(text, dest=lang)
            bot.send_message(m.chat.id, f"✅ ترجمه:\n\n{result.origin} \n\n⬅️ {result.text}")
        except Exception:
            bot.send_message(m.chat.id, "❌ خطا در ترجمه. لطفاً دوباره امتحان کن.")
        finally:
            user_translation_mode[user_id] = False  # خاموش کردن حالت ترجمه
        return  # جلوگیری از برخورد با بقیه کدها در همین handler


# -------------------- پیام‌های عمومی --------------------

@bot.message_handler(content_types=['text'])
def handle_all_messages(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text or ''
    text = text.lower().strip()
    
    first_name = message.from_user.first_name
    username = message.from_user.username or first_name

    
    if text in ['ربات']:
        bot.reply_to(message, f'جانم @{username}\n\n🔸 برای اطلاع از قابلیت هام کلمه <b>«لیست»</b> رو تایپ کن', parse_mode="HTML")
        return  
    
    if text in ['بات']:
        bot.reply_to(message, f'جان @{username} مِه رِه کار داشتی؟\n\n 🔸 برای اطلاع داشتِن از مِه قابِلیِت کلِمه <b> «لیست» </b> رِه راهی هاکِن', parse_mode="HTML")
        return  
   
    if text in ['ریات', 'روبات', 'رباط']:
            bot.reply_to(message, 'معلم ادبیاتت کی بود🤔\n زنده میخوامش')
            return
        
    if text == 'سلام':
            bot.reply_to(message, 'سلام خوبی عزیزم') 
            return     
        
    if message.chat.type == 'private' or (
        message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id
):  
        if text == 'مدیریت گروه🤵‍♂️':
            bot.reply_to(message, 'برای استفاده از امکانات مدیریتی،\n\n ابتدا ربات را به گروه خود اضافه و سپس ادمین کامل کنید ')

        elif text == 'ارتباط با ما📞':
            bot.reply_to(message, 'آیدی سازنده ربات: @AliamA7931')
            
        elif text == 'جرعت حقیقت❓':
            bot.send_message(chat_id,           
                '1. اگر زندگی ات یک فیلم بود کدام فیلم می شد؟\n\n 2. آیا آلرژی خاصی داری؟\n\n 3. اگر میتوانستی به یک زمان خاص در تاریخ برگردی کدام زمان بود؟\n\n 4. اگر ابر قدرت بودی چه قدرتی داشتی؟\n\n 5. وقتی آلارم گوشیت زنگ میزند بلافاصله بیدار میشوید یا دکمه بعدا را فشار میدهد؟\n\n 6. اولین کاری که هر روز صبح انجام میدی چیه؟\n\n 7. آخرین کاری که هر شب انجام میدی چیه؟\n\n 8. آخرین باری که گریه کردی کی بوده و چرا؟\n\n 9. عجیب ترین کاری که در تنهایی هایت انجام دادی چه بوده؟\n\n 10. بدترین بحثی که در آن شرکت کرده ای چه بوده؟\n\n 11. مسخره ترین لباسی که تابحال پوشیده ای چه بوده؟\n\n 12. اگر می توانستی یک چیز را در خودت تغییر دهی چه چیزی را تغییر می دادی؟\n\n 13. بزرگ ترین رازت چیه؟\n\n 14. چه چیزی باعث خجالتت میشه؟\n\n 15. خجالت آورترین اتفاقی که تاحالا برات افتاده؟\n\n 16. بزرگترین اشتباهی که تاحالا مرتکب شدی؟\n\n 17. توی چه کاری اصلا خوب نیستی؟\n\n 18. بزرگ ترین دروغی که تا حالا گفتی؟\n\n 19. تا حالا توی بازی تقلب کردی؟\n\n 20. عجیب ترین عادتی که داری؟\n\n 21. عجیب ترین غذایی که عاشقشی؟\n\n 22. بزرگ ترین ترس دوران بچگیت؟\n\n 23. پایین ترین نمره ای که توی دانشگاه یا مدرسه گرفتی؟\n\n 24. تا حالا یه چیز گرون قیمت رو شکستی؟\n\n 25. اگه یه دفعه صد میلیون تومن به دست بیاری، چطوری خرجش می کنی؟\n\n 26. بدترین غذایی که تا حالا امتحان کردی؟\n\n 27. خجالت آورترین چیزی که تا حالا توی فضای مجازی پست کردی؟\n\n 28. تا حالا راز دوستت رو به کسی گفتی؟\n\n 29. دوست داری در آینده چندتا بچه داشته باشی؟\n\n 30. اگه قرار باشه تا آخر عمرت فقط یه غذا رو بخوری، چه غذاییه؟\n\n 31. آخرین پیامی که برای دوست صمیمیت ارسال کردی؟\n\n 32. بدترین درد فیزیکی که تا حالا داشتی؟\n\n 33. از لحاظ شخصیتی، بیشتر شبیه مامانتی یا بابات؟\n\n 34. آخرین باری که از کسی عذرخواهی کردی کی بود؟ بابت چه کاری؟\n\n 35. اگه خونت آتش بگیره و فقط بتونی 3 تا چیزو برداری (به غیر از افراد)، چه چیزهایی رو بر می داری؟\n\n 36. توی بچگیات دوست داشتی چه سرگرمی یا ورزشی رو تجربه کنی؟\n\n 37. عجیب ترین کاری که تا حالا توی مکان عمومی انجام دادی؟\n\n 38. آخرین بهانه ای که برای کنسل کردن برنامه هات آوردی؟\n\n 39. بدترین اشتباهی که توی مدرسه یا سر کارت انجام دادی؟\n\n 40. کدوم یکی از اعضای خانوادت خیلی رو اعصابته؟')
            bot.reply_to(message, 'لیست جرعت حقیقت❓ارسال شد')                           

        elif text == 'جوک😄':
            jock = ["آش رشته تنها جایی بود که گیاهان موفق شدن بدون کمک گوشت و خودشون\n\n به تنهایی طعم مطبوعی تولید کنن بقیه تجربه هاشون به شکست مطلق منجر شد", "چوپان دروغگو میمیره توی قبر ازش میپرسن اسمت چیه\n\n میگه دهقان فداکار", "با دختری که میگه “میسیییی” به جای “مرسی” باید درجا قطع رابطه کرد\n\nچون تا بیای براش توضیح بدی که نگو “میسییی” بهت میگه “چلااااااا؟”", "استقاده از آسانسو در فیلم ها چه ایرانی چه خارجی!\n\n یارو باعجله میره سمت آسانسور و فقط دکمشو میزنه بعد از پله ها میره بالا!!", "غضنفر می ره عروسی ‌‌‌ تو عروسی\n\n برف شادی می زنن  سرما می خوره!!", "غضنفر با کلید گوشش رو تمیز می کرده گردنش قفل می کنه!!", "مردی در هوای سرد، اسبی را دید که از\n\n بینی اش بخار بیرون می آمد با خود گفت فهمیدم پس اسب بخار که می گن همینه", "الان یکی زنگ زد گفت: شما!!!!!؟!\n\n منم گفتم: ببخشید اشتباه برداشتم خودش مرد از خنده فردا تشییع جنازشه", "هر کی میگه پول خوشبختی نمیاره پیام بده\n\n شماره حسابمو بدم پولاشو بریزه تو حسابم", "غضنفر به دوستش می گه: می دونستی آب سه تا جن داره؟\n\n دوستش: نه اسمش چیه؟ غضنفر : یکی اکسی جن و دو تا هیدرو جن.!!", "برای یه گوسفند فرق نمی کنه قراره\n\n کباب سلطانی، کالباس یا حلیم بشه سعی میکنه از علف خوردنش لذت ببره.", "می‌دونین اگه یه ماهی تو بانک کار کنه بهش چی می‌گن؟\n\n بهش می‌گن: فیش بانکی.", "به پشهه می گن: چرا زمستون پیداتون نیست؟ می گه:\n\n نه اینکه تابستون ها خیلی برخوردتون خوبه!", "به مرغه می‌گن: می‌تونی روزی پونزده‌ تا\n\n تخم بذاری؟ می‌گه: اون کار رو فقط ج**ده‌های تلاونگ می‌کنن.", "گلبول سفید میره تو خون می‌بینه\n\n همه گولبول‌ها قرمزن می‌گه »ای بابا چرا منو در شریان نذاشتین»", "یک روز دوتا سیاره داشتن دعوا می‌کردن\n\n نپتون می‌گه «آقا ولش کن همیشه حق با مشتریه…»", "می‌دونی کیبوردها چرا هم روزها کار می‌کنن هم شب‌ها؟\n\n چون دوتا شیفت دارن.", "سه نفر رو میندازن جهنم بعد چند روز میان\n\n می‌بینن خاکی و درب و داغونن می‌پرسن\n\n داستان چیه؟ می‌گن: خدایی کار ۳نفر نبود ولی بالاخره خاموشش کردیم.", "خره داشته می‌رفته چشمش به یه\n\n اسب میفته با حسرت می‌گه: ای کاش تحصیلاتم رو ادامه می‌دادم.", "غضنفر هی نگاه به گوشیش میکرده و میخندیده بهش میگن اس ام اس اومده ؟\n\nمیگه آره ، میگن چیه ؟\n\nمیگه یکی هی اس ام اس میده \nLow Battery"]
            random_message = random.choice(jock)
            bot.reply_to(message, random_message)

        elif text == 'بیوگرافی🗨️':
            bio = [" <code> میان تمام نداشته‌هایم هنوز «خودی» دارم که سرسختانه پای من ایستاده است.🫂🤍️ </code>", "<code> دِل مَن میگه بِمونو بِساز، غُرورَم میگه وِلِش کُن بِباز:)️ </code>", "<code> بهترین حس ..؟ وقتی که تنهایی و تو آهنگات غرق شدی... </code>", "<code> -عَـقلتو‌ دنبـال ‌کـن، قَـلبت‌ احمقـه.️   </code>", "<code> 𝒂 𝒎𝒊𝒏𝒅 𝒇𝒖𝒍𝒍 𝒐𝒇 𝒖𝒏𝒔𝒂𝒊𝒅 𝒕𝒉𝒊𝒏𝒈𝒔 یه ذهن پر از چیزای نگفته️   </code>", " <code> بی تفاوت به هر تفاوت🕸🕷</code>", " <code> معرفتاشون‌ وصله‌ به‌ منفعت‌‌‌‌؛ </code>", " <code> «بهش نگو رويا، بگو هدف!»‌</code>", " <code> جوری باش که حتی مغزتم منت فکر کردنشو گذاشت خیلی راحت درش بیاری😏️</code>", " <code> گمشده در جنگل متروکه افکار....  </code>", " <code> از لحظه لحظه زندگیت لذت ببر شاید فردایی نباشد..  </code>", " <code> بلاخره یه روزی یه جایی دفتر زندگی منم بسته میشه و راحت میخوابم....  </code>", " <code> گاهی وقتا کلمات مانند شیشه میشند: «اگه سکوت کنی درد داره » «اگه حرف بزنی خونریزی میکنه» </code>", " <code> اما چـہ باید گفتـ... انسان نمایانی ڪ ننگِ نام انسانند🙂  </code>", " <code>-جوانہ باور کرد،درخت شُد!🌱✨.  </code>", " <code> آرامش یعنی نگاه به گذشته و شـــــکر خـــــــدا ، نگاه به آینده و اعتمــــاد به خــــــــــــــدا </code>", " <code> برای کشف اقیانوس های جدید باید جرات ترک ساحل را داشت، این دنیا، دنیای تغییر است نه تقدیر </code>", " <code> خری کِه از پُل گذشتِه باشِه هار میشِه!🖤 </code>", " <code> موفقیت داده نمیشه، بدست میاد🤞🏻🕊 </code>", " <code> خسته ام مثل لاک پشتی که یک خیابان را اشتباه رفته است🐢:) </code> "]
            random_message = random.choice(bio)
            bot.reply_to(message, random_message, parse_mode="HTML")
            bot.send_message(message.chat.id, 'برای کپی کردن ❐ روی متن بزنید')

        elif text == 'اصطلاح انگلیسی🔠':
            essential = [ "<code> After Blood\n\nخونخواهی و انتقام</code>", "<code> A Busy Body\n\nآدم فوضول </code>", "<code> A Proper Meal\n\nیه غذای درست و حسابی  </code> ", "<code> All In Stitches\n\nاز خنده روده بر شدن </code>", "<code>Appearances Are Deceptive\n\nظاهر افراد فریبنده هست </code>", "<code> A Ray of Sunshine\n\nکورسوی امید</code>", "<code> Are You Sulking?\n\nقهری؟ </code>", "<code> Are You Ticklish\n\nقلقلکی هستی؟ </code>", "<code> As They Say\n\nبه قول معروف... </code>", "<code> At The Eleventh Hour\n\nدقیقه نود (لحظه آخر) </code>", " <code> Beet Red\n\nسرخ شدن از خجالت </code>", " <code> Bend Over Backwards\n\nجون کندن </code>", " <code> Being Broke Hurts!\n\nبی پولی بد دردیه </code>", " <code> Better Late Than Never\n\nدیر رسیدن بهتر از هرگز نرسیدنه </code>", " <code> Blow Hot And Cold\n\nهر دفعه یه سازی میزنه </code>", "<code> Blue In The Face\n\nزبونم مو در آورد </code>", "<code> Bust Hump\n\nبرو گمشو </code>",  "<code> Buy The Farm\n\nنخود هر آشی شدن </code>", "<code> Catch Someone Red Handed\n\nمچ کسی رو گرفتن </code>", "<code> Cat Got Your Tongue?\n\nگربه زبونتو خورده؟ </code>" ]
            random_message = random.choice(essential)
            bot.reply_to(message, random_message, parse_mode="HTML")
            bot.send_message(message.chat.id, 'برای کپی کردن ❐ روی متن بزنید')

        elif text == 'دانستنی⁉️':
            messages = [
        "آیا می دانید کهکشان راه شیری 100 میلیون ستاره و یا بیشتر دارد.", "آیا می دانید ستاره دریایی مغز ندارد",  "آیا می دانید مساحت کره زمین 515 میلیون کیلومتر می باشد",  "آیا می دانید چینی ها بیشتر از آمریکایی ها انگلیسی بلدند", "آیا می دانید سیاره زهره گرمترین سیاره است و درجه حرارت آن درجه462 می باشد", "آیا می دانید 33 میلیارد الکترون در هر قطره آب وجود دارد", "آیا می دانید حلزون قادر است سه سال بخوابد", "آیا می دانید کوتاهترین جمله کامل در زبان انگلیسی جمله I am است", "آیا می دانید حیوانی که چشمانش از مغزش بزرگ تر است شتر مرغ می باشد", "آیا می دانید عمر خورشید 5 میلیارد سال است", "آیا می دانید نقره می تواند 650 نوع میکروب را از بین ببرد ومواد ضد عفونی قوی است", "آیا می دانید زبان مقاوم ترین ماهیچه در بدن است", "آیا می دانید پخش موسیقی برای مرغ سبب می شود او بزرگترین تخم را بگذارد", "آیا می دانید عسل تنها غذایی فاسد نشدنی است", "آیا می دانید تمام رگ های خونی بدن 97 هزار کیلومتر است", "اسب های دریایی تنها حیواناتی هستند که در آن ها جنس نر باردار می شود", "آیا می دانید قلب میگو در سرش قرار گرفته است", "آیا می دانید یونانیان باستان از ادرار خود\n\n برای تمیز کردن و سفید کردن دندان های شان استفاده می کردند", "آیا می دانید هشت پا سه قلب در بدنش دارد", "آیا می دانید شیر اسب آبی صورتی رنگ است"]
            random_message = random.choice(messages)
            bot.reply_to(message, random_message)

       
        elif text in ['سلام خوبی', 'خوبی', 'خوب هستی', 'چطوری']:
            bot.reply_to(message, 'سلام خوبم حال خودت خوبه؟')
            
       

        elif text == 'چه خبرا':
            bot.reply_to(message, 'خبر سلامتیت، خودت چه خبر؟')

        elif text in ['فدات', 'فدابشم']:
            bot.reply_to(message, 'قربونت عزیز❤️')

        elif text in ['خداحافظ', 'بای']:
            bot.reply_to(message, 'خدانگهدار👋')

        elif text in ['اهل کجایی']:
            bot.reply_to(message, 'من از سیاره ربات‌ها اومدم!')
            
        elif text == 'کجایی':
            bot.reply_to(message, 'تو تلگرام منتظر پیامتم😊')    

        elif text == 'اسمت چیه':
            bot.reply_to(message, 'اسمم علی بات🤖 هست')

        elif text == 'درود':
            bot.reply_to(message, 'درود بر تو گل🌹')
            
        elif text in ['فدات خوبی', 'فدات تو خوبی']:
            bot.reply_to(message, 'قربونت برم خوبم شکر')     

        elif text in ['شکر خوبم', 'خوبم شکر']:
            bot.reply_to(message, 'خداروشکر همیشه خوب باشی')
        
        elif text in ['خوبم فدات', 'فدات خوبم']:
            bot.reply_to(message, 'نشی شکر که خوبی😊')
        
    #### Mazani Lang ####
        elif text in ['سلام خاری', 'خاری', 'ربات خاری']:
            bot.reply_to(message, 'خارِمه تِه خاری')

        elif text in ['ممنون ته خاری', 'مرسی ته خاری', 'اره ته خاری']:
            bot.reply_to(message, 'اَرِه خار هَستِمِه')
        
        elif text in ['چه خبر', 'ربات چه خبر', 'شکر چه خبر']:
            bot.reply_to(message, 'سِلامِتی تِه چه خَبِر')

        elif text == 'منم سلامتی خبری نییه':
            bot.reply_to(message, ' آها همیشه سِلامِت بوشی')

        elif text == 'گم بواش':
            bot.reply_to(message, 'گوم نَوومبه شِه سِرِه راه رِه بَلِدِمه')

        elif text == 'گیخار':
            bot.reply_to(message, 'بِرو مِه گی رِه بَخار')
            
        elif text in ['گی بخار', 'گی بخر']:
            bot.reply_to(message, 'بَخاردِنی نیی تِه رِه بَخارِم😄')    

        elif text in ['چیکار کندی', 'چیکار کاندی']:
            bot.reply_to(message, 'چیکار خاستی هاکانِم دَرمه تِه جِه گَپ زَمبه😑')

        elif text in ['کجه دری', 'کاجه دری']:
            bot.reply_to(message, 'تِلِگرام دِله دَرمه دیگه اینتا هم بَییه سوال🙄')

        elif text in ['ته اسم چیه', 'ته اسم چیچیه']:
            bot.reply_to(message, 'مِن علی بات🤖هَستِمه شِما مِه رِه نِشناسِنی😁')

        elif text in ['ربات ته ره دوست دارمه', 'ربات دوست دارمه']:
            bot.reply_to(message, 'مِنِم تِه رِه خَله دوست دارمه ولی از یه نَظِر دیگه🙂')

        elif text in ['ربات مه جه رل زندی', 'ربات مه جا رل زندی', 'مه جه رل زندی', 'مه جا رل زندی']:
            bot.reply_to(message, 'اَرِه تِه فِدابَووشِم ناز رِه بَخارِم😁')

        elif text == 'من بورم':
            bot.reply_to(message, 'به سِلامِت شِه هِوا رِه دار')
        
        elif text in ['خارمه ته خاری', 'خارمه ته چی', 'شکر ته خار هستی', 'شکر ته خاری']:
            bot.reply_to(message, 'مِنِم خارِمه خَلِه ممنون🙏')
        
        elif text in ['بد نیمه ته خاری', 'بد نیمه ته چی', 'بد نیمه']:
            bot.reply_to(message, 'خار بَووشی اَره خِدا رِه شُکر')    

        elif text in ['ته فدا بووشم', 'فدا بووشم', 'ته دا بووم']:
            bot.reply_to(message, 'نَووشی بَمونی ارزش دارنی')
        
        elif text in ['شکر خارمه', 'خارمه شکر']:
            bot.reply_to(message, 'شکر همیشه خار بوشی') 
        
        elif text in ['فدات خارمه','قربونت خارمه', 'فدا خارمه']:
            bot.reply_to(message, 'خارِه خوشحال بَییمه که خار هستی')
    
        elif text in ['ربات عشق منی', 'ربات عشقی']:
            bot.reply_to(message, 'تِه فِدا دوسِت دارمه قلبی☺️🫀')       
    
    if text in ['پین', 'حذف پین', 'بن', 'حذف بن', 'سکوت', 'حذف سکوت', 'افزودن ادمین', 'حذف ادمین', 'سکوت ', 'لیست', 'افزودن']:
        return

 # حذف پیام های حاوی کلمات زشت
    bad_words = ['کیر', 'کص','کونی', 'کس' 'جق', 'جق زدن', 'به تخمم', 'حروم زاده',
    'کص نگو', 'خایه', 'بی ناموس', 'کونکش', 'به کیرم', 'حرومی',
    'خارتو گاییدم', 'کص خارت', 'کص مغز', 'کیری', 'کیر بخور', 'کیرم',
    'کسکش', 'کیرم', 'کیرت', 'خار کصده', 'کون', 'کص مار',
    'مادر جنده', 'پدر جنده', 'مادرتو', 'پدرتو', 'ممه',
    'جنده', 'کیر خور', 'کص خر', 'کیر خر', 'حروم لقمه','تخمی',
    'گاییدم', 'گاییدن', 'میکنمت', 'بکنمت', 'کردمت', 'گاییدمت',
    'شل ناموس', 'کاصم', 'کاسم', 'کاص', 'کاس', 'کاص مار', 'کونده'
    'تخم سگ', 'تخم حروم', 'ننه جنده', 'ننه کصده', 'ننه کونده', 'زن کصده',
    'زن کاصده','پدر سگ', 'سگ پدر', 'مادر سگ', 'زن جنده', 'زنتو گاییدم', 'زنتو کردم',
    ]
    whitelist = ['کسی', 'کسیو', 'کسی‌که']  
    
    for word in bad_words:
        if word in text and not any(w in text for w in whitelist):
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(chat_id, "🚫 پیام نامناسب حذف شد")
            break
   
 
  
    
    # بررسی وجود لینک در پیام
    if re.search(r"(https?://|t\.me/)", text):
        # در پیوی فقط حذف پیام بدون اخطار
        if message.chat.type == 'private':
            try:
                bot.delete_message(chat_id, message.message_id)
            except:
                pass
            return

        # در گروه یا سوپرگروه
        elif message.chat.type in ['group', 'supergroup']:
            is_admin = False
            try:
                admins = bot.get_chat_administrators(chat_id)
                is_admin = any(admin.user.id == user_id for admin in admins)
            except:
                pass  # اگر نتونست بررسی کنه، فرض می‌گیریم که کاربر ادمین نیست

            if not is_admin:
                try:
                    bot.delete_message(chat_id, message.message_id)
                except:
                    pass

                # ثبت اخطار و برخورد
                user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

                if user_warnings[user_id] == 1:
                    bot.send_message(chat_id, f"⚠️ کاربر @{message.from_user.username or 'بی‌نام'} (ارسال لینک 1 از 2)\n\nلینک ممنوع هست 🚫")
                elif user_warnings[user_id] >= 2:
                    bot.send_message(chat_id, f"⛔️ کاربر @{message.from_user.username or 'بی‌نام'} (ارسال لینک 2 از 2)\n\nاز گروه حذف شد 🚮")
                    try:
                        bot.ban_chat_member(chat_id, user_id)
                    except:
                        pass

           

   
    
    
    
    
    
    
               

  

weekday_names = {
    'Saturday': 'شنبه',
    'Sunday': 'یکشنبه',
    'Monday': 'دوشنبه',
    'Tuesday': 'سه‌شنبه',
    'Wednesday': 'چهارشنبه',
    'Thursday': 'پنجشنبه',
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
        weekday_en = shamsi_time.strftime('%A')
        month_en = shamsi_time.strftime('%B')

        weekday_fa = weekday_names.get(weekday_en, weekday_en)
        month_fa = month_names.get(month_en, month_en)
        date_str = f"{shamsi_time.day} {month_fa} {shamsi_time.year}"
        time_str = shamsi_time.strftime('%H:%M:%S')
        response = f"{weekday_fa} {date_str}\n\nزمان: {time_str}"

        group_name = message.chat.title or "گپ"

        # بررسی نام → اگر نبود، از username استفاده کن
        display_name = new_member.first_name if new_member.first_name else f"@{new_member.username or 'کاربر'}"

        bot.send_message(
            message.chat.id,
            f"درود بر<b> {display_name}</b> عزیز 🌟\n\n"
            f"به گروه<b> «{group_name}»</b>\nخوش اومدی ✨❤️\n\n"
            f"امروز: {response}",
            parse_mode="HTML"
        )


@bot.message_handler(content_types=['left_chat_member'])
def left_user(message):
    left_user = message.left_chat_member

    # فقط اگر کاربر خودش ترک کرده باشه
    if message.from_user.id == left_user.id:
        bot.reply_to(message, "بودی خوش نبودی فراموش 👋")




@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
        bot.process_new_updates([update])
        return '', 200
    return 'Invalid', 403

@app.route('/')
def index():
    return "ربات فعاله 🤖", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render به PORT مقدار می‌ده
    app.run(host='0.0.0.0', port=port)
