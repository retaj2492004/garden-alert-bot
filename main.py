import requests
from bs4 import BeautifulSoup
import time
import telebot
import threading
from flask import Flask
import os

app = Flask(__name__)

bot_token = os.getenv('8338398375:AAEkYrjh8ynQkjRtNsXhHR9KSP9mEVw2-Tw')  # حط توكن بوت تيليغرام في متغير بيئة BOT_TOKEN
chat_id = int(os.getenv('1639846336'))  # رقم الشات في متغير CHAT_ID (رقم فقط)
target_plant = "Strawberry"  # الكلمة المستهدفة

bot = telebot.TeleBot(bot_token)
seen_plants = set()

def check_website():
    url = 'https://www.gamersberg.com/grow-a-garden/stock'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    product_divs = soup.find_all('div', class_='bg-gradient-to-br')

    print(f"🧪 Found {len(product_divs)} items")

    for div in product_divs:
        name_div = div.find('div', class_='text-xs sm:text-sm font-semibold text-white/90 mb-1.5 truncate px-0.5')
        if name_div:
            plant_name = name_div.get_text(strip=True)
            print(f"Checking: {plant_name}")

            if target_plant.lower() in plant_name.lower():
                if plant_name not in seen_plants:
                    seen_plants.add(plant_name)
                    bot.send_message(chat_id, f"🌱 The plant appeared: {plant_name}!\n{url}")
                    print("🚀 Sent Telegram message!")

def run_checker():
    while True:
        try:
            check_website()
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(60)  # كل دقيقة

@app.route('/')
def home():
    return "Bot is running ✔️"

if __name__ == '__main__':
    threading.Thread(target=run_checker, daemon=True).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
