# (C) @KashDaYash 

from os import getenv
from dotenv import load_dotenv

import time
import datetime
import pytz
import pyrogram

load_dotenv()
# Api Strings From my.telegram.org

API_ID = int(getenv("API_ID", None))
API_HASH = getenv("API_HASH", None)

# Your Session Strings
SESSION = getenv("SESSION_STRING", None)

# Your Bots Username Without '@' With A Space 1 To Another
BOTS = [i.strip() for i in getenv("BOTS", None).split(' ')]

# Your Username Without '@'
BOT_OWNER = getenv("BOT_OWNER", None)

# Your Channel Username Without '@'
UPDATE_CHANNEL = getenv("UPDATE_CHANNEL", None)

# Message Id Of Your Channel Bot Status Message
STATUS_MESSAGE_ID = int(getenv("STATUS_MESSAGE_ID", None))

# Time & Limits
TIME = int(getenv("TIME", None))

# Restart My Bot
REBOTS = [i.strip() for i in getenv("BOTS", None).split(' ')]

app = pyrogram.Client(SESSION, api_id=API_ID, api_hash=API_HASH)

def main():
    with app:
        while True:
            print("💬 [INFO] Starting To Check Uptime..")
            TEXT = f"<b>👾 @{UPDATE_CHANNEL} Our Bot's Status (Updating Every  {round(TIME / 60)} Hours)</b>\n\n<b>📜 BOTS :</b>\n\n"

            for bot in BOTS:
                print(f"💬 [INFO] Checking @{bot}")

                x = app.send_message(bot, '/start')

                time.sleep(15)
                msg = app.get_history(bot, 1)[0]

                if x.message_id == msg.message_id:
                    print(f"⚠️ [WARNING] @{bot} Is Down")
                    TEXT += f"❌ - @{bot}\n"
                    app.send_message(BOT_OWNER, f"❌ - @{bot} IS DOWN !")

                else:
                    print(f"☑ [INFO] All Good With @{bot}")
                    TEXT += f"✅ - @{bot}\n"
                app.read_history(bot)

            utc_now = datetime.datetime.now(pytz.timezone('UTC')).strftime("%I:%M %p %d/%m/%y")
            ma_now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%y %I:%M:%S %p")

            TEXT += f"\n⏱ <b>LAST UPDATE :</b>\n\n🌎 UTC : {str(utc_now)}\n🇮🇳 MA : {str(ma_now)}"



            for re in REBOTS:
                print(f"💬 [INFO] Checking @{re}")

                x = app.send_message(re, '/restart')

                time.sleep(15)
                msg = app.get_history(re, 1)[0]

                if x.message_id == msg.message_id:
                    print(f"⛔ [WARNING] I Can't Restart @{re}")
                    TEXT += f"❌ - @{re}\n"
                    app.send_message(BOT_OWNER, f"⛔ - I Can't Restart @{re} !")

                else:
                    print(f"✅ [INFO] Restarted @{re}")
                    app.send_message(BOT_OWNER, f"✅ - @{re} #RESTARTED #DONE !")

                app.read_history(re)

            app.edit_message_text(UPDATE_CHANNEL, STATUS_MESSAGE_ID, text=TEXT, disable_web_page_preview=True, parse_mode="html")
            print(f"[INFO] Everything Done! Sleeping For {round(TIME / 60)} Hours...")
            time.sleep(TIME * 60)

main()
