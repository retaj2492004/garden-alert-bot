import os
import time
import threading
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import telebot
from flask import Flask

# إعداد التوكن و الشات
bot_token = os.getenv('BOT_TOKEN') or 'حط_التوكن_هون_لو_بدك'
chat_id = int(os.getenv('CHAT_ID') or 123456789)

# هدف البوت
target_word = "strawberry".lower()
seen_items = set()

# تيليغرام
bot = telebot.TeleBot(bot_token)

# تثبيت الكروم درايفر تلقائياً
chromedriver_autoinstaller.install()

# إعدادات Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.binary_location = "/usr/bin/chromium-browser"

driver = webdriver.Chrome(options=chrome_options)

# وظيفة الفحص
def check_website():
    url = 'https://arcaiuz.com/grow-a-garden-stock'
    driver.get(url)
    time.sleep(5)  # انتظار تحميل الصفحة

    items = driver.find_elements('css selector', 'li.bg-gray-900')
    print(f"🚀 عدد العناصر: {len(items)}")

    for item in items:
        text = item.text.lower()
        print("📦 عنصر:", text)
        if target_word in text and text not in seen_items:
            seen_items.add(text)
            bot.send_message(chat_id, f"🌱 ظهرت النبتة: {text}\n{url}")
            print("✅ أُرسلت رسالة!")

# تكرار الفحص
def run_checker():
    while True:
        try:
            check_website()
        except Exception as e:
            print("❌ خطأ:", e)
        time.sleep(300)  # كل 5 دقائق

# Flask لواجهة بسيطة
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت يعمل ويبحث عن Strawberry..."

if __name__ == '__main__':
    threading.Thread(target=run_checker).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
