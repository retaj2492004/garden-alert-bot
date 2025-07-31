import os
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import telebot
from flask import Flask

# إعدادات التوكن ورقم الشات من متغيرات البيئة
bot_token = os.getenv('BOT_TOKEN')
chat_id = int(os.getenv('CHAT_ID'))

target_word = "strawberry".lower()
seen_items = set()

bot = telebot.TeleBot(bot_token)

# إعدادات كروم لـ Selenium (headless)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# مسار ملف كروم على رندر (بعد تثبيته)
chrome_options.binary_location = "/usr/bin/google-chrome-stable"

# إنشاء الدرايفر
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def check_website():
    url = 'https://arcaiuz.com/grow-a-garden-stock'
    driver.get(url)
    time.sleep(5)  # ننتظر تحميل الصفحة جافاسكربت

    items = driver.find_elements('css selector', 'li.bg-gray-900')
    print(f"🚀 عدد العناصر: {len(items)}")

    for item in items:
        text = item.text.lower()
        print("📦 عنصر:", text)
        if target_word in text and text not in seen_items:
            seen_items.add(text)
            bot.send_message(chat_id, f"🌱 ظهرت النبتة: {text}\n{url}")
            print("✅ أُرسلت رسالة!")

def run_checker():
    while True:
        try:
            check_website()
        except Exception as e:
            print("❌ خطأ:", e)
        time.sleep(20)  # كل 5 دقائق

# تطبيق Flask لصفحة بسيطة
app = Flask(__name__)

@app.route('/')
def home():
    return "البوت شغال ✔️"

if __name__ == '__main__':
    threading.Thread(target=run_checker).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
