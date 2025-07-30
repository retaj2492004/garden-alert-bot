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
target_word = "strawberry"

bot = telebot.TeleBot(bot_token)
seen_items = set()

def check_website():
    url = 'https://vulcanvalues.com/grow-a-garden/stock'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('li', class_='bg-gray-900 p-3 rounded-md border border-gray-700 text-white font-medium flex items-center space-x-3')
    
    print(f"عدد العناصر التي تم العثور عليها: {len(items)}")

    for item in items:
    name_elem = item.find('span')
    if name_elem:
        plant_name = name_elem.get_text(strip=True)
        print(f"تم العثور على: {plant_name}")

        if target_word.lower() in plant_name.lower():
            if plant_name not in seen_items:
                seen_items.add(plant_name)
                bot.send_message(chat_id, f"🌱 ظهرت النبتة: {plant_name}!\n{url}")
                print("🚀 تم إرسال رسالة إلى تيليغرام")





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
