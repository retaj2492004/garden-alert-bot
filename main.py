import time
import threading
import requests
from bs4 import BeautifulSoup
import telebot
from flask import Flask
import os

app = Flask(__name__)

bot_token = '8338398375:AAEkYrjh8ynQkjRtNsXhHR9KSP9mEVw2-Tw'
chat_id = 1639846336
target_word = 'Strawberry'

bot = telebot.TeleBot(bot_token)
seen_items = set()

def check_website():
    url = 'https://vulcanvalues.com/grow-a-garden/stock'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='item-card')
    print(f"تم العثور على {len(items)} عناصر في الصفحة")

    for item in items:
        name_elem = item.find('h2')
        if name_elem:
            print("وجدت نبتة:", name_elem.text)
            if target_word.lower() in name_elem.text.lower():
                print("النبتة المطلوبة موجودة!")
                if name_elem.text not in seen_items:
                    seen_items.add(name_elem.text)
                    bot.send_message(chat_id, f"🌱 ظهرت النبتة: {name_elem.text}!\n{url}")
                    print("تم إرسال رسالة تليغرام")



def run_checker():
    while True:
        try:
            check_website()
        except Exception as e:
            print("خطأ:", e)
        time.sleep(60)

@app.route('/')
def home():
    return "البوت شغال ✔️"

if __name__ == '__main__':
    threading.Thread(target=run_checker).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
