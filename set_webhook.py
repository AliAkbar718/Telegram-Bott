import requests

TOKEN = '7579645804:AAHt5O6hHdXtdigsQQ-WMGiIm7cJexySTVc'  # اینجا توکن رباتت
URL = 'https://telegram-bott-mdb1.onrender.com'  # اینجا آدرس دقیق دامنه یا ngrok

response = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL}")
print(response.text)