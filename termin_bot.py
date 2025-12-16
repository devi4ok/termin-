import time
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))

URL = "https://tempus-termine.com/termine/index.php?anr=92&sna=T1c38f0e7667ea6ba43472ad2e1d542fc&action=open&page=standortauswahl&tasks=11761&kuerzel=TERMIN&schlangen=2-5"

CHECK_INTERVAL = 180

bot = Bot(token=BOT_TOKEN)

def check_appointments():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers, timeout=20)
    text = BeautifulSoup(r.text, "html.parser").get_text()
    return "Keine Termine verfügbar" not in text

def main():
    bot.send_message(CHAT_ID, "🤖 Бот запущено на сервері (24/7)")
    notified = False

    while True:
        try:
            if check_appointments():
                if not notified:
                    bot.send_message(
                        CHAT_ID,
                        "🚗❗ ЗʼЯВИВСЯ ВІЛЬНИЙ ТЕРМІН!\n\n" + URL
                    )
                    notified = True
            else:
                notified = False
        except Exception as e:
            bot.send_message(CHAT_ID, f"⚠️ Помилка: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
