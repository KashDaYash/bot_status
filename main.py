# (C) @KashDaYash 

from os import getenv
from dotenv import load_dotenv

import time
import datetime
import pytz
import pyrogram

load_dotenv()
# Api Strings From my.telegram.org

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Your Session Strings
SESSION_STRING = getenv("SESSION_STRING")

# Your Bots Username Without '@' With A Space 1 To Another
BOTS = [i.strip() for i in getenv("BOTS").split(' ')]

# Your Username Without '@'
BOT_OWNER = getenv("BOT_OWNER")

# Your Channel Username Without '@'
UPDATE_CHANNEL = getenv("UPDATE_CHANNEL")

# Message Id Of Your Channel Bot Status Message
STATUS_MESSAGE_ID = int(getenv("STATUS_MESSAGE_ID"))

# Time & Limits
TIME = int(getenv("TIME"))

# Restart My Bot
REBOTS = [i.strip() for i in getenv("BOTS").split(' ')]

Alty = pyrogram.Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

def main():
    with Alty:
        while True:
            print("💬 [INFO] Starting To Check Uptime..")
            TEXT = f"<b>👾 @{UPDATE_CHANNEL} Our Bot's Status (Updating Every  {round(TIME / 60)} Hours)</b>\n\n<b>📜 BOTS :</b>\n\n"

            for bot in BOTS:
                print(f"💬 [INFO] Checking @{bot}")

                x = Alty.send_message(bot, '/start')

                time.sleep(15)
                msg = Alty.get_history(bot, 1)[0]

                if x.message_id == msg.message_id:
                    print(f"⚠️ [WARNING] @{bot} Is Down")
                    TEXT += f"❌ - @{bot}\n"
                    Alty.send_message(BOT_OWNER, f"❌ - @{bot} IS DOWN !")

                else:
                    print(f"☑ [INFO] All Good With @{bot}")
                    TEXT += f"✅ - @{bot}\n"
                Alty.read_history(bot)

            utc_now = datetime.datetime.now(pytz.timezone('UTC')).strftime("%I:%M %p %d/%m/%y")
            ma_now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime("%d/%m/%y %I:%M:%S %p")

            TEXT += f"\n⏱ <b>LAST UPDATE :</b>\n\n🌎 UTC : {str(utc_now)}\n🇮🇳 MA : {str(ma_now)}"



            for re in REBOTS:
                print(f"💬 [INFO] Checking @{re}")

                x = Alty.send_message(re, '/restart')

                time.sleep(15)
                msg = Alty.get_history(re, 1)[0]

                if x.message_id == msg.message_id:
                    print(f"⛔ [WARNING] I Can't Restart @{re}")
                    TEXT += f"❌ - @{re}\n"
                    Alty.send_message(BOT_OWNER, f"⛔ - I Can't Restart @{re} !")

                else:
                    print(f"✅ [INFO] Restarted @{re}")
                    Alty.send_message(BOT_OWNER, f"✅ - @{re} #RESTARTED #DONE !")

                Alty.read_history(re)

            Alty.edit_message_text(UPDATE_CHANNEL, STATUS_MESSAGE_ID, text=TEXT, disable_web_page_preview=True, parse_mode="html")
            print(f"[INFO] Everything Done! Sleeping For {round(TIME / 60)} Hours...")
            time.sleep(TIME * 60)

main()
