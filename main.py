import time
import threading
import requests
from bs4 import BeautifulSoup
import telebot
from flask import Flask
import os

# إعداد Flask
app = Flask(__name__)

# إعدادات البوت
bot_token = os.getenv("BOT_TOKEN")  # ضع التوكن كمتغير بيئي في Render
chat_id = int(os.getenv("CHAT_ID"))  # ضع رقم الشات كمتغير بيئي في Render
bot = telebot.TeleBot(bot_token)

# الكلمة المستهدفة
TARGET = "strawberry"

# لحفظ النباتات التي أُرسلت سابقاً
seen_items = set()

# رابط الموقع
URL = "https://arcaiuz.com/grow-a-garden-stock"

# الدالة التي تفحص الموقع
def check_website():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("li", class_="bg-gray-900 p-3 rounded-md border border-gray-700 text-white font-medium flex items-center space-x-3")

        for item in items:
            span = item.find("span")
            if span:
                plant_name = span.get_text(strip=True).lower()
                if TARGET in plant_name and plant_name not in seen_items:
                    seen_items.add(plant_name)
                    bot.send_message(chat_id, f"🌱 ظهرت النبتة: {plant_name.capitalize()}!\n{URL}")
                    print(f"✅ تم إرسال: {plant_name}")
    except Exception as e:
        print(f"🚨 خطأ في الفحص: {e}")

# تشغيل الفحص كل دقيقة
def run_checker():
    while True:
        check_website()
        time.sleep(10)

# صفحة رئيسية بسيطة
@app.route("/")
def home():
    return "Bot is running."

# التشغيل
if __name__ == '__main__':
    threading.Thread(target=run_checker).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
